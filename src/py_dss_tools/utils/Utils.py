# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 03:26:21
 Project: py_dss_tools [set, 2021]
"""
import random
import string
from inspect import currentframe


class Utils:
    @staticmethod
    def get_linenumber():
        cf = currentframe()
        return cf.f_back.f_lineno

    @staticmethod
    def remove_blank_spaces(content: str):
        content = content.lower()
        return content.replace(" ", "_")

    @staticmethod
    def generate_random_string():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
