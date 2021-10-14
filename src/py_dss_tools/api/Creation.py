# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 09/10/2021 at 01:07:44
 Project: py-dss-tools [out, 2021]
"""
from re import search

from py_dss_tools.model.pdelement import Line
from py_dss_tools.model.pdelement import Transformer
from py_dss_tools.secondary import Scenario, Circuit


# TODO
def check_scenario_exist(sc) -> bool:
    return isinstance(sc, Scenario)


# TODO
def check_circuit_exist(circuit) -> bool:
    return isinstance(circuit, Circuit)


def create_scenario(name: str, frequency_base: [int, float] = 60, **kwargs) -> [object, Scenario]:
    """Create a scenario to starts work with OpenDSS."""
    try:
        sc = Scenario(name=name, frequency_base=frequency_base)
        sc = treat_object(obj=sc, kwargs=kwargs)
        return sc
    except Exception as e:
        print(f"Error when tried to create a Scenario! {e}")


def create_circuit(sc: Scenario, name: str, basekv: [int, float] = 115, bus1: str = 'sourcebus',
                   pu: [int, float] = 1.0001, phases: int = 3, angle: [int, float] = 0,
                   **kwargs) -> bool:
    if check_scenario_exist(sc):
        try:
            circuit = Circuit(name=name, basekv=basekv, bus1=bus1, pu=pu, phases=phases, angle=angle)
            sc.circuit = treat_object(obj=circuit, kwargs=kwargs)
            return True
        except Exception as e:
            print(f"Error when tried to create a Circuit {e.message}")
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


def add_line(sc: Scenario, line: Line) -> bool:
    if not isinstance(line, Line):
        return False
    try:
        sc.lines = line
        return True
    except Exception as e:
        print(f"Error when tried to attribute line to a Cictuit! {e.message}")


def add_transformer(sc: Scenario, trafo: Transformer) -> bool:
    if not isinstance(trafo, Transformer):
        return False
    try:
        sc.transformers = trafo
        return True
    except Exception as e:
        print(f"Error when tried to attribute transformer to a Cictuit! {e.message}")


def create_line(sc: Scenario, name: str, bus1: str, bus2: str, **kwargs) -> bool:
    try:
        line = Line(name=name, bus1=bus1, bus2=bus2)
        sc.lines = treat_object(obj=line, kwargs=kwargs)
        return True
    except Exception as e:
        print(e)
        return False


def create_transformer(sc: Scenario, name: str, **kwargs) -> bool:
    try:
        trafo = Transformer(name=name)
        sc.transformers = treat_object(obj=trafo, kwargs=kwargs)
        return True
    except Exception as e:
        print(e)
        return False


def __translate_lines(sc: Scenario):
    list_name_attr = generate_list_keys_without_(Line())
    result = ''
    for line in sc.lines.iterrows():
        name = ''
        for idx, v in enumerate(line[1].values):
            if v in ['', '[]']:
                continue
            if isinstance(v, str) and list_name_attr[idx] != 'name':
                v = f"'{v}'"
            if list_name_attr[idx] == 'name':
                name = v
                continue
            attribute_name = list_name_attr[idx]
            attribute_value = v
            result += f"{attribute_name}={attribute_value} "

        result = f"new line.{name} {result}"
        sc.dss.text(result)


def __translate_transformers(sc: Scenario):
    list_name_attr = generate_list_keys_without_(Transformer())
    result = ''
    for trafo in sc.transformers.iterrows():
        trafo_name = ''
        for idx, v in enumerate(trafo[1].values):
            attribute_name = list_name_attr[idx]
            attribute_value = v

            if search('ppmantifloat', attribute_name):
                attribute_name = 'ppm_antifloat'

            if attribute_value in ['', '[]']:
                continue

            if attribute_name == 'name':
                trafo_name = attribute_value
                continue

            if isinstance(attribute_value, str) and attribute_name != 'name':
                attribute_value = f"'{attribute_value}'"

            result += f"{attribute_name}={attribute_value} "

        result = f"new transformer.{trafo_name} {result}"
        print(result)
        try:
            sc.dss.text(result)
        except Exception as e:
            print(f"Error when tried to add a trafo! {e}")


def __translate_pdelements(sc: Scenario):
    # autotrans capacitor gictransformer reactor
    __translate_lines(sc)
    __translate_transformers(sc)


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
    sc.dss.text("solve")
