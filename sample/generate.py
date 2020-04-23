import sample.report as report

def summary_table(summary, symptoms):
    summary = [report.beautify_number(i) for i in summary]#applying formatting function to all numbers in summary array
    print('Generating Summary table...')
    link = report.info()['link']
    date = report.info()['report_date']
    suspected_cases = summary[0]
    confirmed_cases = summary[1]
    not_confirmed_cases = summary[2]
    waiting_results = summary[3]
    recovered = summary[4]
    deaths = summary[5]
    under_surveillance = summary[6]

    f = open('output/SummaryTable.txt', 'w+')
    result ="{"
    result += f"""| class="wikitable"
|+COVID-19
! colspan="2" |Cases [{link} {date}]
|-
!total confirmed cases
|{confirmed_cases}
|-
!total not confirmed cases 
|{not_confirmed_cases}
|-
!total suspected cases (since 1 January 2020)
|{suspected_cases}
|-
!under surveillance
|{under_surveillance}
|-
!waiting for results
|{waiting_results}
|-
!recovered
|{recovered}
|-
!deaths
|{deaths}
|-
|"""
    result+="}\n\n"

    percentages = symptoms['percentages']
    occurrence = symptoms['occurrence']
    result += "{"
    result += f"""| {{Table}}
!   !! high fever !! dry cough !! difficult breathing !! headache !! muscular pain !! tiredness
|-
! % of cases with symptoms
| {percentages[0]}
| {percentages[1]}
| {percentages[2]}
| {percentages[3]}
| {percentages[4]}
| {percentages[5]}
|-
|"""
    result+="}\n"
    result+=f"""There was only reported information regarding the occurrence of symptoms on {occurrence} of confirmed cases.<ref>{{cite web|url={report.info()['link']} |title=COVID-19 RELATÓRIO DE SITUAÇÃO |date={report.info()['report_date'].replace('/', '-')} |website=covid19.min-saude.pt}}</ref>"""
    

    f.write(result)
    f.close()




def age_and_gender_graphs(cases, deaths):
    print('Generating cases by age and gender graph...')
    cases_men = cases['men']
    cases_women = cases['women']

    deaths_men = deaths['men']
    deaths_women = deaths['women']

    result = f"""
=== Cases by age and gender ===
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
|y1= {cases_men}
|y2= {cases_women}
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
|y1={deaths_men}
|y2= {deaths_women}
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}"""
    f = open('output/GraphsCasesByAgeAndGender.txt', 'w+')
    f.write(result)
    f.close()