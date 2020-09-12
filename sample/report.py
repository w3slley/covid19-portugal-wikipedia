import sample.website as web
import urllib.request
import os
import sample.date as date
import sample.pdf as pdf
import sample.format as format

def info_latest(): #of the latest DGS report on Covid-19
    li_tags = web.get_li_items()
    link = li_tags[0].a.get('href') #get the url from the upmost link (which is the most recent report)
    most_recent_pdf_date = str(li_tags[0].text[-10:])
    
    return {'link': link, 'report_date':most_recent_pdf_date}

#if there is no report on DGS' website for the current day, download latest report (previous day).If not, there is a report for today and the date will be the current one for the path
def download(url, REPORT_PATH):
    if os.path.isfile(REPORT_PATH):
        print('PDF report was already downloaded')
    else:
        print('Downloading PDF file')
        urllib.request.urlretrieve(url, REPORT_PATH)


def delete(REPORT_PATH):
    if os.path.isfile(REPORT_PATH):
        os.remove(REPORT_PATH)
        
    else:
        print('No file in directory '+REPORT_PATH) 

#I need to find a way to only call the convert_pdf_to_txt() function only once (for efficiency reasons)
def get_summary_data(REPORT_PATH):
    data = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[0])
    lines = format.remove_empty_str(data.splitlines())
    fields = ['active', 'recovered','deaths','under_surveillance', 'confirmed_cases']
    report_values = ['ATIVOS', 'RECUPERADOS', 'ÓBITOS', 'EM VIGILÂNCIA', 'CONTACTOS EM VIGILÂNCIA', 'CONFIRMADOS']
    results=[]
    for index, value in enumerate(lines):
        if len(results) == 5:
            break
        #checking for each item on pdf(change in format could break this though)
        if value in report_values:
            result_str = lines[index-1] #getting string two positions before curr value (based on format)
            operator = format.get_operator(result_str)#getting the operator (+ or -) which separates data from change in increase/decrease
            results.append(format.get_digits(result_str.split(operator)[0]))#getting only the digits from the leftmost part of string (where the correct values are)
    obj = {}
    for i in range(len(results)):
        obj[fields[i]] = results[i]
    data_age_gender = get_data_by_age_and_gender(REPORT_PATH)    
    obj.update(data_age_gender)
    return obj

    
def get_data_by_age_and_gender(REPORT_PATH):
    data = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[1])
    lines = format.remove_empty_str(data.splitlines())
    #initial index for cases and deaths numbers
    cases_index = 0
    deaths_index = 0
    #array which stores data to be returned
    data = []
    for index, value in enumerate(lines):
        if value == 'TOTAL DE CASOS':
            cases_index = index+1
        if value == 'TOTAL DE ÓBITOS':
            deaths_index = index+1
    labels = ['homens', 'mulheres','875'] #875 is somehow hidden in the pdf but is displayed when we get the text from it, so one needs to ignore it to get correct values (in this case for the death numbers). If it changes in future reports, one should update it here
    for i in range(4):
        content_case = lines[cases_index+i]
        content_death = lines[deaths_index+i]
        if content_case.lower() not in labels:
            data.append(format.get_digits(content_case))
        if content_death.lower() not in labels:
            data.append(format.get_digits(content_death))
 
    return {'cases_men': data[0], 'deaths_men': data[1], 'cases_women': data[2], 'deaths_women': data[3]}

def get_hospitalized_data(REPORT_PATH):
    data = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[0])
    lines = format.remove_empty_str(data.splitlines())
    values = []
    init = 0
    #getting index where data starts
    for index, value in enumerate(lines):
        if value == 'DISTRIBUIÇÃO DOS CASOS EM INTERNAMENTO':
            init = index+1

    for i in range(6):#going through the next 6 items in the list from the DISTRIB.. text
        op = format.get_operator(lines[init+i])
        if op != '|' and lines[init+i].lower() != 'internamento':
            value = format.get_digits(lines[init+i].split(op)[0])
            values.append(value)
    
    return {'hospital_stable': values[0], 'hospital_icu': values[1]}
    


