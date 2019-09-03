import requests
from bs4 import BeautifulSoup,NavigableString,Tag,Comment
from bs4.element import Tag

url = 'http://whois.chinaz.com/fungaming.me'
rep = requests.get(url)

soup = BeautifulSoup(rep.text,'html.parser')

tags = soup.find(attrs={'id':'sh_info'}).children
for tag in tags:
    if type(tag) == Tag:
        for row in tag.children:
            print(row.string)

