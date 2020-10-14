#! /usr/bin/python3

import AC_IR

def encode_gree(device):
    Gree_template = "79080050"
    GREE_HDR_MARK_USER = "9000"
    GREE_HDR_SPACE_USER = "4500"
    GREE_BIT_MARK_USER = "650"
    GREE_ONE_SPACE_USER = "1600"
    GREE_ZERO_SPACE_USER = "550"
    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode

    if _swing == 0:
        _swing = 4
    elif _swing == 1:
        _swing = 0
    else:
        _mode = 0

    if _mode == 0:
        _mode = 0
    elif _mode == 1:
        _mode = 4
    elif _mode == 2:
        _mode = 1
    elif _mode == 3:
        _mode = 2
    elif _mode == 4:
        _mode = 3
    else:
        _mode = 0

    if _fan == 0:
        _fan = 0
    elif _fan == 1:
        _fan = 1
    elif _fan == 2:
        _fan = 2
    elif _fan == 3:
        _fan = 3
    else:
        _fan = 0
    
    _buff = AC_IR.hex_string_to_byte_array(Gree_template)
    if device.mode == "off":
        _buff = switch_off(_buff)
        _buff = change_mode(_buff, _mode)
        if _temp == 0:
            _buff = temp_down(_buff)
        elif _temp == 1:
            _buff = temp_up(_buff)
        elif _temp == 2:
            pass
        elif (_temp > 15) and (_temp < 31):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _fan)
    else:
        _buff = switch_on(_buff)
        _buff = change_mode(_buff, _mode)
        if _temp == 0:
            _buff = temp_down(_buff)
        elif _temp == 1:
            _buff = temp_up(_buff)
        elif _temp == 2:
            pass
        elif (_temp > 15) and (_temp < 31):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _fan)
    
    str_raw = ""
    str_bin = ""
    for i in range(0, len(_buff)):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
    str_raw += GREE_BIT_MARK_USER
    str_raw += ','
    str_raw += GREE_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 8*4):
        str_raw += GREE_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += GREE_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += GREE_ZERO_SPACE_USER
            str_raw += ','
    str_raw += GREE_BIT_MARK_USER
    str_raw += ','
    str_raw += GREE_ONE_SPACE_USER
    str_raw += ','
    str_raw += GREE_BIT_MARK_USER
    str_raw += ','
    str_raw += GREE_ZERO_SPACE_USER
    str_raw += ','
    str_raw += GREE_BIT_MARK_USER
    str_raw += ','
    str_raw += GREE_ONE_SPACE_USER
    str_raw += ','
    str_raw += GREE_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"

def switch_off(_buff):
    _buff[0] = _buff[0] & 0xf7
    _buff[0] = _buff[0] | 0x00
    state = 0
    return _buff

def switch_on(_buff):
    _buff[0] = _buff[0] & 0xf7 
    _buff[0] = _buff[0] | 0x08
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 31):
        if temp == 30:
            pass
        else:
            _buff[1] = _buff[1] + 1
    return _buff
    
def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 31):
        if temp == 16:
            pass
        else:
            _buff[1] = _buff[1] - 1
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 16
    __temp = _temp
    _buff[1] = _buff[1] & 0xf0
    _buff[1] = _buff[1] | __temp
    return _buff

def read_temp(_buff):
    _temp =[None] * 4
    _temp[0] = (_buff[1] >> 0) & 0x01
    _temp[1] = (_buff[1] >> 1) & 0x01
    _temp[2] = (_buff[1] >> 2) & 0x01
    _temp[3] = (_buff[1] >> 3) & 0x01
    temp = 16 + AC_IR.bit_to_int(_temp, 4, 0)
    return temp

def change_fan(_buff, _fan):
    if _fan == 0:
        _buff[0] = _buff[0] & 0xcf
        _buff[0] = _buff[0] | 0x00
    elif _fan == 1:
        _buff[0] = _buff[0] & 0xcf
        _buff[0] = _buff[0] | 0x10
    elif _fan == 2:
        _buff[0] = _buff[0] & 0xcf
        _buff[0] = _buff[0] | 0x20
    elif _fan == 3:
        _buff[0] = _buff[0] & 0xcf
        _buff[0] = _buff[0] | 0x30
    else:
        pass

def read_fan(_buff):
    _fan = [None]*2
    _fan[0] = (_buff[16] >> 4) & 0x01
    _fan[0] = (_buff[16] >> 4) & 0x01
    fan = AC_IR.bit_to_int(_fan, 2, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 4:
        _buff[0] = _buff[0] & 0xbf
        _buff[0] = _buff[0] | 0x00
    elif _swing == 0:
        _buff[0] = _buff[0] & 0xbf
        _buff[0] = _buff[0] | 0x00
    else:
        pass

def read_swing(_buff):
    _swing = [None]
    _swing[0] = (_buff[0] >> 6) & 0x01
    swing = AC_IR.bit_to_int(_swing, 1, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[0] = _buff[0] & 0xf8
    elif _mode == 4:
        _buff[0] = _buff[0] & 0xf8
        _buff[0] = _buff[0] | 0x04
    elif _mode == 1:
        _buff[0] = _buff[0] & 0xf8
        _buff[0] = _buff[0] | 0x01
    elif _mode == 2:
        _buff[0] = _buff[0] & 0xf8
        _buff[0] = _buff[0] | 0x02
    elif _mode == 3:
        _buff[0] = _buff[0] & 0x0f
        _buff[0] = _buff[0] | 0x03
    else:
        pass

def read_mode(_buff):
    _mode = [None] * 3
    _mode[0] = (_buff[0] >> 0) & 0x01
    _mode[1] = (_buff[0] >> 1) & 0x01
    _mode[2] = (_buff[0] >> 2) & 0x01
    mode = AC_IR.bit_to_int(_mode, 3, 0)
    return mode