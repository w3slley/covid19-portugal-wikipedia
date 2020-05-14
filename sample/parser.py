import sample.report as report
import sample.date as date
import sample.format as format
import pandas as pd

def statistics_english(cases,deaths,summary,symptoms):
    print('Generating tables and graphs for the english statistics page...')
    
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    date = [format.date_timeline(i) for i in list(df.date)]
    data = {}
    for i in columns:
        if i=='date':
            data[i] = format.data_for_timeline(date)
        else:
            data[i] = format.data_for_timeline(list(df[i]))
    
    f = open('output/PortugalCovid-19-Statistics.txt', 'w+')
    result = ""
    print('Generating Summary table...')
    result += summary_table(summary,symptoms)
    print('Generating Statistics charts...')
    result += total_cases(data)
    result += new_cases(data)
    result += cases_by_age_and_gender_english(cases)
    result += total_cases_log()
    result += total_deaths_and_recoveries(data)
    result += new_deaths(data)
    result += deaths_by_age_and_gender_english(deaths)
    result += hospital_admitted(data)
    result += icu_variation(data)
    result += cases_deaths_by_region()
    result += deaths_cases_comparison()
    result += footer()
    f.write(result)
    f.close()

def summary_table(summary, symptoms):
    #adding comma formatting to numbers in results array
    for k,v in summary.items(): 
        summary[k] = format.add_commas(v)

    link = report.info()['link']
    date_summary = format.date_symptom(report.info()['report_date'])

    #Symptoms occurrence table
    percentages = symptoms['percentages']
    occurrence = symptoms['occurrence']#watch out for {{}} problems while using string literals in python
    return """{{main|COVID-19 pandemic in Portugal}}

== Current status ==
{| class="wikitable" 
|+COVID-19
! colspan="2" |Cases ["""+link+""" """+report.info()['report_date']+"""]
|-
!total confirmed cases
|"""+summary['confirmed_cases']+"""
|-
!total not confirmed cases 
|"""+summary['not_confirmed_cases']+"""
|-
!total suspected cases (since 1 January 2020)
|"""+summary['suspected_cases']+"""
|-
!under surveillance
|"""+summary['under_surveillance']+"""
|-
!waiting for results
|"""+summary['waiting_results']+"""
|-
!recovered
|"""+summary['recovered']+"""
|-
!deaths
|"""+summary['deaths']+"""
|-
|}

{| {{Table}} 
!   !! high fever !! dry cough !! difficult breathing !! headache !! muscular pain !! tiredness
|-
! % of cases with symptoms
| """+percentages[0]+"""
| """+percentages[1]+"""
| """+percentages[2]+"""
| """+percentages[3]+"""
| """+percentages[4]+"""
| """+percentages[5]+"""
|-
|}
There was only reported information regarding the occurrence of symptoms on """+occurrence+""" of confirmed cases.<ref>{{cite web|url="""+link+""" |title=COVID-19 RELATÓRIO DE SITUAÇÃO |date="""+date_summary+""" |website=covid19.min-saude.pt}}</ref>"""
    
    
def total_cases(data):
    return"""
== Statistics ==
<section begin="Statistics"/>
The following graphs show the evolution of the pandemic starting from 2 March 2020, the day the first cases were confirmed in the country<ref>{{Cite web|url=https://www.publico.pt/2020/03/02/sociedade/noticia/coronavirus-ha-dois-infectados-portugal-1905823|title=Coronavírus: há dois casos confirmados em Portugal|date=March 2, 2020|website=Público|url-status=live}}</ref>.

<div style='display: inline-block; width: 800px; vertical-align: top;'>
=== Total confirmed cases ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=600
|colors=#F46D43,#A50026,#C4ADA0,#C4ADB0,#C4ADC0
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|y1= """+data['total_cases']+"""
|y1Title=Total confirmed cases
|yGrid= |xGrid=
}}

"""

def new_cases(data):
    return"""=== New cases per day ===
{{Graph:Chart
|type=area
|linewidth=2
|showSymbols=1
|width=600
|colors=#80ff8000
|xType=date
|xAxisFormat=%b %e
|xAxisTitle=Date
|x= """+data['date']+"""
|yAxisTitle=New cases
|y1= """+data['daily_cases']+"""
|y1Title=New cases per day
|yGrid= |xGrid=
}}

"""


def cases_by_age_and_gender_english(cases):
    return"""=== Total confirmed cases by age and gender ===
{{Graph:Chart
|width=600
|colors=blue,orange
|showValues=
|xAxisTitle=Age
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=No. of cases
|legend=Legend
|y1= """+cases['men']+"""
|y2= """+cases['women']+"""
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}
<noinclude>

"""

def total_cases_log():
    return"""=== Total cases on logarithmic scale ===
[[File:CoViD-19 PT.svg|left|Number of cases (blue) and number of deaths (red) on a [[logarithmic scale]].]]
</noinclude>
</div>

"""

def total_deaths_and_recoveries(data):
    return"""<div style='display: inline-block; width: 800px; vertical-align: top;'>
=== Total confirmed deaths, and confirmed recoveries ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=600
|colors={{Medical cases chart/Bar colors|1}},{{Medical cases chart/Bar colors|2}}
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|legend=Legend
|y1Title=Total confirmed deaths
|y1= """+data['total_deaths']+"""
|y2Title=Total confirmed recoveries
|y2= """+data['recovered']+"""
|yGrid= |xGrid=
}}

"""
def new_deaths(data):
    return"""=== New deaths per day ===
{{Graph:Chart
|type=area
|linewidth=2
|showSymbols=
|width=600
|colors=#80001e62
|xAxisAngle=-60
|xType=date
|xAxisFormat=%b %e
|xAxisTitle=Date
|x= """+data['date']+"""
|yAxisTitle=New deaths
|y1=  """+data['daily_deaths']+"""
|y1Title=New deaths per day
|yGrid= |xGrid=
}}

"""

def deaths_by_age_and_gender_english(deaths):
    return"""=== Total confirmed deaths by age and gender ===
{{Graph:Chart
|width=600
|colors=blue,orange
|showValues=
|xAxisTitle=Age
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=No. of deaths
|legend=Legend
|y1="""+deaths['men']+"""
|y2= """+deaths['women']+"""
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}
</div>
<section end="Statistics"/>

"""

def hospital_admitted(data):
    return"""=== Hospital admitted cases ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=600
|colors={{Medical cases chart/Bar colors|4}},{{Medical cases chart/Bar colors|5}}
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|legend=Legend
|y1Title=ICU
|y1= """+data['hospital_icu']+"""
|y2Title=Stable
|y2= """+data['hospital_stable']+"""
|yGrid= |xGrid=
}}

"""

def icu_variation(data):
    return"""=== ICU Variation ===
{{Graph:Chart
|type=line
|linewidth=1.5
|width=600
|colors={{Medical cases chart/Bar colors|4}}
|showValues=offset:2
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Cases in ICU variation
|legend=Legend
|y1= """+data['icu_variation']+"""
|y1Title = Cases in ICU variation per day
|yGrid= |xGrid= 
}}

"""

def cases_deaths_by_region():
    return """=== Confirmed cases and deaths, by region===
{{COVID-19_pandemic_data/Portugal_medical_cases}}

"""

def deaths_cases_comparison():
    return"""=== 2009-20 deaths cases comparison ===

According to the Portuguese mortality surveillance (EVM<ref>{{cite web|url=https://evm.min-saude.pt |title=SICO - eVM {{!}} Mortalidade em tempo real |publisher=Evm.min-saude.pt |date= |accessdate=2020-05-08}}</ref>), the following chart presents the total number of deaths per day in Portugal for the years 2009-2020 (updated on 1<sup>st</sup> of May).
[[File:Total deaths portugal.png|thumb|left|720px|The total number of deaths per day in Portugal for various years including all ages.<ref>{{Cite web|url=https://evm.min-saude.pt/#shiny-tab-a_total|title=SICO - eVM {{!}} Mortalidade geral |publisher=Evm.min-saude.pt}}</ref>]]
{{clear}}

In the following two graphs, the total deaths per day and by age group are presented for the years 2019 and 2020.<ref>{{Cite web|url=https://evm.min-saude.pt/#shiny-tab-a_idade|title=SICO - eVM {{!}} Mortalidade por grupo etário |publisher=Evm.min-saude.pt}}</ref>
<div style='display: inline-block; width: 800px; vertical-align: top;'>
[[File:Total deaths portugal age 2019.png|thumb|left|720px|Total number of deaths per day for Portugal per age group for the year 2019.]]
</div>
<div style='display: inline-block; width: 800px; vertical-align: top;'>
[[File:Total deaths portugal age 2020.png|thumb|left|720px|Total number of deaths per day for Portugal per age group for the year 2020.]]
</div>
{{clear}}

"""

def footer():
    return"""== References ==
{{reflist|colwidth=30em}}

{{2019-nCoV|state=expanded}}
[[Category:COVID-19 pandemic in Portugal|statistics]]"""

#portuguese graphs
def age_and_gender_graphs_portuguese(cases, deaths):
    print('Generating cases by age and gender graphs in portuguese...')
    result="""=== Casos por idade e sexo ===
{{Gráfico
|width=450
|colors=blue,orange
|showValues=
|xAxisTitle=Idade
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=Número de casos
|legend=Legenda
|y1= """+cases['men']+"""
|y2= """+cases['women']+"""
|y1Title=Men
|y1Title=Homens
|y2Title=Mulheres
|yGrid= |xGrid=
}}
<br>
{{Gráfico
|width=450
|colors=blue,orange
|showValues=
|xAxisTitle=Idade
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=Número de mortes
|legend=Legenda
|y1= """+deaths['men']+"""
|y2= """+deaths['women']+"""
|y1Title=Homens
|y2Title=Mulheres
|yGrid= |xGrid=
}}
<br>
"""
    with open('output/portuguese/GraphsCasesByAgeAndGender.txt', 'w+') as f:
        f.write(result)


def timeline_graphs_portuguese():
    print('Generating portuguese timeline graphs...')
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    date = [format.date_timeline(i) for i in list(df.date)]
    data = {}
    for i in columns:
        if i=='date':
            data[i] = format.data_for_timeline(date)
        else:
            data[i] = format.data_for_timeline(list(df[i]))

    result = """
=== Gráficos da evolução dos casos ===
<!-- Total casos confirmados -->
{{Gráfico
|type=line
|linewidth=1
|showSymbols=1.5
|width=700
|colors=#F46D43,#A50026,#C4ADA0,#C4ADB0,#C4ADC0
|showValues= 
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['total_cases']+"""
|y1Title=casos totais confirmados
|yGrid= |xGrid=
}}<small>
* {{caixa cor|#F46D43}} casos totais confirmados</small>

<!-- Mortes e recuperações -->
{{Gráfico
|type=line
|linewidth=1.5
|showSymbols=1
|width=700
|colors=#262626,#87CEEB,#9F0B0B
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['total_deaths']+""" 
|y2= """+data['recovered']+"""
|yGrid= |xGrid=
|y1Title=total de mortes confirmadas
|y2Title=total de recuperações confirmadas
}}
<small>{{div col|2}}
* {{caixa cor|#262626}} total de mortes confirmadas
* {{caixa cor|#87CEEB}} total de recuperações confirmadas
{{div col fim}}</small><br />

<!-- Internados -->
{{Gráfico
|type=line
|linewidth=1.5
|showSymbols=1
|width=700
|colors=#FF0000, #FF4080
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1Title=UCI
|y1= """+data['hospital_icu']+"""
|y2Title=Internados
|y2= """+data['hospital_stable']+"""
|yGrid= 
|xGrid=
}}
<small>{{div col|2}}
* {{caixa cor|#FF0000}} total de casos internados em UCI (Unidade de Cuidados Intensivos)
* {{caixa cor|#FF4080}} total de casos internados
{{div col fim}}</small>

<!-- Novos casos por dia -->
{{Gráfico
|type=line
|linewidth=1.5
|showSymbols=1
|width=700
|colors=#F46D43
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Novos casos
|y1= """+data['daily_cases']+"""
|y1Title=total de novos casos confirmados por dia
|yGrid= 
|xGrid=
}}<small>
* {{caixa cor|#F46D43}} total de novos casos confirmados por dia</small>

<!-- Mortes por dia -->
{{Gráfico
|type=line
|linewidth=1.5
|showSymbols=1
|width=700
|colors=#000000
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Novas mortes
|y1= """+data['daily_deaths']+"""
|y1Title=total de mortes confirmadas por dia
|yGrid= |xGrid=
}}<small>
* {{caixa cor|#000000}} total de mortes confirmadas por dia</small>
"""
    with open('output/portuguese/TimelineGraphs.txt', 'w+') as f:
        f.write(result)
