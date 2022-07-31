import os

os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
from ParseJobDescriptions import ParseJobDescriptions
from Utils import *
from Path import *
from tqdm import tqdm

if __name__ == "__main__":
    jobs_list = read_json(LINKEDIN_JOBS_DATA_PATH)
    jobs_parsed = []
    for job in tqdm(jobs_list):
        job_parsed = ParseJobDescriptions(job)
        jobs_parsed.append(job_parsed.parse_jd())
    write_json(jobs_parsed, LINKEDIN_PARSED_JOBS_DATA_PATH)
