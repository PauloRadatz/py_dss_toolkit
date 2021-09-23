# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:51
 Project: py_dss_tools [set, 2021]
"""


class StorageController:
    name = "StorageController"
    name_plural = "StorageControllers"
    columns = ['%kwband', '%kwbandlow', '%ratecharge', '%ratekw', '%reserve', 'basefreq', 'daily', 'dispfactor', 'duty',
               'element', 'elementlist', 'enabled', 'eventlog', 'inhibittime', 'kwactual', 'kwband', 'kwbandlow',
               'kwhactual', 'kwhtotal', 'kwneed', 'kwtarget', 'kwtargetlow', 'kwthreshold', 'kwtotal', 'like',
               'modecharge', 'modedischarge', 'monphase', 'resetlevel', 'seasons', 'seasontargets', 'seasontargetslow',
               'tdn', 'terminal', 'tflat', 'timechargetrigger', 'timedischargetrigger', 'tup', 'weights', 'yearly']

    def __init__(self):
        pass
