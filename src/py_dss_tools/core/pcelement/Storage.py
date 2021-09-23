# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:41
 Project: py_dss_tools [set, 2021]
"""


class Storage:
    name = "Storage"
    name_plural = "Storages"
    columns = ['%charge', '%cutin', '%cutout', '%discharge', '%effcharge', '%effdischarge', '%idlingkvar', '%idlingkw',
               '%kwrated', '%pminkvarmax', '%pminnovars', '%r', '%reserve', '%stored', '%x', 'balanced', 'basefreq',
               'bus1', 'chargetrigger', 'class', 'conn', 'daily', 'debugtrace', 'dischargetrigger', 'dispmode', 'duty',
               'dynadata', 'dynadll', 'effcurve', 'enabled', 'kv', 'kva', 'kvar', 'kvarmax', 'kvarmaxabs', 'kw',
               'kwhrated', 'kwhstored', 'kwrated', 'like', 'limitcurrent', 'model', 'pf', 'pfpriority', 'phases',
               'spectrum', 'state', 'timechargetrig', 'userdata', 'usermodel', 'varfollowinverter', 'vmaxpu', 'vminpu',
               'wattpriority', 'yearly']

    def __init__(self):
        pass
