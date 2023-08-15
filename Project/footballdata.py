import requests
from bs4 import BeautifulSoup
import json


class FootballData:
    
    main_url = 'http://www.vilniausfutbolas.lt/lyga/III-lyga/20'
    
    def get_target_url(self):
        first_response = requests.get(self.main_url)
        if first_response.status_code != 200:
            print('Request failed with status code:', first_response.status_code)
            return
        soup = BeautifulSoup(first_response.content, 'html.parser')
        for link in soup.select('a[href*="turnyrine-lentel"]'):        
            return link['href']

    def get_table(self):
        target_url = self.get_target_url()
        if target_url is None:
            return
        final_response = requests.get(target_url)
        if final_response.status_code != 200:
            print('Final request failed with status code:', final_response.status_code)
            return
        soup = BeautifulSoup(final_response.content, 'html.parser')
        table = soup.find('table', class_='standings')
        if table:
            return table
        else: 
            print("Table's location has changed")
            return
    
    def format_data(self):
        target_table = self.get_table()
        if target_table is None:
            return      
        headings = []
        rows = []
        for th_elements in target_table.find_all('th'):
            headings.append(th_elements.text)
        for tr_blocks in target_table.find_all('tr')[1:]:
            seperated_rows = []
            for td_blocks in tr_blocks.find_all('td'):
                seperated_rows.append(td_blocks.text.strip())
                a_tag = td_blocks.find('a')
                if a_tag:
                    img_tag = a_tag.find('img')
                    if img_tag and img_tag.has_attr('src'):
                        img_name = a_tag.get_text(strip=True).lower().replace(' ', '-')
                        seperated_rows.append(img_name.strip())
                    else: 
                        seperated_rows.append(None)      
            rows.append(seperated_rows)
        headings.insert(headings.index('Komanda') + 1, 'Logo')
        return headings, rows

    #Create a list of images and save images in a distinct file
    def get_logo(self):
        target_table = self.get_table()
        if target_table is None:
            return 
        target_url = self.get_target_url()
        if target_url is None:
            return
        target_response = requests.get(target_url)
        if target_response.status_code != 200:
            return
        for tr_blocks in target_table.find_all('tr')[1:]:
            pass      



    def get_data(self):
        try: 
            headings, rows = self.format_data()
            my_lst = []
            for row in rows: 
                combined = dict(zip(headings, row))
                my_lst.append(combined)
            json_data = json.dumps(my_lst, ensure_ascii=False, indent=4)
            return json_data
        except:
            return 

    def save_data(self):
        try:
            json_string = json.loads(self.get_data())
            with open('footballdata.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_string, json_file, ensure_ascii=False, indent=4)
        except:
            return print('Json string cannot be serialized. Go to the link and check whether the table is there')
            
