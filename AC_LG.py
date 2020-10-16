import AC_IR

def encode_lg(device):
    LG_Test = "88100001"
    LG_template_on = "88089405"
    LG_template_off = "88C00501"
    LG_template_swing_on = "88100001"
    LG_HDR_MARK_USER = "8300"
    LG_HDR_SPACE_USER = "4190"
    LG_BIT_MARK_USER = "520"
    LG_ONE_SPACE_USER = "1600"
    LG_ZERO_SPACE_USER = "520"
    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode
    
    if _mode == "cool":
        _mode = 4
    elif _mode == "auto":
        _mode = 0
    elif _mode == "dry":
        _mode = 1
    else:
        _mode = 4
    
    if _fan == "auto":
        _fan = 5
    elif _fan == "1":
        _fan = 0
    elif _fan == "3":
        _fan = 2
    elif _fan == "2":
        _fan = 4
    else:
        _fan = 5
    
    if _swing == 0:
        _swing = 0
    elif _swing == -1:
        _swing = 1
    else:
        _swing = 1

    _buff = AC_IR.hex_string_to_byte_array(LG_template_on)
    if device.mode == "off":
        _buff = AC_IR.hex_string_to_byte_array(LG_template_off)
    else:
        if _swing == 0:
            _buff = AC_IR.hex_string_to_byte_array(LG_template_swing_on)
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
    
    str_raw = ""
    str_bin = ""
    cs = check_sum(_buff, 0, 3)
    for i in range(0, len(_buff) - 1):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 1)
    str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 1)
    
    _str = ""
    _str += str_bin[0: len(str_bin) - 8]
    _str += str_bin[len(str_bin) - 4: len(str_bin)]
    str_bin = _str
    
    str_raw += LG_HDR_MARK_USER
    str_raw += ','
    str_raw += LG_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 28):
        str_raw += LG_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += LG_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += LG_ZERO_SPACE_USER
            str_raw += ','
    str_raw += LG_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"
    str_raw = AC_IR.gz_base64_compress(str_raw)
    return str_raw

def switch_off(_buff):
    state = 0

def switch_on(_buff):
    _buff[1] = _buff[1] & 0x00
    _buff[1] = _buff[1] | 0x00
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 31):
        if temp == 30:
            pass
        else:
            _buff[2] = _buff[2] + 16
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 31):
        if temp == 16:
            pass
        else:
            _buff[2] = _buff[2] - 16
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 15
    __temp = _temp
    _buff[2] = _buff[2] & 0x0f
    _buff[2] = _buff[2] | (__temp << 4)
    return _buff

def read_temp(_buff):
    _temp = [None] * 4
    _temp[0] = (_buff[2] >> 4) & 0x01
    _temp[1] = (_buff[2] >> 5) & 0x01
    _temp[2] = (_buff[2] >> 6) & 0x01
    _temp[3] = (_buff[2] >> 7) & 0x01
    temp = 15 + AC_IR.bit_to_int(_temp, 4, 0)
    return temp

def change_fan(_buff, _fan):
    if _fan == 5:
        _buff[2] = _buff[2] & 0xf8
        _buff[2] = _buff[2] | 0x05
    elif _fan == 0:
        _buff[2] = _buff[2] & 0xf8
        _buff[2] = _buff[2] | 0x00
    elif _fan == 4:
        _buff[2] = _buff[2] & 0xf8
        _buff[2] = _buff[2] | 0x04
    elif _fan == 2:
        _buff[2] = _buff[2] & 0xf8
        _buff[2] = _buff[2] | 0x02
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = [None] * 3
    _fan[0] = (_buff[2] >> 0) & 0x01
    _fan[1] = (_buff[2] >> 1) & 0x01
    _fan[2] = (_buff[2] >> 2) & 0x01
    fan = AC_IR.bit_to_int(_fan, 3, 0)
    return fan

def change_swing(_buff, _swing):
    pass

def read_swing(_buff):
    return 1

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x00
    elif _mode == 1:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x01
    elif _mode == 4:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x04
    else:
        pass
    return _buff

def read_mode(_buff):
    _mode = [None] * 3
    _mode[0] = (_buff[1] >> 0) & 0x01
    _mode[1] = (_buff[1] >> 1) & 0x01
    _mode[2] = (_buff[1] >> 2) & 0x01
    mode = AC_IR.bit_to_int(_mode, 3, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        half_low = _buf[i] & 0x0f
        half_high = (_buf[i] & 0xf0) >> 4
        _cs = _cs + half_low
        _cs = _cs + half_high
    _cs = _cs % 16
    return _cs