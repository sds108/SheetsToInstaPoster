import imp
import os, platform
from pickle import FALSE
import sys
from os import path
from tkinter import TRUE
from urllib import response
from pyparsing import col
from Google import Create_Service
import json
import PIL
from PIL import Image, ImageDraw, ImageFont
import textwrap
from pilmoji_fixed import Pilmoji
from datetime import datetime
from googleapiclient.http import MediaFileUpload
import schedule
import time
from defines_2 import getCreds, makeApiCall
from html2image import Html2Image
from jinja2 import Environment
import requests
from random import randint


CLIENT_SECRET_FILE = 'client_secret.json'
SHEETS_API_NAME = 'sheets'
SHEETS_API_VERSION = 'v4'
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

DRIVE_API_NAME = 'drive'
DRIVE_API_VERSION = 'v3'
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']

# Variables
data_dict = {}
connected = 'FALSE'

sheets_service = Create_Service(CLIENT_SECRET_FILE, SHEETS_API_NAME, SHEETS_API_VERSION, SHEETS_SCOPES)
drive_service = Create_Service(CLIENT_SECRET_FILE, DRIVE_API_NAME, DRIVE_API_VERSION, DRIVE_SCOPES)

# dict_keys(['spreadsheetId', 'properties', 'sheets', 'spreadsheetUrl'])
spreadsheet_id = ''
range_ = 'Form responses 1'



def main():
    global connected
    time.sleep(1)
    host = "8.8.8.8"
    response = os.system("ping " + ("-n 1 " if  platform.system().lower()=="windows" else "-c 1 ") + host)
    # and then check the response...
    if response != 0:
        connected = 'FALSE'
        loopTime = 1.0
    elif response == 0:
        connected = 'TRUE'
        loopTime = 2.0
    else:
        print("error")
    
    print("Network Status: " + connected)
    print("loopTime: " + str(loopTime))
    time.sleep(1)



def load_sheet():
    global data_dict

    try:
        request = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, majorDimension='COLUMNS')
        response = request.execute()
    except:
        return 'error'

    data = response['values']


    # Remove Column Titles
    try:
        data[1].remove('Submission')
    except:
        print('error trying to remove element')

    try:
        data[2].remove('Approval')
    except:
        print('error trying to remove element')

    try:
        data[3].remove('Number')
    except:
        print('error trying to remove element')

    try:
        data[4].remove('Status')
    except:
        print('error trying to remove element')
    
    try:
        data[5].remove('DriveID')
    except:
        print('error trying to remove element')

    try:
        data[6].remove('IGid')
    except:
        print('error trying to remove element')

    try:
        data[7].remove('PostTime')
    except:
        print('error trying to remove element')

    print(data)
    # Put Data into Dict

    for i in range(0, len(data[0])):

        data_dict[i] = {'Submission': '', 'Approval': '', 'Number': '', 'Status': '', 'DriveID': '', 'IGid': '', 'PostTime': ''}

        try:
            data_dict[i]['Approval'] = data[2][i]
        except:
            data_dict[i]['Approval'] = 'FALSE'
            print('error trying to append Approval')
    
        try:
            data_dict[i]['Number'] = data[3][i]
        except:
            data_dict[i]['Number'] = '0'
            print('error trying to append Number')
    
        try:
            data_dict[i]['Status'] = data[4][i]
        except:
            data_dict[i]['Status'] = 'N'
            print('error trying to append Status')

        try:
            data_dict[i]['DriveID'] = data[5][i]
        except:
            data_dict[i]['DriveID'] = ''
            print('error trying to append DriveID')

        try:
            data_dict[i]['IGid'] = data[6][i]
        except:
            data_dict[i]['IGid'] = ''
            print('error trying to append IGid')
        
        try:
            data_dict[i]['PostTime'] = data[7][i]
        except:
            data_dict[i]['PostTime'] = ''
            print('error trying to append PostTime')
    
        try:
            data_dict[i]['Submission'] = data[1][i]
        except:
            print('error trying to adding submission')

    print(data_dict)



def Find_Biggest_Number():
    global data_dict

    # Find Biggest Number
    numbers = [0]

    for i in data_dict.keys():
        print(data_dict[i]['Number'])
        if data_dict[i]['Number'] != '':
            numbers.append(int(data_dict[i]['Number']))
    print(numbers)

    return max(numbers)



def Create_Image(submission_number, submission_text):
    print("Creating Image")
    # Create Image
    with Image.open("Template.png") as im:

        xsize, ysize = im.size

        lines = textwrap.wrap(submission_text, width=40)
        wrapped_text = ''

        print("len:"+str(len(lines)))

        # Add spaces to fill space (comment out if not using Pilmoji)
        for i in range(0, len(lines)):
            if len(lines[i]) < 38:
                spaces_to_add = round((40-len(lines[i])))
                for n in range(0, spaces_to_add):
                    lines[i] = " " + lines[i]

        print(lines)

        # Choose y-pos based on amount of lines ######## comment out if not using Pilmoji
        y_pos = abs(540-(len(lines)*36))

        # Conjoin split text
        if len(lines) > 1:
            for i in range(0, len(lines)):
                wrapped_text = wrapped_text + "\n" + str(lines[i])
        else:
            wrapped_text = lines[0]

        print(wrapped_text)

        fnt0 = ImageFont.truetype('OpenSans-ExtraBold.ttf', 72)
        fnt1 = ImageFont.truetype('OpenSans-Light.ttf', 54)
        d = ImageDraw.Draw(im)
        #d1 = ImageDraw.Draw(im) ###################### uncomment if not using Pilmoji

        # Draw Title
        d.text((xsize/2, 132/2), "Engineering Confession #" + str(submission_number), font=fnt0, anchor="mm", align="center", fill=(255, 255, 255))

        # Draw Submission
        #d1.text((int(xsize/2), int(ysize/2)), wrapped_text, font=fnt1, anchor="mm", align="center", fill=(0, 0, 0, 0), embedded_color='True') ###### uncomment if not using Pilmoji

        #################### comment out if not using Pilmoji
        Pilmoji(im).text((15, y_pos), wrapped_text, font=fnt1, fill=(0, 0, 0), emoji_size_factor=0.75, emoji_position_offset=(0, 20))
 
        im.save(str(submission_number) + ".png")



def Queue_for_creation():
    global data_dict
    print("Queueing for creation")
    # Find to-be-generated Submissions
    submissions_to_create = []

    test = load_sheet()
    if (test) == 'error':
        return 'error'

    for i in data_dict.keys():
        if (data_dict[i]['Submission'] != '') and ((data_dict[i]['Approval'] == 'TRUE') and (data_dict[i]['Approval'] != 'FALSE') and (data_dict[i]['Approval'] != '')) and ((data_dict[i]['Status'] != 'Waiting') and ((data_dict[i]['Status'] == 'N') or (data_dict[i]['Status'] == '')) and (data_dict[i]['Status'] != 'Processing') and (data_dict[i]['Status'] != 'Queued') and (data_dict[i]['Status'] != 'Posted')) and ((data_dict[i]['Number'] == '0') or (data_dict[i]['Number'] == '')) and (data_dict[i]['DriveID'] == '') and (data_dict[i]['IGid'] == ''):
            submissions_to_create.append(i)
        else:
            print("Could Not Verify")
            print(data_dict[i])

    #print(submissions_to_create)

    # Create Image for Post
    if len(submissions_to_create) >= 1:
        last_number = Find_Biggest_Number()
        for i in range(0, len(submissions_to_create)):
            print("Calling screenshot")
            data_dict[submissions_to_create[i]]['Number'] = last_number+1+i
            screenshot(last_number+1+i, data_dict[submissions_to_create[i]]['Submission'])
            data_dict[submissions_to_create[i]]['Status'] = "Processing"

            test = Update_sheet(submissions_to_create[i], 'Approval', data_dict[submissions_to_create[i]]['Approval'])
            if (test) == 'error':
                return 'error'
            test = Update_sheet(submissions_to_create[i], 'Number', data_dict[submissions_to_create[i]]['Number'])
            if (test) == 'error':
                return 'error'
            test = Update_sheet(submissions_to_create[i], 'Status', data_dict[submissions_to_create[i]]['Status'])
            if (test) == 'error':
                return 'error'

            test = Upload_to_Drive(submissions_to_create[i])
            if (test) == 'error':
                return 'error'
    
        print(data_dict)

    else:
        print("No Submissions to Create")



def Upload_to_Drive(index):
    global data_dict
    print("Uploading file to Drive")
    folder_id = ''
    file_metadata = {'name': str(data_dict[index]['Number'])+".png", 'parents': [folder_id]}

    print(str(os.getcwd()) + "\\" + str(data_dict[index]['Number'])+".png")
    media = MediaFileUpload(str(os.getcwd()) + "\\" + str(data_dict[index]['Number'])+".png", mimetype='image/png')
    
    # Check file doesn't already exist and is on Drive
    result = Read_Drive(str(data_dict[index]['Number'])+".png", folder_id)
    print(result)

    if result['exists'] == 'TRUE':
        # Assign Correct DriveID
        data_dict[index]['DriveID'] = result['id']

        # Update Sheet
        data_dict[index]['Status'] = 'Waiting'
        Update_sheet(index, 'DriveID', data_dict[index]['DriveID'])
        Update_sheet(index, 'Status', data_dict[index]['Status'])
        print("done updating DriveID")

    elif result['exists'] == 'FALSE':
        # Try Upload
        request = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(request)
        # Update Sheet
        data_dict[index]['DriveID'] = request['id']
        data_dict[index]['Status'] = 'Waiting'
        Update_sheet(index, 'DriveID', data_dict[index]['DriveID'])
        Update_sheet(index, 'Status', data_dict[index]['Status'])
    
    elif result['exists'] == 'error':
        return 'error'

    else:
        return 'error'
    
    time.sleep(0.5)



def Read_Drive(file_name, folder_id):
    print("Checking files in Drive")

    return_values = {'exists': '', 'id': ''}

    # Check it doesn't exist already
    query = f"parents = '{folder_id}'"
    try:
        drive_search = drive_service.files().list(q=query).execute()
    except:
        return_values['exists'] = 'error'
        return return_values
    
    files = drive_search.get('files')
    nextPageToken = drive_search.get('nextPageToken')

    while nextPageToken:
        try:
            drive_search = drive_service.files().list(q=query, pageToken=nextPageToken).execute()
            files.extend(drive_search.get('files'))
            nextPageToken = drive_search.get('nextPageToken')
        except:
            return_values['exists'] = 'error'
            return return_values
    
    print(files)

    if len(files) > 0:
        for i in range(0, len(files)):
            if file_name == files[i]['name']:
                print("file already exists in Drive")
                
                return_values['exists'] = 'TRUE'
                return_values['id'] = files[i]['id']

                return return_values
        # if it didn't find the file, do this
        return_values['exists'] = 'FALSE'
        return_values['id'] = ''

        return return_values
    
    else:
        print('Drive is empty')

        return_values['exists'] = 'FALSE'
        return_values['id'] = ''

        return return_values



def Queue_for_posting():
    global data_dict
    print("Queueing for posting")
    submissions_to_queue = []
    #submissions_in_prev_queue = []
    #submissions_in_prev_queue_to_persist = []
    # final destination
    #submissions_in_queue = []
    #url_part = 'https://drive.google.com/uc?export=download&id='

    # Refresh data
    test = load_sheet()
    if (test) == 'error':
        return 'error'

    for i in data_dict.keys():
        if (data_dict[i]['Submission'] != '') and ((data_dict[i]['Approval'] == 'TRUE') and (data_dict[i]['Approval'] != 'FALSE') and (data_dict[i]['Approval'] != '')) and (((data_dict[i]['Status'] == 'Waiting') or (data_dict[i]['Status'] == 'Queued')) and (data_dict[i]['Status'] != 'Processing') and (data_dict[i]['Status'] != 'N') and (data_dict[i]['Status'] != 'Posted') and (data_dict[i]['Status'] != '')) and ((data_dict[i]['Number'] != '0') and (data_dict[i]['Number'] != '')) and (data_dict[i]['DriveID'] != '') and (data_dict[i]['IGid'] == '') and (data_dict[i]['PostTime'] == ''):
            submissions_to_queue.append(i)
    
    print(submissions_to_queue)
    
    '''
    # Check if some posts have not been posted yet
    #timecurrent = checkTime()

    #persistentTimes = []
    #time_increment = 400 #1800.0 #float(time.mktime(datetime.strptime('30', "%M").timetuple()))

    # Find Unposted Posts
    #for i in data_dict.keys():
    #    if (data_dict[i]['Submission'] != '') and ((data_dict[i]['Approval'] == 'TRUE') and (data_dict[i]['Approval'] != 'FALSE') and (data_dict[i]['Approval'] != '')) and ((data_dict[i]['Status'] != 'Waiting') and (data_dict[i]['Status'] != 'Processing') and (data_dict[i]['Status'] != 'N') and (data_dict[i]['Status'] == 'Queued') and (data_dict[i]['Status'] != 'Posted') and (data_dict[i]['Status'] != '')) and ((data_dict[i]['Number'] != '0') and (data_dict[i]['Number'] != '')) and (data_dict[i]['DriveID'] != '') and (data_dict[i]['IGid'] == '') and (data_dict[i]['PostTime'] != ''):
    #        submissions_in_prev_queue.append(i)

    # Remove Old Queue Times
    #if len(submissions_to_queue) > 0:
    #    for i in range(0, len(submissions_to_queue)):
    #        if data_dict[submissions_to_queue[i]]['PostTime'] != '':
    #            if (float(time.mktime(datetime.strptime(data_dict[submissions_to_queue[i]]['PostTime'], "%d/%m/%Y %H:%M:%S").timetuple()))) - (float(time.mktime(datetime.strptime(timecurrent['dt'], "%d/%m/%Y %H:%M:%S").timetuple())) + time_increment) <= 0.0:
    #                data_dict[submissions_to_queue[i]]['PostTime'] = ''
    #                submissions_in_prev_queue.append(submissions_to_queue[i])
                
    #                Update_sheet(submissions_to_queue[i], 'PostTime', data_dict[submissions_to_queue[i]]['PostTime'])
            
    #            elif (float(time.mktime(datetime.strptime(data_dict[submissions_to_queue[i]]['PostTime'], "%d/%m/%Y %H:%M:%S").timetuple()))) - (float(time.mktime(datetime.strptime(timecurrent['dt'], "%d/%m/%Y %H:%M:%S").timetuple())) + time_increment) > 0.0:
    #                submissions_in_prev_queue_to_persist.append(submissions_to_queue[i])
            
    #            else:
    #                print("PostTime removing error")
        
    #        else:
    #            print("...")
        
    #    for i in range(0, len(submissions_in_prev_queue)):
    #        submissions_to_queue.remove(submissions_in_prev_queue[i])
        
    #    for i in range(0, len(submissions_in_prev_queue_to_persist)):
    #        submissions_to_queue.remove(submissions_in_prev_queue_to_persist[i])
        
    #    print(submissions_to_queue)

    # Find most recent Queue Time
    #if len(submissions_in_prev_queue_to_persist) > 0:
    #    for i in range(0, len(submissions_in_prev_queue_to_persist)):
    #        persistentTimes.append((float(time.mktime(datetime.strptime(data_dict[submissions_in_prev_queue_to_persist[i]]['PostTime'], "%d/%m/%Y %H:%M:%S").timetuple()))))

    #if len(persistentTimes) > 0:
    #    latestQueueTime = max(persistentTimes)
    #else:
    #    latestQueueTime = (float(time.mktime(datetime.strptime(timecurrent['dt'], "%d/%m/%Y %H:%M:%S").timetuple())))
    
    # Assign Queue Times
    #print(submissions_in_prev_queue_to_persist)

    #if len(submissions_in_prev_queue_to_persist) > 0:
    #    for i in range(0, len(submissions_in_prev_queue_to_persist)):
    #        submissions_in_queue.append(submissions_in_prev_queue_to_persist[i])
    #        data_dict[submissions_in_prev_queue_to_persist[i]]['Status'] = 'Queued'
    #        Update_sheet(submissions_in_prev_queue_to_persist[i], 'PostTime', data_dict[submissions_in_prev_queue_to_persist[i]]['PostTime'])
    #        Update_sheet(submissions_in_prev_queue_to_persist[i], 'Status', data_dict[submissions_in_prev_queue_to_persist[i]]['Status'])
        
    #    submissions_in_prev_queue_to_persist.clear()

    

    # Assign Times
    #previous_time = (float(time.mktime(datetime.strptime(timecurrent['dt'], "%d/%m/%Y %H:%M:%S").timetuple())))

    # Get the old posts out of the way first
    #if len(submissions_in_prev_queue) > 0:
    #    submissions_in_prev_queue.sort()

    #    for i in range(0, len(submissions_in_prev_queue)):
    #        previous_time = previous_time + time_increment
    #        queueTime = datetime.fromtimestamp(previous_time)

    #        data_dict[submissions_in_prev_queue[i]]['PostTime'] = str(queueTime)
    #        data_dict[submissions_in_prev_queue[i]]['Status'] = 'Queued'

    #        submissions_in_queue.append(submissions_in_prev_queue[i])

    #        Update_sheet(submissions_in_prev_queue[i], 'PostTime', data_dict[submissions_in_prev_queue[i]]['PostTime'])
    #        Update_sheet(submissions_in_prev_queue[i], 'Status', data_dict[submissions_in_prev_queue[i]]['Status'])

            
        
    #    submissions_in_prev_queue.clear()
    '''

    if len(submissions_to_queue) > 0:
        submissions_to_queue.sort()

        for i in range(0, len(submissions_to_queue)):
            #previous_time = previous_time + time_increment
            #queueTime = datetime.fromtimestamp(previous_time)

            #data_dict[submissions_to_queue[i]]['PostTime'] = str(queueTime)
            data_dict[submissions_to_queue[i]]['Status'] = 'Queued'

            #submissions_in_queue.append(submissions_to_queue[i])
            
            #Update_sheet(submissions_to_queue[i], 'PostTime', data_dict[submissions_to_queue[i]]['PostTime'])
            test = Update_sheet(submissions_to_queue[i], 'Status', data_dict[submissions_to_queue[i]]['Status'])
            if (test) == 'error':
                return 'error'
        
        #submissions_to_queue.clear()



def Update_sheet(index, category, value):
    range_to_write = ''
    column_letter = ''
    row_number = ''
    _value = ([str(value)], [])

    # Assign Column Letter
    if category == 'Approval':
        column_letter = 'C'
        '''
        #if value == 'TRUE':
        #    _value = TRUE
        #elif value == 'FALSE':
        #    _value = FALSE
        #else:
        #    _value = value
        #    print("boss, we're gonna have a problem")
        '''
    elif category == 'Status':
        column_letter = 'E'
    elif category == 'Number':
        column_letter = 'D'
    elif category == 'DriveID':
        column_letter = 'F'
    elif category == 'IGid':
        column_letter = 'G'
    elif category == 'PostTime':
        column_letter = 'H'
    else:
        print("could not classify category, update_sheet()")
    
    # Assign Row Number
    try:
        row_number = str(int(index) + 2)
    except:
        print("could not assign row number, update_sheet()")

    # Assign Range to Write
    try:
        range_to_write = str(column_letter) + str(row_number)
    except:
        print("could not assign range to write, update_sheet()")

    print(index, category)
    print(range_to_write)
    
    value_ = {'majorDimension': 'ROWS', 'values': _value}

    print("VALUE:" + str(value_))

    print("range:"+ str(str(range_)+"!"+str(range_to_write)))

    try:
        sheets_service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=str(range_)+"!"+str(range_to_write), valueInputOption="USER_ENTERED", body=value_).execute()
    except:
        return 'error'
    
    time.sleep(0.5)



def checkTime():
    # datetime object containing current date and time
    now = datetime.now()
 
    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    return_data = {'dt': dt_string}

    return return_data



def createMediaObject(params) :
	""" Create media object
	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
		https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['caption'] = params['caption']  # caption for the post
	endpointParams['access_token'] = params['access_token'] # access token

	if 'IMAGE' == params['media_type'] : # posting image
		endpointParams['image_url'] = params['media_url']  # url to the asset
	else : # posting video
		endpointParams['media_type'] = params['media_type']  # specify media type
		endpointParams['video_url'] = params['media_url']  # url to the asset
	
	return makeApiCall(url, endpointParams, 'POST') # make the api call



def getMediaObjectStatus(mediaObjectId, params) :
	""" Check the status of a media object
	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'status_code' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall(url, endpointParams, 'GET') # make the api call



def publishMedia(mediaObjectId, params) :
	""" Publish content
	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['creation_id'] = mediaObjectId # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall(url, endpointParams, 'POST') # make the api call



def getContentPublishingLimit(params) :
	""" Get the api limit for the user
	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'config,quota_usage' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall(url, endpointParams, 'GET') # make the api call

'''

#def orderOfOperations():
#    time.sleep(1)
#    load_sheet()
#    time.sleep(1)
#    Queue_for_creation()
#    time.sleep(1)
#    print("Regular Check Completed")
'''


def choose_post():
    global data_dict
    global connected
    print("Network Status: " + connected)
    time.sleep(0.2)
    test = Queue_for_creation()
    if (test) == 'error':
        print("Network Error")
        connected = 'FALSE'
        return
    else:
        print("No problems with Queue Creation")
        connected = 'TRUE'
    time.sleep(0.2)
    test = Queue_for_posting()
    if (test) == 'error':
        print("Network Error")
        connected = 'FALSE'
        return
    else:
        print("No problems with Queue for Posting")
        connected = 'TRUE'
    time.sleep(0.2)
    test = load_sheet()
    if (test) == 'error':
        print("Network Error")
        connected = 'FALSE'
        return
    else:
        print("No problems with Loading Sheet")
        connected = 'TRUE'

    submissions_in_queue = []
    numbers_of_submissions = []

    #timecurrent = checkTime()
    submission_to_post = ''

    for i in data_dict.keys():
        if (data_dict[i]['Submission'] != '') and ((data_dict[i]['Approval'] == 'TRUE') and (data_dict[i]['Approval'] != 'FALSE') and (data_dict[i]['Approval'] != '')) and ((data_dict[i]['Status'] != 'Waiting') and (data_dict[i]['Status'] != 'Processing') and (data_dict[i]['Status'] != 'N') and (data_dict[i]['Status'] == 'Queued') and (data_dict[i]['Status'] != 'Posted') and (data_dict[i]['Status'] != '')) and ((data_dict[i]['Number'] != '0') and (data_dict[i]['Number'] != '')) and (data_dict[i]['DriveID'] != '') and (data_dict[i]['IGid'] == '') and (data_dict[i]['PostTime'] == ''):
            submissions_in_queue.append(i)
            numbers_of_submissions.append(int(data_dict[i]['Number']))
    
    if len(submissions_in_queue) > 0:
        for i in range(0, len(submissions_in_queue)):            
            #if abs((float(time.mktime(datetime.strptime(data_dict[submissions_in_queue[i]]['PostTime'], "%Y-%m-%d %H:%M:%S").timetuple()))) - (float(time.mktime(datetime.strptime(timecurrent['dt'], "%d/%m/%Y %H:%M:%S").timetuple())))) < 150.0:
            #    submission_to_post = submissions_in_queue[i]
            #    print("Attempting to Post")
            #    post_image(submission_to_post)
            #else:
            #    print("Not Going To Post Anything")
            if data_dict[submissions_in_queue[i]]["Number"] == str(min(numbers_of_submissions)):
                submission_to_post = submissions_in_queue[i]
                print("Attempting to Post")
                test = post_image(submission_to_post)
                if (test) == 'error':
                    print("Network Error")
                    connected = 'FALSE'
                    return
                else:
                    connected = 'TRUE'
            else:
                print("Not Going To Post Anything")
    
    print("Network Status: " + connected)
    print("check completed at " + str(datetime.now()))
                


def post_image(index):
    global data_dict
    print('Attempting to send Image')

    sleep_time = randint(30, 120)
    time.sleep(sleep_time)

    host = "8.8.8.8"
    response = os.system("ping " + ("-n 1 " if  platform.system().lower()=="windows" else "-c 1 ") + host)
    # and then check the response...
    if response != 0:
        return 'error'

    params = getCreds() # get creds from defines

    params['media_type'] = 'IMAGE' # type of asset
    params['media_url'] = 'https://drive.google.com/uc?export=download&id=' + str(data_dict[index]['DriveID']) # url on public server for the post
    params['caption'] = str(data_dict[index]['Submission'])

    imageMediaObjectResponse = createMediaObject(params) # create a media object through the api
    imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created
    imageMediaStatusCode = 'IN_PROGRESS'

    while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
        imageMediaObjectStatusResponse = getMediaObjectStatus(imageMediaObjectId, params) # check the status on the object
        imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code

        print("\n---- IMAGE MEDIA OBJECT STATUS -----\n") # display status response
        print("\tStatus Code:") # label
        print("\t" + imageMediaStatusCode) # status code of the object

        time.sleep(5) # wait 5 seconds if the media object is still being processed

    publishMedia(imageMediaObjectId, params) # publish the post to instagram

    data_dict[index]['IGid'] = imageMediaObjectId
    data_dict[index]['Status'] = 'Posted'
    data_dict[index]['PostTime'] = (checkTime())['dt']

    test = Update_sheet(index, 'IGid', data_dict[index]['IGid'])
    if (test) == 'error':
        return 'error'
    test = Update_sheet(index, 'Status', data_dict[index]['Status'])
    if (test) == 'error':
        return 'error'
    test = Update_sheet(index, 'PostTime', data_dict[index]['PostTime'])
    if (test) == 'error':
        return 'error'

    contentPublishingApiLimit = getContentPublishingLimit(params) # get the users api limit

    print(contentPublishingApiLimit['json_data_pretty'])



def screenshot(number, text):

    font_size = 46.0

    title_size = 72.0

    if len(text) < 500:
        font_size = 46.0
    elif len(text) < 750:
        font_size = 38.0
    elif len(text) < 1000:
        font_size = 33.0
    elif len(text) < 1250:
        font_size = 29.0
    elif len(text) < 1750:
        font_size = 25.0
    elif len(text) < 2000:
        font_size = 23.0
    elif len(text) < 3000:
        font_size = 19.0
    elif len(text) < 4000:
        font_size = 16.0
    elif len(text) < 5000:
        font_size = 15.0
    elif len(text) < 7500:
        font_size = 12.0
    elif len(text) < 10000:
        font_size = 10.5
    else:
        font_size = 9.0

    if len(str(number)) < 4:
        title_size = 72.0
    elif len(str(number)) < 5:
        title_size = 68.0
    elif len(str(number)) < 6:
        title_size = 65.0
    else:
        title_size = 62.0
    
    content = dict(title = number, description = text, fontSize = font_size, titleSize = title_size)

    HTML = '''
    <!DOCTYPE html>
    <html>
    <head> 
    <style>
    .container {
        position: relative;
        text-align: center;
        height: 1080px;
        width: 1080px;
    }

    .centered {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: sans-serif;
        font-size:{{fontSize}}px;
        font-weight: light;
    }

    .top-center {
        position: absolute;
        top: 66px;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: sans-serif;
        font-size:{{titleSize}}px;
        font-weight: bold;
    }

    div {
        word-wrap: break-word;
        width: 1060px;
    }

    body {
        margin: 0;
        padding: 0;
    }
    
    </style>
    </head>
    <body>
    <div class="container">
        <img src='C:\\Users\\Dark Menace\\proj\\Template.png' style="width:1080px;height:1080px;">
	    <div class="top-center"; style="text-align:center; color:white;">Engineering Confession #{{title}}</div>
        <div class="centered"; style="text-align:center; color:black;">{{description}}</div>
    </div>
    </body>
    </html>
    '''
    rendered_output = Environment().from_string(HTML).render(**content)
    with open('base.html', 'w', encoding='utf8') as f:
        f.write(rendered_output)
    
    time.sleep(0.2)

    hti = Html2Image()
    hti.screenshot(html_file='base.html', save_as=(str(number) + '.png'), size=(1080, 1080))
    time.sleep(0.2)


'''
def refresh_ig_token():
    # Perform age check
    age_check = {}
    timecurrent = checkTime()
    try:
        params = getCreds()
        params['type'] = ''
        age_check = debugAccessToken(params)
    except:
        print("NO_GO")
    
    difference = 7776000.0 - (float(age_check['json_data']['data']['data_access_expires_at']) - float(time.mktime(datetime.strptime(timecurrent['dt'], "%d/%m/%Y %H:%M:%S").timetuple())))
    print(difference)
    print(datetime.fromtimestamp(difference))
    print(datetime.fromtimestamp(age_check['json_data']['data']['data_access_expires_at']))

    if difference > 172800.0:
        params = getCreds()
        params['type'] = ''
        print(params)
        #refresh = refreshLongLivedAccessToken(params)
        url = "https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token="# + ''
        print(url)
        refresh = requests.get(url)
        #try:
        #except:
        #    print("NO GO")
        print("Response: "+str(refresh))
        #print(refresh['access_token'])
        #print(refresh['expires_in'])
    else:
        print("Access Token is still new")
'''


main()
#schedule.every(loopTime).minutes.do(choose_post)

time.sleep(1)

while True:
    #schedule.run_pending()
    #time.sleep(1)
    print("Network Status: " + connected)
    if connected == 'TRUE':
        time.sleep(120)
        choose_post()
    elif connected == 'FALSE':
        time.sleep(60)
        choose_post()
    else:
        print("Error choosing scheduling time")