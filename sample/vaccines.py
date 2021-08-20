import pdf
import sys
import format

def assign_vaccination_data(results,age_range):
    results['vacinacao_faixa_etaria'][age_range]['Pelo menos uma dose'] = a[i+8] + " ("+a[i+14]+")"
    results['vacinacao_faixa_etaria'][age_range]['Vacinação completa'] = a[i+20] + " ("+a[i+26]+")"

filename = sys.argv[1]
txt = pdf.convert_pdf_to_txt(filename)
a=txt.splitlines()
a=format.remove_empty_str(a)
results = {}
results['vacinacao_faixa_etaria'] = {}

list_age = ['0_17','18_24','25_49','50_64','65_79','greater_than_80']
for i in list_age:
    results['vacinacao_faixa_etaria'][i] = {}
for i in range(len(a)):
    if 'pelo menos' in a[i]:
        if a[i+1] == 'vacinação iniciada 1':
            results["vacinacao_uma_dose"] = a[i+2]
        else: 
            results["vacinacao_uma_dose"] = a[i+1]
    if 'vacinação completa' in a[i]:
        results["vacinacao_completa"] = a[i+1]
        break
for i in range(len(a)):
    if 'Doses Recebidas' in a[i]:
        results["doses_recebidas"] = a[i+2]
    if 'Doses Distribu' in a[i]: 
        results["doses_distribuidas"] = a[i+2]  
    if '0 – 17' in a[i]:
        assign_vaccination_data(results,'0_17')    
    if '18 – 24' in a[i]:
        assign_vaccination_data(results,'18_24') 
    if '25 – 49' in a[i]:
        assign_vaccination_data(results,'25_49')
    if '50 – 64' in a[i]:
        assign_vaccination_data(results,'50_64')
    if '65 – 79' in a[i]:
        assign_vaccination_data(results,'65_79')
    if '≥ 80' in a[i]:
        assign_vaccination_data(results,'greater_than_80')
print(results)