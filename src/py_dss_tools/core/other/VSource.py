# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:11:52
 Project: py_dss_tools [set, 2021]
"""
from .OtherElement import Other


class VSource(Other):
    name = "VSource"
    name_plural = "VSources"
    columns = ['angle', 'basefreq', 'basekv', 'basemva', 'bus1', 'bus2', 'daily', 'duty', 'enabled', 'frequency',
               'isc1', 'isc3', 'like', 'model', 'mvasc1', 'mvasc3', 'phases', 'pu', 'puz0', 'puz1', 'puz2', 'puzideal',
               'r0', 'r1', 'scantype', 'sequence', 'spectrum', 'x0', 'x0r0', 'x1', 'x1r1', 'yearly', 'z0', 'z1', 'z2']

    # TODO: A proposta é criar um list com os valores default, criat todos os atributos dinamicamente no init e usar
    #  property para o autocomplete funcionar
    # values = ['0', '115', '60']

    def __init__(self):
        super().__init__()
        self.__angle = 0
        self.__basekv = ''
        self.__basemva = ''
        self.__bus1 = ''
        self.__bus2 = ''
        self.__daily = ''
        self.__duty = ''
        self.__frequency = 60
        self.__isc1 = ''
        self.__isc3 = ''
        self.__model = 'Thevenin'
        self.__mvasc1 = 21000
        self.__mvasc3 = 20000
        self.__pu = 1.0001
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

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        self.__angle = value

    @property
    def basekv(self):
        return self.__basekv

    @basekv.setter
    def basekv(self, value):
        self.__basekv = value

    @property
    def basemva(self):
        return self.__basemva

    @basemva.setter
    def basemva(self, value):
        self.__basemva = value

    @property
    def bus1(self):
        return self.__bus1

    @bus1.setter
    def bus1(self, value):
        self.__bus1 = value

    @property
    def bus2(self):
        return self.__bus2

    @bus2.setter
    def bus2(self, value):
        self.__bus2 = value

    @property
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @property
    def isc1(self):
        return self.__isc1

    @isc1.setter
    def isc1(self, value):
        self.__isc1 = value

    @property
    def isc3(self):
        return self.__isc3

    @isc3.setter
    def isc3(self, value):
        self.__isc3 = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def mvasc1(self):
        return self.__mvasc1

    @mvasc1.setter
    def mvasc1(self, value):
        self.__mvasc1 = value

    @property
    def mvasc3(self):
        return self.__mvasc3

    @mvasc3.setter
    def mvasc3(self, value):
        self.__mvasc3 = value

    @property
    def pu(self):
        return self.__pu

    @pu.setter
    def pu(self, value):
        self.__pu = value

    @property
    def puz0(self):
        return self.__puz0

    @puz0.setter
    def puz0(self, value):
        self.__puz0 = value

    @property
    def puz1(self):
        return self.__puz1

    @puz1.setter
    def puz1(self, value):
        self.__puz1 = value

    @property
    def puz2(self):
        return self.__puz2

    @puz2.setter
    def puz2(self, value):
        self.__puz2 = value

    @property
    def puzideal(self):
        return self.__puzideal

    @puzideal.setter
    def puzideal(self, value):
        self.__puzideal = value

    @property
    def r0(self):
        return self.__r0

    @r0.setter
    def r0(self, value):
        self.__r0 = value

    @property
    def r1(self):
        return self.__r1

    @r1.setter
    def r1(self, value):
        self.__r1 = value

    @property
    def scantype(self):
        return self.__scantype

    @scantype.setter
    def scantype(self, value):
        self.__scantype = value

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self, value):
        self.__sequence = value

    @property
    def spectrum(self):
        return self.__spectrum

    @spectrum.setter
    def spectrum(self, value):
        self.__spectrum = value

    @property
    def x0(self):
        return self.__x0

    @x0.setter
    def x0(self, value):
        self.__x0 = value

    @property
    def x0r0(self):
        return self.__x0r0

    @x0r0.setter
    def x0r0(self, value):
        self.__x0r0 = value

    @property
    def x1(self):
        return self.__x1

    @x1.setter
    def x1(self, value):
        self.__x1 = value

    @property
    def x1r1(self):
        return self.__x1r1

    @x1r1.setter
    def x1r1(self, value):
        self.__x1r1 = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value

    @property
    def z0(self):
        return self.__z0

    @z0.setter
    def z0(self, value):
        self.__z0 = value

    @property
    def z1(self):
        return self.__z1

    @z1.setter
    def z1(self, value):
        self.__z1 = value

    @property
    def z2(self):
        return self.__z2

    @z2.setter
    def z2(self, value):
        self.__z2 = value

# self.__angle = '0'
# self.__basekv = basekv
# self.__basefreq = '60'
# self.__basemva = '100'
# self.__bus1 = 'sourcebus'
# self.__bus2 = 'sourcebus.0.0.0'
# self.__daily = ''
# self.__duty = ''
# self.__enabled = 'true'
# self.__frequency = '60'
# self.__isc1 = ''
# self.__isc3 = ''
# self.__like = ''
# self.__model = 'Thevenin'
# self.__mvasc1 = '21000'
# self.__mvasc3 = '20000'
# self.__name = name
# self.__phases = '3'
# self.__pu = '1.0001'
# self.__puz0 = ''
# self.__puz1 = ''
# self.__puz2 = ''
# self.__puzideal = ''
# self.__r0 = ''
# self.__r1 = ''
# self.__scantype = 'Pos'
# self.__sequence = 'Pos'
# self.__spectrum = 'defaultvsource'
# self.__x0 = ''
# self.__x0r0 = ''
# self.__x1 = ''
# self.__x1r1 = ''
# self.__yearly = ''
# self.__z0 = ''
# self.__z1 = ''
# self.__z2 = ''

# def __str__(self):
#     output = ""
#     for _, var in vars(self).items():
#         output += str(var) + "\n"
#     return output
