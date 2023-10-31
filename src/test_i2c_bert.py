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
#	SCL_MODE=true
#
#  PUSH_PULL_MODE=true make
#  PUSH_PULL_MODE=true GATES=yes make
#
#
# SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
# SPDX-License-Identifier: Apache2.0
#
#
import os
import sys
import re
import random
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
    r'[\./]clkbuf_[\d_]+__f_clk',
    r'[\./]clknet_[\d_]+__leaf_clk',
    r'[\./]clkbuf_[\d_]+_clk',
    r'[\./]clknet_[\d_]+_clk',
    r'[\./]net\d+[\./]',
    r'[\./]net\d+$',
    r'[\./]fanout\d+[\./]',
    r'[\./]fanout\d+$',
    r'[\./]input\d+[\./]',
    r'[\./]input\d+$',
    r'[\./]hold\d+[\./]',
    r'[\./]hold\d+$',
    r'[\./]max_cap\d+[\./]',
    r'[\./]max_cap\d+$',
    r'[\./]wire\d+[\./]',
    r'[\./]wire\d+$'
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
    r'[\./]HI$',
    r'[\./]LO$',
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


def resolve_SCL_MODE():
    scl_mode = False
    if 'SCL_MODE' in os.environ and os.environ['SCL_MODE'] != 'false':
        scl_mode = True
    return scl_mode


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


def cmd_alu(len4: int = 0, read: bool = False, op_and: bool = False, op_or: bool = False, op_xor: bool = False, op_add: bool = False) -> int:
    v = int((len4 & 0xf) << 4)
    v |= 0x02
    if read:
        v |= 0x01
    if op_and:
        v |= 0x00 << 2
    elif op_or:
        v |= 0x01 << 2
    elif op_xor:
        v |= 0x02 << 2
    elif op_add:
        v |= 0x03 << 2
    return v



@cocotb.test()
async def test_i2c_bert(dut):
    if 'DEBUG' in os.environ and os.environ['DEBUG'] != 'false':
        dut._log.setLevel(cocotb.logging.DEBUG)

    sim_config = SimConfig(dut, cocotb)

    PUSH_PULL_MODE = resolve_PUSH_PULL_MODE()
    SCL_MODE = resolve_SCL_MODE()
    DIV12 = 0

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
    LATCHED_16 = 0xa5
    LATCHED_24 = 0x5a

    dut.ui_in.value = LATCHED_16
    dut.uio_in.value = LATCHED_24
    await ClockCycles(dut.clk, 1)	# need to crank it one for always_latch to work in sim

    dut.ena.value = 1
    await ClockCycles(dut.clk, 4)
    assert dut.ena.value == 1		# validates SIM is behaving as expected

    if not GL_TEST:	# Latch state set
        assert dut.dut.latched_ena_ui_in.value == LATCHED_16
        assert dut.dut.latched_ena_uio_in.value == LATCHED_24

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
    v = 0
    # LATCHED not the same layout as GETCFG
    if SCL_MODE:
        v |= 0x02
    if PUSH_PULL_MODE:
        v |= 0x04
    if DIV12 != 0:
        v |= 0x08
        v |= DIV12 << 4
    LATCHED_00_08 = v

    LATCHED_00 = LATCHED_00_08 & 0xff 		# 0x34
    LATCHED_08 = (LATCHED_00_08 >> 8) & 0xff	# 0x12

    dut.ui_in.value = LATCHED_00
    dut.uio_in.value = LATCHED_08
    await ClockCycles(dut.clk, 1)	# need to crank it one for always_latch to work in sim

    # Reset state setup
    dut.ui_in.value = 0x00
    dut.uio_in.value = 0x00

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.rst_n.value == 1

    if not GL_TEST:    # Reset state set
        dut.dut.latched_rst_n_ui_in.value == LATCHED_00
        dut.dut.latched_rst_n_uio_in.value == LATCHED_08

    await ClockCycles(dut.clk, 2)

    debug(dut, '001_TEST')

    TICKS_PER_BIT = 3 #int(CLOCK_FREQUENCY / SCL_CLOCK_FREQUENCY)

    #CYCLES_PER_BIT = 3
    #CYCLES_PER_HALFBIT = 1
    #HALF_EDGE = True
    CYCLES_PER_BIT = 6
    CYCLES_PER_HALFBIT = 3
    HALF_EDGE = False

    ctrl = I2CController(dut, CYCLES_PER_BIT = CYCLES_PER_BIT, pp = PUSH_PULL_MODE, GL_TEST = GL_TEST)
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

    report_resolvable(dut, 'checkpoint001 ', depth=depth, filter=exclude_re_path)

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

    report_resolvable(dut, 'checkpoint002 ', depth=depth, filter=exclude_re_path)

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

    report_resolvable(dut, 'checkpoint200 ', depth=depth, filter=exclude_re_path)

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
        dut._log.info(f"STRETCH = {str(data)}  0x{data:02x}")
        if not GL_TEST:	## FIXME reinstante this
            nack = await ctrl.recv_ack()
        #assert nack is None	## FIXME

        await ctrl.send_stop()

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '400_GETCFG')

        await ctrl.send_start()

        await ctrl.send_data(0xc1)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        data = await ctrl.recv_data()
        dut._log.info(f"GETCFG[0] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        # GETCFG not the same layout as LATCHED
        # bit1  SCL MODE
        # bit0  PULLUP MODE
        v = 0
        if SCL_MODE:
            v |= 0x02	# bit1
        if PUSH_PULL_MODE:
            v |= 0x01	# bit0
        if not GL_TEST:	## FIXME reinstate this
            assert data == v

        ctrl.sda_idle()
        assert await ctrl.check_recv_is_idle()

        await ctrl.send_stop()

        ctrl.idle()

        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '410_GETLEN')

        await ctrl.send_start()

        await ctrl.send_data(0xd1)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        data = await ctrl.recv_data()
        dut._log.info(f"GETLEN[0] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        assert data == 0x00

        ctrl.sda_idle()
        debug(dut, '.')
        assert await ctrl.check_recv_is_idle()

        await ctrl.send_stop()

        ctrl.idle()

        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '420_GETENDS')

        await ctrl.send_start()

        await ctrl.send_data(0xe1)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        data = await ctrl.recv_data()
        dut._log.info(f"GETENDS[0] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        if not GL_TEST: ## FIXME reinstante this
            assert data == 0x05

        data = await ctrl.recv_data()
        dut._log.info(f"GETENDS[1] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        assert data == 0x00

        ctrl.sda_idle()
        assert await ctrl.check_recv_is_idle()

        await ctrl.send_stop()

        ctrl.idle()

        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    report_resolvable(dut, 'checkpoint430 ', depth=depth, filter=exclude_re_path)

    if run_this_test(True):
        debug(dut, '430_GETLATCH')

        await ctrl.send_start()

        await ctrl.send_data(0xf1)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        data = await ctrl.recv_data()
        dut._log.info(f"LATCH[0] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        if not GL_TEST:	## FIXME reinstante this, RANDOM_POLICY fixes, ransom is random error PP=true
            assert data == LATCHED_00

        data = await ctrl.recv_data()
        dut._log.info(f"LATCH[1] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        assert data == LATCHED_08

        data = await ctrl.recv_data()
        dut._log.info(f"LATCH[2] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        if not GL_TEST:	## FIXME reinstante this, RANDOM_POLICY fixes, ransom is random error
            assert data == LATCHED_16

        data = await ctrl.recv_data()
        dut._log.info(f"LATCH[3] = {str(data)}  0x{data:02x}")
        await ctrl.send_ack()
        if not GL_TEST:	## FIXME reinstante this, RANDOM_POLICY fixes, ransom is random error
            assert data == LATCHED_24

        ctrl.sda_idle()
        assert await ctrl.check_recv_is_idle()

        await ctrl.send_stop()

        ctrl.idle()

        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '500_SETDATA')

        await ctrl.send_start()

        await ctrl.send_data(0xf8)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x87)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '510_GETDATA')

        await ctrl.send_start()

        await ctrl.send_data(0xf9)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        maxpos = 1
        for pos in range(maxpos):
            data = await ctrl.recv_data()
            dut._log.info(f"GETDATA[{pos}] = {str(data)}  0x{data:02x}")
            await ctrl.send_ack()
            assert data == 0x87

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '520_ALU_ADD')

        await ctrl.send_start()

        await ctrl.send_data(cmd_alu(read=False, len4=0, op_add=True))
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x03)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)



    if run_this_test(True):
        debug(dut, '530_SEND')

        await ctrl.send_start()

        await ctrl.send_data(0xfd)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        maxpos = 2
        for pos in range(maxpos):
            data = await ctrl.recv_data()
            dut._log.info(f"SEND[{pos}] = {str(data)}  0x{data:02x}")
            nack = ctrl.ACK if pos != (maxpos - 1) else ctrl.NACK
            await ctrl.send_acknack(nack)
            assert data == (0x87 + 0x03)

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '540_ALU_XOR')

        await ctrl.send_start()

        await ctrl.send_data(cmd_alu(read=False, len4=1, op_xor=True))
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x08)	# 0x8a => 0x83
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0xc0)	# 0x83 => 0x43
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)



    if run_this_test(True):
        debug(dut, '550_SEND')

        await ctrl.send_start()

        await ctrl.send_data(0xfd)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        maxpos = 3
        for pos in range(maxpos):
            data = await ctrl.recv_data()
            dut._log.info(f"SEND[{pos}] = {str(data)}  0x{data:02x}")
            nack = ctrl.ACK if pos != (maxpos - 1) else ctrl.NACK
            await ctrl.send_acknack(nack)
            assert data == (0x87 + 0x03) ^ 0x08 ^ 0xc0

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '560_ALU_OR')

        await ctrl.send_start()

        await ctrl.send_data(cmd_alu(read=False, len4=2, op_or=True))
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x01)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x02)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x08)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '570_SEND')

        await ctrl.send_start()

        await ctrl.send_data(0xfd)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        maxpos = 4
        for pos in range(maxpos):
            data = await ctrl.recv_data()
            dut._log.info(f"SEND[{pos}] = {str(data)}  0x{data:02x}")
            nack = ctrl.ACK if pos != (maxpos - 1) else ctrl.NACK
            await ctrl.send_acknack(nack)
            assert data == ((0x87 + 0x03) ^ 0x08 ^ 0xc0) | 0x01 | 0x02 | 0x08

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '580_ALU_AND')

        await ctrl.send_start()

        await ctrl.send_data(cmd_alu(read=False, len4=3, op_and=True))
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0xfe)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0xfd)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0x7f)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        await ctrl.send_data(0xf7)	#
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '590_SEND')

        await ctrl.send_start()

        await ctrl.send_data(0xfd)
        nack = await ctrl.recv_ack(ctrl.ACK, CAN_ASSERT)
        if not GL_TEST:	## FIXME reinstante this
            assert nack is ctrl.ACK

        maxpos = 5
        for pos in range(maxpos):
            data = await ctrl.recv_data()
            dut._log.info(f"SEND[{pos}] = {str(data)}  0x{data:02x}")
            nack = ctrl.ACK if pos != (maxpos - 1) else ctrl.NACK
            await ctrl.send_acknack(nack)
            assert data == (((0x87 + 0x03) ^ 0x08 ^ 0xc0) | 0x01 | 0x02 | 0x08) & 0xfe & 0xfd & 0x7f & 0xf7

        assert await ctrl.check_recv_is_idle()
        await ctrl.send_stop()
        ctrl.idle()
        assert await ctrl.check_recv_has_been_idle(CYCLES_PER_BIT*3)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)



    ##############################################################################################

    # FIXME observe FSM cycle RESET->HUNT

    if run_this_test(True):
        debug(dut, '800_TIMEOUT_START')

        ctrl.idle()

        await ctrl.send_start()

        ctrl.idle()
        await ClockCycles(dut.clk, CYCLES_PER_BIT*12)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        for bitid in range(8):
            debug(dut, f"81{bitid}_TIMEOUT_{bitid}BITS")

            ctrl.idle()

            await ctrl.send_start()
            for loop in range(bitid):
                await ctrl.send_bit(bool(random.getrandbits(1)))

            ctrl.idle()
            await ClockCycles(dut.clk, CYCLES_PER_BIT*12)

            debug(dut, '')
            await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        for bitid in range(8):
            debug(dut, f"85{bitid}_STOP_{bitid}BITS")

            ctrl.idle()

            await ctrl.send_start()
            for loop in range(bitid):
                await ctrl.send_bit(bool(random.getrandbits(1)))
            await ctrl.send_stop();

            ctrl.idle()
            await ClockCycles(dut.clk, CYCLES_PER_BIT*12)

            debug(dut, '')
            await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '860_TIMEOUT_STARTSTOP')

        ctrl.idle()

        await ctrl.send_start()
        await ctrl.send_stop()

        ctrl.idle()
        await ClockCycles(dut.clk, CYCLES_PER_BIT*12)

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '880_STOPTEST1')

        ctrl.idle()

        await ctrl.send_stop()
        # observe FSM cycle RESET->HUNT

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)


    if run_this_test(True):
        debug(dut, '890_STOPTEST2')

        ctrl.idle()

        await ctrl.send_stop()
        # observe FSM cycle RESET->HUNT

        ctrl.idle()

        debug(dut, '')
        await ClockCycles(dut.clk, CYCLES_PER_BIT*4)

    ##############################################################################################

    await ClockCycles(dut.clk, 256)

    ##############################################################################################

    if run_this_test(True):
        debug(dut, '900_CMD00_RESET')


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

