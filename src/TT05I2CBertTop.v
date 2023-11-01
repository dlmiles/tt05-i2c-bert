// Generator : SpinalHDL dev    git head : efcba5fcd17d0cfe48fa0981e8dec6e70234b294
// Component : TT05I2CBertTop

`timescale 1ns/1ps

module TT05I2CBertTop (
  input               ena /* verilator public */ ,
  output reg [7:0]    uo_out /* verilator public */ ,
  input      [7:0]    ui_in /* verilator public */ ,
  output reg [7:0]    uio_out /* verilator public */ ,
  input      [7:0]    uio_in /* verilator public */ ,
  output reg [7:0]    uio_oe /* verilator public */ ,
  input               debug_SCL_ie /* verilator public */ ,
  output              debug_SCL_od /* verilator public */ ,
  output              debug_SCL_pp /* verilator public */ ,
  output              debug_SCL_og /* verilator public */ ,
  output              debug_SCL_pg /* verilator public */ ,
  output              debug_SCL_os /* verilator public */ ,
  output              debug_SCL_ps /* verilator public */ ,
  input               debug_SDA_ie /* verilator public */ ,
  output              debug_SDA_od /* verilator public */ ,
  output              debug_SDA_pp /* verilator public */ ,
  output              debug_SDA_og /* verilator public */ ,
  output              debug_SDA_pg /* verilator public */ ,
  output              debug_SDA_os /* verilator public */ ,
  output              debug_SDA_ps /* verilator public */ ,
  input               simulation_z /* verilator public */ ,
  input      [31:0]   latched /* verilator public */ ,
  input               rst_n,
  input               clk
);

  wire                timer_1_io_timerRun;
  wire                i2c_io_bus_sclIn;
  wire                i2c_io_bus_sdaIn;
  wire                powerOnSense_D;
  wire                powerOnSense_GATE;
  wire                timer_1_io_sclTick;
  wire                timer_1_io_timeoutError;
  wire                timer_1_io_canPowerOnReset;
  wire                timer_1_io_canStart;
  wire       [11:0]   timer_1_io_timerEndstop;
  wire                i2c_io_bus_sclOut;
  wire                i2c_io_bus_sclOe;
  wire                i2c_io_bus_sdaOut;
  wire                i2c_io_bus_sdaOe;
  wire                i2c_io_sdaSignal;
  wire                i2c_io_timerRun;
  wire                i2c_io_timerLoad;
  wire                i2c_io_wantReset;
  wire                i2c_io_wantStart;
  wire                i2c_io_wantTick;
  wire                i2c_io_nackRxStrobe;
  wire       [7:0]    i2c_io_data8rx;
  wire       [7:0]    i2c_io_data8rxNow;
  wire                myState_1_io_canSend;
  wire                myState_1_io_canRecv;
  wire                myState_1_io_canNack;
  wire                myState_1_io_canStretch;
  wire       [7:0]    myState_1_io_data8tx;
  wire                myState_1_io_timerLoadH;
  wire                myState_1_io_timerLoadL;
  wire                powerOnSenseCaptured_Q;
  wire                powerOnSense_Q;
  wire                _zz_debug_SCL_od;
  wire                _zz_debug_SCL_od_1;
  wire                _zz_debug_SCL_od_2;
  wire                _zz_debug_SDA_od;
  wire                _zz_debug_SDA_od_1;
  wire                _zz_debug_SDA_od_2;
  wire                pushPullMode;
  wire                sclMode;
  wire                div12active;
  wire       [11:0]   div12;

  Timer timer_1 (
    .io_sclTick         (timer_1_io_sclTick           ), //o
    .io_timeoutError    (timer_1_io_timeoutError      ), //o
    .io_timerRun        (timer_1_io_timerRun          ), //i
    .io_timerLoad       (i2c_io_timerLoad             ), //i
    .io_canPowerOnReset (timer_1_io_canPowerOnReset   ), //o
    .io_canStart        (timer_1_io_canStart          ), //o
    .io_div12active     (div12active                  ), //i
    .io_div12           (div12[11:0]                  ), //i
    .io_timerLoadH      (myState_1_io_timerLoadH      ), //i
    .io_timerLoadL      (myState_1_io_timerLoadL      ), //i
    .io_timerData       (i2c_io_data8rxNow[7:0]       ), //i
    .io_timerEndstop    (timer_1_io_timerEndstop[11:0]), //o
    .rst_n              (rst_n                        ), //i
    .clk                (clk                          )  //i
  );
  MyI2C i2c (
    .io_bus_sclOut   (i2c_io_bus_sclOut        ), //o
    .io_bus_sclIn    (i2c_io_bus_sclIn         ), //i
    .io_bus_sclOe    (i2c_io_bus_sclOe         ), //o
    .io_bus_sdaOut   (i2c_io_bus_sdaOut        ), //o
    .io_bus_sdaIn    (i2c_io_bus_sdaIn         ), //i
    .io_bus_sdaOe    (i2c_io_bus_sdaOe         ), //o
    .io_sdaSignal    (i2c_io_sdaSignal         ), //o
    .io_sclTick      (timer_1_io_sclTick       ), //i
    .io_timeoutError (timer_1_io_timeoutError  ), //i
    .io_timerRun     (i2c_io_timerRun          ), //o
    .io_timerLoad    (i2c_io_timerLoad         ), //o
    .io_canRecv      (myState_1_io_canRecv     ), //i
    .io_canSend      (myState_1_io_canSend     ), //i
    .io_canNack      (myState_1_io_canNack     ), //i
    .io_canStretch   (myState_1_io_canStretch  ), //i
    .io_wantReset    (i2c_io_wantReset         ), //o
    .io_wantStart    (i2c_io_wantStart         ), //o
    .io_wantTick     (i2c_io_wantTick          ), //o
    .io_nackRxStrobe (i2c_io_nackRxStrobe      ), //o
    .io_data8rx      (i2c_io_data8rx[7:0]      ), //o
    .io_data8rxNow   (i2c_io_data8rxNow[7:0]   ), //o
    .io_data8tx      (myState_1_io_data8tx[7:0]), //i
    .io_sclMode      (sclMode                  ), //i
    .io_pushPullMode (pushPullMode             ), //i
    .rst_n           (rst_n                    ), //i
    .clk             (clk                      )  //i
  );
  MyState myState_1 (
    .io_wantReset    (i2c_io_wantReset             ), //i
    .io_wantStart    (i2c_io_wantStart             ), //i
    .io_wantTick     (i2c_io_wantTick              ), //i
    .io_nackRxStrobe (i2c_io_nackRxStrobe          ), //i
    .io_canSend      (myState_1_io_canSend         ), //o
    .io_canRecv      (myState_1_io_canRecv         ), //o
    .io_canNack      (myState_1_io_canNack         ), //o
    .io_canStretch   (myState_1_io_canStretch      ), //o
    .io_datain8rx    (i2c_io_data8rx[7:0]          ), //i
    .io_datain8rxNow (i2c_io_data8rxNow[7:0]       ), //i
    .io_data8tx      (myState_1_io_data8tx[7:0]    ), //o
    .io_latched      (latched[31:0]                ), //i
    .io_timerLoadH   (myState_1_io_timerLoadH      ), //o
    .io_timerLoadL   (myState_1_io_timerLoadL      ), //o
    .io_timerEndstop (timer_1_io_timerEndstop[11:0]), //i
    .io_cfgSclMode   (sclMode                      ), //i
    .io_cfgPushPull  (pushPullMode                 ), //i
    .clk             (clk                          ), //i
    .rst_n           (rst_n                        )  //i
  );
  (* keep , syn_keep *) sky130_fd_sc_hd__dlrtp powerOnSenseCaptured (
    .D       (1'b1                      ), //i
    .GATE    (timer_1_io_canPowerOnReset), //i
    .RESET_B (rst_n                     ), //i
    .Q       (powerOnSenseCaptured_Q    )  //o
  );
  (* keep , syn_keep *) sky130_fd_sc_hd__dlrtp powerOnSense (
    .D       (powerOnSense_D   ), //i
    .GATE    (powerOnSense_GATE), //i
    .RESET_B (rst_n            ), //i
    .Q       (powerOnSense_Q   )  //o
  );
  always @(*) begin
    uo_out = 8'bxxxxxxxx;
    uo_out[7] = powerOnSense_Q;
  end

  always @(*) begin
    uio_out = 8'bxxxxxxxx;
    uio_out[3] = i2c_io_bus_sdaOut;
    uio_out[2] = i2c_io_bus_sclOut;
  end

  always @(*) begin
    uio_oe = 8'h00;
    uio_oe[3] = i2c_io_bus_sdaOe;
    uio_oe[2] = i2c_io_bus_sclOe;
  end

  assign _zz_debug_SCL_od = uio_out[2];
  assign _zz_debug_SCL_od_1 = uio_oe[2];
  assign _zz_debug_SCL_od_2 = uio_in[2];
  assign debug_SCL_od = (_zz_debug_SCL_od_1 ? _zz_debug_SCL_od : ((debug_SCL_ie && (! _zz_debug_SCL_od_2)) ? _zz_debug_SCL_od_2 : simulation_z));
  assign debug_SCL_og = ((_zz_debug_SCL_od_1 && _zz_debug_SCL_od) ? 1'b0 : ((debug_SCL_ie && _zz_debug_SCL_od_2) ? 1'b0 : ((_zz_debug_SCL_od_1 && (! _zz_debug_SCL_od)) ? 1'b1 : ((debug_SCL_ie && (! _zz_debug_SCL_od_2)) ? 1'b1 : 1'b1))));
  assign debug_SCL_os = ((_zz_debug_SCL_od_1 && debug_SDA_ie) ? 1'bx : (_zz_debug_SCL_od_1 ? _zz_debug_SCL_od : (debug_SDA_ie ? _zz_debug_SCL_od_2 : 1'b1)));
  assign debug_SCL_pp = (_zz_debug_SCL_od_1 ? _zz_debug_SCL_od : (debug_SCL_ie ? _zz_debug_SCL_od_2 : simulation_z));
  assign debug_SCL_pg = ((_zz_debug_SCL_od_1 && debug_SCL_ie) ? 1'b0 : (_zz_debug_SCL_od_1 ? 1'b1 : (debug_SCL_ie ? 1'b1 : (((! debug_SCL_ie) && (! _zz_debug_SCL_od_2)) ? 1'b1 : 1'b1))));
  assign debug_SCL_ps = ((_zz_debug_SCL_od_1 && debug_SCL_ie) ? 1'bx : (_zz_debug_SCL_od_1 ? _zz_debug_SCL_od : (debug_SCL_ie ? _zz_debug_SCL_od_2 : simulation_z)));
  assign _zz_debug_SDA_od = uio_out[3];
  assign _zz_debug_SDA_od_1 = uio_oe[3];
  assign _zz_debug_SDA_od_2 = uio_in[3];
  assign debug_SDA_od = (_zz_debug_SDA_od_1 ? _zz_debug_SDA_od : ((debug_SDA_ie && (! _zz_debug_SDA_od_2)) ? _zz_debug_SDA_od_2 : simulation_z));
  assign debug_SDA_og = ((_zz_debug_SDA_od_1 && _zz_debug_SDA_od) ? 1'b0 : ((debug_SDA_ie && _zz_debug_SDA_od_2) ? 1'b0 : ((_zz_debug_SDA_od_1 && (! _zz_debug_SDA_od)) ? 1'b1 : ((debug_SDA_ie && (! _zz_debug_SDA_od_2)) ? 1'b1 : 1'b1))));
  assign debug_SDA_os = ((_zz_debug_SDA_od_1 && debug_SDA_ie) ? 1'bx : (_zz_debug_SDA_od_1 ? _zz_debug_SDA_od : (debug_SDA_ie ? _zz_debug_SDA_od_2 : 1'b1)));
  assign debug_SDA_pp = (_zz_debug_SDA_od_1 ? _zz_debug_SDA_od : (debug_SDA_ie ? _zz_debug_SDA_od_2 : simulation_z));
  assign debug_SDA_pg = ((_zz_debug_SDA_od_1 && debug_SDA_ie) ? 1'b0 : (_zz_debug_SDA_od_1 ? 1'b1 : (debug_SDA_ie ? 1'b1 : (((! debug_SDA_ie) && (! _zz_debug_SDA_od_2)) ? 1'b1 : 1'b1))));
  assign debug_SDA_ps = ((_zz_debug_SDA_od_1 && debug_SDA_ie) ? 1'bx : (_zz_debug_SDA_od_1 ? _zz_debug_SDA_od : (debug_SDA_ie ? _zz_debug_SDA_od_2 : simulation_z)));
  assign pushPullMode = latched[2];
  assign sclMode = latched[1];
  assign div12active = latched[3];
  assign div12 = latched[15 : 4];
  assign i2c_io_bus_sdaIn = uio_in[3];
  assign i2c_io_bus_sclIn = uio_in[2];
  assign timer_1_io_timerRun = ((! powerOnSenseCaptured_Q) || i2c_io_timerRun);
  assign powerOnSense_D = (! i2c_io_sdaSignal);
  assign powerOnSense_GATE = ((! powerOnSenseCaptured_Q) && timer_1_io_canPowerOnReset);

endmodule

module MyState (
  input               io_wantReset,
  input               io_wantStart,
  input               io_wantTick,
  input               io_nackRxStrobe,
  output reg          io_canSend,
  output reg          io_canRecv,
  output reg          io_canNack,
  output reg          io_canStretch,
  input      [7:0]    io_datain8rx,
  input      [7:0]    io_datain8rxNow,
  output reg [7:0]    io_data8tx,
  input      [31:0]   io_latched,
  output reg          io_timerLoadH,
  output reg          io_timerLoadL,
  input      [11:0]   io_timerEndstop,
  input               io_cfgSclMode,
  input               io_cfgPushPull,
  input               clk,
  input               rst_n
);
  localparam fsmPhase_enumDef_BOOT = 3'd0;
  localparam fsmPhase_enumDef_RESET = 3'd1;
  localparam fsmPhase_enumDef_CONTROL = 3'd2;
  localparam fsmPhase_enumDef_RECV = 3'd3;
  localparam fsmPhase_enumDef_SEND = 3'd4;
  localparam fsmPhase_enumDef_STRETCH = 3'd5;

  wire       [1:0]    alu_1_io_op;
  reg        [0:0]    alu_1_io_op2;
  reg                 alu_1_io_reset;
  reg                 alu_1_io_en;
  wire       [7:0]    alu_1_io_acc;
  wire       [2:0]    _zz_io_op2;
  wire       [7:0]    _zz__zz_io_data8tx;
  wire       [3:0]    _zz__zz_io_data8tx_1;
  reg                 readWriteBit;
  reg        [6:0]    cmd7;
  reg        [7:0]    cmd8;
  reg        [7:0]    len8;
  wire       [11:0]   len12;
  reg        [11:0]   counter;
  reg                 fsmPhase_wantExit;
  reg                 fsmPhase_wantStart;
  wire                fsmPhase_wantKill;
  reg        [2:0]    fsmPhase_stateReg;
  reg        [2:0]    fsmPhase_stateNext;
  wire                when_I2CBertTop_l318;
  wire                when_I2CBertTop_l386;
  wire                when_I2CBertTop_l388;
  wire                when_I2CBertTop_l414;
  wire                when_I2CBertTop_l430;
  wire       [0:0]    switch_Misc_l226;
  reg        [7:0]    _zz_io_data8tx;
  reg        [7:0]    _zz_io_data8tx_1;
  wire       [1:0]    switch_Misc_l226_1;
  reg        [7:0]    _zz_io_data8tx_2;
  wire                when_I2CBertTop_l475;
  wire                when_I2CBertTop_l491;
  wire                when_I2CBertTop_l497;
  wire                when_I2CBertTop_l511;
  wire                when_I2CBertTop_l512;
  `ifndef SYNTHESIS
  reg [55:0] fsmPhase_stateReg_string;
  reg [55:0] fsmPhase_stateNext_string;
  `endif


  assign _zz_io_op2 = 3'b100;
  assign _zz__zz_io_data8tx_1 = io_timerEndstop[11 : 8];
  assign _zz__zz_io_data8tx = {4'd0, _zz__zz_io_data8tx_1};
  ALU alu_1 (
    .io_acc   (alu_1_io_acc[7:0]   ), //o
    .io_opand (io_datain8rxNow[7:0]), //i
    .io_op    (alu_1_io_op[1:0]    ), //i
    .io_op2   (alu_1_io_op2        ), //i
    .io_reset (alu_1_io_reset      ), //i
    .io_en    (alu_1_io_en         ), //i
    .clk      (clk                 ), //i
    .rst_n    (rst_n               )  //i
  );
  `ifndef SYNTHESIS
  always @(*) begin
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_BOOT : fsmPhase_stateReg_string = "BOOT   ";
      fsmPhase_enumDef_RESET : fsmPhase_stateReg_string = "RESET  ";
      fsmPhase_enumDef_CONTROL : fsmPhase_stateReg_string = "CONTROL";
      fsmPhase_enumDef_RECV : fsmPhase_stateReg_string = "RECV   ";
      fsmPhase_enumDef_SEND : fsmPhase_stateReg_string = "SEND   ";
      fsmPhase_enumDef_STRETCH : fsmPhase_stateReg_string = "STRETCH";
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
      fsmPhase_enumDef_STRETCH : fsmPhase_stateNext_string = "STRETCH";
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
      fsmPhase_enumDef_STRETCH : begin
        io_canSend = (readWriteBit == 1'b1);
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
      fsmPhase_enumDef_STRETCH : begin
        io_canRecv = (readWriteBit == 1'b0);
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_canNack = 1'b1;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
        io_canNack = readWriteBit;
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_canStretch = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
        io_canStretch = 1'b1;
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_data8tx = 8'bxxxxxxxx;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
        if(when_I2CBertTop_l430) begin
          casez(cmd8)
            8'b11111001 : begin
              io_data8tx = alu_1_io_acc;
            end
            8'b11100001 : begin
              io_data8tx = _zz_io_data8tx;
            end
            8'b11000001 : begin
              io_data8tx = _zz_io_data8tx_1;
            end
            8'b11010001 : begin
              io_data8tx = len8;
            end
            8'b11111101 : begin
              io_data8tx = alu_1_io_acc;
            end
            8'b11110001 : begin
              io_data8tx = _zz_io_data8tx_2;
            end
            8'b??????1? : begin
              io_data8tx = alu_1_io_acc;
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_STRETCH : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_timerLoadH = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          casez(cmd8)
            8'b11100000 : begin
              if(!when_I2CBertTop_l386) begin
                if(when_I2CBertTop_l388) begin
                  io_timerLoadH = 1'b1;
                end
              end
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_timerLoadL = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          casez(cmd8)
            8'b11100000 : begin
              if(when_I2CBertTop_l386) begin
                io_timerLoadL = 1'b1;
              end
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
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
          if(!when_I2CBertTop_l318) begin
            casez(io_datain8rxNow)
              8'b11110000 : begin
                alu_1_io_reset = 1'b1;
              end
              8'b1000000? : begin
              end
              8'b1000010? : begin
              end
              8'b11001000 : begin
              end
              8'b11001100 : begin
              end
              8'b??????1?, 8'b11111000, 8'b11100000, 8'b11000000, 8'b11010000, 8'b11111100, 8'b00000000 : begin
              end
              default : begin
              end
            endcase
          end
        end
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
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
          casez(cmd8)
            8'b11111000 : begin
              alu_1_io_en = 1'b1;
            end
            8'b??????1? : begin
              alu_1_io_en = 1'b1;
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
      end
      default : begin
      end
    endcase
  end

  assign alu_1_io_op = cmd8[3 : 2];
  always @(*) begin
    alu_1_io_op2 = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          casez(cmd8)
            8'b11111000 : begin
              alu_1_io_op2 = _zz_io_op2[2];
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    fsmPhase_wantExit = 1'b0;
    case(fsmPhase_stateReg)
      fsmPhase_enumDef_RESET : begin
        if(io_wantReset) begin
          fsmPhase_wantExit = 1'b1;
        end
      end
      fsmPhase_enumDef_CONTROL : begin
      end
      fsmPhase_enumDef_RECV : begin
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
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
        if(io_wantReset) begin
          fsmPhase_stateNext = fsmPhase_enumDef_BOOT;
        end
      end
      fsmPhase_enumDef_CONTROL : begin
        if(io_wantTick) begin
          if(when_I2CBertTop_l318) begin
            casez(io_datain8rxNow)
              8'b1000000?, 8'b00000001 : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
              8'b1000010? : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
              8'b??????1?, 8'b11111001, 8'b11100001, 8'b11000001, 8'b11010001, 8'b11110001, 8'b11111101 : begin
                fsmPhase_stateNext = fsmPhase_enumDef_SEND;
              end
              default : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
            endcase
          end else begin
            casez(io_datain8rxNow)
              8'b11110000 : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
              8'b1000000? : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
              8'b1000010? : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
              8'b11001000 : begin
                fsmPhase_stateNext = fsmPhase_enumDef_STRETCH;
              end
              8'b11001100 : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
              8'b??????1?, 8'b11111000, 8'b11100000, 8'b11000000, 8'b11010000, 8'b11111100, 8'b00000000 : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RECV;
              end
              default : begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
            endcase
          end
        end
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          casez(cmd8)
            8'b11010000 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b11100000 : begin
              if(!when_I2CBertTop_l386) begin
                if(when_I2CBertTop_l388) begin
                  fsmPhase_stateNext = fsmPhase_enumDef_RESET;
                end
              end
            end
            8'b11111000 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b00000000 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b11000000 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b??????1? : begin
              if(when_I2CBertTop_l414) begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_SEND : begin
        if(io_nackRxStrobe) begin
          fsmPhase_stateNext = fsmPhase_enumDef_RESET;
        end
        if(io_wantTick) begin
          casez(cmd8)
            8'b11111001 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b11100001 : begin
              if(when_I2CBertTop_l475) begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
            end
            8'b11000001 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b11010001 : begin
              fsmPhase_stateNext = fsmPhase_enumDef_RESET;
            end
            8'b11110001 : begin
              if(when_I2CBertTop_l491) begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
            end
            8'b??????1? : begin
              if(when_I2CBertTop_l497) begin
                fsmPhase_stateNext = fsmPhase_enumDef_RESET;
              end
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_STRETCH : begin
        if(io_wantTick) begin
          if(when_I2CBertTop_l511) begin
            if(when_I2CBertTop_l512) begin
              fsmPhase_stateNext = fsmPhase_enumDef_SEND;
            end else begin
              fsmPhase_stateNext = fsmPhase_enumDef_RECV;
            end
          end
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

  assign when_I2CBertTop_l318 = (io_datain8rxNow[0] == 1'b1);
  assign when_I2CBertTop_l386 = (counter == 12'h000);
  assign when_I2CBertTop_l388 = (counter == 12'h001);
  assign when_I2CBertTop_l414 = (counter == len12);
  assign when_I2CBertTop_l430 = 1'b1;
  assign switch_Misc_l226 = counter[0 : 0];
  always @(*) begin
    case(switch_Misc_l226)
      1'b0 : begin
        _zz_io_data8tx = io_timerEndstop[7 : 0];
      end
      default : begin
        _zz_io_data8tx = _zz__zz_io_data8tx;
      end
    endcase
  end

  always @(*) begin
    _zz_io_data8tx_1[7 : 2] = 6'h00;
    _zz_io_data8tx_1[1] = io_cfgSclMode;
    _zz_io_data8tx_1[0] = io_cfgPushPull;
  end

  assign switch_Misc_l226_1 = counter[1 : 0];
  always @(*) begin
    case(switch_Misc_l226_1)
      2'b00 : begin
        _zz_io_data8tx_2 = io_latched[7 : 0];
      end
      2'b01 : begin
        _zz_io_data8tx_2 = io_latched[15 : 8];
      end
      2'b10 : begin
        _zz_io_data8tx_2 = io_latched[23 : 16];
      end
      default : begin
        _zz_io_data8tx_2 = io_latched[31 : 24];
      end
    endcase
  end

  assign when_I2CBertTop_l475 = (counter == 12'h001);
  assign when_I2CBertTop_l491 = (counter == 12'h003);
  assign when_I2CBertTop_l497 = (counter == len12);
  assign when_I2CBertTop_l511 = (counter == len12);
  assign when_I2CBertTop_l512 = (readWriteBit == 1'b1);
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
            if(when_I2CBertTop_l318) begin
              casez(io_datain8rxNow)
                8'b1000000?, 8'b00000001 : begin
                end
                8'b1000010? : begin
                end
                8'b??????1?, 8'b11111001, 8'b11100001, 8'b11000001, 8'b11010001, 8'b11110001, 8'b11111101 : begin
                  counter <= 12'h000;
                end
                default : begin
                end
              endcase
            end else begin
              casez(io_datain8rxNow)
                8'b11110000 : begin
                  len8 <= 8'h00;
                end
                8'b1000000? : begin
                end
                8'b1000010? : begin
                end
                8'b11001000 : begin
                end
                8'b11001100 : begin
                end
                8'b??????1?, 8'b11111000, 8'b11100000, 8'b11000000, 8'b11010000, 8'b11111100, 8'b00000000 : begin
                  counter <= 12'h000;
                end
                default : begin
                end
              endcase
            end
          end
        end
        fsmPhase_enumDef_RECV : begin
          if(io_wantTick) begin
            casez(cmd8)
              8'b11010000 : begin
                len8 <= io_datain8rxNow;
              end
              default : begin
              end
            endcase
            counter <= (counter + 12'h001);
          end
        end
        fsmPhase_enumDef_SEND : begin
          if(io_wantTick) begin
            counter <= (counter + 12'h001);
          end
        end
        fsmPhase_enumDef_STRETCH : begin
          if(io_wantTick) begin
            if(!when_I2CBertTop_l511) begin
              counter <= (counter + 12'h001);
            end
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
          cmd7 <= io_datain8rxNow[7 : 1];
          if(when_I2CBertTop_l318) begin
            casez(io_datain8rxNow)
              8'b1000000?, 8'b00000001 : begin
                readWriteBit <= 1'b0;
              end
              8'b1000010? : begin
                readWriteBit <= 1'b1;
              end
              8'b??????1?, 8'b11111001, 8'b11100001, 8'b11000001, 8'b11010001, 8'b11110001, 8'b11111101 : begin
                readWriteBit <= io_datain8rxNow[0];
              end
              default : begin
                readWriteBit <= 1'b1;
              end
            endcase
          end else begin
            casez(io_datain8rxNow)
              8'b11110000 : begin
                readWriteBit <= 1'b0;
              end
              8'b1000000? : begin
                readWriteBit <= 1'b0;
              end
              8'b1000010? : begin
                readWriteBit <= 1'b1;
              end
              8'b11001000 : begin
                readWriteBit <= 1'b0;
              end
              8'b11001100 : begin
                readWriteBit <= 1'b1;
              end
              8'b??????1?, 8'b11111000, 8'b11100000, 8'b11000000, 8'b11010000, 8'b11111100, 8'b00000000 : begin
                readWriteBit <= io_datain8rxNow[0];
              end
              default : begin
                readWriteBit <= 1'b1;
              end
            endcase
          end
        end
      end
      fsmPhase_enumDef_RECV : begin
        if(io_wantTick) begin
          casez(cmd8)
            8'b11010000 : begin
              readWriteBit <= 1'b0;
            end
            8'b11100000 : begin
              if(!when_I2CBertTop_l386) begin
                if(when_I2CBertTop_l388) begin
                  readWriteBit <= 1'b0;
                end
              end
            end
            8'b11111000 : begin
              readWriteBit <= 1'b0;
            end
            8'b00000000 : begin
              readWriteBit <= ((io_datain8rxNow == (~ len8)) ? 1'b0 : 1'b1);
            end
            8'b11000000 : begin
              readWriteBit <= 1'b1;
            end
            8'b??????1? : begin
              if(when_I2CBertTop_l414) begin
                readWriteBit <= 1'b0;
              end
            end
            default : begin
            end
          endcase
        end
      end
      fsmPhase_enumDef_SEND : begin
      end
      fsmPhase_enumDef_STRETCH : begin
      end
      default : begin
      end
    endcase
  end


endmodule

module MyI2C (
  output reg          io_bus_sclOut,
  input               io_bus_sclIn,
  output              io_bus_sclOe,
  output reg          io_bus_sdaOut,
  input               io_bus_sdaIn,
  output              io_bus_sdaOe,
  output              io_sdaSignal,
  input               io_sclTick,
  input               io_timeoutError,
  output reg          io_timerRun,
  output reg          io_timerLoad,
  input               io_canRecv,
  input               io_canSend,
  input               io_canNack,
  input               io_canStretch,
  output reg          io_wantReset,
  output reg          io_wantStart,
  output reg          io_wantTick,
  output reg          io_nackRxStrobe,
  output reg [7:0]    io_data8rx,
  output     [7:0]    io_data8rxNow,
  input      [7:0]    io_data8tx,
  input               io_sclMode,
  input               io_pushPullMode,
  input               rst_n,
  input               clk
);
  localparam fsm_enumDef_BOOT = 4'd0;
  localparam fsm_enumDef_RESET = 4'd1;
  localparam fsm_enumDef_HUNT = 4'd2;
  localparam fsm_enumDef_RECV = 4'd3;
  localparam fsm_enumDef_ACKNACK = 4'd4;
  localparam fsm_enumDef_SEND = 4'd5;
  localparam fsm_enumDef_PRECHECK = 4'd6;
  localparam fsm_enumDef_CHECK = 4'd7;
  localparam fsm_enumDef_POSTCHECK = 4'd8;
  localparam fsm_enumDef_AUTOBAUD = 4'd9;

  wire                clockGate_reset;
  wire                sdaMaj3_X;
  wire                sclMaj3_X;
  wire                clockGate_clk_out;
  reg                 sdaTx;
  reg                 sclTx;
  wire                when_Utils_l1149;
  wire                sdaHistory_0;
  reg                 sdaHistory_1;
  reg                 sdaHistory_2;
  wire                sda;
  wire                when_Utils_l1149_1;
  wire                sclHistory_0;
  reg                 sclHistory_1;
  reg                 sclHistory_2;
  wire                scl;
  wire                sdaEdge_rise;
  wire                sdaEdge_fall;
  wire                sdaEdge_toggle;
  reg                 sda_regNext;
  wire                sclEdge_rise;
  wire                sclEdge_fall;
  wire                sclEdge_toggle;
  reg                 scl_regNext;
  wire                isStart;
  wire                isStop;
  reg        [7:0]    shifter;
  wire       [7:0]    shifterNow;
  wire                fsm_wantExit;
  reg                 fsm_wantStart;
  wire                fsm_wantKill;
  reg        [2:0]    fsm_bitCount;
  reg        [3:0]    fsm_stateReg;
  reg        [3:0]    fsm_stateNext;
  wire                when_I2CBertTop_l750;
  wire                when_I2CBertTop_l775;
  wire                _zz_io_bus_sdaOut;
  wire                when_I2CBertTop_l781;
  wire                when_I2CBertTop_l764;
  wire                when_I2CBertTop_l801;
  wire                when_I2CBertTop_l832;
  wire                when_I2CBertTop_l843;
  `ifndef SYNTHESIS
  reg [71:0] fsm_stateReg_string;
  reg [71:0] fsm_stateNext_string;
  `endif


  (* keep , syn_keep *) sky130_fd_sc_hd__maj3 sdaMaj3 (
    .A (sdaHistory_0), //i
    .B (sdaHistory_1), //i
    .C (sdaHistory_2), //i
    .X (sdaMaj3_X   )  //o
  );
  (* keep , syn_keep *) sky130_fd_sc_hd__maj3 sclMaj3 (
    .A (sclHistory_0), //i
    .B (sclHistory_1), //i
    .C (sclHistory_2), //i
    .X (sclMaj3_X   )  //o
  );
  glitch_free_clock_mux_async_reset clockGate (
    .clk_0   (sclHistory_0     ), //i
    .clk_1   (io_sclTick       ), //i
    .sel     (io_sclMode       ), //i
    .clk_out (clockGate_clk_out), //o
    .reset   (clockGate_reset  )  //i
  );
  `ifndef SYNTHESIS
  always @(*) begin
    case(fsm_stateReg)
      fsm_enumDef_BOOT : fsm_stateReg_string = "BOOT     ";
      fsm_enumDef_RESET : fsm_stateReg_string = "RESET    ";
      fsm_enumDef_HUNT : fsm_stateReg_string = "HUNT     ";
      fsm_enumDef_RECV : fsm_stateReg_string = "RECV     ";
      fsm_enumDef_ACKNACK : fsm_stateReg_string = "ACKNACK  ";
      fsm_enumDef_SEND : fsm_stateReg_string = "SEND     ";
      fsm_enumDef_PRECHECK : fsm_stateReg_string = "PRECHECK ";
      fsm_enumDef_CHECK : fsm_stateReg_string = "CHECK    ";
      fsm_enumDef_POSTCHECK : fsm_stateReg_string = "POSTCHECK";
      fsm_enumDef_AUTOBAUD : fsm_stateReg_string = "AUTOBAUD ";
      default : fsm_stateReg_string = "?????????";
    endcase
  end
  always @(*) begin
    case(fsm_stateNext)
      fsm_enumDef_BOOT : fsm_stateNext_string = "BOOT     ";
      fsm_enumDef_RESET : fsm_stateNext_string = "RESET    ";
      fsm_enumDef_HUNT : fsm_stateNext_string = "HUNT     ";
      fsm_enumDef_RECV : fsm_stateNext_string = "RECV     ";
      fsm_enumDef_ACKNACK : fsm_stateNext_string = "ACKNACK  ";
      fsm_enumDef_SEND : fsm_stateNext_string = "SEND     ";
      fsm_enumDef_PRECHECK : fsm_stateNext_string = "PRECHECK ";
      fsm_enumDef_CHECK : fsm_stateNext_string = "CHECK    ";
      fsm_enumDef_POSTCHECK : fsm_stateNext_string = "POSTCHECK";
      fsm_enumDef_AUTOBAUD : fsm_stateNext_string = "AUTOBAUD ";
      default : fsm_stateNext_string = "?????????";
    endcase
  end
  `endif

  always @(*) begin
    sdaTx = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l775) begin
          sdaTx = 1'b1;
        end
      end
      fsm_enumDef_SEND : begin
        sdaTx = 1'b1;
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    sclTx = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l775) begin
          if(when_I2CBertTop_l781) begin
            sclTx = io_canStretch;
          end
        end
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
      end
      default : begin
      end
    endcase
  end

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
        if(when_I2CBertTop_l775) begin
          io_bus_sdaOut = _zz_io_bus_sdaOut;
        end
      end
      fsm_enumDef_SEND : begin
        io_bus_sdaOut = shifter[7];
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
      end
      default : begin
      end
    endcase
  end

  assign io_bus_sdaOe = (sdaTx && (io_pushPullMode || (! io_bus_sdaOut)));
  always @(*) begin
    io_bus_sclOut = 1'b1;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l775) begin
          if(when_I2CBertTop_l781) begin
            io_bus_sclOut = io_canStretch;
          end
        end
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
      end
      default : begin
      end
    endcase
  end

  assign io_bus_sclOe = (sclTx && (io_pushPullMode || (! io_bus_sclOut)));
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
        if(when_I2CBertTop_l775) begin
          if(!when_I2CBertTop_l781) begin
            if(sclEdge_rise) begin
              io_timerRun = 1'b0;
            end
          end
        end
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
      fsm_enumDef_POSTCHECK : begin
        io_timerRun = 1'b0;
      end
      fsm_enumDef_AUTOBAUD : begin
        io_timerRun = 1'b1;
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_timerLoad = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
        if(sclEdge_rise) begin
          if(when_I2CBertTop_l832) begin
            io_timerLoad = 1'b1;
          end
        end
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
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
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
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
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
        if(sclEdge_rise) begin
          if(when_I2CBertTop_l750) begin
            io_wantTick = 1'b1;
          end
        end
      end
      fsm_enumDef_ACKNACK : begin
      end
      fsm_enumDef_SEND : begin
        if(sclEdge_rise) begin
          if(when_I2CBertTop_l764) begin
            io_wantTick = 1'b1;
          end
        end
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_nackRxStrobe = 1'b0;
    case(fsm_stateReg)
      fsm_enumDef_RESET : begin
      end
      fsm_enumDef_HUNT : begin
      end
      fsm_enumDef_RECV : begin
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l775) begin
          if(!when_I2CBertTop_l781) begin
            if(sclEdge_rise) begin
              io_nackRxStrobe = _zz_io_bus_sdaOut;
            end
          end
        end
      end
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
        if(sclEdge_rise) begin
          io_nackRxStrobe = sda;
        end
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
      end
      default : begin
      end
    endcase
  end

  always @(*) begin
    io_data8rx = 8'bxxxxxxxx;
    io_data8rx = shifter;
  end

  assign when_Utils_l1149 = 1'b1;
  assign sdaHistory_0 = io_bus_sdaIn;
  assign sda = (io_sclMode ? sdaMaj3_X : sdaHistory_0);
  assign io_sdaSignal = sda;
  assign when_Utils_l1149_1 = 1'b1;
  assign sclHistory_0 = io_bus_sclIn;
  assign scl = (io_sclMode ? sclMaj3_X : sclHistory_0);
  assign clockGate_reset = (! rst_n);
  assign sdaEdge_rise = ((! sda_regNext) && sda);
  assign sdaEdge_fall = (sda_regNext && (! sda));
  assign sdaEdge_toggle = (sda_regNext != sda);
  assign sclEdge_rise = ((! scl_regNext) && scl);
  assign sclEdge_fall = (scl_regNext && (! scl));
  assign sclEdge_toggle = (scl_regNext != scl);
  assign isStart = (sclHistory_0 && sdaEdge_fall);
  assign isStop = (sclHistory_0 && sdaEdge_rise);
  assign shifterNow = {shifter[6 : 0],sda};
  assign io_data8rxNow = shifterNow;
  assign fsm_wantExit = 1'b0;
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
      fsm_enumDef_SEND : begin
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
      end
      fsm_enumDef_AUTOBAUD : begin
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
        if(sclEdge_rise) begin
          if(when_I2CBertTop_l750) begin
            fsm_stateNext = fsm_enumDef_ACKNACK;
          end
        end
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l775) begin
          if(!when_I2CBertTop_l781) begin
            if(sclEdge_rise) begin
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
      end
      fsm_enumDef_SEND : begin
        if(sclEdge_rise) begin
          if(when_I2CBertTop_l764) begin
            fsm_stateNext = fsm_enumDef_PRECHECK;
          end
        end
      end
      fsm_enumDef_PRECHECK : begin
        if(when_I2CBertTop_l801) begin
          fsm_stateNext = fsm_enumDef_CHECK;
        end
      end
      fsm_enumDef_CHECK : begin
        if(sclEdge_rise) begin
          fsm_stateNext = fsm_enumDef_POSTCHECK;
        end
      end
      fsm_enumDef_POSTCHECK : begin
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
      fsm_enumDef_AUTOBAUD : begin
        if(sclEdge_rise) begin
          if(when_I2CBertTop_l832) begin
            fsm_stateNext = fsm_enumDef_ACKNACK;
          end
        end
      end
      default : begin
      end
    endcase
    if(when_I2CBertTop_l843) begin
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

  assign when_I2CBertTop_l750 = (fsm_bitCount == 3'b111);
  assign when_I2CBertTop_l775 = (((! sclHistory_0) || sclEdge_rise) || io_canStretch);
  assign _zz_io_bus_sdaOut = ((io_canNack && (! io_canSend)) && (! io_canRecv));
  assign when_I2CBertTop_l781 = ((! sclHistory_0) && io_canStretch);
  assign when_I2CBertTop_l764 = (fsm_bitCount == 3'b111);
  assign when_I2CBertTop_l801 = (! sclHistory_0);
  assign when_I2CBertTop_l832 = (fsm_bitCount == 3'b111);
  assign when_I2CBertTop_l843 = (isStop && (! sdaTx));
  always @(posedge clk) begin
    if(when_Utils_l1149) begin
      sdaHistory_1 <= sdaHistory_0;
    end
    if(when_Utils_l1149) begin
      sdaHistory_2 <= sdaHistory_1;
    end
    if(when_Utils_l1149_1) begin
      sclHistory_1 <= sclHistory_0;
    end
    if(when_Utils_l1149_1) begin
      sclHistory_2 <= sclHistory_1;
    end
    sda_regNext <= sda;
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
        if(sclEdge_rise) begin
          shifter <= shifterNow;
          if(!when_I2CBertTop_l750) begin
            fsm_bitCount <= (fsm_bitCount + 3'b001);
          end
        end
      end
      fsm_enumDef_ACKNACK : begin
        if(when_I2CBertTop_l775) begin
          if(!when_I2CBertTop_l781) begin
            if(sclEdge_rise) begin
              fsm_bitCount <= 3'b000;
              if(io_canSend) begin
                shifter <= io_data8tx;
              end
            end
          end
        end
      end
      fsm_enumDef_SEND : begin
        if(sclEdge_rise) begin
          shifter <= {shifter[6 : 0],shifter[7]};
          if(!when_I2CBertTop_l764) begin
            fsm_bitCount <= (fsm_bitCount + 3'b001);
          end
        end
      end
      fsm_enumDef_PRECHECK : begin
      end
      fsm_enumDef_CHECK : begin
      end
      fsm_enumDef_POSTCHECK : begin
        fsm_bitCount <= 3'b000;
        if(io_canSend) begin
          shifter <= io_data8tx;
        end
      end
      fsm_enumDef_AUTOBAUD : begin
        if(sclEdge_rise) begin
          if(!when_I2CBertTop_l832) begin
            fsm_bitCount <= (fsm_bitCount + 3'b001);
          end
        end
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
  input               io_timerLoadH,
  input               io_timerLoadL,
  input      [7:0]    io_timerData,
  output     [11:0]   io_timerEndstop,
  input               rst_n,
  input               clk
);

  reg        [11:0]   endstop;
  wire                when_I2CBertTop_l556;
  reg        [11:0]   ticker_count;
  wire                ticker_sclTick;
  reg                 ticker_timeoutError;
  reg                 ticker_canStart;
  reg                 ticker_canPowerOnReset;
  wire                ticker_reset;
  reg        [2:0]    ticker_tickState;
  reg        [7:0]    ticker_endstopTmpL;
  wire                when_I2CBertTop_l583;
  wire                when_I2CBertTop_l589;
  wire                when_I2CBertTop_l592;
  wire                when_I2CBertTop_l595;

  assign when_I2CBertTop_l556 = (! rst_n);
  assign io_timerEndstop = endstop;
  assign ticker_sclTick = 1'b0;
  always @(*) begin
    ticker_timeoutError = 1'b0;
    if(when_I2CBertTop_l592) begin
      ticker_timeoutError = 1'b1;
    end
  end

  always @(*) begin
    ticker_canStart = 1'b0;
    if(when_I2CBertTop_l589) begin
      ticker_canStart = 1'b1;
    end
  end

  always @(*) begin
    ticker_canPowerOnReset = 1'b0;
    if(when_I2CBertTop_l595) begin
      ticker_canPowerOnReset = 1'b1;
    end
  end

  assign ticker_reset = (! io_timerRun);
  assign when_I2CBertTop_l583 = (ticker_tickState == 3'b101);
  assign when_I2CBertTop_l589 = (ticker_count == 12'h012);
  assign when_I2CBertTop_l592 = (ticker_count == 12'h03c);
  assign when_I2CBertTop_l595 = (ticker_count == 12'h004);
  assign io_timeoutError = ticker_timeoutError;
  assign io_sclTick = ticker_sclTick;
  assign io_canStart = ticker_canStart;
  assign io_canPowerOnReset = ticker_canPowerOnReset;
  always @(posedge clk) begin
    if(when_I2CBertTop_l556) begin
      if(io_div12active) begin
        endstop <= io_div12;
      end else begin
        endstop <= 12'h005;
      end
    end
    if(io_timerLoad) begin
      endstop <= ticker_count;
    end else begin
      if(io_timerLoadH) begin
        endstop[7 : 0] <= ticker_endstopTmpL;
        endstop[11 : 8] <= io_timerData[3 : 0];
      end else begin
        if(io_timerLoadL) begin
          ticker_endstopTmpL <= io_timerData;
        end
      end
    end
  end

  always @(posedge clk) begin
    if(!rst_n) begin
      ticker_count <= 12'h000;
      ticker_tickState <= 3'b000;
    end else begin
      if(when_I2CBertTop_l583) begin
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
  input      [0:0]    io_op2,
  input               io_reset,
  input               io_en,
  input               clk,
  input               rst_n
);

  wire       [7:0]    _zz_acc;
  reg        [7:0]    acc;
  wire       [2:0]    switch_I2CBertTop_l181;

  assign _zz_acc = (acc + io_opand);
  assign switch_I2CBertTop_l181 = {io_op2,io_op};
  assign io_acc = acc;
  always @(posedge clk) begin
    if(!rst_n) begin
      acc <= 8'h00;
    end else begin
      if(io_reset) begin
        acc <= 8'h00;
      end else begin
        if(io_en) begin
          case(switch_I2CBertTop_l181)
            3'b000 : begin
              acc <= (acc & io_opand);
            end
            3'b001 : begin
              acc <= (acc | io_opand);
            end
            3'b010 : begin
              acc <= (acc ^ io_opand);
            end
            3'b011 : begin
              acc <= _zz_acc;
            end
            default : begin
              acc <= io_opand;
            end
          endcase
        end
      end
    end
  end


endmodule
