import requests
import sys
import urllib.request
from bs4 import BeautifulSoup
import time
# reviewarray = []
# paraarray = []
# linkarray = []
# titles = []
# link = "/redmi-note-7-pro-nebula-red-64-gb/product-reviews/itmferghuf9ky6ru?pid=MOBFDXZ3UJJ7ETTE&page=2"
r = urllib.request.urlopen('https://www.flipkart.com/oppo-k1-piano-black-64-gb/product-reviews/itmfdy9keddxqvbt?pid=MOBFDY9KSZFK5RDZ')
# content = r.content.decode(encoding='UTF-8')
soup = BeautifulSoup(r, "lxml")
reviews = soup.find_all('reviewsData',{"text" : ""})
# title = soup.find_all('h1', {"class":"title"})
print(reviews)
# for review in reviews:
#     p = review.find_all("p")
#     for s in p:
#         reviewarray.append(s.text+"\n")
#     sp = review.find_all("span", {"class" : "review-text-full"})
#     if(len(sp)==0):
#         sp = review.find_all("span", {"class" : "review-text"})
#     for s1 in sp:
#         if(s1.text not in paraarray):
#             paraarray.append(s1.text.strip())
#             linkarray.append(link)
#             if(len(title)==1):
#                 titles.append(title[0].text)
#             else:
#                 titles.append("Deafult")
# time.sleep(1)
# f = open("reviews.txt", "w+")
# f.write(str(reviewarray))
# f = open("paraarray.txt", "w+")
# prevlink = ""
# for i in range(len(linkarray)):
#     if(linkarray[i]!=prevlink): 
#         f.write('http://www.flipkart.com'+linkarray[i]+"\n")
#         f.write(titles[i]+"\n")
#         f.write(paraarray[i]+"\n")
#         prevlink = linkarray[i]
#     else:
#         f.write(paraarray[i]+"\n")