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

#given the inputs one or two positions before the "report_values" tags, select the correct one
def choose_valid_input(lines,index):
    ans = ""
    #loop through the two valid positions where the valid data should be
    for i in range(1,3):
        data = format.remove_space(lines[index-i])
        #getting the operator (+ or -) which separates data from change in increase/decrease
        operator = format.get_operator(data)
        if format.is_digit(data):
            return data
        elif len(data.split(operator)[0])!=0: 
            return format.remove_space(data.split('+')[0])

#I need to find a way to only call the convert_pdf_to_txt() function only once (for efficiency reasons)
def get_summary_data(REPORT_PATH):
    data = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[0])
    lines = format.remove_empty_str(data.splitlines())
    fields = ['active', 'recovered','deaths','under_surveillance', 'confirmed_cases']
    #added a ' ' at the end of the fields (due to change in the PDF format)
    report_values = ['ATIVOS ', 'RECUPERADOS ', 'ÓBITOS ', 'EM VIGILÂNCIA ', 'CONTACTOS EM VIGILÂNCIA ', 'CONFIRMADOS ']
    results=[]
    for index, value in enumerate(lines):
        if len(results) == 5:
            break
        #checking for each item on pdf(change in format could break this though)
        if value in report_values:
            #adding to results list only valid data from pdf
            results.append(choose_valid_input(lines,index))

    obj = {}
    for i in range(len(results)):
        obj[fields[i]] = results[i]
    data_age_gender = get_data_by_age_and_gender(REPORT_PATH)    
    obj.update(data_age_gender)

    if format.are_values_valid(obj)==False:
         raise Exception("An error has occured while parsing the data in the method get_summary_data()")

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
        #looking for total cases/deaths numbers in txt file (actual data is one index after the words TOTAL DE CASOS e TOTAL DE ÓBITOS)
        #strip_empty_str removes all ' ' characters in a string
        if format.remove_space(value.lower()) == 'totaldecasos':
            cases_index = index+1
        if format.remove_space(value.lower()) == 'totaldeóbitos':
            deaths_index = index+1
    
    #appending number of cases/deaths to list data
    for i in range(2):
        cases = format.get_digits(lines[cases_index+i])

        #fixing problem with data on women's death out of order
        if i == 1:
            pos = i
            for j in range(-5,6):#loop through neighbor positions and check if they are valid
                d = format.get_digits(lines[deaths_index+j])
                if len(d)>=4 and not(d in data): 
                    pos = j
        else:
            pos = i
        deaths = format.get_digits(lines[deaths_index+pos])
        if cases=='' or deaths=='': 
            raise Exception("An error has occured while parsing the data in the get_data_by_age_and_gender() method")
        data.append(cases)
        data.append(deaths)
    
    return {'cases_men': data[0], 'deaths_men': data[1], 'cases_women': data[2], 'deaths_women': data[3]}

def get_hospitalized_data(REPORT_PATH):
    data = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[0])
    lines = format.remove_empty_str(data.splitlines())
    values = []
    init = 0
    #getting index where data starts (using method remove_space to prevent future changes in the format - like adding a ' ' at the end of the words like in this case)
    for index, value in enumerate(lines):
        if format.remove_space(value.lower()) == 'distribuiçãodoscasoseminternamento':
            init = index+1
    #Data regarding patients in hospital and in ICU are in positions init+0 e init+2
    for i in range(2):
        number = format.remove_space(lines[init+(2*i)])
        if(format.is_digit(number)):
            values.append(number)

    return {'hospital_stable': values[0], 'hospital_icu': values[1]}
    


