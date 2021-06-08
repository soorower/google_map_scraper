import os
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
chrome_options  = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
import re
import requests
from bs4 import BeautifulSoup as bs
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""


print('\n')
quer = input('Input Place/Town: ')
ry = input('Bussiness/Industry type: ')
query = ry + ' in ' + quer
search_que = query.replace('+','%2B').replace(' ','+').replace('(','%28').replace(')','%29').replace('/','%2F').replace('&','%26').replace("'","%27").replace(',','%2C').replace(':','%3A').replace(';','%3B').replace('=','%3D').replace('?','%3F').replace('@','%40').replace('*','%2A').replace('!','%20').replace('#','%23').replace('$','%24')


output_file_name = []
output_file_type = []
file_name = input('Output file name: ')
file_type = input('Output file type(excel/csv): ')
output_file_name.append(file_name)
output_file_type.append(file_type)

limit_search = int(input('How many results you want to scrape: '))+1


driver.get('https://www.google.com/search?q=test&rlz=1C1BNSD_enBD955BD955&oq=test&aqs=chrome.0.69i59j0i271l3j69i60l3j69i61.618j0j7&sourceid=chrome&ie=UTF-8')
sleep(0.5)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

url = 'https://www.google.com/search?q=' + search_que
driver.get(url)
sleep(0.5)

driver.find_element_by_xpath("//div[@class='MXl0lf mtqGb']/span[2]").click()
sleep(0.5)

driver.maximize_window()

lists = []
dat = {}
count = 0
try:
    for i in range(11):
        names = driver.find_elements_by_xpath("//div[@class='cXedhc']/div/div")
        k = len(driver.find_elements_by_xpath("//span[@class='VqFMTc p8AiDd']"))
        names = names[k:]
        
        for nam in names:
            count = count + 1
            if count != limit_search:

                try:
                    name1= nam.text
                    nam.click()
                except:
                    name1 = '-'
                sleep(2)
                name2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='SPZz6b']/h2/span"))
                )
                name2 = name2.text
                name = name2
                try:   
                    if 'http' in driver.find_element_by_xpath("//a[@class='CL9Uqc ab_button']").get_attribute('href'):
                        website1 = driver.find_element_by_xpath("//a[@class='CL9Uqc ab_button']").get_attribute('href')
                        if website1.find('google')+1:
                            website = '-'
                        else:
                            website = website1
                    else:
                        website = '-'
                except:
                    website = '-'

                try:
                    r = requests.get(website, headers = headers,timeout = 5)
                    emails = []
                    for re_match in re.finditer(EMAIL_REGEX, r.text):
                        if re_match.group() in emails:
                            pass
                        else:
                            emails.append(re_match.group())
                    email = emails[0]
                except:
                    email = '-'
                # type = ''
                type = driver.find_element_by_xpath("//span[@class='YhemCb']").text
                # for ty in type1:
                #     type = type + '\n' + ty.text

                try:
                    phone = driver.find_element_by_xpath("//a[@data-dtype='d3ifr']/span").text
                except:
                    phone = '-'

                try:
                    full_add = driver.find_element_by_xpath("//span[@class='LrzXr']").text
                except:
                    full_add = '-'


                try:
                    city = full_add.split(',')[1]
                except:
                    city = '-'


                try:
                    x = full_add.split(',')[-2] + full_add.split(',')[-3]
                    post_co = int(re.search(r'\d+', x).group())
                
                except:
                    post_co = '-'

                # try:
                #     map_link1 = driver.find_element_by_xpath(f"//div[@data-title='{name}']").get_attribute('data-place')
                #     map_link = f'https://www.google.com{map_link1}'
                # except:
                #     map_link = '-'

                # try:
                #     longitude = map_link.split(',')[0].split('@')[1]
                # except:
                #     longitude = '-'


                # try:
                #     lattitude = map_link.split(',')[1]
                # except:
                #     lattitude = '-'

                try:
                    rating = driver.find_element_by_xpath("//div[@class='Ob2kfd']/div/span[@class='Aq14fc']").text
                except:
                    rating = '-'


                try:
                    review_num = driver.find_element_by_xpath("//a[@jsaction='FNFY6c']/span").text.split(' ')[0]
                except:
                    review_num = '-'

                try:
                    social = ''
                    for all in  driver.find_elements_by_xpath("//g-link/a"):
                        social = social + '\n' + all.get_attribute('href')
                except:
                    social = '-'

                try:
                    first_review = driver.find_element_by_xpath("//div[@class='b4vunb']/a").text
                except:
                    first_review = '-'

                try:
                    second_review = driver.find_elements_by_xpath("//div[@class='b4vunb']/a")[1].text
                except:
                    second_review = '-'

                
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

                try:
                    social = ''
                    for all in driver.find_elements_by_xpath("//g-link/a"):
                        social = all.get_attribute('href') + '\n' + social
                except:
                    social = '-'
                dat = {
                'Name':name,
                'Website':website,
                'Email':email,
                'Type': type,
                'Phone':phone,
                'Social': social,
                'Full address': full_add,
                'Rating': rating,
                'Review Number': review_num,
                'First review': first_review,
                'Second Review': second_review,
                'City': city,
                'Postal code': post_co
                # 'Map Link': map_link,
                # 'Longitude': longitude,
                # 'Lattitude': lattitude,
                
                }
                lists.append(dat)
            else:
                sys.exit()
                
        driver.find_element_by_xpath("//*[@id='pnnext']/span[2]").click()
        sleep(4)
        driver.execute_script("window.scrollTo(0, 1000)")
        

    kls = output_file_name[-1]
    if 'excel' in output_file_type:
        df = pd.DataFrame(lists)
        df.to_excel(f'{kls}.xlsx',encoding='utf-8', index=False)
    elif 'Excel' in output_file_type:
        df = pd.DataFrame(lists)
        df.to_excel(f'{kls}.xlsx',encoding='utf-8', index=False)
    elif 'EXCEL' in output_file_type:
        df = pd.DataFrame(lists)
        df.to_excel(f'{kls}.xlsx',encoding='utf-8', index=False)

    else:
        df = pd.DataFrame(lists)
        df.to_csv(f'{kls}.csv',encoding='utf-8', index=False)
    # driver.quit()
except KeyboardInterrupt:
    pass
finally:
    kls = output_file_name[-1]
    if 'excel' in output_file_type:
        df = pd.DataFrame(lists)
        df.to_excel(f'{kls}.xlsx',encoding='utf-8', index=False)
    elif 'Excel' in output_file_type:
        df = pd.DataFrame(lists)
        df.to_excel(f'{kls}.xlsx',encoding='utf-8', index=False)
    elif 'EXCEL' in output_file_type:
        df = pd.DataFrame(lists)
        df.to_excel(f'{kls}.xlsx',encoding='utf-8', index=False)

    else:
        df = pd.DataFrame(lists)
        df.to_csv(f'{kls}.csv',encoding='utf-8', index=False)