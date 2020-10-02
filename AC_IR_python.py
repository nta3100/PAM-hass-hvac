#! /usr/bin/python3

import gzip
import base64
#IR_AC.java
#Set AC
#Read AC
#Bit to int
def bit_to_int(_buf, _len, _s):
    value = 0
    __buff = _buf
    if _s==1:
        __buff = bit_reverse(_buf, _len)
    for i in range(_len):
        value = value + (int)(__buff[i])*(int)(2**i)
    return value
#Bit_reverse
def bit_reverse(_buffin, len):
    _buffout = []
    for i in range(len):
        _buffout.append(_buffin[len-1-i])
    #return: ['0', '1', ....]
    return _buffout
#Bit to Byte
def bit_to_byte(_bits):
    __byte = 0
    __byte |= _bits[0]<<0
    __byte |= _bits[1]<<0
    __byte |= _bits[2]<<0
    __byte |= _bits[3]<<0
    __byte |= _bits[4]<<0
    __byte |= _bits[5]<<0
    __byte |= _bits[6]<<0
    __byte |= _bits[7]<<0
    __byte = bitReverse(__byte)
    return __byte
#BitReverse
def bitReverse(x):
    x = (((x >> 1) & 0x55) | ((x << 1) & 0xAA))
    x = (((x >> 2) & 0x33) | ((x << 2) & 0xCC))
    x = (((x >> 4) & 0x0F) | ((x << 4) & 0xF0))
    return x
#Hex string to byte array
def hex_string_to_byte_array(str_in):
    str_out = bytearray.fromhex(str_in)
    return str_out
#Byte to string
def byte_to_string(_b, _type):
    str_out = ""
    txt = "{0:{fill}8b}"
    if _type == 1:
        for i in _b:
            str_out += txt.format(i, fill = '0')
    else:
        for i in _b:
            str_buff = txt.format(i, fill = '0')
            #print(str_buff)
            for j in range(7, -1 , -1):
                str_out += str_buff[j]
    return str_out

#GZbase64Compress
def gz_base64_compress(str_in):
    str_in = str_in.encode('utf-8')
    compress = gzip.compress(str_in)
    str_out = base64.b64encode(b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\xff' + compress[10:])
    #str_out = base64.b64encode(compress)
    str_out = str_out.decode('utf-8')
    return str_out
