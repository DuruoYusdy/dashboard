import requests
from bs4 import BeautifulSoup
from .model import pourQStatu
from flask import jsonify

def update_cx_q():
    r3 = requests.get('http://activemq.fcgylapp.cn/admin/queues.jsp', auth=('admin', 'admin'))
    soup = BeautifulSoup(r3.text, 'html5lib')
    data_list = []
    for tab in soup.findAll('table', id='queues'):
        for idx, tr in enumerate(tab.find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                if ('_DEAD' not in tds[0].string):
                    qname = tds[0].string.replace('\n', '')
                    if ('OMS_PURCH_ORDERS_ERP_SUZHOU' in qname or 'OMS_TRADE_ORDERS_ERP_SUZHOU' in qname):
                        if (int(tds[1].string) <= 1000 and int(tds[2].string) == 2):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='11', type='chanxian')
                        elif(int(tds[1].string) <= 1000 and int(tds[2].string) != 2):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='10', type='chanxian')
                        elif (int(tds[1].string) > 1000 and int(tds[2].string) == 2):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='01', type='chanxian')
                        elif (int(tds[1].string) > 1000 and int(tds[2].string) != 2):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='00', type='chanxian')
                    else:
                        if (int(tds[1].string) <= 1000 and int(tds[2].string) == 1):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='11', type='chanxian')
                        elif(int(tds[1].string) <= 1000 and int(tds[2].string) != 1):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='10', type='chanxian')
                        elif (int(tds[1].string) > 1000 and int(tds[2].string) == 1):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='01', type='chanxian')
                        elif (int(tds[1].string) > 1000 and int(tds[2].string) != 1):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='00', type='chanxian')
                    data_list.append({
                        'name': qname,
                        'pend_num': tds[1].string,
                        'cos_num': tds[2].string,
                        'mess_enq': tds[3].string,
                        'mess_deq': tds[4].string
                    })

    return jsonify(data_list)

def update_yc_q():
    r3 = requests.get('http://activemq.yuncang.fcgylapp.cn/admin/queues.jsp', auth=('admin', 'admin'))
    soup = BeautifulSoup(r3.text, 'html5lib')
    data_list = []
    for tab in soup.findAll('table', id='queues'):
        for idx, tr in enumerate(tab.find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                if '_YCH_' not in tds[0].string:
                    qname = tds[0].string.replace('\n', '')
                    if int(tds[1].string) > 1000 or int(tds[2].string) != 1:
                        if (int(tds[1].string) > 1000 and int(tds[2].string) == 1):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='01', type='yuncang')
                        elif (int(tds[1].string) <= 1000 and int(tds[2].string) == 0):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='10', type='yuncang')
                        elif (int(tds[1].string) > 1000 and int(tds[2].string) == 0):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='00', type='yuncang')
                        else:
                            pass
                    else:
                        pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='11', type='yuncang')
                    data_list.append({
                        'name': qname,
                        'pend_num': tds[1].string,
                        'cos_num': tds[2].string,
                        'mess_enq': tds[3].string,
                        'mess_deq': tds[4].string
                    })
    return jsonify(data_list)

def update_ych_q():
    r3 = requests.get('http://ychcallback.fcgylapp.cn/admin/queues.jsp', auth=('admin', 'admin'))
    soup = BeautifulSoup(r3.text, 'html5lib')
    data_list = []
    for tab in soup.findAll('table', id='queues'):
        for idx, tr in enumerate(tab.find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                qname = tds[0].string.replace('\n', '')
                if("OMS_WMSCALLBACK_YCH_PRODUCTION" in qname and "_DEAD" not in qname):
                    if(int(tds[1].string) > 1000 or int(tds[2].string)!=1):
                        if(int(tds[1].string) > 1000 and int(tds[2].string)==1):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='01', type='callback')
                        elif (int(tds[1].string) <= 1000 and int(tds[2].string) == 0):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='10', type='callback')
                        elif (int(tds[1].string) > 1000 and int(tds[2].string) == 0):
                            pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='00', type='callback')
                        else:
                            pass
                    else:
                        pourQStatu(qname=qname, pend=tds[1].string, cos=tds[2].string, statu='11',type = 'callback')
                    data_list.append({
                        'name': qname,
                        'pend_num': tds[1].string,
                        'cos_num': tds[2].string,
                        'mess_enq': tds[3].string,
                        'mess_deq': tds[4].string
                    })

    return jsonify(data_list)
