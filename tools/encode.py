#!/usr/bin/env python3

# This is a precomputed lookup table for the broken UTF-8 encoding used by CANON
from lut import UTF8_LUT
import sys, struct
from functools import lru_cache
import binascii


@lru_cache
def lut_find_full(v):
    v = bytes([v])
    for k in UTF8_LUT.keys():
        if UTF8_LUT[k] == v:
            return k
    return None


@lru_cache
def lut_find_prefix(v):
    for k in UTF8_LUT.keys():
        if UTF8_LUT[k].startswith(v):
            return k
    return None


@lru_cache
def lut_find_suffix(v):
    for k in UTF8_LUT.keys():
        if UTF8_LUT[k].endswith(v):
            return k
    return None


def is_upper_ascii(v):
    if v >= 0x41 and v <= 0x5A:
        return True
    return False


def encode32(val):
    b = struct.pack("<L", val)

    for i in range(3):
        if is_upper_ascii(b[i]):
            return False

    # use mirror
    if is_upper_ascii(b[3]):
        b = b[0:3] + bytes([b[3] + 0x40])

    # the following is super ugly, but it works(tm)

    # full * 4
    o = []
    v = lut_find_full(b[0])
    if v is not None:
        o.append(v)
        v = lut_find_full(b[1])
        if v is not None:
            o.append(v)
            v = lut_find_full(b[2])
            if v is not None:
                o.append(v)
                v = lut_find_full(b[3])
                if v is not None:
                    o.append(v)
                    return o

    # full * 2 + prefix(2)
    o = []
    v = lut_find_full(b[0])
    if v is not None:
        o.append(v)
        v = lut_find_full(b[1])
        if v is not None:
            o.append(v)
            v = lut_find_prefix(b[2:])
            if v is not None:
                o.append(v)
                return o

    # full * 3 + prefix(2)
    o = []
    v = lut_find_full(b[0])
    if v is not None:
        o.append(v)
        v = lut_find_full(b[1])
        if v is not None:
            o.append(v)
            v = lut_find_full(b[2])
            if v is not None:
                o.append(v)
                v = lut_find_prefix(b[3:])
                if v is not None:
                    o.append(v)
                    return o

    # suffix(2) + full * 2
    o = []
    v = lut_find_suffix(b[0:2])
    if v is not None:
        o.append(v)
        v = lut_find_full(b[2])
        if v is not None:
            o.append(v)
            v = lut_find_full(b[3])
            if v is not None:
                o.append(v)
                return o

    # suffix(3) + full
    o = []
    v = lut_find_suffix(b[0:3])
    if v is not None:
        o.append(v)
        v = lut_find_full(b[3])
        if v is not None:
            o.append(v)
            return o

    # suffix(3) + prefix(1)
    o = []
    v = lut_find_suffix(b[0:3])
    if v is not None:
        o.append(v)
        v = lut_find_prefix(b[3:])
        if v is not None:
            o.append(v)
            return o

    # suffix(2) + prefix(2)
    o = []
    v = lut_find_suffix(b[0:2])
    if v is not None:
        o.append(v)
        v = lut_find_prefix(b[2:])
        if v is not None:
            o.append(v)
            return o

    # suffix(1) + prefix(3)
    o = []
    v = lut_find_suffix(b[0:1])
    if v is not None:
        o.append(v)
        v = lut_find_prefix(b[1:])
        if v is not None:
            o.append(v)
            return o

    return False


if __name__ == "__main__":
    addr = int(sys.argv[1], 0)
    r = encode32(int(sys.argv[1], 0))
    if r is False:
        print("fail")
        exit(-1)
    o = b""
    vv = ""
    for v in r:
        vv += "&#x%X;" % (v)
        o += UTF8_LUT[v]
    print(vv)
    print(binascii.hexlify(o))
    print(len(o))
