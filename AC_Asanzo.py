#! /usr/bin/python3

import AC_IR

def encode_asanzo(device):
    Asanzo_template = ""
    ASANZO_HDR_MARK_USER = "8900"
    ASANZO_HDR_SPACE_USER = "4450"
    ASANZO_BIT_MARK_USER = "520"
    ASANZO_ONE_SPACE_USER = "1720"
    ASANZO_ZERO_SPACE_USER = "580"
    state = 1

    if device.swing == 0:
        _swing = 7
    elif device.swing == 1:
        _swing = 0
    else:
        _swing = 7
    
    if device.mode == 0:
        _mode = 0
    elif device.mode == 1:
        _mode = 4
    elif device.mode == 2:
        _mode = 1
    elif device.mode == 3:
        _mode = 2
    elif device.mode == 4:
        _mode = 6
    else: 
        _mode = 0
    
    if device.fan == 0:
        _fan = 5
    elif device.fan == 1:
        _fan = 3
    elif device.fan == 2:
        _fan = 2
    elif device.fan == 3:
        _fan = 1
    else:
        _fan = 5
    
    _temp = (int)(device.temp)

    _buff = AC_IR.hex_string_to_byte_array(Asanzo_template)
    if device.mode == "off":
        _buff = switch_off(_buff)
        _buff = change_mode(_buff, _mode)
        if (int)(_temp) == 0:
            _buff = temp_down(_buff)
        elif (int)(_temp) == 1:
            _buff = temp_up(_buff)
        elif (int)(_temp) == 2:
            pass
        elif ((int)(_temp) > 15) and ((int)(_temp) < 33):
            _buff = change_temp(_buff, (int)(_temp))
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    else:
        switch_on(_buff)
        change_mode(_buff, _mode)
        if (int)(_temp) == 0:
            _buff = temp_down(_buff)
        elif (int)(_temp) == 1:
            _buff = temp_up(_buff)
        elif (int)(_temp) == 2:
            pass
        elif (_temp > 15) and (_temp < 33):
            change_temp(_buff, _temp)
        else:
            pass
        change_fan(_buff, _fan)
        change_swing(_buff, _swing)
    cs = check_sum(_buff, 0 , 12)
    str_raw = ""
    str_bin = ""
    for i in range(0, len(_buff)):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
    str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 0)
    
    str_raw += ASANZO_HDR_MARK_USER
    str_raw += ','
    str_raw += ASANZO_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 13*8):
        str_raw += ASANZO_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += ASANZO_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += ASANZO_ZERO_SPACE_USER
            str_raw += ','
    str_raw += ASANZO_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"

    str_raw = AC_IR.gz_base64_compress(str_raw)

    return str_raw

def switch_off(_buff):
    _buff[9] = _buff[9] & 0xdf
    _buff[9] = _buff[9] | 0x40
    state = 0
    return _buff

def switch_on(_buff):
    _buff[9] = _buff[9] & 0xdf
    _buff[9] = _buff[9] | 0x00
    state = 1
    return _buff

def temp_up(_buff):
    pass

def temp_down(_buff):
    pass

def change_temp(_buff, _temp):
    _temp = _temp - 8
    __temp = _temp
    _buff[1] = _buff[1] & (~(0x3f << 3))
    _buff[1] = _buff[1] | (__temp << 3)
    return _buff

def change_fan(_buff, _fan):
    if _fan == 5:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0xa0
    elif _fan == 3:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0x60
    elif _fan == 2:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0x40
    elif _fan == 1:
        _buff[4] = _buff[4] & 0x1f
        _buff[4] = _buff[4] | 0x20
    else:
        pass
    return _buff

def change_swing(_buff, _swing):
    if _swing == 7:
        _buff[1] = _buff[1] & 0xf8
        _buff[1] = _buff[1] | 0x07
    elif _swing == 0:
        _buff[1] = _buff[1] & 0xf8
    else:
        pass
    return _buff

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[6] = _buff[6] & 0x1f
    elif _mode == 1:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0x20
    elif _mode == 2:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0x40
    elif _mode == 4:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0x80
    elif _mode == 6:
        _buff[6] = _buff[6] & 0x1f
        _buff[6] = _buff[6] | 0xc0
    else:
        pass
    return _buff

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + _buf[i]
    _cs = _cs % 256
    return _cs