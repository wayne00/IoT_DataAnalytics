import time,sys
import random

# 仅用来做构造模拟数据测试使用
def getSensorData():
    mosfet = 6
    sensordata = {}
    try:
        # Mock data
        sensordata["temp"] = random.randint(0,30)
        sensordata["mois"] = random.randint(0,500)
        sensordata["light"] = random.randint(0,700)
        time.sleep(.5)
        return sensordata

    except KeyboardInterrupt:
        print ("Test by Mock","KeyboardInterrupt!")
    except TypeError:
        REPORTER = "Please power off your raspberry3, and start it again!"
        print ("Raspberry3 overcurrent",REPORTER)
    except IOError:
        print ("Error")