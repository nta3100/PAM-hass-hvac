#! /usr/bin/python3

import AC_IR

def encode_funiki2(device):
    Funiki_2_template = "C38700002000200000200005AF"
    FUNIKI_2_HDR_MARK_USER = "8900"
    FUNIKI_2_HDR_SPACE_USER = "4450"
    FUNIKI_2_BIT_MARK_USER = "550"
    FUNIKI_2_ONE_SPACE_USER = "1650"
    FUNIKI_2_ZERO_SPACE_USER = "550"

    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode

    if _swing == 0:
        _swing = 0
    elif _swing == 1:
        _swing = 1
    elif _swing == 2:
        _swing = 2
    elif _swing == 3:
        _swing = 3
    elif _swing == 4:
        _swing = 4
    elif _swing == 5:
        _swing = 5
    else:
        _swing = 0
    
    if _mode == 1:
        _mode = 4
    elif _mode == 2:
        _mode = 1
    elif _mode == 3:
        _mode = 2
    elif _mode == 4:
        _mode = 6
    else: 
        _mode = 4

    if _fan == 0:
        _fan = 0
    elif _fan == 1:
        _fan = 3
    elif _fan == 2:
        _fan = 5
    else:
        _fan = 0
    
    _buff = AC_IR.hex_string_to_byte_array(Funiki_2_template)
    if device.mode == "off":
        _buff = switch_off(_buff)
        _buff = change_mode(_buff, _mode)
        if _temp == 0:
            _buff = temp_down(_buff)
        elif _temp == 1:
            _buff = temp_up(_buff)
        elif _temp == 2:
            pass
        elif (_temp > 15) and (_temp < 32):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    else:
        _buff = switch_on(_buff)
        _buff = change_mode(_buff, _mode)
        if _temp == 0:
            _buff = temp_down(_buff)
        elif _temp == 1:
            _buff = temp_up(_buff)
        elif _temp == 2:
            pass
        elif (_temp > 15) and (_temp < 32):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    cs = check_sum(_buff, 0, 12)
    str_raw = ""
    str_bin = ""
    for i in range(0, len(_buff) - 1):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
    str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 0)

    str_raw += FUNIKI_2_HDR_MARK_USER
    str_raw += ','
    str_raw += FUNIKI_2_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 8*13):
        str_raw += FUNIKI_2_BIT_MARK_USER
        str_raw += ','
        if str_bin == '1':
            str_raw += FUNIKI_2_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += FUNIKI_2_ZERO_SPACE_USER
            str_raw += ','
    str_raw += FUNIKI_2_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"
    str_raw = AC_IR.gz_base64_compress(str_raw)
    return str_raw
        
def switch_off(_buff):
    _buff[9] = _buff[9] & 0xdf
    _buff[9] = _buff[9] | 0x00
    state = 0
    return _buff

def switch_on(_buff):
    _buff[9] = _buff[9] & 0xdf
    _buff[9] = _buff[9] | 0x20
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 32):
        if temp == 31:
            pass
        else:
            _buff[1] = _buff[1] + 1
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 32):
        if temp == 16:
            pass
        else:
            _buff[1] = _buff[1] - 1
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 8
    __temp = _temp
    _buff[1] = _buff[1] & (~(0x3f << 3))
    _buff[1] = _buff[1] | (__temp << 3)
    return _buff

def read_temp(_buff):
    _temp = [None] * 5
    _temp[0] = (_buff[1] >> 3) & 0x01
    _temp[1] = (_buff[1] >> 4) & 0x01
    _temp[2] = (_buff[1] >> 5) & 0x01
    _temp[3] = (_buff[1] >> 6) & 0x01
    _temp[4] = (_buff[1] >> 7) & 0x01
    temp = 8 + AC_IR.bit_to_int(_temp, 5, 0)
    return temp

def change_fan(_buff, _fan):
    if _fan == 0:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0x00
    elif _fan == 3:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0x60
    elif _fan == 1:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0x20
    elif _fan == 5:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0xa0
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = [None] * 2
    _fan[0] = (_buff[0] >> 4) & 0x01
    _fan[1] = (_buff[0] >> 5) & 0x01
    fan = AC_IR.bit_to_int(_fan, 2, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 0:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x00
    elif _swing == 1:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x01
    elif _swing == 2:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x02
    elif _swing == 3:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x03
    elif _swing == 4:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x04
    elif _swing == 5:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x05
    else:
        pass
    return _buff

def read_swing(_buff):
    _swing = [None] * 3
    _swing[0] = (_buff[4] >> 0) & 0x01
    _swing[1] = (_buff[4] >> 1) & 0x01
    _swing[2] = (_buff[4] >> 2) & 0x01
    swing = AC_IR.bit_to_int(_swing, 3, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 0:
        pass
    elif _mode == 4:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0x80
    elif _mode == 1:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0x20
    elif _mode == 2:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0x40
    elif _mode == 6:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0xc0
    else:
        pass
    return _buff

def read_mode(_buff):
    _mode = [None] * 2
    _mode[0] = (_buff[0] >> 6) & 0x01
    _mode[1] = (_buff[0] >> 7) & 0x01
    mode = AC_IR.bit_to_int(_mode, 2, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + _buf[i]
    _cs = _cs % 256
    return _cs

