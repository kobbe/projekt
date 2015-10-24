#!/usr/bin/env python -u
# -*- coding:utf-8 -*-


#####################################################################
######   Hans Koberg Google Calendar script v1.02 (2013-03-16) ######
#####################################################################
######                       How to use:                       ######
######                                                         ######
######    *create 'database.pkl' with pickle as []             ######
######    *create 'idDatabase.pkl' with pickle as []           ######
#####################################################################                
######                       KNOWN BUGS:                       ######
######    *Needs file 'database.pkl' to be created manually    ######
######  *Needs file 'idDatabase.pkl' to be created manually    ######
######  *Recursive events stored forever in database           ######
######  *Excluded calendar names can't handle å,ä,ö.           ######
#####################################################################


## Should perform a backup every week or so! something if everything gets messed up


#No idea if these are neccecary, should test
import gdata
from gdata import *
from apiclient.discovery import build
import gflags
import sys
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import time
import datetime
import json, ast
import pickle
import copy

#Make standardout to a file insted
sys.stdout = open ("PRIVATE STRING",'a',0)

#Make standarderror to a file insted
sys.stderr = open ("PRIVATE STRING",'a',0)


#Times 1 minutes to skip
UPDATE_TIME_MIN = 1
#Count connections done
CC = 0
CC1 = 0
CC2 = 0
CC3 = 0
CC4 = 0
CC5 = 0

def getList():
    pkl_file = open('PRIVATE STRING', 'rb')
    list = pickle.load(pkl_file)
    pkl_file.close()
    return list
    
    
def to_datetime(e):
    if 'recurrence' in e: #Cheating here, should do it for real. reccurence 'dateTime' is wrong.
        #list = e['recurrence']
        #string = list.pop()
        #position = string.find("UNTIL=")
        #if position == -1:
        #    return datetime.datetime.now()
        #else:
        #    position = position+7
        #    position2 = string.find(";BY")
        #    time = string[position:position2-1]
        #    print time
        #    return datetime.datetime.strptime(time,'%Y%m%dT%H%M%S')
        return datetime.datetime.now()
    if 'dateTime' in e['end']:
        #print e['end']['dateTime']
        
        if e['end']['dateTime'].find('Z') != -1 :
            return datetime.datetime.strptime(e['end']['dateTime'][:-1], '%Y-%m-%dT%H:%M:%S')
        return datetime.datetime.strptime(e['end']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
    else:
        return datetime.datetime.strptime(e['end']['date'], '%Y-%m-%d')
    
    
def removeOld(list):
    now = datetime.datetime.now()-datetime.timedelta(days=1) #Moves the date where the events are removed a full day.
    return [e for e in list if  to_datetime(e) >= now]
     
    
def readExcludedCals():    #Cant handle å,ä,ö
    try:
        return [unicode(line.strip()) for line in open('PRIVATE STRING') if line.strip() != ""]
    except:
        return [u"PRIVATE STRING"]

    #Läs in kalendrar som inte finns exkluderade i filen.
    
def smsSender(service):
    #try:
    global CC
    global CC1
    primary = 'RIVATE STRING'
    id = 'PRIVATE STRING'
    event = service.events().get(calendarId=primary, eventId=id).execute()
    CC+=1
    CC1+=1
    #put in ip in sms
    now = datetime.datetime.now()
    event['start']['dateTime'] = (now+datetime.timedelta(minutes=40)).strftime("%Y-%m-%d")+"T"+(now+datetime.timedelta(minutes=40)).strftime("%H:%M:%S")+"+01:00"
    event['end']['dateTime'] = (now+datetime.timedelta(minutes=45)).strftime("%Y-%m-%d")+"T"+(now+datetime.timedelta(minutes=45)).strftime("%H:%M:%S")+"+01:00"
    updated_event = service.events().update(calendarId=primary, eventId=event['id'], body=event).execute()
    CC+=1
    CC1+=1
    #except:
    #    print "Error occured, sms error."
    #    print sys.exc_info()[0]
    #    print "middle"
    #    print sys.exc_traceback.tb_lineno
    #    print "sms error done"
    return
    
def getAColor(id): ##Should reset or clear the list sometime
    pkl_file = open('PRIVATE STRING', 'rb')
    list = pickle.load(pkl_file)
    pkl_file.close()
    save = True
    for (x,y,compId) in list:
        if compId==id:
            color=y
            save = False
    if save:
        if len(list) > 0:
            (number,string,id2) = list.pop()
            list.append((number,string,id2))
        else:
            number = 0
        color = int(string)+1 % 12
        #color = (number+1) % 12
        #color += (number+1) 
        if color == 0 :
            color = 1
        color = str(color)
        list.append((number+1,color,id))
        output = open('PRIVATE STRING', 'wb')
        pickle.dump(list, output)
        output.close()
    return color

def main(argv):
    global CC
    global CC1
    global CC2
    global CC3
    global CC4
    global CC5
    newCalsCounter = 1440
    newCalsCounter_compare = 1440/UPDATE_TIME_MIN
    smsCounter = 30
    smsCounter_compare = 30/UPDATE_TIME_MIN
    refresh = 360
    refresh_compare = 360/UPDATE_TIME_MIN
    remove = 30
    remove_compare = 30/UPDATE_TIME_MIN
    
    idList = []
    FLAGS = gflags.FLAGS
    
    FLOW = OAuth2WebServerFlow(
    client_id='PRIVATE STRING',
    client_secret='PRIVATE STRING',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Calendar test ') #Random name here
    list = getList()
    #-----Initalization-----#
    while True:
        #try:
        if refresh >= refresh_compare:
            try:
                argv = FLAGS(argv)
            except gflags.FlagsError,e :
                print ' felpåflaggan'
                sys.exit(1)
            storage = Storage('PRIVATE STRING')
            credentials = storage.get()
            if credentials is None or credentials.invalid == True:
                credentials = run(FLOW,storage)
            http = httplib2.Http()
            http = credentials.authorize(http)
            service = build('calendar','v3', http=http,developerKey='PRIVATE STRONG')
            refresh = 0
            
    
        refresh+=1
        smsCounter +=1
        newCalsCounter +=1
        remove +=1
        
        if smsCounter >= smsCounter_compare:
            smsSender(service)
            smsCounter = 0
        
        excluded = readExcludedCals()
        
        if newCalsCounter >= newCalsCounter_compare:
            newCalsCounter = 0
            page_token = None
            idList = []
            while True:
                calendar_list = service.calendarList().list(pageToken=page_token).execute()
                CC+=1
                CC2+=1
                
                if 'items' in calendar_list:
                    for calendar_list_entry in calendar_list['items']:
                        if not calendar_list_entry['summary'] in excluded :
                                idList.append(calendar_list_entry['id'])
                page_token = calendar_list.get('nextPageToken')
                if not page_token:
                    break

        if remove >= remove_compare:
            #print "here"
            #print list
            #print "done"
            list = removeOld(list)
            remove = 0
        #kör för varje id i idList
        #try:
        for id in idList:
            colourId = getAColor(id)            
            now = datetime.datetime.now()
            
            events = service.events().list(
            calendarId=id
            ,timeMin=now.strftime("%Y-%m-%d")+"T"+now.strftime("%H:%M:%S")+"+01:00"
            ,timeMax=(now+datetime.timedelta(days=100)).strftime("%Y-%m-%d")+"T"+(now+datetime.timedelta(days=100)).strftime("%H:%M:%S")+"+01:00"
            ).execute()
            CC+=1
            CC3+=1
            if 'items' in events:
                while True:
                    for event in events['items']:
                        del event['etag']
                        if event['status'] != 'cancelled':
                            if not event in list:
                                
                                eventToStore = copy.deepcopy(event)
                                
                                event[u'colorId'] = colourId
                                del event['id']
                                
                                del event['htmlLink']
                                del event['iCalUID']
                                del event['creator']
                                del event['reminders']
                                del event['organizer']
                                if 'description' in event:
                                    event['description'] = event['description']+" Made: "+str(now)
                                else:
                                    event['description'] = " Made: "+str(now)
                                print event
                                service.events().insert(calendarId='PRIVATE STRING', body=event).execute()
                                CC+=1
                                CC4+=1
                                print "new event started to be added!"
                                list.append(eventToStore)
                                output = open('PRIVATE STRING', 'wb')
                                pickle.dump(list, output)
                                output.close()
                                print "new event saved!"
                    page_token = events.get('nextPageToken')
                    if page_token:
                        CC+=1
                        CC5+=1
                        events = service.events().list(calendarId=id, pageToken=page_token).execute()
                    else:
                        break
        #except:
        #    print "Error occured, nr 0."
        #    print sys.exc_info()[0]
        #    print "middle"
        #    print sys.exc_traceback.tb_lineno
        #    print "error done"
        now = datetime.datetime.now()
        print str(now)+" ,number of events: "+str(len(list))+" , "+str(CC)+" recuests done. CC1: " + str(CC1) + " CC2: " + str(CC2) + " CC3: " + str(CC3) + " CC4: " + str(CC4) + " CC5: " + str(CC5)
        CC=0
        CC1 = 0
        CC2 = 0
        CC3 = 0
        CC4 = 0
        CC5 = 0
        #except: 
         #   now = datetime.datetime.now()
          #  print str(now)+" probebly no network"
           # print "Error message: " + str(sys.exc_info()[0])
            #print "Error line " + str(sys.exc_traceback.tb_lineno)
            #print "error done"
        time.sleep(UPDATE_TIME_MIN*60)

if __name__ == '__main__':
    main(sys.argv)
