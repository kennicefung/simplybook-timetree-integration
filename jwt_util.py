import os
import time
import jwt
import json
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from cryptography.hazmat.primitives.asymmetric import dsa, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

load_dotenv()

def get_private_key():
	pem_data = ''

	with open(os.getenv('TIMETREE_PRIVATE_KEY_LOCATION')) as f:
	    pem_data += f.read()

	key = load_pem_private_key(pem_data.encode(), password=None)
	return key

def generate_jwt():
	#now = time.mktime(datetime.now().timetuple())
	exp = time.mktime((datetime.now() + timedelta(minutes=10)).timetuple())
	iss = os.getenv('TIMETREE_ID')
	#payload = '{"iat": "' + str(now) + '", "exp": "' + str(exp) + '", "iss": "' + iss + '"}'
	payload = '{"exp": "' + str(exp) + '", "iss": "' + iss + '"}'
	encoded = jwt.encode(json.loads(payload), get_private_key(), algorithm='RS256')
	return encoded
