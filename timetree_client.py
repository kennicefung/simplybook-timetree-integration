import os
import requests
import jwt_util
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
	url = os.getenv('TIMETREE_PATH_GET_TOKEN')
	jwt_token = jwt_util.generate_jwt()
	res = requests.post(url, headers={'Accept':'application/vnd.timetree.v1+json', 'Authorization':'Bearer ' + jwt_token})
	if res.status_code == 200:
		print(res.json()['access_token'])
		return res.json()['access_token']



def create_event(client_name, event_name, start_date_time, end_date_time):
	url = os.getenv('TIMETREE_PATH_CREATE_EVENT')
	access_token = get_access_token()
	payload = {
		'data': {
			'attributes': {
				'category': 'schedule',
				'title': client_name + ' - ' + event_name,
				'all_day': 'false',
				#'start_at': '2022-06-17T05:00:00.000Z',
				'start_at': start_date_time,
				'start_timezone': 'Asia/Hong_Kong',
				#'end_at': '2022-06-17T06:00:00.000Z',
				'end_at': end_date_time,
				'end_timezone': 'Asia/Hong_Kong'
			}
		}
	}
	print(payload)
	res = requests.post(url, json = payload, headers={'Accept':'application/vnd.timetree.v1+json', 'Authorization':'Bearer ' + access_token})
	if res.status_code == 201:
		print(res.json())
		return res.json()['data']['id']
	else:
		print(res.json())

def create_comment(client_name, client_email, client_phone):
	url = os.getenv('TIMETREE_PATH_CREATE_COMMENT') + f'/{event_id}/activities'
	access_token = get_access_token()
	payload = {
		'data': {
			'attributes': {
				'content': f'{client_name} ({client_email}  {client_phone}) joined'
			}
		}
	}
	print(payload)
	res = requests.post(url, json = payload, headers={'Accept':'application/vnd.timetree.v1+json', 'Authorization':'Bearer ' + access_token})
	if res.status_code == 201:
		print(res.json())
		return res.json()['data']['id']
	else:
		print(res)

def update_event(event_id, client_name, event_name, start_date_time, end_date_time):
	url = os.getenv('TIMETREE_PATH_UPDATE_EVENT') + f'/{event_id}'
	access_token = get_access_token()
	payload = {
		'data': {
			'attributes': {
				'category': 'schedule',
				'title': client_name + ' - ' + event_name,
				'all_day': 'false',
				#'start_at': '2022-06-17T05:00:00.000Z',
				'start_at': start_date_time,
				'start_timezone': 'Asia/Hong_Kong',
				#'end_at': '2022-06-17T06:00:00.000Z',
				'end_at': end_date_time,
				'end_timezone': 'Asia/Hong_Kong'
			}
		}
	}
	print(payload)
	res = requests.put(url, json = payload, headers={'Accept':'application/vnd.timetree.v1+json', 'Authorization':'Bearer ' + access_token})
	if res.status_code == 200:
		print(res.json())
		return res.json()['data']['id']
	else:
		print(res)


def delete_event(event_id):
	url = os.getenv('TIMETREE_PATH_DELETE_EVENT') + f'/{event_id}'
	access_token = get_access_token()
	res = requests.delete(url, headers={'Accept':'application/vnd.timetree.v1+json', 'Authorization':'Bearer ' + access_token})
	if res.status_code == 204:
		return True
	else:
		print(res)

