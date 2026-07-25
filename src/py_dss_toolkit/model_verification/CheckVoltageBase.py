import os
import math
import pathlib
from py_dss_interface import DSS
from py_dss_toolkit import dss_tools

from py_dss_toolkit.model.ModelBase import ModelBase

class CheckVoltageBase:
    def __init__(self, dss: DSS, model: ModelBase, feeder):
        self._dss = dss
        self._model = model
        self._feeder = feeder

    def _check_voltage_base(self):
        """
        Verifica a tensão de base definida pelo openDSS para as todas as barras conectadas no secundario dos transformadores.
        São obtidas as tensões de fase para a barra do secundario do TR e compara com a informada pelo openDSS
        Em caso de diferença são localizadas todas barras conectadas no secundario do transformador e set o kv_base
        de todas as barras com o valor obtido da avaliação das conexoes do transformador.
        :return:
        """
        n = 0
        dss.transformers.first()
        for _ in range(dss.transformers.count):
            transformer_name = dss.transformers.name
            if transformer_name.lower().startswith("reg"):
                dss.transformers.next()
                continue

            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            tr_ph = dss.cktelement.num_phases
            if tr_ph == 3:
                vll = dss.transformers.kv
                vln = vll / math.sqrt(3)
            elif tr_ph == 1:
                num_wdg = dss.transformers.num_windings
                if num_wdg == 2:
                    if dss.transformers.is_delta:
                        vll = dss.transformers.kv
                        vln = vll / 2
                    else:
                        vln = dss.transformers.kv
                        vll = vln * 2
                elif num_wdg == 3:
                    dss.transformers.wdg = 2
                    vln = dss.transformers.kv
                    vll = 2 * vln

            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base = dss.bus.kv_base
            if round(vln, 3) != round(kv_base, 3):
                if n == 0:
                    n += 1
                    # print(f'VERIFICAÇÃO DAS TENSÕES DE BASE - {self._feeder}\n')

                # print(f"transformer.{transformer_name} - kv_base:{kv_base} - new_kv_base:{vln}")
                dss.text(f'SetkVBase Bus={bus_transformer_name} kVLN={vln}')
                dss.topology.first()
                while True:
                    indx = dss.topology.active_branch
                    indx_level = dss.topology.active_level
                    branch_name = dss.topology.branch_name
                    if branch_name == f"Transformer.{transformer_name}":
                        dss.circuit.set_active_element(f"transformer.{transformer_name}")
                        dss.circuit.set_active_bus(bus_transformer_name)
                        break
                    index_branch = dss.topology.forward_branch()

                while True:
                    index_branch_2 = dss.topology.next()
                    indx_level_2 = dss.topology.active_level
                    branch_name_2 = dss.topology.branch_name
                    if not dss.topology.branch_name.lower().startswith(('line.sbt', 'line.rbt')):
                        break
                    dss.circuit.set_active_element(branch_name_2)
                    dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
                    bus_line_name = dss.bus.name
                    kv_base_2 = dss.bus.kv_base
                    dss.text(f'SetkVBase Bus={bus_line_name} kVLN={vln}')

            dss.transformers.next()

if __name__ == '__main__':
    script_path = os.path.dirname(os.path.realpath(__file__))
    dss_file = pathlib.Path(script_path).joinpath("..","..", "..", "examples", "feeders", "sub__MTQ", "RMTQ1302", "Master_DU01_202501391_RMTQ1302_------1-----.dss")
    feeder = dss_file.parent.name
    dss = DSS()
    dss_tools.update_dss(dss)
    model = ModelBase(dss)

    dss.text(f"compile [{dss_file}]")
    dss.text("solve")

    dss.transformers.first()
    for _ in range(dss.transformers.count):
        transformer_name = dss.transformers.name
        if transformer_name.upper() == "TRF_260ET000303749A":
            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base_original = dss.bus.kv_base
            print(f"Transformer: {transformer_name}; Voltage Base: {kv_base_original} kV")
        elif transformer_name.upper() == "TRF_260ET000427099A":
            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base_original = dss.bus.kv_base
            print(f"Transformer: {transformer_name}; Voltage Base: {kv_base_original} kV")
        elif transformer_name.upper() == "TRF_260ET000403419A":
            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base_original = dss.bus.kv_base
            print(f"Transformer: {transformer_name}; Voltage Base: {kv_base_original} kV")

        dss.transformers.next()

    check = CheckVoltageBase(dss, model, feeder)
    check._check_voltage_base()

    dss.transformers.first()
    for _ in range(dss.transformers.count):
        transformer_name = dss.transformers.name
        if transformer_name.upper() == "TRF_260ET000303749A":
            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base_modified = dss.bus.kv_base
            print(f"Transformer: {transformer_name}; New Voltage Base: {kv_base_modified} kV")
        elif transformer_name.upper() == "TRF_260ET000427099A":
            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base_original = dss.bus.kv_base
            print(f"Transformer: {transformer_name}; New Voltage Base: {kv_base_original} kV")
        elif transformer_name.upper() == "TRF_260ET000403419A":
            dss.circuit.set_active_element(f"transformer.{transformer_name}")
            dss.circuit.set_active_bus(dss.cktelement.bus_names[1])
            bus_transformer_name = dss.bus.name
            kv_base_original = dss.bus.kv_base
            print(f"Transformer: {transformer_name}; New Voltage Base: {kv_base_original} kV")

        dss.transformers.next()

    print("here")
