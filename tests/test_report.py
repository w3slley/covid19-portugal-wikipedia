import pytest
import sys,os
sys.path.append(os.path.abspath(os.path.join('.', '')))
import src.format as format
import src.report as report 

def test_download():
    url = report.info_latest()['link']
    filename = 'tests/'+report.info_latest()['report_date'].replace('/','-')+'.pdf'
    report.download(url, filename)
    assert os.path.isfile(filename)
    report.delete(filename)

def test_get_summary_data():
    result = report.get_summary_data('var/23-12-2020.pdf')
    print(result)
    assert result == {
        'confirmed_cases': '383258',
        'active': '68469',
        'recovered': '308446',
        'deaths': '6343',
        'under_surveillance': '87043',
        'cases_men': '172152',
        'cases_women': '210969',
        'deaths_men': '3299',
        'deaths_women': '3044'
    }

def test_get_hospitalized_data():
    result = report.get_hospitalized_data('var/26-12-2020.pdf')
    print(result)
    assert result == {
        'hospital_stable': '2990',
        'hospital_icu': '511'
    }