from bs4 import BeautifulSoup
import requests

def get_li_items():
    page = requests.get('https://covid19.min-saude.pt/relatorio-de-situacao/')
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", class_="single_content")
    ul = div.find_all("ul")[0]
    li_tags = ul.find_all('li')#li with all links for reports
    return li_tags