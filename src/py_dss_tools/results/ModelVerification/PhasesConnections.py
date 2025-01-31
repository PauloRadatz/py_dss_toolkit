# -*- coding: utf-8 -*-
# @Author  : Iury Zanelato
# @Email   : iury.ribeirozanelato@gmail.com
# @File    : Phases_Connections.py
# @Software: PyCharm

from py_dss_interface import DSS
import pandas as pd

"""
This code checks whether the phases connections are correct between the elements connected to the same bus.
"""

class PhasesConnections:

    def __init__(self, dss: DSS):
        self._dss = dss
        self._phases_connections = pd.DataFrame()

    @property
    def phases_connections(self) -> None:
        return self.__check_phases_connections() #Todo - it should return a dataframe with the element names

    def __add_default_nodes(self, elem_nodes):
        if not elem_nodes:
            return ['1', '2', '3']
        else:
            return elem_nodes

    def __check_phase_connection(self, parent_elem_nodes, elem_nodes):
        issue_flag = False
        for node in elem_nodes:
            if node not in parent_elem_nodes:
                if node != '4' and node != '0':
                    issue_flag = True

        if set(elem_nodes).issubset({'4', '0'}):
            issue_flag = True
        return issue_flag

    def __check_phases_connections(self):
        self._dss.text("solve")
        self._dss.meters.first()
        end_elements_pd = self._dss.meters.all_end_elements
        elements_pc = self._dss.meters.all_pce_in_zone

        elements_checked = list() # All network elements analyzed
        data = [] # To DataFrame

        for end_elem in end_elements_pd:
            if end_elem not in elements_checked:

                self._dss.circuit.set_active_element(end_elem)
                elem_name = self._dss.cktelement.name
                elements_checked.append(elem_name)

                elem_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                elem_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]
                elem_nodes1 = self._dss.cktelement.bus_names[0].split(".")[1:]
                elem_nodes2 = self._dss.cktelement.bus_names[1].split(".")[1:]

                while self._dss.circuit.parent_pd_element:

                    parent_elem_name = self._dss.cktelement.name

                    if parent_elem_name not in elements_checked:
                        if parent_elem_name.lower().split(".")[0] == "transformer":

                            transformer_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                            transformer_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]

                            transformer_bank = list()
                            transformer_bus1_nodes1 = list()
                            transformer_bus2_nodes2 = list()
                            transformer_nodes1_bus1 = list()
                            transformer_nodes2_bus2 = list()

                            elements = self._dss.circuit.elements_names

                            for element in elements: # Association of transformers of a bank
                                if element.lower().split(".")[0] == "transformer":

                                    self._dss.circuit.set_active_element(element)

                                    transformer_bus1_ = self._dss.cktelement.bus_names[0].split(".")[0]
                                    transformer_bus2_ = self._dss.cktelement.bus_names[1].split(".")[0]
                                    transformer_bus1_node1 = self._dss.cktelement.bus_names[0].split(".")[1:]
                                    transformer_bus2_node2 = self._dss.cktelement.bus_names[1].split(".")[1:]

                                    elem_nodes1 = self.__add_default_nodes(elem_nodes1)[0:]
                                    elem_nodes2 = self.__add_default_nodes(elem_nodes2)[0:]
                                    transformer_bus1_node1 = self.__add_default_nodes(transformer_bus1_node1)[0:]
                                    transformer_bus2_node2 = self.__add_default_nodes(transformer_bus2_node2)[0:]

                                    if transformer_bus1 == transformer_bus1_ and transformer_bus2 == transformer_bus2_:
                                        if element not in transformer_bank:
                                            transformer_bank.append(element)

                                        if transformer_bus1_node1 not in transformer_bus1_nodes1:
                                            transformer_bus1_nodes1.append(transformer_bus1_node1)

                                        if transformer_bus2_node2 not in transformer_bus2_nodes2:
                                            transformer_bus2_nodes2.append(transformer_bus2_node2)

                            for sublista in transformer_bus1_nodes1: # Removes the square brackets and associates the node in a new list
                                for num in sublista:
                                    if num not in transformer_nodes1_bus1:
                                        transformer_nodes1_bus1.append(num)
                                        transformer_nodes1_bus1.sort()  # Sort the new list in ascending order

                            for sublista in transformer_bus2_nodes2: # Removes the square brackets and associates the node in a new list
                                for num in sublista:
                                    if num not in transformer_nodes2_bus2:
                                        transformer_nodes2_bus2.append(num)
                                        transformer_nodes2_bus2.sort()  # Sort the new list in ascending order

                            if len(transformer_bank) == 2:
                                print(f"\nTransformer Bank found:{transformer_bank} - Open Delta")

                            if len(transformer_bank) == 3:
                                print(f"\nTransformer Bank found:{transformer_bank} - Closed Delta")

                            # Case 1 (Checks if the element's bus1 is equal to the parent's bus2)
                            if elem_bus1 == transformer_bus2:
                                if self.__check_phase_connection(transformer_nodes2_bus2, elem_nodes1):
                                    print(
                                        f"\nPhase issue between (Case 1):\nParent: {transformer_bank} with bus {transformer_bus2} and nodes {transformer_nodes2_bus2}"
                                        f"\nElement: {elem_name} with bus {elem_bus1} and nodes {elem_nodes1}")

                                    data.append([transformer_bank, transformer_bus2, transformer_nodes2_bus2, elem_name,
                                                 elem_bus1, elem_nodes1])

                            # Case 2 (Checks if the element's bus1 is equal to the parent's bus1)
                            elif elem_bus1 == transformer_bus1:
                                if self.__check_phase_connection(transformer_nodes1_bus1, elem_nodes1):
                                    print(
                                        f"\nPhase issue between (Case 2):\nParent: {transformer_bank} with bus {transformer_bus1} and nodes {transformer_nodes1_bus1}"
                                        f"\nElement: {elem_name} with bus {elem_bus1} and nodes {elem_nodes1}")

                                    data.append([transformer_bank, transformer_bus1, transformer_nodes1_bus1, elem_name,
                                                 elem_bus1, elem_nodes1])

                            # Case 3 (Checks if the element's bus2 is equal to the parent's bus2)
                            elif elem_bus2 == transformer_bus2:
                                if self.__check_phase_connection(transformer_nodes2_bus2, elem_nodes2):
                                    print(
                                        f"\nPhase issue between (Case 3):\nParent: {transformer_bank} with bus {transformer_bus2} and nodes {transformer_nodes2_bus2}"
                                        f"\nElement: {elem_name} with bus {elem_bus2} and nodes {elem_nodes2}")

                                    data.append([transformer_bank, transformer_bus2, transformer_nodes2_bus2, elem_name,
                                                 elem_bus2, elem_nodes2])

                            # Case 4 (Checks if the element's bus2 is equal to the parent's bus1)
                            elif elem_bus2 == transformer_bus1:
                                if self.__check_phase_connection(transformer_nodes1_bus1, elem_nodes2):
                                    print(
                                        f"\nPhase issue between (Case 4):\nParent: {transformer_bank} with bus {transformer_bus1} and nodes {transformer_nodes1_bus1}"
                                        f"\nElement: {elem_name} with bus {elem_bus2} and nodes {elem_nodes2}")

                                    data.append([transformer_bank, transformer_bus1, transformer_nodes1_bus1, elem_name,
                                                 elem_bus2, elem_nodes2])

                            if transformer_bank not in elements_checked:
                                for transformer in transformer_bank:
                                    if transformer not in elements_checked:
                                        elem_name = parent_elem_name
                                        elem_bus1 = transformer_bus1
                                        elem_bus2 = transformer_bus2
                                        elem_nodes1 = transformer_nodes1_bus1
                                        elem_nodes2 = transformer_nodes2_bus2
                                        elements_checked.append(transformer)

                        else:

                            parent_elem_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                            parent_elem_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]
                            parent_elem_nodes1 = self._dss.cktelement.bus_names[0].split(".")[1:]
                            parent_elem_nodes2 = self._dss.cktelement.bus_names[1].split(".")[1:]

                            elem_nodes1 = self.__add_default_nodes(elem_nodes1)[0:]
                            elem_nodes2 = self.__add_default_nodes(elem_nodes2)[0:]
                            parent_elem_nodes1 = self.__add_default_nodes(parent_elem_nodes1)[0:]
                            parent_elem_nodes2 = self.__add_default_nodes(parent_elem_nodes2)[0:]

                            #Case 1 (Checks if the element's bus1 is equal to the parent's bus2)
                            if elem_bus1 == parent_elem_bus2:
                                if self.__check_phase_connection(parent_elem_nodes2, elem_nodes1):
                                    print(
                                        f"\nPhase issue between (Case 1):\nParent: {parent_elem_name} with bus {parent_elem_bus2} and nodes {parent_elem_nodes2}"
                                        f"\nElement: {elem_name} with bus {elem_bus1} and nodes {elem_nodes1}")

                                    data.append([parent_elem_name, parent_elem_bus2, parent_elem_nodes2, elem_name,
                                                 elem_bus1, elem_nodes1])

                            # Case 2 (Checks if the element's bus1 is equal to the parent's bus1)
                            elif elem_bus1 == parent_elem_bus1:
                                if self.__check_phase_connection(parent_elem_nodes1, elem_nodes1):
                                    print(
                                        f"\nPhase issue between (Case 2):\nParent: {parent_elem_name} with bus {parent_elem_bus1} and nodes {parent_elem_nodes1}"
                                        f"\nElement: {elem_name} with bus {elem_bus1} and nodes {elem_nodes1}")

                                    data.append([parent_elem_name, parent_elem_bus1, parent_elem_nodes1, elem_name,
                                                 elem_bus1, elem_nodes1])

                            # Case 3 (Checks if the element's bus2 is equal to the parent's bus2)
                            elif elem_bus2 == parent_elem_bus2:
                                if self.__check_phase_connection(parent_elem_nodes2, elem_nodes2):
                                    print(
                                        f"\nPhase issue between (Case 3):\nParent: {parent_elem_name} with bus {parent_elem_bus2} and nodes {parent_elem_nodes2}"
                                        f"\nElement: {elem_name} with bus {elem_bus2} and nodes {elem_nodes2}")

                                    data.append([parent_elem_name, parent_elem_bus2, parent_elem_nodes2, elem_name,
                                                 elem_bus2, elem_nodes2])

                            # Case 4 (Checks if the element's bus2 is equal to the parent's bus1)
                            elif elem_bus2 == parent_elem_bus1:
                                if self.__check_phase_connection(parent_elem_nodes1, elem_nodes2):
                                    print(
                                        f"\nPhase issue between (Case 4):\nParent: {parent_elem_name} with bus {parent_elem_bus1} and nodes {parent_elem_nodes1}"
                                        f"\nElement: {elem_name} with bus {elem_bus2} and nodes {elem_nodes2}")

                                    data.append([parent_elem_name, parent_elem_bus1, parent_elem_nodes1, elem_name,
                                                 elem_bus2, elem_nodes2])

                            elem_name = parent_elem_name
                            elem_bus1 = parent_elem_bus1
                            elem_bus2 = parent_elem_bus2
                            elem_nodes1 = parent_elem_nodes1
                            elem_nodes2 = parent_elem_nodes2

                            if elem_name not in elements_checked:
                                elements_checked.append(elem_name)

        for elem_pc in elements_pc:
            if not elem_pc.lower().split(".")[0] == "reactor":
                if elem_pc not in elements_checked:

                    self._dss.circuit.set_active_element(elem_pc)
                    elem_name_pc = self._dss.cktelement.name

                    elem_bus_pc = self._dss.cktelement.bus_names[0].split(".")[0]
                    elem_nodes_pc = self._dss.cktelement.bus_names[0].split(".")[1:]

                    if elem_name_pc not in elements_checked:

                        elements_circuit = self._dss.circuit.elements_names

                        trans_bank = list()
                        elements_bus1 = list()
                        elements_bus2 = list()
                        element_bus1 = list()
                        element_bus2 = list()
                        element_bus1_nodes1 = list()
                        element_bus2_nodes2 = list()
                        element_nodes1_bus1 = list()
                        element_nodes2_bus2 = list()

                        _ = "Not applicable"

                        for element_circuit in elements_circuit:  # Association with the pc elements
                            if element_circuit not in elements_pc:
                                if not element_circuit.lower().split(".")[0] == "energymeter":
                                    if element_circuit.lower().split(".")[0] == "transformer":
                                        if element_circuit not in trans_bank:

                                            self._dss.circuit.set_active_element(element_circuit)

                                            transformer_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                                            transformer_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]

                                            transformer_bank = list()

                                            if transformer_bus1 in elem_bus_pc or transformer_bus2 in elem_bus_pc:

                                                elem_cir = self._dss.circuit.elements_names

                                                for elem in elem_cir:  # Association of transformers of a bank
                                                    if elem.lower().split(".")[0] == "transformer":

                                                        self._dss.circuit.set_active_element(elem)

                                                        transformer_bus1_ = self._dss.cktelement.bus_names[0].split(".")[0]
                                                        transformer_bus2_ = self._dss.cktelement.bus_names[1].split(".")[0]
                                                        element_bus1_node1 = self._dss.cktelement.bus_names[0].split(".")[1:]
                                                        element_bus2_node2 = self._dss.cktelement.bus_names[1].split(".")[1:]

                                                        elem_nodes_pc = self.__add_default_nodes(elem_nodes_pc)[0:]
                                                        element_bus1_node1 = self.__add_default_nodes(element_bus1_node1)[0:]
                                                        element_bus2_node2 = self.__add_default_nodes(element_bus2_node2)[0:]

                                                        if transformer_bus1 == transformer_bus1_ and transformer_bus2 == transformer_bus2_:
                                                            if elem not in transformer_bank:
                                                                transformer_bank.append(elem)
                                                                trans_bank.append(elem)

                                                            if element_bus1_node1 not in element_bus1_nodes1:
                                                                element_bus1_nodes1.append(element_bus1_node1)

                                                            if element_bus2_node2 not in element_bus2_nodes2:
                                                                element_bus2_nodes2.append(element_bus2_node2)

                                                            if transformer_bus1 not in elements_bus1:
                                                                elements_bus1.append(transformer_bus1)

                                                            if transformer_bus2 not in elements_bus2:
                                                                elements_bus2.append(transformer_bus2)

                                    else:

                                        self._dss.circuit.set_active_element(element_circuit)

                                        parent_elem_bus1 = self._dss.cktelement.bus_names[0].split(".")[0]
                                        parent_elem_bus2 = self._dss.cktelement.bus_names[1].split(".")[0]
                                        parent_elem_nodes1 = self._dss.cktelement.bus_names[0].split(".")[1:]
                                        parent_elem_nodes2 = self._dss.cktelement.bus_names[1].split(".")[1:]

                                        elem_nodes_pc = self.__add_default_nodes(elem_nodes_pc)[0:]
                                        parent_elem_nodes1 = self.__add_default_nodes(parent_elem_nodes1)[0:]
                                        parent_elem_nodes2 = self.__add_default_nodes(parent_elem_nodes2)[0:]

                                        if parent_elem_bus1 in elem_bus_pc or parent_elem_bus2 in elem_bus_pc:
                                            element_bus1_nodes1.append(parent_elem_nodes1)
                                            element_bus2_nodes2.append(parent_elem_nodes2)

                                            if parent_elem_bus1 not in element_bus1:
                                                elements_bus1.append(parent_elem_bus1)

                                            if parent_elem_bus2 not in element_bus2:
                                                elements_bus2.append(parent_elem_bus2)

                        for sublista in element_bus1_nodes1:  # Removes the square brackets and associates the node in a new list
                            for num in sublista:
                                if num not in element_nodes1_bus1:
                                    element_nodes1_bus1.append(num)
                                    element_nodes1_bus1.sort()  # Sort the new list in ascending order

                        for sublista in element_bus2_nodes2:  # Removes the square brackets and associates the node in a new list
                            for num in sublista:
                                if num not in element_nodes2_bus2:
                                    element_nodes2_bus2.append(num)
                                    element_nodes2_bus2.sort()  # Sort the new list in ascending order

                        for bus in elements_bus1:  # Removes the square brackets and associates the node in a new list
                            if bus == elem_bus_pc:
                                element_bus1.append(bus)
                        element_bus1 = ', '.join(map(str, element_bus1))

                        for bus in elements_bus2:  # Removes the square brackets and associates the node in a new list
                            if bus == elem_bus_pc:
                                element_bus2.append(bus)
                        element_bus2 = ', '.join(map(str, element_bus2))

                        # Case 1 (Checks if the element's bus is equal to the parent's bus2)
                        if elem_bus_pc == element_bus2:
                            if self.__check_phase_connection(element_nodes2_bus2, elem_nodes_pc):
                                print(
                                    f"\nPhase issue between (Case 1):\nParent: {_} with bus {element_bus2} and nodes {element_nodes2_bus2}"
                                    f"\nElement: {elem_name_pc} with bus {elem_bus_pc} and nodes {elem_nodes_pc}")

                                data.append([_, element_bus2, element_nodes2_bus2,
                                             elem_name_pc, elem_bus_pc, elem_nodes_pc])

                        # Case 2 (Checks if the element's bus is equal to the parent's bus1)
                        elif elem_bus_pc == element_bus1:
                            if self.__check_phase_connection(element_nodes1_bus1, elem_nodes_pc):
                                print(
                                    f"\nPhase issue between (Case 2):\nParent: {_} with bus {element_bus1} and nodes {element_nodes1_bus1}"
                                    f"\nElement: {elem_name_pc} with bus {elem_bus_pc} and nodes {elem_nodes_pc}")

                                data.append([_, element_bus1, element_nodes1_bus1,
                                             elem_name_pc, elem_bus_pc, elem_nodes_pc])

                        if elem_name_pc not in elements_checked:
                            elements_checked.append(elem_name_pc)

        print("All elements checked")

        return pd.DataFrame(data, columns=["Parent Name", "Parent Bus", "Parent Node", "Element Name", "Element Bus",
                                           "Element Node"])

if __name__ == '__main__':
    import os
    import pathlib
    import time

    inicio = time.time()  # Marca o tempo de início

    dss = DSS()

    script_path = os.path.dirname(os.path.abspath(__file__))
    #dss_file = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "4Bus-DY-Bal_modified.dss")
    #dss_file = pathlib.Path(script_path).joinpath("..", "..","..", "..", "examples", "feeders", "123Bus", "IEEE123Master.dss")
    dss_file = pathlib.Path(script_path).joinpath("C:/bdgd2opendss/dss_models_output/1_3PAS_1/Master_DU03_202312598_1_3PAS_1_--MBS-1--T--.dss")

    dss.text(f"compile [{dss_file}]")
    #dss.text("new energymeter.m element=line.line1")  # To 4Bus-DY-Bal_modified
    #dss.text("new energymeter.m element=Line.L115")  # To IEEE123Master
    dss.text("new energymeter.m element=Line.smt_36960") # To Master_DU03_202312598_1_3PAS_1

    #result_1 = PhasesConnections(dss).phases_connections  # To get results.
    #print(f"\nNo problem added")
    #print(result_1)

    ### Add problem to IEEE123Master ###
    # To Case 1
    #dss.text("edit transformer.reg4c buses=[160.3 160r.4]")

    #dss.text("edit Line.L103 Bus1=103.1")

    # To Case 2
    #dss.text("New Line.L5652 Phases=3 Bus1=55.4 Bus2=52.1.2.3 LineCode=1 Length=0.6")

    # To Case 3
    #dss.text("edit Line.L117 Bus1=67.1.2.3 Bus2=160r.1.2.3")
    #dss.text("edit transformer.reg4c buses=[160.3 160r.4]")

    #dss.text("edit Line.L52 Bus2=53.4")
    #dss.text("edit Line.L53 Bus1=54.1.2.3 Bus2=53.1.2.3")

    # To Case 4
    #dss.text("New Line.L114112 Phases=3 Bus1=114.4 Bus2=112.1 LineCode=1 Length=0.85")
    ### End of Problem to 123Bus ###

    ### Add problem to 4Bus-DY-Bal_modified ###
    # To Case 1
    #dss.text("edit line.line2 bus2=n4.2.3")
    #dss.text("edit line.line3 bus2=n6.1")
    #dss.text("edit load.load2 bus1=n7.5")
    #dss.text("edit load.load1 bus1=n4.4")

    ### Add problem to Master_DU03_202312598_1_3PAS_1 ###
    # To Case 1
    #dss.text("edit Line.SMT_37467 bus2=797841.3")
    #dss.text("edit Load.BT_2806086_M1 bus1=UC2806086.5")

    result_2 = PhasesConnections(dss).phases_connections
    print("\nproblem added")
    print(result_2)

    fim = time.time()  # Marca o tempo ao chegar no ponto desejado
    print(f"Tempo decorrido: {fim - inicio:.4f} segundos")

    print("\nhere")
