# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog


ifneq ($(CI),true)
# Only for local simulation, at this time all CI and production removes this feature,
#  but ideally we want it included in GHA pre-synth simulation (need to add verilog ifdef)
NOCI_COMPILE_ARGS = -DHAVE_DEBUG_I2C
NOCI_EXTRA_ARGS   = -DHAVE_DEBUG_I2C
endif

# normal simulation
ifneq ($(GATES),yes)

# this is the only part you should need to modify:
VERILOG_SOURCES += $(PWD)/tbc_tt_um_dlmiles_tt05_i2c_bert.v
VERILOG_SOURCES += $(PWD)/top_tt_um_dlmiles_tt05_i2c_bert.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/dffqn_negedge.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/dff.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/glitch_free_clock_mux.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/dffqn_negedge_async_reset.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/dff_async_reset.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/glitch_free_clock_mux_async_reset.v
VERILOG_SOURCES += $(PWD)/sky130_toolbox/sky130_behavioral_udp_dlatch_pr.v
VERILOG_SOURCES += $(PWD)/pdk_generic/sky130_fd_sc_hd__dlrtp.v
VERILOG_SOURCES += $(PWD)/pdk_generic/sky130_fd_sc_hd__maj3.v
VERILOG_SOURCES += $(PWD)/TT05I2CBertTop.v

ifeq ($(SIM),icarus)
# FIXME review this (for the maj3.v)
COMPILE_ARGS    += -DFUNCTIONAL
endif


else

# gate level simulation requires some extra setup, you shouldn't need to touch this
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=\#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v
#VERILOG_SOURCES += sky130_fd_sc_hd/primitives.v
#VERILOG_SOURCES += sky130_fd_sc_hd/sky130_fd_sc_hd.v

# this gets copied in by the GDS action workflow
VERILOG_SOURCES += $(PWD)/tbc_tt_um_dlmiles_tt05_i2c_bert.v $(PWD)/gate_level_netlist.v
endif

ifeq ($(SIM),icarus)
COMPILE_ARGS    += -DTIMING
COMPILE_ARGS    += -DUNIT_DELAY=\#1
COMPILE_ARGS    += $(NOCI_COMPILE_ARGS)
endif

ifeq ($(SIM),verilator)
EXTRA_ARGS += -Wno-WIDTHTRUNC
EXTRA_ARGS += --trace --trace-structs --no-timing
# FIXME review this (for the maj3.v)
EXTRA_ARGS += -DFUNCTIONAL
EXTRA_ARGS += -DUNIT_DELAY=
#COMPILE_ARGS    += -DUSE_POWER_PINS
EXTRA_ARGS += $(NOCI_EXTRA_ARGS)

ifeq ($(COVERAGE),yes)
EXTRA_ARGS += --coverage --coverage-underscore
endif

ifeq ($(RANDOM_POLICY),zero)
PLUSARGS += +verilator+rand+reset+0
else ifeq ($(RANDOM_POLICY),one)
PLUSARGS += +verilator+rand+reset+1
else ifeq ($(RANDOM_POLICY),random)
PLUSARGS += +verilator+rand+reset+2
endif
endif

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = tb_i2c_bert

# MODULE is the basename of the Python test file
MODULE = test_i2c_bert

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
