from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from bs4 import BeautifulSoup as bs
import os
#LMS URL LIST
loginURL = 'http://lms.sunmoon.ac.kr/ilos/lo/login.acl'
mainURL = 'https://lms.sunmoon.ac.kr/ilos/main/main_form.acl'
returnURI = '%2Filos%2Fst%2Fcourse%2Fsubmain_form.acl'
eclass_room2 = 'https://lms.sunmoon.ac.kr/ilos/st/course/eclass_room2.acl'
submain_form = 'https://lms.sunmoon.ac.kr/ilos/st/course/submain_form.acl'
report_list_form = 'https://lms.sunmoon.ac.kr/ilos/st/course/report_list_form.acl'
loginCheck = True
# Create your views here.
@csrf_exempt
def home(request):

	if request.method == 'GET':
		return HttpResponse("<h1>GET</h1>")
	
	if request.method == 'POST':
		lms_id = request.POST.get('lms_id', '')
		lms_pw = request.POST.get('lms_pw', '')
		print("LOG: ", lms_id, lms_pw)

		if not lms_id or not lms_pw:
			print("null")
			return HttpResponse("<h1>NULL</h1>")

		if lms_id and lms_pw:
			print("LOG: User information is not null")

			with requests.Session() as s:

				class_name = list()
				class_code = list()
				report_list = list()

				LOGIN_INFO = {
					'usr_id': lms_id,
					'usr_pwd': lms_pw,
				}

				ECLASS_INFO = {
					'KJKEY' : 'A2018305351111',
					'returnURI' : returnURI,
					'encoding' : 'utf-8'
				}

				login_req = s.post(loginURL, data = LOGIN_INFO)
				#로그인 인증
				if "false" in login_req.text:
					print("LOG: login success")
					loginCheck = False

				elif "true" in login_req.text:
					print("LOG: login fail")
					loginCheck = True

				if loginCheck == True:
					print("<h1>LOG: CHECK YOUR ID, PW</h1>")
					return HttpResponse("<h1>LOG: CHECK YOUR ID, PW</h1>")

				elif loginCheck == False:

					main_req = s.get(mainURL)
					soup_mainBody = bs(main_req.text, 'html.parser')
					opened_class = soup_mainBody.select('em.sub_open ')

					#태그에서 과목명, 분반 얻어냄
					for TAG in opened_class:
						test = str(TAG.text)
						class_name.append(" ".join((test.replace("\n", "").strip().split())))
						print(TAG)

					#태그에서 과목 코드만 얻어냄
					for TAG in opened_class:
						test = str(TAG)
						class_code.append(test[42:56])

					# 과목명, 과목코드 출력
					# for i in range(len(class_name)):
					#  	print(class_name[i] + " " + class_code[i])

					#for j in range(len(class_name)):
					#test = list()
					
					merged_report = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
					#과제 가져오기 시작
					for j in range(1):
						eclass2_req = s.post(eclass_room2, data =
						{
							'KJKEY' : class_code[0],
							'returnURI' : returnURI,
							'encoding' : 'utf-8'
						})

						soup_eclass2 = bs(eclass2_req.text, 'html.parser')
						print(soup_eclass2)

						report_req = s.post(report_list_form)
						soup_report = bs(report_req.text, 'html.parser')

						report_info = soup_report.select('tr > td')

						for TAG in report_info:
							test = str(TAG.text)
							report_list.append(" ".join((test.replace("\n", "").strip().split())))
							#print(report_list, "\n")
						
						for i in range(len(report_list)):
							merged_report[int(i/7)] = merged_report[int(i/7)] + report_list[i] + " "

						array = json.dumps(merged_report)
						
						print(merged_report)
						return HttpResponse(array, content_type='application/json')
		'''
	from django.core import serializers
	def wall_copy(request):
	    posts = user_post.objects.all().order_by('id')[:20].reverse()
	    posts_serialized = serializers.serialize('json', posts)
	    return JsonResponse(posts_serialized, safe=False) 
   


로그인 성공

jsonLogin ({
"isError":false,
"message":"로그인 성공.",
"count":1,
"returnURL" : "",
"ids_yn" : "N"
});

로그인 실패
jsonLogin ({
"isError":true,
"message":"로그인 정보가 일치하지 않습니다.",
"count":1,
"returnURL" : "",
"ids_yn" : ""
});

				'''