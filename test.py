import pprint
import json
from collections import defaultdict
import collections
'''
			dict_sub_title['과목명']
			dict_report_title['과제명']
			dict_report_submit['제출방식']
			dict_report_post['게시일']
			dict_report_dead['마감일']
			dict_report_late['지각제출']
			dict_report_content['과제내용']


dict_report = defaultdict(list)

for i in range(0, 3):
    subject = '과목명 ' + str(i)
    report = '과제 ' + str(i)
    
    dict_report[subject].append( {report : 'test'})
    dict_report[subject][0][report] = {'과제명' : 'X', '제출방식' : 'X', '게시일' : 'X', '마감일' : 'X', '지각제출' : 'X', '과제내용' : 'X'}
    # dict_report['subject'][0]['과제 0'].append("제출기한" : "ㅁㄴㅇ")
    # dict_report['subject'][report].append([{'과제명' : 'X', '제출방식' : 'X', '게시일' : 'X', '마감일' : 'X', '지각제출' : 'X', '과제내용' : 'X'}])

dict_report['과목명 1'][0]['과제2'] = {'과제명' : 'X', '제출방식' : 'X', '게시일' : 'X', '마감일' : 'X', '지각제출' : 'X', '과제내용' : 'X'}
dict_report['과목명 1'][0]['과제2'] = {'과제명' : 'X', '제출방식' : 'X', '게시일' : 'X', '마감일' : 'X', '지각제출' : 'X', '과제내용' : 'X'}
dict_report['과목명 1'][0]['과제2'] = {'과제명' : 'X', '제출방식' : 'X', '게시일' : 'X', '마감일' : 'X', '지각제출' : 'X', '과제내용' : 'X'}


# dict_subject['subject']['과제 0']['과제명'] = '123'
# dict_subject['subject']['과목'] = test1

print(json.dumps(dict_report, indent = 4, ensure_ascii=False))
'''
# JSONObject jsonObject = new JSONObject(response);
# Iterator subject = jsonObject.keys(); #과목명임

# JSONObject jsonObject2 = jsonObejct.getJSONObject((String) subject.next) #과목에 대한 object -> 과제 
# Iterator keys2 = jsonObject2.keys(); #과제 0 ~ N
test_str = "strqwqweqwe"
print(type(test_str))