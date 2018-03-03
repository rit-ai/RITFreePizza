from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
try:
    import argparse
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

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        response = service.users().messages().list(
            userId='me').execute()
        message_id_dict = response['messages']
        message_id_list = []
        for d in message_id_dict:
            message_id_list.append(d['id'])
        print(message_id_list)

        #message = service.users().messages().get(
        #    userId='me', id=message_id).execute()

        #for part in message['payload']['parts']:
        #    if part['filename'] == 'MFT_Status.xls':
        #        att_id = part['body']['attachmentId']
        #        att = service.users().messages().attachments().get(
        #            userId='me', messageId=message_id, id=att_id).execute()
        #        data = att['data']
        #        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        #        return file_data

    except errors.HttpError:
        print('An error occurred: {}'.format(errors.HttpError))

if __name__ == '__main__':
    main()