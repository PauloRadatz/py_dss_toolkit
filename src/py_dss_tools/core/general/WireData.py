# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:10:04
 Project: py_dss_tools [set, 2021]
"""


class WireData:
    name = "WireData"
    name_plural = "WireData"
    columns = ['capradius', 'diam', 'emergamps', 'gmrac', 'gmrunits', 'like', 'normamps', 'rac', 'radius', 'radunits',
               'ratings', 'rdc', 'runits', 'seasons']

    def __init__(self):
        self.__capradius = None
        self.__diam = None
        self.__emergamps = None
        self.__gmrac = None
        self.__gmrunits = None
        self.__normamps = None
        self.__rac = None
        self.__radius = None
        self.__radunits = None
        self.__ratings = None
        self.__rdc = None
        self.__runits = None
        self.__seasons = None

    @property
    def capradius(self):
        return self.__capradius

    @capradius.setter
    def capradius(self, value):
        self.__capradius = value

    @property
    def diam(self):
        return self.__diam

    @diam.setter
    def diam(self, value):
        self.__diam = value

    @property
    def emergamps(self):
        return self.__emergamps

    @emergamps.setter
    def emergamps(self, value):
        self.__emergamps = value

    @property
    def gmrac(self):
        return self.__gmrac

    @gmrac.setter
    def gmrac(self, value):
        self.__gmrac = value

    @property
    def gmrunits(self):
        return self.__gmrunits

    @gmrunits.setter
    def gmrunits(self, value):
        self.__gmrunits = value

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
