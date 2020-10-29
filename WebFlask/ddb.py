from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# dynamodb = boto3.resource('dynamodb', region_name='cn-northwest-1', endpoint_url='dynamodb.cn-northwest-1.amazonaws.com.cn')

dynamodb = boto3.resource('dynamodb')


table = dynamodb.Table('kmdata')

print("read from kmdata")

dt = '2020-01-01 00:00:00'

response = table.query(
    KeyConditionExpression=Key('id').eq('1') & Key('timestamp').lt(dt),
    ScanIndexForward = True,
    Limit = 1000,
)



    # KeyConditionExpression=Key('id').eq('1') & Key('timestamp').lt('2019-01-01 00:00:00'),
    # ScanIndexForward = False,
    # Limit = 2,



for i in response['Items']:
    print(i['id'], ":", i['timestamp'], ":" , i['value'])