import AC_IR

def encode_general(device):
    General_template_state_test = "1463001010FE0930700210000000202E"
    General_template_state_on = "1463001010FE0930910101000000201D"
    General_template_state_off = "146300101002FD"
    General_template_swing_on = "14630010106C93"
    GENERAL_HDR_MARK_USER = "3250"
    GENERAL_HDR_SPACE_USER = "1600"
    GENERAL_BIT_MARK_USER = "400"
    GENERAL_ONE_SPACE_USER = "1200"
    GENERAL_ZERO_SPACE_USER = "400"
    state = 1
    _temp = (int)(device.temp)
    _swing = device.swing
    _fan = device.fan
    _mode = device.mode

    if _mode == "auto":
        _mode = 0
    elif _mode == "heat":
        _mode = 4
    elif _mode == "cool":
        _mode = 1
    elif _mode == "dry":
        _mode = 2
    elif _mode == "fan_only":
        _mode = 3
    else:
        pass

    if _fan == "auto":
        _fan = 0
    elif _fan == "1":
        _fan = 4
    elif _fan == "2":
        _fan = 3
    elif _fan == "3":
        _fan = 2
    elif _fan == "4":
        _fan = 1
    else:
        _fan = 0

    if _swing == "set":
        _swing = 0
    elif _swing == "swing":
        _swing = 1
    elif _swing == "swing":
        _swing = 2
    else:
        _swing = 2

    str_raw = ""
    str_bin = ""

    if device.mode != "off": 
        if _swing == 1:
            _buff = AC_IR.hex_string_to_byte_array(General_template_swing_on)
            for i in range(0,7):
                str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
            str_raw += GENERAL_HDR_MARK_USER
            str_raw += ','
            str_raw += GENERAL_HDR_SPACE_USER
            str_raw += ','
            for i in range(0, 7*8):
                str_raw += GENERAL_BIT_MARK_USER
                str_raw += ','
                if str_bin[i] == '1':
                    str_raw += GENERAL_ONE_SPACE_USER
                    str_raw += ','
                else:
                    str_raw += GENERAL_ZERO_SPACE_USER
                    str_raw += ','
            str_raw += GENERAL_BIT_MARK_USER
            str_raw += ','
            str_raw = "0"
        else:
            _buff = AC_IR.hex_string_to_byte_array(General_template_state_on)
            _buff = switch_on(_buff)
            _buff = change_swing(_buff, _swing)
            _buff = change_mode(_buff, _mode)
            if _temp == 0:
                _buff = temp_down(_buff)
            elif _temp == 1:
                _buff = temp_up(_buff)
            elif _temp == 2:
                pass
            elif (_temp > 17) and (_temp < 31):
                _buff = change_temp(_buff, _temp)
            _buff = change_fan(_buff, _fan)

            cs = check_sum(_buff, 7, len(_buff) - 1)
            for i in range(0, len(_buff) - 1):
                str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
            str_bin += AC_IR.byte_to_string(cs.to_bytes(1, 'big'), 0, signed = True)
            
            str_raw += GENERAL_HDR_MARK_USER
            str_raw += ','
            str_raw += GENERAL_HDR_SPACE_USER
            str_raw += ','
            for i in range(0, 16*8):
                str_raw += GENERAL_BIT_MARK_USER
                str_raw += ','
                if str_bin[i] == '1':
                    str_raw += GENERAL_ONE_SPACE_USER
                    str_raw += ','
                else:
                    str_raw += GENERAL_ZERO_SPACE_USER
                    str_raw += ','
            str_raw += GENERAL_BIT_MARK_USER
            str_raw += ','
            str_raw += "0"
    else:
        _buff = AC_IR.hex_string_to_byte_array(General_template_state_off)
        for i in range(0, 7):
            str_bin += AC_IR.byte_to_string(_buff[i].to_bytes(1, 'big'), 0)
        str_raw += GENERAL_HDR_MARK_USER
        str_raw += ','
        str_raw += GENERAL_HDR_SPACE_USER
        str_raw += ','
        for i in range(0, 7*8):
            str_raw += GENERAL_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += GENERAL_ONE_SPACE_USER
                str_raw += ','
            else:
                str_raw += GENERAL_ZERO_SPACE_USER
                str_raw += ','
        str_raw += GENERAL_BIT_MARK_USER
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

def temp_down(_buff):
    pass

def change_temp(_buff, _temp):
    _temp = _temp - 16
    __temp = _temp
    _buff[8] = _buff[8] & 0x0f
    _buff[8] = _buff[8] | __temp
    return _buff

def change_fan(_buff, _fan):
    if _fan == 0:
        _buff[10] = _buff[10] & 0xf8
        _buff[10] = _buff[10] | 0x00
    elif _fan == 4:
        _buff[10] = _buff[10] & 0xf8
        _buff[10] = _buff[10] | 0x04
    elif _fan == 3:
        _buff[10] = _buff[10] & 0xf8
        _buff[10] = _buff[10] | 0x03
    elif _fan == 2:
        _buff[10] = _buff[10] & 0xf8
        _buff[10] = _buff[10] | 0x02
    elif _fan == 1:
        _buff[10] = _buff[10] & 0xf8
        _buff[10] = _buff[10] | 0x01
    else:
        pass
    return _buff

def read_fan(_buff):
    return 0

def change_swing(_buff, _swing):
    if _swing == 1:
        _buff[10] = _buff[10] & 0xef
        _buff[10] = _buff[10] | 0x00
    elif _swing == 2:
        _buff[10] = _buff[10] & 0xef
        _buff[10] = _buff[10] | 0x10
    else:
        pass
    return _buff

def read_swing(_buff):
    return 0

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[9] = _buff[9] & 0xf8
        _buff[9] = _buff[9] | 0x00
    elif _mode == 4:
        _buff[9] = _buff[9] & 0xf8
        _buff[9] = _buff[9] | 0x04
    elif _mode == 1:
        _buff[9] = _buff[9] & 0xf8
        _buff[9] = _buff[9] | 0x01
    elif _mode == 2:
        _buff[9] = _buff[9] & 0xf8
        _buff[9] = _buff[9] | 0x02
    elif _mode == 3:
        _buff[9] = _buff[9] & 0xf8
        _buff[9] = _buff[9] | 0x03
    else:
        pass
    return _buff

def read_mode(_buff):
    return 0

def check_sum(_buf, _add_start, _len):
    _cs = 0x00
    for i in range(_add_start, _len):
        _cs = _cs + _buf[i]
    _cs = ~_cs
    _cs = _cs + 1
    if __debug__:
        print(_cs)
    return _cs