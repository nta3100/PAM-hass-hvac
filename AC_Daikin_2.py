#! /usr/bin/python3

import AC_IR

def encode_daikin_2(device):
    Daikin_template = "11DA27F00D000F11DA2700D3313100001C070872"
    DAIKIN_HDR_MARK_USER = "5000"
    DAIKIN_HDR_SPACE_USER = "2100"
    DAIKIN_BIT_MARK_USER = "360"
    DAIKIN_ONE_SPACE_USER = "1725"
    DAIKIN_ZERO_SPACE_USER = "670"
    state = 1

    if device.swing == 0:
        _swing = 15
    elif device.swing == 1:
        _swing = 1
    elif device.swing == 2:
        _swing = 2
    elif device.swing == 3: 
        _swing = 3
    elif device.swing == 4:
        _swing = 4
    elif device.swing == 5:
        _swing = 5
    else:
        _swing = 15
    
    if device.mode == 1:
        _mode = 4
    elif device.mode == 2:
        _mode = 3
    elif device.mode == 3:
        _mode = 2
    elif device.mode == 4:
        _mode = 6
    else:
        _mode = 4
    
    if device.fan == 0:
        _fan = 10
    elif device.fan == 1:
        _fan = 3
    elif device.fan == 2:
        _fan = 4
    elif device.fan == 3:
        _fan = 5
    elif device.fan == 4:
        _fan = 6
    elif device.fan == 5:
        _fan = 7
    else:
        _fan = 10
    
    _temp = (int)(device.temp)

    _buff = AC_IR.hex_string_to_byte_array(Daikin_template)
    if device.mode == "off":
        _buff = switch_off(_buff)
        _buff = change_mode(_buff, _mode)
        if _temp == 0:
            _buff = temp_down(_buff)
        elif _temp == 1:
            _buff = temp_up(_buff)
        elif _temp == 2:
            pass
        elif (_temp > 17) and (_temp < 33):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _mode)
        _buff = change_swing(_buff, _swing)
    else:
        _buff = switch_on(_buff)
        _buff = change_mode(_buff)
        if _temp == 0:
            _buff = temp_down(_buff)
        elif _temp == 1:
            _buff = temp_up(_buff)
        elif _temp == 2:
            pass
        elif (_temp > 17) and (_temp < 33):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    
    cs = check_sum(_buff, 7, 19)
    str_raw = ""
    str_bin = ""
    for i in range(0, len(_buff) - 1):
        str_bin += AC_IR.byte_to_string(_buff[i].tobytes(1, 'big'), 0)
    str_bin += AC_IR.byte_to_string(cs.tobytes(1, 'big'), 0)

    str_raw += DAIKIN_HDR_MARK_USER
    str_raw += ','
    str_raw += DAIKIN_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 7*8):
        str_raw += DAIKIN_BIT_MARK_USER
        str_bin += ','
        if str_bin[i] == '1':
            str_raw += DAIKIN_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += DAIKIN_ZERO_SPACE_USER
            str_raw += ','
        str_raw += DAIKIN_BIT_MARK_USER
        str_raw += ','
        str_raw += "29500"
        str_raw += ','
        str_raw += DAIKIN_HDR_MARK_USER
        str_raw += ','
        str_raw += DAIKIN_HDR_SPACE_USER
        str_raw += ','
        for i in range(7*8, 20*8):
            str_raw += DAIKIN_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += DAIKIN_ONE_SPACE_USER
                str_raw += ','
            else:
                str_bin += DAIKIN_ZERO_SPACE_USER
                str_bin += ','
        str_raw += DAIKIN_BIT_MARK_USER
        str_raw += ','
        str_raw += "0"
        str_raw = AC_IR.gz_base64_compress(str_raw)
        return str_raw


def switch_off(_buff):
    _buff[12] = _buff[12] & 0xfe
    _buff[12] = _buff[12] | 0x00
    state = 0
    return _buff

def switch_on(_buff):
    _buff[12] = _buff[12] & 0xfe
    _buff[12] = _buff[12] | 0x01
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 17) and (temp < 33):
        if temp == 32:
            pass
        else:
            _buff[16] = _buff[16] + 2
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 17) and (temp < 16):
        if temp == 18:
            pass
        else:
            _buff[16] = _buff[16] - 2

def change_temp(_buff, _temp):
    _temp = _temp - 10
    __temp = _temp
    _buff[16] = _buff[16] & (~(0x1f << 1))
    _buff[16] = _buff[16] | (__temp << 1)
    return _buff

def read_temp(_buff):
    _temp = []
    _temp.append((_buff[16] >> 1) & 0x01)
    _temp.append((_buff[16] >> 2) & 0x01)
    _temp.append((_buff[16] >> 3) & 0x01)
    _temp.append((_buff[16] >> 4) & 0x01)
    _temp.append((_buff[16] >> 5) & 0x01)
    temp = AC_IR.bit_to_int(_temp, 5, 0)
    temp = temp + 10
    return temp

def change_fan(_buff, _fan):
    if _fan == 10:
        _buff[17] = _buff[17] & 0xf0
        _buff[17] = _buff[17] | 0x0a
    elif _fan == 3:
        _buff[17] = _buff[17] & 0xf0
        _buff[17] = _buff[17] | 0x03
    elif _fan == 4:
        _buff[17] = _buff[17] & 0xf0
        _buff[17] = _buff[17] | 0x04
    elif _fan == 5:
        _buff[17] = _buff[17] & 0xf0
        _buff[17] = _buff[17] | 0x05
    elif _fan == 6:
        _buff[17] = _buff[17] & 0xf0
        _buff[17] = _buff[17] | 0x06
    elif _fan == 7:
        _buff[17] = _buff[17] & 0xf0
        _buff[17] = _buff[17] | 0x07
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = []
    _fan.append((_buff[17] >> 0) & 0x01)
    _fan.append((_buff[17] >> 1) & 0x01)
    _fan.append((_buff[17] >> 2) & 0x01)
    _fan.append((_buff[17] >> 3) & 0x01)
    fan = AC_IR.bit_to_int(_fan, 4, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 15:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0xf0
    elif _swing == 1:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x10
    elif _swing == 2:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x20
    elif _swing == 3:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x30
    elif _swing == 4:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x40
    elif _swing == 5:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x50
    else:
        pass
    return _buff

def read_swing(_buff):
    _swing = []
    _swing.append((_buff[13] >> 4) & 0x01)
    _swing.append((_buff[13] >> 5) & 0x01)
    _swing.append((_buff[13] >> 6) & 0x01)
    _swing.append((_buff[13] >> 7) & 0x01)
    swing = AC_IR.bit_to_int(_swing, 4, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 2:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x02
    elif _mode == 3:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x30
    elif _mode == 4:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x40
    elif _mode == 6:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x60
    else:
        pass
    return _buff

def read_mode(_buff):
    _mode = [None] * 3
    _mode[0] = (_buff[12] >> 4) & 0x01
    _mode[1] = (_buff[12] >> 5) & 0x01
    _mode[2] = (_buff[12] >> 6) & 0x01
    mode = AC_IR.bit_to_int(_mode, 3, 0)
    return _mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + buf[i]
    _cs = _cs%256
    return _cs
