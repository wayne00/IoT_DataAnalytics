# from future import print_function
import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
import boto3

region_name = '<region_name>'
def sendEmail():
    # Create an SNS client
    sns = boto3.client('sns',region_name=region_name)
    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='<sns topic>',    
        Message='ALARM -- there maybe sth wrong with the machine!',    
    )
    # Print out the response
    print(response)


def sendPartition(iter):
    print("--------------------------------------------------------")
    for record in iter:
        temperature = json.loads(record)["value"]
        if(temperature > 25):
            sendEmail()
    print("--------------------------------------------------------")

sc = SparkContext()
ssc = StreamingContext(sc, 1)

streamName = 'lynf-datastream'
appName = 'lynf_data'
endpointUrl = '<kinesis endpointUrl>'
regionName = 'region_name'

dstream = KinesisUtils.createStream(ssc, appName, streamName, endpointUrl, regionName, InitialPositionInStream.TRIM_HORIZON, 5)
# py_rdd = dstream.map(lambda x: json.loads(x))
dstream.foreachRDD(lambda rdd: rdd.foreachPartition(sendPartition))

# py_rdd.pprint(10)
# py_rdd.saveAsTextFiles("s3n://maweijun-test4/lynf_data/output.txt")


ssc.start()
ssc.awaitTermination()
# ssc.stop()

------------------------------------------------------------------------------------------
# 提交任务
pyspark:
  spark-submit --packages org.apache.spark:spark-streaming-kinesis-asl_2.11:2.4.2 spark-streaming.py
