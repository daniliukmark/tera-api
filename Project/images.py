from bs4 import BeautifulSoup
import requests
import os

url = 'http://www.vilniausfutbolas.lt/turnyrine-lentele/20?comp_id=37'
xresponse = requests.get(url)
if xresponse.status_code != 200:
    print('Final request failed with status code:', xresponse.status_code)
    #return
soup = BeautifulSoup(xresponse.content, 'html.parser')
table = soup.find('table', class_='standings')

if table: 
    #img_related_tags = table.find_all('img')
    for tr_block in table.find_all('tr'):
        a_tag = tr_block.find('a')
        if a_tag:
            img_tag = a_tag.find('img')
            if img_tag: #and img_tag.has.attr('src'): #Specify a certain td block in html
                img_src = a_tag.img['src']
            #img_text = a_tag.get_text(strip=True).lower().replace(' ', '-')
                print(img_src)
#            
# GET THE LINKS ONLY
# # #    
    #dict_images_names = [{img.text.lower(): img['src']} for img in img_related_tags]
    #print(dict_images_names)
    
"""output_dir = "logo_images"
os.makedirs(output_dir, exist_ok=True)

for index, image_url in enumerate(image_urls, start=1):
    response = requests.get(image_url)
    
    if response.status_code == 200:
        image_name = f"image_{index}.jpg"  # Or use a different naming scheme
        image_path = os.path.join(output_dir, image_name)
        
        with open(image_path, "wb") as f:
            f.write(response.content)
"""