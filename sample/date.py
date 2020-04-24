import datetime

#formatting current date  
def get_current_date():
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month) if len(str(now.month))==2 else '0'+str(now.month)
    day = str(now.day) if len(str(now.day))==2 else '0'+str(now.day)
    curr_date = day+'-'+ month +'-'+year
    return curr_date

def format_date_summary(date):
    d = date.split('/')
    return d[2]+'-'+d[1]+'-'+d[0]