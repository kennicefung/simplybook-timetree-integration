import timetree_client
import simplybook_client
import firestore_client
import gsheet_client

import json

from datetime import datetime

def handler(event, context):
    booking_id = json.loads(event['body'])['booking_id']
    booking_hash = json.loads(event['body'])['booking_hash']
    company = json.loads(event['body'])['company']
    notification_type = json.loads(event['body'])['notification_type']


    # record the whole received request
    firestore_client.record_simplybook_noti(booking_id,booking_hash,company,notification_type)

    # get booking detail from simplybook
    booking = simplybook_client.get_booking_details(booking_id, booking_hash)

    booking_code = booking['result']['code']
    event_id = booking['result']['event_id']
    event_name = booking['result']['event_name']

    client_name = booking['result']['client_name']
    client_email = booking['result']['client_email']
    client_phone = booking['result']['client_phone']

    start_date_time_obj = datetime. strptime(booking['result']['start_date_time'], '%Y-%m-%d %H:%M:%S').isoformat()
    end_date_time_obj = datetime. strptime(booking['result']['end_date_time'], '%Y-%m-%d %H:%M:%S').isoformat()

    duration = booking['result']['event_duration']
    class_package = booking['result']['membership_name'] if booking['result']['membership_name'] != None else ''
    rental_package = booking['result']['package_name'] if booking['result']['package_name'] != None else ''

    membership_rest = booking['result']['membership_rest']
    membership_limit = booking['result']['membership_limit']
    remaining_class_session = f'{membership_rest} / {membership_limit}' if class_package != '' else 'N/A'

    package_rest = booking['result']['package_service_rest']
    package_limit = booking['result']['package_service_limit']
    remaining_rental_session = f'{package_rest} / {package_limit}' if rental_package != '' else 'N/A'

    class_package_deadline = booking['result']['membership_period_end'] if class_package != '' else 'N/A'
    rental_package_deadline = booking['result']['package_period_end'] if rental_package != '' else 'N/A'


    if(notification_type == 'create'):

        if event_name != None and 'RENTAL' in event_name.upper():
            # create timetree event
            timetree_id = timetree_client.create_event(client_name, event_name, start_date_time_obj, end_date_time_obj)

            # record timetree id
            firestore_client.record_timetree_id(booking_id,timetree_id)

        #else:
        #    timestamp = datetime.strptime(booking['result']['start_date_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M')
        #    timetree_id = firestore_client.get_timetree_id(f'gc{event_id}-{timestamp}')
        #    timetree_client.create_comment(client_name, client_email, client_phone)

        # insert google sheet
        gsheet_client.insert_booking(booking_code, client_name, client_phone, client_email, event_name, start_date_time_obj, end_date_time_obj, duration, class_package, rental_package, remaining_class_session, remaining_rental_session, class_package_deadline, rental_package_deadline)
    
    if(notification_type == 'change'):
        # get timetree event id
        timetree_id = firestore_client.get_timetree_id(booking_id)

        # update timetree event
        timetree_client.update_event(timetree_id, client_name, event_name, start_date_time_obj, end_date_time_obj)

        # update google sheet
        gsheet_client.update_booking(booking_code, client_name, client_phone, client_email, event_name, start_date_time_obj, end_date_time_obj, duration, class_package, rental_package, remaining_class_session, remaining_rental_session, class_package_deadline, rental_package_deadline)
    
    if(notification_type == 'cancel'):
        # get timetree event id
        timetree_id = firestore_client.get_timetree_id(booking_id)

        # delete timetree event
        timetree_client.delete_event(timetree_id)

        # delete from google sheet
        gsheet_client.cancel_booking(booking_code)



    return {
        'statusCode': 200,
        #'body': json.dumps(booking_id + ' ; ' + booking_hash + ' ; ' + company + ' ; ' + notification_type)
        'body': json.dumps('success')
    }