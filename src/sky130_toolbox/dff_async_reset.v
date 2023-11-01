`default_nettype none
`timescale 1ns/1ps
//
// MetaData-1.0::
// Module-Name: dff_async_reset
// Module-Language: Verilog-200?
// Input-Count: 3
// Input-1: clk Clock (posedge)
// Input-2: reset Reset (async active-high)
// Input-3: d data
// Output-Count: 1
// Output-1: q Q
//
//
//  D Flip-Flop, async Reset (active HIGH) (verilog register simulation)
//
//
//
module dff_async_reset (
    input		clk,
    input		reset,	// active high
    input		d,

    output reg		q
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            q <= 0;		// reset
        end else begin
            q <= d;
        end
    end

endmodule
