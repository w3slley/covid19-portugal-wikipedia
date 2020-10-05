import sample.report as report
import sample.date as date
import sample.format as format
import pandas as pd

def graphs_english(summary, hospital):
    print('Generating tables and graphs for the english statistics page')
    
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    #dates for new cases/deaths graphs
    date_daily = [format.date_timeline_daily_stats(i) for i in list(df.date)]
    #dates for scatter plots
    date = [format.date_timeline(i) for i in list(df.date)]
    #objects which stores all data from portugal_data.csv file
    data = {'date':format.data_for_timeline(date), 'date_daily':format.data_for_timeline(date_daily)}
    
    #Formatting data from .csv file and putting into the dictionary 'data'
    for i in columns:
        if i!='date':#because date key was already assigned
            data[i] = format.data_for_timeline(list(df[i]))
    
    f = open('output/PortugalCovid-19-Statistics.txt', 'w+')
    result = ""
    print('Generating Summary table')
    result += summary_table(summary, hospital)
    print('Generating Statistics charts')
    result += total_cases(data)
    result += new_cases(data)
    result += cases_by_age_and_gender_english()
    result += total_cases_log()
    result += total_deaths(data)
    result += total_recoveries(data)
    result += new_deaths(data)
    result += deaths_by_age_and_gender_english()
    result += hospital_admitted(data)
    result += icu_variation(data)
    result += cases_deaths_by_region()
    result += growth()
    result += weekly_cases()
    result += weekly_deaths()
    result += deaths_cases_comparison()
    result += footer()
    f.write(result)
    f.close()

def summary_table(summary, hospital):
    #adding comma formatting to numbers in results array
    for k,v in summary.items(): 
        summary[k] = format.add_commas(v)

    link = report.info_latest()['link']
    date_summary = format.date_symptom(report.info_latest()['report_date'])

    return """{{main|COVID-19 pandemic in Portugal}}
{{Current COVID}}

== Statistics ==
<section begin="Statistics"/>
<div style='width: 400px;margin: 0 auto;'>
{| class="wikitable" 
|+COVID-19 Summary
! colspan="2" |DGS latest COVID-19 report: ["""+link+""" """+report.info_latest()['report_date']+"""]
|-
!Total confirmed cases
|"""+summary['confirmed_cases']+"""
|-
!Active cases
|"""+summary['active']+"""
|-
!Total cases (men)
|"""+summary['cases_men']+"""
|-
!Total cases (women)
|"""+summary['cases_women']+"""
|-
!Total deaths (men)
|"""+summary['deaths_men']+"""
|-
!Total deaths (women)
|"""+summary['deaths_women']+"""
|-
!Under surveillance
|"""+summary['under_surveillance']+"""
|-
!Recovered
|"""+summary['recovered']+"""
|-
!Deaths
|"""+summary['deaths']+"""
|-
!Currently admitted to hospital
|"""+hospital['hospital_stable']+"""
|-
!Currently admitted to ICU (Intensive Care Unit)
|"""+hospital['hospital_icu']+"""
|-
|}
</div>
"""

def total_cases(data):
    return"""
The following graphs show the evolution of the pandemic starting from 2 March 2020, the day the first cases were confirmed in the country.<ref>{{Cite web|url=https://www.publico.pt/2020/03/02/sociedade/noticia/coronavirus-ha-dois-infectados-portugal-1905823|title=Coronavírus: há dois casos confirmados em Portugal|date=March 2, 2020|website=Público|url-status=live}}</ref>

<div style='display: inline-block; width: 750px; vertical-align: top;'>
=== Total confirmed cases ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
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
</div>

"""

def new_cases(data):
    return"""
=== New cases per day ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
|colors=#F46D43
|showValues= offset:2
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=New cases
|y1= """+data['daily_cases']+"""
|y1Title=New cases per day
|yGrid=
}}

"""


def cases_by_age_and_gender_english():
    return"""<div style='display: inline-block; width: 750px; vertical-align: top; margin-top:50px'>
=== Total confirmed cases by age and gender ===
The following chart present the data from the last published DGS report where information regarding the total number of cases by age and gender was available.<ref name=DGS-2020-08-16>{{citeweb |url=https://covid19.min-saude.pt/wp-content/uploads/2020/08/167_DGS_boletim_20200816.pdf |title= DGS report from August 16th 2020}}</ref>
{{Graph:Chart
|width=750
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Age
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+, Unknown 
|yAxisTitle=No. of cases
|legend=Legend
|y1= 1073, 1199, 3897, 4214, 4028, 3515, 2550, 1761, 1982, 44
|y2= 932, 1357, 4467, 4640, 4904, 4601, 2842, 1972, 4092, 32
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}
</div>

"""

def total_cases_log():
    return"""<noinclude>
=== Total cases on logarithmic scale ===
[[File:CoViD-19 PT.svg|left|Number of cases (blue) and number of deaths (red) on a [[logarithmic scale]].]]
</noinclude>

"""
def total_deaths(data):
    return"""<div style='display: inline-block; width: 750px; vertical-align: top;'>
=== Total confirmed deaths ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
|colors={{Medical cases chart/Bar colors|1}}
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=No. of confirmed deaths
|y= """+data['total_deaths']+"""
|yGrid= |xGrid=
}}
</div>

"""

def total_recoveries(data):
    return"""<div style='display: inline-block; width: 750px; vertical-align: top;'>
=== Total confirmed recoveries ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
|colors={{Medical cases chart/Bar colors|2}}
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=No. of confirmed recoveries
|y= """+data['recovered']+"""
|yGrid= |xGrid=
}}
</div>

"""

def new_deaths(data):
    return"""<div style='display: inline-block; width: 750px; vertical-align: top;'>
=== New deaths per day ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
|colors={{Medical cases chart/Bar colors|1}}
|showValues=offset:2
|xAxisTitle=Date
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=New deaths
|y1=  """+data['daily_deaths']+"""
|y1Title=New deaths per day
|yGrid=
}}
</div>

"""

def deaths_by_age_and_gender_english():
    return"""<div style='display: inline-block; width: 750px; vertical-align: top; margin-top:50px'>
=== Total confirmed deaths by age and gender ===
The following chart present the data from the last published DGS report where information regarding the total number of deaths by age and gender was available.<ref name=DGS-2020-08-16/>
{{Graph:Chart
|width=750
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Age
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=No. of deaths
|legend=Legend
|y1= 0, 0, 1, 1, 11, 40, 110, 212, 520, 895
|y2= 0, 0, 1, 3, 10, 17, 49, 135, 668, 883
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}
</div>

"""

def hospital_admitted(data):
    return"""=== Hospital admitted cases ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
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
<section end="Statistics"/>

"""

def icu_variation(data):
    return"""=== ICU Variation ===
{{Graph:Chart
|type=line
|linewidth=1.5
|showSymbols=1
|width=750
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
|yGrid=
}}
"""

def growth(): #right now this is only the static version. I need to implement this using data from the csv file
    return """
=== Growth of cases by Municipalities  ===

The following graph presents the total number of COVID-19 cases per day for the municipalities of Portugal with more than 1000 confirmed cases (updated on 30 May), according to the Data Science for Social Good Portugal.<ref>{{cite web |url=https://github.com/dssg-pt/covid19pt-data |website=DSSG Portugal |title=Dados relativos à pandemia COVID-19 em Portugal |access-date=16 May 2020}}</ref>

[[File:Total deaths per region.png|thumb|left|800px|The total number of COVID-19 cases per municipality for those municipalities with more than 1000 confirmed cases. The legend shows which municipality corresponds to which coloured line in the graph and the vertical black line denotes the 4th of May 2020 as the end of the quarantine state.]]
{{clear}}

"""

def weekly_cases():
    return """
<div style="max-width: 750px; overflow-x: scroll;">
=== New cases per week ===
{{Graph:Chart
|type=rect
|width=750
|colors=#F46D43
|xAxisAngle=-60
|showValues= offset:2
|xAxisTitle=Week
|x= 2 Mar - 8 Mar, 9 Mar - 15 Mar, 16 Mar - 22 Mar, 23 Mar - 29 Mar, 30 Mar -5 Apr, 
6 Apr - 12 Apr, 13 Apr - 19 Apr, 20 Apr - 26 Apr, 27 Apr - 3 May, 4 May - 10 May, 
11 May - 17 May, 18 May - 24 May, 25 May - 31 May, 1 Jun - 7 Jun, 8 Jun - 14 Jun, 
15 Jun - 21 Jun, 22 Jun - 28 Jun, 29 Jun - 5 Jul, 6 Jul - 12 Jul, 13 Jul - 19 Jul, 
20 Jul - 26 Jul, 27 Jul - 2 Aug, 3 Aug - 9 Aug, 10 Aug - 16 Aug (5 days)
|yAxisTitle=New cases
|y1=  30 <!--2, 2, 2, 3, 4, 8, 9-->, 215 <!--9, 2, 18, 19, 34, 57, 76-->, 
1355 <!--86, 117, 194, 143, 235, 260, 320-->, 4362 <!--460, 302, 633, 549, 724, 902, 792-->, 
5316 <!--446, 1035, 808, 783, 852, 638, 754-->, 5307 <!--452, 712, 699, 815, 1516, 515, 598-->, 
3621 <!--349, 514, 643, 750, 181, 663, 521-->, 3467 <!--657, 516, 603, 371, 444, 474, 412-->,
1609 <!--163, 295, 183, 368, 295, 203, 92-->, 2299 <!--242, 178, 480, 533, 553, 138, 175-->, 
1455 <!--98, 234, 219, 187, 264, 227, 226-->, 1587 <!--173, 223, 228, 252, 288, 271, 152-->, 
1877 <!--165, 219, 285, 304, 350, 257, 297-->, 2193 <!--200, 195, 366, 331, 377, 382, 342-->, 
1997 <!--192, 421, 294, 310, 270, 283, 227-->, 2443 <!--346, 300, 336, 417, 375, 377, 292-->, 
2513 <!--259, 345, 367, 311, 451, 323, 457-->, 2251 <!--266, 229, 313, 328, 374, 413, 328-->,
2615 <!--232, 287, 443, 418, 602, 342, 291-->, 2124 <!--306, 233, 375, 339, 312, 313, 246-->, 
1528 <!--135, 127, 252, 229, 313, 263, 209-->, 1299 <!--135, 111, 203, 255, 204, 238, 153-->, 
1205 <!--106, 112, 167, 213, 290, 186, 131-->, 1115 <!--157, 120, 278, 325, 235-->
|y1Title=New cases per week
|yGrid=
}}
</div>"""

def weekly_deaths():
    return """
<div style="max-width: 750px; overflow-x: scroll;>
=== New deaths per week ===
{{Graph:Chart
|type=rect
|width=750
|colors={{Medical cases chart/Bar colors|1}}
|xAxisAngle=-60
|showValues= offset:2
|xAxisTitle=Week
|x= 2 Mar - 8 Mar, 9 Mar - 15 Mar, 16 Mar - 22 Mar, 23 Mar - 29 Mar, 30 Mar -5 Apr, 
6 Apr - 12 Apr, 13 Apr - 19 Apr, 20 Apr - 26 Apr, 27 Apr - 3 May, 4 May - 10 May, 
11 May - 17 May, 18 May - 24 May, 25 May - 31 May, 1 Jun - 7 Jun, 8 Jun - 14 Jun, 
15 Jun - 21 Jun, 22 Jun - 28 Jun, 29 Jun - 5 Jul, 6 Jul - 12 Jul, 13 Jul - 19 Jul, 
20 Jul - 26 Jul, 27 Jul - 2 Aug, 3 Aug - 9 Aug, 10 Aug - 16 Aug (5 days)
|yAxisTitle=New deaths
|y1=  0 <!--0, 0, 0, 0, 0, 0, 0-->, 0 <!--0, 0, 0, 0, 0, 0, 0-->, 
14 <!--1, 0, 1, 2, 2, 6, 2-->, 105 <!--9, 10, 10, 17, 16, 24, 19-->, 
176 <!--21, 20, 27, 22, 37, 20, 29-->, 209 <!--16, 34, 35, 29, 26, 35, 34-->, 
210 <!--31, 32, 32, 30, 28, 30, 27-->, 189 <!--21, 27, 23, 35, 34, 26, 23-->,
140 <!--25, 20, 25, 16, 18, 16, 20-->, 92 <!--20, 11, 15, 16, 9, 12, 9-->, 
83 <!--9, 19, 12, 9, 6, 13, 15-->, 98 <!--13, 16, 16, 14, 12, 13, 14-->, 
94 <!--14, 12, 14, 13, 14, 13, 14-->, 69 <!--14, 12, 11, 8, 10, 9, 5-->, 
38 <!--6, 7, 5, 7, 1, 7, 5-->, 13 <!--3, 2, 1, 1, 3, 1, 2-->, 
34 <!--4, 6, 3, 6, 6, 6, 3-->, 50 <!--4, 8, 3, 8, 11, 7, 9-->,
47 <!--6, 9, 3, 13, 2, 8, 6-->, 29 <!--2, 6, 8, 3, 3, 2, 5-->, 
28 <!--2, 6, 5, 3, 7, 4, 1-->, 21 <!--2, 3, 3, 2, 8, 2, 1-->, 
18 <!--0, 1, 1, 3, 3, 4, 6-->, 16 <!--3, 2, 3, 6, 2-->
|y1Title=New deaths per week
|yGrid=
}}
</div>    
"""

def cases_deaths_by_region():
    return """
=== Confirmed cases and deaths, by region===
{{COVID-19_pandemic_data/Portugal_medical_cases}}

The following graph shows the daily cases of COVID-19 for each region of Portugal (updated on the 10th of June) according to DGS<ref>https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/</ref> visualising the table above.
[[File:Daily cases per region update 2.png|left|800px|thumb|Daily cases of COVID-19 per region in Portugal. The lines are smoothed for better visualisation and are coloured according to each region of Portugal. The negative values are not shown here for better visualisation.]]
{{clear}}


Similarly, the following graph presents the daily deaths by COVID-19 for each region of Portugal (updated on the 10th of June) according to DGS.<ref>https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/</ref>
[[File:Daily deaths per region 2.png|left|800px|thumb|Daily deaths from COVID-19 per region in Portugal. The lines are smoothed for better visualisation and are coloured according to each region of Portugal. The negative values are not shown here for better visualisation.]]
{{clear}}
"""

def deaths_cases_comparison():
    return"""=== 2009-20 deaths cases comparison ===

According to the Portuguese mortality surveillance (EVM<ref>{{cite web|url=https://evm.min-saude.pt |title=SICO - eVM {{!}} Mortalidade em tempo real |publisher=Evm.min-saude.pt |date= |accessdate=2020-05-08}}</ref>), the following chart presents the total number of deaths per day in Portugal for the years 2009-2020 (updated on 10 June).
[[File:Deaths_2009_2020.png|thumb|left|720px|The total number of deaths per day in Portugal for various years including all ages.<ref>{{Cite web|url=https://evm.min-saude.pt/#shiny-tab-a_total|title=SICO - eVM {{!}} Mortalidade geral |publisher=Evm.min-saude.pt}}</ref>]]
{{clear}}

In the following two graphs, the total deaths per day and by age group are presented for the years 2019 and 2020.<ref>{{Cite web|url=https://evm.min-saude.pt/#shiny-tab-a_idade|title=SICO - eVM {{!}} Mortalidade por grupo etário |publisher=Evm.min-saude.pt}}</ref>
<div style='display: inline-block; width: 750px; vertical-align: top;'>
[[File:Deaths_per_age_group_2019.png|thumb|left|720px|Total number of deaths per day for Portugal per age group for the year 2019.]]
</div>
<div style='display: inline-block; width: 750px; vertical-align: top;'>
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
def age_and_gender_graphs_portuguese():
    print('Generating cases by age and gender graphs in portuguese')
    result="""=== Casos por idade e género ===
Os gráficos a seguir refletem dados do último relatório da DGS em que tais informações estavam disponíveis (16 de agosto de 2020).<ref>{{citeweb |url=https://covid19.min-saude.pt/wp-content/uploads/2020/08/167_DGS_boletim_20200816.pdf |title= Relatório da DGS do dia 16 de agosto de 2020}}</ref>  

{{Gráfico
|width=450
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Idade
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+, Desconhecido
|yAxisTitle=Número de casos
|legend=Legenda
|y1= 1073, 1199, 3897, 4214, 4028, 3515, 2550, 1761, 1982, 44
|y2= 932, 1357, 4467, 4640, 4904, 4601, 2842, 1972, 4092, 32
|y1Title=Men
|y1Title=Homens
|y2Title=Mulheres
|yGrid= |xGrid=
}}
<br>
{{Gráfico
|width=450
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Idade
|xAxisAngle=-50
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=Número de mortes
|legend=Legenda
|y1= 0, 0, 1, 1, 11, 40, 110, 212, 520, 895
|y2= 0, 0, 1, 3, 10, 17, 49, 135, 668, 883
|y1Title=Homens
|y2Title=Mulheres
|yGrid= |xGrid=
}}
<br>
"""
    with open('output/portuguese/GraphsCasesByAgeAndGender.txt', 'w+') as f:
        f.write(result)


def timeline_graphs_portuguese():
    print('Generating portuguese timeline graphs')
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    date = [format.date_timeline(i) for i in list(df.date)]
    data = {}
    for i in columns:
        if i=='date':
            data[i] = format.data_for_timeline(date)
        else:
            data[i] = format.data_for_timeline(list(df[i]))

    result = """=== Gráficos da evolução dos casos ===
<div style="float:left;margin-right:12px;">{{Dados da pandemia de COVID-19/Gráfico de casos médicos em Portugal}}
</div>[[Imagem:CoViD-19 PT.svg|left|thumb|500px|Evolução diária do número de casos (a azul {{caixa cor|#004586}}) e de óbitos — totais acumulado (a vermelho {{caixa cor|#FF420E}}) e dos últimos 10 dias (a tracejado preto e branco <span style="font-size:175%;">◨</span>) —, em escala logarítmica.]]<div style="clear:left;" />

<!-- Total casos confirmados -->
{{Gráfico
|type=line
|linewidth=2
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

<!-- Mortes  -->
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=#262626
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['total_deaths']+""" 
|yGrid= |xGrid=
|y1Title=total de mortes confirmadas
}}
<small>{{div col|2}}
* {{caixa cor|#262626}} total de mortes confirmadas
{{div col fim}}</small><br />

<!-- Recuperações -->

{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=#87CEEB
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['recovered']+"""
|yGrid= |xGrid=
|y1Title=total de recuperações confirmadas
}}
<small>{{div col|2}}
* {{caixa cor|#87CEEB}} total de recuperações confirmadas
{{div col fim}}</small><br />

<!-- Ativos  -->
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=#22BB66
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisFormat=%b %e
|x= """+data['date']+"""
|yAxisTitle=Nº de casos ativos
|y1= """+data['active_cases']+"""
|yGrid= |xGrid=
|y1Title=total de casos ativos
}}
<small>{{div col|2}}
* {{caixa cor|#22BB66}} total de casos ativos (#''confirmados'' − #''óbitos'' − #''recuperados'')<ref name="dgs" />
{{div col fim}}</small><br />

<!-- Internados -->
{{Gráfico
|type=line
|linewidth=2
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
|linewidth=2
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
|linewidth=2
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
