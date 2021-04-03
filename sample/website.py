from bs4 import BeautifulSoup
import requests

def get_li_items():
    page = requests.get('https://covid19.min-saude.pt/relatorio-de-situacao/')
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find_all("div", class_="c-accordion__content")
    li_tags = []
    for tag in div:
        lis = tag.find_all('ul')[0].find_all('li')
        for li in lis:
            li_tags.append(li)
    return li_tags