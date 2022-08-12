import os
import pygsheets
from datetime import datetime
from dotenv import load_dotenv



load_dotenv()

gc = pygsheets.authorize(service_file=os.getenv('GOOGLE_SHEET_CRED_TOKEN'))


sh = gc.open_by_url(os.getenv('GOOGLE_SHEET_URL'))
bws = sh.worksheet_by_title(os.getenv('GOOGLE_SHEET_BOOKING_RECORD'))
pws = sh.worksheet_by_title(os.getenv('GOOGLE_SHEET_PURCHASE_RECORD'))

record_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def insert_booking(booking_code, client_name, client_phone, client_email, event_name, start_date_time, end_date_time, duration, class_package, rental_package, remaining_class_session, remaining_rental_session, class_package_deadline, rental_package_deadline):
	bws.append_table(values=[booking_code, record_date_time, client_name, client_phone, client_email, event_name, start_date_time, end_date_time, duration, class_package, rental_package, remaining_class_session, remaining_rental_session, class_package_deadline, rental_package_deadline, 'Active'])

def update_booking(booking_code, client_name, client_phone, client_email, event_name, start_date_time, end_date_time, duration, class_package, rental_package, remaining_class_session, remaining_rental_session, class_package_deadline, rental_package_deadline):
	row_num = bws.find(booking_code)[0].row
	bws.update_row(row_num, values=[booking_code, record_date_time, client_name, client_phone, client_email, event_name, start_date_time, end_date_time, duration, class_package, rental_package, remaining_class_session, remaining_rental_session, class_package_deadline, rental_package_deadline, 'Active'])

def cancel_booking(booking_code):
	row_num = bws.find(booking_code)[0].row
	bws.delete_rows(row_num)

def remove_not_yet_paid_record():
	while True:
		cells = pws.find('Pay Later')
		if(len(cells) > 0):
			print('Found in row ' + cells[0].row)
			pws.delete_rows(cells[0].row)
		else:
			break
