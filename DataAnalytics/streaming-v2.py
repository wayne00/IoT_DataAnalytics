# from future import print_function
import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
import boto3
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle

region_name = '<region_name>'
loaded_model = pickle.load(open('/home/hadoop/lf-model','rb'))

def predict(temperature):
    result = 1
    vec = np.array([temperature]).reshape(-1,1)
    print(loaded_model.predict(vec))
    if loaded_model.predict(vec) == -1 and temperature > 28:
        result = -1
    else:
        result = 1
    return result

def sendEmail(temperature):
    # Create an SNS client
    sns = boto3.client('sns',region_name=region_name)
    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='<sns topic>',    
        Message='ALARM -- The temperature value is :' + str(temperature) + '\n there maybe sth wrong with the machine!  \n\n this alarm from SparkStreaming!',    
    )
    # Print out the response
    print(response)
    return 

def sendPartition(iter):
    print("--------------------------------------------------------")
    for record in iter:
        temperature = json.loads(record)["value"]
        if(predict(temperature)== -1):
            sendEmail(temperature)
    print("--------------------------------------------------------")
    return

sc = SparkContext()
ssc = StreamingContext(sc, 2)

streamName = 'lynf-datastream'
appName = 'lynf_data'
endpointUrl = '<kinesis endpointUrl>'
regionName = region_name

dstream = KinesisUtils.createStream(ssc, appName, streamName, endpointUrl, regionName, InitialPositionInStream.TRIM_HORIZON, 5)
# py_rdd = dstream.map(lambda x: json.loads(x))
dstream.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

# py_rdd.pprint(10)
# py_rdd.saveAsTextFiles("s3n://maweijun-test4/lynf_data/output.txt")

ssc.start()
ssc.awaitTermination()
# ssc.stop()
