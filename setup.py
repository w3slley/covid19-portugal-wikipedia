
import sample.report as report
import sample.generate as generate

if report.download():
    print('Parsing data from PDF file...')

    summary = report.get_summary_data()
    symptoms = report.get_symptoms_data()
    cases = report.get_data_by_age_and_gender('cases')
    deaths = report.get_data_by_age_and_gender('deaths')

    print('Generating graphs and tables...')

    generate.summary_table(summary, symptoms)
    generate.age_and_gender_graphs(cases, deaths)
    
    print('Graphs and tables generated succesfuly!')
    print('The text files were saved in the directory output/')
