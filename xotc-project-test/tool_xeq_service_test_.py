#!/usr/bin/python
#-*- coding: UTF-8 -*-
#lvzhuqang at 2023.3.17：可用于定价平台计算服务主要场景的测试
#
# 

import json
import datetime
import base64
import hashlib
import sys
import random
import threading
import time
import requests
import logging
import hashlib
from urllib.parse import urlencode
import configparser

#系统参数
g_sysParams = {}
#如果uToken为空，则每次都会尝试登录
COOKIES = {"Cookie": ""}

g_iniFileName = './ini/xeq.ini'

#-------------------通用方法(begin)-----------------------------------


def LogMsg(strLogMsg,level):
    nowDay = datetime.datetime.now()
    strLogMsg = nowDay.strftime("%Y-%m-%d %H:%M:%S ->") + strLogMsg
    if level > 0:
        logging.info(strLogMsg)
    print(strLogMsg)

#get http request
def httpGetRequest(requestUrl,cookies,params):
    
    inParams = urlencode(params)
    fullUrl = requestUrl + "?"+ inParams
    response = requests.get(fullUrl,cookies = cookies)
    resBuf = response.text
    return resBuf

def httpGetRequestAuth(requestUrl,cookies,params):
    
    inParams = urlencode(params)
    fullUrl = requestUrl + "?"+ inParams

    headers = {  
        'Authorization': 'Bearer '+  cookies['uToken']
    }
    response = requests.get(fullUrl,cookies = cookies, headers=headers)
    resBuf = response.text
    return resBuf   
 


#post http request
def httpPostRequestJson(requestUrl,cookies,params):


    #关闭长连接
    headers = {'Content-Type':'application/json','Connection':'close'}

    requests.adapters.DEFAULT_RETRIES = 5
    #字典方式
    response = requests.post(requestUrl,headers=headers,json=params,cookies=cookies)
 
    resBuf = response.text
    response.close()
    return resBuf


def httpPostRequestJsonAuth(requestUrl,cookies,params):


    #关闭长连接
    headers = {'Content-Type':'application/json','Connection':'close','Authorization': 'Bearer '+  cookies['uToken']}
    requests.adapters.DEFAULT_RETRIES = 5
    #字典方式
    response = requests.post(requestUrl,headers=headers,json=params,cookies=cookies)
 
    resBuf = response.text
    response.close()
    return resBuf

def httpPostRequestUrl(requestUrl,cookies,data):


    #关闭长连接
    headers = {'Content-Type':'application/x-www-form-urlencoded','Connection':'close'}

    requests.adapters.DEFAULT_RETRIES = 5
    #字典方式
    response = requests.post(requestUrl,headers=headers,data=data,cookies=cookies)
 
    resBuf = response.text
    response.close()
    return resBuf

def httpPutRequest(requestUrl,cookies,params):

    '''
    #浏览器的原生 form 表单，如果不设置 enctype 属性，那么最终就会以 application/x-www-form-urlencoded 方式提交数据。
    #headers = {'Content-Type':'application/x-www-form-urlencoded'}
    #常见的POST 数据提交的方式。我们使用表单上传文件时，必须让 form 的 enctyped 等于这个值
    #headers = {'Content-Type':'multipart/form-data '}
    #它是一种使用 HTTP 作为传输协议，XML 作为编码方式的远程调用规范。
    headers = {'Content-Type':'text/xml'}
    '''

    headers = {'Content-Type':'application/json','Connection':'close','Authorization': 'Bearer '+  cookies['uToken']}  
    #postData = json.dumps(params)
    #print(postData)
    #json方式
    #response = requests.post(requestUrl,json=postData)
    #字典方式
    response = requests.put(requestUrl,json=params,headers=headers)
    resBuf = response.text
    return resBuf

def httpDeleteRequest(requestUrl,cookies):
    headers = {'Content-Type':'application/json','Connection':'close','Authorization': 'Bearer '+  cookies['uToken']}  
    response = requests.delete(requestUrl,headers=headers)
    resBuf = response.text
    return resBuf


#-------------------通用方法(end)-----------------------------------
#系统启动的时候加载和设置参数
def loadParamsIniFile():
    #logging模块设置
    logging.basicConfig(filename='./log/output.log', level=logging.INFO)

    # 类实例化
    config = configparser.ConfigParser() 
    config.read(g_iniFileName,encoding='utf-8')
    g_sysParams['serviceUrl'] = config['sys']['url']
    g_sysParams['uToken'] = config['sys']['token']
    g_sysParams['lastLogin'] = config['sys']['last_login']
    g_sysParams['userName'] = config['sys']['userName']
    g_sysParams['userPwd'] = config['sys']['userPwd']
    #g_sysParams['maxThreads'] = int(config['sys']['maxThreads'])
    #g_sysParams['maxCalcs'] = int(config['sys']['maxCalcs'])

    COOKIES['uToken'] = g_sysParams['uToken']
    print (g_sysParams)

def setParamsIniFile(uToken):
    config = configparser.ConfigParser() 
    config.read(g_iniFileName)
    #config.read('./ficc.ini')
    config.set('sys','token',uToken)
    config.set('sys','last_login',str((int)(time.time())) )
    config.write(open(g_iniFileName,'w+'))  
    print('setParamsIniFile of token:{}'.format(uToken))


#密码md5加密
def getEncodePwd(pwd):

    #dbPwnd = 'Xpar'+'Admin'+'123456'
    #str = '123456'
    # 创建md5加密对象
    md5 = hashlib.md5()     
    # 指定需要加密的字符串            
    md5.update(pwd.encode('utf-8'))   
    # 加密后的字符串  
    str_md5 = md5.hexdigest()          
    # 结果：e10adc3949ba59abbe56e057f20f883e
    return str_md5
    #print(str_md5)                      



def ssoLoginSystem():

    loginLong = (int)(time.time()) - int(g_sysParams['lastLogin'])
    #6小时后，自动再次登录
    if loginLong < 6*3600:
        return 1
    LogMsg('token失效，重新登录...',1)

    params = {}
    params['username'] = 'admin'
    params['password'] = '123456'

    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += '/sso/login'

    print('sso login params is {}'.format(params))
    headers = {'Content-Type':'application/json','Connection':'close'}
    response = requests.post(requestUrl,headers=headers,json=params)
    print(response)
    try:
        errorCode = -1
        respJson = json.loads(response.text)
        print(response.text)

        if respJson != None:
            token  = respJson['data']['token']
            print('token is {}'.format(token))

            g_sysParams['uToken'] =  token
            COOKIES['uToken'] = g_sysParams['uToken'] 
            setParamsIniFile(g_sysParams['uToken'])
    except Exception as e:
        print('exception is {}',e)
        print(e)

    if len(g_sysParams['uToken']) < 1:
        return 0
    return 1


def testForFpml():

    methodUrl = '/ttrdOtcEquitySwap'
    
    #params = {}

    irStream = {}
    irStream['isPayer'] = 'false'
    irStream['currency'] = 'CNY'
    irStream['dayCounter'] = 'Actual/365 (Fixed)'
    irStream['effectiveDate'] ='2007-09-27'
    irStream['terminationDate'] ='2010-09-27'
    irStream['calcPeriodFreq'] = '3M'
    irStream['calcConv'] = 'Unadjusted'
    irStream['calcCalendar'] = 'CHINA_IB'
    irStream['paymentConv'] = 'ModifiedFollowing'
    irStream['paymentCalendar'] = 'CHINA_IB'
    irStream['paymentFreq'] = '3M'
    irStream['fixingDayOffset'] = '-1D'
    irStream['fixingConv'] = 'Unadjusted'
    irStream['fixingCalendar'] = 'CHINA_IB'
    irStream['resetFreq'] = '3M'
    irStream['resetConv'] = 'ModifiedFollowing'
    irStream['resetCalendar'] = 'CHINA_IB'


    notional = {}
    notional['initValue'] = 100.0
    irStream['notional'] = notional

    irStream['floatingRateIndex'] = 'SHIBOR-1Y-10d,SPT_IBOR,X_CNBD'
    
    frate = {}
    frate['initValue'] = 1.0
    irStream['floatingRateMultiplier'] = frate

    coupon = {}
    coupon['initValue'] = 0.0029;
    irStream['coupon'] = coupon

    irStream['compoundingType'] = 'NoneCompounding'

    instrument = {}
    instrument['instrumentID'] = 'Bond_Normal_Floating,SPT_BD,X_CNBD'
    instrument['productType'] = 'BOND'

    instrument['irStream'] = irStream
    instrument['issuePrice'] = 100.000000

    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
    print(json.dumps(instrument))
    #resBuf = httpPostRequestUrl(requestUrl,COOKIES,instrument)
    resBuf = httpPostRequestJson(requestUrl,COOKIES,instrument)
    print(resBuf)


def testForCustomType():

    methodUrl = '/trade/group/type/list'
    params = {} 
    params['pageSize'] = 10
    params['pageNum'] = 1  
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
    print(requestUrl)

    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)

def testForTradeGroupList():
    
    methodUrl = '/trade/group/list/'
    params = {} 
    params['pageSize'] = 5
    params['pageNum'] = 1
    #params['condition'] = 'group_lzq_test_06'
    params['customType'] = '对冲'
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl

    print(requestUrl)

    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)

def testForTradeGroupDetail():
    methodUrl = '/trade/group/'
    params = {} 
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
    requestUrl += '00065030'    
    print(requestUrl)

    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)

def testForAddTradeGroup():
    methodUrl = '/trade/group/add'
    params = {} 
    params['grpName'] = 'group_lzq_test_1115_01'
    params['customType'] = '对冲'
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl 
    #print(requestUrl)

    resBuf = httpPostRequestJsonAuth(requestUrl,COOKIES,params)
    print(resBuf)

def testForUpdateTradeGroup():
    methodUrl = '/trade/group/update'
    params = {} 
    params['grpId'] = '00065120'
    params['grpName'] = 'group_lzq_test_1114_02'
    #params['customType'] = '海鸥变形'
    params['customType'] = '对冲'
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl

    #print(requestUrl)
    resBuf = httpPutRequest(requestUrl,COOKIES,params)
    print(resBuf)

def testForOtcTradeList():
    methodUrl = '/trade/group/otclist'
    params = {}
    params['grpId'] = '00065197'
    params['customType'] = '对冲'
    params['pageSize'] = 3
    params['pageNum'] = 1
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
 
    print(requestUrl)
    print(params)

    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)

def testForDeleteTradeGroup():
    methodUrl = '/trade/group/delete/'
    params = {}

    grpId = '00065032'
    #grpId = '00057592'
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
    requestUrl += grpId
    print(requestUrl)

    resBuf = httpDeleteRequest(requestUrl,COOKIES)
    print(resBuf)


def testForAddToGroup():
    methodUrl = '/trade/group/trade/add'
    params = {} 
    params['sysOrdIds'] = '302490,302489,302483,302481,302462,302411,302342,302340,302339,302338'
    params['grpName'] = '空白144233'
    params['grpId'] = '00065411'
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl 

    resBuf = httpPostRequestJsonAuth(requestUrl,COOKIES,params)
    print(resBuf)

def testQueryTradeList():
    

    methodUrl = '/xirOtcOptionTrade/queryTradeList.action/'
    params = {} 
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
    params['pageSize'] = 10
    params['pageNum'] = 1
    params['endDate'] = '2023-11-2'
    params['IsForward'] = 'false'
    params['orderCol'] = 'ORDSTATUS'
    params['orderBy'] = 'DESC'

    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)


def testQueryTradeConfirmList():
    

    methodUrl = '/trade/confirm/list'
    params = {} 
    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl
    params['pageSize'] = 10
    params['pageNum'] = 1
    params['tradeBegTime'] = '2023-01-01'
    params['tradeEndTime'] = '2023-01-01'


    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)





def initFlowSteps(sysOrdId):
    stepList = []

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''
    stepItem['stepName'] = '报文发送'
    stepItem['stepId'] = 'SENDPACKAGE'
    stepItem['busNodeName'] = '交易确认'
    stepList.append(stepItem)

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''
    stepItem['stepName'] = '报文匹配'
    stepItem['stepId'] = 'FITPACKAGE'
    stepItem['busNodeName'] = '交易确认'
    stepList.append(stepItem)   


    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''
    stepItem['stepName'] = '交易确认'
    stepItem['stepId'] = 'TRADECONFIRM'
    stepItem['busNodeName'] = '交易确认'
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''
    stepItem['stepName'] = '主管审批'
    stepItem['stepId'] = 'SETTLEAUDIT1'
    stepItem['busNodeName'] = '清算审批'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '负责人审批'
    stepItem['stepId'] = 'SETTLEAUDIT2'
    stepItem['busNodeName'] = '清算审批'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '副总审批'
    stepItem['stepId'] = 'SETTLEAUDIT3'
    stepItem['busNodeName'] = '清算审批'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem)

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '轧差'
    stepItem['stepId'] = 'NETTINGMERGE'
    stepItem['busNodeName'] = '外汇双边净额结算'
    stepItem['feeAmount'] = 0
    stepItem['nettingResult'] = '1'
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '核准'
    stepItem['stepId'] = 'NETTINGCHECK'
    stepItem['busNodeName'] = '外汇双边净额结算'
    stepItem['feeAmount'] = 0
    stepItem['nettingResult'] = '1'
    stepList.append(stepItem) 


    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '主管审批'
    stepItem['stepId'] = 'FINANCEAUDIT1'
    stepItem['busNodeName'] = '财务审批'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '负责人审批'
    stepItem['stepId'] = 'FINANCEAUDIT2'
    stepItem['busNodeName'] = '财务审批'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '副总审批'
    stepItem['stepId'] = 'FINANCEAUDIT3'
    stepItem['busNodeName'] = '财务审批'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem)

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '经办'
    stepItem['stepId'] = 'HANDLING'
    stepItem['busNodeName'] = '指令结算'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '复核'
    stepItem['stepId'] = 'CHECKING'
    stepItem['busNodeName'] = '指令结算'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem) 

    stepItem = {}
    stepItem['sysOrdId'] = sysOrdId
    stepItem['instId'] = ''    
    stepItem['stepName'] = '报文发送'
    stepItem['stepId'] = 'SENDPACKAGE2'
    stepItem['busNodeName'] = '指令结算'
    stepItem['feeAmount'] = 6000
    stepList.append(stepItem)

    return stepList

def testQueryFlowLogs():
    methodUrl = '/workflow/log'
    params = {} 
    params['sysOrdId'] = '306596'
    params['instId'] = ''
    params['stepName'] = ''
    params['stepId'] = ''
    params['busNodeName'] = ''

    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl 
    startTime = (int)(time.time()*1000)
    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)
    endTime = (int)(time.time()*1000)
    print('cost time of :{}.'.format(endTime - startTime))

def testStartProcess(sysOrdId):
    methodUrl = '/workflow/start'
    params = {} 
    params['sysOrdId'] = sysOrdId
    params['instId'] = ''
    params['stepName'] = ''
    params['stepId'] = ''
    params['busNodeName'] = ''

    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl 

    resBuf = httpPostRequestJsonAuth(requestUrl,COOKIES,params)
    print(resBuf)
    time.sleep(2)

def testCompleteProcess(sysOrdId):
    methodUrl = '/workflow/complete'

    stepList = initFlowSteps(sysOrdId)

    testStep = 'SENDPACKAGE'
    testStep = '*'
    testStep = 'SENDPACKAGE2'
    for stepItem in stepList:
        params =  stepItem
        if len(testStep) > 0:
            stepId = stepItem['stepId']
            if testStep != stepId and testStep != '*':
                continue
        print('start flow of stepId={},stepName={},nodeName={} .'.format(stepItem['stepId'],stepItem['stepName'],stepItem['busNodeName']))

        requestUrl = g_sysParams['serviceUrl'] 
        requestUrl += methodUrl 

        resBuf = httpPostRequestJsonAuth(requestUrl,COOKIES,params)
        print(resBuf)
       
        time.sleep(1)

def testQueryUserDemo():
    methodUrl = '/user/demo/list/v2'
    params = {} 
    params['userId'] = '1'


    requestUrl = g_sysParams['serviceUrl'] 
    requestUrl += methodUrl 
    startTime = (int)(time.time()*1000)
    print(requestUrl)
    resBuf = httpGetRequestAuth(requestUrl,COOKIES,params)
    print(resBuf)
    endTime = (int)(time.time()*1000)
    print('cost time of :{}.'.format(endTime - startTime))


def testTradeGroup():
    #testForCustomType()
    #testForTradeGroupList()
    
    #testForTradeGroupDetail()
    
    #testForAddTradeGroup()
    #testForUpdateTradeGroup()
    #testForOtcTradeList()
    #testForDeleteTradeGroup()
    #testForAddToGroup()
    #testQueryTradeList()
    #testQueryTradeConfirmList()
    #testStartProcess('306621')
    #testCompleteProcess('306608')
    #testQueryFlowLogs()
    testQueryUserDemo()

if __name__ == "__main__":

 
    loadParamsIniFile()
    if ssoLoginSystem() == 1:
        testTradeGroup()
        
    
    
