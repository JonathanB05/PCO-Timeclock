import pypco
import dateutil.parser
from dateutil import tz
import datetime
from datetime import timezone
import threading
import schedule
import time
from os import system
import os
import logging
import auth
import keyboard

def utc_to_local(utc_dt): #define the conversion from UTC to local time
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
def printit(): #define function to run every second
    islive = pco.get(f'/services/v2/people/{user_id}/recent_plans/{plan_id}/live/current_item_time') #get current item time file
    item_id=(islive['data']['relationships']['item']['data']['id']) #get the id of the current item
    for id in pco.iterate(f'/services/v2/people/{user_id}/recent_plans/{plan_id}/items'): #run through the list of items in a plan
        if (id['data']['id'])== item_id: #check if the id of an item matches the id of the current live item
            livestart=dateutil.parser.isoparse((islive['data']['attributes']['live_start_at']))#get the start time of the current item
            starttime=utc_to_local(livestart)#convert livestart to the local time zone
            length=(id['data']['attributes']['length'])*(0.01666666666666666666666666666667)#convert the time to minutes
            newlength=datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=length, hours=0, weeks=0)#convert the time to the same format as the start time
            endtime=(starttime+newlength)#calculate a predicted end time
            item_title=(id['data']['attributes']['title'])#get the item title
            system('cls' if os.name == 'nt' else 'clear')#clear the command window
            print(f'{item_title} - {churchname}')#print the item title and our church name
            nowtime=datetime.datetime.now().replace(microsecond=0)#get the current time
            nowtimeformat=nowtime.strftime("%H:%M:%S")#format the current time
            runtime=(nowtime-starttime.replace(tzinfo=None))#calculate the run time
            #print("Run Time:",runtime)#print the run time
            #print('End Time:',endtime.strftime("%H:%M:%S"))  
            if runtime > newlength: #check if the item is overtime
                remtime=(runtime-newlength)#if overtime, set remtime to a negative time value
                print('-' + str(remtime)) #print remtime
            else: 
                remtime=(newlength-runtime) #if time remaining in the current item, set remtime to the remaining time
                print(f'Remaining Time: {str(remtime)}')#print remtime
pco = pypco.PCO(auth.id, auth.secret) #authenticate using auth.py
org=pco.get('/services/v2')#get info on the organization
churchname=org['data']['attributes']['name']#define churchname
user=pco.get('/people/v2/me')
user_id=user['data']['id']
while True:
    if keyboard.is_pressed('enter'):
        system('cls' if os.name == 'nt' else 'clear')
        print('Have a good day, ' + user['data']['attributes']['first_name'])
        exit()
    for type in pco.iterate(f'/services/v2/people/{user_id}/recent_plans'): #run through the list of plans and get the id and name
        plan_id=(type['data']['id'])
        plan_name=(type['data']['attributes']['title'])
        try: #try to find plans that are live
            schedule.every(1).seconds.do(printit)
            while 1:
                schedule.run_pending()
            break              
        except Exception as e: #if error, respond as follows
            logdatetime = time.strftime("%m-%d-%Y")
            logging.basicConfig(filename=os.getcwd() + '\\logs\\' +logdatetime + '.log',datefmt='%m/%d/%Y %I:%M:%S %p',level = logging.ERROR)#start logging 
            if e.status_code==429: #if rate limited, do nothing
                system('cls' if os.name == 'nt' else 'clear')#clear the command window
                logging.exception(f'{nowtimeformat}\n')
                logging.exception(f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}')
                print('Rate Limited')
                pass
            elif e.status_code==404: #if not found, post error to log
                system('cls' if os.name == 'nt' else 'clear')#clear the command window
                nowtime=datetime.datetime.now().replace(microsecond=0)#
                nowtimeformat=nowtime.strftime("%H:%M:%S")
                logging.exception(nowtimeformat)
                logging.exception(f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}')
                print('No Service Found')
                print('The time is',nowtimeformat,'\n')
                pass
            else: #if any other error, print info and error, print to log
                system('cls' if os.name == 'nt' else 'clear')
                print('No Service Found')
                nowtime=datetime.datetime.now().replace(microsecond=0)
                nowtimeformat=nowtime.strftime("%H:%M:%S")
                print('The time is',nowtimeformat,'\n')
                print(f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}')
                logging.exception(f'{nowtimeformat}\n')
                logging.exception(f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}')
                pass
    