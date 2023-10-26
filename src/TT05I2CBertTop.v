// Generator : SpinalHDL dev    git head : efcba5fcd17d0cfe48fa0981e8dec6e70234b294
// Component : TT05I2CBertTop

`timescale 1ns/1ps

module TT05I2CBertTop (
  input               ena /* verilator public */ ,
  output     [7:0]    uo_out /* verilator public */ ,
  input      [7:0]    ui_in /* verilator public */ ,
  output reg [7:0]    uio_out /* verilator public */ ,
  input      [7:0]    uio_in /* verilator public */ ,
  output reg [7:0]    uio_oe /* verilator public */ ,
  output              debug_SCL_od /* verilator public */ ,
  output              debug_SCL_pp /* verilator public */ ,
  input               debug_SCL_ie /* verilator public */ ,
  output              debug_SCL_og /* verilator public */ ,
  output              debug_SCL_pg /* verilator public */ ,
  output              debug_SDA_od /* verilator public */ ,
  output              debug_SDA_pp /* verilator public */ ,
  input               debug_SDA_ie /* verilator public */ ,
  output              debug_SDA_og /* verilator public */ ,
  output              debug_SDA_pg /* verilator public */ ,
  input               rst_n,
  input               clk
);

  wire                i2c_io_bus_sclIn;
  wire                i2c_io_bus_sdaIn;
  wire                timer_1_io_sclTick;
  wire                timer_1_io_timeoutError;
  wire                timer_1_io_canPowerOnReset;
  wire                timer_1_io_canStart;
  wire                i2c_io_bus_sclOut;
  wire                i2c_io_bus_sclOe;
  wire                i2c_io_bus_sdaOut;
  wire                i2c_io_bus_sdaOe;
  wire                i2c_io_timerRun;
  wire                i2c_io_wantReset;
  wire                i2c_io_wantStart;
  wire                i2c_io_wantTick;
  wire       [7:0]    i2c_io_data8rx;
  wire       [7:0]    i2c_io_data8rxNow;
  wire                myState_1_io_canSend;
  wire                myState_1_io_canRecv;
  wire       [7:0]    myState_1_io_data8tx;
  wire                _zz_debug_SCL_od;
  wire                _zz_debug_SCL_od_1;
  wire                _zz_debug_SCL_od_2;
  wire                _zz_debug_SDA_od;
  wire                _zz_debug_SDA_od_1;
  wire                _zz_debug_SDA_od_2;
  wire                when_Latch_l15;
  reg                 pushPullMode;
  wire                when_Latch_l15_1;
  reg                 sclMode;
  wire                div12active;
  wire       [11:0]   div12;

  Timer timer_1 (
    .io_sclTick         (timer_1_io_sclTick        ), //o
    .io_timeoutError    (timer_1_io_timeoutError   ), //o
    .io_timerRun        (i2c_io_timerRun           ), //i
    .io_timerLoad       (1'b0                      ), //i
    .io_canPowerOnReset (timer_1_io_canPowerOnReset), //o
    .io_canStart        (timer_1_io_canStart       ), //o
    .io_div12active     (div12active               ), //i
    .io_div12           (div12[11:0]               ), //i
    .rst_n              (rst_n                     ), //i
    .clk                (clk                       )  //i
  );
  MyI2C i2c (
    .io_bus_sclOut   (i2c_io_bus_sclOut        ), //o
    .io_bus_sclIn    (i2c_io_bus_sclIn         ), //i
    .io_bus_sclOe    (i2c_io_bus_sclOe         ), //o
    .io_bus_sdaOut   (i2c_io_bus_sdaOut        ), //o
    .io_bus_sdaIn    (i2c_io_bus_sdaIn         ), //i
    .io_bus_sdaOe    (i2c_io_bus_sdaOe         ), //o
    .io_sclTick      (timer_1_io_sclTick       ), //i
    .io_timeoutError (timer_1_io_timeoutError  ), //i
    .io_timerRun     (i2c_io_timerRun          ), //o
    .io_canRecv      (myState_1_io_canRecv     ), //i
    .io_canSend      (myState_1_io_canSend     ), //i
    .io_wantReset    (i2c_io_wantReset         ), //o
    .io_wantStart    (i2c_io_wantStart         ), //o
    .io_wantTick     (i2c_io_wantTick          ), //o
    .io_data8rx      (i2c_io_data8rx[7:0]      ), //o
    .io_data8rxNow   (i2c_io_data8rxNow[7:0]   ), //o
    .io_data8tx      (myState_1_io_data8tx[7:0]), //i
    .io_sclMode      (sclMode                  ), //i
    .io_pushPullMode (pushPullMode             ), //i
    .clk             (clk                      ), //i
    .rst_n           (rst_n                    )  //i
  );
  MyState myState_1 (
    .io_wantReset    (i2c_io_wantReset         ), //i
    .io_wantStart    (i2c_io_wantStart         ), //i
    .io_wantTick     (i2c_io_wantTick          ), //i
    .io_canSend      (myState_1_io_canSend     ), //o
    .io_canRecv      (myState_1_io_canRecv     ), //o
    .io_datain8rx    (i2c_io_data8rx[7:0]      ), //i
    .io_datain8rxNow (i2c_io_data8rxNow[7:0]   ), //i
    .io_data8tx      (myState_1_io_data8tx[7:0]), //o
    .clk             (clk                      ), //i
    .rst_n           (rst_n                    )  //i
  );
  assign uo_out = 8'bxxxxxxxx;
  always @(*) begin
    uio_out = 8'bxxxxxxxx;
    uio_out[2] = i2c_io_bus_sdaOut;
    uio_out[3] = i2c_io_bus_sclOut;
  end

  always @(*) begin
    uio_oe = 8'h00;
    uio_oe[2] = i2c_io_bus_sdaOe;
    uio_oe[3] = i2c_io_bus_sclOe;
  end

  assign _zz_debug_SCL_od = uio_out[3];
  assign _zz_debug_SCL_od_1 = uio_oe[3];
  assign _zz_debug_SCL_od_2 = uio_in[3];
  assign debug_SCL_od = (_zz_debug_SCL_od_1 ? _zz_debug_SCL_od : ((debug_SCL_ie && (! _zz_debug_SCL_od_2)) ? _zz_debug_SCL_od_2 : 1'bx));
  assign debug_SCL_og = ((_zz_debug_SCL_od_1 && _zz_debug_SCL_od) ? 1'b0 : ((debug_SCL_ie && _zz_debug_SCL_od_2) ? 1'b0 : ((_zz_debug_SCL_od_1 && (! _zz_debug_SCL_od)) ? 1'b1 : ((debug_SCL_ie && (! _zz_debug_SCL_od_2)) ? 1'b1 : 1'bx))));
  assign debug_SCL_pp = (_zz_debug_SCL_od_1 ? _zz_debug_SCL_od : (debug_SCL_ie ? _zz_debug_SCL_od_2 : 1'bx));
  assign debug_SCL_pg = ((_zz_debug_SCL_od_1 && debug_SCL_ie) ? 1'b0 : (_zz_debug_SCL_od_1 ? 1'b1 : (debug_SCL_ie ? 1'b1 : (((! debug_SCL_ie) && (! _zz_debug_SCL_od_2)) ? 1'b1 : 1'bx))));
  assign _zz_debug_SDA_od = uio_out[2];
  assign _zz_debug_SDA_od_1 = uio_oe[2];
  assign _zz_debug_SDA_od_2 = uio_in[2];
  assign debug_SDA_od = (_zz_debug_SDA_od_1 ? _zz_debug_SDA_od : ((debug_SDA_ie && (! _zz_debug_SDA_od_2)) ? _zz_debug_SDA_od_2 : 1'bx));
  assign debug_SDA_og = ((_zz_debug_SDA_od_1 && _zz_debug_SDA_od) ? 1'b0 : ((debug_SDA_ie && _zz_debug_SDA_od_2) ? 1'b0 : ((_zz_debug_SDA_od_1 && (! _zz_debug_SDA_od)) ? 1'b1 : ((debug_SDA_ie && (! _zz_debug_SDA_od_2)) ? 1'b1 : 1'bx))));
  assign debug_SDA_pp = (_zz_debug_SDA_od_1 ? _zz_debug_SDA_od : (debug_SDA_ie ? _zz_debug_SDA_od_2 : 1'bx));
  assign debug_SDA_pg = ((_zz_debug_SDA_od_1 && debug_SDA_ie) ? 1'b0 : (_zz_debug_SDA_od_1 ? 1'b1 : (debug_SDA_ie ? 1'b1 : (((! debug_SDA_ie) && (! _zz_debug_SDA_od_2)) ? 1'b1 : 1'bx))));
  assign when_Latch_l15 = (! rst_n);
  always_latch begin
    if(when_Latch_l15) begin
      pushPullMode = ui_in[2];
    end
  end

  assign when_Latch_l15_1 = (! rst_n);
  always_latch begin
    if(when_Latch_l15_1) begin
      sclMode = ui_in[1];
    end
  end

  assign div12active = ui_in[3];
  assign div12 = {uio_in[7 : 0],ui_in[7 : 4]};
  assign i2c_io_bus_sdaIn = uio_in[2];
  assign i2c_io_bus_sclIn = uio_in[3];

endmodule

module MyState (
  input               io_wantReset,
  input               io_wantStart,
  input               io_wantTick,
  output reg          io_canSend,
  output reg          io_canRecv,
  input      [7:0]    io_datain8rx,
  input      [7:0]    io_datain8rxNow,
  output reg [7:0]    io_data8tx,
  input               clk,
  input               rst_n
);
  localparam fsmPhase_enumDef_BOOT = 3'd0;
  localparam fsmPhase_enumDef_RESET = 3'd1;
  localparam fsmPhase_enumDef_CONTROL = 3'd2;
  localparam fsmPhase_enumDef_RECV = 3'd3;
  localparam fsmPhase_enumDef_SEND = 3'd4;

  wire       [1:0]    alu_1_io_op;
  reg                 alu_1_io_reset;
  reg                 alu_1_io_en;
  wire       [7:0]    alu_1_io_acc;
  reg                 readWriteBit;
  reg        [6:0]    cmd7;
  reg        [7:0]    cmd8;
  reg        [7:0]    len8;
  wire       [11:0]   len12;
  reg        [11:0]   counter;
  wire                muxDataOut8Alu;
  reg                 fsmPhase_wantExit;
  reg                 fsmPhase_wantStart;
  wire                fsmPhase_wantKill;
  reg        [2:0]    fsmPhase_stateReg;
  reg        [2:0]    fsmPhase_stateNext;
  wire                when_I2CBertTop_l230;
  wire                when_I2CBertTop_l231;
  wire                when_I2CBertTop_l235;
  wire                when_I2CBertTop_l243;
  wire                when_I2CBertTop_l259;
  wire                when_I2CBertTop_l260;
  `ifndef SYNTHESIS
  reg [55:0] fsmPhase_stateReg_string;
  reg [55:0] fsmPhase_stateNext_string;
  `endif


  ALU alu_1 (
    .io_acc   (alu_1_io_acc[7:0]), //o
    .io_opand (io_datain8rx[7:0]), //i
    .io_op    (alu_1_io_op[1:0] ), //i
    .io_reset (alu_1_io_reset   ), //i
    .io_en    (alu_1_io_en      ), //i
    .clk      (clk              ), //i
    .rst_n    (rst_n            )  //i
  );
  `ifndef SYNTHESIS
  always @(*) begin
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_BOOT : fsmPhase_stateReg_string = "BOOT   ";
      fsmPhase_enumDef_RESET : fsmPhase_stateReg_string = "RESET  ";
      fsmPhase_enumDef_CONTROL : fsmPhase_stateReg_string = "CONTROL";
      fsmPhase_enumDef_RECV : fsmPhase_stateReg_string = "RECV   ";
      fsmPhase_enumDef_SEND : fsmPhase_stateReg_string = "SEND   ";
      default : fsmPhase_stateReg_string = "???????";
    endcase
  end
  always @(*) begin
    case(fsmPhase_stateNext)
      fsmPhase_enumDef_BOOT : fsmPhase_stateNext_string = "BOOT   ";
      fsmPhase_enumDef_RESET : fsmPhase_stateNext_string = "RESET  ";
      fsmPhase_enumDef_CONTROL : fsmPhase_stateNext_string = "CONTROL";
      fsmPhase_enumDef_RECV : fsmPhase_stateNext_string = "RECV   ";
      fsmPhase_enumDef_SEND : fsmPhase_stateNext_string = "SEND   ";
      default : fsmPhase_stateNext_string = "???????";
    endcase
  end
  `endif

  always @(*) begin
    io_canSend = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
        io_canSend = 1'b1;
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_canRecv = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
        io_canRecv = 1'b1;
      end
      fsmPhase_enumDef_RECV : begin
        io_canRecv = 1'b1;
      end
      fsmPhase_enumDef_SEND : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    cmd8[7 : 1] = cmd7;
    cmd8[0] = readWriteBit;
  end

  assign len12 = {len8,cmd8[7 : 4]};
  always @(*) begin
    alu_1_io_reset = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
        if(io_wantTick) begin
          if(when_I2CBertTop_l230) begin
            if(when_I2CBertTop_l231) begin
              alu_1_io_reset = 1'b1;
            end
          end else begin
            if(when_I2CBertTop_l243) begin
              alu_1_io_reset = 1'b1;
            end
          end
        end
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    alu_1_io_en = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          alu_1_io_en = 1'b1;
        end
      end
      fsmPhase_enumDef_SEND : begin
      end
      default : begin
      end
    endcase
  end

  assign alu_1_io_op = cmd8[2 : 1];
  assign muxDataOut8Alu = 1'b0;
  always @(*) begin
    io_data8tx = (muxDataOut8Alu ? alu_1_io_acc : io_datain8rx);
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
        if(io_wantTick) begin
          io_data8tx = alu_1_io_acc;
        end
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    fsmPhase_wantExit = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
        if(io_wantTick) begin
          fsmPhase_wantExit = 1'b1;
        end
      end
      fsmPhase_enumDef_CONTROL : begin
        if(io_wantTick) begin
          if(when_I2CBertTop_l230) begin
            if(!when_I2CBertTop_l231) begin
              if(!when_I2CBertTop_l235) begin
                fsmPhase_wantExit = 1'b1;
              end
            end
          end
        end
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      default : begin
      end
    endcase
    if(io_wantReset) begin
      fsmPhase_wantExit = 1'b1;
    end
  end

  always @(*) begin
    fsmPhase_wantStart = 1'b0;
    if(io_wantStart) begin
      fsmPhase_wantStart = 1'b1;
    end
  end

  assign fsmPhase_wantKill = 1'b0;
  always @(*) begin
    fsmPhase_stateNext = fsmPhase_stateReg;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
        if(io_wantTick) begin
          fsmPhase_stateNext = fsmPhase_enumDef_BOOT;
        end
      end
      fsmPhase_enumDef_CONTROL : begin
        if(io_wantTick) begin
          if(when_I2CBertTop_l230) begin
            if(when_I2CBertTop_l231) begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end else begin
              if(when_I2CBertTop_l235) begin
                fsmPhase_stateNext = fsmPhase_enumDef_SEND;
              end else begin
                fsmPhase_stateNext = fsmPhase_enumDef_BOOT;
              end
            end
          end else begin
            if(when_I2CBertTop_l243) begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end else begin
              fsmPhase_stateNext = fsmPhase_enumDef_RECV;
            end
          end
        end
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          if(when_I2CBertTop_l259) begin
            if(!when_I2CBertTop_l260) begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
          end
        end
      end
      fsmPhase_enumDef_SEND : begin
        if(io_wantTick) begin
          fsmPhase_stateNext = fsmPhase_enumDef_RESET;
        end
      end
      default : begin
      end
    endcase
    if(io_wantReset) begin
      fsmPhase_stateNext = fsmPhase_enumDef_BOOT;
    end
    if(fsmPhase_wantStart) begin
      fsmPhase_stateNext = fsmPhase_enumDef_CONTROL;
    end
    if(fsmPhase_wantKill) begin
      fsmPhase_stateNext = fsmPhase_enumDef_BOOT;
    end
  end

  assign when_I2CBertTop_l230 = io_datain8rx[0];
  assign when_I2CBertTop_l231 = (io_datain8rx[2 : 1] == 2'b10);
  assign when_I2CBertTop_l235 = (io_datain8rx[2 : 1] == 2'b11);
  assign when_I2CBertTop_l243 = (io_datain8rx[7 : 4] == 4'b1111);
  assign when_I2CBertTop_l259 = (counter == len12);
  assign when_I2CBertTop_l260 = 1'b0;
  always @(posedge clk) begin
    if(!rst_n) begin
      len8 <= 8'h00;
      counter <= 12'h001;
      fsmPhase_stateReg <= fsmPhase_enumDef_BOOT;
    end else begin
      fsmPhase_stateReg <= fsmPhase_stateNext;
      case(fsmPhase_stateReg)
        fsmPhase_enumDef_RESET : begin
        end
        fsmPhase_enumDef_CONTROL : begin
          if(io_wantTick) begin
            if(when_I2CBertTop_l230) begin
              if(when_I2CBertTop_l231) begin
                len8 <= 8'h00;
              end else begin
                if(when_I2CBertTop_l235) begin
                  counter <= 12'h000;
                end
              end
            end else begin
              if(when_I2CBertTop_l243) begin
                len8 <= 8'h00;
              end else begin
                counter <= 12'h000;
              end
            end
          end
        end
        fsmPhase_enumDef_RECV : begin
          if(io_wantTick) begin
            if(!when_I2CBertTop_l259) begin
              counter <= (counter + 12'h001);
            end
          end
        end
        fsmPhase_enumDef_SEND : begin
          if(io_wantTick) begin
            counter <= (counter + 12'h001);
          end
        end
        default : begin
        end
      endcase
    end
  end

  always @(posedge clk) begin
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
        if(io_wantTick) begin
          readWriteBit <= io_datain8rx[0];
          cmd7 <= io_datain8rx[7 : 1];
        end
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      default : begin
      end
    endcase
  end


endmodule

module MyI2C (
  output              io_bus_sclOut,
  input               io_bus_sclIn,
  output              io_bus_sclOe,
  output reg          io_bus_sdaOut,
  input               io_bus_sdaIn,
  output reg          io_bus_sdaOe,
  input               io_sclTick,
  input               io_timeoutError,
  output reg          io_timerRun,
  input               io_canRecv,
  input               io_canSend,
  output reg          io_wantReset,
  output reg          io_wantStart,
  output reg          io_wantTick,
  output reg [7:0]    io_data8rx,
  output     [7:0]    io_data8rxNow,
  input      [7:0]    io_data8tx,
  input               io_sclMode,
  input               io_pushPullMode,
  input               clk,
  input               rst_n
);
  localparam fsm_enumDef_BOOT = 4'd0;
  localparam fsm_enumDef_RESET = 4'd1;
  localparam fsm_enumDef_HUNT = 4'd2;
  localparam fsm_enumDef_RECV = 4'd3;
  localparam fsm_enumDef_ACKNACK = 4'd4;
  localparam fsm_enumDef_ACK = 4'd5;
  localparam fsm_enumDef_NACK = 4'd6;
  localparam fsm_enumDef_SEND = 4'd7;
  localparam fsm_enumDef_PRECHECK = 4'd8;
  localparam fsm_enumDef_CHECK = 4'd9;

  wire                maj3_X;
  wire                clockGate_clk_out;
  wire                history_0;
  reg                 history_1;
  reg                 history_2;
  wire                sda;
  wire                sdaAtReset;
  wire                sdaAtResetCaptured;
  wire                attention;
  reg                 sclSignalNext;
  wire                scl;
  wire                sdaEdge_rise;
  wire                sdaEdge_fall;
  wire                sdaEdge_toggle;
  reg                 i2c_maj3_X_regNext;
  wire                sclEdge_rise;
  wire                sclEdge_fall;
  wire                sclEdge_toggle;
  reg                 scl_regNext;
  wire                isStart;
  wire                isStop;
  reg        [7:0]    shifter;
  wire       [7:0]    shifterNow;
  reg                 fsm_wantExit;
  reg                 fsm_wantStart;
  wire                fsm_wantKill;
  reg        [2:0]    fsm_bitCount;
  reg        [3:0]    fsm_stateReg;
  reg        [3:0]    fsm_stateNext;
  wire                when_I2CBertTop_l471;
  wire                when_I2CBertTop_l500;
  wire                when_I2CBertTop_l489;
  wire                when_I2CBertTop_l518;
  `ifndef SYNTHESIS
  reg [63:0] fsm_stateReg_string;
  reg [63:0] fsm_stateNext_string;
  `endif


  sky130_fd_sc_hd__maj3 maj3 (
    .A (history_0), //i
    .B (history_1), //i
    .C (history_2), //i
    .X (maj3_X   )  //o
  );
  glitch_free_clock_mux clockGate (
    .clk_0   (sclSignalNext    ), //i
    .clk_1   (io_sclTick       ), //i
    .sel     (io_sclMode       ), //i
    .clk_out (clockGate_clk_out)  //o
  );
  `ifndef SYNTHESIS
  always @(*) begin
    case(fsm_stateReg)
      fsm_enumDef_BOOT : fsm_stateReg_string = "BOOT    ";
      fsm_enumDef_RESET : fsm_stateReg_string = "RESET   ";
      fsm_enumDef_HUNT : fsm_stateReg_string = "HUNT    ";
      fsm_enumDef_RECV : fsm_stateReg_string = "RECV    ";
      fsm_enumDef_ACKNACK : fsm_stateReg_string = "ACKNACK ";
      fsm_enumDef_ACK : fsm_stateReg_string = "ACK     ";
      fsm_enumDef_NACK : fsm_stateReg_string = "NACK    ";
      fsm_enumDef_SEND : fsm_stateReg_string = "SEND    ";
      fsm_enumDef_PRECHECK : fsm_stateReg_string = "PRECHECK";
      fsm_enumDef_CHECK : fsm_stateReg_string = "CHECK   ";
      default : fsm_stateReg_string = "????????";
    endcase
  end
  always @(*) begin
    case(fsm_stateNext)
      fsm_enumDef_BOOT : fsm_stateNext_string = "BOOT    ";
      fsm_enumDef_RESET : fsm_stateNext_string = "RESET   ";
      fsm_enumDef_HUNT : fsm_stateNext_string = "HUNT    ";
      fsm_enumDef_RECV : fsm_stateNext_string = "RECV    ";
      fsm_enumDef_ACKNACK : fsm_stateNext_string = "ACKNACK ";
      fsm_enumDef_ACK : fsm_stateNext_string = "ACK     ";
      fsm_enumDef_NACK : fsm_stateNext_string = "NACK    ";
      fsm_enumDef_SEND : fsm_stateNext_string = "SEND    ";
      fsm_enumDef_PRECHECK : fsm_stateNext_string = "PRECHECK";
      fsm_enumDef_CHECK : fsm_stateNext_string = "CHECK   ";
      default : fsm_stateNext_string = "????????";
    endcase
  end
  `endif

  always @(*) begin
    io_bus_sdaOut = (! io_pushPullMode);
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l500) begin
          io_bus_sdaOut = ((! io_canSend) && (! io_canRecv));
        end
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
        if(scl) begin
          io_bus_sdaOut = shifter[0];
        end
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_bus_sdaOe = (io_pushPullMode && io_bus_sdaOut);
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l500) begin
          io_bus_sdaOe = 1'b1;
        end
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
        io_bus_sdaOe = 1'b1;
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
      end
    endcase
  end

  assign io_bus_sclOut = 1'b1;
  assign io_bus_sclOe = (io_pushPullMode && io_bus_sclOut);
  always @(*) begin
    io_timerRun = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
        io_timerRun = 1'b1;
      end
      fsm_enumDef_ACKNACK : begin
        io_timerRun = 1'b1;
        if(when_I2CBertTop_l500) begin
          if(scl) begin
            io_timerRun = 1'b0;
          end
        end
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
        io_timerRun = 1'b1;
      end
      fsm_enumDef_PRECHECK : begin
        io_timerRun = 1'b1;
      end
      fsm_enumDef_CHECK : begin
        io_timerRun = 1'b1;
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_wantReset = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
        io_wantReset = 1'b1;
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_wantStart = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
        if(isStart) begin
          io_wantStart = 1'b1;
        end
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_wantTick = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
        if(scl) begin
          if(when_I2CBertTop_l471) begin
            if(io_canRecv) begin
              io_wantTick = 1'b1;
            end
          end
        end
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
        if(scl) begin
          if(when_I2CBertTop_l489) begin
            io_wantTick = 1'b1;
          end
        end
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_data8rx = 8'bxxxxxxxx;
    io_data8rx = shifter;
  end

  assign history_0 = io_bus_sdaIn;
  assign sda = (io_sclMode ? maj3_X : history_0);
  assign sdaAtReset = io_bus_sdaIn;
  assign sdaAtResetCaptured = 1'b0;
  assign attention = io_bus_sdaIn;
  assign scl = (io_sclMode ? clockGate_clk_out : (io_bus_sclIn && (! clockGate_clk_out)));
  assign sdaEdge_rise = ((! i2c_maj3_X_regNext) && maj3_X);
  assign sdaEdge_fall = (i2c_maj3_X_regNext && (! maj3_X));
  assign sdaEdge_toggle = (i2c_maj3_X_regNext != maj3_X);
  assign sclEdge_rise = ((! scl_regNext) && scl);
  assign sclEdge_fall = (scl_regNext && (! scl));
  assign sclEdge_toggle = (scl_regNext != scl);
  assign isStart = (sclSignalNext && sdaEdge_fall);
  assign isStop = (sclSignalNext && sdaEdge_rise);
  assign shifterNow = {shifter[6 : 0],sda};
  assign io_data8rxNow = shifterNow;
  always @(*) begin
    fsm_wantExit = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
        if(sclSignalNext) begin
          if(!io_canSend) begin
            fsm_wantExit = 1'b1;
          end
        end
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    fsm_wantStart = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
        fsm_wantStart = 1'b1;
      end
    endcase
  end

  assign fsm_wantKill = 1'b0;
  always @(*) begin
    fsm_stateNext = fsm_stateReg;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
        fsm_stateNext = fsm_enumDef_HUNT;
      end
      fsm_enumDef_HUNT : begin
        if(isStart) begin
          fsm_stateNext = fsm_enumDef_RECV;
        end
      end
      fsm_enumDef_RECV : begin
        if(scl) begin
          if(when_I2CBertTop_l471) begin
            fsm_stateNext = fsm_enumDef_ACKNACK;
            if(io_canRecv) begin
              fsm_stateNext = fsm_enumDef_ACK;
            end else begin
              fsm_stateNext = fsm_enumDef_NACK;
            end
          end
        end
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l500) begin
          if(scl) begin
            if(io_canSend) begin
              fsm_stateNext = fsm_enumDef_SEND;
            end else begin
              if(io_canRecv) begin
                fsm_stateNext = fsm_enumDef_RECV;
              end else begin
                fsm_stateNext = fsm_enumDef_RESET;
              end
            end
          end
        end
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
        if(scl) begin
          if(when_I2CBertTop_l489) begin
            fsm_stateNext = fsm_enumDef_PRECHECK;
          end
        end
      end
      fsm_enumDef_PRECHECK : begin
        if(when_I2CBertTop_l518) begin
          fsm_stateNext = fsm_enumDef_CHECK;
        end
      end
      fsm_enumDef_CHECK : begin
        if(sclSignalNext) begin
          if(io_canSend) begin
            fsm_stateNext = fsm_enumDef_SEND;
          end else begin
            fsm_stateNext = fsm_enumDef_BOOT;
          end
        end
      end
      default : begin
      end
    endcase
    if(isStop) begin
      fsm_stateNext = fsm_enumDef_RESET;
    end
    if(io_timeoutError) begin
      fsm_stateNext = fsm_enumDef_RESET;
    end
    if(fsm_wantStart) begin
      fsm_stateNext = fsm_enumDef_RESET;
    end
    if(fsm_wantKill) begin
      fsm_stateNext = fsm_enumDef_BOOT;
    end
  end

  assign when_I2CBertTop_l471 = (fsm_bitCount == 3'b111);
  assign when_I2CBertTop_l500 = (! sclSignalNext);
  assign when_I2CBertTop_l489 = (fsm_bitCount == 3'b111);
  assign when_I2CBertTop_l518 = (! sclSignalNext);
  always @(posedge clk) begin
    history_1 <= history_0;
    history_2 <= history_1;
    sclSignalNext <= io_bus_sclIn;
    i2c_maj3_X_regNext <= maj3_X;
    scl_regNext <= scl;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
        if(isStart) begin
          fsm_bitCount <= 3'b000;
        end
      end
      fsm_enumDef_RECV : begin
        if(scl) begin
          shifter <= shifterNow;
          if(!when_I2CBertTop_l471) begin
            fsm_bitCount <= (fsm_bitCount + 3'b001);
          end
        end
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l500) begin
          if(scl) begin
            fsm_bitCount <= 3'b000;
          end
        end
      end
      fsm_enumDef_ACK : begin
      end
      fsm_enumDef_NACK : begin
      end
      fsm_enumDef_SEND : begin
        if(scl) begin
          shifter <= {shifter[6 : 0],shifter[7]};
          if(!when_I2CBertTop_l489) begin
            fsm_bitCount <= (fsm_bitCount + 3'b001);
          end
        end
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      default : begin
      end
    endcase
  end

  always @(posedge clk) begin
    if(!rst_n) begin
      fsm_stateReg <= fsm_enumDef_BOOT;
    end else begin
      fsm_stateReg <= fsm_stateNext;
    end
  end


endmodule

module Timer (
  output              io_sclTick,
  output              io_timeoutError,
  input               io_timerRun,
  input               io_timerLoad,
  output              io_canPowerOnReset,
  output              io_canStart,
  input               io_div12active,
  input      [11:0]   io_div12,
  input               rst_n,
  input               clk
);

  reg        [11:0]   endstop;
  wire                when_I2CBertTop_l306;
  reg        [11:0]   ticker_count;
  reg                 ticker_sclTick;
  reg                 ticker_timeoutError;
  reg                 ticker_canStart;
  reg                 ticker_canPowerOnReset;
  wire                ticker_reset;
  reg        [2:0]    ticker_tickState;
  wire                when_I2CBertTop_l331;
  wire                when_I2CBertTop_l337;
  wire                when_I2CBertTop_l340;
  wire                when_I2CBertTop_l343;

  assign when_I2CBertTop_l306 = (! rst_n);
  always @(*) begin
    ticker_sclTick = 1'b0;
    if(when_I2CBertTop_l331) begin
      ticker_sclTick = 1'b1;
    end
  end

  always @(*) begin
    ticker_timeoutError = 1'b0;
    if(when_I2CBertTop_l340) begin
      ticker_timeoutError = 1'b1;
    end
  end

  always @(*) begin
    ticker_canStart = 1'b0;
    if(when_I2CBertTop_l337) begin
      ticker_canStart = 1'b1;
    end
  end

  always @(*) begin
    ticker_canPowerOnReset = 1'b0;
    if(when_I2CBertTop_l343) begin
      ticker_canPowerOnReset = 1'b1;
    end
  end

  assign ticker_reset = (! io_timerRun);
  assign when_I2CBertTop_l331 = (ticker_tickState == 3'b101);
  assign when_I2CBertTop_l337 = (ticker_count == 12'h012);
  assign when_I2CBertTop_l340 = (ticker_count == 12'h03c);
  assign when_I2CBertTop_l343 = (ticker_count == 12'h004);
  assign io_timeoutError = ticker_timeoutError;
  assign io_sclTick = ticker_sclTick;
  assign io_canStart = ticker_canStart;
  assign io_canPowerOnReset = ticker_canPowerOnReset;
  always @(posedge clk) begin
    if(when_I2CBertTop_l306) begin
      if(io_div12active) begin
        endstop <= io_div12;
      end else begin
        endstop <= 12'h005;
      end
    end
    if(io_timerLoad) begin
      endstop <= ticker_count;
    end
  end

  always @(posedge clk) begin
    if(!rst_n) begin
      ticker_count <= 12'h000;
      ticker_tickState <= 3'b000;
    end else begin
      if(when_I2CBertTop_l331) begin
        ticker_tickState <= 3'b000;
      end else begin
        ticker_tickState <= (ticker_tickState + 3'b001);
      end
      if(ticker_reset) begin
        ticker_count <= 12'h000;
        ticker_tickState <= 3'b010;
      end else begin
        ticker_count <= (ticker_count + 12'h001);
      end
    end
  end


endmodule

module ALU (
  output     [7:0]    io_acc,
  input      [7:0]    io_opand,
  input      [1:0]    io_op,
  input               io_reset,
  input               io_en,
  input               clk,
  input               rst_n
);

  reg        [7:0]    acc;

  assign io_acc = acc;
  always @(posedge clk) begin
    if(!rst_n) begin
      acc <= 8'h00;
    end else begin
      if(io_reset) begin
        acc <= 8'h00;
      end else begin
        if(io_en) begin
          case(io_op)
            2'b00 : begin
              acc <= (acc & io_opand);
            end
            2'b01 : begin
              acc <= (acc | io_opand);
            end
            2'b10 : begin
              acc <= (acc ^ io_opand);
            end
            default : begin
              acc <= 8'hff;
            end
          endcase
        end
      end
    end
  end


endmodule
