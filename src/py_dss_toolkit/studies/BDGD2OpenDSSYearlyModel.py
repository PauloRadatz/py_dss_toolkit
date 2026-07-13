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

    def _write_master_and_copy_grid(self, output_folder: str, total_hours: int, add_nt_redirects: bool = False):
        master_files = self._find_files(r"^Master_.*\.dss$")
        if not master_files:
            raise FileNotFoundError(f"No Master file found in {self.dss_model_folder}")
            
        base_master = master_files[0]
        grid_files_to_copy = []
        
        new_master_path = os.path.join(output_folder, "master.dss")
        with open(base_master, 'r', encoding='utf-8') as fin, open(new_master_path, 'w', encoding='utf-8') as fout:
            wrote_new_loads = False
            for line in fin:
                line_strip = line.strip()
                
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
                                if add_nt_redirects:
                                    fout.write('Redirect "CargaBT_annual_energy_adjustment.dss"\n')
                                    fout.write('Redirect "CargaMT_annual_energy_adjustment.dss"\n')
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
                else:
                    fout.write(line)
                    
        for fname in grid_files_to_copy:
            src = os.path.join(self.dss_model_folder, fname)
            dst = os.path.join(output_folder, fname)
            if os.path.exists(src):
                shutil.copy2(src, dst)

    def _create_loading_info(self, output_folder, calendar_dict):
        from py_dss_toolkit.dss_tools.dss_tools import dss_tools
        
        master_dss = os.path.join(output_folder, "master.dss")
        dss = self._dss
        dss_tools.update_dss(dss)
        dss.text(f"compile [{master_dss}]")
        
        dss_tools.model.add_line_in_vsource(add_meter=True, add_monitors=True)
        dss.text("solve")
        
        dss.monitors.name = "monitor_feeder_head_pq"
        header = dss.monitors.header
        
        kw_channels = [i + 1 for i, h in enumerate(header) if "kW" in h]
        
        total_kw = [0.0] * dss.monitors.sample_count
        for ch in kw_channels:
            data = dss.monitors.channel(ch)
            for i in range(len(total_kw)):
                if i < len(data):
                    total_kw[i] += data[i]
                    
        month_boundaries = {}
        current_hour = 0
        for m in range(1, 13):
            if m in calendar_dict:
                days_in_month = len(calendar_dict[m])
                hours_in_month = days_in_month * 24
                month_boundaries[m] = (current_hour, current_hour + hours_in_month)
                current_hour += hours_in_month
                
        if not total_kw:
            return
            
        global_peak_val = max(total_kw)
        global_peak_ts = total_kw.index(global_peak_val) + 1 # 1-indexed timestep is more readable
        global_offpeak_val = min(total_kw)
        global_offpeak_ts = total_kw.index(global_offpeak_val) + 1
        
        summary = [
            {"Scope": "Global", "Peak Value (kW)": round(global_peak_val, 2), "Peak Timestep": global_peak_ts,
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
                        "Peak Value (kW)": round(m_peak_val, 2),
                        "Peak Timestep": m_peak_ts,
                        "Off-Peak Value (kW)": round(m_offpeak_val, 2),
                        "Off-Peak Timestep": m_offpeak_ts
                    })
                    
        csv_path = os.path.join(output_folder, "loading_info.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["Scope", "Peak Value (kW)", "Peak Timestep", "Off-Peak Value (kW)", "Off-Peak Timestep"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary:
                writer.writerow(row)
        print(f"Loading info CSV created at: {csv_path}")

    def execute_base_case(self, output_folder: str = None, create_loading_info_file: bool = True):
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
        self._write_master_and_copy_grid(output_folder, total_hours)
        
        print(f"8760 Base Case generation complete. Output saved to: {output_folder}")
        
        if create_loading_info_file:
            print("Running simulation to create loading info file...")
            self._create_loading_info(output_folder, calendar_dict)

    def execute_annual_energy_case(
        self,
        output_folder: str = None,
        tolerance_kwh_per_month: float = 500.0,
        lv_energy_share: float = 1.0,
        max_iterations: int = 20,
        create_loading_info_file: bool = True,
    ):
        
        if output_folder is None:
            folder_name = os.path.basename(self.dss_model_folder)
            output_folder = os.path.join(self.dss_model_folder, f"{folder_name}_8760_annual_energy_case")
            
        output_folder = os.path.abspath(output_folder)
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder, ignore_errors=True)
        os.makedirs(output_folder, exist_ok=True)
        
        # 1. Base case setup
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
        
        # We need the NT redirects
        self._write_master_and_copy_grid(output_folder, total_hours, add_nt_redirects=True)
        
        # 2. Extract target energy from CircMT_
        csv_folder = os.path.join(self.dss_model_folder, "csv_files")
        circ_mt_files = [f for f in os.listdir(csv_folder) if f.lower().startswith("circmt") and f.lower().endswith(".csv")]
        if not circ_mt_files:
            raise FileNotFoundError("CircMT CSV not found.")
        circ_mt_path = os.path.join(csv_folder, circ_mt_files[0])
        
        df_circ = pd.read_csv(circ_mt_path)
        target_annual_energy_mwh = 0.0
        for col in df_circ.columns:
            if col.startswith("EnerCirc") and col.endswith("_MWh"):
                target_annual_energy_mwh += df_circ[col].sum()
        
        target_kwh = target_annual_energy_mwh * 1000.0
        tolerance_kwh = 12 * tolerance_kwh_per_month
        
        # 3. Calculate original base energies and write NT loads
        original_energies = []
        nt_bt_loads = []
        nt_mt_loads = []
        
        for k, v in bt_loads.items():
            ann_energy = sum(v['curve'])
            original_kw = v['max_kw']
            shape_sum = (ann_energy / original_kw) if original_kw > 0 else 0.0
            original_energies.append({"Load": k, "Type": "LV", "Base_kW": original_kw, "Shape_Sum": shape_sum, "Annual_Energy_kWh": ann_energy})
            if lv_energy_share > 0:
                line = v['template']
                line = re.sub(fr'(?i)(Load\.{re.escape(k)})', fr'\1_NT', line)
                line = re.sub(r'(kw\s*=\s*)"?([^"\s]+)"?', 'kw=0.0', line, flags=re.IGNORECASE)
                line = re.sub(r'((?:daily|yearly)\s*=\s*)"?([^"\s]+)"?', fr'yearly="{k}_8760"', line, flags=re.IGNORECASE)
                nt_bt_loads.append(line)
                
        for k, v in mt_loads.items():
            ann_energy = sum(v['curve'])
            original_kw = v['max_kw']
            shape_sum = (ann_energy / original_kw) if original_kw > 0 else 0.0
            original_energies.append({"Load": k, "Type": "MV", "Base_kW": original_kw, "Shape_Sum": shape_sum, "Annual_Energy_kWh": ann_energy})
            if lv_energy_share < 1.0:
                line = v['template']
                line = re.sub(fr'(?i)(Load\.{re.escape(k)})', fr'\1_NT', line)
                line = re.sub(r'(kw\s*=\s*)"?([^"\s]+)"?', 'kw=0.0', line, flags=re.IGNORECASE)
                line = re.sub(r'((?:daily|yearly)\s*=\s*)"?([^"\s]+)"?', fr'yearly="{k}_8760"', line, flags=re.IGNORECASE)
                nt_mt_loads.append(line)
                
        df_energies = pd.DataFrame(original_energies)
        df_energies["NT_kW"] = 0.0
        df_energies["NT_Annual_Energy_kWh"] = 0.0
        df_energies["Effective_Annual_Energy_kWh"] = df_energies["Annual_Energy_kWh"]
        
        total_lv_energy = df_energies[df_energies["Type"] == "LV"]["Annual_Energy_kWh"].sum()
        total_mv_energy = df_energies[df_energies["Type"] == "MV"]["Annual_Energy_kWh"].sum()
        
        # Create empty/initial NT files
        with open(os.path.join(output_folder, "CargaBT_annual_energy_adjustment.dss"), 'w') as f:
            if nt_bt_loads:
                f.write("\n".join(nt_bt_loads))
        with open(os.path.join(output_folder, "CargaMT_annual_energy_adjustment.dss"), 'w') as f:
            if nt_mt_loads:
                f.write("\n".join(nt_mt_loads))
            
        # 4. Iterative Process
        master_dss = os.path.join(output_folder, "master.dss")
        dss = self._dss
        dss.text(f"compile [{master_dss}]")
        
        iteration_history = []
        
        for iteration in range(1, max_iterations + 1):
            dss.text("set hour=0")
            dss.meters.first()
            dss.meters.reset()
            dss.text("solve")
            
            dss.meters.first()
            simulated_kwh = dss.meters.register_values[0] # register 0 is kWh
            
            diff_kwh = target_kwh - simulated_kwh
            within_tolerance = abs(diff_kwh) <= tolerance_kwh
            
            lv_alloc = diff_kwh * lv_energy_share
            mv_alloc = diff_kwh * (1.0 - lv_energy_share)
            
            iteration_history.append({
                "Iteration": iteration,
                "Simulated_kWh": simulated_kwh,
                "Target_kWh": target_kwh,
                "Diff_kWh": diff_kwh,
                "LV_Allocated": lv_alloc,
                "MV_Allocated": mv_alloc,
                "Within_Tolerance": within_tolerance
            })
            
            print(f"Iter {iteration}: Sim={simulated_kwh:.2f}, Target={target_kwh:.2f}, Diff={diff_kwh:.2f} (Tol={tolerance_kwh:.2f})")
            
            if within_tolerance:
                break
                
            # Distribute LV alloc
            if lv_energy_share > 0 and total_lv_energy > 0:
                for idx, row in df_energies[df_energies["Type"] == "LV"].iterrows():
                    if row["Shape_Sum"] > 0 and row["Annual_Energy_kWh"] > 0:
                        share = row["Annual_Energy_kWh"] / total_lv_energy
                        load_alloc = lv_alloc * share
                        dss.loads.name = f"{row['Load']}_NT"
                        dss.loads.kw = dss.loads.kw + (load_alloc / row["Shape_Sum"])
                        
            # Distribute MV alloc
            if lv_energy_share < 1.0 and total_mv_energy > 0:
                for idx, row in df_energies[df_energies["Type"] == "MV"].iterrows():
                    if row["Shape_Sum"] > 0 and row["Annual_Energy_kWh"] > 0:
                        share = row["Annual_Energy_kWh"] / total_mv_energy
                        load_alloc = mv_alloc * share
                        dss.loads.name = f"{row['Load']}_NT"
                        dss.loads.kw = dss.loads.kw + (load_alloc / row["Shape_Sum"])
                        
        # 5. After converged (or max iter), rewrite final NT files
        if lv_energy_share > 0:
            final_bt = []
            for idx, row in df_energies[df_energies["Type"] == "LV"].iterrows():
                dss.loads.name = f"{row['Load']}_NT"
                final_kw = dss.loads.kw
                
                df_energies.at[idx, "NT_kW"] = final_kw
                nt_energy = final_kw * row["Shape_Sum"]
                df_energies.at[idx, "NT_Annual_Energy_kWh"] = nt_energy
                df_energies.at[idx, "Effective_Annual_Energy_kWh"] = row["Annual_Energy_kWh"] + nt_energy
                
                v = bt_loads[row['Load']]
                line = v['template']
                line = re.sub(fr'(?i)(Load\.{re.escape(row["Load"])})', fr'\1_NT', line)
                line = re.sub(r'(kw\s*=\s*)"?([^"\s]+)"?', f'kw={final_kw:.6f}', line, flags=re.IGNORECASE)
                line = re.sub(r'((?:daily|yearly)\s*=\s*)"?([^"\s]+)"?', fr'yearly="{row["Load"]}_8760"', line, flags=re.IGNORECASE)
                final_bt.append(line)
            with open(os.path.join(output_folder, "CargaBT_annual_energy_adjustment.dss"), 'w') as f:
                f.write("\n".join(final_bt))
                
        if lv_energy_share < 1.0:
            final_mt = []
            for idx, row in df_energies[df_energies["Type"] == "MV"].iterrows():
                dss.loads.name = f"{row['Load']}_NT"
                final_kw = dss.loads.kw
                
                df_energies.at[idx, "NT_kW"] = final_kw
                nt_energy = final_kw * row["Shape_Sum"]
                df_energies.at[idx, "NT_Annual_Energy_kWh"] = nt_energy
                df_energies.at[idx, "Effective_Annual_Energy_kWh"] = row["Annual_Energy_kWh"] + nt_energy
                
                v = mt_loads[row['Load']]
                line = v['template']
                line = re.sub(fr'(?i)(Load\.{re.escape(row["Load"])})', fr'\1_NT', line)
                line = re.sub(r'(kw\s*=\s*)"?([^"\s]+)"?', f'kw={final_kw:.6f}', line, flags=re.IGNORECASE)
                line = re.sub(r'((?:daily|yearly)\s*=\s*)"?([^"\s]+)"?', fr'yearly="{row["Load"]}_8760"', line, flags=re.IGNORECASE)
                final_mt.append(line)
            with open(os.path.join(output_folder, "CargaMT_annual_energy_adjustment.dss"), 'w') as f:
                f.write("\n".join(final_mt))
                
        df_energies.to_csv(os.path.join(output_folder, "original_load_energies.csv"), index=False)
        
        df_hist = pd.DataFrame(iteration_history)
        df_hist.to_csv(os.path.join(output_folder, "iteration_history.csv"), index=False)
        print(f"Annual Energy Allocation complete. History saved.")
        
        if create_loading_info_file:
            print("Running simulation to create loading info file...")
            self._create_loading_info(output_folder, calendar_dict)
            
        return output_folder
