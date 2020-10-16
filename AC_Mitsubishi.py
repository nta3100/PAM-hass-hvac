import AC_IR

def encode_mitsubishi(device):
    Mitsubishi_template = "23CB260100A403070500000000C8"
    MITSUBISHI_HDR_MARK_USER = "3450"
    MITSUBISHI_HDR_SPACE_USER = "1670"
    MITSUBISHI_BIT_MARK_USER = "460"
    MITSUBISHI_ONE_SPACE_USER = "1180"
    MITSUBISHI_ZERO_SPACE_USER = "360"

    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode

    if _mode == "cool":
        _mode = 8
    elif _mode == "heat":
        _mode = 3
    elif _mode == "auto":
        _mode = 2
    elif _mode == "dry":
        _mode = 7
    else: 
        _mode = 8
    
    if _fan == "auto":
        _fan = 0
    elif _fan == "1":
        _fan = 2
    elif _fan == "2":
        _fan = 3
    elif _fan == "3":
        _fan = 5
    else:
        _fan = 0
    
    if _swing == "auto":
        _swing = 0
    elif _swing == "1":
        _swing = 1
    elif _swing == "2":
        _swing = 2
    elif _swing == "3":
        _swing = 3
    elif _swing == "4":
        _swing = 4
    elif _swing == "5":
        _swing = 5

    _buff = AC_IR.hex_string_to_byte_array(Mitsubishi_template)
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
        _buff = change_fan(_buff, _swing)
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
        _buff = change_fan(_buff, _swing)
        _buff = change_swing(_buff, _swing)
    cs = check_sum(_buff, 0, 13)
    
    str_raw = ""
    str_bin = ""
    for i in range(0, len(_buff) - 1):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
    str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 0)

    str_raw += MITSUBISHI_HDR_MARK_USER
    str_raw += ','
    str_raw += MITSUBISHI_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 14*8):
        str_raw += MITSUBISHI_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += MITSUBISHI_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += MITSUBISHI_ZERO_SPACE_USER
            str_raw += ','
    str_raw += MITSUBISHI_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"

    str_raw = AC_IR.gz_base64_compress(str_raw)
    return str_raw


def switch_off(_buff):
    _buff[5] = _buff[5] & 0xfb
    _buff[5] = _buff[5] | 0x00
    state = 0
    return _buff

def switch_on(_buff):
    _buff[5] = _buff[5] & 0xfb
    _buff[5] = _buff[5] | 0x04
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 32):
        if temp == 31:
            pass
        else:
            _buff[7] = _buff[7] - 1
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 15) and (temp < 32):
        if temp == 16:
            pass
        else: 
            _buff[7] = _buff[7] + 1
    return _buff

def change_temp(_buff, _temp):
    _temp = 31 - _temp
    __temp = _temp
    _buff[7] = _buff[7] & 0xf0
    _buff[7] = _buff[7] | __temp
    return _buff

def read_temp(_buff):
    _temp = [None] * 4
    _temp[0] = (_buff[7] >> 0) & 0x01
    _temp[1] = (_buff[7] >> 1) & 0x01
    _temp[2] = (_buff[7] >> 2) & 0x01
    _temp[3] = (_buff[7] >> 3) & 0x01
    temp = 31 - AC_IR.bit_to_int(_temp, 4, 0)
    return _temp

def change_fan(_buff, _fan):
    if _fan == 0:
        _buff[8] = _buff[8] & 0xf8
        _buff[8] = _buff[8] | 0x00
    elif _fan == 2:
        _buff[8] = _buff[8] & 0xf8
        _buff[8] = _buff[8] | 0x02
    elif _fan == 3:
        _buff[8] = _buff[8] & 0xf8
        _buff[8] = _buff[8] | 0x03
    elif _fan == 5:
        _buff[8] = _buff[8] & 0xf8
        _buff[8] = _buff[8] | 0x05
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = [None] * 3
    _fan[0] = (_buff[8] >> 0) & 0x01
    _fan[1] = (_buff[8] >> 1) & 0x01
    _fan[2] = (_buff[8] >> 2) & 0x01
    fan = AC_IR.bit_to_int(_fan, 3, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 0:
        _buff[8] = _buff[8] & 0xc7
        _buff[8] = _buff[8] | 0x00
    elif _swing == 1:
        _buff[8] = _buff[8] & 0xc7
        _buff[8] = _buff[8] | 0x08
    elif _swing == 2:
        _buff[8] = _buff[8] & 0xc7
        _buff[8] = _buff[8] | 0x10
    elif _swing == 3:
        _buff[8] = _buff[8] & 0xc7
        _buff[8] = _buff[8] | 0x18
    elif _swing == 4:
        _buff[8] = _buff[8] & 0xc7
        _buff[8] = _buff[8] | 0x20
    elif _swing == 5:
        _buff[8] = _buff[8] & 0xc7
        _buff[8] = _buff[8] | 0x28
    else:
        pass

def read_swing(_buff):
    _swing = [None] * 3
    _swing[0] = (_buff[8] >> 3) & 0x01
    _swing[1] = (_buff[8] >> 4) & 0x01
    _swing[2] = (_buff[8] >> 5) & 0x01
    swing = AC_IR.bit_to_int(_swing, 3, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 8:
        _buff[6] = _buff[6] & 0xf0
        _buff[6] = _buff[6] | 0x08
    elif _mode == 2:
        _buff[6] = _buff[6] & 0xf0
        _buff[6] = _buff[6] | 0x02
    elif _mode == 7:
        _buff[6] = _buff[6] & 0xf0
        _buff[6] = _buff[6] | 0x07
    elif _mode == 3:
        _buff[6] = _buff[6] & 0xf0
        _buff[6] = _buff[6] | 0x03
    else:
        pass

def read_mode(_buff):
    _mode = [None] * 4
    _mode[0] = (_buff[6] >> 0) & 0x01
    _mode[1] = (_buff[6] >> 1) & 0x01
    _mode[2] = (_buff[6] >> 2) & 0x01
    _mode[3] = (_buff[6] >> 3) & 0x01
    mode = AC_IR.bit_to_int(_mode, 4, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + buf[i]
    _cs = _cs % 256
    return _cs