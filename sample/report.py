import sample.website as web
import urllib.request
import os
import sample.date as date
import sample.pdf as pdf
import sample.format as format

def info(): #of the latest DGS report on Covid-19
    li_tags = web.get_li_items()
    link = li_tags[0].a.get('href') #get the url from the upmost link (which is the most recent report)
    most_recent_pdf_date = str(li_tags[0].text.split(' | ')[1])
    
    return {'link': link, 'report_date':most_recent_pdf_date}

#if there is no report on DGS' website for the current day, download latest report (previous day).If not, there is a report for today and the date will be the current one for the path
def download(REPORT_PATH):
    #Checking if the latest report was downloaded
    if os.path.isfile(REPORT_PATH):
        print('Most current PDF report was already downloaded')
        #in case there are .txt files in the output folder (which means the tables and graphs were already parsed)
        if date.get_current_date().replace('-','/') == info()['report_date'] and os.path.isfile('output/english/SummaryTable.txt'): #cheking only one since they are generated together
            print('Tables and graphs were already generated!')
            confirm = input('Do you want to generate the Wikipedia graphs and tables again? (y/n): ')
            while confirm != 'y' and confirm != 'n':#while answer is not y/n
                confirm = input('Not a valid response. Answer y (yes) or n (no): ')
            if confirm == 'n':
                return False
    else:
        print('Downloading latest DGS report as a PDF file...')
        urllib.request.urlretrieve(info()['link'], REPORT_PATH)
        print('PDF file downloaded successfuly!')
     
    return True


#I need to find a way to only call the convert_pdf_to_txt() function only once (for efficiency reasons)
def get_summary_data(REPORT_PATH):
    page_summary = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[0])
    lines = page_summary.splitlines()
    fields = ['suspected_cases','confirmed_cases','not_confirmed_cases', 'waiting_results','recovered','deaths','under_surveillance']
    results=[]
    on = False
    for line in lines:
        if len(results)==7:#results list already has all values
            break
        first_char=line[0] if line !='' else ''
        if on and first_char>='0' and first_char<='9':
            results.append(line)
        if line == '2020) ':#getting total suspected cases data
            on = True
    obj = {}
    for i in range(len(results)):
        obj[fields[i]] = results[i] 
    return obj


def get_data_from_list(l, start, end):
    data_points = []
    on = False
    for line in l:
        if on:
            data_points.append(line)
        if line == start:
            on = True
        if line == end:
            break
    return data_points
    
def get_data_by_age_and_gender(option, REPORT_PATH):
    #config for each option
    if option == 'cases':
        txt = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[1]).splitlines()
        start = 'Total'
        end = 'Dados até dia 22 | ABRIL | 2020 | 24:00'
    elif option == 'deaths':
        txt = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[3]).splitlines()
        start = 'Total'
        end = 'Saiba mais em https://covid19.min-saude.pt/'
    else:
        raise TypeError('option must be either "cases" or "deaths"')
    #returning data as string
    men = ''
    women = ''
    n = 9 #number of fields in the graph (ranging from ages 0-09 to 80+)
    list_of_data = get_data_from_list(txt, start, end)
    cases = []
    #removing empty strings from list
    for i in list_of_data:
        if i!='':cases.append(i)
    for i in range(n):
        if i == n-1: 
            men+=cases[i]
            women+=cases[i+10]
        else:
            men+=str(cases[i])+', '
            women+=str(cases[i+10])+', '
    return {'men': men, 'women': women}

def get_hospitalized_data(REPORT_PATH):
    page_hospitalized = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[3]).splitlines()
    
    txt = get_data_from_list(page_hospitalized, 'COVID-19', 'FEBRE')
    data = []
    #parsing only the desired data (which are numbers and in that interval they are the only ones)
    for i in txt:
        #there are empty strings in the list and they should be ignored
        if i=='': continue 
        if i[0]>='0' and i[0]<='9':
            data.append(i)
    hospital_stable = data[0] if len(data)!=0 else '0'
    hospital_icu = data[1] if len(data)!=0 else '0'
    return {'hospital_stable':hospital_stable, 'hospital_icu': hospital_icu}


def get_symptoms_data(REPORT_PATH):
    page_deaths = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[3]).splitlines()
    data = get_data_from_list(page_deaths, 'FEBRE', 'GRUPO ETÁRIO')
    percentages = []
    phrase_occurance = []
    for i in data:
        #there are empty strings in the list and they should be ignored
        if i=='': continue
        #getting all percentages
        if i[2]=='%':
            percentages.append(i)
        #getting occurrence data
        elif i[:10]=='Informação':
            phrase_occurance.append(i)
    occurrence = phrase_occurance[0].split('em ')[1].split(' dos')[0]
    
    return {'occurrence': occurrence, 'percentages': percentages}

