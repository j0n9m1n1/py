from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup as bs
from flow.models import UserData
from collections import defaultdict
import requests
import json
import django
import os
import pprint
import ast
from multiprocessing import Pool
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
django.setup()
'''
start_time = time.time() 
print("--- %s seconds ---" %(time.time() - start_time))
'''
#LMS URL LIST
lms = 'https://lms.sunmoon.ac.kr'
loginURL         = 'http://lms.sunmoon.ac.kr/ilos/lo/login.acl'
mainURL          = 'https://lms.sunmoon.ac.kr/ilos/main/main_form.acl'
returnURI        = '%2Filos%2Fst%2Fcourse%2Fsubmain_form.acl'
eclass_room2     = 'https://lms.sunmoon.ac.kr/ilos/st/course/eclass_room2.acl'
submain_form     = 'https://lms.sunmoon.ac.kr/ilos/st/course/submain_form.acl'
notice_list_form = 'https://lms.sunmoon.ac.kr/ilos/st/course/notice_list_form.acl'
report_list_form = 'https://lms.sunmoon.ac.kr/ilos/st/course/report_list_form.acl'
exam_list_form   = 'https://lms.sunmoon.ac.kr/ilos/st/course/test_list_form.acl'
# @csrf_exempt
# def ptest(request):
# 	p = Pool(1)
# 	p.map(get_report, request) 
@csrf_exempt
def login(request):
	
	print("(def) login failed")

	if request.method == 'GET':
		return HttpResponse("<h1>plz</h1>")
	
	elif request.method == 'POST':

		lms_id = request.POST.get('lms_id', '')
		lms_pw = request.POST.get('lms_pw', '')
		token = request.POST.get('token', '')
		#요청온 lms_id 조회
		
		check_id = UserData.objects.filter(lms_id=lms_id)

		if lms_id and lms_pw and token:
			#id, pw으로 로그인 요청
			check_login = requests.post(loginURL, data = { 'usr_id' : lms_id, 'usr_pwd' : lms_pw })

			#로그인 성공 -> db에 lms_id가 없거나 token이 이 전 토큰과 다르면 request lms_id, token을 save to DB
			if "false" in check_login.text: # error : false = success
				print("(def login)login success")

				#db에 lms_id가 있으면
				if check_id:
					userdata = UserData.objects.get(lms_id=lms_id)
					if userdata.device_token != token:
						userdata.device_token = token
						userdata.save(update_fields=['device_token'])
						userdata.save()
						print("(def login)saved token")
						print("(def login)call get_report")
						
					#과제 목록 불러오기
					else:
						print("(def login)call get_report")
						
				#db에 lms_id가 없으면
				else:
					print('(def login)id not in db')
					#id, token을 insert에 넣고
					insert = UserData(lms_id = lms_id, device_token = token)
					insert.save()
					
					#과제 목록 불러오기
				print("(def login) success")
				return HttpResponse(1)
			#로그인 실패(error : true = fail)
			else:
				print("(def login) fail")
				return HttpResponse(0)
	# return HttpResponse("LOGIN:0")			

@csrf_exempt
def get_report(request):

	start_time = time.time()
	
	lms_id = request.POST.get('lms_id', '')
	lms_pw = request.POST.get('lms_pw', '')
	
	with requests.Session() as s:

		class_name = []
		class_code = []
		report = [[]]

		#로그인 요청
		login_req = s.post(loginURL, data = {'usr_id': lms_id,	'usr_pwd': lms_pw})

		#로그인 실패
		if "true" in login_req.text: 
			print("(def get_report)login fail")
			return HttpResponse("(def get_report)login fail")

		#로그인 성공
		elif "false" in login_req.text:
			print("(def get_report)login success")
			
			main_req = s.get(mainURL)
			soup_mainBody = bs(main_req.text, 'html.parser')
			opened_class = soup_mainBody.select('em.sub_open')

			#태그에서 과목명, 과목 코드 얻어냄
			for TAG in opened_class:
				first = 0
				last = 0
				temp_code = str(TAG)
				temp_str = str(TAG.text)
				class_name.append(" ".join((temp_str.replace("\n", "").strip().split())))

				for i in range(0, len(temp_code)):
					if temp_code[i] == "'":
						if first != 0:	
							last = i

						elif first == 0:
							first = i + 1
				class_code.append(temp_code[first:last])

			usr_class_length = len(class_code)
			list_reports_detail = [[] for i in range(usr_class_length)]
			list_temp_report = []
			length = 0
			
			for code in class_code:
				
				#먼저 eclass_room 세션을 가져와야 조회 가능
				eclass2_req = s.post(eclass_room2, data =
				{
					'KJKEY' : code,
					'returnURI' : returnURI,
					'encoding' : 'utf-8'
				})

				report_req = s.post(report_list_form)
				soup_report = bs(report_req.text, 'html.parser')
				report_info = soup_report.select('tr > td')

				list_urls = []

				for TAG in report_info:
					first = 0
					last = 0
					temp_str = str(TAG.text)
					temp_url = str(TAG)

					if "조회할 자료가 없습니다" not in temp_str:
						list_temp_report.append(" ".join((temp_str.replace("\n", "").strip().split())))

					if "site-link" in temp_url:
						# url index in tag : first = 44, last = 95
						for i in range(len(temp_url)):
							if temp_url[i] == "/" and first == 0:
								first = i
							elif temp_url[i] == '&' and last == 0:
								last = i
						
						list_urls.append(temp_url[first:last])

				 
						
				for i in range(len(list_urls)):
					
					inside_report = s.post(lms+list_urls[i])
					soup_inside_report = bs(inside_report.text, 'html.parser')
					detail_report_info = soup_inside_report.select('tbody > tr > td')
					
					for j in range(0, 6):
						list_reports_detail[length].append(" ".join((detail_report_info[j].text.replace("\n", "").strip().split())))
				
				length += 1	
			
			dict_report = defaultdict(list)
			
			for i in range(len(list_reports_detail)):
				if len(list_reports_detail[i]) < 1:
					for j in range(0, 6):
						list_reports_detail[i].append("과제없음")

				report = '과제 ' + str(0)
				dict_report[class_name[i]] = ({report : ' '})

				for j in range(int(len(list_reports_detail[i])/6)):
					report = '과제 ' + str(j)
					dict_report[class_name[i]][report] = ({

						'과제명' :   list_reports_detail[i][(j * 6 + 1) - 1],
						'제출방식' : list_reports_detail[i][(j * 6 + 2) - 1],
						'게시일' :   list_reports_detail[i][(j * 6 + 3) - 1],
						'마감일'  :  list_reports_detail[i][(j * 6 + 4) - 1],
						'지각제출' : list_reports_detail[i][(j * 6 + 5) - 1],
						'과제내용' : list_reports_detail[i][(j * 6 + 6) - 1],
														    })
			# print(json.dumps(dict_report, indent = 4, ensure_ascii=False))
			print("(def get_report) done")
			prepare_report(lms_id, dict_report, class_name, usr_class_length)
			return JsonResponse(dict_report, safe = False, json_dumps_params = {'ensure_ascii': False})
			
@csrf_exempt
def prepare_report(lms_id, dict_report, class_name, usr_class_length):
	
	list_new_subjects  = []
	list_old_subjects  = []
	list_diff_subjects = []
	list_new_reports   = []
	list_old_reports   = []
	list_diff_reports  = []

	#list_subjects, reports에 최근에 가져온 과목, 과제들 append
	for i in range(usr_class_length):	
		list_new_subjects.append(class_name[i])

		if len(dict_report[class_name[i]]["과제 0"]["과제명"]) > 0:
			list_new_reports.append(dict_report[class_name[i]]["과제 0"]["과제명"])	
		else:
			list_new_reports.append("자료없음")

	# 'SELECT....WHERE lms_id = "hacker" then 컬럼 userdata로 접근가능
	userdata = UserData.objects.get(lms_id = lms_id)

	#userdata.old_subjects가 null이 아니면
	if userdata.old_subjects != 'null':
		#str인 userdata.old_subjects를 list로 바꿔서 대입
		list_old_subjects = ast.literal_eval(userdata.old_subjects)

		for i in range(len(list_new_subjects)):
			#old, new subjects 같을때
			if list_old_subjects[i] == list_new_subjects[i]:
				print("같음")
			#old, new subjects 다를때
			else:
				list_diff_subjects.append(list_old_subjects[i])
				list_diff_subjects.append(list_new_subjects[i])
				print("다름")

	if list_old_subjects != list_new_subjects:
		userdata.old_subjects = list_new_subjects
		userdata.save(update_fields=['old_subjects'])
		userdata.save()
		print("(def prepare_report)NULL SAVED old_subjects")

	if userdata.old_reports != 'null':
		list_old_reports = ast.literal_eval(userdata.old_reports)

		for i in range(len(list_new_reports)):

			if list_old_reports[i] == list_new_reports[i]:
				print("같음")

			else:
				list_diff_reports.append(list_new_subjects[i])
				list_diff_reports.append(list_new_reports[i])
				print("다름")

	if list_old_reports != list_new_reports:
		userdata.old_reports = list_new_reports
		userdata.save(update_fields=['old_reports'])
		userdata.save()
		print("(def prepare_report)NULL SAVED old_reports")

	#NULL일때(첫 로그인시)는 list_diff_에 들어가지 않음
	print("(def prepare_report")
	if len(list_diff_subjects) > 0:
		push_to_client(lms_id, list_diff_subjects, list_diff_reports)

	if len(list_diff_reports)  > 0:
		push_to_client(lms_id, list_diff_subjects, list_diff_reports)

@csrf_exempt
def push_to_client(lms_id, list_diff_subjects, list_diff_reports):

	userdata = UserData.objects.get(lms_id = lms_id)
	token = userdata.device_token
	list_recent_push = []

    # fcm 푸시 메세지 요청 주소
	url = 'https://fcm.googleapis.com/fcm/send'    
	headers = {
        'Authorization': 'key=AAAAVlH36iQ:APA91bEsM4DZZSszq9SMexYkYd1MOwUf3nHAyn2A-wOq2lTPqQA7gPwS8H-DHrE9NMFv3o23CnEqKE2VYjzTcTGGFl9L3AyBiiyCYrB9Mt5JaUGSrmOdblYRS4c7yOGDIe491nM0fGRu',
        'Content-Type': 'application/json; UTF-8',
	}

	 # 한명 지정이면 to, 여럿일 경우 registration_ids[]
	if len(list_diff_subjects) > 0:
		for i in range(int(len(list_diff_subjects) / 2)):
			list_recent_push = ast.literal_eval(userdata.recent_push)

			list_recent_push.insert(0, list_diff_subjects[i+1])
			list_recent_push.insert(0, list_diff_subjects[i])

			userdata.recent_push = list_recent_push
			userdata.save(update_fields=['recent_push'])
			userdata.save()

			content = {'to': token, 'notification': { 'title': list_diff_subjects[i], 'body': list_diff_subjects[i+1]}}
			push_req = requests.post(url, data=json.dumps(content), headers=headers)

	if len(list_diff_reports) > 0:
		for i in range(int(len(list_diff_reports) / 2)):
			list_recent_push = ast.literal_eval(userdata.recent_push)

			list_recent_push.insert(0, list_diff_reports[i+1])
			list_recent_push.insert(0, list_diff_reports[i])

			userdata.recent_push = list_recent_push
			userdata.save(update_fields=['recent_push'])
			userdata.save()
			
			content ={'to': token, 'notification': { 'title': list_diff_reports[i], 'body': list_diff_reports[i+1]}}
			push_req = requests.post(url, data=json.dumps(content), headers=headers)

@csrf_exempt
def get_recent_push(request):
	print("def(get_recent_push) start")

	list_recent_push = []
	lms_id = request.POST.get('lms_id', '')
	userdata = UserData.objects.get(lms_id = lms_id)
	list_recent_push = ast.literal_eval(userdata.recent_push)

	dict_recent_push = defaultdict(list)

	for i in range(int(len(list_recent_push) / 2)):
		title = "제목 " + str(i)
		body = "내용 " + str(i)

		dict_recent_push[title] = list_recent_push[i*2]
		dict_recent_push[body] = list_recent_push[i*2+1]
	
	print("def(get_recent_push) done")
	return JsonResponse(dict_recent_push, safe = False, json_dumps_params = {'ensure_ascii': False})
	