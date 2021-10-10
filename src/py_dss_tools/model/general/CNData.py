# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:08:17
 Project: py_dss_tools [set, 2021]
"""


class CNData:
    name = "CNData"
    name_plural = "CNData"
    columns = ['capradius', 'diacable', 'diains', 'diam', 'diastrand', 'emergamps', 'epsr', 'gmrac', 'gmrstrand',
               'gmrunits', 'inslayer', 'k', 'like', 'normamps', 'rac', 'radius', 'radunits', 'ratings', 'rdc',
               'rstrand', 'runits', 'seasons']

    def __init__(self):
        self.__capradius = None
        self.__diacable = None
        self.__diains = None
        self.__diam = None
        self.__diastrand = None
        self.__emergamps = None
        self.__epsr = None
        self.__gmrac = None
        self.__gmrstrand = None
        self.__gmrunits = None
        self.__inslayer = None
        self.__k = None
        self.__normamps = None
        self.__rac = None
        self.__radius = None
        self.__radunits = None
        self.__ratings = None
        self.__rdc = None
        self.__rstrand = None
        self.__runits = None
        self.__seasons = None

    @property
    def capradius(self):
        return self.__capradius

    @capradius.setter
    def capradius(self, value):
        self.__capradius = value

    @property
    def diacable(self):
        return self.__diacable

    @diacable.setter
    def diacable(self, value):
        self.__diacable = value

    @property
    def diains(self):
        return self.__diains

    @diains.setter
    def diains(self, value):
        self.__diains = value

    @property
    def diam(self):
        return self.__diam

    @diam.setter
    def diam(self, value):
        self.__diam = value

    @property
    def diastrand(self):
        return self.__diastrand

    @diastrand.setter
    def diastrand(self, value):
        self.__diastrand = value

    @property
    def emergamps(self):
        return self.__emergamps

    @emergamps.setter
    def emergamps(self, value):
        self.__emergamps = value

    @property
    def epsr(self):
        return self.__epsr

    @epsr.setter
    def epsr(self, value):
        self.__epsr = value

    @property
    def gmrac(self):
        return self.__gmrac

    @gmrac.setter
    def gmrac(self, value):
        self.__gmrac = value

    @property
    def gmrstrand(self):
        return self.__gmrstrand

    @gmrstrand.setter
    def gmrstrand(self, value):
        self.__gmrstrand = value

    @property
    def gmrunits(self):
        return self.__gmrunits

    @gmrunits.setter
    def gmrunits(self, value):
        self.__gmrunits = value

    @property
    def inslayer(self):
        return self.__inslayer

    @inslayer.setter
    def inslayer(self, value):
        self.__inslayer = value

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, value):
        self.__k = value

    @property
    def normamps(self):
        return self.__normamps

    @normamps.setter
    def normamps(self, value):
        self.__normamps = value

    @property
    def rac(self):
        return self.__rac

    @rac.setter
    def rac(self, value):
        self.__rac = value

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        self.__radius = value

    @property
    def radunits(self):
        return self.__radunits

    @radunits.setter
    def radunits(self, value):
        self.__radunits = value

    @property
    def ratings(self):
        return self.__ratings

    @ratings.setter
    def ratings(self, value):
        self.__ratings = value

    @property
    def rdc(self):
        return self.__rdc

    @rdc.setter
    def rdc(self, value):
        self.__rdc = value

    @property
    def rstrand(self):
        return self.__rstrand

    @rstrand.setter
    def rstrand(self, value):
        self.__rstrand = value

    @property
    def runits(self):
        return self.__runits

    @runits.setter
    def runits(self, value):
        self.__runits = value

    @property
    def seasons(self):
        return self.__seasons

    @seasons.setter
    def seasons(self, value):
        self.__seasons = value
