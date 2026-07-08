# -*- encoding: utf-8 -*-
"""
Created by Ênio Viana at 04/09/2021 at 03:26:21
Project: py_dss_toolkit [set, 2021]
"""

import random
import string
from inspect import currentframe
from typing import List
from typing import Union


class Utils:
    @staticmethod
    def get_linenumber():
        cf = currentframe()
        return cf.f_back.f_lineno

    @staticmethod
    def remove_blank_spaces(content: str):
        if isinstance(content, str):
            content = content.lower()
            return content.replace(" ", "_")
        return

    @staticmethod
    def generate_random_string():
        return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))

    @staticmethod
    def check_instance(value: Union[str, float, int], property_name: str, type_: List[str]) -> None:
        if type(value).__name__ not in type_:
            raise TypeError(f"Type error for {property_name}. Expected one of {type_}, but found {type(value)}.")
