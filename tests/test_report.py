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

def test_get_data_by_age_and_gender():
    result = report.get_data_by_age_and_gender('var/17-08-2020.pdf')
    assert result == {
        'cases_men': '24335',
        'cases_women': '29899',
        'deaths_men': '896',
        'deaths_women': '883'
    }

def test_get_summary_data():
    result = report.get_summary_data('var/09-09-2020.pdf')
    assert result == {
        'confirmed_cases': '61541',
        'active': '16408',
        'recovered': '43284',
        'deaths': '1849',
        'under_surveillance': '35151',
        'cases_men': '27744',
        'cases_women': '33797',
        'deaths_men': '930',
        'deaths_women': '919'
    }

def test_get_hospitalized_data():
    result = report.get_hospitalized_data('var/09-09-2020.pdf')
    assert result == {
        'hospital_stable': '391',
        'hospital_icu': '52'
    }