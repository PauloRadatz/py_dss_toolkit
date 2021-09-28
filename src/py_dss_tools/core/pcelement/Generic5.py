# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:03:07
 Project: py_dss_tools [set, 2021]
"""
from .PCElement import PCElement


class Generic5(PCElement):
    name = "Generic5"
    name_plural = "Generic5s"
    columns = ['basefreq', 'bus1', 'cc_switch', 'cluster_num', 'conn', 'ctrl_mode', 'd', 'daily', 'debugtrace', 'droop',
               'duty', 'enabled', 'h', 'kcd', 'kcq', 'kcq_drp2', 'kqi', 'kv', 'kva', 'kw', 'like', 'maxslip',
               'p_ref1kw', 'p_ref2kw', 'p_ref3kw', 'p_refkw', 'pbiaskw', 'pf', 'pfctr1', 'pfctr2', 'pfctr3', 'pfctr4',
               'pfctr5', 'pfctr6', 'phases', 'pmaxkw', 'pminkw', 'pmppkw', 'pqpriority', 'q_ref1kvar', 'q_ref2kvar',
               'q_ref3kvar', 'q_refkvar', 'qv_flag', 'slipoption', 'spectrum', 'v_ref1kvln', 'v_ref2kvln', 'v_ref3kvln',
               'v_refkvln', 'volt_trhd', 'yearly']

    def __init__(self):
        super().__init__()
        self.__cc_switch = None
        self.__cluster_num = None
        self.__conn = None
        self.__ctrl_mode = None
        self.__d = None
        self.__daily = None
        self.__debugtrace = None
        self.__droop = None
        self.__duty = None
        self.__h = None
        self.__kcd = None
        self.__kcq = None
        self.__kcq_drp2 = None
        self.__kqi = None
        self.__kv = None
        self.__kva = None
        self.__kw = None
        self.__maxslip = None
        self.__p_ref1kw = None
        self.__p_ref2kw = None
        self.__p_ref3kw = None
        self.__p_refkw = None
        self.__pbiaskw = None
        self.__pf = None
        self.__pfctr1 = None
        self.__pfctr2 = None
        self.__pfctr3 = None
        self.__pfctr4 = None
        self.__pfctr5 = None
        self.__pfctr6 = None
        self.__pmaxkw = None
        self.__pminkw = None
        self.__pmppkw = None
        self.__pqpriority = None
        self.__q_ref1kvar = None
        self.__q_ref2kvar = None
        self.__q_ref3kvar = None
        self.__q_refkvar = None
        self.__qv_flag = None
        self.__slipoption = None
        self.__v_ref1kvln = None
        self.__v_ref2kvln = None
        self.__v_ref3kvln = None
        self.__v_refkvln = None
        self.__volt_trhd = None
        self.__yearly = None

    @property
    def cc_switch(self):
        return self.__cc_switch

    @cc_switch.setter
    def cc_switch(self, value):
        self.__cc_switch = value

    @property
    def cluster_num(self):
        return self.__cluster_num

    @cluster_num.setter
    def cluster_num(self, value):
        self.__cluster_num = value

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, value):
        self.__conn = value

    @property
    def ctrl_mode(self):
        return self.__ctrl_mode

    @ctrl_mode.setter
    def ctrl_mode(self, value):
        self.__ctrl_mode = value

    @property
    def d(self):
        return self.__d

    @d.setter
    def d(self, value):
        self.__d = value

    @property
    def daily(self):
        return self.__daily

    @daily.setter
    def daily(self, value):
        self.__daily = value

    @property
    def debugtrace(self):
        return self.__debugtrace

    @debugtrace.setter
    def debugtrace(self, value):
        self.__debugtrace = value

    @property
    def droop(self):
        return self.__droop

    @droop.setter
    def droop(self, value):
        self.__droop = value

    @property
    def duty(self):
        return self.__duty

    @duty.setter
    def duty(self, value):
        self.__duty = value

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        self.__h = value

    @property
    def kcd(self):
        return self.__kcd

    @kcd.setter
    def kcd(self, value):
        self.__kcd = value

    @property
    def kcq(self):
        return self.__kcq

    @kcq.setter
    def kcq(self, value):
        self.__kcq = value

    @property
    def kcq_drp2(self):
        return self.__kcq_drp2

    @kcq_drp2.setter
    def kcq_drp2(self, value):
        self.__kcq_drp2 = value

    @property
    def kqi(self):
        return self.__kqi

    @kqi.setter
    def kqi(self, value):
        self.__kqi = value

    @property
    def kv(self):
        return self.__kv

    @kv.setter
    def kv(self, value):
        self.__kv = value

    @property
    def kva(self):
        return self.__kva

    @kva.setter
    def kva(self, value):
        self.__kva = value

    @property
    def kw(self):
        return self.__kw

    @kw.setter
    def kw(self, value):
        self.__kw = value

    @property
    def maxslip(self):
        return self.__maxslip

    @maxslip.setter
    def maxslip(self, value):
        self.__maxslip = value

    @property
    def p_ref1kw(self):
        return self.__p_ref1kw

    @p_ref1kw.setter
    def p_ref1kw(self, value):
        self.__p_ref1kw = value

    @property
    def p_ref2kw(self):
        return self.__p_ref2kw

    @p_ref2kw.setter
    def p_ref2kw(self, value):
        self.__p_ref2kw = value

    @property
    def p_ref3kw(self):
        return self.__p_ref3kw

    @p_ref3kw.setter
    def p_ref3kw(self, value):
        self.__p_ref3kw = value

    @property
    def p_refkw(self):
        return self.__p_refkw

    @p_refkw.setter
    def p_refkw(self, value):
        self.__p_refkw = value

    @property
    def pbiaskw(self):
        return self.__pbiaskw

    @pbiaskw.setter
    def pbiaskw(self, value):
        self.__pbiaskw = value

    @property
    def pf(self):
        return self.__pf

    @pf.setter
    def pf(self, value):
        self.__pf = value

    @property
    def pfctr1(self):
        return self.__pfctr1

    @pfctr1.setter
    def pfctr1(self, value):
        self.__pfctr1 = value

    @property
    def pfctr2(self):
        return self.__pfctr2

    @pfctr2.setter
    def pfctr2(self, value):
        self.__pfctr2 = value

    @property
    def pfctr3(self):
        return self.__pfctr3

    @pfctr3.setter
    def pfctr3(self, value):
        self.__pfctr3 = value

    @property
    def pfctr4(self):
        return self.__pfctr4

    @pfctr4.setter
    def pfctr4(self, value):
        self.__pfctr4 = value

    @property
    def pfctr5(self):
        return self.__pfctr5

    @pfctr5.setter
    def pfctr5(self, value):
        self.__pfctr5 = value

    @property
    def pfctr6(self):
        return self.__pfctr6

    @pfctr6.setter
    def pfctr6(self, value):
        self.__pfctr6 = value

    @property
    def pmaxkw(self):
        return self.__pmaxkw

    @pmaxkw.setter
    def pmaxkw(self, value):
        self.__pmaxkw = value

    @property
    def pminkw(self):
        return self.__pminkw

    @pminkw.setter
    def pminkw(self, value):
        self.__pminkw = value

    @property
    def pmppkw(self):
        return self.__pmppkw

    @pmppkw.setter
    def pmppkw(self, value):
        self.__pmppkw = value

    @property
    def pqpriority(self):
        return self.__pqpriority

    @pqpriority.setter
    def pqpriority(self, value):
        self.__pqpriority = value

    @property
    def q_ref1kvar(self):
        return self.__q_ref1kvar

    @q_ref1kvar.setter
    def q_ref1kvar(self, value):
        self.__q_ref1kvar = value

    @property
    def q_ref2kvar(self):
        return self.__q_ref2kvar

    @q_ref2kvar.setter
    def q_ref2kvar(self, value):
        self.__q_ref2kvar = value

    @property
    def q_ref3kvar(self):
        return self.__q_ref3kvar

    @q_ref3kvar.setter
    def q_ref3kvar(self, value):
        self.__q_ref3kvar = value

    @property
    def q_refkvar(self):
        return self.__q_refkvar

    @q_refkvar.setter
    def q_refkvar(self, value):
        self.__q_refkvar = value

    @property
    def qv_flag(self):
        return self.__qv_flag

    @qv_flag.setter
    def qv_flag(self, value):
        self.__qv_flag = value

    @property
    def slipoption(self):
        return self.__slipoption

    @slipoption.setter
    def slipoption(self, value):
        self.__slipoption = value

    @property
    def v_ref1kvln(self):
        return self.__v_ref1kvln

    @v_ref1kvln.setter
    def v_ref1kvln(self, value):
        self.__v_ref1kvln = value

    @property
    def v_ref2kvln(self):
        return self.__v_ref2kvln

    @v_ref2kvln.setter
    def v_ref2kvln(self, value):
        self.__v_ref2kvln = value

    @property
    def v_ref3kvln(self):
        return self.__v_ref3kvln

    @v_ref3kvln.setter
    def v_ref3kvln(self, value):
        self.__v_ref3kvln = value

    @property
    def v_refkvln(self):
        return self.__v_refkvln

    @v_refkvln.setter
    def v_refkvln(self, value):
        self.__v_refkvln = value

    @property
    def volt_trhd(self):
        return self.__volt_trhd

    @volt_trhd.setter
    def volt_trhd(self, value):
        self.__volt_trhd = value

    @property
    def yearly(self):
        return self.__yearly

    @yearly.setter
    def yearly(self, value):
        self.__yearly = value
