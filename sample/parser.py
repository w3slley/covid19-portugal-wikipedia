import sample.report as report
import sample.date as date
import sample.format as format
import pandas as pd

def statistics_english(cases,deaths,summary,symptoms):
    print('Generating tables and graphs for the english statistics page...')
    
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    #dates for new cases/deaths graphs
    date_daily = [format.date_timeline_daily_stats(i) for i in list(df.date)]
    #dates for scatter plots
    date = [format.date_timeline(i) for i in list(df.date)]
    #objects which stores all data from portugal_data.csv file
    data = {'date':format.data_for_timeline(date), 'date_daily':format.data_for_timeline(date_daily)}
    for i in columns:
        if i!='date':#because date key was already assigned
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
    result += growth()
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
|width=650
|colors=#F46D43
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
|type=rect
|width=750
|colors=#F46D43
|xAxisAngle=-60
|showValues= offset:2
|xAxisTitle=Date
|x= """+data['date_daily']+"""
|yAxisTitle=New cases
|y1= """+data['daily_cases']+"""
|y1Title=New cases per day
|yGrid=
}}

"""


def cases_by_age_and_gender_english(cases):
    return"""=== Total confirmed cases by age and gender ===
{{Graph:Chart
|width=650
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
|width=650
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
|type=rect
|width=750
|colors={{Medical cases chart/Bar colors|1}}
|showValues=offset:2
|xAxisAngle=-60
|xAxisTitle=Date
|x= """+data['date_daily']+"""
|yAxisTitle=New deaths
|y1=  """+data['daily_deaths']+"""
|y1Title=New deaths per day
|yGrid=
}}

"""

def deaths_by_age_and_gender_english(deaths):
    return"""=== Total confirmed deaths by age and gender ===
{{Graph:Chart
|width=650
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
|width=650
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
|width=650
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

def growth(): #right now this is only the static version. I need to implement this using data from the csv file
    return """
<noinclude>

=== Growth  ===
{{Side box
|position=Left
|metadata=No
|above='''Growth of confirmed cases'''<br/><small>a rising straight line indicates exponential growth, while a horizontal line indicates linear growth</small>
|abovestyle=text-align:center
|below=<small>Source: #insert source#</small>
|text= {{Graph:Chart
    |type=line
    |linewidth=2
    |width=600
    |colors={{Medical cases chart/Bar colors|3}}
    |showValues=
    |xAxisTitle=Total confirmed cases
    |xAxisAngle=-30
    |xScaleType=log
    |x=2, 4, 6, 9, 13, 21, 30, 39, 41, 59, 
78, 112, 169, 245, 331, 448, 642, 785, 1020, 1280, 
1600, 2060, 2362, 2995, 3544, 4268, 5170, 5962, 6408, 7443, 
8251, 9034, 9886, 10524, 11278, 11730, 12442, 13141, 13956, 15472, 
15987, 16585, 16934, 17448, 18091, 18841, 19022, 19685, 20206, 20863, 
21379, 21982, 22353, 22797, 23271, 23683, 23846, 24141, 24324, 24692, 
24987, 25190, 25282, 25524, 25702, 26182, 26715, 27268, 27406, 27581, 
27679, 27913, 28132, 28319
    |yAxisTitle=New confirmed cases
    |yScaleType=log
    |y=2, 2, 2, 3, 4, 8, 9, 9, 2, 18, 
19, 34, 57, 76, 86, 117, 194, 143, 235, 260, 
320, 460, 302, 633, 549, 724, 902, 792, 446, 1035, 
808, 783, 852, 638, 754, 452, 712, 699, 815, 1516, 
515, 598, 349, 514, 643, 750, 181, 663, 521, 657, 
516, 603, 371, 444, 474, 412, 163, 295, 183, 368, 
295, 203, 92, 242, 178, 480, 533, 553, 138, 175, 
98, 234, 219, 187
    |yGrid= |xGrid=
    }}
}}
<br>
{{Side box
|position=Left
|metadata=No
|above='''Growth of confirmed deaths'''<br/><small>a rising straight line indicates exponential growth, while a horizontal line indicates linear growth</small>
|abovestyle=text-align:center
|below=<small>Source: #insert source#</small>
|text= {{Graph:Chart
    |type=line
    |linewidth=2
    |width=600
    |colors={{Medical cases chart/Bar colors|1}}
    |showValues=
    |xAxisTitle=Total confirmed deaths
    |xAxisAngle=-30
    |xScaleType=log
    |x=1, 2, 3, 6, 12, 
14, 23, 33, 43, 60, 76, 100, 119, 140, 160, 
187, 209, 246, 266, 295, 311, 345, 380, 409, 435, 
470, 504, 535, 567, 599, 629, 657, 687, 714, 735, 
762, 785, 820, 854, 880, 903, 928, 948, 973, 989, 
1007, 1023, 1043, 1063, 1074, 1089, 1105, 1114, 1126, 1135, 
1144, 1163, 1175, 1184
    |yAxisTitle=New confirmed deaths
    |yScaleType=log
    |y=1, 1, 2, 2, 6, 
2, 9, 10, 10, 17, 16, 24, 19, 21, 20, 
27, 22, 37, 20, 29, 16, 34, 35, 29, 26, 
35, 34, 31, 32, 32, 30, 28, 30, 27, 21, 
27, 23, 35, 34, 26, 23, 25, 20, 25, 16, 
18, 16, 20, 20, 11, 15, 16, 9, 12, 9, 
9, 19, 12, 9
    |yGrid= |xGrid=
    }}
}}

</noinclude>


The following graph presents the total number of COVID-19 cases per day for the six most affected municipalities of Portugal, according to the Data Science for Social Good Portugal<ref>{{cite web |url=https://github.com/dssg-pt/covid19pt-data |website=DSSG Portugal |title=Dados relativos à pandemia COVID-19 em Portugal |access-date=16 May 2020}}</ref>.
[[File:Total cases per concelho.png|thumb|left|800px|The total number of Covid-19 cases per municipality for the 6 most affected municipalities. The legend shows which municipality corresponds to which coloured line in the graph. The vertical black line denotes the 4th of May 2020 as the end of the quarantine state.]]
{{clear}}

"""

def cases_deaths_by_region():
    return """=== Confirmed cases and deaths, by region===
{{COVID-19_pandemic_data/Portugal_medical_cases}}


The following graph shows the daily cases of Covid-19 for each region of Portugal (updated on 17th of May) according to DGS<ref>https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/</ref> visualising the table above.
[[File:Daily cases per region.png|thumb|left|800px|Daily cases of Covid-19 per region in Portugal. The lines are smoothed for better visualisation and are coloured according to each region of Portugal. The negative values are not shown here for better visualisation.]]
{{clear}}

"""

def deaths_cases_comparison():
    return"""=== 2009-20 deaths cases comparison ===

According to the Portuguese mortality surveillance (EVM<ref>{{cite web|url=https://evm.min-saude.pt |title=SICO - eVM {{!}} Mortalidade em tempo real |publisher=Evm.min-saude.pt |date= |accessdate=2020-05-08}}</ref>), the following chart presents the total number of deaths per day in Portugal for the years 2009-2020 (updated on 14<sup>st</sup> of May).
[[File:Total_number_of_deaths_2009_2020.png|thumb|left|720px|The total number of deaths per day in Portugal for various years including all ages.<ref>{{Cite web|url=https://evm.min-saude.pt/#shiny-tab-a_total|title=SICO - eVM {{!}} Mortalidade geral |publisher=Evm.min-saude.pt}}</ref>]]
{{clear}}

In the following two graphs, the total deaths per day and by age group are presented for the years 2019 and 2020.<ref>{{Cite web|url=https://evm.min-saude.pt/#shiny-tab-a_idade|title=SICO - eVM {{!}} Mortalidade por grupo etário |publisher=Evm.min-saude.pt}}</ref>
<div style='display: inline-block; width: 800px; vertical-align: top;'>
[[File:Deaths_per_age_group_2019.png|thumb|left|720px|Total number of deaths per day for Portugal per age group for the year 2019.]]
</div>
<div style='display: inline-block; width: 800px; vertical-align: top;'>
[[File:Deaths_per_age_group_2020.png|thumb|left|720px|Total number of deaths per day for Portugal per age group for the year 2020.]]
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
