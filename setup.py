import sample.report as report
import sample.parser as parser
import sample.date as date
import sample.update_csv as csv

REPORT_PATH = 'var/'+report.info()['report_date'].replace('/','-')+'.pdf' #path for latest pdf report
csv.update()

print('Parsing data from PDF file...')

summary = report.get_summary_data(REPORT_PATH)
symptoms = report.get_symptoms_data(REPORT_PATH)
cases = report.get_data_by_age_and_gender('cases', REPORT_PATH)
deaths = report.get_data_by_age_and_gender('deaths', REPORT_PATH)

parser.statistics_english(cases, deaths, summary, symptoms)
parser.timeline_graphs_portuguese()

print('Graphs and tables generated succesfuly!')
print('The text files were saved in the directory output/')
