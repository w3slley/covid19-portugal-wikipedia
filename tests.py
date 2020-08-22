import pytest
import sample.format as format
import sample.report as report

class TestReportMethods:
	def test_get_summary_data(self):
		result = report.get_summary_data('var/22-08-2020.pdf')
		assert result == {
			'confirmed_cases': '55452',
			'active': '13006',
			'recovered': '40652',
			'deaths': '1794',
			'under_surveillance': '34182',
			'cases_men': '24939',
			'cases_women': '30513',
			'deaths_men': '903',
			'deaths_women': '891'
		}

	def test_get_hospitalized_data(self):
		result = report.get_hospitalized_data('var/17-08-2020.pdf')
		assert result == {
			'hospital_stable': '336',
			'hospital_icu': '39'
		}

