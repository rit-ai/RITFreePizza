import httplib2
import os
import argparse
import base64
import pandas as pd
import re
from bs4 import BeautifulSoup
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors

try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'pizza_client.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.
    Creates a Gmail API service object and outputs a list emails.
    """
    pattern= re.compile(' +')
    batch = BatchHttpRequest()
    for msg_id in message_ids:
        batch.add(service.users().messages().get(userId='me', id=msg_id['id']), callback=mycallbackfunc)
    batch.execute()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    email_csv = pd.DataFrame(columns=['body'])
    try:
        response = service.users().messages().list(
            userId='me').execute()
        message_id_dict = response['messages']
        message_id_list = []
        for d in message_id_dict:
            message_id_list.append(d['id'])
        for message_id in message_id_list:
            message = service.users().messages().get(userId='me', id=message_id).execute()
            if 'parts' in message['payload']:
                if message['payload']['parts'][0]['mimeType'] == 'multipart/alternative':
                    message_raw = message['payload']['parts'][0]['parts'][0]['body']['data']
                else:
                    message_raw = message['payload']['parts'][0]['body']['data']
            else:
                message_raw = message['payload']['body']['data']
            msg_str = base64.urlsafe_b64decode(message_raw.encode('UTF-8'))
            soup = BeautifulSoup(msg_str.decode("utf-8"), "lxml")
            [s.extract() for s in soup('style')]
            text = soup.get_text()
            text = re.sub(pattern, ' ', text).replace('\n', ' ').replace('\r', '')
            email_csv = email_csv.append({'body': text}, ignore_index=True)
        email_csv.to_csv('list_of_emails.csv')

    except errors.HttpError:
        print('An error occurred: {}'.format(errors.HttpError))

if __name__ == '__main__':
    main()
