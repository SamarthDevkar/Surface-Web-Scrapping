from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import DataManager as dm
import pandas as pd
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# dm.connect_db()
def scrape_latest_incidents(last_entry_date):
    ttl = []
    dts = []
    urll = []
    body = []

    url = 'https://cybernews.com/search/Automotive/'
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("window-size=1920,1080")
    driver = Chrome(options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 80)
    time.sleep(3)


    Dates = driver.find_elements(By.TAG_NAME, 'span')
    titles = driver.find_elements(By.TAG_NAME, 'h3')
    urr = driver.find_elements(By.CLASS_NAME, 'thumbnail')

    for title in titles:
        ttl.append(title.text)
    for Date in Dates:
        if Date.text != '':
            date_text = Date.text.strip()
            if date_text[0].isdigit():
                dts.append(date_text)

    for ur in urr:
        urls = ur.find_element(By.TAG_NAME, 'a')
        urll.append(urls.get_attribute('href'))
    for i in urll:
        driver.get(i)
        data = driver.find_element(By.CLASS_NAME, 'content')
        p_text = ""

        soup = BeautifulSoup(data.get_attribute('innerHTML'), "html.parser")
        for element in soup:
            if element.name == "hr":
                break
            p_text += element.get_text(strip=True) + " "
        body.append(p_text)

    driver.quit()

    # Filter out the latest incidents based on the last entry date
    new_dts = []
    new_ttl = []
    new_urll = []
    new_body = []
    for dt, title, url, content in zip(dts, ttl, urll, body):
        incident_date = pd.to_datetime(dt)
        if incident_date > last_entry_date:
            new_dts.append(dt)
            new_ttl.append(title)
            new_urll.append(url)
            new_body.append(content)

    return new_dts, new_ttl, new_urll, new_body

scrapper_name = "cybernews"
last_entry_date = dm.get_last_entry_date(scrapper_name)
dts, ttl, urll, body = scrape_latest_incidents(last_entry_date)

record_flag = 0
descrip = ""
df = pd.DataFrame(list(zip(dts, ttl, urll, body)), columns=['Date', 'Title', 'URL', 'Body'])
df['record_flag'] = record_flag
df['Description'] = descrip
df['Date'] = pd.to_datetime(df['Date'])

print(df.shape)

df.sort_values(by='Date', ascending=False, inplace=True)
if df.empty:
    print("No new data to dump")
else:
    dm.insert_data(df)
