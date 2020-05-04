import sample.date as date
import sample.website as web
import sample.report as report
import sample.format as format
import pandas as pd
import urllib
import os

def get_latest_csv_date():
    #create test for this method later (if last line is an empty string, then false)
    data = pd.read_csv('portugal_data.csv')
    last_index = data.tail(1).index.start
    raw_date = data.iloc[last_index].date #DD-MM-YY (with days like january first as 1-1-20)
    d = raw_date.split('-')
    #taking care of formatting issues
    day = d[0] if len(d[0])!=1 else '0'+d[0] #if day is like 4, turn into 04
    month = d[1] if len(d[1])!=1 else '0'+d[1] #if month is 8 (august), turn to 08
    year = d[2]
    
    return day+'/'+month+'/20'+year#returns DD-MM-YYYY for formatted
        
def get_urls_missing_reports(): #aka reports whose data are not in the csv file
    latest_date = get_latest_csv_date()
    li_tags = web.get_li_items()
    urls = []
    for i in li_tags:
        d = i.text[-10:] #date of each report
        print(d)
        if d == latest_date:#if it's equal to latest date on csv file, get out of loop
            break
        urls.insert(0, {'url': i.a.get('href'), 'date':d})
    return urls

def update():#method that updates csv file with data from reports until the most recent one on DGS' website
    report_urls= get_urls_missing_reports()
    n = len(report_urls)
    if n == 0:
        print('The portugal_data.csv file is up to date with all DGS reports')
    else:
        print('Data from '+str(n)+' DGS report(s) need to be parsed into the .csv file!')
    #download PDFs and updates csv file
    for i in report_urls:
        # encode to urlencoded to prevent errors from acentos and other portuguese specific characters
        url = urllib.parse.quote(i['url']).replace('%3A', ':') # %3A is : in urlencoded. I had to replace it because for some reason the browser (and urllib) was not recognizing %3A as ":".

        print('Updating portugal_data.csv file with data from the '+i['date']+' DGS report...')
        REPORT_PATH = 'var/DGS_report'+i['date'].replace('/','-')+'.pdf'
        if not os.path.isfile(REPORT_PATH):
            print('Downloading PDF file...')
            urllib.request.urlretrieve(url,REPORT_PATH)#download pdf report
        old_df = pd.read_csv('portugal_data.csv')
        latest_index = old_df.tail(1).index.start
        old_total_cases = old_df.iloc[latest_index].total_cases
        old_total_deaths = old_df.iloc[latest_index].total_deaths
        old_hospital_icu = old_df.iloc[latest_index].hospital_icu

        summary = report.get_summary_data(REPORT_PATH)
        total_cases = int(summary['confirmed_cases'])
        total_deaths = int(summary['deaths'])
        recovered = int(summary['recovered'])
        h = report.get_hospitalized_data(REPORT_PATH)

        new_data = {
            'date': format.date_for_csv(i['date']),
            'total_cases': total_cases,
            'daily_cases': total_cases - old_total_cases,
            'total_deaths': total_deaths,
            'daily_deaths': total_deaths - old_total_deaths,
            'recovered': recovered,
            'hospital_stable': h['hospital_stable'],
            'hospital_icu': h['hospital_icu'],
            'icu_variation': int(h['hospital_icu'])-old_hospital_icu
        }
        new_data_values = list(new_data.values())
        new_df = pd.DataFrame([new_data], columns=list(new_data.keys()))
        updated_df = pd.concat([old_df, new_df]) #concatenate the two dataframes
        updated_df.to_csv('portugal_data.csv', index=False) #save
        print('.csv file updated successfully!')