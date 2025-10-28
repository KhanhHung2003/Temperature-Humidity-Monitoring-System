from urllib import request, parse
from time import sleep	
from seeed_dht import DHT

sensor = DHT('11', 5)
def make_params_thingspeak(temperature, humidity):
    params = parse.urlencode({'field1':temperature,'field2':humidity}).encode()
    return params
def thingspeak_post(params):
    api_key_write = "Q007UOU4X02IJY6R"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    r = request.urlopen(req, data=params)
    respone_data=r.read()
    return respone_data

while True:
    humi, temp = sensor.read()
    print("Temp: {0:2}, Humi: {0:2}".format(temp, humi))
    params_thingspeak = make_params_thingspeak(temp, humi)
    thingspeak_post(params_thingspeak)
    sleep(20)
