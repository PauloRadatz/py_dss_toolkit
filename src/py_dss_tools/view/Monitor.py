# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : Monitor.py
# @Software: PyCharm

from py_dss_tools.results.TemporalResults import TemporalResults
import matplotlib.pyplot as plt
from py_dss_interface import DSS


class Monitor:

    def __init__(self, dss: DSS, results: TemporalResults):
        self._results = results
        self._dss = dss

    def monitor(self, name: str):
        df = self._results.monitor(name)[(name, 0)]

        plt.figure(figsize=(10, 6))
        plt.xlabel('Distance')
        plt.ylabel('Voltage (pu)')
        plt.title('Voltage Profile')
        plt.xticks(rotation=45)

        plt.plot(df["Hour"], df[" V1"])

        plt.grid(True)
        plt.tight_layout()

        plt.show()
