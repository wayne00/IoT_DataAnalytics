from flask import Flask,render_template,url_for,request

import pymysql
import json

app = Flask(__name__)


@app.route('/',methods=['get','post'])
def index():
    return render_template('dynamicData4.html')


@app.route('/orders/<int:order_id>')
def get_order_id(order_id):
    return 'order_id %s' %order_id


@app.route('/test', methods=['GET','POST'])
def my_echart():
    data = []
    print("==========come to test ==================")

    strf = str(request.get_data().decode())[16:30]
    datef = str2date(strf)

    conn = pymysql.connect(host='', user='', password='', db='')
    cur = conn.cursor()
    sql = 'SELECT * FROM plc_data t where tm > \'%s\' ' %(datef)

    print(sql)

    cur.execute(sql)
    u = cur.fetchall()

    for dt in u:
        oneData = {}
        oneData['name'] = dt[2].strftime('%Y/%m/%d %H:%M:%S')
        oneData['value'] = [dt[2].strftime('%Y/%m/%d %H:%M:%S'), dt[3]]

        print(oneData['name'])
        print(oneData['value'])
        data.append(oneData)

    j = json.dumps(data)

    cur.close()
    conn.close()

    return j


@app.route('/init', methods=['GET', 'POST'])
def my_initEchart():
    print("==========come to init ==================")
    conn = pymysql.connect(host='', user='', password='', db='')
    cur = conn.cursor()
    sql = 'select * from plc_data t order by tm asc'
    cur.execute(sql)
    u = cur.fetchall()

    data=[]

    for dt in u:
        oneData = {}
        oneData['name'] = dt[2].strftime('%Y/%m/%d %H:%M:%S')
        year = str(dt[2].year)
        month = str(dt[2].month+1)
        day = str(dt[2].day)
        oneData['value'] = [year+"/"+month+"/"+day, dt[3]]

        print(oneData['name'])
        print(oneData['value'][0])
        print(oneData['value'][1])

        data.append(oneData)

    j = json.dumps(data)

    cur.close()
    conn.close()
    print("=========end init =====================")
    return j

def str2date(str):
    # 20190512000000
    dateStr = str[0:4]+"-"+str[4:6]+"-"+str[6:8]+" "+str[8:10]+":"+str[10:12]+":"+str[12:14]
    print(dateStr)
    return dateStr

if __name__ == '__main__':
    app.run(debug=True)