import pprint
import json
from collections import defaultdict
import collections

for TAG in report_info:
   temp_str = str(TAG.text)

   if "조회할 자료가 없습니다" not in temp_str:
      list_temp_report.append(" ".join((temp_str.replace("\n", "").strip().split())))

   # else:
      

list_urls = []

for TAG in report_info:
   first = 0
   last = 0
   temp_url = str(TAG)

   if "site-link" in temp_url:
      # url index in tag : first = 44, last = 95
      for i in range(len(temp_url)):
         if temp_url[i] == "/" and first == 0:
            first = i
         elif temp_url[i] == '&' and last == 0:
            last = i
      list_urls.append(temp_url[first:last])	

   