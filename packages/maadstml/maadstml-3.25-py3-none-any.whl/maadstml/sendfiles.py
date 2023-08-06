#############################################################
#
#  Author: Sebastian Maurice, PhD
#  Copyright by Sebastian Maurice 2018
#  All rights reserved.
#  Email: Sebastian.maurice@otics.ca
#
#############################################################

import json, urllib
import requests
import csv
import os
import imp
import re
import urllib.request
import asyncio
import validators
from urllib.parse import urljoin
from urllib.parse import urlsplit
import aiohttp
from aiohttp import ClientSession,ClientTimeout
import async_timeout
import readpdf


connectionerror=""

loop = asyncio.get_event_loop()

def cancelalltasks():
    try:
      pending = asyncio.all_tasks()
      for task in pending:
        task.cancel()
    except Exception as e:
      pass  

def formaturl(maindata,host,microserviceid,prehost,port):

    if len(microserviceid)>0:    
      mainurl=prehost + "://" + host +  ":" + str(port) +"/" + microserviceid + "/?hyperpredict=" + maindata
    else:
      mainurl=prehost + "://" + host + ":" + str(port) +"/?hyperpredict=" + maindata
        
    return mainurl
    
async def tcp_echo_client(message, loop,host,port,usereverseproxy,microserviceid):

    hostarr=host.split(":")
    hbuf=hostarr[0]
   # print(hbuf)
    hbuf=hbuf.lower()
    domain=''
    if hbuf=='https':
       domain=host[8:]
    else:
       domain=host[7:]
    host=domain  

    if usereverseproxy:
        geturl=formaturl(message,host,microserviceid,hbuf,port) #host contains http:// or https://
        message="GET %s\n\n" % geturl 

    reader, writer = await asyncio.open_connection(host, port, loop=loop)
    try:
      mystr=str.encode(message)
      writer.write(mystr)
      datam=''
      while True:
        data = await reader.read(1024)
      #  print(data)
        datam=datam+data.decode("utf-8")
       # print(datam)
        if not data:
           break
        
        await writer.drain()
   #   print(datam)  
      prediction=("%s" % (datam))
      writer.close()
    except Exception as e:
      print(e)
      return e
    
    return prediction

def hyperpredictions(maadstoken,pkey,theinputdata,host,port,usereverseproxy=0,microserviceid='',username='',password='',company='',email=''):
    if '_nlpclassify' not in pkey:
      theinputdata=theinputdata.replace(",",":")
    else:  
      buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', theinputdata)
      buf2=buf2.replace("\n", "").strip()
      buf2=buf2.replace("\r", "").strip()
      theinputdata=buf2

    if usereverseproxy:
       theinputdata=urllib.parse.quote(theinputdata)
  
    value="%s,[%s],%s" % (pkey,theinputdata,maadstoken)
    loop = asyncio.new_event_loop()
    val=loop.run_until_complete(tcp_echo_client(value, loop,host,port,usereverseproxy,microserviceid))
    loop.close()

    return val
#########################################################
#######################VIPER Functions

def formaturlviper(maindata,host,microserviceid,prehost,port):

    if len(microserviceid)>0:    
      mainurl=prehost + "://" + host +  ":" + str(port) +"/" + microserviceid + "/" + maindata
    else:
      mainurl=prehost + "://" + host + ":" + str(port) +"/" + maindata
        
    return mainurl


async def fetch(client,url):
    async with client.get(url) as resp:
        #asycio.ensure_future()
        return await resp.text()

async def fetch2(client,url):
    tasks = []
    tasks.append(asyncio.ensure_future(fetch(client, url)))
    original = await asyncio.gather(*tasks)
    for info in original:
        return info
    
#############################VIPER API CALLS ################    
async def tcp_echo_clientviper(message, loop,host,port,microserviceid,timeout=600):
    global connectionerror

    connectionerror=""
    hostarr=host.split(":")
    hbuf=hostarr[0]
    hbuf=hbuf.lower()
    domain=''
    if hbuf=='https':
       domain=host[8:]
    else:
       domain=host[7:]
    host=domain  

    geturl=formaturlviper(message,host,microserviceid,hbuf,port) #host contains http:// or https://
    message="%s" % geturl
    stimeout = ClientTimeout(total=timeout)
     
    try:
     with async_timeout.timeout(timeout):
      async with ClientSession(connector = aiohttp.TCPConnector(ssl=False),timeout=stimeout) as session:
        try:
          html = await fetch2(session,message)
          await session.close()
          return html
        except Exception as e:
          print(e)
          pass
    except (aiohttp.ServerDisconnectedError, aiohttp.ClientResponseError,aiohttp.ClientConnectorError) as e:       
     connectionerror=str(e)   
     print("TCPConnectionError=",e)   
     pass   


def viperstats(vipertoken,host,port=-999,brokerhost='',brokerport=-999,microserviceid=''):
    global connectionerror

    if len(vipertoken)==0 or len(host)==0 or port==-999:
       return "Please enter vipertoken,host and port"

    value="viperstats?vipertoken="+vipertoken + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
    loop = asyncio.new_event_loop()
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    loop.close()
    if connectionerror:
         return connectionerror

    return val


def viperlisttopics(vipertoken,host,port=-999,brokerhost='',brokerport=-999,microserviceid=''):
    global connectionerror

    if len(vipertoken)==0 or len(host)==0 or port==-999:
       return "Please enter vipertoken,host and port"
    
    value="listtopics?vipertoken="+vipertoken + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipersubscribeconsumer(vipertoken,host,port,topic,companyname,contactname,contactemail,location,description,brokerhost='',brokerport=-999,groupid='',microserviceid=''):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(companyname)==0 or len(contactname)==0 or len(contactemail)==0 or len(location)==0 or len(description)==0:
         return "Please enter host,port,vipertoken,topic, companyname,contactname,contactemail,location and description"
        
    value=("subscribeconsumer?vipertoken="+vipertoken + "&topic="+topic + "&companyname=" + companyname + "&contactname="+contactname +
           "&contactemail="+contactemail + "&location="+location+"&description="+description+ "&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&groupid=" + groupid)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val


def viperunsubscribeconsumer(vipertoken,host,port,consumerid,brokerhost='',brokerport=-999,microserviceid=''):
    global connectionerror

    if len(vipertoken)==0 or len(consumerid)==0 or len(host)==0:
         return "Please enter vipertoken,consumerid,host and port"
        
    value=("unsubscribeconsumer?vipertoken="+vipertoken + "&consumerid="+consumerid + "&brokerhost="+brokerhost +"&brokerport="+str(brokerport))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val


def vipermirrorbrokers(vipertoken,host,port,brokercloudusernamepassfrom,brokercloudusernamepassto,enabletlsfrom,enabletlsto,
                                          replicationfactorfrom,replicationfactorto,compressionfrom,compressionto,
                                          saslfrom,saslto,partitions,brokerlistfrom,brokerlistto,                                         
                                          topiclist,asynctimeout=300,microserviceid="",servicenamefrom="broker",servicenameto="broker",
                                          partitionchange=0,replicationchange=0,topicfilter="",rollbackoffset=0):
    global connectionerror


    if (len(host)==0 or len(vipertoken)==0 or len(brokercloudusernamepassfrom)==0 or len(brokercloudusernamepassto)==0
         or len(enabletlsfrom)==0 or len(enabletlsto)==0 
         or len(compressionfrom)==0 or len(compressionto)==0 or len(saslfrom)==0 or len(saslto)==0
         or len(brokerlistfrom)==0 or  len(brokerlistto)==0 ):
          return ("Please enter host,port,vipertoken,brokercloudusernamepassfrom, brokercloudusernamepassto, enabletlsfrom,\
enabletlsto,compressionfrom,compressionto,saslfrom,saslto,brokerlistfrom,brokerlistto")
    
    value=("writestreamtobrokers?vipertoken="+vipertoken + "&enabletlsfrom="+enabletlsfrom + "&enabletlsto=" + enabletlsto
           + "&replicationfactorfrom=" + replicationfactorfrom + "&replicationfactorto=" + replicationfactorto
           + "&compressionfrom=" + compressionfrom + "&compressionto=" + compressionto +  "&saslfrom="+saslfrom
           + "&saslto="+saslto+"&partitions="+partitions + "&servicenamefrom="+servicenamefrom + "&servicenameto=" + servicenameto 
           + "&brokerlistfrom=" + brokerlistfrom + "&brokerlistto=" + brokerlistto +  "&topiclist=" + topiclist
           + "&brokercloudusernamepassfrom=" + urllib.parse.quote(brokercloudusernamepassfrom) + "&brokercloudusernamepassto=" + urllib.parse.quote(brokercloudusernamepassto)
           + "&rollbackoffset=" + str(rollbackoffset) + "&changepartitionperc=" + str(partitionchange) + "&changereplication=" + str(replicationchange)
           + "&filter=" + topicfilter)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))

    if connectionerror:
         return connectionerror

    return val

def viperstreamquerybatch(vipertoken,host,port,topic,producerid,offset=-1,maxrows=0,enabletls=1,delay=100,brokerhost='',
                                          brokerport=-999,microserviceid='',topicid="-999",streamstojoin='',preprocessconditions='',
                                          identifier='',preprocesstopic='',description='',array=0,timedelay=0,asynctimeout=120,
                                          wherecondition='',wheresearchkey='PreprocessIdentifier',rawdataoutput=1):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0 or len(streamstojoin)==0 or len(preprocessconditions)==0:
         return "Please enter host,port,vipertoken,topic, producerid, streamstojoin, preprocessconditions"
    
    value=("streamquerybatch?vipertoken="+vipertoken + "&topicname="+topic + "&producerid=" + producerid + "&offset=" + str(offset)
           + "&maxrows=" + str(maxrows) + "&delay=" + str(delay) +  "&enabletls="+str(enabletls)
           + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport) + "&streamstojoin="+streamstojoin + "&topicid=" + topicid 
           + "&identifier=" + identifier + "&preprocesstopic=" + str(preprocesstopic) +  "&description=" + str(description)
           + "&preprocessconditions=" + preprocessconditions + "&array=" + str(array)+ "&timedelay=" + str(timedelay)+ "&wherecondition=" + wherecondition
           + "&wheresearchkey=" + wheresearchkey + "&rawdataoutput=" + str(rawdataoutput))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))

    if connectionerror:
         return connectionerror

    return val

def viperstreamquery(vipertoken,host,port,topic,producerid,offset=-1,maxrows=0,enabletls=1,delay=100,brokerhost='',
                                          brokerport=-999,microserviceid='',topicid=-999,streamstojoin='',preprocessconditions='',
                                          identifier='',preprocesstopic='',description='',array=0, wherecondition='',
                                          wheresearchkey='PreprocessIdentifier',rawdataoutput=1):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0 or len(streamstojoin)==0 or len(preprocessconditions)==0:
         return "Please enter host,port,vipertoken,topic, producerid, streamstojoin, preprocessconditions"
    
    value=("streamquery?vipertoken="+vipertoken + "&topicname="+topic + "&producerid=" + producerid + "&offset=" + str(offset)
           + "&maxrows=" + str(maxrows) + "&delay=" + str(delay) +  "&enabletls="+str(enabletls)
           + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport) + "&streamstojoin="+streamstojoin + "&topicid=" + str(topicid) 
           + "&identifier=" + identifier + "&preprocesstopic=" + str(preprocesstopic) +  "&description=" + str(description)
           + "&preprocessconditions=" + preprocessconditions + "&array=" + str(array) + "&wherecondition=" + wherecondition
           + "&wheresearchkey=" + wheresearchkey + "&rawdataoutput=" + str(rawdataoutput))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))

    if connectionerror:
         return connectionerror

    return val


def viperstreamcluster(vipertoken,host,port,topic,producerid,offset=-1,maxrows=0,enabletls=1,delay=100,brokerhost='',
                                          brokerport=-999,microserviceid='',topicid=-999,iterations=1000, numclusters=8,
                                          distancealgo=1,description='',rawdataoutput=0,valuekey='',filterkey='',groupkey='',
                                          identifier='',datetimekey='',valueidentifier='',msgid='',valuecondition='',
                                          identifierextractpos='',preprocesstopic='',
                                          alertonclustersize=0,alertonsubjectpercentage=50,sendalertemailsto='',emailfrequencyinseconds=0,
                                          companyname='',analysisdescription='',identifierextractposlatitude=-1,
                                          identifierextractposlongitude=-1,identifierextractposlocation=-1,
                                          identifierextractjoinedidentifiers=-1,pdfformat='',minimumsubjects=2):

                                          
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  or len(valuekey)==0 or len(msgid)==0 or len(datetimekey)==0:
         return "Please enter host,port,vipertoken,topic,valuekey, msgid,datetimekey"
    
    value=("streamcluster?vipertoken="+vipertoken + "&topicname="+topic + "&producerid=" + producerid + "&offset=" + str(offset)
           + "&maxrows=" + str(maxrows) + "&delay=" + str(delay) +  "&enabletls="+str(enabletls)
           + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport) + "&iterations="+ str(iterations) + "&numclusters=" + str(numclusters) 
           + "&distancealgo=" + str(distancealgo) + "&rawdataoutput=" + str(rawdataoutput)
           + "&valuekey=" + valuekey + "&filterkey=" + filterkey+ "&groupkey=" + groupkey+ "&identifier=" + identifier
           + "&datetimekey=" + datetimekey + "&valueidentifier=" + valueidentifier + "&msgid=" + msgid
           + "&valuecondition=" + valuecondition + "&identifierextractpos=" + identifierextractpos
           + "&alertonclustersize=" + str(alertonclustersize) +"&sendalertemailsto=" + sendalertemailsto
           + "&emailfrequencyinseconds=" + str(emailfrequencyinseconds)
           + "&preprocesstopic=" + preprocesstopic + "&companyname=" + companyname
           + "&description=" + description + "&analysisdescription=" + analysisdescription
           + "&identifierextractposlatitude=" + str(identifierextractposlatitude) + "&identifierextractposlongitude=" + str(identifierextractposlongitude)
           + "&identifierextractposlocation=" + str(identifierextractposlocation)
           + "&identifierextractjoinedidentifiers=" + str(identifierextractjoinedidentifiers)
           + "&pdfformat=" + pdfformat + "&alertonsubjectpercentage=" + str(alertonsubjectpercentage) + "&minimumsubjects=" + str(minimumsubjects))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))

    if connectionerror:
         return connectionerror

    return val

def viperstreamcorr(vipertoken,host,port,topic,producerid,offset=-1,maxrows=0,enabletls=1,delay=100,brokerhost='',
                                          brokerport=-999,microserviceid='',topicid=-999,streamstojoin='',
                                          identifier='',preprocesstopic='',description='',array=0, wherecondition='',
                                          wheresearchkey='PreprocessIdentifier',rawdataoutput=0,threshhold=0,pvalue=0,
                                          identifierextractpos="",topcorrnum=5,jsoncriteria='',tmlfilepath='',usemysql=0,
                                          pathtotmlattrs='',mincorrvectorlen=5,writecorrstotopic='',
                                          outputtopicnames=0,nlp=0,correlationtype='',docrosscorr=0 ):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0:
         return "Please enter host,port,vipertoken,topic"
    
    value=("streamcorr?vipertoken="+vipertoken + "&topicname="+topic + "&producerid=" + producerid + "&offset=" + str(offset)
           + "&maxrows=" + str(maxrows) + "&delay=" + str(delay) +  "&enabletls="+str(enabletls)
           + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport) + "&streamstojoin="+streamstojoin + "&topicid=" + str(topicid) 
           + "&identifier=" + identifier + "&preprocesstopic=" + str(preprocesstopic) +  "&description=" + str(description)
           + "&array=" + str(array) + "&wherecondition=" + wherecondition
           + "&wheresearchkey=" + wheresearchkey + "&rawdataoutput=" + str(rawdataoutput) + "&threshhold=" + str(threshhold)
           + "&pvalue=" + str(pvalue) + "&identifierextractpos=" + identifierextractpos+ "&topcorrnum="
           + str(topcorrnum) + "&jsoncriteria=" + jsoncriteria + "&tmlfilepath=" + tmlfilepath + "&usemysql=" + str(usemysql)
           +  "&pathtotmlattrs=" + pathtotmlattrs + "&mincorrvectorlen=" + str(mincorrvectorlen)
           + "&writecorrstotopic=" + writecorrstotopic + "&outputtopicnames=" + str(outputtopicnames)
           + "&nlp=" + str(nlp) + "&correlationtype=" + correlationtype + "&docrosscorr=" + str(docrosscorr))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))

    if connectionerror:
         return connectionerror

    return val
        
def viperproducetotopic(vipertoken,host,port,topic,producerid,enabletls=1,delay=100,inputdata='',maadsalgokey='',maadstoken='',
                        getoptimal=0,externalprediction='',subtopics='',topicid=-999,identifier='',array=0,
                        brokerhost='',brokerport=-999,microserviceid=''):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0:
         return "Please enter host,port,vipertoken,topic, producerid"

    
    value=("producetotopic?vipertoken="+vipertoken + "&topic="+topic + "&producerid=" + producerid + "&getoptimal="+str(getoptimal) +
          "&delay=" + str(delay) +  "&enabletls="+str(enabletls)+ "&externalprediction="+externalprediction + "&inputdata="+inputdata +
           "&maadsalgokey="+maadsalgokey +"&maadstoken="+maadstoken + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
           + "&subtopics="+subtopics + "&topicid=" + str(topicid) + "&identifier=" + identifier + "&array=" + str(array))

           
    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val


def viperproducetotopicbulk(vipertoken,host,port,topic,producerid,inputdata,partitionsize=100,enabletls=1,delay=100,brokerhost='',brokerport=-999,microserviceid=''):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0 or len(inputdata)==0:
         return "Please enter host,port,vipertoken,topic, producerid,inputdata"
        
    value=("producetotopicbulk?vipertoken="+vipertoken + "&topic="+topic + "&producerid=" + producerid + 
          "&delay=" + str(delay) +  "&enabletls="+str(enabletls)+ "&externalprediction="+inputdata +
          "&brokerhost="+brokerhost+"&brokerport="+str(brokerport) + "&partitionsize="+str(partitionsize)) 

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperconsumefromtopicbatch(vipertoken,host,port,topic,consumerid,companyname,partition=-1,enabletls=0,delay=100,offset=0,brokerhost='',
                          brokerport=-999,microserviceid='',topicid='-999',rollbackoffsets=0,preprocesstype='',timedelay=0,asynctimeout=120):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  or len(companyname)==0:
         return "Please enter host,port,vipertoken,topic,companyname"
        
    value=("consumefromtopicbatch?vipertoken="+vipertoken + "&topic="+topic + "&consumerid=" + consumerid + "&offset="+str(offset) +
      "&partition=" + str(partition) +  "&delay=" + str(delay) +  "&enabletls=" + str(enabletls) + "&brokerhost="+brokerhost
           + "&brokerport="+str(brokerport)+"&companyname="+companyname + "&topicid=" + topicid +
           "&rollbackoffsets=" + str(rollbackoffsets) + "&preprocesstype=" + preprocesstype+ "&timedelay=" + str(timedelay))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror

    return val

def viperconsumefromtopic(vipertoken,host,port,topic,consumerid,companyname,partition=-1,enabletls=0,delay=100,offset=0,brokerhost='',
                          brokerport=-999,microserviceid='',topicid='-999',rollbackoffsets=0,preprocesstype=''):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  or len(companyname)==0:
         return "Please enter host,port,vipertoken,topic,companyname"
        
    value=("consumefromtopic?vipertoken="+vipertoken + "&topic="+topic + "&consumerid=" + consumerid + "&offset="+str(offset) +
      "&partition=" + str(partition) +  "&delay=" + str(delay) +  "&enabletls=" + str(enabletls) + "&brokerhost="+brokerhost
           + "&brokerport="+str(brokerport)+"&companyname="+companyname + "&topicid=" + topicid +
           "&rollbackoffsets=" + str(rollbackoffsets) + "&preprocesstype=" + preprocesstype)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperhpdepredictbatch(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,inputdata,maxrows=0,algokey='',partition=-1,offset=-1,
                     enabletls=1,delay=100,hpdeport=-999,brokerhost='',brokerport=9092,
                     timeout=120,usedeploy=0,microserviceid='',topicid="-999", maintopic='', streamstojoin='',array=0,timedelay=0,
                     asynctimeout=120,pathtoalgos=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or
        len(companyname)==0 or len(hpdehost)==0 or hpdeport==-999 or len(pathtoalgos)==0):
         return "Please enter host,port,vipertoken,consumefrom,inputdata,produceto,companyname,hpdehost,hpdeport,pathtoalgos"
        
    value=("viperhpdepredictbatch?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&delay=" + str(delay) + "&inputdata="+ inputdata + "&algokey="+algokey + "&maxrows=" +
           str(maxrows) + "&partition="+str(partition)+"&offset="+str(offset)+ "&enabletls=" + str(enabletls)
           + "&producerid="+producerid + "&usedeploy=" +str(usedeploy) +"&companyname="+companyname + "&hpdehost="
           +hpdehost +"&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) +
           "&topicid=" + topicid + "&maintopic=" + maintopic + "&streamstojoin=" + streamstojoin + "&array=" +
           str(array)+ "&timedelay=" + str(timedelay) + "&pathtoalgos="+pathtoalgos)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror
    
    return val

def viperhpdepredict(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,inputdata,maxrows=0,algokey='',partition=-1,offset=-1,
                     enabletls=1,delay=1000,hpdeport=-999,brokerhost='',brokerport=9092,
                     timeout=120,usedeploy=0,microserviceid='',topicid=-999, maintopic='',
                     streamstojoin='',array=0,pathtoalgos=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or
        len(companyname)==0 or len(hpdehost)==0 or hpdeport==-999 or len(pathtoalgos)==0):
         return "Please enter host,port,vipertoken,consumefrom,inputdata,produceto,companyname,hpdehost,hpdeport,pathtoalgos"
        
    value=("viperhpdepredict?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&delay=" + str(delay) + "&inputdata="+ inputdata + "&algokey="+algokey + "&maxrows=" +
           str(maxrows) + "&partition="+str(partition)+"&offset="+str(offset)+ "&enabletls=" + str(enabletls)
           + "&producerid="+producerid + "&usedeploy=" +str(usedeploy) +"&companyname="+companyname + "&hpdehost="
           +hpdehost +"&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) +
           "&topicid=" + str(topicid) + "&maintopic=" + maintopic + "&streamstojoin=" + streamstojoin + "&array=" + str(array) +
           "&pathtoalgos="+pathtoalgos)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,timeout))
    if connectionerror:
         return connectionerror
    
    return val

def viperhpdepredictprocess(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,inputdata,processtype,maxrows=0,algokey='',partition=-1,offset=-1,
                     enabletls=1,delay=1000,hpdeport=-999,brokerhost='',brokerport=9092,
                     timeout=120,usedeploy=0,microserviceid='',topicid=-999, maintopic='',
                     streamstojoin='',array=0,pathtoalgos=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or
        len(companyname)==0 or len(hpdehost)==0 or hpdeport==-999 or len(pathtoalgos)==0 or len(processtype)==0):
         return "Please enter host,port,vipertoken,consumefrom,inputdata,produceto,companyname,hpdehost,hpdeport,pathtoalgos,processtype"
        
    value=("viperhpdepredictprocess?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&delay=" + str(delay) + "&inputdata="+ inputdata + "&algokey="+algokey + "&maxrows=" +
           str(maxrows) + "&partition="+str(partition)+"&offset="+str(offset)+ "&enabletls=" + str(enabletls)
           + "&producerid="+producerid + "&usedeploy=" +str(usedeploy) +"&companyname="+companyname + "&hpdehost="
           +hpdehost +"&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) +
           "&topicid=" + str(topicid) + "&maintopic=" + maintopic + "&streamstojoin=" + streamstojoin + "&array=" + str(array) +
           "&pathtoalgos="+pathtoalgos + "&processtype="+processtype)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,timeout))
    if connectionerror:
         return connectionerror
    
    return val

def viperhpdeoptimizebatch(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,partition=-1,offset=-1,
                      enabletls=1,delay=100,hpdeport=-999,usedeploy=0,
                      ismin=1,constraints='best',stretchbounds=20,constrainttype=1,epsilon=10,brokerhost='',brokerport=9092,
                      timeout=120,microserviceid='',topicid="-999",timedelay=0,asynctimeout=120):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(companyname)==0
        or len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,hpdehost,hpdeport"
        
    value=("viperhpdeoptimizebatch?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
         "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&producerid="+producerid + "&companyname="+companyname +
         "&partition="+str(partition)+"&offset="+str(offset)+"&ismin="+str(ismin)+"&constraints="+constraints+"&stretchbounds="+str(stretchbounds)+
         "&hpdehost=" +hpdehost +"&hpdeport="+str(hpdeport) + "&usedeploy=" +str(usedeploy) + "&constrainttype=" +str(constrainttype) +"&epsilon=" +
           str(epsilon) + "&topicid=" + topicid + "&timedelay=" + str(timedelay))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror

    return val

def viperhpdeoptimize(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,partition=-1,offset=-1,
                      enabletls=1,delay=1000,hpdeport=-999,usedeploy=0,
                      ismin=1,constraints='best',stretchbounds=20,constrainttype=1,epsilon=10,brokerhost='',brokerport=9092,
                      timeout=120,microserviceid='',topicid=-999):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(companyname)==0
        or len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,hpdehost,hpdeport"
        
    value=("viperhpdeoptimize?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
         "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&producerid="+producerid + "&companyname="+companyname +
         "&partition="+str(partition)+"&offset="+str(offset)+"&ismin="+str(ismin)+"&constraints="+constraints+"&stretchbounds="+str(stretchbounds)+
         "&hpdehost=" +hpdehost +"&hpdeport="+str(hpdeport) + "&usedeploy=" +str(usedeploy) + "&constrainttype=" +str(constrainttype) +"&epsilon=" +str(epsilon) + "&topicid=" + str(topicid) )

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,timeout))
    if connectionerror:
         return connectionerror

    return val

def viperhpdetraining(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,deploy=0,modelruns=10,modelsearchtuner=80,hpdeport=-999,offset=-1,islogistic=0,
                      brokerhost='',brokerport=9092,timeout=120,microserviceid='',topicid=-999,maintopic='',
                      independentvariables='',dependentvariable='',rollbackoffsets=0,fullpathtotrainingdata='',processlogic='',
                      identifier='',array=0,transformtype='',sendcoefto='',coeftoprocess='',coefsubtopicnames=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999  or len(produceto)==0 or len(companyname)==0 or
        len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,hpdehost,hpdeport"
    if (islogistic==1 and processlogic==''):
         return "Since you are doing logistic, please enter processlogic"
        
    value=("viperhpdetraining?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&producerid="+producerid + "&companyname="+companyname + "&partition="+str(partition)+"&modelruns="+str(modelruns) +"&hpdehost=" +hpdehost +
           "&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost+ "&modelsearchtuner="+str(modelsearchtuner)+ "&offset="+str(offset) + "&viperconfigfile="+viperconfigfile +
           "&brokerport="+str(brokerport)+"&enabletls="+str(enabletls) +"&deploy="+str(deploy) + "&islogistic=" + str(islogistic) +
           "&timeout="+str(timeout) + "&topicid=" + str(topicid) + "&maintopic=" + maintopic + "&independentvariables=" + independentvariables +
           "&dependentvariable=" + dependentvariable + "&rollbackoffsets=" + str(rollbackoffsets)+
           "&fullpathtotrainingdata="+fullpathtotrainingdata + "&processlogic=" + processlogic+ "&identifier=" + identifier +
           "&array=" + str(array) + "&transformtype=" + transformtype + "&sendcoefto=" + sendcoefto + "&coeftoprocess=" + coeftoprocess +
           "&coefsubtopicnames=" + coefsubtopicnames)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,timeout))
    if connectionerror:
         return connectionerror

    return val

def viperhpdetrainingbatch(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,deploy=0,modelruns=10,modelsearchtuner=80,hpdeport=-999,offset=-1,islogistic=0,
                      brokerhost='',brokerport=9092,timeout=120,microserviceid='',topicid="-999",maintopic='',
                      independentvariables='',dependentvariable='',rollbackoffsets=0,fullpathtotrainingdata='',processlogic='',
                      identifier='',array=0,timedelay=0,asynctimeout=120):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999  or len(produceto)==0 or len(companyname)==0 or
        len(hpdehost)==0 or hpdeport==-999):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,hpdehost,hpdeport"
    if (islogistic==1 and processlogic==''):
         return "Since you are doing logistic, please enter processlogic"
        
    value=("viperhpdetrainingbatch?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&producerid="+producerid + "&companyname="+companyname + "&partition="+str(partition)+"&modelruns="+str(modelruns) +"&hpdehost=" +hpdehost +
           "&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost+ "&modelsearchtuner="+str(modelsearchtuner)+ "&offset="+str(offset) + "&viperconfigfile="+viperconfigfile +
           "&brokerport="+str(brokerport)+"&enabletls="+str(enabletls) +"&deploy="+str(deploy) + "&islogistic=" + str(islogistic) +
           "&timeout="+str(timeout) + "&topicid=" + topicid + "&maintopic=" + maintopic + "&independentvariables=" + independentvariables +
           "&dependentvariable=" + dependentvariable + "&rollbackoffsets=" + str(rollbackoffsets)+
           "&fullpathtotrainingdata="+fullpathtotrainingdata + "&processlogic=" + processlogic+ "&identifier=" + identifier + "&array="
           + str(array)+ "&timedelay=" + str(timedelay))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror

    return val

def viperanomalytrainbatch(vipertoken,host,port,consumefrom,produceto,producepeergroupto,produceridpeergroup,consumeridproduceto,
                      streamstoanalyse,
                      companyname,consumerid,producerid,flags,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,hpdeport=-999,topicid="-999",maintopic='',rollbackoffsets=0,fullpathtotrainingdata='',
                      brokerhost='',brokerport=9092,delay=1000,timeout=120,microserviceid='',timedelay=0,asynctimeout=120):
    global connectionerror

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(produceto)==0 or len(companyname)==0
                or len(hpdehost)==0 or hpdeport==-999 or len(streamstoanalyse)==0 or len(producepeergroupto)==0
                or len(flags)==0 or len(viperconfigfile)==0):
         return "Please enter host,port,vipertoken,produceto,companyname,streamstoanalyse,flags,producepeergroupto,hpdehost,hpdeport"
    
    value=("viperanomalytrainbatch?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&producepeergroupto=" + producepeergroupto + "&produceridpeergroup=" + produceridpeergroup + "&consumeridproduceto="+consumeridproduceto +
           "&streamstoanalyse="+streamstoanalyse + "&flags="+flags + "&delay=" +str(delay) + "&timeout=" + str(timeout) +
           "&producerid="+producerid + "&companyname="+companyname + "&partition="+str(partition) +"&hpdehost=" +hpdehost +
           "&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&viperconfigfile="+viperconfigfile +
           "&brokerport="+str(brokerport)+"&enabletls="+str(enabletls) +"&topicid=" + topicid + "&maintopic=" + maintopic +
           "&rollbackoffsets=" + str(rollbackoffsets) + "&fullpathtotrainingdata="+fullpathtotrainingdata+ "&timedelay=" + str(timedelay))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror

    return val

def viperanomalytrain(vipertoken,host,port,consumefrom,produceto,producepeergroupto,produceridpeergroup,consumeridproduceto,
                      streamstoanalyse,
                      companyname,consumerid,producerid,flags,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,hpdeport=-999,topicid=-999,maintopic='',rollbackoffsets=0,fullpathtotrainingdata='',
                      brokerhost='',brokerport=9092,delay=1000,timeout=120,microserviceid=''):
    global connectionerror

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(produceto)==0 or len(companyname)==0
                or len(hpdehost)==0 or hpdeport==-999 or len(streamstoanalyse)==0 or len(producepeergroupto)==0
                or len(flags)==0 or len(viperconfigfile)==0):
         return "Please enter host,port,vipertoken,produceto,companyname,streamstoanalyse,flags,producepeergroupto,hpdehost,hpdeport"
    
    value=("viperanomalytrain?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&producepeergroupto=" + producepeergroupto + "&produceridpeergroup=" + produceridpeergroup + "&consumeridproduceto="+consumeridproduceto +
           "&streamstoanalyse="+streamstoanalyse + "&flags="+flags + "&delay=" +str(delay) + "&timeout=" + str(timeout) +
           "&producerid="+producerid + "&companyname="+companyname + "&partition="+str(partition) +"&hpdehost=" +hpdehost +
           "&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&viperconfigfile="+viperconfigfile +
           "&brokerport="+str(brokerport)+"&enabletls="+str(enabletls) +"&topicid="+str(topicid) + "&maintopic=" + maintopic +
           "&rollbackoffsets=" + str(rollbackoffsets) + "&fullpathtotrainingdata="+fullpathtotrainingdata)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,timeout))
    if connectionerror:
         return connectionerror

    return val

def viperanomalypredictbatch(vipertoken,host,port,consumefrom,produceto,consumeinputstream,produceinputstreamtest,produceridinputstreamtest,
                      streamstoanalyse,consumeridinputstream,
                      companyname,consumerid,producerid,flags,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,hpdeport=-999,topicid="-999",maintopic='',rollbackoffsets=0,fullpathtopeergroupdata='',
                      brokerhost='',brokerport=9092,delay=1000,timeout=120,microserviceid='',timedelay=0,asynctimeout=120):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(produceto)==0 or len(companyname)==0 
                 or len(hpdehost)==0 or hpdeport==-999 or len(streamstoanalyse)==0 
                 or len(flags)==0 or len(viperconfigfile)==0):
         return "Please enter host,port,vipertoken,produceto,companyname,streamstoanalyse,flags,consumerid,hpdehost,hpdeport"
        
    value=("viperanomalypredictbatch?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&produceinputstreamtest="+produceinputstreamtest + "&produceridinputstreamtest="+produceridinputstreamtest + "&consumeridinputstream="+consumeridinputstream+
           "&streamstoanalyse="+streamstoanalyse + "&flags="+flags + "&delay=" +str(delay) + "&timeout=" + str(timeout) +
           "&producerid="+producerid + "&companyname="+companyname + "&partition="+str(partition) +"&hpdehost=" +hpdehost +
           "&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&viperconfigfile="+viperconfigfile + "&consumeinputstream="+consumeinputstream+
           "&brokerport="+str(brokerport)+"&enabletls="+str(enabletls) + "&topicid=" + topicid + "&maintopic=" +maintopic
           + "&rollbackoffsets=" +str(rollbackoffsets)+ "&fullpathtopeergroupdata="+fullpathtopeergroupdata+ "&timedelay=" + str(timedelay))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror

    return val


def viperanomalypredict(vipertoken,host,port,consumefrom,produceto,consumeinputstream,produceinputstreamtest,produceridinputstreamtest,
                      streamstoanalyse,consumeridinputstream,
                      companyname,consumerid,producerid,flags,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,hpdeport=-999,topicid=-999,maintopic='',rollbackoffsets=0,fullpathtopeergroupdata='',
                      brokerhost='',brokerport=9092,delay=1000,timeout=120,microserviceid=''):

    #reads the fieldnames and gets latest data from each stream (or fieldname)
    global connectionerror
    
    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(produceto)==0 or len(companyname)==0 
                 or len(hpdehost)==0 or hpdeport==-999 or len(streamstoanalyse)==0 
                 or len(flags)==0 or len(viperconfigfile)==0):
         return "Please enter host,port,vipertoken,produceto,companyname,streamstoanalyse,flags,consumerid,hpdehost,hpdeport"
        
    value=("viperanomalypredict?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto=" + produceto + "&consumerid="+consumerid +
           "&produceinputstreamtest="+produceinputstreamtest + "&produceridinputstreamtest="+produceridinputstreamtest + "&consumeridinputstream="+consumeridinputstream+
           "&streamstoanalyse="+streamstoanalyse + "&flags="+flags + "&delay=" +str(delay) + "&timeout=" + str(timeout) +
           "&producerid="+producerid + "&companyname="+companyname + "&partition="+str(partition) +"&hpdehost=" +hpdehost +
           "&hpdeport="+str(hpdeport)+"&brokerhost="+brokerhost + "&viperconfigfile="+viperconfigfile + "&consumeinputstream="+consumeinputstream+
           "&brokerport="+str(brokerport)+"&enabletls="+str(enabletls) + "&topicid=" + str(topicid) + "&maintopic=" +maintopic
           + "&rollbackoffsets=" +str(rollbackoffsets)+ "&fullpathtopeergroupdata="+fullpathtopeergroupdata)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,timeout))
    if connectionerror:
         return connectionerror

    return val

def viperproducetotopicstream(vipertoken,host,port,topic,producerid,offset,maxrows=0,enabletls=0,delay=100,brokerhost='',brokerport=-999,microserviceid='',
                              topicid=-999,mainstreamtopic='',streamstojoin=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0):
         return "Please enter host,port,vipertoken,topic,producerid"
        
    value=("producetotopicstream?vipertoken="+vipertoken + "&topicname="+topic + "&delay=" + str(delay) + "&maxrows=" +str(maxrows) +
           "&enabletls="+str(enabletls) +"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&producerid="+producerid +
           "&offset="+str(offset) + "&topicid=" + str(topicid) + "&mainstreamtopic="+mainstreamtopic + "&streamstojoin="+streamstojoin)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

    
def viperpreprocessproducetotopicstream(vipertoken,host,port,topic,producerid,offset,maxrows=0,enabletls=0,delay=100,brokerhost='',brokerport=-999,microserviceid='',
                              topicid=-999,streamstojoin='',preprocesslogic='',preprocessconditions='',identifier='',preprocesstopic='',array=0,saveasarray=0,rawdataoutput=0):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0 or len(preprocesslogic)==0):
         return "Please enter host,port,vipertoken,topic,producerid,preprocesslogic"
        
    value=("preprocessproducetotopicstream?vipertoken="+vipertoken + "&topicname="+topic + "&delay=" + str(delay) + "&maxrows=" +str(maxrows) +
           "&enabletls="+str(enabletls) +"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&producerid="+producerid +
           "&offset="+str(offset) + "&topicid=" + str(topicid) + "&streamstojoin="+streamstojoin
           + "&preprocesslogic="+preprocesslogic + "&preprocessconditions=" + preprocessconditions
           + "&identifier=" + identifier + "&preprocesstopic=" + preprocesstopic + "&array=" + str(array)+
           "&saveasarray=" + str(saveasarray) + "&rawdataoutput=" + str(rawdataoutput) )

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))

    if connectionerror:
         return connectionerror

    return val

        
def vipersearchanomaly(vipertoken,host,port,topic,producerid,offset,jsoncriteria='',rawdataoutput=0,maxrows=0,enabletls=0,delay=100,
                       brokerhost='',brokerport=-999,microserviceid='',topicid=-999,identifier='',preprocesstopic='',
                       timedelay=0,asynctimeout=120,searchterms='',entitysearch='',tagsearch='',checkanomaly=1,testtopic='',
                       includeexclude=1,anomalythreshold=0,sendanomalyalertemail='',emailfrequency=3600):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(jsoncriteria)==0 or len(producerid)==0):
         return "Please enter host,port,vipertoken,topic,producerid, jsoncriteria"
            
    value=("nlpsearchanomaly?vipertoken="+vipertoken + "&topicname="+topic + "&delay=" + str(delay) + "&maxrows=" +str(maxrows) +
           "&enabletls="+str(enabletls) +"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&producerid="+producerid +
           "&offset="+str(offset) + "&topicid=" + str(topicid) + "&preprocesstopic=" + preprocesstopic + "&timedelay=" + str(timedelay) + "&jsoncriteria=" + jsoncriteria
           + "&rawdataoutput=" + str(rawdataoutput) + "&searchterms=" + searchterms + "&entitysearch=" + entitysearch
           + "&tagsearch=" + tagsearch + "&checkanomaly=" + str(checkanomaly) + "&testtopic=" + testtopic
           + "&includeexclude=" + str(includeexclude) + "&anomalythreshold=" + str(anomalythreshold)
           + "&sendanomalyalertemail=" + sendanomalyalertemail + "&emailfrequency=" + str(emailfrequency))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))

    if connectionerror:
         return connectionerror

    return val

def viperpreprocesscustomjson(vipertoken,host,port,topic,producerid,offset,jsoncriteria='',rawdataoutput=0,maxrows=0,enabletls=0,delay=100,brokerhost='',brokerport=-999,microserviceid='',
                              topicid=-999,streamstojoin='',preprocesslogic='',preprocessconditions='',identifier='',preprocesstopic='',
                              array=0,saveasarray=0,timedelay=0,asynctimeout=120,usemysql=0,tmlfilepath='',pathtotmlattrs=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(jsoncriteria)==0 or len(producerid)==0 or len(preprocesslogic)==0):
         return "Please enter host,port,vipertoken,topic,producerid,preprocesslogic, jsoncriteria"
            
    value=("preprocesscustomjson?vipertoken="+vipertoken + "&topicname="+topic + "&delay=" + str(delay) + "&maxrows=" +str(maxrows) +
           "&enabletls="+str(enabletls) +"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&producerid="+producerid +
           "&offset="+str(offset) + "&topicid=" + str(topicid) + "&streamstojoin="+streamstojoin
           + "&preprocesslogic="+preprocesslogic + "&preprocessconditions=" + preprocessconditions
           + "&identifier=" + identifier + "&preprocesstopic=" + preprocesstopic + "&array=" + str(array)+
           "&saveasarray=" + str(saveasarray) + "&timedelay=" + str(timedelay) + "&jsoncriteria=" + jsoncriteria
           + "&rawdataoutput=" + str(rawdataoutput) + "&usemysql=" + str(usemysql) + "&tmlfilepath=" + tmlfilepath + "&pathtotmlattrs=" + pathtotmlattrs )

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))

    if connectionerror:
         return connectionerror

    return val


def viperpreprocessbatch(vipertoken,host,port,topic,producerid,offset,maxrows=0,enabletls=0,delay=100,brokerhost='',brokerport=-999,microserviceid='',
                              topicid="-999",streamstojoin='',preprocesslogic='',preprocessconditions='',identifier='',preprocesstopic='',
                              array=0,saveasarray=0,timedelay=0,asynctimeout=120,rawdataoutput=0):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(producerid)==0 or len(preprocesslogic)==0):
         return "Please enter host,port,vipertoken,topic,producerid,preprocesslogic"
        
    value=("preprocessbatch?vipertoken="+vipertoken + "&topicname="+topic + "&delay=" + str(delay) + "&maxrows=" +str(maxrows) +
           "&enabletls="+str(enabletls) +"&brokerhost="+brokerhost + "&brokerport="+str(brokerport) + "&producerid="+producerid +
           "&offset="+str(offset) + "&topicid=" + topicid + "&streamstojoin="+streamstojoin
           + "&preprocesslogic="+preprocesslogic + "&preprocessconditions=" + preprocessconditions
           + "&identifier=" + identifier + "&preprocesstopic=" + preprocesstopic + "&array=" + str(array)+
           "&saveasarray=" + str(saveasarray) + "&timedelay=" + str(timedelay) + "&rawdataoutput=" + str(rawdataoutput))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid,asynctimeout))
    if connectionerror:
         return connectionerror

    return val


def vipercreatetrainingdata(vipertoken,host,port,consumefrom,produceto,dependentvariable,independentvariables,
                            consumerid,producerid,companyname,partition=-1,enabletls=0,delay=100,brokerhost='',brokerport=-999,
                            microserviceid='',topicid=-999):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(consumefrom)==0 or len(produceto)==0 or len(dependentvariable)==0 or
        len(independentvariables)==0 or len(companyname)==0 or len(consumerid)==0 or len(producerid)==0):
         return "Please enter host,port,vipertoken,consumefrom,produceto,companyname,consumerid,producerid"
        
    value=("createtrainingdata?vipertoken="+vipertoken + "&consumefrom="+consumefrom + "&produceto="+produceto +
           "&dependentvariable="+dependentvariable+"&independentvariables="+independentvariables +
           "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&partition="+str(partition)+"&consumerid="+consumerid +
           "&producerid="+producerid+"&companyname="+companyname + "&brokerhost="+brokerhost +
           "&brokerport="+str(brokerport) + "&topicid=" + str(topicid))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipercreatetopic(vipertoken,host,port,topic,companyname,contactname,contactemail,location,description,enabletls=0,brokerhost='',brokerport=-999,numpartitions=1,replication=1,microserviceid=''):
    global connectionerror
    
    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(companyname)==0 or len(contactname)==0 or len(contactemail)==0 or len(location)==0 or len(description)==0:
         return "Please enter host,port,vipertoken,topic, companyname,contactname,contactemail,location and description"
        
    value=("createtopics?vipertoken="+vipertoken + "&topic="+topic + "&companyname=" + companyname + "&contactname="+contactname +
           "&contactemail="+contactemail + "&location="+location+"&description="+description+ "&enabletls="+str(enabletls) + "&numpartitions="+str(numpartitions)+
           "&replicationfactor="+str(replication) + "&brokerhost="+brokerhost + "&brokerport=" + str(brokerport) )


    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperconsumefromstreamtopic(vipertoken,host,port,topic,consumerid,companyname,partition=-1,enabletls=0,delay=100,offset=0,
                                brokerhost='',brokerport=-999,microserviceid='',topicid=-999):
    global connectionerror

    if len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0 or len(consumerid)==0 or len(companyname)==0:
         return "Please enter host,port,vipertoken,topic, consumerid,companyname"
        
    value=("consumefromstreamtopic?vipertoken="+vipertoken + "&topic="+topic + "&consumerid=" + consumerid + "&offset="+str(offset) +
        "&partition=" + str(partition) + "&delay=" + str(delay) + "&enabletls=" + str(enabletls) + "&brokerhost="+
        brokerhost + "&brokerport="+str(brokerport)+ "&companyname="+companyname + "&topicid=" + str(topicid))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val


def vipercreatejointopicstreams(vipertoken,host,port,topic,topicstojoin,companyname,contactname,contactemail,description,
                                location,enabletls=0,brokerhost='',brokerport=-999,replication=1,numpartitions=1,microserviceid='',topicid=-999):

    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(contactname)==0 or len(contactemail)==0 or len(description)==0 or
        len(location)==0 ):
         return "Please enter host,port,vipertoken,contactname,contactemail,companyname,description,location"
        
    value=("createjointopicstreams?vipertoken="+vipertoken + "&topicname="+topic + "&topicstojoin="+topicstojoin +
           "&companyname="+companyname+"&contactname="+contactname +"&contactemail="+contactemail+"&brokerhost="+brokerhost+"&brokerport="+str(brokerport)+
           "&enabletls=" + str(enabletls) + "&description="+description + "&location="+location+"&replicationfactor="+str(replication)+
           "&numpartitions="+str(numpartitions) + "&topicid=" + str(topicid))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipercreateconsumergroup(vipertoken,host,port,topic,groupname,companyname,contactname,contactemail,description,
                                location,enabletls=1,brokerhost='',brokerport=-999,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or len(topic)==0 or len(groupname)==0) or len(topic)==0:
         return "Please enter host,port,vipertoken,contactname,contactemail,companyname,description,location,groupname"
        
    value=("createconsumergroup?vipertoken="+vipertoken + "&topic="+topic + "&groupname="+groupname +
           "&companyname="+companyname+"&contactname="+contactname +"&contactemail="+contactemail+ "&enabletls="+str(enabletls)+
           "&description="+description + "&location="+location+"&brokerhost="+brokerhost+"&brokerport="+str(brokerport))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperconsumergroupconsumefromtopic(vipertoken,host,port,topic,consumerid,groupid,companyname,partition=-1,enabletls=1,delay=1000,
                                       offset=-1,rollbackoffset=0,brokerhost='',brokerport=-999,microserviceid='',preprocesstype=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or len(groupid)==0 or len(companyname)==0):
         return "Please enter host,port,vipertoken,companyname,groupid"
        
    value=("consumergroupconsumefromtopic?vipertoken="+vipertoken + "&topic="+topic + "&consumerid="+consumerid +
        "&partition=" + str(partition) +  "&delay=" + str(delay) + "&rollbackoffset=" + str(rollbackoffset)
           + "&enabletls=" + str(enabletls) + "&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
           +"&offset="+str(offset) +"&companyname="+companyname+"&groupid="+groupid + "&preprocesstype=" +
           preprocesstype)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipermodifyconsumerdetails(vipertoken,host,port,topic,companyname,consumerid,contactname='',contactemail='',location='',brokerhost='',brokerport=9092,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(companyname)==0 or len(consumerid)==0 ):
         return "Please enter host,port,vipertoken,consumerid,companyname,consumerid"
        
    value=("modifyconsumerdetails?vipertoken="+vipertoken + "&topic="+topic + "&consumerid="+consumerid +"&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
            +"&companyname="+companyname+"&contactname="+contactname+"&contactemail="+contactemail+"&location="+location)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipermodifytopicdetails(vipertoken,host,port,topic,companyname,partition=0,enabletls=1,isgroup=0,contactname='',contactemail='',location='',brokerhost='',brokerport=9092,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(companyname)==0 or len(topic)==0):
         return "Please enter host,port,topic,vipertoken,consumerid,companyname"
        
    value=("modifytopicdetails?vipertoken="+vipertoken + "&topic="+topic +"&brokerhost="+brokerhost+"&brokerport="+str(brokerport)
          + "&isgroup=" + str(isgroup) +"&partition="+str(partition) +"&enabletls="+str(enabletls)+"&companyname="+companyname+"&contactname="+contactname+"&contactemail="+contactemail+"&location="+location)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperactivatetopic(vipertoken,host,port,topic,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  ):
         return "Please enter host,port,vipertoken,topic"
        
    value=("activatetopic?vipertoken="+vipertoken + "&topic="+topic )

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperdeletetopics(vipertoken,host,port,topic,enabletls=1,brokerhost='',brokerport=9092,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  ):
         return "Please enter host,port,vipertoken,topic"
        
    value=("deletetopics?vipertoken="+vipertoken + "&topic="+topic +"&enabletls="+str(enabletls) +"&brokerhost="+brokerhost+"&brokerport="+str(brokerport))

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def viperdeactivatetopic(vipertoken,host,port,topic,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(topic)==0  ):
         return "Please enter host,port,vipertoken,topic"
        
    value=("deactivatetopic?vipertoken="+vipertoken + "&topic="+topic )

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipergroupactivate(vipertoken,host,port,groupname,groupid,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(groupname)==0   or len(groupid)==0 ):
         return "Please enter host,port,vipertoken,groupname,groupid"
        
    value=("activategroup?vipertoken="+vipertoken + "&groupname="+groupname +"&groupid="+groupid)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipergroupdeactivate(vipertoken,host,port,groupname,groupid,microserviceid=''):
    global connectionerror

    if (len(host)==0 or len(vipertoken)==0 or port==-999 or len(groupname)==0   or len(groupid)==0 ):
         return "Please enter host,port,vipertoken,groupname,groupid"
        
    value=("deactivategroup?vipertoken="+vipertoken + "&groupname="+groupname +"&groupid="+groupid)

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

def vipernlp(filename,fvalue,keys):
    if filename=="":
         return "Please enter host,port,vipertoken,groupname,groupid"
    if fvalue > 10000:
        return "Summary count too high. Must be  < 10000"
    if keys > 100:
        return "Keyword count too high. Must be  < 100"
        
    return readpdf.startpdfreading(filename,300,10)
    
def areyoubusy(host,port=-999,microserviceid=''):
    global connectionerror

    if (len(host)==0 or port==-999 ):
         return "Please enter host,port"
    value=("areyoubusy")

    val=loop.run_until_complete(tcp_echo_clientviper(value, loop,host,port,microserviceid))
    if connectionerror:
         return connectionerror

    return val

