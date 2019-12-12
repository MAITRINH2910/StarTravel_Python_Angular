##python crawl.py --no-startup-window

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
import pandas as pd
import time
import pickle
import os 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)

citys = {'Ho Chi Minh':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF07LjmmnLgZgnM1blLbNdWPe0SBKuauRn4jtN1m4TWqGBzNmOm1McbIY6fWLoWg%2BviUj%2FP7hBPDoilM%2B79bUbgIhboztsquKmnhn83%2FWY9torMZu3xIHSdiL4X%2BOW1rU1fvHu08SnTOUi%2BPmnDHbHCFttiEC19Vj5LClSDnH9ADhP6vE%2FhqV6wtJKkjsCW3BgkMFzu4KwBgLvk7atJ0hdOw%3D&city=13170&tick=637039116782&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Ho%20Chi%20Minh%20City&productType=-1&travellerType=1&familyMode=off',
        'Da Nang': 'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9Ll%2BdW79RBPTqc%2FD049StxIFzDYzXpCMqWEjA98CewHcNNXcF3b8m3w9RyX0kC3WLffuorKcIqWxsH6JUEoHVutlB5GLJpJoRnckeclAbBbZxcP47HWDCW8h37XlkBeaaXeiGnjAfFj718KJ7a7pyaQ%3D%3D&city=16440&tick=637038160092&txtuuid=589f56d2-e923-47a2-ace9-0820d2863894&languageId=1&userId=a67a5e7f-f2fe-4359-8c05-ad40c3783b20&sessionId=bw2gpjgmmxre1giy0ty11eh3&pageTypeId=1&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=a67a5e7f-f2fe-4359-8c05-ad40c3783b20&prid=0&checkIn=2019-09-20&checkOut=2019-09-21&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Da%20Nang&productType=-1&travellerType=1&familyMode=off',
        'Ha Noi':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF9KnDlGcy1O%2FCb7nhCRHqBCMPtLCffVIBeoY%2BiY7%2FW0ClmquAKG0EKEiDXgtKYyo0sZwrbl%2FCPjG%2FPFaenrWETU%2FQwUx5zYVkRT9V1SRqIuHQ3fvaxx%2FvSQPmnWDs2AUwbBs9eGBEoCHw6eVC1%2BXloiacY%2FwPspU3wBrNaiQo5vZILskCsWCMh5w6GSWyARLrQ%3D%3D&city=2758&tick=637039116966&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Hanoi&productType=-1&travellerType=1&familyMode=off',
        'Nha Trang':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF4nXBEFt8WfGbmiC%2FljJXfi9R1xRXEs3RlLFc1I%2BnPwzgaWsZry4D8u2ZqHImbNnC0WE2jkGop%2B4ghmDo51%2BcGIdRjNPkpct04fF5NFk%2FXHY%2B35gdLNBLTxzj7oRE3lYsi1J2Q3gAlTX9SRDYdbvchB0pPzPHlbkGKgx1S4b%2F%2BqDUGhF5qJXFIAHM2mvssfgbg%3D%3D&city=2679&tick=637039117178&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Nha%20Trang&productType=-1&travellerType=1&familyMode=off',
        'Da Lat':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF1hHdHn1Z%2FAcMl0P3EmlWyIbulm0%2FxiBJriyiwu3hWTupa551wZJmU1jJ1qPuvPgbHXAPleRNT%2BKzvYUA4TmMFRnUO0JLXHM0VDTESuWXPXmfZjjdruc%2BPPNWljg%2FLBpFXPPWPlZJ3GBRFeYuOTubM9XbBJlPDcezModExOhewivqqNLKBfda4nmEyTBVo%2BWPw%3D%3D&city=15932&tick=637039117364&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Dalat&productType=-1&travellerType=1&familyMode=off',
        'Vung Tau':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9C3GfUjctApwXUPVnhXw1OohujG%2FhlRV74OO4IEx6HWh%2BS6zxaWzxkJI3%2FX2KegDZp4RD6mYcVTunFtl4enUGsjiXytUWCOR7Iq5l1jpiYJczvuDwt%2BPP4JVZ5TC%2BMa3WxfkFVjQ6pq54JTx%2BnutqKw%3D%3D&city=15932&tick=637039117504&txtuuid=98162403-9c82-4d13-826c-d1baf963e603&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Vung%20Tau&productType=-1&travellerType=1&familyMode=off',
        'Sa pa':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF9wg0ayI8TCjDbmas6nEQO0vs9eeHo8OVcXL8IQF0IPalmquAKG0EKEiDXgtKYyo0sZwrbl%2FCPjG%2FPFaenrWETU%2FQwUx5zYVkRT9V1SRqIuHQ3fvaxx%2FvSQPmnWDs2AUwbBs9eGBEoCHw6eVC1%2BXloiacY%2FwPspU3wBrNaiQo5vZQ8MccNiHaUGTbMsJEOBo4A%3D%3D&city=17160&tick=637039117788&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Sapa&productType=-1&travellerType=1&familyMode=off',
        'Hue':'https://www.agoda.com/pages/agoda/default/DestinationSearchResult.aspx?asq=u2qcKLxwzRU5NDuxJ0kOF797AuVSQko8%2FPWLms8S9V5f1fbT90j7iLfEiQzz2M5%2BwgI%2FDzCLKKMqybUrgDR7l5wYHidPP%2FT0UT9olSOV%2BblSdlCmrRvDffNqGNslGgQ%2FgcbOmxJdN6dnVOJhyn3qu%2BNXkMrN4L8GSQsLfM4C6EPs5t3YtLkleXGAktpRrekKqODEtJ0jsAwuCi2pJvBgRA%3D%3D&city=3738&tick=637039117973&languageId=1&userId=81b8f41d-936d-4d7b-9c96-407c79be1f71&sessionId=vow1qmcfu5haczlmed300kle&pageTypeId=103&origin=VN&locale=en-US&cid=-1&aid=130243&currencyCode=VND&htmlLanguage=en-us&cultureInfoName=en-US&ckuid=81b8f41d-936d-4d7b-9c96-407c79be1f71&prid=0&checkIn=2019-09-21&checkOut=2019-09-22&rooms=1&adults=2&children=0&priceCur=VND&los=1&textToSearch=Hue&productType=-1&travellerType=1&familyMode=off'}

# city = 'Da Lat'
import sys
city = sys.argv[1]
print(city)

def getlink(city):
    ad = True
    link_hotel = []
    
    # for city in citys:
    driver.get(citys[city])
    time.sleep(2)
    # textbox_hotel =  driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div/div/div[1]/div/div/input')
    # textbox_hotel.send_keys(city)
    # textbox_hotel.send_keys(Keys.ENTER)
    
    # btn_day = driver.find_element(By.XPATH,'/html/body')
    # btn_day.click()
    # time.sleep(1)

    # btn_search = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div/div/button')
    # btn_search.click()
    # time.sleep(3)

    num_page = driver.find_element(By.XPATH,'//*[@id="paginationPageCount"]').text
    num_page = int(num_page.split(' ')[-1])

    while ad:
        input()
        ad = False
        continue

    for _ in range(num_page):    
        list_hotel = driver.find_element_by_class_name('hotel-list-container').find_elements_by_tag_name("a")
        print(len(list_hotel))
        for hotel in list_hotel:
            # hotel.find_elements_by_tag_name("a")
            # print(hotel)
            try:
                link_hotel.append([city,hotel.get_attribute('href')])
            except:
                pass

        btn_next = driver.find_element_by_xpath('//*[@id="paginationNext"]')
        # driver.execute_script("arguments[0].click();", btn_next)

        btn_next.send_keys("\n")
        time.sleep(5)

        print('link',len(link_hotel))
        
    df = pd.DataFrame(link_hotel)
    df.to_csv('hotels/'+city+'.csv',encoding='utf-8-sig',index = False,header = ['city','url'])


# getlink('Da Nang')


def save(data,list_of_pro,city):
    with open('data/raw_data_hotel_'+city+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('data/list_of_pro_hotel_'+city+'.pickle', 'wb') as handle:
        pickle.dump(list_of_pro, handle, protocol=pickle.HIGHEST_PROTOCOL)

def crawlData(city):
    if os.path.exists('data/raw_data_hotel_'+city+'.pickle'):
        with open('data/raw_data_hotel_'+city+'.pickle', 'rb') as handle:
            data = pickle.load(handle)
    else: data = {}

    if os.path.exists('data/list_of_pro_hotel_'+city+'.pickle'):
        with open('data/list_of_pro_hotel_'+city+'.pickle', 'rb') as handle:
            list_of_pro = pickle.load(handle)
    else: list_of_pro = []

    link_hotel = pd.read_csv('hotels/'+city+'.csv')['url']
    
    for percent,link in enumerate(link_hotel):
        if percent % 100 == 0:
            save(data,list_of_pro,city)
            print('save')
        print(str(percent) + '/' +str(len(link_hotel)))

        list_pro = []
        try:
            driver.get(link)
        except:
            continue
        time.sleep(1)
        try:
            name = driver.find_element_by_xpath('//*[@id="property-critical-root"]/div/div[3]/div[3]/div[2]/div[1]/div[2]/div[1]/h1').text
            address = driver.find_element_by_xpath('//*[@id="property-critical-root"]/div/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/span[1]').text
            # price = int(driver.find_element_by_class_name('PriceRibbon__Price').text.replace(',',''))
            price = int(driver.find_element(By.XPATH,'//*[@id="property-critical-root"]/div/div[3]/div[2]/div[6]/div/div[1]/span[3]').text.replace(',',''))
            
            img = driver.find_element_by_xpath('//*[@id="property-critical-root"]/div/div[3]/div[2]/div[1]/div/img').get_attribute('src')
            rating =  float(driver.find_element_by_xpath('//*[@id="property-critical-root"]/div/div[3]/div[3]/div[1]/div[1]/div/div/div/div[1]/div/span').text)
            
            # 
        except Exception as e:
            # print('e1',e)
            continue
        
        try:
            popular_facility = driver.find_element(By.XPATH, '//*[@id="property-room-grid-root"]/div/div[1]/div[2]/ul').find_elements_by_tag_name("li")
            spro = '//*[@id="property-room-grid-root"]/div/div[1]/div[2]/ul/'
        except Exception as e:
            # print('129',e)
            try:
                popular_facility = driver.find_element(By.XPATH, '//*[@id="abouthotel-features"]/div/div[2]/div[2]/div/div[1]/div/ul').find_elements_by_tag_name("li")
                spro = '//*[@id="abouthotel-features"]/div/div[2]/div[2]/div/div[1]/div/ul/'
            except Exception as e1:
                # print('134',e1)
                continue     

        for i in range(len(popular_facility)):
            # //*[@id="abouthotel-features"]/div/div[2]/div[2]/div/div[1]/div/ul/li[1]/div/span/span
            try:
                # //*[@id="property-room-grid-root"]/div/div[1]/div[2]/ul
                pro = driver.find_element_by_xpath(spro+'li['+str(i+1)+']/div/span/span').text
                # //*[@id="abouthotel-features"]/div/div[2]/div[2]/div/div[1]/div/ul
                list_of_pro.append(pro)
                list_pro.append(pro)
                # print(pro)
            except Exception as e:
                # print('e2',e)
                pass
        list_of_pro = list(set(list_of_pro))
        data[city.replace(' ','')+str(len(data))] = {'name':name,'link':link,'img':img,'address':address, 'rating':rating, 'price':price  ,'properties':list_pro}
        
    return data,list_of_pro
    # for url in link_hotel:
    #     driver.get(url)
    #     time.sleep(2)
    #     break

if not os.path.exists('data/'):
    os.mkdir('data')



data,list_of_pro = crawlData(city)
# print(data)
# print(list_of_pro)
save(data,list_of_pro,city)

# driver.close()
# driver.quit()
