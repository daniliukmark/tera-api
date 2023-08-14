import requests
from bs4 import BeautifulSoup
import json


class FootballData:
    
    main_url = 'http://www.vilniausfutbolas.lt/lyga/III-lyga/20'
    

    def get_target_url(self):
        first_response = requests.get(self.main_url)
        if first_response.status_code != 200:
            
            return print('Request failed with status code:', first_response.status_code)
        soup = BeautifulSoup(first_response.content, 'html.parser')
        for link in soup.select('a[href*="turnyrine-lentel"]'):        
            return link['href']
    
    def format_data(self):
        target_url = self.get_target_url()
        final_response = requests.get(target_url)
        if final_response.status_code != 200:
            return print('Final request failed with status code:', final_response.status_code)
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
        return headings, rows

    def get_data(self):
        try:
            headings, rows = self.format_data()
            my_lst = []
            for row in rows: 
                combined = dict(list(zip(headings, row)))
                my_lst.append(combined)
            json_data = json.dumps(my_lst, ensure_ascii=False, indent=4)
            return json_data
        except:
            return print("Response status is not 200")

    def save_data(self):
        try:
            json_string = json.loads(self.get_data())
            with open('footballdata.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_string, json_file, ensure_ascii=False, indent=4)
        except:
            return print('Json string cannot be serialized. Response status is not 200')
            

my_url = FootballData()
my_url.save_data()