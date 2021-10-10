# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 03/10/2021 at 19:38:16
 Project: py-dss-tools [out, 2021]
"""


class Linha:
    @staticmethod
    def falar():
        return "Sou uma linha"


class Reator:
    @staticmethod
    def falar():
        return "Sou um reator"


class PDElementFactory:

    @staticmethod
    def create(tipo: str):
        return eval(tipo).falar()


print(PDElementFactory.create("Linha"))
print(PDElementFactory.create("Reator"))
