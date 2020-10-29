from __future__ import print_function # Python 2/3 compatibility
from flask import Flask,render_template,url_for,request
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal
import switchLight

app = Flask(__name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


@app.route('/',methods=['get','post'])
def index():
    return render_template('dynamicData.html')

@app.route('/orders/<int:order_id>')
def get_order_id(order_id):
    return 'order_id %s' %order_id


@app.route('/test', methods=['GET','POST'])
def my_echart():
    data = []
    print("............ dynamic flash ............")
    strf = str(request.get_data().decode())[16:30]
    datef = str2date(strf)

    dynamodb = boto3.resource('dynamodb',region_name='')
    table = dynamodb.Table('<table-name>')
    response = table.query(
        KeyConditionExpression=Key('id').eq('kmplc01') & Key('timestamp').gt(datef),
        ScanIndexForward=False,
    )

    data = []
    for dt in response['Items']: #dt is a dic type
        oneData = {}
        # print(dt['timestamp'])
        oneData['name'] = dt['timestamp'].replace('-','/',2)

        year = dt['timestamp'][0:4]
        month = dt['timestamp'][5:7]
        day = dt['timestamp'][8:10]
        hms = dt['timestamp'][11:20]
        oneData['value'] = [year + "/" + month + "/" + day+" "+hms, dt['value']]

        data.append(oneData)

    # j = json.dumps(data)
    j = json.dumps(data,cls=DecimalEncoder)

    return j
    print("............ dynamic flash finish ............")


@app.route('/init', methods=['GET', 'POST'])
def my_initEchart():
    print("............ start init ............")
    dynamodb = boto3.resource('dynamodb',region_name='')
    table = dynamodb.Table('<table-name>')

    dt = '9999-01-01 00:00:00'
    dt1 = '2019-05-29 00:00:00'
    response = table.query(
        KeyConditionExpression=Key('id').eq('kmplc01') & Key('timestamp').lt(dt),
        ScanIndexForward=False,
        # ConsistentRead=True,
        Limit=50,
    )

    data = []
    for dt in response['Items']: #dt is a dic type
        oneData = {}
        # print(dt['timestamp'])
        oneData['name'] = dt['timestamp'].replace('-','/',2)

        year = dt['timestamp'][0:4]
        month = dt['timestamp'][5:7]
        day = dt['timestamp'][8:10]
        hms = dt['timestamp'][11:20]
        oneData['value'] = [year + "/" + month + "/" + day+" "+hms, dt['value']]

        print(oneData['name'])
        print(oneData['value'][0])
        print(oneData['value'][1])

        data.append(oneData)

    j = json.dumps(data, cls=DecimalEncoder)
    print("............ end init ............")

    return j


@app.route('/on-off', methods=['GET', 'POST'])
def switchLight():
    import switchLight
    strf = str(request.get_data().decode())
    print(request.get_data().decode())

    if int(request.get_data().decode()) == 0:
        #OFF
        print("we will turn off the light")
        switchLight.switch("OFF")
    elif int(request.get_data().decode()) == 1:
        #ON
        print("we will turn on the light")
        switchLight.switch("ON")
    else:
        print("we will do nothing")

    data ={}
    return json.dumps(data,cls=DecimalEncoder)


def str2date(str):
    dateStr = str[0:4]+"-"+str[4:6]+"-"+str[6:8]+" "+str[8:10]+":"+str[10:12]+":"+str[12:14]
    # print(dateStr)
    return dateStr

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')