import AC_IR_python

def encode_sumikura(device):
    Sumikura_template = "56740000210600000C000C2529114B"
    SUMIKURA_HDR_MARK_USER = "8340"
    SUMIKURA_HDR_SPACE_USER = "4120"
    SUMIKURA_BIT_MARK_USER = "550"
    SUMIKURA_ONE_SPACE_USER = "1600"
    SUMIKURA_ZERO_SPACE_USER = "520"
    state = 1

    if device.swing == "auto":
        _swing = 26
    elif device.swing == "1":
        _swing = 6
    elif device.swing == "2":
        _swing = 10
    elif device.swing == "3":
        _swing = 14
    elif device.swing == "4":
        _swing = 18
    elif device.swing == "5":
        _swing = 22
    else:
        _swing = 26

    if device.mode == "cool":
        _mode = 2
    elif device.mode == "heat":
        _mode = 3
    elif device.mode == "fan_only":
        _mode = 5
    else: 
        _mode = 2

    if device.fan == "auto":
        _fan = 0
    elif device.fan == "1":
        _fan = 2
    elif device.fan == "2":
        _fan = 3
    elif device.fan == "3":
        _fan = 1
    else: 
        _fan = 0

    str_raw = ""
    str_bin = ""

    _buff = AC_IR_python.hex_string_to_byte_array(Sumikura_template)
    if device.mode == "off":
        _buff = switch_off(_buff)
        _buff = change_mode(_buff, _mode)
        if (int)(device.temp) == 0:
            _buff = temp_down(_buff)
        elif (int)(device.temp) == 1:
            _buff = temp_up(_buff)
        elif (int)(device.temp) == 2:
            pass
        elif (int(device.temp) > 15) and (int(device.temp) < 33):
            _buff = change_temp(_buff, int(device.temp))
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
        elif ((int(device.temp) > 15) and (int(device.temp) < 32)):
            _buff = change_temp(_buff, int(device.temp))
        else:
            pass
        _buff = change_fan(_buff, _fan)
        _buff = change_swing(_buff, _swing)
    cs = check_sum(_buff, 0, len(_buff) - 1)
    _buff_temp = _buff
    _buff_temp.pop(len(_buff) - 1)
    str_bin = AC_IR_python.byte_to_string(_buff_temp, 0)
    str_bin += AC_IR_python.byte_to_string(cs.to_bytes(1, 'big'), 0)
    str_raw += SUMIKURA_HDR_MARK_USER
    str_raw += ','
    str_raw += SUMIKURA_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 15*8):
        str_raw += SUMIKURA_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += SUMIKURA_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += SUMIKURA_ZERO_SPACE_USER
            str_raw += ','
    str_raw += SUMIKURA_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"
    str_raw = AC_IR_python.gz_base64_compress(str_raw)
    return str_raw

def switch_off(_buff):
    _buff[5] = _buff[5] & 0x3D
    _buff[5] = _buff[5] | 0xC0
    state = 0
    return _buff

def switch_on(_buff):
    _buff[5] = _buff[5] & 0x3D
    _buff[5] = _buff[5] | 0x00
    state = 1
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if ((temp>15)and(temp<33)):
        if temp == 32:
            pass
        else:
            _buff[1] = _buff[1] + 1
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if((temp>15)and(temp<33)):
        if temp == 16:
            pass
        else:
            _buff[1] = _buff[1] - 1
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 4
    __temp = _temp
    _buff[1] = _buff[1]&(~0x1F)
    _buff[1] = _buff[1]|__temp
    return _buff

def read_temp(_buff):
    _temp = []
    _temp[0] = (int)((_buff[16] >> 1) & 0x01)
    _temp[1] = (int)((_buff[16] >> 2) & 0x01)
    _temp[2] = (int)((_buff[16] >> 3) & 0x01)
    _temp[3] = (int)((_buff[16] >> 4) & 0x01)
    _temp[4] = (int)((_buff[16] >> 5) & 0x01)
    temp = AC_IR_python.bit_to_int(_temp, 5, 0)
    temp = temp + 10
    return temp

def change_fan(_buff, _fan):
    if _fan == 0:
        _buff[4] = _buff[4] & 0xFC
        _buff[4] = _buff[4] | 0x00
    elif _fan == 2:
        _buff[4] = _buff[4] & 0xFC
        _buff[4] = _buff[4] | 0x02
    elif _fan == 3:
        _buff[4] = _buff[4] & 0xFC
        _buff[4] = _buff[4] | 0x03
    elif _fan == 1:
        _buff[4] = _buff[4] & 0xFC
        _buff[4] = _buff[4] | 0x01
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = []
    _fan[0] = (int)((_buff[17] >> 0) & 0x01)
    _fan[1] = (int)((_buff[17] >> 1) & 0x01)
    _fan[2] = (int)((_buff[17] >> 2) & 0x01)
    _fan[3] = (int)((_buff[17] >> 3) & 0x01)
    fan = AC_IR_python.bit_to_int(_fan, 4, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 26:
        _buff[5] = _buff[5] & 0xE0
        _buff[5] = _buff[5] | 0x1A
    elif _swing == 6:
        _buff[5] = _buff[5] & 0xE0
        _buff[5] = _buff[5] | 0x06
    elif _swing == 10:
        _buff[5] = _buff[5] & 0xE0
        _buff[5] = _buff[5] | 0x0A
    elif _swing == 14:
        _buff[5] = _buff[5] & 0xE0
        _buff[5] = _buff[5] | 0x0E
    elif _swing == 18:
        _buff[5] = _buff[5] & 0xE0
        _buff[5] = _buff[5] | 0x12
    elif _swing == 22:
        _buff[5] = _buff[5] & 0xE0
        _buff[5] = _buff[5] | 0x16
    else: 
        pass
    return _buff

def read_swing(_buff):
    _swing = []
    _swing[0] = (int)((_buff[13] >> 4) & 0x01)
    _swing[1] = (int)((_buff[13] >> 5) & 0x01)
    _swing[2] = (int)((_buff[13] >> 6) & 0x01)
    _swing[3] = (int)((_buff[13] >> 7) & 0x01)
    swing = AC_IR_python.bit_to_int(_swing, 4, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 2:
        _buff[4] = _buff[4] & 0x0F
        _buff[4] = _buff[4] | 0x20
    elif _mode == 3:
        _buff[4] = _buff[4] & 0x0F
        _buff[4] = _buff[4] | 0x30
    elif _mode == 5:
        _buff[4] = _buff[4] & 0x0F
        _buff[4] = _buff[4] | 0x50
    return _buff

def read_mode(_buff):
    _mode = []
    _mode[0] = ((_buff[12] >> 4) & 0x01)
    _mode[1] = ((_buff[12] >> 5) & 0x01)
    _mode[2] = ((_buff[12] >> 6) & 0x01)
    mode = AC_IR_python.bit_to_int(_mode, 3, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        half_low = _buf[i] & 0x0F
        half_high = (_buf[i] & 0xF0) >> 4
        _cs = _cs + half_low
        _cs = _cs + half_high
    _cs = _cs % 256
    return _cs