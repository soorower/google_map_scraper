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


sleep(3)

url = 'https://www.google.com/search?q=abattoirs+in+uk&sxsrf=ALeKk00cqbYPGFRthPsaAbZqmoO_G-6BnQ%3A1616764810946&source=hp&ei=it9dYM7BN_bbz7sPw4i1cA&iflsig=AINFCbYAAAAAYF3tmh-xSUTL_sV3e1VQ6-Ux1qclrBqH&oq=&gs_lcp=Cgdnd3Mtd2l6EAEYADIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1AAWABg-vgBaAFwAHgAgAEAiAEAkgEAmAEAqgEHZ3dzLXdperABCg&sclient=gws-wiz'
driver.get(url)
sleep(0.5)

driver.find_element_by_link_text("View all").click()
sleep(0.5)
name_list=[]
lst = {}
for i in range(10):
    names = driver.find_elements_by_xpath("//div[@class='dbg0pd']/div")
    
    for name in names:
        list1= name.text
        list = f'{list1} uk'
        lst = {
            'industry':list
        }
        name_list.append(lst)
    driver.find_element_by_link_text("Next").click()
    sleep(4)
    driver.execute_script("window.scrollTo(0, 1000)")
df = pd.DataFrame(name_list)
df.to_excel('gmap_links.xlsx',encoding='utf-8', index=False)
