import os
import requests
import hashlib

from dotenv import load_dotenv

load_dotenv()



# def get_token():
# 	url = os.getenv('SIMPLYBOOK_PATH_GET_TOKEN')
# 	company = os.getenv('SIMPLYBOOK_COMPANY')
# 	api_key = os.getenv('SIMPLYBOOK_API_KEY')
# 	payload = {
#         "method": "getToken",
#         "params": [company, api_key],
#         "jsonrpc": "2.0",
#         "id": 1,
#     }
# 	res = requests.post(url, json=payload).json()
# 	return res['result']

def get_token():
	url = os.getenv('SIMPLYBOOK_PATH_GET_TOKEN')
	company = os.getenv('SIMPLYBOOK_COMPANY')
	api_key = os.getenv('SIMPLYBOOK_API_KEY')
	username = os.getenv('SIMPLYBOOK_USERNAME')
	password = os.getenv('SIMPLYBOOK_PASSWORD')
	payload = {
        "method": "getUserToken",
        "params": [company, username, password],
        "jsonrpc": "2.0",
        "id": 1,
    }
	res = requests.post(url, json=payload).json()
	return res['result']


def get_booking_details(booking_id, booking_hash):
	url = os.getenv('SIMPLYBOOK_PATH_ADMIN')
	company = os.getenv('SIMPLYBOOK_COMPANY')
	plaintext = booking_id + booking_hash + os.getenv('SIMPLYBOOK_SECRET_KEY')
	sign=hashlib.md5(plaintext.encode('utf-8')).hexdigest()
	token = get_token()
	payload = {
        "method": "getBookingDetails",
        "params": [booking_id, sign],
        "jsonrpc": "2.0",
        "id": 1,
    }
	#res = requests.post(url, json=payload, headers={'X-Company-Login': company, 'X-Token': token}).json()
	res = requests.post(url, json=payload, headers={'X-Company-Login': company, 'X-User-Token': token}).json()
	print (res)
	return res
