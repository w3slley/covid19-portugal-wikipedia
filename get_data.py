import os
import sample.report as report
import sample.parser as parser
import sample.date as date
import sample.update_csv as csv

#running tests
os.system('pytest -v --disable-warnings tests/test_global.py');

REPORT_PATH = 'var/'+report.info_latest()['report_date'].replace('/','-')+'.pdf' #path for latest pdf report
csv.update()

print('Parsing data from latest DGS report')

summary = report.get_summary_data(REPORT_PATH)
hospital = report.get_hospitalized_data(REPORT_PATH)
parser.graphs_english(summary, hospital)
parser.age_and_gender_graphs_portuguese(report.get_recent_data_age_gender())
parser.timeline_graphs_portuguese()

print('Graphs and tables generated succesfuly')
print('The text files were saved in the directory output/')

#opening output files (both portuguese and english)
open = input("Open .txt files?[y][n]")
if(open == 'y'):
    os.system('xed output/PortugalCovid-19-Statistics.txt output/portuguese/GraphsCasesByAgeAndGender.txt output/portuguese/TimelineGraphs.txt')


