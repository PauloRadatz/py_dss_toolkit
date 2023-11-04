# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 09/10/2021 at 01:07:44
 Project: py-dss-tools [out, 2021]
"""
from re import search

from py_dss_tools.secondary import Scenario
from py_dss_tools.algorithms.PowerFlow import PowerFlow

from typing import Optional


# TODO
def check_scenario_exist(sc) -> bool:
    return isinstance(sc, Scenario)


def create_scenario(name: str, dss_file: str, study_type: str ="Unknown", frequency_base: [int, float] = 60, dll: Optional[str] = None, **kwargs) -> Scenario:
    """Create a scenario to starts work with OpenDSS."""
    try:
        if study_type == "Unknown":
            sc = Scenario(name, dss_file, frequency_base, dll)
            # sc = treat_object(obj=sc, kwargs=kwargs)  # TODO Understand it later
        elif study_type == "powerflow":
            sc = PowerFlow(name, dss_file, frequency_base, dll)
        return sc
    except Exception as e:
        raise
        print(f"Error when tried to create a Scenario! {e}")



# def update_circuit_df(sc: Scenario):
#     if sc.circuit.created:
#         names = sc.circuit.dss.cktelement_all_property_names()
#         total = int(sc.circuit.dss.cktelement_num_properties())
#         for i in range(total):
#             command_ = f"sc.circuit.{names[i].lower()} = '{sc.circuit.dss.dssproperties_read_value(str(i + 1))}'"
#             exec(command_)

def remove_percentage(my_list: list) -> list:
    new_list = []
    for value in my_list:
        if search('percentage', value):
            value = value.replace('percentage', '%')
        new_list.append(value)
    return new_list


def generate_list_keys_without_(obj: object) -> list:
    if callable(getattr(obj, "to_list")):
        my_list = remove_percentage(obj.to_list())

        try:
            return sorted((list_keys.replace("_", "")) for list_keys in my_list)
        except Exception as e:
            print(f"Error tried generate list keys! {e.message}")
    print("There isn't a function called to_list(), please creat it!")
    return []


def set_all_attibutes(obj: object, kwargs: dict, list_keys) -> bool:
    for k, v in kwargs.items():
        if k not in list_keys:
            raise Exception(f"\n\nPAY ATTENTION: The attribute {k} doesn't exist in Class {obj}")
        try:
            setattr(obj, k, v)
        except Exception as e:
            print(f"Error when trying set attributes ! {e}")
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






def __translate_controls(sc: Scenario):
    pass


def __translate_generals(sc: Scenario):
    pass


def __translate_meters(sc: Scenario):
    pass


def __translate_others(sc: Scenario):
    pass


def __translate_pcelements(sc: Scenario):
    pass


def __create_text_(obj: object) -> [str, str]:
    name = ''
    result = ''
    for k in dir(obj):
        if not search('_', k) and not search('name', k):
            attribute_value = getattr(obj, k)
            if isinstance(attribute_value, str):
                result += f"{k}='{attribute_value}' "
            else:
                result += f"{k}={attribute_value} "
        if search('name', k):
            name = getattr(obj, k)
    return name, result


def __translate_circuit(sc: Scenario) -> bool:
    try:
        name, text = __create_text_(sc.circuit)
        result = f"new circuit.{name} {text}"
        sc.dss.text(result)
        return True
    except Exception as e:
        print(f"Error when tried translate circuit to DSS! {e.message}")
        return False


def run_scenario(sc: Scenario):
    try:
        __translate_circuit(sc)
        # __translate_controls(sc)
        # __translate_generals(sc)
        # __translate_meters(sc)
        # __translate_others(sc)
        # __translate_pcelements(sc)
        __translate_pdelements(sc)
        # return True
    except Exception as e:
        print(f"Error when tried to compile Scenario! {e}")
        return False


def solve_scenario(sc):
    sc.__dss.text("solve")
