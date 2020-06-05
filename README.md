# PostgreSQLBackup
Backup your PostgreSQL Database and upload it to your drive!

## Requirements
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
**Source:** https://developers.google.com/drive/api/v3/quickstart/python
Tested with **Python 3.8**, but should work also for **3.6**.

## How to use
### Configure the File
```python
# path to your PostgreSQL directory. If the Python file is in directory leave it ''
PG_BACKUP_PATH: str = '' 

# Your PostgreSQL password
PG_PASSWORD: str = ''

# If the files should be ziped
ZIP_FILES: bool = True
```
#### Google Drive
First you need access to the drive API. 
Get an API key at [**Google Dev Page**](https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the)
- Click on `Enable the Drive API`
- Select `Desktop app` 
- Click on `CREATE`
- Download the client configuration and move them to the python file

#### Configure
```python
# Set to True on the first use. You need to have access to a webbrowser
login: bool = False

# If the files should be uploaded to Google Drive
UPLOAD_DRIVE: bool = True

# If the files should be deleted after uploading
REMOVE_FILES: bool = True
```

**When you use Drive, `token.pickle` and `credentials.json` have to be in the same folder!**
