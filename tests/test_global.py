import pytest
import sys,os
sys.path.append(os.path.abspath(os.path.join('.', '')))
import sample.format as format
import sample.report as report

def test_PDF_format():
    latest_report_date = report.info_latest()['report_date'].replace('/','-')
    filename = 'var/'+latest_report_date+'.pdf'
    #downloading DGS report
    report.download(report.info_latest()['link'], filename)
    #getting data
    data_summary = report.get_summary_data(filename)
    data_hospt = report.get_hospitalized_data(filename)
    age_and_gender = report.get_data_by_age_and_gender(filename)
    print(data_summary)
    #deleting report
    report.delete(filename)
    #assertion
    assert format.are_values_valid(data_summary) and format.are_values_valid(data_hospt) and format.are_values_valid(age_and_gender) and len(data_summary) == 9 and len(data_hospt) == 2 and len(age_and_gender) == 4
