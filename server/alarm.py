# -*- coding:utf-8 -*-

import requests
from datetime import datetime
from .config import url_sku
import json

# 服务告警
def throwAlarm(servername,log=""):
    if('tag_' in servername):
        errormessage = {'msg': '{}: | 快发波次告警！：Dashboard Down | Service {} has errors ! '  \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), servername)}
    elif ('sku_' in servername):
        r = requests.get(url_sku[servername])
        info = json.loads(r.text)
        errormessage = {'msg': '{}: | Sku 告警！：Dashboard Down | Service {} has errors ! info:{}' \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), servername, info['sku']['msg'])}
    elif ('base_' in servername):
        errormessage = {'msg': '{}: | 基础服务告警！：Dashboard Down | Service {} has errors ! {} ' \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), servername,log)}
    else:
        errormessage = {'msg': '{}: | 服务告警！：Dashboard Down | Service {} has errors ! ' \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), servername)}
    requests.post('http://test.fcgylapp.cn:9191/dingding/chat/3/', data=errormessage)

# 服务恢复
def throwRecover(servername,time):
    message = {'msg': '{}:服务恢复！Dashboard Up | Service {} back to normal ! | duration time : {}s '. \
        format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), servername,time)}
    requests.post('http://test.fcgylapp.cn:9191/dingding/chat/3/', data = message)


def alarm_control(instruct,servername,begintime = datetime.now(),log=""):
    if(instruct == 'alarm'):
        throwAlarm(servername,log)
    elif(instruct == 'recover'):
        nowtime = datetime.now()
        oldtime = datetime.strptime(begintime, "%Y-%m-%d %H:%M:%S")
        time = (nowtime - oldtime).seconds
        throwRecover(servername,time)
    else:
        print('you throw an unknown instruct')


def throwqAlarm(qname,pend,cos,type,info):
    if(type == 'callback'):
        errormessage = {'msg': '{}: | 御城河ActiveMQ告警！：ActiveMQ down |  {} has errors !\n {}----- pend_num:{} cos_num:{} ' \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), qname, info,pend,cos)}
        requests.post('http://test.fcgylapp.cn:9191/dingding/chat/3/', data=errormessage)
    elif (type == 'chanxian'):
        errormessage = {'msg': '{}: | 产线ActiveMQ告警！：ActiveMQ down |  {} has errors !\n {}----- pend_num:{} cos_num:{} ' \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), qname, info, pend, cos)}
        requests.post('http://test.fcgylapp.cn:9191/dingding/chat/3/', data=errormessage)
    elif (type == 'yuncang'):
        errormessage = {'msg': '{}: | 云仓ActiveMQ告警！：ActiveMQ down |  {} has errors !\n {}----- pend_num:{} cos_num:{} ' \
            .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), qname, info, pend, cos)}
        requests.post('http://test.fcgylapp.cn:9191/dingding/chat/3/', data=errormessage)


def throwqRecover(qname,pend,cos,info,time):
    message = {'msg': '{}:ActiveMQ恢复！ActiveMQ up |  {} back to normal ! |\n {}----- pend_num:{} cos_num:{}\n 耗费时长：{}s'. \
        format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), qname,info,pend,cos,time)}
    requests.post('http://test.fcgylapp.cn:9191/dingding/chat/3/', data = message)


def qalarm_control(instruct,qname,pend,cos,statu,type, begintime = datetime.now()):
    if (instruct == 'alarm'):
        if(statu=='01'):
            throwqAlarm(qname, pend, cos, type, 'info: pend-num 超1000了：')
        elif(statu=='10'):
            throwqAlarm(qname, pend, cos, type, 'info: cos-num 不正常：')
        elif(statu=='00'):
            throwqAlarm(qname, pend, cos, type, 'info: pend-num 与 cos-num 出错：')
        else:
            pass
    elif (instruct == 'recover'):
        nowtime = datetime.now()
        oldtime = datetime.strptime(begintime, "%Y-%m-%d %H:%M:%S")
        time = (nowtime - oldtime).seconds
        if(statu == 'pend'):
            throwqRecover(qname, pend, cos, 'pend-num 恢复正常了', time)
        elif(statu == 'cos'):
            throwqRecover(qname, pend, cos, 'cos-num 恢复正常了', time)
        pass
    else:
        print('you throw an unknown instruct')

