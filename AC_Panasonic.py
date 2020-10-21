import AC_IR

def encode_panasonic(device):
    Panasonic_template = "40040720000000600220E004003930807F00000EE00000810000DD"
    PANASONIC_HDR_MARK_USER = "3500"
    PANASONIC_HDR_SPACE_USER = "1750"
    PANASONIC_BIT_MARK_USER = "435"
    PANASONIC_ONE_SPACE_USER = "1300"
    PANASONIC_ZERO_SPACE_USER = "435"

    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode

    if _swing == "auto":
        _swing = 15
    elif _swing == "1":
        _swing = 1
    elif _swing == "2":
        _swing = 2
    elif _swing == "3":
        _swing == 3
    elif _swing == "4":
        _swing = 4
    elif _swing == "5":
        _swing = 5
    else:
        _swing = 15
    
    if _mode == "auto":
        _mode = 0
    elif _mode == "heat":
        _mode = 4
    elif _mode == "cool":
        _mode == 3
    elif _mode == "dry":
        _mode = 2
    elif _mode == "fan_only":
        _mode = 6
    else:
        _mode = 0
    
    if _fan == "auto":
        _fan = 10
    elif _fan == "1":
        _fan = 3
    elif _fan == "2":
        _fan = 4
    elif _fan == "3":
        _fan = 5
    elif _fan == "4":
        _fan = 6
    elif _fan == "4":
        _fan = 7
    else:
        _fan = 10
    
    _buff = AC_IR.hex_string_to_byte_array(Panasonic_template)
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
        elif (_temp > 15) and (_temp < 31):
            _buff = change_temp(_buff, _temp)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    cs = check_sum(_buff, 8, 26)
    str_raw = ""
    str_bin = ""
    for i in range(0,8):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 1)
    for i in range(8, len(_buff) - 1):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
    str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 0)

    str_raw += PANASONIC_HDR_MARK_USER
    str_raw += ','
    str_raw += PANASONIC_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 8*8):
        str_raw += PANASONIC_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += PANASONIC_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += PANASONIC_ZERO_SPACE_USER
            str_raw += ','
    str_raw += PANASONIC_BIT_MARK_USER
    str_raw += ','
    str_raw += "9950"
    str_raw += ','
    str_raw += PANASONIC_HDR_MARK_USER
    str_raw += ','
    str_raw += PANASONIC_HDR_SPACE_USER
    str_raw += ','
    for i in range(8*8, 27*8):
        str_raw += PANASONIC_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += PANASONIC_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += PANASONIC_ZERO_SPACE_USER
            str_raw += ','
    str_raw += PANASONIC_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"
    
    str_raw = AC_IR.gz_base64_compress(str_raw)
    return str_raw



def switch_off(_buff):
    _buff[13] = _buff[13] & 0xf0
    _buff[13] = _buff[13] | 0x04
    state = 0
    return _buff

def switch_on(_buff):
    _buff[13] = _buff[13] & 0xf0
    _buff[13] = _buff[13] | 0x09
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 31):
        if temp == 30:
            pass
        else:
            _buff[14] = _buff[14] + 2
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 31):
        if temp == 16:
            pass
        else:
            _buff[14] = _buff[14] - 2
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 16
    __temp = _temp
    _buff[14] = _buff[14] & (~(0x0f << 1))
    _buff[14] = _buff[14] | (__temp << 1)
    return _buff

def read_temp(_buff):
    _temp = [None] * 4
    _temp[0] = (_buff[14] >> 1) & 0x01
    _temp[1] = (_buff[14] >> 2) & 0x01
    _temp[2] = (_buff[14] >> 3) & 0x01
    _temp[3] = (_buff[14] >> 4) & 0x01
    temp = 16 + AC_IR.bit_to_int(temp, 4, 0)
    return temp

def change_fan(_buff, _fan):
    if _fan == 10:
        _buff[16] = _buff[16] & 0x0f
        _buff[16] = _buff[16] | 0xa0
    elif _fan == 3:
        _buff[16] = _buff[16] & 0x0f
        _buff[16] = _buff[16] | 0x30
    elif _fan == 4:
        _buff[16] = _buff[16] & 0x0f
        _buff[16] = _buff[16] | 0x40
    elif _fan == 5:
        _buff[16] = _buff[16] & 0x0f
        _buff[16] = _buff[16] | 0x50
    elif _fan == 6:
        _buff[16] = _buff[16] & 0x0f
        _buff[16] = _buff[16] | 0x60
    elif _fan == 7:
        _buff[16] = _buff[16] & 0x0f
        _buff[16] = _buff[16] | 0x70
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = [None] * 4
    _fan[0] = (_buff[16] >> 4) & 0x01
    _fan[1] = (_buff[16] >> 5) & 0x01
    _fan[2] = (_buff[16] >> 6) & 0x01
    _fan[3] = (_buff[16] >> 7) & 0x01
    fan = AC_IR.bit_to_int(_fan, 4, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 15:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x0f
    elif _swing == 1:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x01
    elif _swing == 2:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x02
    elif _swing == 3:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x03
    elif _swing == 4:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x04
    elif _swing == 5:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x05
    else: 
        pass
    return _buff

def read_swing(_buff):
    _swing = [None] * 4
    _swing[0] = (_buff[16] >> 0) & 0x01
    _swing[1] = (_buff[16] >> 1) & 0x01
    _swing[2] = (_buff[16] >> 2) & 0x01
    _swing[3] = (_buff[16] >> 3) & 0x01
    swing = AC_IR.bit_to_int(_swing, 4, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[13] = _buff[13] & 0x0f
    elif _mode == 2:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x20
    elif _mode == 3:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x30
    elif _mode == 4:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x40
    elif _mode == 6:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x60
    else:
        pass
    return _buff

def read_mode(_buff):
    _mode = [None] * 4
    _mode[0] = (_buff[13] >> 4) & 0x01
    _mode[1] = (_buff[13] >> 5) & 0x01
    _mode[2] = (_buff[13] >> 6) & 0x01
    _mode[3] = (_buff[13] >> 7) & 0x01
    mode = AC_IR.bit_to_int(_mode, 4, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + _buf[i]
    _cs = _cs % 256
    return _cs