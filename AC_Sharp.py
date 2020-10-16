import AC_IR

def encode_sharp(device):
    Sharp_template = ""
    SHARP_HDR_MARK_USER ="3830"
    SHARP_HDR_SPACE_USER = "1820"
    SHARP_BIT_MARK_USER = "520"
    SHARP_ONE_SPACE_USER = "1330"
    SHARP_ZERO_SPACE_USER = "400"

    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing 
    _fan = device.fan
    _mode = device.mode

    if _fan == 0:
        _fan = 2
    elif _fan == 1:
        _fan = 3
    elif _fan == 2:
        _fan = 5
    elif _fan == 3:
        _fan =7
    
    if _swing == 0:
        _swing = 7
    elif _swing == -1:
        _swing = 1
    else:
        _swing = 1
    
    _buff = AC_IR.hex_string_to_byte_array(Sharp_template)





def switch_off(_buff):
    _buff[5] = _buff[5] & 0xcf
    _buff[5] = _buff[5] | 0x20
    state = 0
    return _buff

def switch_on(_buff):
    _buff[5] = _buff[5] & 0xcf
    _buff[5] = _buff[5] | 0x10
    state = 1
    return _buff

def switch_active(_buff):
    _buff[5] = _buff[5] & 0xf3
    _buff[5] = _buff[5] | 0x30
    state = 2
    return _buff

def temp_up(_buff):
    temp = read_temp(_buff)
    if (temp > 17) and (temp < 33):
        if temp == 32:
            pass
        else:
            _buff[4] = _buff[4] + 1
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if (temp > 17) and (temp < 33):
        if temp == 18:
            pass
        else:
            _buff[4] = _buff[4] - 1
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 17
    __temp = _temp
    _buff[4] = _buff[4] & 0xf0
    _buff[4] = _buff[4] | __temp
    return _buff

def read_temp(_buff):
    _temp = [None] * 4
    _temp[0] = (_buff[4] >> 0) & 0x01
    _temp[1] = (_buff[4] >> 1) & 0x01
    _temp[2] = (_buff[4] >> 2) & 0x01
    _temp[3] = (_buff[4] >> 3) & 0x01
    temp = 17 + AC_IR.bit_to_int(_temp , 4, 0)
    return temp

def change_fan(_buff, _fan):
    if _fan == 2:
        _buff[6] = _buff[6] & 0x8f
        _buff[6] = _buff[6] | 0x20
    elif _fan == 3:
        _buff[6] = _buff[6] & 0x8f
        _buff[6] = _buff[6] & 0x30
    elif _fan == 5:
        _buff[6] = _buff[6] & 0x8f
        _buff[6] = _buff[6] & 0x50
    elif _fan == 7:
        _buff[6] = _buff[6] & 0x8f
        _buff[6] = _buff[6] & 0x70
    else:
        pass
    return _buff

def read_fan(_buff):
    _fan = [None] * 3
    _fan[0] = (_buff[6] >> 4) & 0x01
    _fan[1] = (_buff[6] >> 5) & 0x01
    _fan[2] = (_buff[6] >> 6) & 0x01
    fan = AC_IR.bit_to_int(_fan, 3, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 7:
        _buff[8] = _buff[8] & 0xf8
        _buff[8] = _buff[8] | 0x07
    else:
        pass
    return _buff

def read_swing(_buff):
    _swing = [None] * 3
    _swing[0] = (_buff[8] >> 0) & 0x01
    _swing[1] = (_buff[8] >> 1) & 0x01
    _swing[2] = (_buff[8] >> 2) & 0x01
    swing = AC_IR.bit_to_int(_swing, 3, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[6] = _buff[6] & 0xf8
    elif _mode == 3:
        _buff[6] = _buff[6] & 0xf8
        _buff[6] = _buff[6] | 0x03
    elif _mode == 2:
        _buff[6] = _buff[6] & 0xf8
        _buff[6] = _buff[6] | 0x02
    elif _mode == 1:
        _buff[6] = _buff[6] & 0xf8
        _buff[6] = _buff[6] | 0x01
    elif _mode == 4:
        _buff[6] = _buff[6] & 0xf8
        _buff[6] = _buff[6] | 0x04
    else:
        pass
    return _buff

def read_mode(_buff):
    _mode = [None] * 3
    _mode[0] = (_buff[6] >> 0) & 0x01
    _mode[1] = (_buff[6] >> 1) & 0x01
    _mode[2] = (_buff[6] >> 2) & 0x01
    mode = AC_IR.bit_to_int(_mode, 3, 0)
    return mode

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs ^ _buf[i]
    _ts = 0x01
    _cs ^= _ts & 0x0f
    _cs ^= (_cs >> 4)
    _cs &= 0x0f
    _ts |= (_cs << 4)
    return _ts