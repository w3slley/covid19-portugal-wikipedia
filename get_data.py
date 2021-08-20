import os
import sample.report as report
import sample.parser as parser
import sample.date as date
import sample.update_csv as csv

REPORT_PATH = 'reports/situation/'+report.info_latest()['report_date'].replace('/','-')+'.pdf' #path for latest pdf report
csv.update_situation_reports()
csv.update_vaccine_reports()

print('Parsing data from latest DGS report')


parser.graphs_english()
parser.age_and_gender_graphs_portuguese(report.get_recent_data_age_gender())
parser.timeline_graphs_portuguese()

print('Graphs and tables generated succesfuly')
print('The text files were saved in the directory output/')

#opening output files (both portuguese and english)
open = input("Open .txt files?[y][n]")
if(open == 'y'):
    os.system('xed output/PortugalCovid-19-Statistics.txt output/portuguese/GraphsCasesByAgeAndGender.txt output/portuguese/TimelineGraphs.txt')


