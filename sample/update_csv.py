import sample.date as date
import sample.website as web
import sample.report as report
import sample.pdf as pdf
import sample.format as format
import pandas as pd
import urllib
import os
import sys

def get_latest_csv_date(filename):
    #create test for this method later (if last line is an empty string, then false)
    data = pd.read_csv(filename)
    last_index = data.tail(1).index.start
    raw_date = data.iloc[last_index].date #DD-MM-YY (with days like january first as 1-1-20)
    d = raw_date.split('-')
    #taking care of formatting issues
    day = d[0] if len(d[0])!=1 else '0'+d[0] #if day is like 4, turn into 04
    month = d[1] if len(d[1])!=1 else '0'+d[1] #if month is 8 (august), turns it to 08
    year = d[2]
    
    return day+'/'+month+'/20'+year#returns DD/MM/YYYY
        
def get_urls_missing_reports(filename): #aka reports whose data are not in the csv file
    latest_date = get_latest_csv_date(filename)
    li_tags = web.get_li_items(filename)
    urls = []
    for i in li_tags:
        if filename == 'portugal_data.csv':
            report_date = i.text[-11:] 
        else:
            report_date = i.text[-11:-1]
        
        if format.remove_space(report_date) == latest_date:#if it's equal to latest date on csv file, get out of loop
            break
        urls.insert(0, {'url': i.a.get('href'), 'date':report_date})
    return urls

def update_situation_reports():#method that updates csv file with data from reports until the most recent one on DGS' website
    report_urls= get_urls_missing_reports('portugal_data.csv')
    n = len(report_urls)
    if n == 0:
        print('The portugal_data.csv file is up to date with all DGS reports')
        print('Most current PDF report was already downloaded, nothing else to do')
    else:
        print('Data from '+str(n)+' DGS situation report(s) need to be parsed into the .csv file')
    #download PDFs and updates csv file
    for i in report_urls:
        # encode to urlencoded to prevent errors from acentos and other portuguese specific characters
        url = format.parse_url(i['url'])

        print('Updating portugal_data.csv file with data from the '+i['date']+' DGS report')
        filepath = 'reports/situation/'+i['date'].replace('/','-')+'.pdf'
        report.download(url, filepath)#downloading report
        old_df = pd.read_csv('portugal_data.csv')
        latest_index = old_df.tail(1).index.start
        old_total_cases = old_df.iloc[latest_index].total_cases
        old_total_deaths = old_df.iloc[latest_index].total_deaths
        old_hospital_icu = old_df.iloc[latest_index].hospital_icu
        old_hospital_stable = old_df.iloc[latest_index].hospital_stable

        summary_data = report.get_summary_data(filepath)
        data_coefficients = report.get_incidence_and_transmissibility(filepath)
        total_cases = int(summary_data['confirmed_cases'])
        total_deaths = int(summary_data['deaths'])
        recovered = int(summary_data['recovered'])
        h = report.get_hospitalized_data(filepath)
        under_surveillance = int(summary_data['under_surveillance'])
        
        new_data = {
            'date': format.date_for_csv(i['date']),
            'total_cases': total_cases,
            'daily_cases': total_cases - old_total_cases,
            'total_deaths': total_deaths,
            'daily_deaths': total_deaths - old_total_deaths,
            'recovered': recovered,
            'hospital_stable': h['hospital_stable'],
            'hospital_icu': h['hospital_icu'],
            'icu_variation': int(h['hospital_icu'])-old_hospital_icu,
            'active_cases': total_cases - total_deaths - recovered,
            'hospital_variation': int(h['hospital_stable'])-old_hospital_stable,
            'under_surveillance': under_surveillance,
            'national_incidence': data_coefficients['national_incidence'],
            'continental_incidence': data_coefficients['continental_incidence'],
            'national_r(t)': data_coefficients['national_r(t)'],
            'continental_r(t)': data_coefficients['continental_r(t)']
        }
        new_df = pd.DataFrame([new_data], columns=list(new_data.keys()))
        updated_df = pd.concat([old_df, new_df]) #concatenate the two dataframes
        updated_df.to_csv('portugal_data.csv', index=False) #save
        print('portugal_data.csv file updated successfully')

def update_vaccine_reports():
    report_urls= get_urls_missing_reports('portugal_vaccine_data.csv')
    n = len(report_urls)
    if n == 0:
        print('The portugal_vaccine_data.csv file is up to date with all DGS vaccine reports')
        print('Most current PDF report was already downloaded, nothing else to do')
    else:
        print('Data from '+str(n)+' DGS vaccine report(s) need to be parsed into the .csv file')
    #download PDFs and updates csv file
    for i in report_urls:
        # encode to urlencoded to prevent errors from acentos and other portuguese specific characters
        url = format.parse_url(i['url'])

        print('Updating portugal_vaccine_data.csv file with data from the '+i['date']+' DGS vaccine report')
        filepath = 'reports/vaccine/'+i['date'].replace('/','-')+'.pdf'
        report.download(url, filepath)#downloading report
        old_df = pd.read_csv('portugal_vaccine_data.csv')
        latest_index = old_df.tail(1).index.start

        vaccine_data = report.get_vaccine_data(filepath)
        vaccination_age_group = vaccine_data['vaccination_age_group']
        new_data = {
            'date': format.date_for_csv(i['date']),
            'vaccinated_one_dose': vaccine_data['vaccinated_one_dose'],
            'completely_vaccinated': vaccine_data['completely_vaccinated'],
            'received_doses': vaccine_data['received_doses'],
            'distributed_doses': vaccine_data['distributed_doses']
        }
        age_groups = ['0_17','18_24','25_49','50_64','65_79','greater_than_80']
        for age in age_groups:
            new_data['one_dose_'+age] = vaccine_data['vaccination_age_group'][age]['one_dose']
            new_data['completed_'+age] = vaccine_data['vaccination_age_group'][age]['completed']

        new_df = pd.DataFrame([new_data], columns=list(new_data.keys()))
        updated_df = pd.concat([old_df, new_df]) #concatenate the two dataframes
        updated_df.to_csv('portugal_vaccine_data.csv', index=False) #save
        print('portugal_vaccine_data.csv file updated successfully')