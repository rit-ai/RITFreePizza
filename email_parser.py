import mailbox
from bs4 import BeautifulSoup
import csv
import pandas as pd

import uuid

def prepros(text):
    soup = BeautifulSoup(text, "html5lib")
    clean = soup.get_text()
    return clean
writer = csv.writer(open("clean_mail_B.csv", "wb"))
#second = csv.writer(open("nonemtf.csv", "wb"))
count = 0

output = pd.DataFrame(columns=["Email_id", "data_source", "Building_num", "Room_num", "Pizza_Status", "Event_Date", "Sent_Date", "Text"])

for message in mailbox.mbox('pizza!.mbox'):
    if message.is_multipart():
        content = message.get_payload(0).get_payload(decode=True)
    else:
        content = message.get_payload(decode=True)
    #if content is None:

    if(content is None):
        continue

    output = output.append(pd.DataFrame([[uuid.uuid4(), "email", None, None, None, None, message['date'], prepros(content)]], columns=["Tweet_id", "data_source", "Building_num", "Room_num", "Pizza_Status", "Event_Date", "Sent_Date","Text"]))



output.to_csv("email_output.csv")
    #writer.writerow([message['to'], message['from'], message['date'], message['subject'], content)])