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
        self.__activepchangetolerance = None
        self.__argrahiv = None
        self.__argralowv = None
        self.__avgwindowlen = None
        self.__combimode = None
        self.__dbvmax = None
        self.__dbvmin = None
        self.__deltap_factor = None
        self.__deltaq_factor = None
        self.__derlist = None
        self.__dynreacavgwindowlen = None
        self.__eventlog = None
        self.__hysteresis_offset = None
        self.__lpftau = None
        self.__mode = None
        self.__monbus = None
        self.__monbusesvbase = None
        self.__monvoltagecalc = None
        self.__pvsystemlist = None
        self.__rateofchangemode = None
        self.__refreactivepower = None
        self.__risefalllimit = None
        self.__varchangetolerance = None
        self.__voltage_curvex_ref = None
        self.__voltagechangetolerance = None
        self.__voltwatt_curve = None
        self.__voltwattch_curve = None
        self.__voltwattyaxis = None
        self.__vv_refreactivepower = None
        self.__vvc_curve1 = None
        self.__wattpf_curve = None
        self.__wattvar_curve = None

    @property
    def activepchangetolerance(self):
        return self.__activepchangetolerance

    @activepchangetolerance.setter
    def activepchangetolerance(self, value):
        self.__activepchangetolerance = value

    @property
    def argrahiv(self):
        return self.__argrahiv

    @argrahiv.setter
    def argrahiv(self, value):
        self.__argrahiv = value

    @property
    def argralowv(self):
        return self.__argralowv

    @argralowv.setter
    def argralowv(self, value):
        self.__argralowv = value

    @property
    def avgwindowlen(self):
        return self.__avgwindowlen

    @avgwindowlen.setter
    def avgwindowlen(self, value):
        self.__avgwindowlen = value

    @property
    def combimode(self):
        return self.__combimode

    @combimode.setter
    def combimode(self, value):
        self.__combimode = value

    @property
    def dbvmax(self):
        return self.__dbvmax

    @dbvmax.setter
    def dbvmax(self, value):
        self.__dbvmax = value

    @property
    def dbvmin(self):
        return self.__dbvmin

    @dbvmin.setter
    def dbvmin(self, value):
        self.__dbvmin = value

    @property
    def deltap_factor(self):
        return self.__deltap_factor

    @deltap_factor.setter
    def deltap_factor(self, value):
        self.__deltap_factor = value

    @property
    def deltaq_factor(self):
        return self.__deltaq_factor

    @deltaq_factor.setter
    def deltaq_factor(self, value):
        self.__deltaq_factor = value

    @property
    def derlist(self):
        return self.__derlist

    @derlist.setter
    def derlist(self, value):
        self.__derlist = value

    @property
    def dynreacavgwindowlen(self):
        return self.__dynreacavgwindowlen

    @dynreacavgwindowlen.setter
    def dynreacavgwindowlen(self, value):
        self.__dynreacavgwindowlen = value

    @property
    def eventlog(self):
        return self.__eventlog

    @eventlog.setter
    def eventlog(self, value):
        self.__eventlog = value

    @property
    def hysteresis_offset(self):
        return self.__hysteresis_offset

    @hysteresis_offset.setter
    def hysteresis_offset(self, value):
        self.__hysteresis_offset = value

    @property
    def lpftau(self):
        return self.__lpftau

    @lpftau.setter
    def lpftau(self, value):
        self.__lpftau = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

    @property
    def monbus(self):
        return self.__monbus

    @monbus.setter
    def monbus(self, value):
        self.__monbus = value

    @property
    def monbusesvbase(self):
        return self.__monbusesvbase

    @monbusesvbase.setter
    def monbusesvbase(self, value):
        self.__monbusesvbase = value

    @property
    def monvoltagecalc(self):
        return self.__monvoltagecalc

    @monvoltagecalc.setter
    def monvoltagecalc(self, value):
        self.__monvoltagecalc = value

    @property
    def pvsystemlist(self):
        return self.__pvsystemlist

    @pvsystemlist.setter
    def pvsystemlist(self, value):
        self.__pvsystemlist = value

    @property
    def rateofchangemode(self):
        return self.__rateofchangemode

    @rateofchangemode.setter
    def rateofchangemode(self, value):
        self.__rateofchangemode = value

    @property
    def refreactivepower(self):
        return self.__refreactivepower

    @refreactivepower.setter
    def refreactivepower(self, value):
        self.__refreactivepower = value

    @property
    def risefalllimit(self):
        return self.__risefalllimit

    @risefalllimit.setter
    def risefalllimit(self, value):
        self.__risefalllimit = value

    @property
    def varchangetolerance(self):
        return self.__varchangetolerance

    @varchangetolerance.setter
    def varchangetolerance(self, value):
        self.__varchangetolerance = value

    @property
    def voltage_curvex_ref(self):
        return self.__voltage_curvex_ref

    @voltage_curvex_ref.setter
    def voltage_curvex_ref(self, value):
        self.__voltage_curvex_ref = value

    @property
    def voltagechangetolerance(self):
        return self.__voltagechangetolerance

    @voltagechangetolerance.setter
    def voltagechangetolerance(self, value):
        self.__voltagechangetolerance = value

    @property
    def voltwatt_curve(self):
        return self.__voltwatt_curve

    @voltwatt_curve.setter
    def voltwatt_curve(self, value):
        self.__voltwatt_curve = value

    @property
    def voltwattch_curve(self):
        return self.__voltwattch_curve

    @voltwattch_curve.setter
    def voltwattch_curve(self, value):
        self.__voltwattch_curve = value

    @property
    def voltwattyaxis(self):
        return self.__voltwattyaxis

    @voltwattyaxis.setter
    def voltwattyaxis(self, value):
        self.__voltwattyaxis = value

    @property
    def vv_refreactivepower(self):
        return self.__vv_refreactivepower

    @vv_refreactivepower.setter
    def vv_refreactivepower(self, value):
        self.__vv_refreactivepower = value

    @property
    def vvc_curve1(self):
        return self.__vvc_curve1

    @vvc_curve1.setter
    def vvc_curve1(self, value):
        self.__vvc_curve1 = value

    @property
    def wattpf_curve(self):
        return self.__wattpf_curve

    @wattpf_curve.setter
    def wattpf_curve(self, value):
        self.__wattpf_curve = value

    @property
    def wattvar_curve(self):
        return self.__wattvar_curve

    @wattvar_curve.setter
    def wattvar_curve(self, value):
        self.__wattvar_curve = value
