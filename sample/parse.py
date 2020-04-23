import os
import pdf
#right now I have to create and delete .txt files to take advantage of the readline() function. I have to improve that later
def get_data_age_sex(filename, start, end):
    f = open(filename, 'r')
    male=[]
    female=[]
    cases_age = []
    on = False
    while True:
        line = f.readline()
        if on and line !='\n':
            cases_age.append(line)
        if line == start:
            on = True
        if line==end:
            break
    f.close()
    for i in range(9):
        male.append(cases_age[i].split("\n")[0])
        female.append(cases_age[i+10].split("\n")[0])
    return {'male': male, 'female': female}
    
def get_data_by_age_and_sex(option):
    if option == 'cases':
        page_cases = pdf.convert_pdf_to_txt('../var/most_recent_dgs_report.pdf', pages=[1])
        filename = 'page_cases.txt'
        f = open(filename, 'w+')
        f.write(page_cases)
        f.close()
        
        start = 'Total\n'
        end = 'Dados até dia 22 | ABRIL | 2020 | 24:00\n'
    elif option == 'deaths':
        page_deaths = pdf.convert_pdf_to_txt('../var/most_recent_dgs_report.pdf', pages=[3])
        filename = '../var/page_deaths.txt'
        f = open(filename, 'w+')
        f.write(page_deaths)
        f.close()
        
        start = 'Total\n'
        end = 'Saiba mais em https://covid19.min-saude.pt/\n'
    else:
        raise TypeError('option must be either "cases" or "deaths"')

    male = ''
    female = ''
    data = get_data_age_sex(filename, start, end)
    n = len(data['female'])
    for i in range(n):
        if i == n-1: 
            male+=data['male'][i]
            female+=data['female'][i]
        else:
            male+=str(data['male'][i])+', '
            female+=str(data['female'][i])+', '

    os.remove(filename)#deleting txt file
    return {'male': male, 'female': female}
    

def get_summary_data():
    page_summary = pdf.convert_pdf_to_txt('../var/most_recent_dgs_report.pdf', pages=[0])
    filename = '../var/page_summary.txt'
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
