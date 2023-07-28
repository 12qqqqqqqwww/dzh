import requests
from bs4 import BeautifulSoup
import pandas as pd
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}
def getNews():
    r=requests.get("https://news.cnstock.com/news/sns_jg/index.html",headers=headers)
    r.encoding="utf-8"
    soup=BeautifulSoup(r.text,'html.parser')
    articles=soup.find_all(name='li',attrs={"class":"newslist"})
    title = []
    content = []
    link = []
    for artile in articles:
        title.append(artile.find_all(name="a")[0]['title'])
        link.append(artile.find_all(name="a")[0]['href'])
        content.append(artile.find_all(name="p",attrs={"class":"des"})[0].string)
    df=pd.DataFrame({"title":title,"content":content,"link":link})
    return df
