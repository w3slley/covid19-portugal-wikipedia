import pytest
import sys,os
sys.path.append(os.path.abspath(os.path.join('.', '')))
import src.format as format
import src.report as report

def test_get_summary_data():
    for i in range(1,10):
        result = report.get_summary_data('var/0'+str(i)+'-09-2020.pdf')
        print(result)
    assert True == False