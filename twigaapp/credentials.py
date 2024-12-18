import json
import base64
import requests
from decouple import config
from datetime import datetime
from requests.auth import HTTPBasicAuth


class MpesaC2bCredential:
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    api_URL = config('API_URL')


class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL, auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]


class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = config('BUSINESS_SHORT_CODE')
    OffSetValue = config('OFFSETVALUE')
    passkey = config('PASSKEY')

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')