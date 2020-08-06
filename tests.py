import unittest
import sample.format as format
import sample.report as report

class TestFormat(unittest.TestCase):
    def test_one(self):
        self.assertEqual(1,1)

    def test_add_commas(self):
    	number = '12345'
    	self.assertEqual(format.add_commas(number), '12,345')

    def test_date_symptom(self):
    	self.assertEqual(format.date_symptom('26/07/2020'), '2020-07-26')


class TestReport(unittest.TestCase):
	def test_info(self):
		self.assertEqual(report.info()['link'][:29],'https://covid19.min-saude.pt/')

	def test_get_data_by_age_and_gender(self):
		filename = 'var/25-07-2020.pdf'
		self.assertEqual(len(report.get_data_by_age_and_gender('cases', filename)['men'].split(',')), 10)
		self.assertEqual(len(report.get_data_by_age_and_gender('cases', filename)['women'].split(',')), 10)

if __name__ == '__main__':
    unittest.main()