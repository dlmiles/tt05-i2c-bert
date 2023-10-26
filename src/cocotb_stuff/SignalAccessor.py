#
#
#
#
#
#
# SPDX-FileCopyrightText: Copyright 2023 Darryl Miles
# SPDX-License-Identifier: Apache2.0
#
#
import cocotb

from .cocotbutil import *
from cocotb.binary import BinaryValue
from cocotb.utils import get_sim_time



# Provides a way to encapsulate and isolate a signal
# So the problem is maybe the VPI (or whatever interface model) can only operate on
#  the entire signal, all bits of the bus.  But we want an API that can work in a
#  partial bus that is transparently behaves like it would if we operated on the
#  entire bus.
# This is then a problem if we make 2 or more separate modifucation to the value
#  this clock cycle, performing a read-modify-write can only see the original value
#  at the end of the simulation tick, not the separate modification we made.
#
#
#
#
# Like a wide-bus to a narrow-bus or bit
class SignalAccessor():
    def __init__(self, dut, path: str, bitid: int = None, width: int = 1) -> None:
        assert dut is not None
        assert isinstance(path, str)
        assert bitid is None or bitid >= 0, f"bitid is invalid: {bitid}"
        assert width > 0, f"width is out of range > 0: {width}"
        assert width == 1, f"width != 1 is not supported"	# TODO

        self._dut = dut
        self._path = path
        self._bitid = bitid
        self._width = width

        self._signal_update_list = []
        self._signal_update_sim_time = get_sim_time

        signal = design_element(dut, path)
        if signal is None:
            raise Exception(f"Unable to find signal path: {path}")
        self._signal = signal

        # FIXME maybe for efficient can be optimize the 3 scenarios and generate a value(self)
        #   function and attach
        # 0: direct signal.value (no change)
        # 1: single bit isolation
        # 2: width>1 bus isolation

        return None


    # Allow single bit
    class AccessorBit():
        def __init__(self, sa: 'SignalAccessor', bitid: int):
            self._sa = sa
            assert type(bitid) is int
            assert bitid >= 0 and bitid < 4096	# sanity check
            self._bitid = bitid
            self._width = 1
            return None


        @property
        def value(self):
            if self._bitid is not None:
                vstr = self._sa.signal_str()
                ## isolate
                if self._width == 1:
                    bstr = vstr[-self._bitid-1]		# minus prefix due to bit0 on right hand side
                else:
                    assert False, f"width = {self._width}"
                #print(f"SignalAccessor(path={self._path}) = {vstr} => {self._bitid} for {bstr}")
                v = BinaryValue(bstr, n_bits=len(bstr))
                return v

            return self._signal.value


        @value.setter
        def value(self, v: bool) -> None:
            assert isinstance(v, bool)
            nv = '1' if (v) else '0'
            if self._bitid is not None:
                vstr = self._sa.signal_str()
                ## isolate
                if self._width == 1:
                    nstr = vstr[0:-self._bitid-1] + nv + vstr[-self._bitid:]	# minus prefix due to bit0 on right hand side
                    print(f"vstr = {vstr}, bitid={self._bitid} nstr={nstr} left={vstr[0:-self._bitid-1]} right={vstr[-self._bitid:]} v={v}")
                else:
                    assert False, f"width = {self._width}"
                print(f"SignalAccessor(path={self.path}) = {vstr} => {self._bitid} for {nstr}")
                self._sa.signal_update(BinaryValue(nstr, n_bits=len(nstr)))
                return None

            assert False, f"set_value()"


        @property
        def accessor(self):
            return self._sa


        @property
        def raw(self):
            return self._signal		# maybe this should be removed ?


        @property
        def path(self) -> str:
            return self._sa.path	# maybe we should append f"[{self._bitid}]" ?



    # Allow contigious bus patterns
    class AccessorBus():
        def __init__(self, sa: 'SignalAccessor', first_bit: int, last_bit: int):
            self._sa = sa
            assert type(first_bit) is int
            assert first_bit >= 0 and first_bit < 4096	# sanity check
            self._first_bit = first_bit
            assert type(last_bit) is int
            assert last_bit >= 0 and last_bit < 4096	# sanity check
            self._last_bit = last_bit
            assert last_bit >= first_bit
            self._width = last_bit - first_bit + 1
            assert width > 1
            return None


        @property
        def value(self):
            vstr = self._sa.signal_str()
            ## isolate
            assert False, f"width = {self._width}"
            #print(f"SignalAccessor(path={self._path}) = {vstr} => {self._bitid} for {bstr}")
            v = BinaryValue(bstr, n_bits=len(bstr))
            return v


        @value.setter
        def value(self, v: int) -> None:
            assert isinstance(v, int)
            nv = '1' if (v) else '0'	# FIXME BinaryValue
            vstr = self._sa.signal_str()
            ## isolate
            assert False, f"width = {self._width}"
            print(f"SignalAccessor(path={self.path}) = {vstr} => {self._bitid} for {nstr}")
            self._sa.signal_update(BinaryValue(nstr, n_bits=len(nstr)))
            return None


        @property
        def accessor(self):
            return self._sa


        @property
        def raw(self):
            return self._signal		# maybe this should be removed ?


        @property
        def path(self) -> str:
            return self._sa.path	# maybe we should append f"[{self._first_bit}:{self._last_bit}]" ?


    # Allow non-contigious bus patterns
    class AccessorBusPattern():
        def __init__(self, sa: 'SignalAccessor', pattern: str):
            self._sa = sa
            return None


        @property
        def accessor(self):
            return self._sa


    def register(self, first_bit: int, last_bit: int = -1):
        if last_bit < 0:
            last_bit = first_bit
        assert type(first_bit) is int

        width = last_bit - first_bit + 1
        assert width >= 1

        if width == 1:
            return self.AccessorBit(self, first_bit)
        elif width > 1:
            return self.AccessorBus(self, first_bit, last_bit)


    def register_pattern(self, pattern: str):
        return AccessorBusPattern(self, pattern)


    def signal_str(self):
        return str(self._signal.value)	## FIXME


    # The value probably need to be a before, after, delta-change
    def signal_update(self, value):
        now = get_sim_time
        # Get sim_time
        # If we have a saved sim_time and it is not the same, invalidate changes
        if self._signal_update_sim_time != now:
            self._signal_update_list = []	# invalidate
            # Store timestamp
            self._signal_update_sim_time = now
        # Store this state change
        self._signal_update_list.append(value)	# FIXME
        # Compute new composite value
        new_value = str(self._signal.value)
        for item in self._signal_update_list:
            new_value = self.compute(new_value, item)
        # Commit to signal
        self._signal.value = value	## FIXME


    def compute(self, value, item):
        # FIXME need some magic here
        return value


    # Access full signal width, FIXME move this to subclass like others via auto-selection
    @property
    def value(self):
        if self._bitid is not None:
            vstr = self.signal_str()
            ## isolate
            if self._width == 1:
                bstr = vstr[-self._bitid-1]		# minus prefix due to bit0 on right hand side
            else:
                assert False, f"width = {self._width}"
            #print(f"SignalAccessor(path={self._path}) = {vstr} => {self._bitid} for {bstr}")
            v = BinaryValue(bstr, n_bits=len(bstr))
            return v

        return self._signal.value


    # Access full signal width, FIXME move this to subclass like others via auto-selection
    @value.setter
    def value(self, v: bool) -> None:
        assert isinstance(v, bool)
        nv = '1' if (v) else '0'
        if self._bitid is not None:
            vstr = self.signal_str()
            ## isolate
            if self._width == 1:
                nstr = vstr[0:-self._bitid-1] + nv + vstr[-self._bitid:]	# minus prefix due to bit0 on right hand side
                print(f"vstr = {vstr}, bitid={self._bitid} nstr={nstr} left={vstr[0:-self._bitid-1]} right={vstr[-self._bitid:]} v={v}")
            else:
                assert False, f"width = {self._width}"
            print(f"SignalAccessor(path={self._path}) = {vstr} => {self._bitid} for {nstr}")
            self.signal_update(BinaryValue(nstr, n_bits=len(nstr)))
            return None

        assert False, f"set_value()"


    @property
    def raw(self):
        return self._signal


    @property
    def path(self) -> str:
        return self._path


    # sa_or_path: SignalAccessor|str
    @staticmethod
    def build(dut, sa_or_path) -> tuple:	# SignalAccessor, str
        if isinstance(sa_or_path, str):
            sa = SignalAccessor(dut, sa_or_path)
        if isinstance(sa_or_path, SignalAccessor):
            sa = sa_or_path
        assert sa is not None

        return (sa, sa.path)


__all__ = [
    'SignalAccessor'
]
