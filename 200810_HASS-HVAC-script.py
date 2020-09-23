#Luu y: thong so cac ban tin
import paho.mqtt.client as mqtt
import AC_IR_python
import AC_samsung_python
import AC_sumikura_python
import json

mqtt_server = "192.168.12.43"
mqtt_port = 1883
user = "nta_mqtt"
pwd = "123"

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
    devices.append(Hvac((str)(device_id), "None", "OFF", "Auto", "16", "Auto", "Auto"))

def mqtt_decode(topic, payload):
    check_ = topic[0:5]
    if check_ == "brand":
        #topic: brand/hvac
        #payload: device_id new_brand_name
        device_id = payload[0:6]
        new_brand = payload[7:]
        for device in devices:
            if device_id.decode('utf-8') == device.device_id:
                device.brand = new_brand.decode('utf-8')
                if(new_brand.decode('utf-8') == "Samsung"):
                    Samsung_AC_config(device.device_id, device.brand)
                    device.mode = "Auto"
                    device.fan = "Auto"
                    device.swing = "On"
                elif(new_brand.decode('utf-8') == "Sumikura"):
                    Sumikura_AC_config(device.device_id, device.brand)
                    device.mode = "Cool"
                    device.fan = "Auto"
                    device.swing = "Auto"
                break
    elif check_ == "clima":
        #topic: climate/device_id/change_in
        #payload: 
        device_id = topic[8:14] 
        change_in = topic[15:]
        for device in devices:
            if device.device_id == device_id:
                if change_in == "power":
                    device.state = payload.decode('utf-8')
                elif change_in == "mode":
                    device.mode = payload.decode('utf-8')
                elif change_in == "temp":
                    _temp = payload.decode('utf-8')
                    if _temp.isnumeric():
                        device.temp = payload.decode('utf-8')
                elif change_in == "fan":
                    device.fan = payload.decode('utf-8')
                elif change_in == "swing":
                    device.swing = payload.decode('utf-8')
                str_pub = ""
                if device.brand == "Samsung":
                    str_pub = "/sa/" + AC_samsung_python.encode_samsung(device) + ",msg_id,1,1"
                elif device.brand == "Sumikura":
                    str_pub = "/sa/" + AC_sumikura_python.encode_sumikura(device) + ",msg_id,1,1"
                out_topic = "cmd/" + device_id
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

def Samsung_AC_config(device_id, device_brand):
    name = device_id + ": Dieu hoa " + device_brand
    status = "status/" + device_id
    pubhadhvac = "homeassistant/hvac/" + device_id
    powercmd = "climate/" + device_id + "/power"
    modecmd = "climate/" + device_id + "/mode"
    tempcmd = "climate" + device_id + "/temp"
    fancmd = "climate/" + device_id + "/fan"
    swingcmd = "climate/" + device_id + "/swing"

    fan_modes = ["Auto", "1", "2", "3"]
    max_temp = "30"
    min_temp = "16"
    modes = ["Auto", "Heat", "Cool", "Dry", "Fan only"]
    swing_modes = ["On", "Off"]
 
    payload = {"name": name, "availability_topic": status, "power_command_topic": powercmd,
    "mode_command_topic": modecmd, "temperature_command_topic": tempcmd, "fan_mode_command_topic": fancmd, 
    "swing_mode_command_topic": swingcmd, "mode": modes, "fan_modes": fan_modes, "max_temp": max_temp, "min_temp": min_temp, 
    "swing_modes": swing_modes}

    client.publish(pubhadhvac, payload = json.dumps(payload), retain = True)

def Sumikura_AC_config(device_id, device_brand):
    name = device_id + ": Dieu hoa " + device_brand
    status = "status/" + device_id
    pubhadhvac = "homeassistant/hvac/" + device_id
    powercmd = "climate/" + device_id + "/power"
    modecmd = "climate/" + device_id + "/mode"
    tempcmd = "climate" + device_id + "/temp"
    fancmd = "climate/" + device_id + "/fan"
    swingcmd = "climate/" + device_id + "/swing"

    fan_modes = ["Auto", "1", "2", "3"]
    max_temp = "30"
    min_temp = "16"
    modes = ["Cool", "Heat", "Fan only"]
    swing_modes = ["Auto", "1", "2", "3", "4", "5"]
 
    payload = {"name": name, "availability_topic": status, "power_command_topic": powercmd,
    "mode_command_topic": modecmd, "temperature_command_topic": tempcmd, "fan_mode_command_topic": fancmd, 
    "swing_mode_command_topic": swingcmd, "mode": modes, "fan_modes": fan_modes, "max_temp": max_temp, "min_temp": min_temp, 
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
client.username_pw_set(user, pwd)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, mqtt_port, 60)
client.publish("nta3100", "Hello", 0)
read_old_data()
overwrite_data()
client.loop_forever()
#mqtt