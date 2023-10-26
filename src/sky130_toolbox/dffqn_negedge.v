//
// SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
// SPDX-License-Identifier: Apache2.0
//
`default_nettype none
`timescale 1ns/1ps
//
// MetaData-1.0::
// Module-Name: dffqn_negedge
// Module-Language: Verilog-200?
// Input-Count: 2
// input-1: clk Clock (negedge)
// input-2: d data
// Output-Count: 2
// Output-1: q Q
// Output-2: qn Q-Inverted
//
//
//  D Flip-Flop (verilog register simulation)
//
//
//
module dffqn_negedge (
    input			clk,
    input			d,

    output reg			q,
    output			qn
);

    always @(negedge clk) begin
        q <= d;
    end

    assign qn = ~q;

endmodule
