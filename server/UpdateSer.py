# -*- coding:utf-8 -*-


import requests
from requests import exceptions
from  .model import pourServerStatu
from .config import url_tag,url_sku,url_distrib,url_singlep,url_base
from .BaseStatu import es71_statu,es111_statu,mongo111_statu,redis125_statu,redis43_statu
import json


def update_tag_statu():
    for servername in url_tag:
        url = url_tag[servername]
        try:
            r = requests.get(url,timeout=2)
            if (r.text == '200'):
                pourServerStatu(servername, '1')
            else:
                pourServerStatu(servername, '0')
        except exceptions.Timeout as e:
            print(e)
            pourServerStatu(servername, '3')
        except exceptions.HTTPError as e:
            print(e)
            pourServerStatu(servername, '3')


def update_sku_statu():
    for servername in url_sku:
        url = url_sku[servername]
        try:
            r = requests.get(url,timeout=2)
            data = json.loads(r.text)
            if (data['success'] and data['sku']['activeSkuInEs']>0):
                pourServerStatu(servername, '1')
            elif(data['success'] and data['sku']['activeSkuInEs']==0 and data['sku']['activeSkuInDb']==0):
                pourServerStatu(servername, '1')
            else:
                pourServerStatu(servername, '0')
        except exceptions.Timeout as e:
            print(e)
            pourServerStatu(servername, '3')
        except exceptions.HTTPError as e:
            print(e)
            pourServerStatu(servername, '3')


def update_base_statu():
    url = url_base['base_ES-JVM111']
    r = requests.get(url)
    data = json.loads(r.text)
    if (data['nodes']['He5j8ObLT2auTW0kMu75Kw']['jvm']['mem']['heap_used_percent'] < 80):
        pourServerStatu('base_ES-JVM111', '1')
    else:
        percent = data['nodes']['He5j8ObLT2auTW0kMu75Kw']['jvm']['mem']['heap_used_percent']
        pourServerStatu('base_ES-JVM111', '0', log=percent)
   
    url = url_base['base_ES-JVM71']
    r = requests.get(url)
    data = json.loads(r.text)
    if (data['nodes']['wQW5N2oOQKOcwl4_Qb5nrg']['jvm']['mem']['heap_used_percent'] < 75):
        pourServerStatu('base_ES-JVM71', '1')
    else:
        pourServerStatu('base_ES-JVM71', '0')  

    if(es71_statu()):
        pourServerStatu('base_ES-71','1')
    else:
        pourServerStatu('base_ES-71','0')
    if(es111_statu()):
        pourServerStatu('base_ES-111','1')
    else:
        pourServerStatu('base_ES-111','0')
    if(mongo111_statu()):
        pourServerStatu('base_mongo-111', '1')
    else:
        pourServerStatu('base_mongo-111', '0')
    if(redis125_statu()):
        pourServerStatu('base_redis-125','1')
    else:
        pourServerStatu('base_redis-125','0')
    if (redis43_statu()):
        pourServerStatu('base_redis-43', '1')
    else:
        pourServerStatu('base_redis-43', '0')
    


def update_distrib_statu():
    for servername in url_distrib:
        url = url_distrib[servername]
        try:
            r = requests.get(url, timeout=2)
            if (r.text == '200'):
                pourServerStatu(servername,'1')
            elif ('reportserver' in servername and r.text == 'Hey man!'):
                pourServerStatu(servername,'1')
            else:
                pourServerStatu(servername,'0')
        except exceptions.Timeout as e:
            print(e)
            pourServerStatu(servername,'3')
        except exceptions.HTTPError as e:
            print(e)
            pourServerStatu(servername,'3')



def update_singlep_statu():
    for servername in url_singlep:
        url = url_singlep[servername]
        try:
            r = requests.get(url, timeout=2)
            if (r.text == '200'):
                pourServerStatu(servername, '1')
            elif ('contactservice' in servername and r.text == 'done'):
                pourServerStatu(servername, '1')
            elif ('taggingservice' in servername and 'Hello World From taggingservice' in r.text):
                pourServerStatu(servername, '1')
            elif ('skuservice' in servername and 'Welcome to SKU Service !' in r.text):
                pourServerStatu(servername, '1')
            else:
                pourServerStatu(servername, '0')
        except exceptions.Timeout as e:
            print(e)
            pourServerStatu(servername, '3')
        except exceptions.HTTPError as e:
            print(e)
            pourServerStatu(servername, '3')
