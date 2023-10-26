//
// SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
// SPDX-License-Identifier: Apache2.0
//
`default_nettype none
`timescale 1ns/1ps

`include "config.vh"

module tb_i2c_bert (
`ifdef HAVE_DEBUG_I2C
    output                      debug_SCL_od,
    output                      debug_SCL_pp,
    output                      debug_SCL_og,
    output                      debug_SCL_pg,

    output                      debug_SDA_od,
    output                      debug_SDA_pp,
    output                      debug_SDA_og,
    output                      debug_SDA_pg,
`endif
    //input			clk,
    //input			rst_n,	// async (verilator needed reg)
    //input			ena,

    output		[7:0]	uo_out,
    //input		[7:0]	ui_in,

    output		[7:0]	uio_out,
    //input		[7:0]	uio_in,
    output		[7:0]	uio_oe
);
`ifndef SYNTHESIS
    reg [(8*32)-1:0] DEBUG;
    reg DEBUG_wire;
`endif

    reg clk;
    reg rst_n;
    reg ena;

    reg [7:0] ui_in;
    reg [7:0] uio_in;
`ifdef HAVE_DEBUG_I2C
    reg debug_SCL_ie;
    reg debug_SDA_ie;
`endif

    initial begin
        //$dumpfile ("tb_i2c_bert.vcd");
        $dumpfile ("tb.vcd");	// Renamed for GHA
`ifdef GL_TEST
        // the internal state of a flattened verilog is not that interesting
        $dumpvars (1, tb_i2c_bert);
`else
        $dumpvars (0, tb_i2c_bert);
`endif
`ifdef TIMING
        #1;
`endif
`ifndef SYNTHESIS
        DEBUG = {8'h44, 8'h45, 8'h42, 8'h55, 8'h47, {27{8'h20}}}; // "DEBUG        "
        DEBUG_wire = 0;
`endif
    end


    tt_um_dlmiles_tt05_i2c_bert dut (
`ifdef USE_POWER_PINS
        .VPWR     ( 1'b1),              //i
        .VGND     ( 1'b0),              //i
`endif
`ifdef USE_POWER_PINS_LEGACY
        .vccd1    ( 1'b1),              //i
        .vssd1    ( 1'b0),              //i
`endif
`ifdef HAVE_DEBUG_I2C
        .debug_SCL_ie  (debug_SCL_ie),		//i
        .debug_SCL_od  (debug_SCL_od),		//o
        .debug_SCL_pp  (debug_SCL_pp),		//o
        .debug_SCL_og  (debug_SCL_og),		//o
        .debug_SCL_pg  (debug_SCL_pg),		//o

        .debug_SDA_ie  (debug_SDA_ie),		//i
        .debug_SDA_od  (debug_SDA_od),		//o
        .debug_SDA_pp  (debug_SDA_pp),		//o
        .debug_SDA_og  (debug_SDA_og),		//o
        .debug_SDA_pg  (debug_SDA_pg),		//o
`endif
        .clk      (clk),                //i
        .rst_n    (rst_n),              //i
        .ena      (ena),                //i
        .uo_out   (uo_out),             //o
        .ui_in    (ui_in),              //i
        .uio_out  (uio_out),            //o
        .uio_in   (uio_in),             //i
        .uio_oe   (uio_oe)              //o
    );

endmodule
