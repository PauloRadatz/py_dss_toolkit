# -*- coding: utf-8 -*-
# @Author  : Ferdinando Crispino
# @Email   : ferdinando.crispino@usp.br

import pandas as pd
from py_dss_interface import DSS
from py_dss_tools.dss_tools.dss_tools import dss_tools

"""
Check the bus inversion following the network topology
for each end element, check the bus1 of element with the bus2 of parent element
"""
class PDBusOder:

    def __init__(self, dss: DSS):
        self._dss = dss
        dss_tools.update_dss(self._dss)

    @property
    def pd_bus_order(self) -> pd.DataFrame:
        return self.__check_bus_order()  # Todo - it should return a dataframe with the element names

    def __check_bus_order(self):

        data = []  # list of problem found

        # remove all meters if present in dss files
        for name in self._dss.meters.names:
            self._dss.text(f"disable energymeter.{name}")

        # add meter at first element
        dss_tools.model.add_line_in_vsource(add_meter=True)

        #self._dss.text("solve")

        # search button-up
        self._dss.meters.first()
        end_elements = self._dss.meters.all_end_elements
        for end_elem in end_elements:
            self._dss.circuit.set_active_element(end_elem)
            elem_name = self._dss.cktelement.name
            elem_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
            elem_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]
            # print(f'verification for {elem_name} ==============================================')
            while self._dss.circuit.parent_pd_element:
                parent_elem_name = self._dss.cktelement.name
                parent_elem_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                parent_elem_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]
                if elem_bus1 == parent_elem_bus2:
                    elem_bus1 = parent_elem_bus1
                elif elem_bus1 == parent_elem_bus1:  # bus inversion
                    elem_bus1 = parent_elem_bus2    # inverter to check next
                    print(f'Bus inversion {parent_elem_name} bus1 {parent_elem_bus1} bus2 {parent_elem_bus2}')
                    data.append([parent_elem_name, parent_elem_bus1, parent_elem_bus2])

        df_data = pd.DataFrame(data, columns=["element_name", "bus1", "bus2"])
        df_data.drop_duplicates(subset='element_name', keep='first', inplace=True)
        return df_data


if __name__ == '__main__':
    import os
    import pathlib

    dss = DSS()

    script_path = os.path.dirname(os.path.abspath(__file__))
    dss_file = pathlib.Path(script_path).joinpath("..", "..", "..", "..", "examples", "feeders", "123Bus",
                                                  "IEEE123Master.dss")
    bus_coords = pathlib.Path(script_path).joinpath("..", "..", "..", "..", "examples", "feeders", "123Bus",
                                                    "buscoords.dat")

    dss.text(f"compile [{dss_file}]")
    dss.text(f"buscoords buscoords.dat")
    dss.text("new energymeter.m element=line.l115")

    result_1 = PDBusOder(dss).pd_bus_order  # To get results.
    print("No problem added")
    print(result_1)

    # Set inversion to bus2 and bus1 (Bus1=108.1      Bus2=109.1 )
    dss.text("edit Line.l107 bus1=109.1 bus2=108.1")
    result_1 = PDBusOder(dss).pd_bus_order  # To get results.
    print(result_1)


  # verification for real circuit
    dss_dir = "C:/Users/Ferdinando/Desktop/curso_opendss/1924"
    dss_name = "DU_1_Master_40_MSU_1924.dss"
    dss_file = pathlib.Path(script_path).joinpath(dss_dir, dss_name)

    dss.dssinterface.clear_all()
    dss.text(f"compile [{dss_file}]")
    result_1 = PDBusOder(dss).pd_bus_order  # To get results.
    print(result_1)

    # set transformer problem with 3 Windings (bus1 == bus2 )
    #dss.text("edit Transformer.trf_2391823a buses=['910103B2391823.1.2' '910103B2391823.1.4' '910103B2391823.4.2']")
