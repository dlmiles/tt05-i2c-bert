#
#
#
# SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
# SPDX-License-Identifier: Apache2.0
#
#
#
import re

class SimConfig():
    def __init__(self, dut, cocotb):
        sim_name = cocotb.SIM_NAME
        self._is_iverilog = re.match(r'Icarus Verilog', sim_name, re.IGNORECASE) is not None
        self._is_verilator = re.match(r'Verilator', sim_name, re.IGNORECASE) is not None
        self._SIM_SUPPORTS_X = self.is_iverilog
        dut._log.info("SimConfig(is_iverilog={}, is_verilator={}, SIM_SUPPORTS_X={})".format(
            self.is_iverilog,
            self.is_verilator,
            self.SIM_SUPPORTS_X
        ))
        return None


    def default_value(self, with_value: bool = None):
        if with_value is None:
            with_value = False
        return '1' if with_value else '0'

    def bv_replace_x(self, s: str, with_value: bool = None, force: bool = False):
        if not self._SIM_SUPPORTS_X or force:
            return s.replace('x', self.default_value(with_value))
        return s

    @property
    def is_iverilog(self) -> bool:
        return self._is_iverilog

    @property
    def is_verilator(self) -> bool:
        return self._is_verilator

    @property
    def SIM_SUPPORTS_X(self) -> bool:
        return self._SIM_SUPPORTS_X

