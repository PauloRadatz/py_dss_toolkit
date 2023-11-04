# -*- coding: utf-8 -*-
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : VoltageProfile.py
# @Software: PyCharm

from py_dss_tools.secondary import StudyGeneric
import matplotlib.pyplot as plt

class VoltageProfile:

    def __init__(self, study: StudyGeneric):
        self._study = study
        self._dss = self._study.dss

    def plot_profile(self):
        df = self._study.results.voltages[0]
        buses = [bus.lower().split(".")[0] for bus in self._dss.circuit.buses_names]
        distances = self._dss.circuit.buses_distances

        sections = list()
        self._dss.lines.first()
        for _ in range(self._dss.lines.count):
            sections.append((self._dss.lines.bus1.lower().split(".")[0], self._dss.lines.bus2.lower().split(".")[0]))
            self._dss.lines.next()

        node_colors = {1: 'black', 2: 'red', 3: 'blue'}
        plt.figure(figsize=(10, 6))

        for node in range(1, 4):
            for section in sections:
                bus1, bus2 = section
                distance1 = distances[buses.index(bus1)]
                distance2 = distances[buses.index(bus2)]
                plt.plot([distance1, distance2], [df.loc[bus1, f'node{node}'], df.loc[bus2, f'node{node}']], marker='o',
                         color=node_colors[node])

        plt.xlabel('Distance')
        plt.ylabel('Voltage (pu)')
        plt.title('Voltage Profile')
        plt.xticks(rotation=45)
        plt.legend([f'Node {node}' for node in range(1, 4)])
        plt.grid(True)
        plt.tight_layout()

        plt.show()

        self._dss.text("plot profile phases=all")

