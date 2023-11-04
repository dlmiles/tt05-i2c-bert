#!/bin/bash -e
#
# The purpose of this script is to provide a check/validation/change of the
# verilog is setup for production building.
#
# The changes include:
#   * ensure external toplevel ports debug_S{CL,DA}*  and assignment code
#     is removed
#   * ensure external toplevel port simulation_z and assignment code
#     is removed
#
#
# If you just run this utility it will report the current status encoded into
# the verilog and provide a non-zero exit status if that is not the production
# values.
#
# To auto-patch for production: check_verilog_production.sh patch patch_synthesis
#
#
VERILOG_FILE="TT05I2CBertTop.v"

ask="PROD"
patch=0
patch_coverage=0
patch_simulation=0
patch_synthesis=0
verbose=1
while [ $# -gt 0 ]
do
	case "$1" in
	sim|SIM|-sim|-SIM)
                ask="SIM"
                ;;
	ci|prod|-ci|-prod)
		ask="PROD"
		;;
	q|quiet|-q|-quiet)
		verbose=0
		;;
	patch)
		patch=1
		;;
	patch_simulation)
		patch_simulation=1
		;;
	patch_coverage)
		patch_coverage=1
		;;
	patch_synthesis)
		patch_synthesis=1
		;;
	esac

	shift
done

if [ $patch -gt 0 ]
then
	cp -n "$VERILOG_FILE" "${VERILOG_FILE}.gds_orig"

	sed	-e '\/^  .*put .*debug_SCL/d' \
		-e '\/^  .*put .*debug_SDA/d' \
		-e '\/assign debug_SCL/d' \
		-e '\/assign debug_SDA/d' \
		-e '\/assign _zz_debug_SDA/d' \
		-e '\/assign _zz_debug_SCL/d' \
		-e '\/wire .*debug_SCL/d' \
		-e '\/wire .*debug_SDA/d' \
		-e '\/^  .*put .*simulation.*/d' \
		-i "$VERILOG_FILE"

	if [ $patch_synthesis -gt 0 ]
	then
		echo "###"
		echo "### patch_synthesis=$patch_synthesis"
		echo "###"

		## DISABLED to test alternative method
		# Add _2 suffix to SKY130 cells
		#sed -e 's/ sky130_\([^ ]\+\) / sky130_\1_2 /' -i "$VERILOG_FILE"

		# So for IC flow synthesis there is no timescale, this is a simulation concept
		sed	-e '/`timescale/i\`ifdef TIMESCALE' \
			-e '/`timescale/a\`endif' \
			-i "$VERILOG_FILE"
	fi

	diff -u "${VERILOG_FILE}.gds_orig" "$VERILOG_FILE" || true
fi


grep_debug_SCL=$(egrep -s "\Wdebug_SCL" $VERILOG_FILE || true)
grep_debug_SDA=$(egrep -s "\Wdebug_SDA" $VERILOG_FILE || true)

#if [ -z "$grep_something" ]
#then
#	echo "$0: ERROR unable to find values in file: $VERILOG_FILE"
#	exit 1
#fi

found="unknown"

if      test -z "$grep_debug_SCL"  &&
	test -z "$grep_debug_SDA"
then
	if [ $verbose -gt 0 ]
	then
		echo "### $grep_debug_SCL"
		echo "### $grep_debug_SDA"
		echo "#################################################"
		echo "$VERILOG_FILE: is PRODUCTION ready"
	fi
	found="PROD"
fi

if      ! test -z "$grep_debug_SCL" ||
	! test -z "$grep_debug_SDA"
then
	if [ $verbose -gt 0 ]
	then
		echo "### $grep_debug_SCL"
		echo "### $grep_debug_SDA"
		echo "#################################################"
		echo "$VERILOG_FILE: setup for TESTING (not PRODUCTION ready)"
	fi
	found="SIM"
fi


if [ "$ask" = "$found" ]
then
	exit 0
fi

[ $verbose -gt 0 ] && echo "FAIL: exit=1"
exit 1
