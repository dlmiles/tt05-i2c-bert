#
#
#
#
#
#
#
#
# SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
# SPDX-License-Identifier: Apache2.0
#
#

from cocotb_stuff import *
from cocotb_stuff.cocotbutil import *
from cocotb_stuff.SignalAccessor import *


class I2CController():
    SIGNAL_LIST = [
        'SCL_ie', 'SCL_od', 'SCL_pp', 'SCL_og', 'SCL_pg',
        'SDA_ie', 'SDA_od', 'SDA_pp', 'SDA_og', 'SDA_pg'
    ]
    PULLUP = True

    def __init__(self, dut):
        self._dut = dut

        self._sa = SignalAccessor(dut, 'uio_in')	# FIXME pull from shared registry ?
        self._scl = self._sa.register(SCL_BITID)
        self._sda = self._sa.register(SDA_BITID)

        self._scl_state = self.PULLUP
        self._sda_state = self.PULLUP

        self._modeIsPP = False

        self._haveSclIe     = False
        self._haveSclLineOD = False
        self._haveSclLinePP = False
        self._haveSclLineOG = False
        self._haveSclLinePG = False

        self._haveSdaIe     = False
        self._haveSdaLineOD = False
        self._haveSdaLinePP = False
        self._haveSdaLineOG = False
        self._haveSdaLinePG = False


    def try_attach_debug_signals(self):
        self._haveSclIe     = design_element_exists(self._dut, "dut.debug_SCL_ie")
        self._haveSclLineOD = design_element_exists(self._dut, "dut.debug_SCL_od")
        self._haveSclLinePP = design_element_exists(self._dut, "dut.debug_SCL_pp")
        self._haveSclLineOG = design_element_exists(self._dut, "dut.debug_SCL_og")
        self._haveSclLinePG = design_element_exists(self._dut, "dut.debug_SCL_pg")

        self._haveSdaIe     = design_element_exists(self._dut, "dut.debug_SDA_ie")
        self._haveSdaLineOD = design_element_exists(self._dut, "dut.debug_SDA_od")
        self._haveSdaLinePP = design_element_exists(self._dut, "dut.debug_SDA_pp")
        self._haveSdaLineOG = design_element_exists(self._dut, "dut.debug_SDA_og")
        self._haveSdaLinePG = design_element_exists(self._dut, "dut.debug_SDA_pg")

        self.report()


    def report(self):
        for n in self.SIGNAL_LIST:
            self._dut._log.info("{} = {}".format(n, design_element_exists(self._dut, 'dut.debug_' + n)))


    def initialize(self, PP: bool = None):
        self.scl = self._scl_state
        self.sda = self._sda_state

        if type(PP) is bool:
            self._modeIsPP = PP


    def scl_idle(self) -> None:
        if self._haveSclIe:
            self._dut.debug_SCL_ie.value = False
        self.scl = self.PULLUP


    def sda_idle(self) -> None:
        if self._haveSdaIe:
            self._dut.debug_SDA_ie.value = False
        self.sda = self.PULLUP


    @property
    def scl_raw(self) -> bool:
        return self._scl_state


    @scl_raw.setter
    def scl_raw(self, v: bool) -> None:
        self._scl_state = v
        self._scl.value = v


    @property
    def sda_raw(self) -> bool:
        return self._sda_state


    @sda_raw.setter
    def sda_raw(self, v: bool) -> None:
        self._sda_state = v
        self._sda.value = v


    @property
    def scl(self) -> bool:
        return self._scl_state

    @scl.setter
    def scl(self, v: bool) -> None:
        if v is None:
            self.scl_idle()
        else:
            if self._haveSclIe:
                self._dut.debug_SCL_ie.value = not v or self._modeIsPP
            self.scl_raw = v

    @property
    def sda(self) -> bool:
        return self._sda_state

    @sda.setter
    def sda(self, v: bool) -> None:
        if v is None:
            self.sda_idle()
        else:
            if self._haveSdaIe:
                self._dut.debug_SDA_ie.value = not v or self._modeIsPP
                self.sda_raw = v


