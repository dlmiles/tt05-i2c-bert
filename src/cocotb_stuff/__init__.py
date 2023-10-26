#
#
#
#
#
# SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
# SPDX-License-Identifier: Apache2.0
#
#


SDA_BITID		= 2	# bidi: uio_out & uio_in
SCL_BITID		= 3	# bidi: uio_out & uio_in

# This validate the design under test matches values here
def validate(dut) -> bool:
    return True


__all__ = [
    'SDA_BITID',
    'SCL_BITID',

    'validate'
]
