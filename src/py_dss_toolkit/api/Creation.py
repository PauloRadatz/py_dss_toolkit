# -*- encoding: utf-8 -*-

from re import search
import pathlib

from py_dss_toolkit.studies.SnapShotPowerFlow.StudySnapShotPowerFlow import StudySnapShotPowerFlow
from py_dss_toolkit.studies.TimeSeriesPowerFlow.StudyTimeSeriesPowerFlow import StudyTimeSeriesPowerFlow
from py_dss_toolkit.studies.StudyFault import StudyFault
from py_dss_toolkit.studies.StudyModelVerification import StudyModelVerification

from typing import Optional, Union


# TODO
# def check_scenario_exist(sc) -> bool:
#     return isinstance(sc, Scenario)

class CreateStudy:
    @staticmethod
    def snapshot(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: [int, float] = 60,
        dss_dll: Optional[str] = None) -> StudySnapShotPowerFlow:
        sc = StudySnapShotPowerFlow(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc

    @staticmethod
    def timeseries(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: [int, float] = 60,
        dss_dll: Optional[str] = None) -> StudyTimeSeriesPowerFlow:
        sc = StudyTimeSeriesPowerFlow(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc

    # @staticmethod
    # def fault_study(
    #     name: str,
    #     dss_file: Union[str, pathlib.Path],
    #     base_frequency: [int, float] = 60,
    #     dss_dll: Optional[str] = None) -> StudyFault:
    #     sc = StudyFault(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
    #     return sc

    @staticmethod
    def model_verification(
        name: str,
        dss_file: Union[str, pathlib.Path],
        base_frequency: [int, float] = 60,
        dss_dll: Optional[str] = None) -> StudyModelVerification:
        sc = StudyModelVerification(_name=name, _dss_file=dss_file, _base_frequency=base_frequency, _dss_dll=dss_dll)
        return sc


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

def solve_scenario(sc):
    sc.__dss.text("solve")
