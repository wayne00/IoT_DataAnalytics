#!/usr/bin/python
import Adafruit_DHT as dht
import time
import random

# 使用 Adafruit_DHT 库，来获取温湿度传感器的数据，需要注意温湿度传感器
# 插入到树莓派面包板上的针脚pin
def getSensor():
    sensordata = {}
    try:
        # 使用 Adafruit_DHT 库，来获取温湿度传感器的数据
        sensor = dht.DHT11
        # 根据温湿度传感器插入到面包板的针脚位置来确定
        pin = 2

    	humidity, temperature = dht.read_retry(sensor, pin)
    	if humidity is not None and temperature is not None:
    		humidity, temperature = dht.read_retry(sensor, pin)
    	else:
    		humidity, temperature = 0,0

        sensordata["temp"] = round(temperature,2)
        sensordata["mois"] = round(humidity,2)

	print("temp is:" + str(temperature))
	print("hum is " + str(humidity))
	print("-----------")
        # Mock light data
        sensordata["light"] = random.randint(0,700)
        time.sleep(.5)
        return sensordata

    except KeyboardInterrupt:
        print ("Test by Mock","KeyboardInterrupt!")
    except TypeError:
        print ("Please power off your raspberry3, and start it again!")
        print ("Raspberry3 overcurrent")
    except IOError:
        print ("Error")


if __name__ == "__main__":
	while True:
		getSensor()

