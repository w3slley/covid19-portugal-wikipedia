import pytest
import sys,os
sys.path.append(os.path.abspath(os.path.join('.', '')))
import sample.format as format
import sample.report as report

def test_data_by_age_and_gender():
    for i in range(1,10):
        result = report.get_data_by_age_and_gender('var/0'+str(i)+'-09-2020.pdf')
        print(result)
    assert True == False