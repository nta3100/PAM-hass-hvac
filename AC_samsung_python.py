import AC_IR_python

def encode_samsung(device): 
    samsung_template = "02920F000000F001D2FE718019F001C2FE71C015F0"
    samsung_template_on = "02920F000000F001D20E0000000001C2FE71C015F0"
    samsung_template_off = "02B20F000000C001D20F0000000001E2FE719015C0"
    SAMSUNG_HDR_MARK_USER = "3000"
    SAMSUNG_HDR_SPACE_USER = "9000"
    SAMSUNG_BIT_MARK_USER = "500"
    SAMSUNG_ONE_SPACE_USER = "1500"
    SAMSUNG_ZERO_SPACE_USER = "500"
    state = 1

    if device.swing == "off":
        _swing = 10
    elif device.swing == "swing":
        _swing = 15
    else: 
        _swing = 15

    if device.mode == "auto":
        _mode = 0
    elif device.mode == "heat":
        _mode = 4
    elif device.mode == "cool":
        _mode = 1
    elif device.mode == "dry":
        _mode = 2
    elif device.mode == "fan_only":
        _mode = 3
    else:
        _mode = 0

    if device.fan == "auto":
        _fan = 0
    elif device.fan == "low":
        _fan = 2
    elif device.fan == "medium":
        _fan = 4
    elif device.fan == "high":
        _fan = 5
    else:
        _fan = 0

    str_raw = ""
    str_bin = ""

    _buff_header = AC_IR_python.hex_string_to_byte_array(samsung_template)
    _buff_on = AC_IR_python.hex_string_to_byte_array(samsung_template_on)
    _buff_off = AC_IR_python.hex_string_to_byte_array(samsung_template_off)

    if (device.mode == "off"):
        switch_off(_buff_off)
        str_bin = AC_IR_python.byte_to_string(_buff_off, 0) 
        print(str_bin)
        str_raw += SAMSUNG_HDR_MARK_USER
        str_raw += ','
        str_raw += SAMSUNG_HDR_SPACE_USER
        str_raw += ','
        for i in range(7*8):
            str_raw += SAMSUNG_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += SAMSUNG_ONE_SPACE_USER
                str_raw += ','
            else:
                str_raw += SAMSUNG_ZERO_SPACE_USER
                str_raw += ','
        str_raw += SAMSUNG_BIT_MARK_USER
        str_raw += ','
        str_raw += "3000"
        str_raw += ','
        str_raw += SAMSUNG_HDR_MARK_USER
        str_raw += ','
        str_raw += SAMSUNG_HDR_SPACE_USER
        str_raw += ','
        for i in range(7*8, 14*8):
            str_raw += SAMSUNG_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += SAMSUNG_ONE_SPACE_USER
                str_raw += ','
            else:
                str_raw += SAMSUNG_ZERO_SPACE_USER
                str_raw += ','
        str_raw += SAMSUNG_BIT_MARK_USER
        str_raw += ','
        str_raw += "3000"
        str_raw += ','
        str_raw += SAMSUNG_HDR_MARK_USER
        str_raw += ','
        str_raw += SAMSUNG_HDR_SPACE_USER
        str_raw += ','
        for i in range(14*8, 21*8):
            str_raw += SAMSUNG_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += SAMSUNG_ONE_SPACE_USER
                str_raw += ','
            else: 
                str_raw += SAMSUNG_ZERO_SPACE_USER
                str_raw += ','
        str_raw += SAMSUNG_BIT_MARK_USER
        str_raw += ','
        str_raw += "0"
    else:
        switch_on(_buff_on)
        _buff_on = change_mode(_buff_on, _mode)
        if (int)(device.temp) == 0:
            _buff_on = temp_down(_buff_on)
        elif (int)(device.temp) == 1:
            _buff_on = temp_up(_buff_on)
        elif (int)(device.temp) == 2:
            pass
        elif (((int)(device.temp) > 15) and ((int)(device.temp) < 31)):
            _buff_on = change_temp(_buff_on, (int)(device.temp))
        else:
            pass
        _buff_on = change_fan(_buff_on, _fan)
        _buff_on = change_swing(_buff_on, _swing)
        
        checksum = 0x00
        samsungByte = []
        for j in range(10,14):
            samsungByte = _buff_on[j]
            if j == 2:
                samsungByte &= 0b11111110
            for i in range(0,8):
                if ((samsungByte & 0x01) == 1):
                    checksum += 1
                samsungByte >> 1
        checksum = 28 - checksum
        checksum << 4
        checksum |= 0x02
        _buff_on[8] = checksum
        str_bin = AC_IR_python.byte_to_string(_buff_on, 0)
        str_raw += SAMSUNG_HDR_MARK_USER
        str_raw += ','
        str_raw += SAMSUNG_HDR_SPACE_USER
        str_raw += ','
        for i in range(0,7*8):
            str_raw += SAMSUNG_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += SAMSUNG_ONE_SPACE_USER
                str_raw += ','
            else:
                str_raw += SAMSUNG_ZERO_SPACE_USER
                str_raw += ','
        str_raw += SAMSUNG_BIT_MARK_USER
        str_raw += ','
        str_raw += "3000"
        str_raw += ','
        str_raw += SAMSUNG_HDR_MARK_USER
        str_raw += ','
        str_raw += SAMSUNG_HDR_SPACE_USER
        str_raw += ','
        for i in range(7*8, 14*8):
            str_raw += SAMSUNG_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += SAMSUNG_ONE_SPACE_USER
                str_raw += ','
            else:
                str_raw += SAMSUNG_ZERO_SPACE_USER
                str_raw += ','
        str_raw += SAMSUNG_BIT_MARK_USER
        str_raw += ','
        str_raw += "3000"
        str_raw += ','
        str_raw += SAMSUNG_HDR_MARK_USER
        str_raw += ','
        str_raw += SAMSUNG_HDR_SPACE_USER
        str_raw += ','
        for i in range(14*8, 21*8):
            str_raw += SAMSUNG_BIT_MARK_USER
            str_raw += ','
            if str_bin[i] == '1':
                str_raw += SAMSUNG_ONE_SPACE_USER
                str_raw += ','
            else:
                str_raw += SAMSUNG_ZERO_SPACE_USER
                str_raw += ','
        str_raw += SAMSUNG_BIT_MARK_USER
        str_raw += ','
        str_raw += "0"
    str_raw = AC_IR_python.gz_base64_compress(str_raw)
    return str_raw
#AC_Samsung.java
def switch_on(_buff):
    state = 1

def switch_off(_buff):
    state = 0

def read_temp(_buff):
    _temp = []
    _temp.append((int)((_buff[11] >> 4) & 0x01))
    _temp.append((int)((_buff[11] >> 5) & 0x01))
    _temp.append((int)((_buff[11] >> 6) & 0x01))
    _temp.append((int)((_buff[11] >> 7) & 0x01))
    temp = 16 + AC_IR_python.bit_to_int(_temp, 4, 0)
    #print(temp)
    return temp

def temp_up(_buff):
    temp = read_temp(_buff)
    if ((temp > 15) and (temp < 31)):
        if temp == 30:
            pass
        else:
            _buff[11] = _buff[11] + 16
    return _buff

def temp_down(_buff):
    temp = read_temp(_buff)
    if ((temp > 15) and (temp < 31)):
        if temp == 16:
            pass
        else:
            _buff[11] = _buff[11] - 16
    return _buff

def change_temp(_buff, _temp):
    _temp = _temp - 16
    _buff[11] = _buff[11] & 0x0f
    _buff[11] = _buff[11] | (_temp << 4)
    return _buff

def change_fan(_buff, _fan):
    if _fan == 0:
        _buff[12] = _buff[12] & 0xf1
        _buff[12] = _buff[12] | 0x00
    elif _fan == 2:
        _buff[12] = _buff[12] & 0xf1
        _buff[12] = _buff[12] | 0x04
    elif _fan == 4:
        _buff[12] = _buff[12] & 0xf1
        _buff[12] = _buff[12] | 0x08
    elif _fan == 5:
        _buff[12] = _buff[12] & 0xf1
        _buff[12] = _buff[12] | 0xfa
    return _buff

def read_fan(_buff):
    _fan = []
    _fan.append(int((_buff[12] >> 1) & 0x01))
    _fan.append(int((_buff[12] >> 2) & 0x01))
    _fan.append(int((_buff[12] >> 3) & 0x01))
    fan = AC_IR_python.bit_to_int(_fan, 3, 0)
    return fan

def change_swing(_buff, _swing):
    if _swing == 10:
        _buff[9] = _buff[9] & 0x0f
        _buff[9] = _buff[9] | 0xa0
    elif _swing == 15:
        _buff[9] = _buff[9] & 0x0f
        _buff[9] = _buff[9] | 0xf0
    return _buff

def read_swing(_buff):
    _swing = []
    _swing.append((int)((_buff[9] >> 4) & 0x01))
    _swing.append((int)((_buff[9] >> 5) & 0x01))
    _swing.append((int)((_buff[9] >> 6) & 0x01))
    _swing.append((int)((_buff[9] >> 7) & 0x01))
    swing = AC_IR_python.bit_to_int(_swing, 4, 0)
    return swing

def change_mode(_buff, _mode):
    if _mode == 0:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x00
    elif _mode == 1:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x10
    elif _mode == 2:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x20
    elif _mode == 3:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x30
    elif _mode == 4:
        _buff[12] = _buff[12] & 0x8f
        _buff[12] = _buff[12] | 0x40
    return _buff

def read_mode(_buff):
    _mode = []
    _mode.append((int)(_buff[12] >> 4) & 0x01)
    _mode.append((int)(_buff[12] >> 5) & 0x01)
    _mode.append((int)(_buff[12] >> 6) & 0x01)
    mode = AC_IR_python.bit_to_int(_mode, 3, 0)
    return mode