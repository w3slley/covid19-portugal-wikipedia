
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
    day = d[0] if int(d[0])>=10 else d[0][1] #if day is like 04, turn into 4
    month = d[1] if int(d[1])>=10 else d[1][1] #if month is 08, turn into 8
    year = d[2][2:]
    return day+'-'+month+'-'+year

def date_timeline(date):
    months = {
        '1':'Jan',
        '2':'Feb',
        '3':'Mar',
        '4':'Apr',
        '5':'May',
        '6':'Jun',
        '7':'Jul',
        '8':'Aug',
        '9':'Sep',
        '10':'Oct',
        '11':'Nov',
        '12':'Dec'
    }
    d = date.split('-')
    return d[0]+' '+months[d[1]]

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