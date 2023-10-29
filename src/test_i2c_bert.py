#!/usr/bin/python3
#
#
#  Interesting environment settings:
#
#	CI=true		(validates expected production settings, implies ALL=true)
#	ALL=true	Run all tests (not the default profile to help speed up development)
#	DEBUG=true	Enable cocotb debug logging level
#	MONITOR=no-suspend Disables an optimization to suspend the FSM monitors (if active) around parts
#			of the simulation to speed it up.  Keeping them running is only useful to observe
#			the timing of when an FSM changes state (if that is important for diagnostics)
#	PUSH_PULL_MODE=true
#
#
# SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
# SPDX-License-Identifier: Apache2.0
#
#
import os
import sys
import re
import inspect
from typing import Any
from collections import namedtuple

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.wavedrom import trace
from cocotb.binary import BinaryValue
from cocotb.utils import get_sim_time

from TestBenchConfig import *

from cocotb_stuff import *
from cocotb_stuff.cocotbutil import *
from cocotb_stuff.cocotb_proxy_dut import *
from cocotb_stuff.FSM import *
from cocotb_stuff.I2CController import *
from cocotb_stuff.SignalAccessor import *
from cocotb_stuff.SignalOutput import *
from cocotb_stuff.SimConfig import *
from cocotb_stuff.Monitor import *
from cocotb_stuff.Payload import *



###
###
##################################################################################################################################
###
###

async def send_in7_oneedge(dut, in7):
    in7_before = dut.in7.value
    out8_before = dut.out8.value
    clk_before, = dut.clk.value
    in8 = try_integer(dut.in7.value, 0) << 1 | try_integer(dut.clk.value, 0)	# rebuild for log output
    dut.in7.value = in7
    if dut.clk.value:
        await FallingEdge(dut.clk)
    else:
        await RisingEdge(dut.clk)
    # Try to report non-clock state changes
    out8_equal = try_compare_equal(out8_before, dut.out8.value)
    if True or in7_before != in7 or not out8_equal:
        out8_desc = "SAME" if(out8_equal) else "CHANGED"
        dut._log.info("dut clk={} in7={} {} in8={} {}  =>  out8={} {} => {} {}  [{}]".format(
            clk_before,
            try_binary(dut.in7.value, width=7),  try_decimal_format(try_integer(dut.in7.value), '3d'),
            try_binary(in8, width=8),            try_decimal_format(try_integer(in8), '3d'),
            try_binary(out8_before, width=8),    try_decimal_format(try_integer(out8_before), '3d'),
            try_binary(dut.out8.value, width=8), try_decimal_format(try_integer(dut.out8.value), '3d'),
            out8_desc))

async def send_in7(dut, in7):
    in8 = try_integer(dut.in7.value, 0) << 1 | try_integer(dut.clk.value, 0)	# rebuild for log output
    dut._log.info("dut out8={} in7={} in8={}".format(dut.out8.value, dut.in7.value, in8))
    await FallingEdge(dut.clk)
    dut.in7.value = in7
    await RisingEdge(dut.clk)
    dut._log.info("dut out8={} in7={} in8={}".format(dut.out8.value, dut.in7.value, in8))

async def send_in8(dut, in8):
    in7 = (in8 >> 1) & 0x7f
    await send_in7(dut, in7)

async def send_in8_oneedge(dut, in8):
    want_clk = in8 & 0x01
    # The rom.txt scripts expect to drive CLK as well, so we need to align edge so current
    #  state is mismatched
    if dut.clk.value and want_clk != 0:
        if dut.clk.value:
            dut._log.warning("dut ALIGN INSERT EDGE: Falling (clk={}, want_clk={})".format(dut.clk.value, want_clk))
            await FallingEdge(dut.clk)
        else:
            dut._log.warning("dut ALIGN INSERT EDGE: Rising (clk={}, want_clk={})".format(dut.clk.value, want_clk))
            await RisingEdge(dut.clk)
    in7 = (in8 >> 1) & 0x7f
    await send_in7_oneedge(dut, in7)

async def send_sequence_in8(dut, seq):
    for in8 in seq:
        await send_in8(dut, in8)

###
###
##################################################################################################################################
###
###

# Signals we are not interested in when enumerating at the top of the log
exclude = [
    r'[\./]_',
    r'[\./]FILLER_',
    r'[\./]PHY_',
    r'[\./]TAP_',
    r'[\./]VGND',
    r'[\./]VNB',
    r'[\./]VPB',
    r'[\./]VPWR',
    r'[\./]pwrgood_',
    r'[\./]ANTENNA_',
    r'[\./]clkbuf_leaf_',
    r'[\./]clknet_leaf_',
    r'[\./]clkbuf_[\d_]+_clk',
    r'[\./]clknet_[\d_]+_clk',
    r'[\./]net\d+[\./]',
    r'[\./]net\d+$',
    r'[\./]fanout\d+[\./]',
    r'[\./]fanout\d+$',
    r'[\./]input\d+[\./]',
    r'[\./]input\d+$',
    r'[\./]hold\d+[\./]',
    r'[\./]hold\d+$'
]
EXCLUDE_RE = dict(map(lambda k: (k,re.compile(k)), exclude))

def exclude_re_path(path: str, name: str):
    for v in EXCLUDE_RE.values():
        if v.search(path):
            #print("EXCLUDED={}".format(path))
            return False
    return True

###
# Signals not to touch for ensure_resolvable()
#
# Signals we are not interested in enumerating to assign X with value
ensure_exclude = [
    #r'[\./]_',
    r'[A-Za-z0-9_\$]_[\./]base[\./][A-Za-z0-9_\$]+$',
    r'[\./]FILLER_',
    r'[\./]PHY_',
    r'[\./]TAP_',
    r'[\./]VGND$',
    r'[\./]VNB$',
    r'[\./]VPB$',
    r'[\./]VPWR$',
    r'[\./]CLK$',
    r'[\./]CLK_N$',
    r'[\./]DIODE$',
    r'[\./]GATE$',
    r'[\./]NOTIFIER$',
    r'[\./]RESET$',
    r'[\./]RESET_B$',
    r'[\./]SET$',
    r'[\./]SET_B$',
    r'[\./]SLEEP$',
    r'[\./]UDP_IN$',
    # sky130 candidates to exclude: CLK CLK_N GATE NOTIFIER RESET SET SLEEP UDP_IN
    r'[\./][ABCD][0-9]*$',
    r'[\./][ABCD][0-9]_N*$',
    r'[\./]pwrgood_',
    r'[\./]ANTENNA_',
    r'[\./]clkbuf_leaf_',
    r'[\./]clknet_leaf_',
    r'[\./]clkbuf_[\d_]+_clk',
    r'[\./]clknet_[\d_]+_clk',
    r'[\./]net\d+[\./]',
    r'[\./]net\d+$',
    r'[\./]fanout\d+[\./]',
    r'[\./]fanout\d+$',
    r'[\./]input\d+[\./]',
    r'[\./]input\d+$',
    r'[\./]hold\d+[\./]',
    r'[\./]hold\d+$'
]
ENSURE_EXCLUDE_RE = dict(map(lambda k: (k,re.compile(k)), ensure_exclude))

def ensure_exclude_re_path(path: str, name: str):
    for v in ENSURE_EXCLUDE_RE.values():
        if v.search(path):
            #print("ENSURE_EXCLUDED={}".format(path))
            return False
    return True



# This is used as detection of gatelevel testing, with a flattened HDL,
#  we can only inspect the external module signals and disable internal signal inspection.
def resolve_GL_TEST():
    gl_test = False
    if 'GL_TEST' in os.environ:
        gl_test = True
    if 'GATES' in os.environ and os.environ['GATES'] == 'yes':
        gl_test = True
    return gl_test


def resolve_MONITOR_can_suspend():
    can_suspend = True	# default
    if 'MONITOR' in os.environ and os.environ['MONITOR'] == 'no-suspend':
        can_suspend = False
    return can_suspend


def run_this_test(default_value: bool = True) -> bool:
    if 'CI' in os.environ and os.environ['CI'] != 'false':
        return True	# always on for CI
    if 'ALL' in os.environ and os.environ['ALL'] != 'false':
        return True
    return default_value


def resolve_PUSH_PULL_MODE():
    push_pull_mode = False
    if 'PUSH_PULL_MODE' in os.environ and os.environ['PUSH_PULL_MODE'] != 'false':
        push_pull_mode = True
    return push_pull_mode


def usb_spec_wall_clock_tolerance(value: int, LOW_SPEED: bool) -> tuple:
    freq = 1500000 if(LOW_SPEED) else 12000000
    ppm = 15000 if(LOW_SPEED) else 2500

    variation = (freq * ppm) / 1000000
    varfactor = variation / freq

    tolmin = int(value - (value * varfactor))
    tolmax = int(value + (value * varfactor))

    return (tolmin, tolmax)


def grep_file(filename: str, pattern1: str, pattern2: str) -> bool:
    # The rx_timerLong constants that specify counter units to achieve USB
    #  specification wall-clock timing requirements based on the 48MHz phyCd_clk.
    #
    # resume   HOST instigated, reverse polarity for > 20ms, then a LS EOP.
    #            reverse polarity to what? (does this mean FS/LS)
    #            LS EOP has a specific polarity
    #          DEVICE instigated (optional), send K state for >1ms and <15ms.
    #            Can only be starte after being idle >5ms
    #               (check how this interacts with suspend state)
    #            Host will respond within 1ms (I assume from not sending K state)
    #          Timer 0xe933f looks to be 19.899ms @48MHz
    #
    # reset    HOST send SE0 for >= 10ms, DEVICE may notice after 2.5us
    #          Timer 0x7403f looks to be 9.899ms @48MHz
    #
    # suspend  HOST send IDLE(J) for >= 3ms, is a suspend condition.
    #          This is usually inhibited by SOF(FS) or KeepAlive/EOP(LS) every 1ms.
    #          Timer 0x21fbf looks to be 2.899ms @48MHz
    #
    # The SIM values are 1/200 to speed up simulation testing.
    #
    # We have something in the GHA CI to patch this matter (ensure the production values are put back) with 'sed -i'.
    #
    # PRODUCTION
    # -  assign rx_timerLong_resume = (rx_timerLong_counter == 23'h0e933f);
    # -  assign rx_timerLong_reset = (rx_timerLong_counter == 23'h07403f);
    # -  assign rx_timerLong_suspend = (rx_timerLong_counter == 23'h021fbf);
    # SIM (FS 1/200)
    #    assign rx_timerLong_resume = (rx_timerLong_counter == 23'h0012a7);
    #    assign rx_timerLong_reset = (rx_timerLong_counter == 23'h000947);
    #    assign rx_timerLong_suspend = (rx_timerLong_counter == 23'h0002b7);
    # SIM (LS 1/20 current)
    #          tried at 1/25 but it is on the limit of firing a spurious suspend from specification packet
    #          sizes with not enough gap between tests to allow us to setup testing comfortably
    #    assign rx_timerLong_resume = (rx_timerLong_counter == 23'h00ba8f);
    #    assign rx_timerLong_reset = (rx_timerLong_counter == 23'h005ccf);
    #    assign rx_timerLong_suspend = (rx_timerLong_counter == 23'h001b2f);
    # SIM (LS 1/25 old)
    #    assign rx_timerLong_resume = (rx_timerLong_counter == 23'h00953f);
    #    assign rx_timerLong_reset = (rx_timerLong_counter == 23'h004a3f);
    #    assign rx_timerLong_suspend = (rx_timerLong_counter == 23'h0015bf);
    #
    with open(filename) as file_in:
        lines = []
        for line in file_in:
            lines.append(line.rstrip())
        left = list(filter(lambda l: re.search(pattern1, l), lines))
        # search for a single line match of pattern1 in the whole file (error if not found, or multiple lines)
        if len(left) == 1:
            # search the line found for pattern2 and return True/False on this
            retval = re.search(pattern2, left[0])
            #print("left={} {}".format(left[0], retval))
            return retval
    raise Exception(f"Unable to find any match from file: {filename} for regex {pattern1}")


FSM = FSM({
    'phase':  'dut.i2c_bert.myState_1.fsmPhase_stateReg_string',
    'i2c':    'dut.i2c_bert.i2c.fsm_stateReg_string'
})


def gha_dumpvars(dut):
    dumpvars = ['CI', 'GL_TEST', 'FUNCTIONAL', 'USE_POWER_PINS', 'SIM', 'UNIT_DELAY', 'SIM_BUILD', 'GATES', 'ICARUS_BIN_DIR', 'COCOTB_RESULTS_FILE', 'TESTCASE', 'TOPLEVEL', 'DEBUG', 'LOW_SPEED']
    if 'CI' in os.environ and os.environ['CI'] != 'false':
        for k in os.environ.keys():
            if k in dumpvars:
                dut._log.info("{}={}".format(k, os.environ[k]))


def bit(byte: int, bitid: int) -> int:
    assert bitid >= 0 and bitid <= 7
    assert (byte & ~0xff) == 0
    mask = 1 << bitid
    return (byte & mask) == mask



@cocotb.test()
async def test_i2c_bert(dut):
    if 'DEBUG' in os.environ and os.environ['DEBUG'] != 'false':
        dut._log.setLevel(cocotb.logging.DEBUG)

    sim_config = SimConfig(dut, cocotb)

    PUSH_PULL_MODE = resolve_PUSH_PULL_MODE()

    # The DUT uses a divider from the master clock at this time
    CLOCK_FREQUENCY = 10000000
    CLOCK_MHZ = CLOCK_FREQUENCY / 1e6
    CLOCK_PERIOD_PS = int(1 / (CLOCK_FREQUENCY * 1e-12)) - 1
    CLOCK_PERIOD_NS = int(1 / (CLOCK_FREQUENCY * 1e-9))

    SCL_CLOCK_FREQUENCY = 1000000

    tb_config = TestBenchConfig(dut, CLOCK_FREQUENCY = CLOCK_FREQUENCY, ALT_CLOCK_FREQUENCY = SCL_CLOCK_FREQUENCY)

    dut._log.info("start")

    #clock = Clock(dut.clk, CLOCK_PERIOD_PS, units="ps")
    clock = Clock(dut.clk, CLOCK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    dut._log.info("CLOCK_PERIOD_NS={}".format(CLOCK_PERIOD_NS))
    #dut._log.info("CLOCK_PERIOD_PS={}".format(CLOCK_PERIOD_PS))

    assert design_element_exists(dut, 'clk')
    assert design_element_exists(dut, 'rst_n')
    assert design_element_exists(dut, 'ena')

    gha_dumpvars(dut)

    depth = None
    GL_TEST = resolve_GL_TEST()
    if GL_TEST:
        dut._log.info("GL_TEST={} (detected)".format(GL_TEST))
        #depth = 1

    if GL_TEST:
        dut = ProxyDut(dut)

    report_resolvable(dut, 'initial ', depth=depth, filter=exclude_re_path)

    validate(dut)

    if GL_TEST and 'RANDOM_POLICY' in os.environ:
        await ClockCycles(dut.clk, 1)		## crank it one tick, should assign some non X states
        if os.environ['RANDOM_POLICY'] == 'zero' or os.environ['RANDOM_POLICY'].lower() == 'false':
            ensure_resolvable(dut, policy=False, filter=ensure_exclude_re_path)
        elif os.environ['RANDOM_POLICY'] == 'one' or os.environ['RANDOM_POLICY'].lower() == 'true':
            ensure_resolvable(dut, policy=True, filter=ensure_exclude_re_path)
        else: # if os.environ['RANDOM_POLICY'] == 'random':
            ensure_resolvable(dut, policy='random', filter=ensure_exclude_re_path)

    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    dut.ena.value = 0

    await ClockCycles(dut.clk, 6)

    # Latch state setup
    dut.ui_in.value = 0xa5
    dut.uio_in.value = 0x5a
    await ClockCycles(dut.clk, 1)	# need to crank it one for always_latch to work in sim

    dut.ena.value = 1
    await ClockCycles(dut.clk, 4)
    assert dut.ena.value == 1		# validates SIM is behaving as expected

    if not GL_TEST:	# Latch state set
        assert dut.dut.latched_ena_ui_in.value == 0xa5
        assert dut.dut.latched_ena_uio_in.value == 0x5a

    # We waggle this to see if it resolves RANDOM_POLICY=random(iverilog)
    #  where dut.rst_n=0 and dut.dut.rst_n=1 got assigned, need to understand more here
    #  as I would have expected setting dut.rst_n=anyvalue and letting SIM run would
    #  have propagated into dut.dut.rst_n.
    dut.rst_n.value = 0
    if not GL_TEST:
        # sky130_toolbox/glitch_free_clock_mux.v:
        # Uninitialized internal states that depend on each other need to work themselves out.
        dut.dut.i2c_bert.i2c.clockGate.dff01q.value = False
        dut.dut.i2c_bert.i2c.clockGate.dff02q.value = True
        dut.dut.i2c_bert.i2c.clockGate.dff02qn.value = False
        dut.dut.i2c_bert.i2c.clockGate.dff11q.value = False
        dut.dut.i2c_bert.i2c.clockGate.dff12q.value = True
        dut.dut.i2c_bert.i2c.clockGate.dff12qn.value = False
        await ClockCycles(dut.clk, 4)
        dut.dut.i2c_bert.i2c.clockGate.sel.value = not dut.dut.i2c_bert.i2c.clockGate.sel.value
        await ClockCycles(dut.clk, 2)
        dut.dut.i2c_bert.i2c.clockGate.sel.value = not dut.dut.i2c_bert.i2c.clockGate.sel.value
    await ClockCycles(dut.clk, 2)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 4)

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    assert dut.rst_n.value == 0

    # Reset state setup
    dut.ui_in.value = 0x34
    dut.uio_in.value = 0x12
    await ClockCycles(dut.clk, 1)	# need to crank it one for always_latch to work in sim

    # Reset state setup
    dut.ui_in.value = 0x00
    dut.uio_in.value = 0x00

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.rst_n.value == 1

    if not GL_TEST:    # Reset state set
        dut.dut.latched_rst_n_ui_in.value == 0x34
        dut.dut.latched_rst_n_uio_in.value == 0x12

    await ClockCycles(dut.clk, 2)

    debug(dut, '001_TEST')

    TICKS_PER_BIT = 3 #int(CLOCK_FREQUENCY / SCL_CLOCK_FREQUENCY)

    #CYCLES_PER_BIT = 3
    #CYCLES_PER_HALFBIT = 1
    #HALF_EDGE = True
    CYCLES_PER_BIT = 6
    CYCLES_PER_HALFBIT = 3
    HALF_EDGE = False

    ctrl = I2CController(dut, CYCLES_PER_BIT = CYCLES_PER_BIT, pp = True, GL_TEST = GL_TEST) # PUSH_PULL_MODE)
    ctrl.try_attach_debug_signals()

    # Verilator VPI hierarchy discovery workaround
    if not GL_TEST and sim_config.is_verilator:
        # Verilator appears to require us to access into the Hierarchy path of items in the form below
        #  before they can be found with discovery APIs.  It appears we only need to access into the
        #  containing object, for the signal siblings to also be found.
        dummy1 = dut.dut.i2c_bert.myState_1.fsmPhase_stateReg_string	# this is the magic: myState_1
        assert design_element_exists(dut, FSM.fsm_signal_path('phase'))

        dummy1 = dut.dut.i2c_bert.i2c.fsm_stateReg_string		# this is the magic: i2c
        assert design_element_exists(dut, FSM.fsm_signal_path('i2c'))

        for hierarchy_path in FSM.values():
            assert design_element_exists(dut, hierarchy_path), f"Verilator signal: {hierarchy_path}"


    fsm_monitors = {}
    if not GL_TEST:
        fsm_monitors['phase'] = FSM.fsm_signal_path('phase')
        fsm_monitors['i2c'] = FSM.fsm_signal_path('i2c')
    MONITOR = Monitor(dut, FSM, fsm_monitors)
    await cocotb.start(MONITOR.build_task())

    # This is a custom capture mechanism of the output encoding
    # Goals:
    #         dumping to a text file and making a comparison with expected output
    #         confirming period where no output occured
    #         confirm / measure output duration of special conditions
    #
    SO = SignalOutput(dut, SIM_SUPPORTS_X = sim_config.SIM_SUPPORTS_X)
    signal_accessor_scl_write = SignalAccessor(dut, 'uio_out', SCL_BITID)	# dut.
    signal_accessor_sda_write = SignalAccessor(dut, 'uio_out', SDA_BITID)	# dut.
    await cocotb.start(SO.register('so', signal_accessor_scl_write, signal_accessor_sda_write))
    # At startup in simulation we see writeEnable asserted and so output
    #SO.assert_resolvable_mode(True)
    #SO.assert_encoded_mode(SO.SE0)
    SO.unregister()		# FIXME

    report_resolvable(dut, depth=depth, filter=exclude_re_path)

    signal_accessor_uio_in = SignalAccessor(dut, 'uio_in')
    signal_accessor_scl = signal_accessor_uio_in.register('uio_in:SCL', SCL_BITID)	# dut.
    signal_accessor_sda = signal_accessor_uio_in.register('uio_in:SDA', SDA_BITID)	# dut.

    #############################################################################################

    ## raw more

    debug(dut, '001_RAW_READ')

    #CMD_BYTE = 0xb5
    #CMD_BYTE = 0xf1
    CMD_BYTE = 0x01	# CMD_ONE

    ctrl.initialize()
    ctrl.idle()
    await ClockCycles(dut.clk, CYCLES_PER_BIT)

    # PREMABLE
    ctrl.set_sda_scl(True, True)
    await ClockCycles(dut.clk, CYCLES_PER_BIT)

    # PREMABLE
    ctrl.scl = False
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    ctrl.scl = True
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    ctrl.scl = False
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    ctrl.scl = True
    await ClockCycles(dut.clk, CYCLES_PER_BIT)

    # START
    ctrl.set_sda_scl(False, True)	# START transition (setup)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.sda = False			# START transition
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    # DATA
    ctrl.set_sda_scl(bit(CMD_BYTE, 7), False)	# bit7=1
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 6), False)	# bit6=0
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 5), False)	# bit5=1
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 4), False)	# bit4=1
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 3), False)	# bit3=0
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 2), False)	# bit2=1
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 1), False)	# bit1=0
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(bit(CMD_BYTE, 0), False)	# bit0=0 (WRITE)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.set_sda_scl(None, False)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ## SAMPLE
    if ctrl.sda_oe:
        nack = ctrl.sda_rx
    elif not ctrl._modeIsPP:
        nack = ctrl.PULLUP	# open-drain
    else:
        nack = None
    # GL_TEST is getting: GL_TEST I2CController.sda_rx() = {str(self._sdascl_out)} [IS_NOT_RESOLABLE] using {nv}
    if not GL_TEST:	## FIXME reinstante this
        assert nack is ctrl.ACK

    ctrl.scl = True		## FIXME check SDA still idle
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    # STOP
    ctrl.set_sda_scl(False, False)		# SDA setup to ensure transition
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    ctrl.scl = True
    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.sda = True				# STOP transition
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)
    if HALF_EDGE:
        await FallingEdge(dut.clk)

    if HALF_EDGE:
        await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, CYCLES_PER_HALFBIT)

    ctrl.idle()

    debug(dut, '')
    await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ## cooked mode

    CAN_ASSERT = True

    debug(dut, '002_COOKED_WRITE')

    await ctrl.send_start()

    await ctrl.send_data(0x00)
    nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
    if not GL_TEST:	## FIXME reinstante this
        assert nack is ctrl.ACK

    await ctrl.send_data(0xff)
    nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
    if not GL_TEST:	## FIXME reinstante this
        assert nack is ctrl.ACK

    await ctrl.send_stop()

    ctrl.idle()

    debug(dut, '')
    await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '200_RESET')

        await ctrl.send_start()

        await ctrl.send_data(0xf0)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '210_ACK_wr')

        await ctrl.send_start()

        await ctrl.send_data(0x80)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '220_ACK_rd')

        await ctrl.send_start()

        await ctrl.send_data(0x81)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '230_NACK_wr')

        await ctrl.send_start()

        await ctrl.send_data(0x84)
        nack = await ctrl.recv_ack(ctrl.NACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.NACK	# NACK

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '240_NACK_rd')

        await ctrl.send_start()

        await ctrl.send_data(0x85)
        nack = await ctrl.recv_ack(ctrl.NACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.NACK	# NACK

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '270_AUTOBAUD')

        await ctrl.send_start()

        await ctrl.send_data(0xcc)
        # FIXME this NACKs as noimpl
        nack = await ctrl.recv_ack(ctrl.NACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.NACK

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '300_STRETCH_rd')

        await ctrl.send_start()

        await ctrl.send_data(0xc8)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        # FIXME this ACKs but noimpl

        # FIXME need to add sense on SCL after we try to rise
        data = await ctrl.recv_data()
        dut._log.info("STRETCH = {str(data):x}")
        if not GL_TEST:	## FIXME reinstante this
            nack = await ctrl.recv_ack()
        #assert nack is None	## FIXME

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '400_GETLATCH')

        await ctrl.send_start()

        await ctrl.send_data(0xf1)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        data = await ctrl.recv_data()
        dut._log.info("LATCH[0] = {str(data):x}")
        await ctrl.send_ack()

        data = await ctrl.recv_data()
        dut._log.info("LATCH[1] = {str(data):x}")
        await ctrl.send_ack()

        data = await ctrl.recv_data()
        dut._log.info("LATCH[2] = {str(data):x}")
        await ctrl.send_ack()

        data = await ctrl.recv_data()
        dut._log.info("LATCH[3] = {str(data):x}")
        await ctrl.send_ack()

        ctrl.sda_idle()
        assert await ctrl.check_recv_is_idle(CYCLES_PER_HALFBIT)

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    await ClockCycles(dut.clk, 256)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '100_CMD00_RESET')


    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 4)

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)

    if not GL_TEST:	# Latch state zeroed?
        assert dut.dut.latched_rst_n_ui_in.value == 0x00
        assert dut.dut.latched_rst_n_uio_in.value == 0x00

    await ClockCycles(dut.clk, 3)

    dut.ena.value = 0
    await ClockCycles(dut.clk, 1)

    if not GL_TEST:	# Latch state zeroed?
        assert dut.dut.latched_ena_ui_in.value == 0x00
        assert dut.dut.latched_ena_uio_in.value == 0x00

    await ClockCycles(dut.clk, 3)

    ##############################################################################################

    debug(dut, '999_DONE')


    MONITOR.shutdown()

    await ClockCycles(dut.clk, 32)

    report_resolvable(dut, filter=exclude_re_path)

