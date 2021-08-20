import sample.report as report
import sample.date as date
import sample.format as format
import pandas as pd

def graphs_english():
    print('Generating tables and graphs for the english statistics page')
    
    df = pd.read_csv('portugal_data.csv')
    columns = list(df.columns)
    #dates for scatter plots
    date = [format.date_timeline(i) for i in list(df.date)]
    #objects which stores all data from portugal_data.csv file
    data = {'date':format.data_for_timeline(date)}
    
    #Formatting data from .csv file and putting into the dictionary 'data'
    for i in columns:
        if i!='date':#because date key was already assigned
            data[i] = format.data_for_timeline(list(df[i]))
    
    #getting data regarding cases/deaths by age and gender from DSSG/Vost
    age_gender = report.get_recent_data_age_gender()

    f = open('output/PortugalCovid-19-Statistics.txt', 'w+')
    result = ""
    print('Generating Summary table')
    result += summary_table()
    print('Generating Statistics charts')
    result += total_cases(data)
    result += new_cases(data)
    result += cases_by_age_and_gender_english(age_gender)
    result += total_deaths(data)
    result += new_deaths(data)
    result += deaths_by_age_and_gender_english(age_gender)
    result += hospital_admitted(data)
    result += icu_admitted(data)
    result += cases_deaths_by_region()
    result += growth()
    result += weekly_cases()
    result += weekly_deaths()
    result += deaths_cases_comparison()
    result += footer()
    f.write(result)
    f.close()

def get_last_datapoint_situation(column_name):
    df = pd.read_csv('portugal_data.csv')
    data = list(df[column_name])
    if column_name.find('national') != -1 or column_name.find('continental') != -1:
        return str(data[-1])
    else:
        #Obtaining data variation by subtracting value from most recent day to the day before that
        int_variation = data[-1] - data[-2]
        #Constructing variation string
        formatted_variation = format.add_commas(str(int_variation))
        variation = '+'+formatted_variation if int_variation >= 0 else formatted_variation

        return format.add_commas(str(data[-1])) + " (" + variation + ")"

def get_last_datapoint_vaccine(column_name):
    df = pd.read_csv('portugal_vaccine_data.csv')
    data = list(df[column_name])
    return str(data[-1])
    

def summary_table():

    link = report.info_latest()['link']
    report_date = report.info_latest()['report_date']
    return """{{main|COVID-19 pandemic in Portugal}}
== Statistics ==
<section begin="Statistics"/>
<div style='display:flex;justify-content:center'>
<div style="margin-right:10px">
{| class="wikitable" 
|+COVID-19 Summary (["""+link+""" """+report_date+"""])
!Total confirmed cases
|"""+get_last_datapoint_situation('total_cases')+"""
|-
!Total confirmed deaths
|"""+get_last_datapoint_situation('total_deaths')+"""
|-
!Active cases
|"""+get_last_datapoint_situation('active_cases')+"""
|-
!Under surveillance
|"""+get_last_datapoint_situation('under_surveillance')+"""
|-
!Recovered
|"""+get_last_datapoint_situation('recovered')+"""
|-
!Currently admitted to hospital
|"""+get_last_datapoint_situation('hospital_stable')+"""
|-
!Currently admitted to ICU
|"""+get_last_datapoint_situation('hospital_icu')+"""
|-
!Cases per 100 000 (national/continental)
|"""+get_last_datapoint_situation('national_incidence')+""" / """+get_last_datapoint_situation('continental_incidence')+"""
|-
!R(t) (national/continental)
|"""+get_last_datapoint_situation('national_r(t)')+""" / """+get_last_datapoint_situation('continental_r(t)')+"""
|}
</div>

<div style="display:flex;flex-direction:column;margin-left:10px">
<div style='display:flex;justify-content:center'>
{| class="wikitable"
|+ Vaccine summary ([https://covid19.min-saude.pt/wp-content/uploads/2021/08/Relato%CC%81rio-de-Vacinac%CC%A7a%CC%83o-n.o-27.pdf 15/08/2021])
! People with at least one vaccine dose
| """+get_last_datapoint_vaccine('vaccinated_one_dose')+"""
|-
! People completely vaccinated
| """+get_last_datapoint_vaccine('completely_vaccinated')+"""
|-
! Doses received
| """+get_last_datapoint_vaccine('received_doses')+"""
|-
! Doses distributed
| """+get_last_datapoint_vaccine('distributed_doses')+"""
|-
|}
</div>

<div style='display:flex;justify-content:center;margin-left:15px'>
{| class="wikitable"
|+ Vaccination by age group
! scope="col" | 
! scope="col" | At least one vaccine dose
! scope="col" | Complete vaccination
|-
! scope="row" | 0 - 17
| """+get_last_datapoint_vaccine('one_dose_0_17')+"""
| """+get_last_datapoint_vaccine('completed_0_17')+"""
|-
! scope="row" | 18 - 24
| """+get_last_datapoint_vaccine('one_dose_18_24')+"""
| """+get_last_datapoint_vaccine('completed_18_24')+"""
|-
! scope="row" | 25 - 49
| """+get_last_datapoint_vaccine('one_dose_25_49')+"""
| """+get_last_datapoint_vaccine('completed_25_49')+"""
|-
! scope="row" | 50 - 64
| """+get_last_datapoint_vaccine('one_dose_50_64')+"""
| """+get_last_datapoint_vaccine('completed_50_64')+"""
|-
! scope="row" | 65 - 79
| """+get_last_datapoint_vaccine('one_dose_65_79')+"""
| """+get_last_datapoint_vaccine('completed_65_79')+"""
|-
! scope="row" | ⩾80
| """+get_last_datapoint_vaccine('one_dose_greater_than_80')+"""
| """+get_last_datapoint_vaccine('completed_greater_than_80')+"""
|-
|}
</div>
</div>
</div>
"""

def total_cases(data):
    return"""
The following graphs show the evolution of the pandemic starting from 2 March 2020, the day the first cases were confirmed in the country.<ref>{{Cite web|url=https://www.publico.pt/2020/03/02/sociedade/noticia/coronavirus-ha-dois-infectados-portugal-1905823|title=Coronavírus: há dois casos confirmados em Portugal|date=March 2, 2020|website=Público|url-status=live}}</ref>

=== Total confirmed and recovered cases ===
{{Graph:Chart
|type=line
|height = 300
|width=1000
|colors=#F46D43,aqua
|showValues=
|legend=Legend
|xAxisTitle=Date
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|y1= """+data['total_cases']+"""
|y1Title=Total confirmed cases
|y2= """+data['recovered']+"""
|y2Title=Total recovered cases
|yGrid= |xGrid=
}}

"""

def new_cases(data):
    return"""
=== New cases per day ===
{{Graph:Chart
|type=line
|height=300
|width=1000
|colors=#F46D43
|showValues= offset:2
|xAxisTitle=Date
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=New cases
|y1= """+data['daily_cases']+"""
|y1Title=New cases per day
|yGrid=
}}

"""


def cases_by_age_and_gender_english(age_gender):
    return"""
=== Total confirmed cases by age and gender ===
The following chart displays the proportion of total cases by age and gender on """+format.date_display_english(age_gender['date'])+""".<ref>{{cite web |url=https://github.com/dssg-pt/covid19pt-data |title= Github - Data Science for Social Good (DSSG)}}</ref><ref>{{cite web |url=https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/ |title=Dashboard DGS}}</ref>
{{Graph:Chart
|height = 300
|width=1000
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Age
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
|yAxisTitle=No. of cases
|legend=Legend
|y1= """+age_gender['cases_men']+"""
|y2= """+age_gender['cases_women']+"""
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}


"""

def total_deaths(data):
    return"""
=== Total confirmed deaths ===
{{Graph:Chart
|type=line
|height=300
|width=1000
|colors=purple
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=No. of confirmed deaths
|y= """+data['total_deaths']+"""
|yGrid= |xGrid=
}}

"""


def new_deaths(data):
    return"""
=== New deaths per day ===
{{Graph:Chart
|type=line
|height=300
|width=1000
|colors=purple
|showValues=offset:2
|xAxisTitle=Date
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=New deaths
|y1=  """+data['daily_deaths']+"""
|y1Title=New deaths per day
|yGrid=
}}


"""

def deaths_by_age_and_gender_english(age_gender):
    return"""
=== Total confirmed deaths by age and gender ===
The following chart displays the proportion of total deaths by age and gender on """+format.date_display_english(age_gender['date'])+""".<ref>{{cite web |url=https://github.com/dssg-pt/covid19pt-data |title= Github - Data Science for Social Good (DSSG)}}</ref><ref>{{cite web |url=https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/ |title=Dashboard DGS}}</ref>
{{Graph:Chart
|height=300
|width=1000
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Age
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=No. of deaths
|legend=Legend
|y1= """+age_gender['deaths_men']+"""
|y2= """+age_gender['deaths_women']+"""
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}

"""

def hospital_admitted(data):
    return"""=== Hospital admitted cases - Stable ===
{{Graph:Chart
|type=line
|height = 300
|width=1000
|colors=orange
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|y1= """+data['hospital_stable']+"""
|yGrid= |xGrid=
}}


"""

def icu_admitted(data):
    return"""=== Hospital admitted cases - ICU ===
{{Graph:Chart
|type=line
|height = 300
|width=1000
|colors=maroon
|showValues=
|xAxisTitle=Date
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=No. of cases
|y1= """+data['hospital_icu']+"""
|yGrid= |xGrid=
}}

<section end="Statistics"/>

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
|height=300
|width=1000
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
|height=300
|width=1000
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
[[Category:COVID-19 pandemic in Portugal|statistics]]
[[Category:Statistics of the COVID-19 pandemic|Portugal]]"""

#portuguese graphs
def age_and_gender_graphs_portuguese(age_gender):
    print('Generating cases by age and gender graphs in portuguese')
    result="""=== Casos por idade e género ===
Os gráficos a seguir refletem a proporção dos casos e mortes por idade e sexo divulgados no dia """+format.date_display_portuguese(age_gender['date'])+""".<ref>{{cite web |url=https://github.com/dssg-pt/covid19pt-data |title= Github - Data Science for Social Good (DSSG)}}</ref><ref>{{cite web |url=https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal |title=Dashboard da DGS}}</ref>

{{Gráfico
|width=750
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Idade
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
|yAxisTitle=Número de casos
|legend=Legenda
|y1= """+age_gender['cases_men']+"""
|y2= """+age_gender['cases_women']+"""
|y1Title=Homens
|y2Title=Mulheres
|yGrid= |xGrid=
}}
<br>
{{Gráfico
|width=750
|colors=blue,orange
|showValues=offset:2
|xAxisTitle=Idade
|type=rect
|x= 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+ 
|yAxisTitle=Número de mortes
|legend=Legenda
|y1= """+age_gender['deaths_men']+"""
|y2= """+age_gender['deaths_women']+"""
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

==== Evolução do número total de casos e recuperações confirmadas ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=#F46D43,aqua
|showValues= 
|legend=Legenda
|xAxisTitle=Data
|xType=date
|xAxisAngle=15
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['total_cases']+"""
|y1Title=casos totais confirmados
|y2= """+data['recovered']+"""
|y2Title=total de recuperações confirmadas
|yGrid= |xGrid=
}}

==== Evolução do número diário de casos confirmadas ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=#F46D43
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisAngle=15
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Novos casos
|y1= """+data['daily_cases']+"""
|y1Title=total de novos casos confirmados por dia
|yGrid= 
|xGrid=
}}

==== Evolução do número total de mortes confirmadas ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=purple
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisAngle=15
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['total_deaths']+""" 
|yGrid= |xGrid=
|y1Title=total de mortes confirmadas
}}

==== Evolução do número diário de mortes confirmadas ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=purple
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisAngle=15
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Novas mortes
|y1= """+data['daily_deaths']+"""
|y1Title=total de mortes confirmadas por dia
|yGrid= |xGrid=
}} 

==== Evolução do número de casos ativos ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=#22BB66
|showValues=
|xAxisTitle=Data
|xType=date
|xAxisAngle=15
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Nº de casos ativos
|y1= """+data['active_cases']+"""
|yGrid= |xGrid=
|y1Title=total de casos ativos
}}


==== Evolução do número de internações ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=orange
|showValues=
|xAxisTitle=Date
|xAxisAngle=15
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1= """+data['hospital_stable']+"""
|yGrid= 
|xGrid=
}}

==== Evolução do número de internações em UCI ====
{{Gráfico
|type=line
|linewidth=2
|width=700
|colors=maroon,
|showValues=
|xAxisTitle=Date
|xAxisAngle=15
|xType=date
|xAxisFormat=%d/%m/%y
|x= """+data['date']+"""
|yAxisTitle=Nº de casos
|y1Title=UCI
|y1= """+data['hospital_icu']+"""
|y2Title=Internados
|yGrid= 
|xGrid=
}}

"""
    with open('output/portuguese/TimelineGraphs.txt', 'w+') as f:
        f.write(result)
