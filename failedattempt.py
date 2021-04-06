import requests
from bs4 import BeautifulSoup

# Ok technically this works and I later can make this script output the results in a json
# but the website blocks me from getting all the results on the website and limits me to
# only 160 at a time. Could not find a way around it.

source_code = 'INTERPOL_RN'
source_name = 'INTERPOL Red Notices'

url = 'https://ws-public.interpol.int/notices/v1/red?resultPerPage=100&page='
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
total_results = soup.find("strong", {"id": "searchResults"})

page = 1
data = []

while True:

    response = requests.get(f'{url}{page}')
    current_response = response.json()['_embedded']['notices']
    page += 1

    if len(data) != 0 and current_response[len(current_response) - 1] == data[len(data) - 1]:
        break
    data += current_response

for i in range(len(data)):
    print(data[i])