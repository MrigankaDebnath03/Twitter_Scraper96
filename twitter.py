from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
# import chardet
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#options.add_experimental_option("excludeSwitches",["enable-automation"])
#options.add_experimental_option('useAutomationExtension',False)
#options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")


Keyword = str(input("Enter the keyword: "))
Keyword_data = Keyword.replace(" ", "+")

pages = int(input("Enter number of pages: "))
url = 'https://nitter.net/search?f=tweets&q='+Keyword_data






for i in range(pages):

    driver = webdriver.Chrome(options= options)
    driver.maximize_window()
    driver.get(url)
    time.sleep(15)

    tweet_final=[]
    uname_final=[]
    timesupremacy = []
    

    previous_height = 0
    while True:
        height = driver.execute_script("""
                function getActualHeight(){
                    return Math.max(
                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                    );
                }
                return getActualHeight()
            """)
        
        driver.execute_script(f"window.scrollTo({previous_height},{previous_height+300})")
        time.sleep(1)
        previous_height += 300

        if previous_height >= height:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #driver.quit()

    #print(soup.encode('utf-8'))
    # 
    tweets = soup.findAll('div',{"class":"tweet-content media-body"})

    tweet_list = [[x.text.encode('utf-8')] for x in tweets]
    #print(tweet_list)

    username = soup.findAll('div',{"class":"fullname-and-username"})

    username_list = [[x.text.encode('utf-8')] for x in username]
    #print(username_list)

    timestamp = soup.findAll('span',{"class":"tweet-date"})
    for i in timestamp:
        timestamp_a = i.find('a')
        timestamp_data = timestamp_a['title']
        timesupremacy.append(timestamp_data)

    timesupremacy_a = [[x] for x in timesupremacy]

    for value1, value2, value3 in zip(username_list,tweet_list,timesupremacy_a):
        # thewriter.writerow([value1,value2,value3])
        print((value1[0]).decode("utf-8"),end="\t")
        uname_final.append((value1[0]).decode("utf-8"))
        print((value2[0]).decode("utf-8"),end='\t')
        tweet_final.append((value2[0]).decode("utf-8"))
        print((value3[0]))
        #thewriter.writerows(tweet_list)

        with open('tweetlist_final.csv', 'a', newline='', encoding='utf-8') as g:
            thewriter = csv.writer(g)
            for value1, value2, value3 in zip(uname_final,tweet_final,timesupremacy_a):
                thewriter.writerow([value1,value2,value3])
                print(value1,value2,value3)

        driver.find_element(By.XPATH,'//div[@class="show-more"]/a').click()

        previous_height = 0

    
