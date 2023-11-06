# SpinalHDL Project

git clone https://github.com/SpinalHDL/SpinalTemplateSbt spinalhdl

# Using the version from:
commit a4eb1e65efdfd3317d8125538fc8d01fb8bcc0ec (HEAD -> master, origin/master, origin/HEAD)
Author: Dolu1990 <charles.papon.90@gmail.com>
Date:   Mon Mar 27 09:57:17 2023 +0200

    SpinalHDL 1.8.1



# Install Java 17 LTS
# Install sbt

$ java -version
java version "17.0.6" 2023-01-17 LTS
Java(TM) SE Runtime Environment (build 17.0.6+9-LTS-190)
Java HotSpot(TM) 64-Bit Server VM (build 17.0.6+9-LTS-190, mixed mode, sharing)

$ sbt -V
sbt version in this project: 1.6.0
sbt script version: 1.8.2



$ sbt clean
$ sbt compile
$ sbt test

# To generate the Verilog from the example
sbt "runMain projectname.MyTopLevelVerilog"

# To generate the VHDL from the example
sbt "runMain projectname.MyTopLevelVhdl"

# To run the testbench
sbt "runMain projectname.MyTopLevelSim"

# To run Formal verification
sbt "runMain projectname.MyTopLevelFormal"
