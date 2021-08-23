import pytest
import sys,os
sys.path.append(os.path.abspath(os.path.join('.', '')))
import src.format as format
import src.report as report
import urllib.request
import json

def test_PDF_format():
    latest_report_date = report.info_latest('portugal_data.csv')['report_date'].replace('/','-')
    filename = latest_report_date+'.pdf' #moved file from var/ to ./ to prevent deleting report that was already parsed
    #downloading DGS report
    report.download(report.info_latest('portugal_data.csv')['link'], filename)
    #getting data
    data_summary = report.get_summary_data(filename)
    data_hospt = report.get_hospitalized_data(filename)
    age_and_gender = report.get_data_by_age_and_gender(filename)
    coefficients = report.get_incidence_and_transmissibility(filename)
    print(data_summary,data_hospt)

    #deleting report
    report.delete(filename)
    #assertion
    assert format.are_values_valid(data_summary) and format.are_values_valid(data_hospt) and format.are_values_valid(age_and_gender) and len(data_summary) == 9 and len(data_hospt) == 2 and len(age_and_gender) == 4

    #assertions for incidence and r(t) method
    for col in coefficients.keys():
        assert type(coefficients[col]) is float

def test_get_recent_data_age_gender():
    req = urllib.request.Request('https://covid19-api.vost.pt/Requests/get_last_update')
    req.add_header('User-Agent','Mozilla/5.0')
    url = urllib.request.urlopen(req)
    data_request = url.read()
    data = json.loads(data_request.decode('utf-8'))

    assert data['confirmados_0_9_f'] != None and data['obitos_0_9_f'] != None
