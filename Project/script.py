import requests
from bs4 import BeautifulSoup


url = 'http://www.vilniausfutbolas.lt/turnyrine-lentele/20?comp_id=37'

response = requests.get(url)
if response.status_code == 200: 
    html_content = response.content
    print("Response's successfullly been obtained")

    with open('output.html', 'wb') as file:  # Use 'wb' for binary write mode
        file.write(html_content)

else:
    print('Request failed with status code:', response.status_code) 

#soup = BeautifulSoup(html, "html.parser")

# print the HTML as text
#print(soup.body.get_text().strip())
