#!/usr/bin/python3

import lxml.html
import requests
import sys
import re
import csv

if len(sys.argv) != 3:
    print("Two args required: city name & URL")
    sys.exit(1)

def getRedirURL(url):
    try:
        string = requests.head(url).next.url
        return string
    except:
        return ""

def getContactURLTwitter(url):
    contact_url = url.replace("click?id=", "click?cid=")
    twitter_url = url.replace("click?id=", "click?tid=")
    return getRedirURL(contact_url), getRedirURL(twitter_url)

def getContactInfo(url):
    html = requests.get(url)
    doc = lxml.html.fromstring(html.content)
    contact_h2 = doc.xpath('.//h2[text()="Contact"]')[0]
    try:
        content = contact_h2.getparent().text_content()
    except:
        return ""
    found = re.findall("Contact.*For ", content)[0]
    r1 = re.sub("^Contact", "", found)
    r2 = re.sub("For $", "", r1)
    return r2

url = str(sys.argv[2])

html = requests.get(url)
doc = lxml.html.fromstring(html.content)

urls = doc.xpath("//a[contains(@href, 'click?id=')]")

news = []

for i in urls:
    click_url = i.values()[0]
    next_a = i.getnext()

    news_name = i.getnext().text
    contact_url, twitter  = getContactURLTwitter(click_url)
    try:
        contact = getContactInfo(next_a.values()[0])
    except:
        contact = ""
    row = [news_name, contact, contact_url, twitter]
    print(row)
    news.append(row)

news.sort()

csv_filename = sys.argv[1]+'.csv'
with open(csv_filename, 'w', newline='') as f:
     mywriter = csv.writer(f, delimiter='|') 
     mywriter.writerows(news)
