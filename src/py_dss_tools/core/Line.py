# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:39:04
 Project: py_dss_tools [set, 2021]
"""
from .Scenario import Scenario


class Line:

    def __init__(self, scenario: Scenario, name_, from_, to_, **kwargs):
        """
        :param scenario:
        :param name_:
        :param from_:
        :param to_:
        :param kwargs:
        """

        if scenario.line_exist():
            print('Line already exist')
            exit()
        else:
            self.name_ = name_
            self.from_ = int(from_)
            self.to = int(to_)

            self.phases = 3
            self.line_code = ''
            self.length = 1.0
            self.units = 'm'
            self.base_freq = 60

            # TODO - doubt
            self.c0 = ''
            self.c1 = ''

            value = "new line.{0} bus1={1} bus2={2}".format(self.name_, int(self.from_), int(self.to))

            if 'phases' in kwargs:
                self.phases = kwargs.get('phases')
                value = value + " phases={0}".format(self.phases)
            if 'line_code' in kwargs:
                self.line_code = kwargs.get('line_code')
                value = value + " line_code={0}".format(self.line_code)
            if 'units' in kwargs:
                self.units = kwargs.get('units')
                value = value + " units={0}".format(self.units)
            if 'base_freq' in kwargs:
                self.base_freq = kwargs.get('base_freq')
                value = value + " base_freq={0}".format(self.base_freq)
            #
            # for index, value_ in kwargs:
            #     value = value + " {0}={0}".format(index, value_)

            scenario.dss.text(value)
            # scenario.dss.text(
            #     "new line.{0} phases={1} bus1={2} bus2={3} linecode={4} length={5} units={6}".format(self.name_,
            #                                                                                          self.phases,
            #                                                                                          self.from_,
            #                                                                                          self.to,
            #                                                                                          self.line_code,
            #                                                                                          self.length,
            #                                                                                          self.units))

    def __str__(self):
        return self.name_ + " " + str(self.from_) + " " + str(self.to) + " " + str(self.line_code) + " " + str(
            self.length) + "" + str(self.units) + " " + str(self.base_freq) + " " + str(self.phases)
