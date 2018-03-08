# -*- coding:utf-8 -*-

from flask import render_template, jsonify, request
from . import app
from .config import url_tag,url_sku,url_base,url_distrib,url_singlep
from .model import getServerStatu,getQStatu,updateAlarm
from .UpdateQ import update_cx_q,update_yc_q,update_ych_q
import json

# 侧边栏对应的四个页面的url
@app.route('/')
def dashboard():
    return render_template('product.html',url_tag=url_tag,url_sku=url_sku,url_base=url_base,url_distrib=url_distrib,url_singlep=url_singlep )

@app.route('/yuncang')
def yuncang():
    return render_template('yuncang.html',url_tag=url_tag,url_sku=url_sku)

@app.route('/activemq')
def activemq():
    return render_template('activemq.html')

@app.route('/prod')
def prod():
    return render_template('prod.html')


# 打开关闭告警服务的api
@app.route('/api/alarmstatu',methods=['GET','POST'])
def alarm_statu():
    # 返回数据库中存储的openalarm列表，用于界面上switch按钮开关状态的持久化显示
    if(request.method == 'GET'):
        status = getServerStatu()
        dict = {}
        for server in status:
            dict[server.servername] = server.openalarm
        return jsonify(dict)

    # 接收页面上switch按钮的值，用于控制是否打开告警
    elif(request.method == 'POST'):
        temp = request.form
        for i in temp:
            temp = json.loads(i)
            servername = temp['servername'][1:]
            alarm_statu = temp['alarm_statu']
            updateAlarm(servername,alarm_statu)
        return True

# 获取server数据库中状态的api
@app.route('/api/dashboard')
def dash_api():
    status = getServerStatu()
    dict = {}
    for server in status:
        dict[server.servername] = server.statu
    return jsonify(dict)

# 获取activemq数据库中状态的api
@app.route('/api/activemq')
def activemq_api():
    status = getQStatu()
    list = []
    for q in status:
        dict = {}
        dict['qname'] = q.qname
        dict['qstatu'] = q.statu
        dict['type'] = q.type
        list.append(dict)
    return jsonify(list)


# 以下三个api用于接受q的三个图表的ajax请求
@app.route('/api/cx_activemq')
def cx_activemq():
    data = update_cx_q()
    return data


@app.route('/api/yc_activemq')
def yc_activemq():
    data = update_yc_q()
    return data


@app.route('/api/ychcallback')
def ychcallback():
    data = update_ych_q()
    return data

