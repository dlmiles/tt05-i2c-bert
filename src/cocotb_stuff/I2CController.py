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
import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles

from cocotb_stuff import *
from cocotb_stuff.cocotbutil import *
from cocotb_stuff.SignalAccessor import *


class I2CController():
    SIGNAL_LIST = [
        'SCL_ie', 'SCL_od', 'SCL_pp', 'SCL_og', 'SCL_pg', 'SCL_os', 'SCL_ps',
        'SDA_ie', 'SDA_od', 'SDA_pp', 'SDA_og', 'SDA_pg', 'SDA_os', 'SDA_ps'
    ]
    PULLUP = True
    PREFIX = "dut.debug_"


    def __init__(self, dut, CYCLES_PER_BIT: int, pp: bool = False, GL_TEST: bool = False):
        self._dut = dut
        self.GL_TEST = GL_TEST

        self.CYCLES_PER_BIT = CYCLES_PER_BIT
        self.HALFEDGE = CYCLES_PER_BIT % 2 != 0
        self.CYCLES_PER_HALFBIT = int(CYCLES_PER_BIT / 2)

        self._dut._log.info("I2CController(CYCLES_PER_BIT={self.CYCLES_PER_BIT}, HALFEDGE={self.HALFEDGE}, CYCLES_PER_HALFBIT={self.CYCLES_PER_HALFBIT})")

        self._sa_uio_in = SignalAccessor(dut, 'uio_in')	# FIXME pull from shared registry ?
        # This is a broken idea (over VPI) use self._sdascl
        #self._scl = self._sa.register('uio_in:SCL', SCL_BITID)
        #self._sda = self._sa.register('uio_in:SDA', SDA_BITID)
        self._sdascl = self._sa_uio_in.register('uio_in', SCL_BITID, SDA_BITID)

        # uio_out: This is output from peer, and input/receiver side for us
        self._sa_uio_out = SignalAccessor(dut, 'uio_out')	# FIXME pull from shared registry ?
        self._sdascl_out = self._sa_uio_out.register('uio_out', SCL_BITID, SDA_BITID)
        # uio_oe: This is peer OE
        self._sa_uio_oe = SignalAccessor(dut, 'uio_oe')	# FIXME pull from shared registry ?
        self._sdascl_oe = self._sa_uio_oe.register('uio_oe', SCL_BITID, SDA_BITID)

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
        self._haveSclLineOS = False
        self._haveSclLinePS = False

        self._haveSdaIe     = False
        self._haveSdaLineOD = False
        self._haveSdaLinePP = False
        self._haveSdaLineOG = False
        self._haveSdaLinePG = False
        self._haveSdaLineOS = False
        self._haveSdaLinePS = False


    def try_attach_debug_signals(self) -> bool:
        self._haveSclIe     = design_element_exists(self._dut, self.PREFIX + "SCL_ie")
        self._haveSclLineOD = design_element_exists(self._dut, self.PREFIX + "SCL_od")
        self._haveSclLinePP = design_element_exists(self._dut, self.PREFIX + "SCL_pp")
        self._haveSclLineOG = design_element_exists(self._dut, self.PREFIX + "SCL_og")
        self._haveSclLinePG = design_element_exists(self._dut, self.PREFIX + "SCL_pg")
        self._haveSclLineOS = design_element_exists(self._dut, self.PREFIX + "SCL_os")
        self._haveSclLinePS = design_element_exists(self._dut, self.PREFIX + "SCL_ps")

        self._haveSdaIe     = design_element_exists(self._dut, self.PREFIX + "SDA_ie")
        self._haveSdaLineOD = design_element_exists(self._dut, self.PREFIX + "SDA_od")
        self._haveSdaLinePP = design_element_exists(self._dut, self.PREFIX + "SDA_pp")
        self._haveSdaLineOG = design_element_exists(self._dut, self.PREFIX + "SDA_og")
        self._haveSdaLinePG = design_element_exists(self._dut, self.PREFIX + "SDA_pg")
        self._haveSdaLineOS = design_element_exists(self._dut, self.PREFIX + "SDA_os")
        self._haveSdaLinePS = design_element_exists(self._dut, self.PREFIX + "SDA_ps")

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
        await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)
        if self.HALFEDGE:
            await FallingEdge(self._dut.clk)


    async def cycles_after_hold(self):
        if self.HALFEDGE:
            await RisingEdge(self._dut.clk)
        await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)


    async def send_start(self):
        assert self.sda
        assert self.scl

        if self._sda_idle or self._scl_idle:
            # Probably not needed as line state is like this already but it looks better on VCD
            self.set_sda_scl(True, True)
            await self.cycles_after_hold()
            #await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)

        self.set_sda_scl(False, True)	# START transition (setup)
        await self.cycles_after_setup()

        self.sda = False		# START transition
        await self.cycles_after_hold()


    async def send_stop(self) -> None:
        assert self.scl
        self.set_sda_scl(False, False)	# SDA setup for STOP transition
        await self.cycles_after_setup()

        self.scl = True
        await self.cycles_after_hold()

        self.sda = True			# STOP condition
        await self.cycles_after_setup()


    async def send_data(self, byte: int) -> None:
        for bitid in range(8):
            m = 1 << bitid
            bf = True if((byte & m) != 0) else False

            self.set_sda_scl(bf, False)       # bitN
            await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)
            if self.HALFEDGE:
                await FallingEdge(self._dut.clk)

            self.scl = True
            if self.HALFEDGE:
                await RisingEdge(self._dut.clk)
            await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)


    async def recv_ack(self) -> bool:
        assert self.scl

        self.set_sda_scl(None, False)		# SDA idle
        await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)
        if self.HALFEDGE:
            await FallingEdge(self._dut.clk)

        self.scl = True
        nack = self.sda_rx
        if self.HALFEDGE:
            await RisingEdge(self._dut.clk)
        await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)

        nack


    async def recv_data(self) -> int:
        assert self.scl


    async def send_bit(self, bit: bool = False) -> None:
        assert self.scl

        self.set_sda_scl(bit, False)
        await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)
        if self.HALFEDGE:
            await FallingEdge(self._dut.clk)

        self.scl = True
        if self.HALFEDGE:
            await RisingEdge(self._dut.clk)
        await ClockCycles(self._dut.clk, self.CYCLES_PER_HALFBIT)


    async def send_ack(self) -> None:
        await self.send_bit(False)


    async def send_nack(self) -> None:
        await self.send_bit(True)


    async def check_recv_is_idle(self, cycles: int = 0, no_warn: bool = False) -> bool:
        # warn if we are not idle on our side ?
        if not no_warn and not self._sda_idle:
            self._dut._log.warn(f"check_recv_is_idle() but SDA is not idle sending")

        # signal scl_oe
        if self.sda_oe:
            return False
        for i in range(cycle):
            await ClockCycles(self._dut.clk, 1)
            if self.sda_oe:
                return False
        return True


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

    @property
    def sda_rx(self) -> bool:
        if self.GL_TEST and not self._sdascl_out.raw.is_resolvable():
            nv = False	# FIXME pickup RANDOM_POLICY
            self._dut._log.warn("GL_TEST I2CController.sda_rx() = {str(self._sdascl_out)} [IS_NOT_RESOLABLE] using {nv}")
            return nv
        return self._sdascl_out.value & 2 != 0


    @property
    def sda_oe(self) -> bool:
        if self.GL_TEST and not self._sdascl_out.raw.is_resolvable():
            nv = False	# FIXME pickup RANDOM_POLICY
            self._dut._log.warn("GL_TEST I2CController.sda_rx() = {str(self._sdascl_out)} [IS_NOT_RESOLABLE] using {nv}")
            return nv
        return self._sdascl_oe.value & 2 != 0


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


