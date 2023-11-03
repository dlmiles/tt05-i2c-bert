//
// SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
// SPDX-License-Identifier: Apache2.0
//
`default_nettype none
`ifdef TIMESCALE
`timescale 1ns/1ps
`endif
// for use as behavioral only
`ifndef SYNTHESIS
// udp_dlatch$PR
module sky130_fd_sc_hd__udp_dlatch$PR (
    Q    ,
    D    ,
    GATE ,
    RESET
);

    output Q    ;
    input  D    ;
    input  GATE ;
    input  RESET;

    reg Q;

    always_latch begin
        if (RESET) begin
            Q = 0;		// immediate async
        end else if (GATE) begin
`ifdef TIMING
            // TIMING is not allowed inside always_latch
            //#1			// at next simtime tick
`endif
            Q = D;
        end
    end

endmodule
`endif // SYNTHESIS
