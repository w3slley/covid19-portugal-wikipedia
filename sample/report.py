from bs4 import BeautifulSoup
import datetime
import urllib.request
import requests
import os
import sample.pdf as pdf


def info():
    page = requests.get('https://covid19.min-saude.pt/relatorio-de-situacao/')
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", class_="single_content")
    ul = div.find_all("ul")[0]
    li_tags = ul.find_all('li')
    link = li_tags[0].a.get('href')
    pdf_name = link.split('/2020/')[1][3:]
    most_recent_pdf_date = str(li_tags[0].text.split(' | ')[1])
    
    return {'link': link, 'report_date':most_recent_pdf_date}

def download():
    #formatting current date
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month) if len(str(now.month))==2 else '0'+str(now.month)
    day = str(now.day) if len(str(now.day))==2 else '0'+str(now.day)
    curr_date = day+'/'+ month +'/'+year
    
    filename = 'var/most_recent_dgs_report.pdf'
    data = info()
    ##Checking if the latest report has today's date. If not, download it.
    if os.path.isfile(filename) and curr_date == data['report_date']:
        print('Most recent PDF report was already downloaded!')
        print(f"Date of most recent report: {data['report_date']}")
    else:
        print('Downloading latest DGS report as a PDF file...')
        urllib.request.urlretrieve(data['link'], filename)
        print('PDF file downloaded successfuly!')
        return True
        
    return False


#right now I have to create and delete .txt files to take advantage of the readline() function. I have to improve that later. I also need to find a way to only call the convert_pdf_to_txt() function only once (for efficiency reasons)
def get_summary_data():
    page_summary = pdf.convert_pdf_to_txt('var/most_recent_dgs_report.pdf', pages=[0])
    filename = 'var/page_summary.txt'
    g = open(filename, 'w+')
    g.write(page_summary)
    g.close()
    f = open(filename, 'r')
    results=[]
    on = False
    while True:
        line = f.readline()
        if line == '2020) \n':#getting total suspected cases data
            f.readline()#ignoring break line
            results.append(f.readline().split('\n')[0])
        if line=='Açores\n':
            break
        if on and line !='\n':#retrieving all the other data from front page
            results.append(line.split('\n')[0])
        if line == 'Saúde\n':
            on = True 
    f.close()
    os.remove(filename)
    return results


def get_data_from_txt(filename, start, end):
    f = open(filename, 'r')
    data_points = []
    on = False
    while True:
        line = f.readline()
        if on and line !='\n':
            data_points.append(line.split("\n")[0])
        if line == start:
            on = True
        if line==end:
            break
    f.close()
    
    return data_points
    
def get_data_by_age_and_gender(option):
    if option == 'cases':
        page_cases = pdf.convert_pdf_to_txt('var/most_recent_dgs_report.pdf', pages=[1])
        filename = 'var/page_cases.txt'
        f = open(filename, 'w+')
        f.write(page_cases)
        f.close()
        
        start = 'Total\n'
        end = 'Dados até dia 22 | ABRIL | 2020 | 24:00\n'
    elif option == 'deaths':
        page_deaths = pdf.convert_pdf_to_txt('var/most_recent_dgs_report.pdf', pages=[3])
        filename = 'var/page_deaths.txt'
        f = open(filename, 'w+')
        f.write(page_deaths)
        f.close()
        
        start = 'Total\n'
        end = 'Saiba mais em https://covid19.min-saude.pt/\n'
    else:
        raise TypeError('option must be either "cases" or "deaths"')
    #returning data as string
    men = ''
    women = ''
    n = 9 #number of fields in the graph (ranging from ages 0-09 to 80+)
    cases = get_data_from_txt(filename, start, end)
    for i in range(n):
        if i == n-1: 
            men+=cases[i]
            women+=cases[i+10]
        else:
            men+=str(cases[i])+', '
            women+=str(cases[i+10])+', '

    os.remove(filename)#deleting txt file
    return {'men': men, 'women': women}
    
def get_symptoms_data():
    page_deaths = pdf.convert_pdf_to_txt('var/most_recent_dgs_report.pdf', pages=[3])
    filename = 'var/page_deaths.txt'
    f = open(filename, 'w+')
    f.write(page_deaths)
    f.close()

    g=open(filename,'r')
    data = get_data_from_txt(filename, 'GENERALIZADA\n', 'CARACTERIZAÇÃO DOS ÓBITOS OCORRIDOS\n')
    percentages = data[:6]
    occurrence = data[6].split('em ')[1].split(' dos')[0]
    g.close()
    os.remove(filename)

    return {'occurrence': occurrence, 'percentages': percentages}

def beautify_number(number: str):
    n = len(number)
    pos = []
    ans = ''
    i=1
    while n-i*3>0:
        pos.append(n-i*3-1)
        i+=1
    for j in range(n):
        ans+=str(number[j])
        if j in pos:
            ans+=','
    return ans

    
