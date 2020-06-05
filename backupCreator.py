import datetime
import os
import pickle
import subprocess as sp
import time
from zipfile import ZipFile
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# **With a / at the end**
PG_BACKUP_PATH: str = ''

PG_PASSWORD: str = '1'
ZIP_FILES: bool = True
REMOVE_FILES: bool = True

# ** DRIVE **
# On the first time you need to login on a desktop
# After login, set login to False
login: bool = False
UPLOAD_DRIVE: bool = True


def createConnection():
    creds = None

    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', ['https://www.googleapis.com/auth/drive.file'])
            creds = flow.run_local_server(port=0)

        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def zipFile(fileName):
    zipFileName = fileName + '.zip'
    with ZipFile(zipFileName, 'w') as zipf:
        zipf.write(PG_BACKUP_PATH + fileName + '.backup')

    return zipFileName


def uploadFile(fileName):
    if not UPLOAD_DRIVE:
        return

    if os.path.isfile(PG_BACKUP_PATH + fileName + '.backup'):
        if ZIP_FILES:
            file = zipFile(fileName)
        else:
            file = fileName + '.backup'

        print('Uploading...')
        drive = createConnection()
        media = MediaFileUpload(PG_BACKUP_PATH + file, mimetype=None)
        drive.files().create(body={'name': file},
                             media_body=media,
                             fields='id').execute()
        print('Upload completed.')

        os.remove(PG_BACKUP_PATH + fileName + '.backup')
        if ZIP_FILES:
            os.remove(PG_BACKUP_PATH + fileName + '.zip')
    else:
        print('Cannot upload file.')


def createBackup():
    print('Creating Backup...')
    proc = sp.Popen(['su', 'postgres'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    currentDate = datetime.datetime.now().strftime("B_%d-%m-%Y-%H-%M")
    cmd = 'PGPASSWORD=' + PG_PASSWORD + ' pg_dump discord > ' + currentDate + '.backup\n'
    proc.stdin.write(cmd.encode())
    proc.communicate()

    return currentDate


if login:
    createConnection()
    exit(1)
else:
    while True:
        name = createBackup()
        uploadFile(name)
        time.sleep(86400)

