from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import time
import DataManager as dm

# dm.connect_db()

ttl = []
dts = []
desc_l = []
urll = []
body = []
url = 'https://therecord.media/search-results?category=&sort=articles_date_desc&term=Automotive'
chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument("window-size=1920,1080")
driver = Chrome(options=chrome_options)
driver.get(url)
wait = WebDriverWait(driver, 80)
time.sleep(3)

def scrapping(last_entry_date):
    for title, type, ur, desc in zip(titles, types, urr, descs):
        if type.text != '' and pd.to_datetime(type.text) > last_entry_date:
            title_text = title.text
            if title_text.startswith("BRIEF"):
                title_text = title_text[5:]
            ttl.append(title_text)
            dts.append(type.text)
            urls = ur.find_element(By.TAG_NAME, 'a')
            urll.append(urls.get_attribute('href'))
            desc_l.append(desc.text)

            req = requests.get(urls.get_attribute('href'))
            time.sleep(3)
            soup = BeautifulSoup(req.content, "html.parser")
            ref = soup.find('div', class_="article__content")
            p_text = ""
            for r in ref:
                if str(r).startswith("<div") or str(r).startswith("<div>"):
                    break
                p_text += r.text.strip("\n") + " "
            body.append(p_text)

    return dts, ttl, desc_l, urll, body
scraper_name = "therecord"
last_entry_date = dm.get_last_entry_date(scraper_name)
time.sleep(5)
element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/section/div[1]/main/section/div/div[3]/div/ul/li[4]/a')
driver.execute_script("arguments[0].click();", element)
time.sleep(3)
types = driver.find_elements(By.CLASS_NAME, 'article-tile__meta__date')
titles = driver.find_elements(By.CLASS_NAME, 'article-tile__title')
descs = driver.find_elements(By.CLASS_NAME, 'ais-Snippet')
urr = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
dts, ttl, desc_l, urll, body = scrapping(last_entry_date)
driver.get(url)
time.sleep(3)
types = driver.find_elements(By.CLASS_NAME, 'article-tile__meta__date')
titles = driver.find_elements(By.CLASS_NAME, 'article-tile__title')
descs = driver.find_elements(By.CLASS_NAME, 'ais-Snippet')
urr = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
dts, ttl, desc_l, urll, body = scrapping(last_entry_date)
time.sleep(3)

record_flag = 0
df = pd.DataFrame(list(zip(dts, ttl, desc_l, urll, body)), columns=['Date', 'Title', 'Description', 'URL', 'Body'])
df['record_flag'] = record_flag
df['Date'] = pd.to_datetime(df['Date'])
print(df.shape)

df.sort_values(by='Date', ascending = False, inplace = True)
if df.empty:
    print("Now new data to dump")
else:
    dm.insert_data(df)
driver.quit()