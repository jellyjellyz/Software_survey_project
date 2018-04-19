from plot_all_jobs import *
from plot_job_by_state import *
from plot_num_of_jobs_by_state import *
from plot_top5_jobdescription import *
import get_all_intro_pages
from bs4 import BeautifulSoup
import get_all_detail_pages
import sqlite3
import unittest

class TestDataAccess(unittest.TestCase):
    def test_scrap_intropage(self):
        def make_request_for_jobs_in_page(page_num):
            baseurl = 'https://www.careerbuilder.com'
            extendurl = baseurl + "/jobs-software-engineer?page_number={}".format(page_num)
            para = {'Referer': '{}'.format(extendurl), \
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
            resp = get_all_intro_pages.make_request_using_cache(extendurl, theheader = para)
            soup = BeautifulSoup(resp, 'html.parser')
            jobs = soup.find_all(name="div", attrs={"class":"job-row"})
            job_title = []
            for ajob in jobs:
                try:
                    job_title.append(ajob.find(attrs={"class": "job-title"}).text.strip())
                except:
                    pass
            return job_title

        job_name1 = make_request_for_jobs_in_page(1)[3]
        job_name2 = make_request_for_jobs_in_page(50)[6]
        job_name3 = make_request_for_jobs_in_page(100)[15]
        num_of_job_one_page1 = len(make_request_for_jobs_in_page(2))
        num_of_job_one_page2 = len(make_request_for_jobs_in_page(100))

        self.assertEqual(job_name1, 'Junior Software Developer')
        self.assertEqual(job_name2, 'Sr. Electrical Engineer')
        self.assertEqual(job_name3, 'Technical Sales Engineer')
        self.assertEqual(num_of_job_one_page1, 25)
        self.assertEqual(num_of_job_one_page2, 25)
        
    def test_scrap_detailpage(self):
        def make_detail_page_request_for_a_job(job_num):
            FILENAME = './caches/detail_urls.text'
            detailurl_file = open(FILENAME, "r") 
            aurl = detailurl_file.readlines()[job_num]
            aurl = aurl[:-1]
            para = {'Referer': '{}'.format(aurl), \
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
            resp = get_all_detail_pages.make_request_using_cache(aurl, para, job_num)
            soup = BeautifulSoup(resp, 'html.parser')
            try:
                job_title = soup.find_all(name="div", attrs={"class":"small-12 item"})[0].text.strip()
            except:
                pass
            detailurl_file.close()
            return  job_title
        
        job_name1 = make_detail_page_request_for_a_job(50)
        job_name2 = make_detail_page_request_for_a_job(500)
        job_name3 = make_detail_page_request_for_a_job(2000)

        self.assertEqual(job_name1, 'Junior Software Developer')
        self.assertEqual(job_name2, 'GUI .Net Software Engineer')
        self.assertEqual(job_name3, 'Automation Development Engineer II')

class TestDataBase(unittest.TestCase):
    def test_job_table(self):
        conn = sqlite3.connect('jobs.sqlite')
        cur = conn.cursor()
        statement = '''
            SELECT title, jobtype
            FROM Jobs
        '''
        cur.execute(statement)
        result_list = cur.fetchall()
        self.assertLess(len(result_list), 2500)
        self.assertGreater(len(result_list), 2000)
        self.assertEqual(result_list[-2][0], 'Regional Logistics Engineer')
        self.assertEqual(result_list[-2][1], 'Full-Time')
        conn.close()



    def test_company_table(self):
        conn = sqlite3.connect('jobs.sqlite')
        cur = conn.cursor()
        statement = '''
            SELECT State
            FROM Company
            GROUP BY State
        '''
        cur.execute(statement)
        result_list = cur.fetchall()
        num_of_states = len(result_list)
        self.assertEqual(num_of_states, 50)
        self.assertIn(('CA',), result_list)
        
        statement = '''
            SELECT Name, Region
            FROM Company
        '''
        cur.execute(statement)
        result_list = cur.fetchall()
        self.assertGreater(len(result_list), 1000)
        self.assertEqual(result_list[2][0], 'Kforce Technology')
        self.assertEqual(result_list[2][1], 'Baltimore')



class TestPlot(unittest.TestCase):
    def test_map_plot(self):
        try:
            plot_all_jobs()
        except:
            self.fail()

        try:
            plot_job_by_state('VA')
            plot_job_by_state('OH')
        except:
            self.fail()

    def test_bar_plot(self):
        try:
            plot_num_of_jobs_by_state()
            plot_top5_jobdescription()
        except:
            self.fail()


if __name__ == '__main__':
    unittest.main()

