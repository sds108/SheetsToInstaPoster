import os
from Google import Create_Service
import json
from os import path
import time

CLIENT_SECRET_FILE = 'client_secret_1.json'
SHEETS_API_NAME = 'sheets'
SHEETS_API_VERSION = 'v4'
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

DRIVE_API_NAME = 'drive'
DRIVE_API_VERSION = 'v3'
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']

sheets_service = Create_Service(CLIENT_SECRET_FILE, SHEETS_API_NAME, SHEETS_API_VERSION, SHEETS_SCOPES)
time.sleep(10)
#drive_service = Create_Service(CLIENT_SECRET_FILE, DRIVE_API_NAME, DRIVE_API_VERSION, DRIVE_SCOPES)