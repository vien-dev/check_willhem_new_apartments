import urllib.request
from urllib.parse import unquote
import re
from datetime import datetime
import os
import shutil
import smtplib

message_template="""\
From: {0}
To: {1}
Subject: {2}

Hi!

On the scan at {4} {3}, we have found {6} new apartments:
{5}

Regards,
Vien
"""
apartment_template = """
{5}. Apartment: {0}
   Cost: {1} kr/month
   Total Room: {2}
   Floor: {3}
   Elevator Available: {4}
"""

def read_apartment_detail(apartment_file):
    rental_cost_pattern = re.compile('Hyra: [0-9]+')
    total_room_pattern = re.compile('Antal rum: [0-9]+')
    floor_pattern = re.compile('Våning: [0-9]+')
    elevator_pattern = re.compile('Hiss:  (Ja|Nej)')
    with open(apartment_file, 'r') as f:
        for line in f:
            if rental_cost_pattern.search(line):
                match = rental_cost_pattern.search(line)
                rental_cost = match.group()
                rental_cost = rental_cost.split(': ')[1]
            elif total_room_pattern.search(line):
                match = total_room_pattern.search(line)
                total_room = match.group()
                total_room = total_room.split(': ')[1]
            elif floor_pattern.search(line):
                match = floor_pattern.search(line)
                floor = match.group()
                floor = floor.split(': ')[1]
            elif elevator_pattern.search(line):
                match = elevator_pattern.search(line)
                elevator = match.group()
                elevator = elevator.split(':  ')[1]
    if 'Ja' == elevator:
        elevator = 'Yes'
    elif 'Nej' == elevator:
        elevator = 'No'
    return (rental_cost, total_room, floor, elevator)
    
def send_mail():
    date_str = datetime.today().strftime('%Y-%m-%d')
    sender_email=os.environ['SENDER_MAIL']
    sender_password=os.environ['SENDER_MAIL_PWD']
    smtp_server='smtp.gmail.com'
    smtp_port=587
    receiver_email=os.environ['RECEIVER_MAIL']
    message = message_template.format(sender_email, receiver_email, 'New apartment(s) found', date_str, datetime.now().strftime("%H:%M:%S"), apartment_list, total_apartment)

    #copy from here: https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/
    # creates SMTP session 
    s = smtplib.SMTP(smtp_server, smtp_port) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login(sender_email, sender_password) 
      
    # message to be sent 
    #message = "Message_you_need_to_send"
      
    # sending the mail
    s.sendmail(sender_email, receiver_email, message) 
      
    # terminating the session 
    s.quit() 


if os.path.exists('previous'):
    shutil.rmtree('previous')
if os.path.exists('current'):
    shutil.copytree('current','previous')
    shutil.rmtree('current')
else:
    os.mkdir('previous')

os.mkdir('current')

willhem_url='https://www.willhem.se'
willhem_main_page='/sok-bostad/Goteborg/'
apartment_pattern1 = re.compile('Mer info och intresseanmälan')
apartment_pattern2 = re.compile('/sok-bostad/Goteborg/[a-z,A-Z,0-9,-]+/')

apartment_list = ""
total_apartment = 0
urllib.request.urlretrieve("{0}{1}".format(willhem_url, willhem_main_page), "willhem_sok_bostad_main_page.temp.html")
with open('willhem_sok_bostad_main_page.temp.html', 'r') as f:
    for line in f:
        if apartment_pattern1.search(line):
            m = apartment_pattern2.search(line)
            apartment_sublink = m.group()
            if not os.path.isfile("previous/{0}.temp.html".format(apartment_sublink.split('/')[3])):
                apartment_full_url = "{0}{1}".format(willhem_url, apartment_sublink)
                urllib.request.urlretrieve(apartment_full_url, "current/{0}.temp.html".format(apartment_sublink.split('/')[3]))
                rental_cost, total_room, floor, elevator = read_apartment_detail("current/{0}.temp.html".format(apartment_sublink.split('/')[3]))
                # We consider apartments with more than 1 room only
                if int(total_room) <= 1:
                    continue
                total_apartment += 1
                apartment_text = apartment_template.format(apartment_full_url, rental_cost, total_room, floor, elevator, total_apartment)
                apartment_list = apartment_list + apartment_text
            else:
                shutil.copy("previous/{0}.temp.html".format(apartment_sublink.split('/')[3]),"current/{0}.temp.html".format(apartment_sublink.split('/')[3]))
            

if "" != apartment_list:
    print("Found {} new apartment(s). Sending mail".format(total_apartment))
    send_mail()
else:
    print("There's no new apartment on this scan")