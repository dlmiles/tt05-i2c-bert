//
// SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
// SPDX-License-Identifier: Apache2.0
//
`default_nettype none

module tt_um_dlmiles_tt05_i2c_bert (
`ifdef HAVE_DEBUG_I2C
    input  wire                 debug_SCL_ie,
    output wire                 debug_SCL_od,
    output wire                 debug_SCL_pp,
    output wire                 debug_SCL_og,
    output wire                 debug_SCL_pg,

    input  wire                 debug_SDA_ie,
    output wire                 debug_SDA_od,
    output wire                 debug_SDA_pp,
    output wire                 debug_SDA_og,
    output wire                 debug_SDA_pg,
`endif
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output wire [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);


    TT05I2CBertTop i2c_bert (
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

        .clk        (clk),              //i
        .rst_n      (rst_n),            //i
        .ena        (ena),              //i

        .ui_in      (ui_in),            //i
        .uo_out     (uo_out),           //o
        .uio_in     (uio_in),           //i
        .uio_out    (uio_out),          //o
        .uio_oe     (uio_oe)            //o
    );


endmodule
