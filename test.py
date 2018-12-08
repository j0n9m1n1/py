import pprint
import json
from collections import defaultdict
import collections
import requests

token = "dfwYEjHfWkQ:APA91bGKntXlsnXdp7rSMRxX1TEEa_AJXLlfCP2JKy0ZDWvKIZASWP7HmEuYVOGQo2G0E67PH1KkamkM8ulp_ePLUqr0bcb5fUi3-JSPvifrSl-ibCO8Lk7P22b-m_kJ4jrjLeOyncxh"
list_recent_push = []

   # fcm 푸시 메세지 요청 주소
url = 'https://fcm.googleapis.com/fcm/send'    
headers = {
      'Authorization': 'key=AAAAVlH36iQ:APA91bEsM4DZZSszq9SMexYkYd1MOwUf3nHAyn2A-wOq2lTPqQA7gPwS8H-DHrE9NMFv3o23CnEqKE2VYjzTcTGGFl9L3AyBiiyCYrB9Mt5JaUGSrmOdblYRS4c7yOGDIe491nM0fGRu',
      'Content-Type': 'application/json; UTF-8',
}
content = {
  
    "to":token,
    # "notification":{
    #   "title":"Portugal vs. Denmark",
    #   "body":"great match!"
    # },
    "data" : {
      "title" : "Mario",
      "body" : "PortugalVSDenmark"
    }
  
}
st = requests.post(url, data=json.dumps(content), headers=headers)
print(st)