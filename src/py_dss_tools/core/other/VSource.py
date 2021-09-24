# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:52
 Project: py_dss_tools [set, 2021]
"""


class VSource:
    name = "VSource"
    name_plural = "VSources"
    columns = ['angle', 'basefreq', 'basekv', 'basemva', 'bus1', 'bus2', 'daily', 'duty', 'enabled', 'frequency',
               'isc1', 'isc3', 'like', 'model', 'mvasc1', 'mvasc3', 'phases', 'pu', 'puz0', 'puz1', 'puz2', 'puzideal',
               'r0', 'r1', 'scantype', 'sequence', 'spectrum', 'x0', 'x0r0', 'x1', 'x1r1', 'yearly', 'z0', 'z1', 'z2']

    # TODO: A proposta é criar um list com os valores default, criat todos os atributos dinamicamente no init e usar
    #  property para o autocomplete funcionar
    values = ['0', '115', '60']

    def __init__(self, basekv="115", name="MY_Vsource"):
        self.__angle = '0'
        self.__basekv = basekv
        self.__basefreq = '60'
        self.__basemva = '100'
        self.__bus1 = 'sourcebus'
        self.__bus2 = 'sourcebus.0.0.0'
        self.__daily = ''
        self.__duty = ''
        self.__enabled = 'true'
        self.__frequency = '60'
        self.__isc1 = ''
        self.__isc3 = ''
        self.__like = ''
        self.__model = 'Thevenin'
        self.__mvasc1 = '21000'
        self.__mvasc3 = '20000'
        self.__name = name
        self.__phases = '3'
        self.__pu = '1.0001'
        self.__puz0 = ''
        self.__puz1 = ''
        self.__puz2 = ''
        self.__puzideal = ''
        self.__r0 = ''
        self.__r1 = ''
        self.__scantype = 'Pos'
        self.__sequence = 'Pos'
        self.__spectrum = 'defaultvsource'
        self.__x0 = ''
        self.__x0r0 = ''
        self.__x1 = ''
        self.__x1r1 = ''
        self.__yearly = ''
        self.__z0 = ''
        self.__z1 = ''
        self.__z2 = ''

    # def __str__(self):
    #     output = ""
    #     for _, var in vars(self).items():
    #         output += str(var) + "\n"
    #     return output
