import os
import shutil
import glob
import re
import csv
from datetime import date, timedelta
import pandas as pd
from dataclasses import dataclass
from py_dss_interface import DSS

@dataclass(kw_only=True)
class BDGD2OpenDSSYearlyModel:
    """
    Workflow class to convert BDGD-generated OpenDSS models with 36 representative 
    daily cases into a single 8760 (yearly) base case OpenDSS model.
    """

    _dss: DSS
    dss_model_folder: str

    def __post_init__(self):
        self.dss_model_folder = os.path.abspath(self.dss_model_folder)
        if not os.path.isdir(self.dss_model_folder):
            raise FileNotFoundError(f"Folder not found: {self.dss_model_folder}")

    @property
    def dss(self) -> DSS:
        return self._dss

    def _find_files(self, pattern: str):
        files = []
        for f in os.listdir(self.dss_model_folder):
            if re.match(pattern, f, re.IGNORECASE):
                files.append(os.path.join(self.dss_model_folder, f))
        return files

    def _parse_contagem_dias(self):
        csv_folder = os.path.join(self.dss_model_folder, "csv_files")
        if not os.path.isdir(csv_folder):
            raise FileNotFoundError(f"csv_files folder not found in {self.dss_model_folder}")
            
        csv_files = [f for f in os.listdir(csv_folder) if f.lower().startswith("contagem_dias") and f.lower().endswith(".csv")]
        if not csv_files:
            raise FileNotFoundError(f"contagem_dias CSV not found in {csv_folder}")
            
        csv_path = os.path.join(csv_folder, csv_files[0])
        
        day_counts = {}
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Expecting columns: Mês, DU, SA, DO
                # Handle possible whitespace or different casing
                row_cleaned = {k.strip(): v.strip() for k, v in row.items()}
                # Find month col
                month_col = next((k for k in row_cleaned.keys() if 'm' in k.lower() and 's' in k.lower()), None)
                if not month_col:
                    month_col = list(row_cleaned.keys())[0]
                    
                month = int(row_cleaned[month_col])
                du = int(float(row_cleaned.get('DU', 0)))
                sa = int(float(row_cleaned.get('SA', 0)))
                do = int(float(row_cleaned.get('DO', 0)))
                
                day_counts[month] = {
                    'DU': du,
                    'SA': sa,
                    'DO': do,
                    'total': du + sa + do
                }
        return day_counts

    def _get_month_boundaries(self, calendar_dict):
        month_boundaries = {}
        current_hour = 0
        for m in range(1, 13):
            if m in calendar_dict:
                days_in_month = len(calendar_dict[m])
                hours_in_month = days_in_month * 24
                month_boundaries[m] = (current_hour, current_hour + hours_in_month)
                current_hour += hours_in_month
        return month_boundaries

    def _build_calendar(self, day_counts):
        calendar_dict = {}
        # Infer leap year if Feb has 29 days total
        year = 2024 if day_counts.get(2, {}).get('total', 28) == 29 else 2023
        
        for month in range(1, 13):
            if month not in day_counts:
                continue
            
            target_du = day_counts[month]['DU']
            target_sa = day_counts[month]['SA']
            target_do = day_counts[month]['DO']
            
            standard_month = []
            d = date(year, month, 1)
            while d.month == month:
                if d.weekday() < 5:
                    standard_month.append('DU')
                elif d.weekday() == 5:
                    standard_month.append('SA')
                else:
                    standard_month.append('DO')
                d += timedelta(days=1)
                
            counts = {'DU': standard_month.count('DU'), 'SA': standard_month.count('SA'), 'DO': standard_month.count('DO')}
            target = {'DU': target_du, 'SA': target_sa, 'DO': target_do}
            
            for day_type in ['DU', 'SA', 'DO']:
                while counts[day_type] > target[day_type]:
                    for other_type in ['DU', 'SA', 'DO']:
                        if counts[other_type] < target[other_type]:
                            # swap
                            try:
                                idx = standard_month.index(day_type)
                                standard_month[idx] = other_type
                                counts[day_type] -= 1
                                counts[other_type] += 1
                                break
                            except ValueError:
                                pass
                                
            calendar_dict[month] = standard_month
            
        return calendar_dict

    def _parse_curvacarga(self):
        curva_files = self._find_files(r"CurvaCarga_.*\.dss$")
        if not curva_files:
            raise FileNotFoundError("CurvaCarga DSS file not found.")
            
        shapes_24h = {}
        with open(curva_files[0], 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().lower().startswith("new \"loadshape.") or line.strip().lower().startswith("new loadshape."):
                    # New "Loadshape.RES_1_DU" 24 1 mult=(0.56, 0.57, ...)
                    name_match = re.search(r'loadshape\.([^"\s]+)', line, re.IGNORECASE)
                    mult_match = re.search(r'mult\s*=\s*\(([^)]+)\)', line, re.IGNORECASE)
                    
                    if name_match and mult_match:
                        name = name_match.group(1)
                        mults = [float(x.strip()) for x in mult_match.group(1).split(',')]
                        shapes_24h[name] = mults
        return shapes_24h

    def _process_loads(self, prefix, calendar_dict, shapes_24h):
        files = self._find_files(rf"{prefix}_(DU|SA|DO)(\d{{2}})_.*\.dss$")
        loads = {}
        
        for file in files:
            match = re.search(rf"{prefix}_(DU|SA|DO)(\d{{2}})_", os.path.basename(file), re.IGNORECASE)
            if not match: continue
            day_type = match.group(1).upper()
            month = int(match.group(2))
            
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    line_strip = line.strip()
                    if line_strip.lower().startswith("new \"load.") or line_strip.lower().startswith("new load."):
                        name_match = re.search(r'new\s+"?load\.([^"\s]+)"?', line_strip, re.IGNORECASE)
                        kw_match = re.search(r'kw\s*=\s*([\d\.]+)', line_strip, re.IGNORECASE)
                        daily_match = re.search(r'daily\s*=\s*"?([^"\s]+)"?', line_strip, re.IGNORECASE)
                        
                        if name_match and kw_match and daily_match:
                            name = name_match.group(1)
                            kw = float(kw_match.group(1))
                            daily = daily_match.group(1)
                            
                            if name not in loads:
                                loads[name] = {'def': line_strip}
                            if month not in loads[name]:
                                loads[name][month] = {}
                            loads[name][month][day_type] = {'kw': kw, 'daily': daily}

        final_loads = {}
        for name, data in loads.items():
            curve = []
            for month in range(1, 13):
                if month not in calendar_dict: continue
                for day_type in calendar_dict[month]:
                    if month in data and day_type in data[month]:
                        kw = data[month][day_type]['kw']
                        shape_name = data[month][day_type]['daily']
                        shape_mults = shapes_24h.get(shape_name, [0.0]*24)
                    else:
                        kw = 0.0
                        shape_mults = [0.0]*24
                        
                    for m in shape_mults:
                        curve.append(kw * m)
                        
            max_kw = max(curve) if len(curve) > 0 else 0.0
            if max_kw > 0:
                norm_curve = [c / max_kw for c in curve]
            else:
                norm_curve = [0.0] * len(curve)
                
            final_loads[name] = {
                'max_kw': max_kw,
                'curve': norm_curve,
                'template': data['def']
            }
            
        return final_loads

    def _write_cargas(self, path, loads):
        with open(path, 'w', encoding='utf-8') as f:
            for name, data in loads.items():
                line = data['template']
                # Replace kw
                line = re.sub(r'(kw\s*=\s*)([\d\.]+)', fr'\g<1>{data["max_kw"]:.6f}', line, flags=re.IGNORECASE)
                # Replace daily with yearly
                line = re.sub(r'(daily\s*=\s*)"?([^"\s]+)"?', fr'yearly="{name}_8760"', line, flags=re.IGNORECASE)
                f.write(line + '\n')

    def _write_curvas(self, output_folder, bt_loads, mt_loads):
        import array
        loadshapes_dir = os.path.join(output_folder, "loadshapes")
        os.makedirs(loadshapes_dir, exist_ok=True)
        
        path = os.path.join(output_folder, "CurvaCarga.dss")
        with open(path, 'w', encoding='utf-8') as f:
            for loads in [bt_loads, mt_loads]:
                for name, data in loads.items():
                    curve = data['curve']
                    pts = len(curve)
                    
                    sng_filename = f"{name}_8760.sng"
                    sng_path = os.path.join(loadshapes_dir, sng_filename)
                    with open(sng_path, 'wb') as bin_f:
                        float_array = array.array('f', curve)
                        float_array.tofile(bin_f)
                    
                    f.write(f'New "Loadshape.{name}_8760" npts={pts} interval=1 sngfile="loadshapes/{sng_filename}"\n')

    def _write_master_and_copy_grid(self, output_folder: str, total_hours: int, add_nt_monthly_redirects: bool = False, tolerance_pf: float = 0.0001, max_iterations_pf: int = 15):
        master_files = self._find_files(r"^Master_.*\.dss$")
        if not master_files:
            raise FileNotFoundError(f"No Master file found in {self.dss_model_folder}")
            
        base_master = master_files[0]
        grid_files_to_copy = []
        
        new_master_path = os.path.join(output_folder, "master.dss")
        with open(base_master, 'r', encoding='utf-8') as fin, open(new_master_path, 'w', encoding='utf-8') as fout:
            wrote_new_loads = False
            wrote_pf_settings = False
            for line in fin:
                line_strip = line.strip()
                
                if re.match(r'^set\s+tolerance\s*=', line_strip, re.IGNORECASE):
                    continue
                if re.match(r'^set\s+maxiterations\s*=', line_strip, re.IGNORECASE) or re.match(r'^set\s+maxi\s*=', line_strip, re.IGNORECASE):
                    continue
                
                # Check for redirects
                if re.match(r'^!?\s*(?:redirect|compile)\s+', line_strip, re.IGNORECASE):
                    file_match = re.search(r'(?:redirect|compile)\s+"?([^"\s]+)"?', line_strip, re.IGNORECASE)
                    if file_match:
                        fname = file_match.group(1)
                        lower_fname = fname.lower()
                        if lower_fname.startswith("cargasbt") or lower_fname.startswith("cargasmt") or lower_fname.startswith("curvacarga"):
                            if not wrote_new_loads:
                                fout.write('\n! --- New 8760 Files ---\n')
                                fout.write('Redirect "CurvaCarga.dss"\n')
                                fout.write('Redirect "CargaBT.dss"\n')
                                fout.write('Redirect "CargaMT.dss"\n')
                                if add_nt_monthly_redirects:
                                    fout.write('Redirect "CargaBT_monthly_energy_adjustment.dss"\n')
                                    fout.write('Redirect "CargaMT_monthly_energy_adjustment.dss"\n')
                                fout.write('\n')
                                wrote_new_loads = True
                            continue  # Skip the old ones
                        else:
                            if (lower_fname.startswith("gd_bt") or lower_fname.startswith("gd_mt")) and line_strip.startswith('!'):
                                continue
                            grid_files_to_copy.append(fname)
                            fout.write(line)
                elif re.match(r'^buscoords\s+', line_strip, re.IGNORECASE):
                    file_match = re.search(r'buscoords\s+"?([^"\s]+)"?', line_strip, re.IGNORECASE)
                    if file_match:
                        grid_files_to_copy.append(file_match.group(1))
                    fout.write(line)
                elif re.match(r'^set\s+mode\s*=\s*daily', line_strip, re.IGNORECASE):
                    # We change daily to yearly, because we renamed the property to `yearly=` in the load definitions.
                    fout.write(line.replace("daily", "yearly").replace("Daily", "Yearly"))
                    fout.write(f"Set number = {total_hours}\n")
                    fout.write(f"New monitor.timesteps element=vsource.source terminal=1 mode=5\n")
                elif re.match(r'^!?\s*solve', line_strip, re.IGNORECASE):
                    if not wrote_pf_settings:
                        fout.write(f"set tolerance={tolerance_pf}\n")
                        fout.write(f"set maxi={max_iterations_pf}\n")
                        wrote_pf_settings = True
                    fout.write(line)
                else:
                    fout.write(line)
                    
        for fname in grid_files_to_copy:
            src = os.path.join(self.dss_model_folder, fname)
            dst = os.path.join(output_folder, fname)
            if os.path.exists(src):
                shutil.copy2(src, dst)

    def _create_loading_info(self, output_folder, calendar_dict, tolerance_pf: float = 0.0001, max_iterations_pf: int = 15):
        from py_dss_toolkit.dss_tools.dss_tools import dss_tools
        
        master_dss = os.path.join(output_folder, "master.dss")
        dss = self._dss
        dss_tools.update_dss(dss)
        dss.text(f"compile [{master_dss}]")
        
        dss.solution.tolerance = tolerance_pf
        dss.solution.max_iterations = max_iterations_pf
        
        dss_tools.model.add_line_in_vsource(add_meter=True, add_monitors=True)
        dss.text("solve")
        if not dss.solution.converged:
            raise RuntimeError(f"Power flow did not converge! "
                               f"Current max_iterations is {dss.solution.max_iterations} and tolerance is {dss.solution.tolerance}. "
                               f"You can try to change the maxiteration for the power flow (suggested: between 30 and 50) "
                               f"before changing the tolerance, or increase the tolerance by 10 times.")
        
        dss.monitors.name = "monitor_feeder_head_pq"
        header = dss.monitors.header
        
        kw_channels = [i + 1 for i, h in enumerate(header) if "kW" in h]
        
        total_kw = [0.0] * dss.monitors.sample_count
        for ch in kw_channels:
            data = dss.monitors.channel(ch)
            for i in range(len(total_kw)):
                if i < len(data):
                    total_kw[i] += data[i]
                    
        month_boundaries = self._get_month_boundaries(calendar_dict)
                
        if not total_kw:
            return
            
        global_peak_val = max(total_kw)
        global_peak_ts = total_kw.index(global_peak_val) + 1 # 1-indexed timestep is more readable
        global_offpeak_val = min(total_kw)
        global_offpeak_ts = total_kw.index(global_offpeak_val) + 1
        
        summary = [
            {"Scope": "Global", 
             "Start hour": 1, "End hour": len(total_kw),
             "Peak Value (kW)": round(global_peak_val, 2), "Peak Timestep": global_peak_ts,
             "Off-Peak Value (kW)": round(global_offpeak_val, 2), "Off-Peak Timestep": global_offpeak_ts}
        ]
        
        for m in range(1, 13):
            if m in month_boundaries:
                start, end = month_boundaries[m]
                month_data = total_kw[start:end]
                if month_data:
                    m_peak_val = max(month_data)
                    m_peak_ts = month_data.index(m_peak_val) + start + 1
                    m_offpeak_val = min(month_data)
                    m_offpeak_ts = month_data.index(m_offpeak_val) + start + 1
                    
                    summary.append({
                        "Scope": f"Month {m}",
                        "Start hour": start + 1,
                        "End hour": end,
                        "Peak Value (kW)": round(m_peak_val, 2),
                        "Peak Timestep": m_peak_ts,
                        "Off-Peak Value (kW)": round(m_offpeak_val, 2),
                        "Off-Peak Timestep": m_offpeak_ts
                    })
                    
        csv_path = os.path.join(output_folder, "loading_info.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["Scope", "Start hour", "End hour", "Peak Value (kW)", "Peak Timestep", "Off-Peak Value (kW)", "Off-Peak Timestep"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary:
                writer.writerow(row)
        print(f"Loading info CSV created at: {csv_path}")

    def execute_base_case(self, output_folder: str = None, create_loading_info_file: bool = True, tolerance_pf: float = 0.0001, max_iterations_pf: int = 15):
        if output_folder is None:
            folder_name = os.path.basename(self.dss_model_folder)
            output_folder = os.path.join(self.dss_model_folder, f"{folder_name}_8760_base_case")
            
        output_folder = os.path.abspath(output_folder)
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder, ignore_errors=True)
        os.makedirs(output_folder, exist_ok=True)
        
        day_counts = self._parse_contagem_dias()
        calendar_dict = self._build_calendar(day_counts)
        shapes_24h = self._parse_curvacarga()
        
        bt_loads = self._process_loads("CargasBT", calendar_dict, shapes_24h)
        mt_loads = self._process_loads("CargasMT", calendar_dict, shapes_24h)
        
        self._write_cargas(os.path.join(output_folder, "CargaBT.dss"), bt_loads)
        self._write_cargas(os.path.join(output_folder, "CargaMT.dss"), mt_loads)
        self._write_curvas(output_folder, bt_loads, mt_loads)
        
        total_days = sum(data['total'] for data in day_counts.values())
        total_hours = total_days * 24
        self._write_master_and_copy_grid(output_folder, total_hours, tolerance_pf=tolerance_pf, max_iterations_pf=max_iterations_pf)
        
        print(f"8760 Base Case generation complete. Output saved to: {output_folder}")
        
        if create_loading_info_file:
            print("Running simulation to create loading info file...")
            self._create_loading_info(output_folder, calendar_dict, tolerance_pf=tolerance_pf, max_iterations_pf=max_iterations_pf)

    def execute_monthly_energy_case(
        self,
        output_folder: str = None,
        tolerance_kwh_per_month: float = 100.0,
        lv_energy_share: float = 1.0,
        max_iterations: int = 20,
        create_loading_info_file: bool = True,
        tolerance_pf: float = 0.0001,
        max_iterations_pf: int = 15,
    ):
        import array
        
        self._dss.text("clear")
        
        if output_folder is None:
            folder_name = os.path.basename(self.dss_model_folder)
            output_folder = os.path.join(self.dss_model_folder, f"{folder_name}_8760_monthly_energy_case")
            
        output_folder = os.path.abspath(output_folder)
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder, ignore_errors=True)
        os.makedirs(output_folder, exist_ok=True)
        
        # 1. Base case setup
        day_counts = self._parse_contagem_dias()
        calendar_dict = self._build_calendar(day_counts)
        month_boundaries = self._get_month_boundaries(calendar_dict)
        shapes_24h = self._parse_curvacarga()
        
        bt_loads = self._process_loads("CargasBT", calendar_dict, shapes_24h)
        mt_loads = self._process_loads("CargasMT", calendar_dict, shapes_24h)
        
        self._write_cargas(os.path.join(output_folder, "CargaBT.dss"), bt_loads)
        self._write_cargas(os.path.join(output_folder, "CargaMT.dss"), mt_loads)
        self._write_curvas(output_folder, bt_loads, mt_loads)
        
        total_days = sum(data['total'] for data in day_counts.values())
        total_hours = total_days * 24
        
        self._write_master_and_copy_grid(output_folder, total_hours, add_nt_monthly_redirects=True, tolerance_pf=tolerance_pf, max_iterations_pf=max_iterations_pf)
        
        # 2. Extract target energy from CircMT_ per month
        csv_folder = os.path.join(self.dss_model_folder, "csv_files")
        circ_mt_files = [f for f in os.listdir(csv_folder) if f.lower().startswith("circmt") and f.lower().endswith(".csv")]
        if not circ_mt_files:
            raise FileNotFoundError("CircMT CSV not found.")
        circ_mt_path = os.path.join(csv_folder, circ_mt_files[0])
        
        df_circ = pd.read_csv(circ_mt_path)
        target_kwh_m = {}
        for m in range(1, 13):
            col_name = f"EnerCirc{m:02d}_MWh"
            if col_name in df_circ.columns:
                target_kwh_m[m] = df_circ[col_name].sum() * 1000.0
            else:
                target_kwh_m[m] = 0.0
                
        # 3. Calculate original base energies and create zeroed NT loadshapes
        loadshapes_dir = os.path.join(output_folder, "loadshapes")
        os.makedirs(loadshapes_dir, exist_ok=True)
        
        nt_bt_loads = []
        nt_mt_loads = []
        
        # We will keep track of NT load states
        # nt_loads_info[load_name] = {"Type": ..., "Base_Energy_m": {m: value}, "shape_sum_m": {m: value}, "Base_shape": [], "NT_Energy_m": {m: 0.0}, "NT_shape": [0.0]*8760}
        nt_loads_info = {}
        
        total_lv_energy_m = {m: 0.0 for m in range(1, 13)}
        total_mv_energy_m = {m: 0.0 for m in range(1, 13)}
        
        zero_shape = [0.0] * total_hours
        zero_array = array.array('f', zero_shape)
        
        def process_nt_loads(loads_dict, load_type, nt_list):
            for k, v in loads_dict.items():
                original_kw = v['max_kw']
                base_shape = v['curve']
                
                info = {
                    "Type": load_type,
                    "Base_Energy_m": {},
                    "shape_sum_m": {},
                    "Base_shape": base_shape,
                    "NT_Energy_m": {m: 0.0 for m in range(1, 13)},
                    "NT_shape": list(zero_shape)
                }
                
                for m in range(1, 13):
                    if m in month_boundaries:
                        start, end = month_boundaries[m]
                        m_shape = base_shape[start:end]
                        shape_sum = sum(m_shape)
                        base_energy = original_kw * shape_sum
                        info["Base_Energy_m"][m] = base_energy
                        info["shape_sum_m"][m] = shape_sum
                        
                        if load_type == "LV":
                            total_lv_energy_m[m] += base_energy
                        else:
                            total_mv_energy_m[m] += base_energy
                            
                nt_loads_info[k] = info
                
                # Create load and loadshape definition
                line = v['template']
                line = re.sub(fr'(?i)(Load\.{re.escape(k)})', fr'\1_NT', line)
                line = re.sub(r'(kw\s*=\s*)"?([^"\s]+)"?', '', line, flags=re.IGNORECASE)
                line = re.sub(r'((?:daily|yearly)\s*=\s*)"?([^"\s]+)"?', fr'yearly="{k}_NT_8760"', line, flags=re.IGNORECASE)
                
                # mult=(0) ensures OpenDSS allocates the memory array without throwing Warning 482
                ls_def = f'New "Loadshape.{k}_NT_8760" npts={total_hours} interval=1 UseActual=Yes mult=(0)'
                nt_list.append(ls_def)
                nt_list.append(line)

        if lv_energy_share > 0:
            process_nt_loads(bt_loads, "LV", nt_bt_loads)
        if lv_energy_share < 1.0:
            process_nt_loads(mt_loads, "MV", nt_mt_loads)
        with open(os.path.join(output_folder, "CargaBT_monthly_energy_adjustment.dss"), 'w') as f:
            f.write("\n".join(nt_bt_loads))
        with open(os.path.join(output_folder, "CargaMT_monthly_energy_adjustment.dss"), 'w') as f:
            f.write("\n".join(nt_mt_loads))
            
        # 4. Iterative Process
        master_dss = os.path.join(output_folder, "master.dss")
        dss = self._dss
        dss.text(f"compile [{master_dss}]")
        dss.solution.tolerance = tolerance_pf
        dss.solution.max_iterations = max_iterations_pf
        
        iteration_history = []
        
        for m in range(1, 13):
            if m not in month_boundaries:
                continue
                
            start, end = month_boundaries[m]
            hours_in_month = end - start
            
            print(f"\n--- Month {m} ---")
            
            for iteration in range(1, max_iterations + 1):
                dss.text(f"set hour={start - 1}")
                dss.text(f"set number={hours_in_month}")
                dss.meters.first()
                dss.meters.reset()
                dss.text("solve")
                if not dss.solution.converged:
                    raise RuntimeError(f"Power flow did not converge during Month {m}, Iteration {iteration}. "
                                       f"Current max_iterations is {dss.solution.max_iterations} and tolerance is {dss.solution.tolerance}. "
                                       f"You can try to change the maxiteration for the power flow (suggested: between 30 and 50) "
                                       f"before changing the tolerance, or increase the tolerance by 10 times.")
                
                dss.meters.first()
                sim_kwh = dss.meters.register_values[0]
                tgt_kwh = target_kwh_m[m]
                diff_kwh = tgt_kwh - sim_kwh
                
                hist_record = {"Month": m, "Iteration": iteration, "Sim_M": sim_kwh, "Tgt_M": tgt_kwh, "Diff_M": diff_kwh}
                iteration_history.append(hist_record)
                
                print(f"Iter {iteration}: Target={tgt_kwh:.2f}, Simulated={sim_kwh:.2f}, Diff={diff_kwh:.2f}")
                
                if abs(diff_kwh) <= tolerance_kwh_per_month:
                    print(f"Month {m} converged in {iteration} iterations!")
                    break

                lv_alloc_m = diff_kwh * lv_energy_share
                mv_alloc_m = diff_kwh * (1.0 - lv_energy_share)
                
                # Distribute diff to NT loads for this month
                for k, info in nt_loads_info.items():
                    l_type = info["Type"]
                    base_e = info["Base_Energy_m"].get(m, 0.0)
                    
                    load_alloc = 0.0
                    if l_type == "LV" and total_lv_energy_m[m] > 0 and base_e > 0:
                        share = base_e / total_lv_energy_m[m]
                        load_alloc = lv_alloc_m * share
                    elif l_type == "MV" and total_mv_energy_m[m] > 0 and base_e > 0:
                        share = base_e / total_mv_energy_m[m]
                        load_alloc = mv_alloc_m * share
                    
                    current_nt_e = info["NT_Energy_m"][m]
                    new_nt_e = current_nt_e + load_alloc
                    info["NT_Energy_m"][m] = new_nt_e
                    
                    # Update loadshape array for this month
                    nt_shape = info["NT_shape"]
                    base_shape = info["Base_shape"]
                    shape_sum = info["shape_sum_m"].get(m, 0.0)
                    
                    if shape_sum > 0:
                        multiplier = info["NT_Energy_m"][m] / shape_sum
                        for h in range(start, end):
                            nt_shape[h] = base_shape[h] * multiplier
                            
                    mult_str = " ".join(f"{v:.6f}" for v in nt_shape)
                    dss.text(f"edit loadshape.{k}_NT_8760 mult=({mult_str})")
                
        # 5. Overwrite the final NT files with actual shapes
        final_nt_bt = []
        final_nt_mt = []
        
        for k, info in nt_loads_info.items():
            nt_shape = info["NT_shape"]
            l_type = info["Type"]
            
            sng_filename = f"{k}_NT_8760.sng"
            sng_path = os.path.join(loadshapes_dir, sng_filename)
            with open(sng_path, 'wb') as bin_f:
                float_array = array.array('f', nt_shape)
                float_array.tofile(bin_f)
                
            # Rewrite load definition
            if l_type == "LV":
                base_loads = bt_loads
                target_list = final_nt_bt
            else:
                base_loads = mt_loads
                target_list = final_nt_mt
                
            v = base_loads[k]
            line = v['template']
            line = re.sub(fr'(?i)(Load\.{re.escape(k)})', fr'\1_NT', line)
            line = re.sub(r'(kw\s*=\s*)"?([^"\s]+)"?', '', line, flags=re.IGNORECASE)
            line = re.sub(r'((?:daily|yearly)\s*=\s*)"?([^"\s]+)"?', fr'yearly="{k}_NT_8760"', line, flags=re.IGNORECASE)
            
            ls_def = f'New "Loadshape.{k}_NT_8760" npts={total_hours} interval=1 UseActual=Yes sngfile="loadshapes/{sng_filename}"'
            target_list.append(ls_def)
            target_list.append(line)
            
        with open(os.path.join(output_folder, "CargaBT_monthly_energy_adjustment.dss"), 'w') as f:
            f.write("\n".join(final_nt_bt))
        with open(os.path.join(output_folder, "CargaMT_monthly_energy_adjustment.dss"), 'w') as f:
            f.write("\n".join(final_nt_mt))
                
        # Generate energies CSV
        final_energies = []
        for k, info in nt_loads_info.items():
            row = {"Load": k, "Type": info["Type"]}
            for m in range(1, 13):
                if m in month_boundaries:
                    row[f"Base_Energy_M{m}"] = info["Base_Energy_m"][m]
                    row[f"NT_Energy_M{m}"] = info["NT_Energy_m"][m]
            final_energies.append(row)
            
        df_energies = pd.DataFrame(final_energies)
        df_energies.to_csv(os.path.join(output_folder, "monthly_load_energies.csv"), index=False)
        
        df_hist = pd.DataFrame(iteration_history)
        df_hist.to_csv(os.path.join(output_folder, "iteration_history.csv"), index=False)
        print(f"Monthly Energy Allocation complete. History saved.")
        
        if create_loading_info_file:
            print("Running simulation to create loading info file...")
            self._create_loading_info(output_folder, calendar_dict, tolerance_pf=tolerance_pf, max_iterations_pf=max_iterations_pf)
            
        return output_folder
