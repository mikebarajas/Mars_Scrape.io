

# Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request
import requests
import pymongo
from selenium import webdriver
from splinter import Browser
import time


# Import HTML Code
html = urllib.request.urlopen('https://mars.nasa.gov/news/').read()
soup = bs(html, 'html.parser')
mars = {}

# Print all title texts
news_title = soup.find_all('div', class_='content_title')
for title in news_title:
    news_tit = title.text.strip()
    mars.update({'newsTitle': news_tit})

# Print all paragraph texts
news_p = soup.find_all('div', class_='rollover_description_inner')
for p in news_p:
    text = p.text.strip()
    mars.update({'newsText': text})

# Import Splinter and set the chromedriver path
executable_path = {"executable_path": "./chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Visit the following URL
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
articles = soup.find('a', class_ = 'button fancybox')
browser.click_link_by_partial_text('FULL')
xpath = '//*[@id="fancybox-lock"]/div/div[1]/img'
time.sleep(2)
# to bring up the full resolution image
results = browser.find_by_xpath(xpath)
img = results['src']
mars.update({'featuredImage': img})
time.sleep(2)
# Mars Weather
html = urllib.request.urlopen('https://twitter.com/marswxreport?lang=en').read()
soup = bs(html, 'html.parser')
weather = soup.find("div", class_="js-tweet-text-container").text
text = p.text.strip()
mars.update({'marsWeather': weather})

# Import HTML Code
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
tables[0]
df = tables[0]
df.columns = ['variable','measurements']
fact_list = df["variable"]
value_list = df["measurements"]
fact_value = zip(fact_list, value_list)
table_dic = {}
for fact, value in fact_value:
    table_dic[fact] = value
for fact, value in fact_value:
    mars[fact] = value
# Import Splinter and set the chromedriver path
executable_path = {"executable_path": "./chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
hemispheres = soup.find('div', class_ = 'collapsible results')
title = []
img_url = []
hemispheres = ["Cerberus","Schiaparelli","Syrtis","Valles"]
for hemisphere in hemispheres:
    browser.click_link_by_partial_text(hemisphere) 
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find("div", class_="downloads").ul.li.a["href"]
    text = soup.body.find('h2').text
    mars.update({text:img})
    browser.click_link_by_partial_text('Back')
    time.sleep(2)


print(mars)

