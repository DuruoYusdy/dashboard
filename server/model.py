# -*- coding:utf-8 -*-

from . import db
from .alarm import alarm_control,qalarm_control
from datetime import datetime



class ServerStatu(db.Model):
    __tablename__ = 'serverstatus'

    id = db.Column(db.Integer,primary_key=True)
    servername = db.Column(db.String(64))
    statu = db.Column(db.String(64))
    begintime = db.Column(db.String(512))
    openalarm = db.Column(db.String(64),default='true')

    def __init__(self,servername,statu):
        self.servername = servername
        self.statu = statu

    def setbegin(self,time):
        self.begintime = time

    def setalarm(self,alarm_statu):
        self.openalarm = alarm_statu


class ActiveMQStatu(db.Model):
    __tablename__ = 'qstatus'

    id = db.Column(db.Integer, primary_key=True)
    qname = db.Column(db.String(64))
    statu = db.Column(db.String(64))
    pend_num = db.Column(db.String(64))
    cos_num = db.Column(db.String(64))
    pwrog_begin = db.Column(db.String(512))
    cwrog_begin = db.Column(db.String(512))
    type = db.Column(db.String(64))

    def __init__(self, qname, statu, pnum, cnum ,type):
        self.qname = qname
        self.statu = statu
        self.pend_num = pnum
        self.cos_num = cnum
        self.type = type

    def setbegin0(self, pwrog):
        self.pwrog_begin = pwrog

    def setbegin1(self, cwrog):
        self.cwrog_begin = cwrog


def getAlarm():
    status = ServerStatu.query.all()
    db.session.commit()
    return status


def updateAlarm(servername,alarm_statu):
    serverstatu = db.session.query(ServerStatu).filter_by(servername = servername).first()
    serverstatu.setalarm(alarm_statu)
    db.session.commit()


# 对数据库中serverstatu进行添加或者更新处理
def pourServerStatu(servername,statu,log=""):
    serverstatu = db.session.query(ServerStatu).filter_by(servername = servername).first()
    if(serverstatu):
        if(serverstatu.openalarm == "true"):
            if(statu == '0'):
                alarm_control('alarm', servername,log)
            if(serverstatu.statu == '1' and statu == '0'):
                serverstatu.setbegin(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if (serverstatu.statu == '3' and statu == '0'):
                serverstatu.setbegin(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if(serverstatu.statu == '0' and statu == '1'):
                alarm_control('recover', servername, serverstatu.begintime)   # 恢复告警
        else:
            # print(serverstatu.servername)
            pass
        serverstatu.statu = statu
    else:
        if(statu=='0'):
            alarm_control('alarm',servername,log)
        db.session.add(ServerStatu(servername,statu))
    db.session.commit()

# 获取serverstatu
def getServerStatu():
    status = ServerStatu.query.all()
    db.session.commit()
    return status


def pourQStatu(qname,pend,cos,statu,type):
    qstatu = db.session.query(ActiveMQStatu).filter_by(qname = qname).first()
    if(qstatu):
        if(qstatu.statu[0]=='0' and statu[0]=='1'):
            qalarm_control('recover', qname, pend, cos, 'pend', type, qstatu.pwrog_begin)
        elif (qstatu.statu[1] == '0' and statu[1] == '1'):
            qalarm_control('recover', qname, pend, cos, 'cos' , type,  qstatu.cwrog_begin)
        elif (qstatu.statu[0] == '1' and statu[0] == '0'):
            qstatu.setbegin0(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            qalarm_control('alarm', qname, pend, cos, statu, type)
        elif (qstatu.statu[1] == '1' and statu[1] == '0'):
            qstatu.setbegin1(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            qalarm_control('alarm', qname, pend, cos, statu, type)
        qstatu.statu = statu
    else:
        # if ('0' in statu):
        #     qalarm_control('alarm', qname, pend, cos, statu, type)
        db.session.add(ActiveMQStatu(qname,statu,pend,cos,type))
    db.session.commit()


# 获取qstatu
def getQStatu():
    qstatus = ActiveMQStatu.query.all()
    db.session.commit()
    return qstatus


# 对数据库中qstatu进行添加或者更新处理
# pend,cos为关键的两个监控参数，用于传递给告警服务和保存到数据库
# statu为1时q正常，为0时q不正常,type用于识别是产线，云仓，还是御城河回调，用于传递给告警服务
# def pourQStatu(qname,pend,cos,statu,type):
#     qstatu = db.session.query(ActiveMQStatu).filter_by(qname = qname).first()
#     if(qstatu):
#         if('0' in statu):
#             if(statu == '01'):
#                 qalarm_control('alarm',qname,pend,cos,type)
#             elif (statu == '10'):
#                 qalarm_control('alarm', qname, pend, cos, type)
#             elif (statu == '00'):
#                 qalarm_control('alarm', qname, pend, cos, type)
#         elif('0' in qstatu.statu and statu == '11'):
#             qalarm_control('recover', qname,pend,cos,type)
#         else:
#             pass
#         qstatu.statu = statu
#     else:
#         if('0' in statu):
#             qalarm_control('alarm',qname,pend,cos,type)
#         db.session.add(ActiveMQStatu(qname,statu,pend,cos))
#     db.session.commit()

