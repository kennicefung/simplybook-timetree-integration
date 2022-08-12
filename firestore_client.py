import os
import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import firestore

from dotenv import load_dotenv

load_dotenv()


cred = credentials.Certificate(os.getenv('GOOGLE_CREDENTIALS_JSON'))
firebase_admin.initialize_app(cred)

db = firestore.client()

def record_simplybook_noti(booking_id, booking_hash, company, notication_type):


	doc_ref = db.collection(os.getenv('SIMPLYBOOK_NOTI_TABLE_NAME')).document(booking_id+'_'+datetime.now().strftime('%Y%m%d%H%M%S'))
	doc_ref.set({
	    u'booking_id': booking_id,
	    u'booking_hash': booking_hash,
	    u'company': company,
	    u'notication_type': notication_type
	})


def record_timetree_id(booking_id, timetree_id):


	doc_ref = db.collection(os.getenv('BOOKING_TIMETREE_MAP_TABLE_NAME')).document(booking_id)
	doc_ref.set({
	    u'timetree-id': timetree_id
	})


def get_timetree_id(booking_id):


	doc_ref = db.collection(os.getenv('BOOKING_TIMETREE_MAP_TABLE_NAME'))
	doc = doc_ref.document(booking_id).get()

	if doc.exists:
		return doc.to_dict()['timetree-id']
	
