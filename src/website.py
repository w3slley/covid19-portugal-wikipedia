from bs4 import BeautifulSoup
import requests

def get_li_items(filename):
    if filename == 'portugal_data.csv':
        url = 'https://covid19.min-saude.pt/relatorio-de-situacao/'
        class_name = 'c-accordion__content'
    elif filename == 'portugal_vaccine_data.csv':
        url = 'https://covid19.min-saude.pt/relatorio-de-vacinacao/'
        class_name = 'single_content'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find_all("div", class_=class_name)
    li_tags = []
    for tag in div:
        lis = tag.find_all('ul')[0].find_all('li')
        for li in lis:
            li_tags.append(li)
    return li_tags
