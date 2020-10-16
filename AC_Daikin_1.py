import AC_IR

def encode_daikin1(device):
    Daikin_template = "885BE40F0000004011DA2700003130007F000000000000C00000B2"
    DAIKIN_HDR_MARK_USER = "3400"
    DAIKIN_HDR_SPACE_USER = "1700"
    DAIKIN_BIT_MARK_USER = "420"
    DAIKIN_ONE_SPACE_USER = "1300"
    DAIKIN_ZERO_SPACE_USER = "460"

    if device.swing == 0:
        _swing = 15
    elif device.swing == 1:
        _swing = 0
    else:
        _swing = 15

    if device.mode == 0:
        _mode = 0
    elif device.mode == 1:
        _mode = 4
    elif device.mode == 2:
        _mode = 3
    elif device.mode == 3:
        _mode = 2
    elif device.mode == 4:
        _mode = 6
    else:
        _mode = 0

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

    _buff = AC_IR.hex_string_to_byte_array(Daikin_template)

    if device.mode == "off":
        _buff = switch_off(_buff)
        _buff = change_mode(_buff, _mode)
        if int(device.temp) == 0:
            _buff = temp_down(_buff)
        elif int(device.temp) == 1:
            _buff = temp_up(_buff)
        elif int(device.temp) == 2:
            pass
        elif ((int(device.temp) > 17) & (int(device.temp) < 33)):
            _buff = change_temp(_buff)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    else:
        _buff = switch_on(_buff)
        _buff = change_mode(_buff, _mode)
        if int(device.temp) == 0:
            _buff = temp_down(_buff)
        elif int(device.temp) == 1:
            _buff = temp_up(_buff)
        elif int(device.temp) == 2:
            pass
        elif ((int(device.temp) > 17) & (int(device.temp) < 33)):
            _buff = change_temp(_buff)
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    cs = check_sum(_buff, 8, 26)
    str_raw = ""
    str_bin = ""
    for i in range(0, 8):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 1)
    for i in range(8, len(_buff)):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
    str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 0)

    str_raw += DAIKIN_HDR_MARK_USER
    str_raw += ','
    str_raw += DAIKIN_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 8*8):
        str_raw += DAIKIN_BIT_MARK_USER
        str_raw += ','
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
    for i in range(8*8, 27*8):
        str_raw += DAIKIN_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += DAIKIN_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += DAIKIN_ZERO_SPACE_USER
            str_raw += ','
    str_raw += DAIKIN_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"
    str_raw = AC_IR.gz_base64_compress(str_raw)
    return str_raw

def switch_off(_buff):
    _buff[13] = _buff[13] & 0xf0
    _buff[13] = _buff[13] | 0x00
    return _buff

def switch_on(_buff):
    _buff[13] = _buff[13] & 0xf0
    _buff[13] = _buff[13] | 0x01
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if((temp > 17) and (temp < 33)):
        if(temp == 32):
            pass
        else:
            _buff[14] = _buff[14] - 2
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if ((temp > 17) and (temp < 33)):
        if temp == 18:
            pass
        else:
            _buff[14] = _buff[14] - 2
    return _buff

def change_temp(_buff, _temp):
    __temp = _temp
    _buff[14] = _buff[14] & (~(0x3f << 1))
    _buff[14] = _buff[14] | (_temp << 1)
    return _buff

def read_temp(_buff):
    _temp = []
    _temp.append((_buff[14] >> 1) & 0x01)
    _temp.append((_buff[14] >> 2) & 0x01)
    _temp.append((_buff[14] >> 3) & 0x01)
    _temp.append((_buff[14] >> 4) & 0x01)
    _temp.append((_buff[14] >> 5) & 0x01)
    _temp.append((_buff[14] >> 6) & 0x01)
    temp = AC_IR.bit_to_int(_temp, 6, 0)
    return AC_IR.bit_to_int(_temp, 6, 0)

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
    _fan = []
    _fan.append((_buff[16] >> 4) & 0x01)
    _fan.append((_buff[16] >> 5) & 0x01)
    _fan.append((_buff[16] >> 6) & 0x01)
    _fan.append((_buff[16] >> 7) & 0x01)

    fan = AC_IR.bit_to_int(_fan, 4, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 15:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x0f
    elif _swing == 0:
        _buff[16] = _buff[16] & 0xf0
    else:
        pass
    return _buff

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[13] = _buff[13] & 0x0f
    elif _mode == 2:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x20
    elif _mode == 3:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x20
    elif _mode == 4:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x20
    elif _mode == 6:
        _buff[13] = _buff[13] & 0x0f
        _buff[13] = _buff[13] | 0x20
    else: 
        pass
    return _buff

def read_fan(_buff):
    _fan = []
    _fan.append((_buff[16] << 4) & 0x01)
    _fan.append((_buff[16] << 5) & 0x01)
    _fan.append((_buff[16] << 6) & 0x01)
    _fan.append((_buff[16] << 7) & 0x01)
    fan = AC_IR.bit_to_int(_fan, 4, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 15:
        _buff[16] = _buff[16] & 0xf0
        _buff[16] = _buff[16] | 0x0f
    elif _swing == 0:
        _buff[16] = _buff[16] & 0x0f
    else:
        pass
    return _buff

def read_swing(_buff):
    _swing = []
    _swing.append((_buff[16] >> 0) & 0x01)
    _swing.append((_buff[16] >> 1) & 0x01)
    _swing.append((_buff[16] >> 2) & 0x01)
    _swing.append((_buff[16] >> 3) & 0x01)
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
    _mode = []
    _mode.append((_buff[13] >> 4) & 0x01)
    _mode.append((_buff[13] >> 5) & 0x01)
    _mode.append((_buff[13] >> 6) & 0x01)
    _mode.append((_buff[13] >> 7) & 0x01)
    mode = AC_IR.bit_to_int(_mode, 4, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + _buf[i]
    _cs = _cs % 256
    return _cs