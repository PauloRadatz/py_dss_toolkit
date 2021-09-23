# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 04/09/2021 at 20:38:47
 Project: py_dss_tools [set, 2021]
"""


class Generator:
    name = "Generator"
    name_plural = "Generators"
    columns = ['%fuel', '%reserve', 'balanced', 'basefreq', 'bus1', 'class', 'conn', 'd', 'daily', 'debugtrace',
               'dispmode', 'dispvalue', 'duty', 'dutystart', 'enabled', 'forceon', 'fuelkwh', 'h', 'kv', 'kva', 'kvar',
               'kw', 'like', 'maxkvar', 'minkvar', 'model', 'mva', 'pf', 'phases', 'pvfactor', 'refuel', 'rneut',
               'shaftdata', 'shaftmodel', 'spectrum', 'status', 'usefuel', 'userdata', 'usermodel', 'vmaxpu', 'vminpu',
               'vpu', 'xd', 'xdp', 'xdpp', 'xneut', 'xrdp', 'yearly']

    def __init__(self):
        pass
