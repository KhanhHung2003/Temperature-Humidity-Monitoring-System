from urllib import request
import json, time
from gpiozero import Buzzer, LED
from grove.display.jhd1802 import JHD1802
from grove.grove_relay import GroveRelay

buzzer = Buzzer(16)
led = LED(12)
relay = GroveRelay(22)
lcd = JHD1802()

apiKeyRead1 = "QGOTN9O7RA8OYRZIE"
channelID1 = "2659555"
apiKeyRead = "S7P6P2CQ806WY8WEZ"
channelID = "22659556"

def get_temp():
    req = request.Request(f"https://api.thingspeak.com/channels/{channelID1}/fields/1/last.json?api_key={apiKeyRead1}")
    r = request.urlopen(req)
    data = json.loads(r.read().decode())
    return data.get("field1", 0)

def get_humi():
    req = request.Request(f"https://api.thingspeak.com/channels/{channelID1}/fields/2/last.json?api_key={apiKeyRead1}")
    r = request.urlopen(req)
    data = json.loads(r.read().decode())
    return data.get("field2", 0)

def get_led_state():
    req = request.Request(f"https://api.thingspeak.com/channels/{channelID}/fields/2/last.json?api_key={apiKeyRead}")
    r = request.urlopen(req)
    data = json.loads(r.read().decode())
    return data.get("field2", 0)

def get_buzzer_state():
    req = request.Request(f"https://api.thingspeak.com/channels/{channelID}/fields/4/last.json?api_key={apiKeyRead}")
    r = request.urlopen(req)
    data = json.loads(r.read().decode())
    return data.get("field4", 0)

def get_relay_state():
    req = request.Request(f"https://api.thingspeak.com/channels/{channelID}/fields/3/last.json?api_key={apiKeyRead}")
    r = request.urlopen(req)
    data = json.loads(r.read().decode())
    return data.get("field3", 0)

def get_mode():
    req = request.Request(f"https://api.thingspeak.com/channels/{channelID}/fields/1/last.json?api_key={apiKeyRead}")
    r = request.urlopen(req)
    data = json.loads(r.read().decode())
    return data.get("field1", 0)

while True:
    try:
        temp = get_temp()
        humi = get_humi()
        led_state = get_led_state()
        relay_state = get_relay_state()
        buzzer_state = get_buzzer_state()
        mode = get_mode()
        current_time = int(time.strftime("%H%M", time.localtime()))

        lcd.setCursor(0, 0)
        lcd.write(f'Doam: {humi}%')
        lcd.setCursor(1, 0)
        lcd.write(f'Nhietdo: {temp}C')

        if int(mode) == 1:
            print("Chế độ auto")
            if 1800 <= current_time <= 2200:
                led.on()
            else:
                led.off()

            if int(humi) > 35:
                buzzer.on()
            elif int(humi) < 31:
                buzzer.off()

            if int(temp) > 90:
                relay.on()
            elif int(temp) < 60:
                relay.off()

        elif int(mode) == 0:
            print("Chế độ manual")
            led.on() if int(led_state) == 1 else led.off()
            buzzer.on() if int(buzzer_state) == 1 else buzzer.off()
            relay.on() if int(relay_state) == 1 else relay.off()

    except Exception as e:
        print(f'Mất kết nối: {e}')
        time.sleep(2)
