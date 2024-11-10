import requests
import datetime
import time
import pandas as pd
import CveManager as cm

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=10)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# Initialize variables for pagination
Cve_id = []
Cve_desc = []
Cve_Published_Date = []
source_name = "CVE"
last_entry_date = cm.get_last_entry_date(source_name)

url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate={yesterday}T00:00:00.000-05:00&pubEndDate={today}T23:59:59.999-05:00"
response = requests.get(url, headers=headers)
while response.status_code == 503:
    time.sleep(3)
    response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    vulnerabilities = data.get('vulnerabilities', [])
    for vulnerability in vulnerabilities:
        cve = vulnerability.get('cve', {})
        published_date = cve.get('published', '')
        if published_date > last_entry_date:
            cve_id = cve.get('id', '')
            descriptions = cve.get('descriptions', [])
            desc_value = descriptions[0].get('value', '') if descriptions else 'N/A'
            Cve_id.append(cve_id)
            Cve_desc.append(desc_value)
            Cve_Published_Date.append(published_date)
elif response.status_code == 403:
    print("Access to the API is forbidden by administrative rules. Please check any restrictions or rate limits.")

else:
    print(f"Error: {response.status_code} - {response.text}")


df = pd.DataFrame(list(zip(Cve_id, Cve_desc, Cve_Published_Date)), columns=['CVE-id', 'Description', 'Date'])
df.sort_values(by='Date', ascending=False, inplace=True)

print(df.shape)

if df.empty:
    print("No new CVE's found")
else:
    cm.insert_data(df)
