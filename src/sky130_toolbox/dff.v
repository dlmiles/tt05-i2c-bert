//
// SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
// SPDX-License-Identifier: Apache2.0
//
`default_nettype none
`ifdef TIMESCALE
`timescale 1ns/1ps
`endif
//
// MetaData-1.0::
// Module-Name: dff
// Module-Language: Verilog-200?
// Input-Count: 2
// input-1: clk Clock (posedge)
// input-2: d data
// Output-Count: 1
// Output-1: q Q
//
//
//  D Flip-Flop (verilog register simulation)
//	Master-Slave D type FlipFlop
//	One such implementation can be made from a
//	Level Triggered Gated SR Latch connected to
//      output of a Level Triggered Gated D Latch
//	with an inverter added to the clock line internally.
//	UPPERCASE represents external signal names
//		sr_latch_nand_gated(.s(sr_set_net_Qm), .r(sr_reset_net), .e(!CLK), .q(Q), .qn(QN))	// slave
//		d_latch_nand(.d(D), .gate(CLK), .q(sr_set_net_Qm), .qn(sr_reset_net))	// master
//
//
//
module dff (
    input  wire			clk,
    input  wire			d,

    output  reg			q
);

    always @(posedge clk) begin
        q <= d;
    end

endmodule
