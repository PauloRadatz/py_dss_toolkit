# -*- encoding: utf-8 -*-
"""
 Created by Ênio Viana at 22/09/2021 at 23:05:17
 Project: py_dss_tools [set, 2021]
"""
from dataclasses import dataclass

from .ControlElement import ControlElement


@dataclass
class CapControl(ControlElement):
    """
    __capacitor: Name of Capacitor element which the CapControl controls. No Default; Must be specified.Do not
    specify the full object name; "Capacitor" is assumed for the object class.  Example: Capacitor=cap1.

    __ctphase: Number of the phase being monitored for CURRENT control or one of {AVG | MAX | MIN} for all phases.
    Default=1. If delta or L-L connection, enter the first or the two phases being monitored [1-2, 2-3, 3-1]. Must be
    less than the number of phases. Does not apply to kvar control which uses all phases by default.

    __ctratio: Ratio of the CT from line amps to control ampere setting for current and kvar control types.

    __deadtime: Dead time after capacitor is turned OFF before it can be turned back ON. Default is 300 sec.

    __delay: Time delay, in seconds, from when the control is armed before it sends out the switching command to turn
    ON.  The control may reset before the action actually occurs. This is used to determine which capacity control will
    act first. Default is 15.  You may specify any floating point number to achieve a model of whatever condition is
    necessary.

    __delayoff: Time delay, in seconds, for control to turn OFF when present state is ON. Default is 15.

    __element: Full object name of the circuit element, typically a line or transformer, to which the capacitor
    control's PT and/or CT are connected.There is no default; must be specified.

    __eventlog: {Yes/True* | No/False} Default is YES for CapControl. Log control actions to Eventlog.

    __offsetting: Value at which the control arms to switch the capacitor OFF. (See help for ONsetting)For Time
    control, is OK to have Off time the next day ( < On time).

    __onsetting: Value at which the control arms to switch the capacitor ON (or ratchet up a step).
    Type of Control:
        Current: Line Amps / CTratio
        Voltage: Line-Neutral (or Line-Line for delta) Volts / PTratio
        kvar:    Total kvar, all phases (3-phase for pos seq model). This is directional.
        PF:      Power Factor, Total power in monitored terminal. Negative for Leading.
        Time:    Hrs from Midnight as a floating point number (decimal). 7:30am would be entered as 7.5.

    __pctminkvar: For PF control option, min percent of total bank kvar at which control will close capacitor switch.
    Default = 50.

    __ptphase: Number of the phase being monitored for VOLTAGE control or one of {AVG | MAX | MIN} for all phases.
    Default=1. If delta or L-L connection, enter the first or the two phases being monitored [1-2, 2-3, 3-1]. Must be
    less than the number of phases. Does not apply to kvar control which uses all phases by default.

    __ptratio: Ratio of the PT that converts the monitored voltage to the control voltage. Default is 60.  If the
    capacitor is Wye, the 1st phase line-to-neutral voltage is monitored.  Else, the line-to-line voltage (1st - 2nd
    phase) is monitored.

    __reset: {Yes | No} If Yes, forces Reset of this CapControl.

    __terminal: Number of the terminal of the circuit element to which the CapControl is connected. 1 or 2, typically.
    Default is 1.

    __type: {Current | voltage | kvar | PF | time } Control type.  Specify the ONsetting and OFFsetting appropriately
    with the type of control. (See help for ONsetting).

    __userdata: String (in quotes or parentheses if necessary) that gets passed to the user-written CapControl model
    Edit function for defining the data required for that model.

    __usermodel: Name of DLL containing user-written CapControl model, overriding the default model.  Set to "none" to
    negate previous setting.

    __vbus: Name of bus to use for voltage override function. Default is bus at monitored terminal. Sometimes it is
    useful to monitor a bus in another location to emulate various DMS control algorithms.

    __vmax: Maximum voltage, in volts.  If the voltage across the capacitor divided by the PTRATIO is greater than this
    voltage, the capacitor will switch OFF regardless of other control settings. Default is 126 (goes with a PT ratio
    of 60 for 12.47 kV system).

    __vmin: Minimum voltage, in volts.  If the voltage across the capacitor divided by the PTRATIO is less than this
    voltage, the capacitor will switch ON regardless of other control settings. Default is 115 (goes with a PT ratio of
    60 for 12.47 kV system).

    __voltoverride: {Yes | No}  Default is No.  Switch to indicate whether VOLTAGE OVERRIDE is to be considered. Vmax
    and Vmin must be set to reasonable values if this property is Yes.
    """
    name = "CapControl"
    name_plural = "CapControls"
    columns = ['basefreq', 'capacitor', 'ctphase', 'ctratio', 'deadtime', 'delay', 'delayoff', 'element', 'enabled',
               'eventlog', 'like', 'offsetting', 'onsetting', 'pctminkvar', 'ptphase', 'ptratio', 'reset', 'terminal',
               'type', 'userdata', 'usermodel', 'vbus', 'vmax', 'vmin', 'voltoverride']

    # TODO: we must test it, there is no default value in documentation
    __capacitor: str = ''
    __ctphase: int = 1
    # TODO: what is the default value!?
    __ctratio: float = 1
    __deadtime: int = 300
    __delay: int = 15
    __delayoff: int = 15
    __element: str = ''
    __eventlog: str = 'yes'

    # TODO: what is the default value!?
    __offsetting: str = ''
    # TODO: what is the default value!?
    __onsetting: str = ''
    __pctminkvar: float = 50
    __ptphase: int = 1
    __ptratio: float = 60
    __reset: str = ''
    __terminal: int = 1
    # TODO: we must define a enum
    __type: str = ''
    __userdata: str = ''
    __usermodel: str = ''
    __vbus: str = ''
    __vmax: float = 126
    __vmin: float = 115
    __voltoverride: str = 'No'

    @property
    def capacitor(self):
        return self.__capacitor

    @capacitor.setter
    def capacitor(self, value):
        self.__capacitor = value

    @property
    def ctphase(self):
        return self.__ctphase

    @ctphase.setter
    def ctphase(self, value):
        self.__ctphase = value

    @property
    def ctratio(self):
        return self.__ctratio

    @ctratio.setter
    def ctratio(self, value):
        self.__ctratio = value

    @property
    def deadtime(self):
        return self.__deadtime

    @deadtime.setter
    def deadtime(self, value):
        self.__deadtime = value

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def delayoff(self):
        return self.__delayoff

    @delayoff.setter
    def delayoff(self, value):
        self.__delayoff = value

    @property
    def element(self):
        return self.__element

    @element.setter
    def element(self, value):
        self.__element = value

    @property
    def eventlog(self):
        return self.__eventlog

    @eventlog.setter
    def eventlog(self, value):
        self.__eventlog = value

    @property
    def offsetting(self):
        return self.__offsetting

    @offsetting.setter
    def offsetting(self, value):
        self.__offsetting = value

    @property
    def onsetting(self):
        return self.__onsetting

    @onsetting.setter
    def onsetting(self, value):
        self.__onsetting = value

    @property
    def pctminkvar(self):
        return self.__pctminkvar

    @pctminkvar.setter
    def pctminkvar(self, value):
        self.__pctminkvar = value

    @property
    def ptphase(self):
        return self.__ptphase

    @ptphase.setter
    def ptphase(self, value):
        self.__ptphase = value

    @property
    def ptratio(self):
        return self.__ptratio

    @ptratio.setter
    def ptratio(self, value):
        self.__ptratio = value

    @property
    def reset(self):
        return self.__reset

    @reset.setter
    def reset(self, value):
        self.__reset = value

    @property
    def terminal(self):
        return self.__terminal

    @terminal.setter
    def terminal(self, value):
        self.__terminal = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def userdata(self):
        return self.__userdata

    @userdata.setter
    def userdata(self, value):
        self.__userdata = value

    @property
    def usermodel(self):
        return self.__usermodel

    @usermodel.setter
    def usermodel(self, value):
        self.__usermodel = value

    @property
    def vbus(self):
        return self.__vbus

    @vbus.setter
    def vbus(self, value):
        self.__vbus = value

    @property
    def vmax(self):
        return self.__vmax

    @vmax.setter
    def vmax(self, value):
        self.__vmax = value

    @property
    def vmin(self):
        return self.__vmin

    @vmin.setter
    def vmin(self, value):
        self.__vmin = value

    @property
    def voltoverride(self):
        return self.__voltoverride

    @voltoverride.setter
    def voltoverride(self, value):
        self.__voltoverride = value
