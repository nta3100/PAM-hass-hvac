import AC_IR

def encode_midea(device):
    Midea_template_state_on = "B24D3FC040BF"
    Midea_template_state_off = "B24D7B84E01F"
    Midea_template_swing_on = "B24D6B94E01F"
    Midea_template_swing_set = "B24D0FF0E01F"
    MIDEA_HDR_MARK_USER = "4350"
    MIDEA_HDR_SPACE_USER = "4350"
    MIDEA_BIT_MARK_USER = "550"
    MIDEA_ONE_SPACE_USER = "1650"
    MIDEA_ZERO_SPACE_USER = "550"
    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode

    if _fan == "auto":
        _fan = 4
    elif _fan == "1":
        _fan = 6
    elif _fan == "2":
        _fan = 10
    elif _fan == "3":
        _fan = 12
    elif _fan == "3":
        _fan = 14
    else:
        _fan = 4
    
    if _swing == "set":
        _swing = 0
    elif _swing == "swing":
        _swing = 1
    elif _swing == "swing":
        _swing = 2
    else:
        _swing = 2
    
    if _mode == "auto":
        _mode = 8
    elif _mode == "heat":
        _mode = 12
    elif _mode == "cool":
        _mode = 0
    elif _mode == "dry":
        _mode = 4
    elif _mode == "fan_only":
        _mode = 4
    else:
        _mode = 8
    
    if device.mode != "off":
        if _swing == 0:
            _buff = AC_IR.hex_string_to_byte_array(Midea_template_swing_on)
        elif _swing == 1:
            _buff = AC_IR.hex_string_to_byte_array(Midea_template_swing_set)
        else:
            _buff = AC_IR.hex_string_to_byte_array(Midea_template_state_on)
            _buff = switch_on(_buff)
            _buff = change_mode(_buff, _mode)
            if _temp == 0:
                _buff = temp_down(_buff)
            elif _temp == 1:
                _buff = temp_up(_buff)
            elif _temp == 2:
                pass
            elif (_temp > 16) and (_temp < 32):
                _buff = change_temp(_buff, _temp)
            else:
                pass
            _buff = change_fan(_buff, _fan)
    else:
        _buff = AC_IR.hex_string_to_byte_array(Midea_template_state_off)
    if __debug__:
        print(~_buff[0])
        print(~_buff[3])
        print(~_buff[4])
    _buff[1] = _buff[0] ^ 0xff
    _buff[2] = _buff[3] ^ 0xff
    _buff[5] = _buff[4] ^ 0xff  
    
    str_raw = ""
    str_bin = ""
    for i in range(0, len(_buff)):
        str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 1)

    str_raw += MIDEA_HDR_MARK_USER
    str_raw += ','
    str_raw += MIDEA_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 6*8):
        str_raw += MIDEA_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += MIDEA_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += MIDEA_ZERO_SPACE_USER
            str_raw += ','
    str_raw += MIDEA_BIT_MARK_USER
    str_raw += ','
    if _swing == 1:
        str_raw += "0"
        str_raw = AC_IR.gz_base64_compress(str_raw)
        return str_raw
    str_raw += "5500"
    str_raw += ','
    str_raw += MIDEA_HDR_MARK_USER
    str_raw += ','
    str_raw += MIDEA_HDR_SPACE_USER
    str_raw += ','
    for i in range(0, 6*8):
        str_raw += MIDEA_BIT_MARK_USER
        str_raw += ','
        if str_bin[i] == '1':
            str_raw += MIDEA_ONE_SPACE_USER
            str_raw += ','
        else:
            str_raw += MIDEA_ZERO_SPACE_USER
            str_raw += ','
    str_raw += MIDEA_BIT_MARK_USER
    str_raw += ','
    str_raw += "0"
    str_raw = AC_IR.gz_base64_compress(str_raw)
    return str_raw
    

def switch_off(_buff):
    state = 0
    return _buff

def switch_on(_buff):
    state = 1
    return _buff

def temp_up(_buff):
    pass
    return _buff

def temp_down(_buff):
    pass
    return _buff

def change_temp(_buff, _temp):
    if _temp == 17:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x00
    elif _temp == 18:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x10
    elif _temp == 19:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x30
    elif _temp == 20:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x20
    elif _temp == 21:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x60
    elif _temp == 22:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x70
    elif _temp == 23:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x50
    elif _temp == 24:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x40
    elif _temp == 25:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0xc0
    elif _temp == 26:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0xd0
    elif _temp == 27:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x90
    elif _temp == 28:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0x80
    elif _temp == 29:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0xa0
    elif _temp == 30:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0xb0
    elif _temp == 31:
        _buff[4] = _buff[4] & 0x0f
        _buff[4] = _buff[4] | 0xe0
    else: 
        pass
    return _buff

def read_temp(_buff):
    return 0

def change_fan(_buff, _fan):
    if _fan == 4:
        _buff[3] = _buff[3] & 0x0f
        _buff[3] = _buff[3] | 0x00
    elif _fan == 6:
        _buff[3] = _buff[3] & 0x0f
        _buff[3] = _buff[3] | 0x60
    elif _fan == 10:
        _buff[3] = _buff[3] & 0x0f
        _buff[3] = _buff[3] | 0xa0
    elif _fan == 12:
        _buff[3] = _buff[3] & 0x0f
        _buff[3] = _buff[3] | 0xc0
    elif _fan == 14:
        _buff[3] = _buff[3] & 0x0f
        _buff[3] = _buff[3] | 0xe0
    else:
        pass
    return _buff

def read_fan(_buff):
    return 0

def change_swing(_buff, _swing):
    return _buff

def read_swing(_buff, _swing):
    pass

def change_mode(_buff, _mode):
    if _mode == 8:
        _buff[4] = _buff[4] & 0xf0
        _buff[4] = _buff[4] | 0x08
    elif _mode == 12:
        _buff[4] = _buff[4] & 0xf0
        _buff[4] = _buff[4] | 0x0c
    elif _mode == 0:
        _buff[4] = _buff[4] & 0xf0
        _buff[4] = _buff[4] | 0x00
    elif _mode == 4:
        _buff[4] = _buff[4] & 0xf0
        _buff[4] = _buff[4] | 0x04
    else:
        pass
    return _buff

def read_mode(_buff):
    return 0