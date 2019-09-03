import requests
from bs4 import BeautifulSoup,NavigableString,Tag,Comment
from bs4.element import Tag

url = 'http://whois.chinaz.com/cymsy.cn'
rep = requests.get(url)

soup = BeautifulSoup(rep.text,'html.parser')

tags = soup.find(attrs={'id':'sh_info'})

# for tag in tags.children:
#     if type(tag) == Tag:
#         info = tag.span
#         if info:
#             print(tag.span.string)

for tag in tags.children:
    if type(tag) == Tag:
        div = tag.div
        if(div):
            if div.string == '过期时间':
                print(tag.span.string)

