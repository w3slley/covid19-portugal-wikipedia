
def add_commas(digit_str: str):
    number = get_digits(digit_str)
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
    return ans if int(digit_str) >= 0 else '-'+ans

def date_symptom(date):
    d = date.split('/')
    return d[2]+'-'+d[1]+'-'+d[0]

def date_for_csv(date): #DD/MM/YYYY
    d = date.split('/')
    return d[0]+'-'+d[1]+'-'+d[2][2:] #DD-MM-YY

def date_display_english(date): #DD-MM-YY
    months = {
        '01':'January',
        '02':'February',
        '03':'March',
        '04':'April',
        '05':'May',
        '06':'June',
        '07':'July',
        '08':'August',
        '09':'September',
        '10':'October',
        '11':'November',
        '12':'December'
    }
    d = date.split('-')
    day = d[0][1] if d[0][0]=='0' else d[0] #getting only the day number (remove preceding zero)
    return months[d[1]]+' '+day+', '+d[2] #December 22, 2021

def date_display_portuguese(date): #DD-MM-YY
    months = {
        '01':'Janeiro',
        '02':'Fevereiro',
        '03':'Março',
        '04':'Abril',
        '05':'Maio',
        '06':'Junho',
        '07':'Julho',
        '08':'Agosto',
        '09':'Setembro',
        '10':'Outubro',
        '11':'Novembro',
        '12':'Dezembro'
    }
    d = date.split('-')
    day = d[0][1] if d[0][0]=='0' else d[0] #getting only the day number (remove preceding zero)
    return day+' de '+ months[d[1]]+' de '+d[2] #15 de Maio de 2021

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

#Method that checks if a string is a valid number (to check if the data being gathered from the pdf is actual a valid number of a string or something else)
def is_digit(string):
    for i in string:
        if i <'0' or i>'9':
            return False
    return True
    
def get_digits(number):
    res = ''
    for i in number:
        if i>='0' and i<='9':
            res+=i
    return res

def get_operator(string):
    ops = ['+','-','|']
    for i in string:
        if i in ops:
            return i

#Removes space from a string of numbers
def remove_space(str):
    ans = ""
    for i in range(len(str)):
        if(str[i]!=' '): ans+=str[i]
    return ans

#Removes empty string in a list of strings
def remove_empty_str(l):
    res = []
    for i in l:
        if i != '' and i!=' ': res.append(i)
    return res

#Method that checks if all values in a dictionary are valid (which in this case means they are digits) 
def are_values_valid(obj):
    for i in list(obj.values()):
        if i == '' or i==' ' or (not is_digit(i)): #every value has to be a valid digit (non-empty)
            return False 
    return True

def convert_string_to_float(string):
    ans = '';
    for i in string:
        if i == ',':
            ans+='.'
        else:
            ans+=i
    return float(ans)   