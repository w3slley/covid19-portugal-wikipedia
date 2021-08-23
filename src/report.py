import src.website as web
import urllib.request
import json
import os
import src.date as date
import src.pdf as pdf
import src.format as format

def info_latest(filename): #of the latest DGS report on Covid-19
    li_tags = web.get_li_items(filename)
    link = li_tags[0].a.get('href') #get the url from the upmost link (which is the most recent report)
    if filename == 'portugal_data.csv':
        most_recent_pdf_date = str(li_tags[0].text[-10:])
    else:
        most_recent_pdf_date = str(li_tags[0].text[-11:-1])
    
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


def assign_vaccination_data(results,age_range, a, i):
    results['vaccination_age_group'][age_range]['one_dose'] = a[i+8] + " ("+a[i+14]+")"
    results['vaccination_age_group'][age_range]['completed'] = a[i+20] + " ("+a[i+26]+")"

def get_vaccine_data(VACCINE_REPORT_PATH):
    txt = pdf.convert_pdf_to_txt(VACCINE_REPORT_PATH)
    a=txt.splitlines()
    a=format.remove_empty_str(a)
    results = {}
    results['vaccination_age_group'] = {}

    list_age = ['0_17','18_24','25_49','50_64','65_79','greater_than_80']
    for i in list_age:
        results['vaccination_age_group'][i] = {}
    for i in range(len(a)):
        if 'pelo menos' in a[i]:
            if a[i+1] == 'vacinação iniciada 1':
                results["vaccinated_one_dose"] = a[i+2]
            else: 
                results["vaccinated_one_dose"] = a[i+1]
        if 'vacinação completa' in a[i]:
            results["completely_vaccinated"] = a[i+1]
            break
    for i in range(len(a)):
        if 'Doses Recebidas' in a[i]:
            results["received_doses"] = a[i+2]
        if 'Doses Distribu' in a[i]: 
            results["distributed_doses"] = a[i+2]  
        if '0 – 17' in a[i]:
            assign_vaccination_data(results,'0_17',a,i)    
        if '18 – 24' in a[i]:
            assign_vaccination_data(results,'18_24',a,i) 
        if '25 – 49' in a[i]:
            assign_vaccination_data(results,'25_49',a,i)
        if '50 – 64' in a[i]:
            assign_vaccination_data(results,'50_64',a,i)
        if '65 – 79' in a[i]:
            assign_vaccination_data(results,'65_79',a,i)
        if '≥ 80' in a[i]:
            assign_vaccination_data(results,'greater_than_80',a,i)
    return results
    
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

def get_recent_data_age_gender():
    req = urllib.request.Request('https://covid19-api.vost.pt/Requests/get_last_update')
    req.add_header('User-Agent','Mozilla/5.0')
    url = urllib.request.urlopen(req)
    data_request = url.read()
    data = json.loads(data_request.decode('utf-8'))
    response={
        'date':data['data'],
        'cases_women':[],
        'deaths_women':[],
        'cases_men':[],
        'deaths_men':[]
    }
    for i in range(9):
        c = i
        if i==0: c=''
        ans = '_'+str(c)+'0_'+str(c)+'9_'
        if i==8: ans = '_80_plus_'
        response['cases_women'].append(int(data['confirmados'+ans+'f']))
        response['deaths_women'].append(int(data['obitos'+ans+'f']))
        response['cases_men'].append(int(data['confirmados'+ans+'m']))
        response['deaths_men'].append(int(data['obitos'+ans+'m']))
        
    keys = list(response.keys())   
    for k in keys[1:]:
        response[k]=format.data_for_timeline(response[k])

    return response

def get_incidence_and_transmissibility(REPORT_PATH):
    data = pdf.convert_pdf_to_txt(REPORT_PATH, pages=[2])
    d = format.remove_empty_str(data.splitlines())
    keywords = ['Portugal:', 'Nacional:', 'Continente:']
    obj = {}
    for i,line in enumerate(d):
        if format.remove_space(line.lower()) == 'incidência':
            for word in keywords:
                if d[i+1].find(word) != -1:
                    obj['national_incidence'] = format.convert_string_to_float(format.remove_space(d[i+1].split(word)[1].split('casos')[0]))
                if d[i+2].find(word) != -1:
                    obj['continental_incidence'] = format.convert_string_to_float(format.remove_space(d[i+2].split(word)[1].split('casos')[0]))
        if format.remove_space(line.lower()) == 'r(t)':
            for word in keywords:
                if d[i+1].find(word) != -1:
                    obj['national_r(t)'] = format.convert_string_to_float(format.remove_space(d[i+1].split(word)[1]))
                if d[i+2].find(word) != -1:
                    obj['continental_r(t)'] = format.convert_string_to_float(format.remove_space(d[i+2].split(word)[1]))
    return obj