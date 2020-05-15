
def add_commas(number: str):
    n = len(number)
    pos = []
    ans = ''
    i=1
    while n-i*3>0:
        pos.append(n-i*3-1)
        i+=1
    for j in range(n):
        ans+=str(number[j])
        if j in pos:
            ans+=','
    return ans

def date_symptom(date):
    d = date.split('/')
    return d[2]+'-'+d[1]+'-'+d[0]

def date_for_csv(date): #DD/MM/YYYY
    d = date.split('/')
    return d[0]+'-'+d[1]+'-'+d[2][2:] #DD-MM-YY

def date_timeline_daily_stats(date): #DD-MM-YY
    months = {
        '01':'Jan',
        '02':'Feb',
        '03':'Mar',
        '04':'Apr',
        '05':'May',
        '06':'Jun',
        '07':'Jul',
        '08':'Aug',
        '09':'Sep',
        '10':'Oct',
        '11':'Nov',
        '12':'Dec'
    }
    d = date.split('-')
    day = d[0][1] if d[0][0]=='0' else d[0] #getting only the day number (remove preceding zero)
    return day+' '+months[d[1]] #15 May

def date_timeline(date): #DD-MM-YY
    d = date.split('-')
    return '20'+d[2]+'/'+d[1]+'/'+d[0] #YYYY/MM/YY

def data_for_timeline(data):
    res = ''
    n = len(data)
    for i in range(0, n):
        res+=str(data[i])
        if i!=n-1:
            res+=', ' 
        if (i+1)%10==0:
            res+='\n'
    return res

def remove_chars(number):
    res = ''
    for i in number:
        if i>='0' and i<='9':
            res+=i
    return res