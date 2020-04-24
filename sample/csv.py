import date
import website as web

def update_data(): #adds information to csv file - have to find a way to find latest report localy and download all the other reports till the most recent on the DGS website
    return 0

def get_last_date_csv():
    #create test for this method later (if last line is an empty string, then false)
    with open('../portugal_data.csv', 'r') as f:
        lines = f.read().splitlines()
        #pay attention to empty lines at the end of the csv file.
        raw_date = lines[-1].split(',')[0] #DD-MM-YY (with days like january first as 1-1-20)
        d = raw_date.split('-')
        day,month,year = d[0],d[1],d[2]
        #taking care of formatting issues
        if len(day)==1:
            day='0'+day
        if len(month)==1:
            month='0'+month
        return {'formatted': day+'/'+month+'/20'+year, 'csv_like': raw_date}#returns DD-MM-YYYY for formatted
        
def get_urls_missing_reports(): #aka reports whose data are not in the csv file
    latest_date = get_last_date_csv()['formatted']
    li_tags = web.get_li_items()
    urls = []
    for i in li_tags:
        d = i.text.split(' | ')[1] #date of each report
        if d == latest_date:#if it's equal to latest date on csv file, get out of loop
            break
        urls.insert(0, {'url': i.a.get('href'), 'date':d})
    return urls

def update():#method that updates reports until the most recent one on DGS' website
    report_urls= get_urls_missing_reports()
    #download PDFs and updates csv file
    for i in urls:
        urllib.request.urlretrieve(i.url,'var/DGS_report'+i.date+'.pdf')

    
    

REPORT_PATH = 'var/DGS_report'+date.get_current_date()+'.pdf'

print(get_urls_missing_reports())