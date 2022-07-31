from Path import *
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from Utils import *


class LinkedInJobs:
    def __init__(self):
        self.email = "soumen.soumen.seth@gmail.com"
        self.password = "Connect Me"
        self.website_link = "https://www.linkedin.com/login"

    def get_job_openings(self, position="data scientist", local="India", page_count=40, store_freq=10):
        '''

        :param position: job post
        :param local: region
        :param page_count: how many job pages it would download from
        :param store_freq: number of pages
        :return:
        '''
        # formatting to linkedin model
        position = position.replace(' ', "%20")

        jobs_webpage = f"https://www.linkedin.com/jobs/search/?geoId=102713980&keywords={position}&location={local}"

        # Open browser
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        # Maximizing browser window to avoid hidden elements
        driver.set_window_size(1024, 600)
        driver.maximize_window()

        # Opening linkedin website
        driver.get(self.website_link)
        # waiting load
        time.sleep(2)

        # Search for login and password inputs, send credentials
        driver.find_element(By.ID, 'username').send_keys(self.email)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)

        # Opening jobs webpage
        driver.get(jobs_webpage)
        # waiting load
        time.sleep(2)

        # creating a list where the descriptions will be stored
        disc_list = []

        # each page show us some jobs, sometimes show 25, others 13 or 21 ¯\_(ツ)_/¯
        # with this knowledge I created a loop that will check how many jobs the page is listing
        # LinkedIn show us 40 jobs pages, then the line below will repeat 40 times
        for i in range(1, page_count):
            # click button to change the job list
            driver.find_element(by=By.XPATH, value=f'//button[@aria-label="Page {i}"]').click()
            # each page show us some jobs, sometimes show 25, others 13 or 21 ¯\_(ツ)_/¯
            jobs_lists = driver.find_element(By.CLASS_NAME,
                                             'jobs-search-results__list')  # here we create a list with jobs
            jobs = jobs_lists.find_elements(By.CLASS_NAME,
                                            'jobs-search-results__list-item')  # here we select each job to count
            # waiting load
            time.sleep(1)
            # the loop below is for the algorithm to click exactly on the number of jobs that is showing in list
            # in order to avoid errors that will stop the automation
            print(len(jobs))
            for job in range(1, len(jobs) + 1):
                # job click
                driver.find_element(by=By.XPATH,
                                    value=f'/html/body/div[4]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{job}]/div/div[1]/div[1]/div[2]/div[3]/ul').click()
                # waiting load
                time.sleep(1)
                # select job description
                job_desc = driver.find_element(By.CLASS_NAME, 'jobs-search__right-rail')
                # get text
                soup = BeautifulSoup(job_desc.get_attribute(
                    'outerHTML'), 'html.parser')
                # add text to list
                disc_list.append(soup.text)
            if i % store_freq == 0:
                write_json(disc_list, LINKEDIN_JOBS_DATA_PATH)
        write_json(disc_list, LINKEDIN_JOBS_DATA_PATH)


if __name__ == '__main__':
    linked_in_jobs = LinkedInJobs()
    linked_in_jobs.get_job_openings()
