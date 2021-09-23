# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:06:05
 Project: py_dss_tools [set, 2021]
"""


class InvControl:
    name = "InvControl"
    name_plural = "InvControls"
    columns = ['activepchangetolerance', 'argrahiv', 'argralowv', 'avgwindowlen', 'basefreq', 'combimode', 'dbvmax',
               'dbvmin', 'deltap_factor', 'deltaq_factor', 'derlist', 'dynreacavgwindowlen', 'enabled', 'eventlog',
               'hysteresis_offset', 'like', 'lpftau', 'mode', 'monbus', 'monbusesvbase', 'monvoltagecalc',
               'pvsystemlist', 'rateofchangemode', 'refreactivepower', 'risefalllimit', 'varchangetolerance',
               'voltage_curvex_ref', 'voltagechangetolerance', 'voltwatt_curve', 'voltwattch_curve', 'voltwattyaxis',
               'vv_refreactivepower', 'vvc_curve1', 'wattpf_curve', 'wattvar_curve']

    def __init__(self):
        pass
