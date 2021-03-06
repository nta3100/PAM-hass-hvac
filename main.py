import paho.mqtt.client as mqtt
import AC_IR
import AC_Sumikura
import AC_Samsung
import AC_Daikin_1
import AC_Daikin_2
import AC_Funiki
import AC_Funiki_2
import AC_General
import AC_Gree
import AC_Asanzo
import AC_LG
import AC_Midea
import AC_Mitsubishi
import AC_Nagakawa
import AC_Panasonic
import AC_Sharp
import json

#mqtt_server = "192.168.11.86"
#mqtt_port = 1883
#user = "nta_mqtt"
#pwd = "123"

mqtt_server = "broker.hivemq.com"
mqtt_port = 1883

print("Starting")

class Hvac:
    def __init__(self, device_id, brand, state, mode, temp, fan, swing):
        self.device_id = device_id
        self.brand = brand
        self.state = state
        self.mode = mode
        self.temp = temp
        self.fan = fan
        self.swing = swing
devices = []
#Doc du lieu luu tru trong file hvac_data
def read_old_data():
    #upload: /home/nta/hass-hvac/hvac_data.txt
    with open("hvac_data.txt", 'r') as f:
        while True:
            device_id = f.readline().rstrip("\n")
            brand = f.readline().rstrip("\n")
            state = f.readline().rstrip("\n")
            mode = f.readline().rstrip("\n")
            temp = f.readline().rstrip("\n")
            fan = f.readline().rstrip("\n")
            swing = f.readline().rstrip("\n")
            if (device_id == ""):
                break
            devices.append(Hvac(device_id, brand, state, mode, temp, fan, swing))

#Ghi du lieu (overwrite) file hvac_data
def overwrite_data():
    #upload: /home/nta/hass-hvac/hvac_data.txt
    with open("hvac_data.txt", 'w') as f:
        for device in devices:
            f.write(str(device.device_id) + "\n")
            f.write(str(device.brand) + "\n")
            f.write(str(device.state) + "\n")
            f.write(str(device.mode) + "\n")
            f.write(str(device.temp) + "\n")
            f.write(str(device.fan) + "\n")
            f.write(str(device.swing) + "\n")

#Khi co thiet bi moi xuat hien trong mang
def add_new_device(device_id):
    devices.append(Hvac((str)(device_id), "null", "off", "auto", "16", "auto", "auto"))

def mqtt_decode(topic, payload):
    check_ = topic[0:5]
    if check_ == "brand":
        #topic: brand/hvac
        #payload: device_id new_brand_name
        device_id = payload[0:6]
        new_brand = payload[7:]
        for device in devices:
            if device_id.decode('utf-8') == device.device_id:
                device.brand = new_brand.decode('utf-8').lower()
                new_config(device_id = device.device_id, device_brand = device.brand)
    elif check_ == "clima":
        #topic: climate/device_id/change_in
        #payload: 
        device_id = topic[8:14] 
        change_in = topic[15:]
        for device in devices:
            if device.device_id == device_id:
                if change_in == "mode":
                    device.mode = payload.decode('utf-8').lower()         
                elif change_in == "temp":
                    _temp = payload.decode('utf-8')
                    if _temp.replace('.','',1).isdigit():
                        device.temp = str(int(float(payload.decode('utf-8'))))
                elif change_in == "fan":
                    device.fan = payload.decode('utf-8').lower()
                elif change_in == "swing":
                    device.swing = payload.decode('utf-8').lower()
                str_pub = ""
                if device.brand == "samsung":
                    str_pub = "/sa/" + AC_Samsung.encode_samsung(device) + ",msg_id,1,1"
                elif device.brand == "sumikura":
                    str_pub = "/sa/" + AC_Sumikura.encode_sumikura(device) + ",msg_id,1,1"
                elif device.brand == "daikin1":
                    str_pub = "/sa/" + AC_Daikin_1.encode_daikin1(device) + ",msg_id,1,1"
                elif device.brand == "asanzo":
                    str_pub = "/sa/" + AC_Asanzo.encode_asanzo(device) + ",msg_id,1,1"
                elif device.brand == "daikin2":
                    str_pub = "/sa/" + AC_Daikin_2.encode_daikin_2(device) + ",msg_id,1,1"
                elif device.brand == "funiki2":
                    str_pub = "/sa/" + AC_Funiki_2.encode_funiki2(device) + ",msg_id,1,1"
                elif device.brand == "funiki":
                    str_pub = "/sa/" + AC_Funiki.encode_funiki(device) + ",msg_id,1,1"
                elif device.brand == "general":
                    str_pub = "/sa/" + AC_General.encode_general(device) + ",msg_id,1,1"
                elif device.brand == "gree":
                    str_pub = "/sa/" + AC_Gree.encode_gree(device) + ",msg_id,1,1"
                elif device.brand == "lg":
                    str_pub = "/sa/" + AC_LG.encode_lg(device) + ",msg_id,1,1"
                elif device.brand == "midea":
                    str_pub = "/sa/" + AC_Midea.encode_midea(device) + ",msg_id,1,1"
                elif device.brand == "mitsubishi":
                    str_pub = "/sa/" + AC_Mitsubishi.encode_mitsubishi(device) + ",msg_id,1,1"
                elif device.brand == "nagakawa":
                    str_pub = "/sa/" + AC_Nagakawa.encode_nagakawa(device) + ",msg_id,1,1"
                elif device.brand == "panasonic":
                    str_pub = "/sa/" + AC_Panasonic.encode_panasonic(device) + ",msg_id,1,1"
                elif device.brand == "sharp":
                    str_pub = "/sa/" + AC_Sharp.encode_sharp(device) + ",msg_id,1,1"
                out_topic = "cmd/" + device.device_id
                if __debug__:
                    print(str_pub)
                    print(out_topic)
                client.publish(out_topic, str_pub)
                break
    elif check_ == "hvac/":
        #topic: hvac/newdevice
        #payload: device_id
        new_device = True
        device_id = payload.decode('utf-8')
        for device in devices:
            if device.device_id == device_id:
                new_device = False
        if new_device == True:
            add_new_device(device_id)
    overwrite_data()

def new_config(device_id, device_brand):
    name = "Dieu khien dieu hoa: " + device_id
    status = "status/" + device_id
    hass_mqtt_topic = "homeassistant/climate/" + device_id + "/config"
    mode_cmd = "climate/" + device_id + "/mode"
    temp_cmd = "climate/" + device_id + "/temp"
    fan_cmd = "climate/" + device_id + "/fan"
    swing_cmd = "climate/" + device_id + "/swing"

    if device_brand == "samsung":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["On", "Off"]
    elif device_brand == "sumikura":
        modes = ["off", "cool", "heat", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "asanzo":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "32"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "daikin1":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "32"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "daikin2":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "32"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3", "4", "5"]
        swing_modes = ["On", "Off"]
    elif device_brand == "funiki":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "31"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "funiki2":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "31"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "general":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "17"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Set", "Swing"]
    elif device_brand == "gree":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["On", "Off"]
    elif device_brand == "lg":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Swing"]
    elif device_brand == "midea":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "17"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Swing", "Set"]
    elif device_brand == "mitsubishi":
        modes = ["off", "auto", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "nagakawa":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3", "4", "5"]
        swing_modes = ["On", "Off"]
    elif device_brand == "panasonic":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "30"
        min_temp = "16"
        fan_modes = ["Auto", "1", "2", "3", "4", "5"]
        swing_modes = ["Auto", "1", "2", "3", "4", "5"]
    elif device_brand == "sharp":
        modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
        max_temp = "32"
        min_temp = "18"
        fan_modes = ["Auto", "1", "2", "3"]
        swing_modes = ["Swing"]
    else:
        return 0

    payload = {"name": name, "availability_topic": status, 
        "mode_command_topic": mode_cmd, "temperature_command_topic": temp_cmd, 
        "fan_mode_command_topic": fan_cmd, 
        "swing_mode_command_topic": swing_cmd, "modes": modes, 
        "fan_modes": fan_modes, "max_temp": max_temp, "min_temp": min_temp, 
        "swing_modes": swing_modes}

    client.publish(hass_mqtt_topic, payload = json.dumps(payload), retain = True)


def Samsung_AC_config(device_id, device_brand):
    name = "Dieu khien dieu hoa: " + device_id
    status = "status/" + device_id
    pubhadhvac = "homeassistant/climate/" + device_id + "/config"
    modecmd = "climate/" + device_id + "/mode"
    tempcmd = "climate/" + device_id + "/temp"
    fancmd = "climate/" + device_id + "/fan"
    swingcmd = "climate/" + device_id + "/swing"

    fan_modes = ["Auto", "1", "2", "3"]
    max_temp = "30"
    min_temp = "16"
    modes = ["off", "auto", "heat", "cool", "dry", "fan_only"]
    swing_modes = ["On", "Off"]
 
    payload = {"name": name, "availability_topic": status, 
    "mode_command_topic": modecmd, "temperature_command_topic": tempcmd, 
    "fan_mode_command_topic": fancmd, 
    "swing_mode_command_topic": swingcmd, "modes": modes, 
    "fan_modes": fan_modes, "max_temp": max_temp, "min_temp": min_temp, 
    "swing_modes": swing_modes}

    client.publish(pubhadhvac, payload = json.dumps(payload), retain = True)

def Sumikura_AC_config(device_id, device_brand):
    name = "Dieu khien dieu hoa: " + device_id
    status = "status/" + device_id
    pubhadhvac = "homeassistant/climate/" + device_id + "/config"
    modecmd = "climate/" + device_id + "/mode"
    tempcmd = "climate/" + device_id + "/temp"
    fancmd = "climate/" + device_id + "/fan"
    swingcmd = "climate/" + device_id + "/swing"

    fan_modes = ["Auto", "1", "2", "3"]
    max_temp = "30"
    min_temp = "16"
    modes = ["off", "cool", "heat", "fan_only"]
    swing_modes = ["Auto", "1", "2", "3", "4", "5"]
 
    payload = {"name": name, "availability_topic": status, 
    "mode_command_topic": modecmd, "temperature_command_topic": tempcmd, 
    "fan_mode_command_topic": fancmd, 
    "swing_mode_command_topic": swingcmd, "modes": modes, 
    "fan_modes": fan_modes, "max_temp": max_temp, "min_temp": min_temp, 
    "swing_modes": swing_modes}

    client.publish(pubhadhvac, payload = json.dumps(payload), retain = True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("climate/#")
    client.subscribe("brand/hvac")
    client.subscribe("hvac/newdevice")
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    mqtt_decode(msg.topic, msg.payload)

client = mqtt.Client()
#client.username_pw_set(user, pwd)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, mqtt_port, 60)
client.publish("nta3100", "Hello", 0)
read_old_data()
overwrite_data()
client.loop_forever()
#mqtt