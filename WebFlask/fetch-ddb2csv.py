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


dynamodb = boto3.resource('dynamodb', region_name='cn-north-1')

table = dynamodb.Table('kmdata')

print("export data to csv")

response = table.query(
    KeyConditionExpression=Key('id').eq('kmplc01') & Key('timestamp').gt('2019-07-03 08:00:00')
)


file = open("/Users/maweijun/test.csv","w")
for i in response['Items']:
    # print(i['id'] + "," + i['timestamp'] + "," + str(i['value']))
    file.write(i['id'] + "," + i['timestamp'] + "," + str(i['value'])+"\n")




