'''
/*
 * Copyright 2010-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import random
import sensordata
import diodePowerCtl
from datetime import datetime
import RPi.GPIO as GPIO

global status
status = 0


# endpoint 地址从AWS web控制台 -> IoT 服务 -> 管理  -> Things  -> Details 中获取
# 样例 endpoint = "xxxxxx.ats.iot.cn-north-1.amazonaws.com.cn"
endpoint = "<使用实际endpoint替换>"
# thingName 是Iot平台中该对象的命名
thingName = "raspberryPi"
# 与IoT平台进行通行用的topic
topic = "raspberryPi/sensor/data"
# 以下是标准的证书信息，需要到aws iot 平台获取到对应设备的证书，并且需要为该证书绑定policy
rootCAPath = "cert/root-CA.crt"
certificatePath = "cert/certificate.pem"
privateKeyPath = "cert/private.pem.key"

#定义两个客户端，要求命名不重复
clientId = "randomID1" + str(random.randint(10000,99999))
clientId2 = "randomID2" + str(random.randint(10000,99999))

INITTHRESHOULD = 1
DIODESTATUS = 'OFF' 

#定义发光二极管的初始状态
diodePowerCtl.setDiodeDoor(DIODESTATUS)

class shadowCallbackContainer:

    threshould = INITTHRESHOULD

    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # 回调函数，用户执行“开/关”灯指令后，回调函数执行，树莓派执行灯“开/关”指令
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload 是一个Json串，内容是客户端发送的命令
        print("Received a delta message:")
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        print("!!!!!!!!!!")

        if payloadDict["state"].has_key('threshould'): 
            shadowCallbackContainer.threshould = int(payloadDict["state"]['threshould'])
            print("access to fix threshould =>>>>"+ str(shadowCallbackContainer.threshould))
        print("Request to update the reported state...")
	
        # 解析Json串，获取客户的指令
    	print("==================turn on/off the light start =====================")
    	desireDoorState = payloadDict["state"]['status']
    	print desireDoorState
    	
    	# 执行客户指令，实现开关灯操作
        global DIODESTATUS
        DIODESTATUS = desireDoorState
     	time.sleep(2)
    	diodePowerCtl.setDiodeDoor(desireDoorState)
    	print("==================trun on/off the light end   =====================")

        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)



# 客户 MQTT 消息回调
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message)

# 设备影子回调
def getShadowCallback(client, userdata, message):
    print(">>>>>>>>Received a new getShadowCallback message: ")
    print(userdata)
    print(message)

# 配置日志
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# 初始化 AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient 配置设置
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# 连接到AWS IoT Core
myAWSIoTMQTTShadowClient.connect()

# 创建设备影子
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)
shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)

# 监听客户指令,通过监听delta topic来实现
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)


def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")

def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId2)
myAWSIoTMQTTClient.configureEndpoint(endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient 连接配置
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 600, 300)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  
myAWSIoTMQTTClient.configureDrainingFrequency(2)  
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(600)  
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  
myAWSIoTMQTTClient.onMessage = customOnMessage

# 把设备连接到IoT 平台
myAWSIoTMQTTClient.connect()

# 模拟设备持续publish消息到IoT平台
while True:
    while DIODESTATUS == 'ON':
	    time.sleep(2)
    while DIODESTATUS != 'ON':	
    	try:
        	senData = {}
        	senData["state"] = {}
        	senData["state"]["reported"] = {}
		    simpleSenData = {}

            # 获取温度传感器DHT11/22的温湿度信息，并构造JSON
        	tempData = sensordata.getSensor()

        	senData["state"]["reported"]['mois'] = tempData['mois']
        	senData["state"]["reported"]['temp'] = tempData['temp']
        	senData["state"]["reported"]['light'] = tempData['light']


		    simpleSenData['mois'] = tempData['mois']
            simpleSenData['value'] = tempData['temp']
            simpleSenData['light'] = tempData['light']
	
        	print("class threshold >>>>"+str(shadowCallbackContainer.threshould))
       		new_threshold = shadowCallbackContainer.threshould

		    simpleSenData['status'] = DIODESTATUS
            simpleSenData['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		    simpleSenData['id'] = thingName
		
		    print(">>>>>>>>>>")
    		print(simpleSenData)

        	myAWSIoTMQTTClient.publishAsync(topic, json.dumps(simpleSenData), 1, ackCallback=customPubackCallback)
		    time.sleep(2)

    	except KeyboardInterrupt:
        	print("key interrput")
        	break
    	except IOError:
        	print ("Error")
    	except TypeError, e:
        	print(str(e))
        	print("TypeError Need reboot?")
        	break
    	finally:
        	print ("finally process!")
    time.sleep(2)
