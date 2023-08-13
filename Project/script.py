import requests
from bs4 import BeautifulSoup
import json

url = 'http://www.vilniausfutbolas.lt/lyga/III-Lyga/20'

response = requests.get(url)
if response.status_code == 200: 
    #general_html = response.content
    print("Response's been obtained successfullly")
    
    #Getting the link of interest from the main page
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.select('a[href*="turnyrine-lentel"]'):
        link = link['href']
    
    final_response = requests.get(link)
    if final_response.status_code == 200: 
        print("'Final' response's been obtained successfullly")
        
        #with open('output.html', 'wb') as f:  # Use 'wb' for binary write mode
        #    f.write(final_response.content)
        
        soup = BeautifulSoup(final_response.content, 'html.parser')
        target_table = soup.find('table', class_='standings')
        headings = []
        rows = []
        
        th_elements = target_table.find_all('th')
        for th in th_elements:
            headings.append(th.text)

        for tr_blocks in target_table.find_all('tr')[1:]:
            seperated_rows = []
            for td_blocks in tr_blocks.find_all('td'):
                seperated_rows.append(td_blocks.text.strip())
            rows.append(seperated_rows)
        #print(headings)
        #print(rows)
        
    else:
        print("'Final' request failed with status code:", response.status_code) 
else:
    print('Request failed with status code:', response.status_code) 


def get_json(headings, rows): 
    lst = []
    for row in rows: 
        combined = dict(list(zip(headings, row)))
        lst.append(combined)
    json_data = json.dumps(lst, ensure_ascii=False, indent=4)

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(lst, json_file, ensure_ascii=False, indent=4)
    return json_data

print(get_json(headings, rows))