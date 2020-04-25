import datetime

#formatting current date  
def get_current_date():
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month) if len(str(now.month))==2 else '0'+str(now.month)
    day = str(now.day) if len(str(now.day))==2 else '0'+str(now.day)
    curr_date = day+'-'+ month +'-'+year
    return curr_date

def format_date_path(date):
    return date.replace('/','-')
    
def format_date_symptom(date):
    d = date.split('/')
    return d[2]+'-'+d[1]+'-'+d[0]

def format_date_for_csv(date): #DD/MM/YYYY
    d = date.split('/')
    day = d[0] if int(d[0])>=10 else d[0][1] #if day is like 04, turn into 4
    month = d[1] if int(d[1])>=10 else d[1][1] #if month is 08, turn into 8
    year = d[2][2:]
    return day+'-'+month+'-'+year