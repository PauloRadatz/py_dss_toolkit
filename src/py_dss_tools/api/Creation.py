# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 09/10/2021 at 01:07:44
 Project: py-dss-tools [out, 2021]
"""
from py_dss_tools.model.pdelement import Line
from py_dss_tools.secondary import Scenario, Circuit


# TODO
def check_scenario_exist(sc) -> bool:
    return isinstance(sc, Scenario)


# TODO
def check_circuit_exist(circuit) -> bool:
    return isinstance(circuit, Circuit)


def create_scenario(name: str, frequency_base: [int, float] = 60, **kwargs) -> [object, Scenario]:
    """Create a scenario to starts work with OpenDSS."""
    sc = Scenario(name=name, frequency_base=frequency_base)
    sc = treat_object(obj=sc, kwargs=kwargs)
    return sc


def create_circuit(sc: Scenario, name: str, basekv: [int, float] = 115, bus1: str = 'sourcebus',
                   pu: [int, float] = 1.0001, phases: int = 3, angle: [int, float] = 0,
                   **kwargs) -> bool:
    if check_scenario_exist(sc):
        circuit = Circuit(name=name, basekv=basekv, bus1=bus1, pu=pu, phases=phases, angle=angle)
        sc.circuit = treat_object(obj=circuit, kwargs=kwargs)
        return True
    else:
        print("You must create a Scenario first!")
        return False


# def update_circuit_df(sc: Scenario):
#     if sc.circuit.created:
#         names = sc.circuit.dss.cktelement_all_property_names()
#         total = int(sc.circuit.dss.cktelement_num_properties())
#         for i in range(total):
#             command_ = f"sc.circuit.{names[i].lower()} = '{sc.circuit.dss.dssproperties_read_value(str(i + 1))}'"
#             exec(command_)


def generate_list_keys_without_(obj: object) -> list:
    if callable(getattr(obj, "to_list")):
        return [list_keys.replace("_", "") for list_keys in obj.to_list()]
    print("There isn't a function called to_list(), please creat it!")
    return []


def set_all_attibutes(obj: object, kwargs: dict, list_keys) -> bool:
    for k, v in kwargs.items():
        if k not in list_keys:
            raise Exception(f"\n\nPAY ATTENTION: The attribute {k} doesn't exist in Class {obj}")
            # return False
        else:
            setattr(obj, k, v)
    return True


def treat_object(obj: object, kwargs: dict) -> object:
    list_keys = []
    try:
        list_keys = generate_list_keys_without_(obj)
    except Exception as e:
        print(f"An error occur when tried to remove _ to object {obj}!", e)

    if set_all_attibutes(obj=obj, kwargs=kwargs, list_keys=list_keys):
        return obj
    else:
        raise Exception(f"An error occur when tried to set attributes dynamic in object {obj}!")


def add_line(sc: Scenario, line: Line) -> bool:
    if not isinstance(line, Line):
        return False
    sc.lines = line
    return True


def create_line(sc: Scenario, name: str, bus1: str, bus2: str, **kwargs) -> bool:
    try:
        line = Line(name=name, bus1=bus1, bus2=bus2)
        sc.lines = treat_object(obj=line, kwargs=kwargs)
        return True
    except Exception as e:
        print(e.message)
        return False
