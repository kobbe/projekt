#!/usr/bin/env python
# -*- coding:utf-8 -*-

#####################################################################
######   Hans Koberg Google Calendar SMS script v1.03 (2015-03-24) ######
#####################################################################
#
# Only compatible with python 2.x
#
# Activation of google calendar api at code.google.com/apis/console
#
# Get the python library at
# https://developers.google.com/api-client-library/python/start/installation
# 
# The first time the script is run, you have to verify access to your calendar by loggin in to google, a web browser should pop up.
# There is a way to do it over SSH, it might say something the first time you try.
#
# Fill in all the global variables bellow
#
# To get autostart, edit the file /etc/rc.local with
# python path_to_your_script &
#
# example: python /home/a/Desktop/calendarparse/testCal.py &
# 
# If you want the printing to a file insted, use: 
# import sys
# sys.stdout = open(path, 'a',0)
# Where path is a legit path, i.e "/home/a/Desktop/calendarparse/output.txt"
#
#Debug info event https://www.google.com/calendar/render?gsessionid=OK&eventdeb=1

#Evens to have:
    #Server startup, one time event happening when script start up
    #Server down, push event every 5 min
    #changed IP, one time event when ip changed
    #no internet, ping google, same as server down..
    #Can not access koberg.nu, can be diff from server down but are prop same. if server down I do not want this.


from gdata import *
import gflags
import sys
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
import time
import datetime
import urllib2
import re
import traceback

# How often to update the smsSender, the event itself is created 10 minutes past this time to have some error margin
UPDATE_TIME_MIN = 1
ERROR_MARGIN = 3
EVENT_LENGTH = 5

# Just the id for the calendar
CALENDAR_ID =

# The id for the event (you have to create it yourself and setup the sms function)
EVENT_ID =

# Get it at code.google.com/apis/console
DEVELOPER_KEY =

#Some place to store something related to allowing acces to your calendar.
STORAGE = 

#Where errors should be printed
ERROR_STORAGE = 

#Where IP should be stored
IP_STORAGE = 

#OK strage stored
LOG_STORAGE = 

# Get it at code.google.com/apis/console
CLIENT_ID = 

# Get it at code.google.com/apis/console
CLIENT_SECRET = 

#startup event id
STARTUP_ID = 

#changed ip event id
CHANGED_IP_ID = 

#error when get ip event id
ERROR_IP_ID = 

#print errors to error file
sys.stderr = open (ERROR_STORAGE,'a',0)

#Regex for ip adress
reg = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
  
#Get servers IP
def getIP():
    ip = ''
    try:
        for line in urllib2.urlopen('http://ipecho.net/plain',timeout = 20):
            ip = line.decode('utf-8')
        if reg.match(ip) == None:
            raise Exception("failed to match regex")
    except:
        with open(ERROR_STORAGE, 'a') as f:
            now = datetime.datetime.now()
            f.write(str(now) + ": " + 'GetIp error\n')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            f.write(''.join('  ' + line for line in lines))  # Log it or whatever here
            f.write("\n")
            ip = ''
    return ip
    
#save ip to file. compare ip with last time.
#returns ip and if changed or not
def getIPAndDiff():
    ip = getIP()
    readString = ''
    with open(IP_STORAGE,'r') as f:
        readString = f.readline()
    if ip != '':
        if (readString == ip):
            return (ip,0)
        else:
            with open(IP_STORAGE,'w') as f:
                f.write(ip)
            return (ip,1)
    else:
        return (readString,2)
    
def smsSender(service, eventId , text = None):
    try:
        event = service.events().get(calendarId=CALENDAR_ID, eventId=eventId).execute()
        now = datetime.datetime.utcnow()
        if text != None:
            event['description'] = text
        event['start']['dateTime'] = (now+datetime.timedelta(minutes=UPDATE_TIME_MIN+ERROR_MARGIN)).strftime("%Y-%m-%dT%H:%M:%S+00:00") #+"T"+(now+datetime.timedelta(minutes=UPDATE_TIME_MIN+ERROR_MARGIN)).strftime("%H:%M:%S")+"+01:00"
        event['end']['dateTime'] = (now+datetime.timedelta(minutes=UPDATE_TIME_MIN+ERROR_MARGIN+EVENT_LENGTH)).strftime("%Y-%m-%dT%H:%M:%S+00:00") #+"T"+(now+datetime.timedelta(minutes=UPDATE_TIME_MIN+ERROR_MARGIN+EVENT_LENGTH)).strftime("%H:%M:%S")+"+01:00"
        updated_event = service.events().update(calendarId=CALENDAR_ID, eventId=eventId, body=event).execute()
        return True
    except:
        with open(ERROR_STORAGE, 'a') as f:
            now = datetime.datetime.now()
            f.write(str(now) + ": " + 'SmsSender error\n')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            f.write(''.join('  ' + line for line in lines))  # Log it or whatever here
            f.write("\n")
        return False
 
 
def refreshConnection(argv,FLOW,FLAGS):
    try:
        argv = FLAGS(argv)
    except gflags.FlagsError,e :
        with open(ERROR_STORAGE, 'a') as f:
            now = datetime.datetime.now()
            f.write(str(now) + ": " + 'FlagError happend\n\n')
        sys.exit(1)
    try:
        storage = Storage(STORAGE)
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            credentials = run(FLOW,storage)
        http = credentials.authorize(httplib2.Http())
        service = build('calendar','v3', http=http, developerKey = DEVELOPER_KEY)
    except:
        with open(ERROR_STORAGE, 'a') as f:
            now = datetime.datetime.now()
            f.write(str(now) + ": " + 'Connection error\n')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            f.write(''.join('  ' + line for line in lines))  # Log it or whatever here
            f.write("\n")
        return None
    return service
    
    
def log(status):
    with open(LOG_STORAGE, 'a') as f:
        now = datetime.datetime.now()
        f.write(str(now) + ': ' + status +'\n')
    
    #TODO: see if we got an error somewhere...
    #return status of smsSender
    
def main(argv):
    status = True
    refreshConnectionTimer = 0
    FLAGS = gflags.FLAGS
    FLOW = OAuth2WebServerFlow(client_id = CLIENT_ID,
                               client_secret = CLIENT_SECRET,
                               scope = 'https://www.googleapis.com/auth/calendar',
                               user_agent = 'Calendar sms')
    service = refreshConnection(argv,FLOW,FLAGS)
    
    if (service != None):
        if not smsSender(service,STARTUP_ID): #Startup sms, 3 min after startup.
            log('error')
            status = False
    else:
        log('error')
        status = False
        
    while True:
        if refreshConnectionTimer >= 360: #Refreshes the connection to google calendar every 6h
            service = refreshConnection(argv,FLOW,FLAGS)
            refreshConnectionTimer = 0
        else:
            refreshConnectionTimer += 1*UPDATE_TIME_MIN
        if (service != None):
            (ip,changed) = getIPAndDiff()
            if changed == 0:
                if not smsSender(service,EVENT_ID):
                    log('error')
                    status = False
            elif changed == 1: #update the ip in EVENT_ID and send a special sms
                if not smsSender(service, EVENT_ID, 'IP is now: ' + ip):
                    log('error')
                    status = False
                if not smsSender(service, CHANGED_IP_ID, 'IP is now: ' + ip):
                    log('error')
                    status = False
            else: #changed = 2, what to do here?
                if not smsSender(service,EVENT_ID):
                    log('error')
                    status = False
                #smsSender(service,ERROR_IP_ID) #ignore first, not second. 
                #update e special event here but dont do it for ever if several fails in row.
            if status:
                log('ok')
        else:
            log('error')
        status = True
        time.sleep(UPDATE_TIME_MIN*60)

if __name__ == '__main__':
    main(sys.argv)
