# importing the requests library 
import requests 
import re
# import jsonify
from textblob import *
# api-endpoint 
URL = "https://harshith.in/project/url.php"
# location given here 
location = "https://www.flipkart.com/nokia-6-1-plus-black-64-gb/p/itmf8r36g9gfpafg?pid=MOBF8FCFB9KWUTVQ&srno=b_1_1&otracker=hp_omu_Snapdragon%2BProcessor%2BPhones_1_H15FMINN8LZX_1&otracker1=hp_omu_WHITELISTED_neo%2Fmerchandising_Snapdragon%2BProcessor%2BPhones_NA_dealCard_cc_1_NA_1&lid=LSTMOBF8FCFB9KWUTVQCQ7AWU&fm=neo%2Fmerchandising&iid=142b3287-f004-4f30-95ab-763517588513.MOBF8FCFB9KWUTVQ.SEARCH&ppt=Homepage&ppn=Homepage&ssid=gzm65r6u280000001554061597224"
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'url':location} 
# sending get request and saving the response as response object 
r1 = requests.get(url = URL, params = PARAMS) 
r1 = r1.text
# extracting data in json format 
reviews_list = re.findall(r'"(.*?)"', r1)
total = 0
for x in reviews_list:
    res = TextBlob(str(x))
    p = res.polarity
    if p < 0 :
        a = 'Negative'
    elif p ==0:
        a='Neutral'
    else:
        a="Positive"
        total = total + p
print(total)
# print(r1)