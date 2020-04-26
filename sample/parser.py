import sample.report as report
import sample.date as date
import sample.format as format
import pandas as pd


def summary_table(summary, symptoms):
    print('Generating Summary table...')

    #adding comma formatting to numbers in results array
    for k,v in summary.items(): 
        summary[k] = format.add_commas(v)

    link = report.info()['link']
    date_summary = format.date_symptom(report.info()['report_date'])
 
    
    f = open('output/english/SummaryTable.txt', 'w+')
    result="""== Summary ==
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
|}\n"""

    #Symptoms occurrence table

    percentages = symptoms['percentages']
    occurrence = symptoms['occurrence']#whatch out for {{}} problems while using string literals in python
    result += """
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
    
    f.write(result)
    f.close()


def age_and_gender_graphs_english(cases, deaths):
    print('Generating cases by age and gender graphs in english...')

    result = """=== Cases by age and gender ===
{{Graph:Chart
|width=320
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
<br>
{{Graph:Chart
|width=320
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
}}"""
    with open('output/english/GraphsCasesByAgeAndGender.txt', 'w+') as f:
        f.write(result)

def timeline_graphs_english():
    print('Generating english timeline graphs...')
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    date = [format.date_timeline(i, 'english') for i in list(df.date)]
    data = {}
    for i in columns:
        if i=='date':
            data[i] = format.data_for_timeline(date)
        else:
            data[i] = format.data_for_timeline(list(df[i]))

    result = """=== Timeline graphs ===
<!-- Cumulative Cases per day -->
{{Graph:Chart
|type=line
|linewidth=1
|showSymbols=1
|width=700
|colors=#F46D43,#A50026,#C4ADA0,#C4ADB0,#C4ADC0
|showValues=
|xAxisTitle=Date
|xAxisAngle=-40
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|legend=Legend
|y1= """+data['total_cases']+"""
|y1Title=Total confirmed cases
|yGrid= |xGrid=
}}

<!-- Cases per day -->

{{Graph:Chart
|width=700
|colors=#F46D43
|showValues=
|xAxisTitle=Date
|xAxisAngle=-40
|type=rect
|x= """+data['date']+"""
|yAxisTitle=New cases
|legend=Legend
|y1= """+data['daily_cases']+"""
|y1Title=New cases per day
|yGrid= |xGrid=
}}
<br />

<!-- Cumulative Deaths and Recoveries per day -->

{{Graph:Chart
|type=line
|linewidth=1
|showSymbols=1
|width=700
|colors=#A50026,SkyBlue,#FF0000
|showValues=
|xAxisTitle=Date
|xAxisAngle=-40
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|legend=Legend
|y1Title=Total confirmed deaths
|y1= """+data['total_deaths']+"""
|y2Title=Total confirmed recoveries
|y2= """+data['recovered']+"""
|yGrid= |xGrid=
}}
<br />

<!-- Hospital admitted cases -->

{{Graph:Chart
|type=line
|linewidth=1
|showSymbols=1
|width=700
|colors=red, #FF4080
|showValues=
|xAxisTitle=Date
|xAxisAngle=-40
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|legend=Legend
|y1Title=ICU
|y1= """+data['hospital_icu']+"""
|y2Title=Stable
|y2= """+data['hospital_stable']+"""
|yGrid= |xGrid=
}}
<br />

<!-- ICU Variation -->

{{Graph:Chart
|width=700
|colors=#FF0000
|showValues=offset:2
|xAxisTitle=Date
|xAxisAngle=-40
|type=rect
|x= """+data['date']+"""
|yAxisTitle=Cases in ICU variation
|legend=Legend
|y1= """+data['icu_variation']+"""
|y1Title = Cases in ICU variation per day
|yGrid= |xGrid= 
}}

<!-- Deaths per day -->

{{Graph:Chart
|width=700
|colors=black
|showValues=
|xAxisTitle=Date
|xAxisAngle=-40
|type=rect
|x= """+data['date']+"""
|yAxisTitle=New deaths
|legend=Legend
|y1=  """+data['daily_deaths']+"""
|y1Title=New deaths per day
|yGrid= |xGrid=
}}
<br />

{{clear}}

"""
    with open('output/english/TimelineGraphs.txt', 'w+') as f:
        f.write(result)
    
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
    date = [format.date_timeline(i, 'portuguese') for i in list(df.date)]
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
|showSymbols=1
|width=700
|colors=#F46D43,#A50026,#C4ADA0,#C4ADB0,#C4ADC0
|showValues= 
|xAxisTitle=Data
|xAxisAngle=-50
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
|linewidth=1
|showSymbols=1
|width=700
|colors=#262626,#87CEEB,#9F0B0B
|showValues=
|xAxisTitle=Data
|xAxisAngle=-40
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
|linewidth=1
|showSymbols=1
|width=700
|colors=#FF0000, #FF4080
|showValues=
|xAxisTitle=Date
|xAxisAngle=-40
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
|width=700
|colors=#F46D43
|showValues=
|xAxisTitle=Data
|xAxisAngle=-40
|type=rect
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
|width=700
|colors=#000000
|showValues=
|xAxisTitle=Data
|xAxisAngle=-40
|type=rect
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