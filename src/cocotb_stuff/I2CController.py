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
    PREFIX = "dut.debug_"


    def __init__(self, dut, CYCLES_PER_BIT: int, pp: bool = False):
        self._dut = dut

        self.CYCLES_PER_BIT = CYCLES_PER_BIT
        self.HALFEDGE = CYCLES_PER_BIT % 2 != 0
        self.CYCLES_PER_HALFBIT = CYCLES_PER_BIT / 2

        self._dut._log.info("I2CController(CYCLES_PER_BIT={self.CYCLES_PER_BIT}, HALFEDGE={self.HALFEDGE}, CYCLES_PER_HALFBIT={self.CYCLES_PER_HALFBIT})")

        self._sa = SignalAccessor(dut, 'uio_in')	# FIXME pull from shared registry ?
        # This is broken use self._sdascl
        #self._scl = self._sa.register(SCL_BITID)
        #self._sda = self._sa.register(SDA_BITID)
        self._sdascl = self._sa.register(SCL_BITID, SDA_BITID)

        self._scl_state = self.PULLUP
        self._sda_state = self.PULLUP

        self._scl_idle = True
        self._sda_idle = True

        self._modeIsPP = pp

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


    def try_attach_debug_signals(self) -> bool:
        self._haveSclIe     = design_element_exists(self._dut, self.PREFIX + "SCL_ie")
        self._haveSclLineOD = design_element_exists(self._dut, self.PREFIX + "SCL_od")
        self._haveSclLinePP = design_element_exists(self._dut, self.PREFIX + "SCL_pp")
        self._haveSclLineOG = design_element_exists(self._dut, self.PREFIX + "SCL_og")
        self._haveSclLinePG = design_element_exists(self._dut, self.PREFIX + "SCL_pg")

        self._haveSdaIe     = design_element_exists(self._dut, self.PREFIX + "SDA_ie")
        self._haveSdaLineOD = design_element_exists(self._dut, self.PREFIX + "SDA_od")
        self._haveSdaLinePP = design_element_exists(self._dut, self.PREFIX + "SDA_pp")
        self._haveSdaLineOG = design_element_exists(self._dut, self.PREFIX + "SDA_og")
        self._haveSdaLinePG = design_element_exists(self._dut, self.PREFIX + "SDA_pg")

        self.report()

        self.idle()

        # We shall just work return value off these two signals
        return self._haveSclIe or self._haveSdaIe


    def report(self):
        for n in self.SIGNAL_LIST:
            self._dut._log.info("{}{} = {}".format(self.PREFIX, n, design_element_exists(self._dut, self.PREFIX + n)))


    def initialize(self, PP: bool = None) -> None:
        self.scl = self._scl_state
        self.sda = self._sda_state

        if type(PP) is bool:
            print(f"initialize(PP={PP})")
            self._modeIsPP = PP


    async def cycles_after_setup(self):
        await ClockCycles(dut.clk, self.CYCLES_PER_HALFBIT)
        if self.HALFEDGE:
            await FallingEdge(dut.clk)


    async def cycles_after_hold(self):
        if self.HALFEDGE:
            await RisingEdge(dut.clk)
        await ClockCycles(dut.clk, self.CYCLES_PER_HALFBIT)


    async def send_start(self):
        assert self.sda
        assert self.scl

        self.set_sda_scl(False, True)	# START condition
        await self.cycles_after_setup()

        self.scl = False
        await self.cycles_after_hold()


    async def send_stop(self):
        assert not self.scl
        self.sda = False		# setup for STOP transition
        await self.cycles_after_setup()

        self.scl = True
        await self.cycles_after_hold()

        self.sda = True			# STOP condition
        await self.cycles_after_setup()


    async def send_data(self, byte: int):
        for bitid in range(8):
            m = 1 << bitid
            bf = True if((byte & m) != 0) else False

            self.set_sda_scl(bf, False)       # bitN
            await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
            if self.HALFEDGE:
                await FallingEdge(dut.clk)

            self.scl = True
            if self.HALFEDGE:
                await RisingEdge(dut.clk)
            await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)


    def scl_idle(self, v: bool = None) -> bool:
        if self._haveSclIe:
            bf = v is not None and ( v is not self.PULLUP or self._modeIsPP )
            print(f"scl_idle({v})  pp={self._modeIsPP}  bf={bf}")
            self._dut.dut.debug_SCL_ie.value = bf
        self._scl_idle = v is None
        return v


    def sda_idle(self, v: bool = None) -> bool:
        if self._haveSdaIe:
            bf = v is not None and ( v is not self.PULLUP or self._modeIsPP )
            print(f"sda_idle({v})  pp={self._modeIsPP}  bf={bf}")
            self._dut.dut.debug_SDA_ie.value = bf
        self._sda_idle = v is None
        return v


    def idle(self) -> None:
        self.set_sda_scl(None, None)


    @property
    def scl_raw(self) -> bool:
        return self._scl_state


    @scl_raw.setter
    def scl_raw(self, v: bool) -> None:
        assert type(v) is bool or v is None
        self._scl_state = v if v is not None else self.PULLUP
        sda = self.sda_resolve()
        self._sdascl.value = self.resolve_bits_state(sda, v)


    @property
    def sda_raw(self) -> bool:
        return self._sda_state


    @sda_raw.setter
    def sda_raw(self, v: bool) -> None:
        assert type(v) is bool or v is None
        self._sda_state = v if v is not None else self.PULLUP
        scl = self.scl_resolve()
        self._sdascl.value = self.resolve_bits_state(v, scl)


    @property
    def scl(self) -> bool:
        return self._scl_state

    @scl.setter
    def scl(self, v: bool) -> None:
        assert type(v) is bool or v is None
        self.scl_idle(v)
        self.scl_raw = v

    @property
    def sda(self) -> bool:
        return self._sda_state

    @sda.setter
    def sda(self, v: bool) -> None:
        assert type(v) is bool or v is None
        self.sda_idle(v)
        if v is not None:
            self.sda_raw = v


    def scl_resolve(self, v: bool = None, with_idle: bool = True) -> bool:
        assert type(v) is bool or v is None
        if v is None:
            if self._scl_idle and with_idle:
                return None
            return self._scl_state
        if not with_idle:
            return self._scl_state
        return v


    def sda_resolve(self, v: bool = None, with_idle: bool = True) -> bool:
        assert type(v) is bool or v is None
        if v is None:
            if self._sda_idle and with_idle:
                return None
            return self._sda_state
        if not with_idle:
            return self._sda_state
        return v


    def resolve_bits(self, sda: bool, scl: bool) -> int:
        assert type(sda) is bool
        assert type(scl) is bool
        if scl:
            if sda:
                return SCL_BITID_MASK|SDA_BITID_MASK
            else:
                return SCL_BITID_MASK
        else:
            if sda:
                return SDA_BITID_MASK
            else:
                return 0


    def resolve_bits_zerobased(self, sda: bool, scl: bool) -> int:
        # SCL_BITID is the min(SCL_BITID, SDA_BITID)
        x = self.resolve_bits(scl, sda)
        x_z = x >> SCL_BITID
        #print(f"resolve_bits(sda={sda}, scl={scl}) = {x} {x_z}")
        return self.resolve_bits(sda, scl) >> SCL_BITID


    def resolve_bit_state(self, bf: bool, when_none: str = 'z') -> str:
        assert type(when_none) is str
        if bf is None:
            return when_none
        return '1' if bf else '0'


    def resolve_bits_state(self, sda: bool, scl: bool) -> int:
        assert type(sda) is bool or sda is None
        assert type(scl) is bool or scl is None
        scl_c = self.resolve_bit_state(scl)
        sda_c = self.resolve_bit_state(sda)
        return sda_c + scl_c


    def set_sda_scl(self, sda: bool = None, scl: bool = None, with_idle: bool = True) -> None:
        assert type(sda) is bool or sda is None
        assert type(scl) is bool or scl is None
        self.sda_idle(sda)
        self.scl_idle(scl)
        sda = self.sda_resolve(sda, with_idle)
        scl = self.scl_resolve(scl, with_idle)
        self.set_sda_raw_and_scl_raw(sda, scl)


    def set_sda(self, sda: bool = None, with_idle: bool = True) -> None:
        assert type(sda) is bool or sda is None
        self.sda_idle(sda)
        sda = self.sda_resolve(sda, with_idle)
        scl = self.scl_resolve()
        self.set_sda_raw_and_scl_raw(sda, scl)


    def set_scl(self, scl: bool = None, with_idle: bool = True) -> None:
        assert type(scl) is bool or scl is None
        self.scl_idle(scl)
        sda = self.sda_resolve()
        scl = self.scl_resolve(scl, with_idle)
        self.set_sda_raw_and_scl_raw(sda, scl)


    def set_sda_raw_and_scl_raw(self, sda: bool = None, scl: bool = None) -> None:
        assert type(sda) is bool or sda is None
        assert type(scl) is bool or scl is None

        self._sda_state = sda if sda is not None else self.PULLUP
        self._scl_state = scl if scl is not None else self.PULLUP

        #v = self.resolve_bits_zerobased(sda, scl)
        v = self.resolve_bits_state(sda, scl)
        #print(f"resolve_bits_zerobased(sda={sda}, scl={scl}) = {v}")
        self._sdascl.value = v


