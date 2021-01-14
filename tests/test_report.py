import pytest
import sys,os
sys.path.append(os.path.abspath(os.path.join('.', '')))
import sample.format as format
import sample.report as report 

def test_download():
    url = report.info_latest()['link']
    filename = 'tests/'+report.info_latest()['report_date'].replace('/','-')+'.pdf'
    report.download(url, filename)
    assert os.path.isfile(filename)
    report.delete(filename)

def test_get_summary_data():
    result = report.get_summary_data('var/22-12-2020.pdf')
    print(result)
    assert result == {
        'confirmed_cases': '378656',
        'active': '67577',
        'recovered': '304825',
        'deaths': '6254',
        'under_surveillance': '86334',
        'cases_men': '170035',
        'cases_women': '208484',
        'deaths_men': '3258',
        'deaths_women': '2996'
    }

def test_get_hospitalized_data():
    result = report.get_hospitalized_data('var/22-12-2020.pdf')
    assert result == {
        'hospital_stable': '3095',
        'hospital_icu': '508'
    }