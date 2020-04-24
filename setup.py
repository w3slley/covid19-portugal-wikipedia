import sample.report as report
import sample.parser as parser
import sample.date as date

REPORT_PATH = 'var/DGS_report'+date.get_current_date()+'.pdf' #path for pdf report

if report.download(REPORT_PATH):
    print('Parsing data from PDF file...')

    summary = report.get_summary_data(REPORT_PATH)
    symptoms = report.get_symptoms_data(REPORT_PATH)
    cases = report.get_data_by_age_and_gender('cases', REPORT_PATH)
    deaths = report.get_data_by_age_and_gender('deaths', REPORT_PATH)
    
    print('Generating graphs and tables...')

    parser.summary_table(summary, symptoms)
    parser.age_and_gender_graphs(cases, deaths)
    
    print('Graphs and tables generated succesfuly!')
    print('The text files were saved in the directory output/')
    