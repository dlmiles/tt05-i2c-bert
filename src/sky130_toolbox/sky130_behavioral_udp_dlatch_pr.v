`timescale 1ns / 1ps
`default_nettype none

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
