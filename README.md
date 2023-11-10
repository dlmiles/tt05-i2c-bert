![](../../workflows/spinalhdl/badge.svg) ![](../../workflows/wokwi_test/badge.svg) ![](../../workflows/test/badge.svg)
![](../../workflows/gds/badge.svg) ![](../../workflows/sta_reporter/badge.svg) ![](../../workflows/coverage/badge.svg)
![](../../workflows/docs/badge.svg)



# TT05 I2C Bit Error Rate Tester (BERT)<br/>Echo ALU Peripheral


I2C TinyTapeout
 * TT 7SEG outputs driven from register to provide I2C control of 7SEG.

Included a couple of experimental items:
 * Latching configuration bits on ENA rise and RST_N rise.
 * SDA line status sense at power-on and reset.

GHA actions includes:

 * Gate Level testing
 * Verilator / Cocotb coverage testing and report
 * Online browser of VCD outputs (using Surfer viewer)

[Full Project Documentation and User Manual](https://dlmiles.github.io/tt05-i2c-bert/asciidoc/)


## I2C Peripheral

 * 8-bit ALU write with accumulator (AND, OR, XOR, ADD) on the end of I2C.
 * 8-bit ALU read with accumulator (repeat) on the end of I2C.
 * 8-bit RECV read with accumulator (ADD1) 


 * Send fixed size commands.
 * Received (generate) read response data.


 * Supports Open-Drain (default) and Push Pull line modes.

 * Supports SCL/SDA origin mode (RegNext, MAJ3, 3DFF-synchronizer, ANDNOR3-unanimous,
   5DFF-synchronizer, MAJ5, DIRECT/RAW, ANDNOR5-unanimous)
   These represent methods of line noise immunity for serial communications

 * Supports fixed divisor mode for sample tick 1:1, 1:2, 1:4, 1:8 with master clock.

 * Supports a wide range of master CLK frequencies, I2C communication should
   be possible down to 1:3, as an example of expectations at 10MHz clock
   fast-mode I2C 400Kbps is possible at 1:25.  Ideally with more working on
   hardware design time 1:2 should be possible.


 * ACK generator
 * NACK generator


 * Read/Write ALU accumulator value
 * Write ALU accumulator compare (generates ACK/NACK for expected value)


 * Read data (fixed size command, 1 to 2^12 bytes)
 * Read data (unlimited length)
 * Write data (fixed size command, 1 to 2^12 bytes, processes each byte through ALU)
 * Write data (unlimited length)


 * Read/Write Configuration Mode (OD/PP mode, SCL mode, SCL less
 * Read/Write Timer Endstop (for clock/timeout generation)
 * Read/Write Length Register (high 8 bits of 12 bits)
 * Read 32bit Latched Configuration data

## Clock rate table

This information is based on testbench projections for the limits of the
design.

These are theoretical test-bench projections on performance.

| Master Clock | Ratio | Sampler | 1-stage      | 2-stage      | 3-stage      | 5-stage      |
|--------------|-------|---------|--------------|--------------|--------------|--------------|
| 500 Khz      | 25:1  | 1:1     | 20 Kbps      | 20 Kbps      | 20 Kbps      | 20 Kbps      |
| 1 MHz        | 25:1  | 1:1     | 40 Kbps      | 40 Kbps      | 40 Kbps      | 40 Kbps      |
| 10 MHz       | 25:1  | 1:1     | **400 Kbps** | **400 Kbps** | **400 Kbps** | **400 Kbps** |
| "            | 25:1  | 1:2     | **400 Kbps** | **400 Kbps** | **400 Kbps** | **400 Kbps** |
| "            | 25:1  | 1:4     | **400 Kbps** | **400 Kbps** | **400 Kbps** | **400 Kbps** |
| "            | 25:1  | 1:8     | **400 Kbps** | **400 Kbps** | **400 Kbps** |              |
| "            | 33:1  | 1:8     |              |              |              | 300 Kbps     |
| 25 MHz       | 25:1  | 1:1     | 1 Mbps       | 1 Mbps       | 1 Mbps       | 1 Mbps       |
| 50 MHz       | 25:1  | 1:1     | 2 Mbps       | 2 Mbps       | 2 Mbps       | 2 Mbps       |
| 66 Mhz       | 25:1  | 1:1     | 2.64 Mbps    | 2.64 Mbps    | 2.64 Mbps    | 2.64 Mbps    |

The design has passed STA and PNR for CLOCK_PERIOD=15 ns (66.66 MHz)

The noise immunity method trades clock to sample ratio (thus lowering
maximum I2C bit rate) for improved noise immunity characteristics.

* 1-stage relates to modes: RegNext, DIRECT/RAW
* 2-stage relates to modes: (not included in tt05, 2DFF-synchronizer, ANDNOR2-unanimous)
* 3-stage relates to modes: MAJ3, 3DFF-synchronizer, ANDNOR3-unanimous
* 5-stage relates to modes: MAJ5, 5DFF-synchronizer, ANDNOR5-unanimous

## Latching configuration bits on ENA rise and RST_N rise

This is an experiment to confirm if it is possible to use SKY130 DLATCH on
the input lines to store configuration data during project selection and

The RST_N rise should work as the timing can be completely managed by the TT
project selection and startup and reset procedure.

The ENA rise is more experimental and due to the quiescent nature of all the
input lines before the ENA signal rise it maybe subject to timing relationship
during project activation.  I have not looked into the specific detail TT
multiplexor implementation in this area to know if this idea stands any chance
of working.

It assumes the rise of initial logic state all occur at the same time as the
ENA rise, it is hopeful that due to the nature of latches the negative setup
time will help with being able to observe and latch the input line state at
that time.  The purpose is to allow 16 reconfigurable configurable bits
to be held.

Latches are used instead of flipflops to improve area efficient of this
task.  As there are 16 input lines and two events to latch that is a
total of 32 bit of available state.


## SDA line status sense on power-on and reset

This feature is designed to interpret the SDA line status at the time of
power-on-reset and over a few clock cycles thereafter.  This is intended to
provide and out-of-band mechanism to trigger a diagnostic mode startup.

As per the nature of I2C a normal startup is indicated with sensing the
expected high line state due to pull-up resistor being on the line. To the
powerOnSense flag is raised when SDA line is low during power-on, or very
soon thereafter.


## TODO if there is time

* AUTOBAUD clocking mode, with no SCL
* STRETCH tester

* Additional sample modes: ANDNOR2-unanimous, 2DFF-synchronizer, ...

* 8-bit ALU read with accumulator (repeat, ROL, INVERT, ADD1) on the end of I2C. 
  This did not make TT05 in the form I expected.

* A handful of the features on the list need to be tested that they have been delivered in the TT05 version.

* A few areas not covered yet in coverage report.
  https://dlmiles.github.io/tt05-i2c-bert/coverage/


![VCD Image](tt05-i2c-bert.png)



###

# What is Tiny Tapeout?

TinyTapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip.

To learn more and get started, visit https://tinytapeout.com.

## Wokwi Projects

Edit the [info.yaml](info.yaml) and change the wokwi_id to the ID of your Wokwi project. You can find the ID in the URL of your project, it's the big number after `wokwi.com/projects/`.

The GitHub action will automatically fetch the digital netlist from Wokwi and build the ASIC files.

## Verilog Projects

Edit the [info.yaml](info.yaml) and uncomment the `source_files` and `top_module` properties, and change the value of `language` to "Verilog". Add your Verilog files to the `src` folder, and list them in the `source_files` property.

The GitHub action will automatically build the ASIC files using [OpenLane](https://www.zerotoasiccourse.com/terminology/openlane/).

## Enable GitHub actions to build the results page

- [Enabling GitHub Pages](https://tinytapeout.com/faq/#my-github-action-is-failing-on-the-pages-part)

## Resources

- [FAQ](https://tinytapeout.com/faq/)
- [Digital design lessons](https://tinytapeout.com/digital_design/)
- [Learn how semiconductors work](https://tinytapeout.com/siliwiz/)
- [Join the community](https://discord.gg/rPK2nSjxy8)

## What next?

- Submit your design to the next shuttle [on the website](https://tinytapeout.com/#submit-your-design). The closing date is **November 4th**.
- Edit this [README](README.md) and explain your design, how it works, and how to test it.
- Share your GDS on your social network of choice, tagging it #tinytapeout and linking Matt's profile:
  - LinkedIn [#tinytapeout](https://www.linkedin.com/search/results/content/?keywords=%23tinytapeout) [matt-venn](https://www.linkedin.com/in/matt-venn/)
  - Mastodon [#tinytapeout](https://chaos.social/tags/tinytapeout) [@matthewvenn](https://chaos.social/@matthewvenn)
  - Twitter [#tinytapeout](https://twitter.com/hashtag/tinytapeout?src=hashtag_click) [@matthewvenn](https://twitter.com/matthewvenn)

