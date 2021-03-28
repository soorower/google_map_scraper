from os import read
from shutil import which
from pandas.io.pytables import PossibleDataLossError, dropna_doc
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import randint
import pandas as pd
import datetime
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time



chrome_options  = Options()
chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)

link = 'https://accounts.google.com/AddSession/identifier?service=accountsettings&continue=https%3A%2F%2Fmyaccount.google.com%2Fsecurity&ec=GAlAwAE&flowName=GlifWebSignIn&flowEntry=AddSession'
driver.get(link)
driver.maximize_window()
driver.find_element_by_xpath("//input[@type='email']").send_keys('enlightenme.services@gmail.com')
driver.find_element_by_xpath("//*[@id='identifierNext']/div/button/div[2]").click()
sleep(2)
driver.find_element_by_xpath("//input[@type='password']").send_keys('123test456')
driver.find_element_by_xpath("//*[@id='passwordNext']/div/button/div[2]").click()

url = 'https://www.google.com/search?q=abattoirs+in+uk&sxsrf=ALeKk02km6liliCiH4Ejd7upsZD85axT3A%3A1616766827715&source=hp&ei=a-ddYN-xKf7XrtoPyLC46Aw&iflsig=AINFCbYAAAAAYF31e_YztJC5ouOOPd3TfkdBS6W0ULSS&oq=&gs_lcp=Cgdnd3Mtd2l6EAEYADIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1AAWABg98IKaAFwAHgAgAEAiAEAkgEAmAEAqgEHZ3dzLXdperABBQ&sclient=gws-wiz'
driver.get(url)
sleep(3)
df = pd.read_excel('gmap_links.xlsx')
all_links = df['industry'].tolist()
driver.find_element_by_xpath("//*[@id='Rzn5id']/div/a[2]").click()
sleep(0.5)
datan = []
listn = {}
counter  = 0
for url1 in all_links:
    counter +=1
    print(counter)
    
    # sleep(0.5)
    try:
        driver.find_element_by_xpath("//input[@class='gLFyf gsfi']").clear()
        driver.find_element_by_xpath("//input[@class='gLFyf gsfi']").send_keys(f'{url1}')
        driver.find_element_by_xpath("//input[@class='gLFyf gsfi']").send_keys(Keys.ENTER)
        # driver.find_element_by_xpath("//span[@class='z1asCe MZy1Rb']").click()
    except:
        pass
    sleep(1)


    try:
        name = driver.find_element_by_xpath('//h2/span').text
    except:
        name= '-'
    print(name)
    try:
        website1 = driver.find_element_by_xpath("//a[@class='ab_button']").get_attribute('href')
        if website1.find('google')+1:
            website = '-'
        else:
            website = website1
    except:
        website = '-'
    print(website)

    try:
        type = driver.find_element_by_xpath("//span[@class='YhemCb']").text
    except:
        type = '-'
    print(type)

    try:
        phone = driver.find_element_by_xpath("//span[@role='link']").text
    except:
        phone = '-'
    print(phone)

    try:
        full_add = driver.find_element_by_xpath("//span[@class='LrzXr']").text.replace(', United Kingdom','')
    except:
        full_add = '-'
    print(full_add)
    try:
        street = full_add.split(',')[0]
    except:
        street = '-'
    print(street)

    try:
        if full_add.split(',')[2]:
            borough = full_add.split(',')[1].replace(' ','')
        else:
            borough = full_add.split(',')[1].split(' ')[1].replace(' ','')
    except:
        borough = '-'
    print(borough)

    try:
        city = full_add.split(',')[-1].split(' ')[1]
    except:
        city = '-'
    print(city)

    try:
        post_co1 = full_add.split(',')[-1].split(' ')[2]
        post_co2 = full_add.split(',')[-1].split(' ')[3]
        post_co = f'{post_co1} {post_co2}'
        
    except:
        post_co = '-'
    print(post_co)
    try:
        map_link1 = driver.find_element_by_xpath("//div[@class='rhsg4 rhsmap5col']/a").get_attribute('data-url')
        map_link = f'https://www.google.com{map_link1}'
    except:
        map_link = '-'
    print(map_link)

    try:
        longitude = map_link.split(',')[0].split('@')[1]
    except:
        longitude = '-'
    print(longitude)

    try:
        lattitude = map_link.split(',')[1]
    except:
        lattitude = '-'
    print(lattitude)

    try:
        map_pic = driver.find_element_by_xpath("//div[@class='rhsg4 rhsmap5col']/a/img").get_attribute('src')
    # print(map_pic)
    except:
        map_pic = '-'
    print(map_pic)

    try:
        rating = driver.find_element_by_xpath("//span[@class='Aq14fc']").text
    except:
        rating = '-'
    print(rating)

    try:
        review_num = driver.find_element_by_xpath("//a[@jsaction='FNFY6c']/span").text.split(' ')[0]
    except:
        review_num = '-'
    print(review_num)


    try:
        photo_link = driver.find_element_by_xpath("//div[@class='rhsg4 luib-5']/div/a").get_attribute('href')
    except:
        photo_link = '-'
        pass
    print(photo_link)

    try:
        driver.find_element_by_xpath("//span[@class='JjSWRd']").click()
        sleep(0.1)

        works = driver.find_elements_by_xpath("//table[@class='WgFkxc']/tbody/tr/td")
        working_hr = []
        for work in works:
            working_h = work.text
            working_hr.append(working_h)
        working_hour = f'{working_hr[0]} : {working_hr[1]}\n{working_hr[2]} : {working_hr[3]}\n{working_hr[4]} : {working_hr[5]}\n{working_hr[6]} : {working_hr[7]}\n{working_hr[8]} : {working_hr[9]}\n{working_hr[10]} : {working_hr[11]}\n{working_hr[12]} : {working_hr[13]}\n'
    except:
        working_hour = '-'
    print(working_hour)
    try:
        about = driver.find_element_by_xpath("//div[@data-attrid='kc:/local:merchant_description']/c-wiz/div/div[2]").text
    except:
        about = '-'
    print(about)

    try:
        social = driver.find_element_by_xpath("//g-link/a").get_attribute('href')
    except:
        social = '-'
    print(social)

    try:
        place_id = driver.find_element_by_xpath("//div[@jscontroller='dqWfVe']").get_attribute('data-pid')

        reviews_link = f'https://search.google.com/local/reviews?placeid={place_id}'
    except:
        place_id = '-'
        reviews_link = '-'
    print(place_id)
    print(reviews_link)

    try:
        google_id = photo_link.split(':')[2].split('!')[0]
    except:
        google_id = '-'
    print(google_id)

    listn ={
        'Name': name,
        'Website':website,
        'Type': type,
        'Phone Number': phone,
        'Full Address': full_add,
        'Street': street,
        'Borough':borough,
        'City':city,
        'Postal Code':post_co,
        'Map Link':map_link,
        'Longitude':longitude,
        'Lattitude':lattitude,
        'Map Picture': map_pic,
        'Place Rating':rating,
        'Number of Reviews':review_num,
        'Photo Link':photo_link,
        'Working Hour':working_hour,
        'About':about,
        'Social Media':social,
        'Place ID':place_id,
        'Google ID':google_id,
        'Reviews Link':reviews_link
    }
    datan.append(listn)
    # try:
    #     driver.find_element_by_xpath("//a[@jsaction='FNFY6c']/span").click()
    #     sleep(0.1)
    # except:
    #     pass
    # try:
    #     driver.find_element_by_xpath("//a[@class='review-more-link']").click()
    #     sleep(0.1)
    # except:
    #     pass
    # try:
    #     reviewer_names = driver.find_elements_by_xpath("//div[@jscontroller='e6Mltc']/div[1]/div/div/a")
    #     reviewer_ratings = driver.find_elements_by_xpath("//div[@class='jxjCjc']/div[3]/div/g-review-stars/span")
    #     reviewer = []
    #     ratings = []
    #     for reviewer_name in reviewer_names:
    #         name = reviewer_name.text
    #         reviewer.append(name)
    #     for reviewer_rating in reviewer_ratings:
    #         r = reviewer_rating.get_attribute('aria-label')
    #         ratings.append(r)
    #     print(reviewer)
    #     print(ratings)
    #     two_reviews = f'{reviewer[0]}: {ratings[0]}/n{reviewer[1]}: {ratings[1]}'
    # except:
    #     two_reviews = '-'
    # print(two_reviews)

df = pd.DataFrame(datan)
df.to_excel('gmap_demo_code.xlsx',encoding='utf-8', index=False)