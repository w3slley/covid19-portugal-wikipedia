import sample.report as report
import sample.date as date

def summary_table(summary, symptoms):
    print('Generating Summary table...')

    #adding comma formatting to numbers in results array
    for k,v in summary.items(): 
        summary[k] = report.add_comma(v)

    link = report.info()['link']
    date_summary = date.format_date_symptom(report.info()['report_date'])
 
    
    f = open('output/SummaryTable.txt', 'w+')
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


def age_and_gender_graphs(cases, deaths):
    print('Generating cases by age and gender graphs...')
    cases_men = cases['men']
    cases_women = cases['women']

    deaths_men = deaths['men']
    deaths_women = deaths['women']

    result = """
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
|y1= """+cases_men+"""
|y2= """+cases_women+"""
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
|y1="""+deaths_men+"""
|y2= """+deaths_women+"""
|y1Title=Men
|y2Title=Women
|yGrid= |xGrid=
}}"""
    f = open('output/GraphsCasesByAgeAndGender.txt', 'w+')
    f.write(result)
    f.close()