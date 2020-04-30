
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