import requests
from bs4 import BeautifulSoup as bs
import os
from pprint import pprint
ID = 'hacker'
PW = 'zxcvb1@345'


































with requests.Session() as s:

	loginURL = 'http://lms.sunmoon.ac.kr/ilos/lo/login.acl'
	mainURL = 'https://lms.sunmoon.ac.kr/ilos/main/main_form.acl'
	returnURI = '%2Filos%2Fst%2Fcourse%2Fsubmain_form.acl'
	eclass_room2 = 'https://lms.sunmoon.ac.kr/ilos/st/course/eclass_room2.acl'
	submain_form = 'https://lms.sunmoon.ac.kr/ilos/st/course/submain_form.acl'
	report_list_form = 'https://lms.sunmoon.ac.kr/ilos/st/course/report_list_form.acl'

	class_name = list()
	class_code = list()

	LOGIN_INFO = {
		'usr_id': ID,
		'usr_pwd': PW,
	}

	ECLASS_INFO = {
		'KJKEY' : 'A2018305351111',
		'returnURI' : returnURI,
		'encoding' : 'utf-8'
	}


	login_req = s.post(loginURL, data = LOGIN_INFO)
	mainBody = s.get(mainURL)

	soup_mainBody = bs(mainBody.text, 'html.parser')
	opened_class = soup_mainBody.select('em.sub_open ')

	#태그에서 과목명, 분반 얻어냄
	for TAG in opened_class:
		test = str(TAG.text)
		class_name.append(" ".join((test.replace("\n", "").strip().split())))

	#태그에서 과목 코드만 얻어냄
	for TAG in opened_class:
		test = str(TAG)
		class_code.append(test[42:56])

	# 과목명, 과목코드 출력
	# for i in range(len(class_name)):
	#  	print(class_name[i] + " " + class_code[i])

	#for j in range(len(class_name)):
	#test = list()
	report_list = list()
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

		#print(merged_report[0])
	#과제 가져오기 끝
		#for i in 
		# for i in range(len(report_list)):
		# 	print(i, report_list)
	
		#print(test[0])

		#print(report_info)
# 		submain_req = s.post(submain_form)
# 		soup_submain = bs(submain_req.text, 'html.parser')

# 		notice_class = soup_submain.select(
# 			'#submain-contents > .submain-leftarea  > .submain-notice'
# #공지#submain-contents > div.submain-leftarea > div.submain-notice.submain-notice-first > div.submain-noticebox > ol > li:nth-child(1) > em > a
# #과제#submain-contents > div.submain-leftarea > div:nth-child(4) > div.submain-noticebox > ol > li:nth-child(1) > em > a
# #시험#submain-contents > div.submain-leftarea > div.submain-notice.submain-notice-last > div.submain-noticebox > ol > li:nth-child(1) > em > a
# 			)
		# print(notice_class)

		# for TAG in notice_class:
		# 	test = (str(TAG.text))
		# 	print(test)	
		


	

#로그인 -> 메인에서 과목코드 얻기 -> eclass_room2에 과목코드 보내주고 submain가야함

	#find_classcode = test.find("eclassRoom")
	#print(find_classcode)
	#classname, classcode, classid


	#print(type(test))
	# str(className)
# [선문]English Reading and Writing II (053511-11) A2018305351111
# [선문]리눅스운영체제응용 (245084-11) A2018324508411
# [선문]모바일SW프로젝트(CapstoneDesign) (245107-11) A2018324510711
# [선문]사제동행세미나 (011017-ED) A20183011017ED
# [선문]알고리즘 (244005-12) A2018324400512
# [선문]인성채플 (011022-13) A2018301102213
# [선문]임베디드프로그래밍 (245092-13) A2018324509213
# [선문]창의적 사고와 글쓰기 (011018-23) A2018301101823