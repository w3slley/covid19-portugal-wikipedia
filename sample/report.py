import sample.website as web
import urllib.request
import os
import sample.date as date
import sample.pdf as pdf


def info(): #of the latest DGS report on Covid-19
    li_tags = web.get_li_items()
    link = li_tags[0].a.get('href') #get the url from the upmost link (which is the most recent report)
    pdf_name = link.split('/2020/')[1][3:]
    most_recent_pdf_date = str(li_tags[0].text.split(' | ')[1])
    
    return {'link': link, 'report_date':most_recent_pdf_date}

def download(REPORT_PATH):
    curr_date = date.get_current_date().replace('-', '/')
    #if there is no report on DGS' website for the current day, download latest report (previous day)
    if curr_date != info()['report_date']:
        REPORT_PATH = 'var/DGS_report'+info()['report_date'].replace('/', '-')+'.pdf'
    else:
        REPORT_PATH = 'var/DGS_report'+date.get_current_date()+'.pdf'
    #if not, there is a report for today and the date will be the current one for the path

    ##Checking if the latest report was downloaded
    if os.path.isfile('output/GraphsCasesByAgeAndGender.txt') and os.path.isfile('output/SummaryTable.txt'):
        print('Tables and graphs were already generated!')
        confirm = input('Do you still want to generate the Wikipedia graphs and tables? (y/n): ')
        while confirm != 'y' and confirm != 'n':#while answer is not y/n
            confirm = input('Not a valid response. Answer y (yes) or n (no): ')
        if confirm == 'n':
            return False
    else:
        print('Downloading latest DGS report as a PDF file...')
        urllib.request.urlretrieve(info()['link'], REPORT_PATH)
        print('PDF file downloaded successfuly!')
     
    return True


#right now I have to create and delete .txt files to take advantage of the readline() function. I have to improve that later. I also need to find a way to only call the convert_pdf_to_txt() function only once (for efficiency reasons)
def get_summary_data(REPORT_PATH):
    page_summary = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[0])
    filename = 'var/page_summary.txt'
    g = open(filename, 'w+')
    g.write(page_summary)
    g.close()
    f = open(filename, 'r')
    fields = ['suspected_cases','confirmed_cases','not_confirmed_cases', 'waiting_results','recovered','deaths','under_surveillance']
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
    obj = {}
    for i in range(len(results)):
        obj[fields[i]] = results[i] 
    return obj


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
        if line == '':
            break
    f.close()
    
    return data_points
    
def get_data_by_age_and_gender(option, REPORT_PATH):
    if option == 'cases':
        page_cases = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[1])
        filename = 'var/page_cases.txt'
        f = open(filename, 'w+')
        f.write(page_cases)
        f.close()
        
        start = 'Total\n'
        end = 'Dados até dia 22 | ABRIL | 2020 | 24:00\n'
    elif option == 'deaths':
        page_deaths = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[3])
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

def get_hospitalized_data(REPORT_PATH):
    page_hospitalized = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[3])
    filename = 'var/page_hospitalized.txt'
    f = open(filename, 'w+')
    f.write(page_hospitalized)
    f.close()

    g=open(filename,'r')
    data = get_data_from_txt(filename, 'NÚMERO  DE CASOS\n', 'FEBRE\n')
    g.close()
    os.remove(filename)
    return {'hospital_stable': data[1], 'hospital_icu': data[4]}


def get_symptoms_data(REPORT_PATH):
    page_deaths = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[3])
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

def add_comma(number: str):
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

    
