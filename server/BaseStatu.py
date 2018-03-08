# -*- coding:utf-8 -*-
# 对基础服务进程状态的监控，返回true or false

import paramiko
import os,subprocess,commands


private_key = paramiko.RSAKey.from_private_key_file('/home/tomcat/.ssh/id_rsa')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def es111_statu():
    ssh.connect(hostname=ECS111,port=22,username='tomcat',pkey=private_key)
    stdin,stdout,stderr=ssh.exec_command('ps -ef|grep elasticsearch |grep -v grep')
    result=stdout.read()
    ssh.close()
    if('elasticsearch-2.4.0.jar' in result.decode()):
        return True
    else:
        return False

def mongo111_statu():
    ssh.connect(hostname=ECS111, port=22, username='tomcat', pkey=private_key)
    stdin, stdout, stderr = ssh.exec_command('ps -ef|grep mongod |grep -v grep')
    result = stdout.read()
    ssh.close()
    if ('mongod' in result.decode()):
        return True
    else:
        return False

def es71_statu():
   #ssh.connect(hostname=ECS71, port=22, username='tomcat', pkey=private_key)
   #stdin, stdout, stderr = ssh.exec_command('ps -ef|grep elasticsearch |grep -v grep')
   #result = stdout.read()
   #ssh.close()
   #n = os.system('ps -ef|grep elasticsearch |grep -v grep')
    (status,output)=commands.getstatusoutput('ps -ef|grep elasticsearch |grep -v grep')
    if ('elasticsearch-2.2.0.jar' in output):
        return True
    else:
        return False

def redis125_statu():
    ssh.connect(hostname=ECS125, port=22, username='tomcat', pkey=private_key)
    stdin, stdout, stderr = ssh.exec_command('ps -ef|grep redis-server |grep -v grep')
    result = stdout.read()
    ssh.close()
    if ('redis-server' in result.decode()):
        return True
    else:
        return False

def redis43_statu():
    ssh.connect(hostname=ECS43, port=22, username='tomcat', pkey=private_key)
    stdin, stdout, stderr = ssh.exec_command('ps -ef|grep redis-server |grep -v grep')
    result = stdout.read()
    ssh.close()
    if ('redis-server' in result.decode()):
        return True
    else:
        return False
