from Utils import *
from Services.skills import SkillsExtractor
from spacy.lang.en import English


class ParseJobDescriptions:
    def __init__(self, job_description):
        self.jd = job_description
        self.nlp = English()
        self.skill_extractor = SkillsExtractor(self.nlp)

    def parse_jd(self):
        job_sections = get_text_paragraphs(self.jd)
        job_position = job_sections[0]
        company = job_sections[1]
        location = job_sections[2]
        skills = self.get_skills()

        job_dict = {
            "job_position": job_position,
            "company": company,
            "location": location,
            "job_sections": job_sections,
            "skills": skills
        }
        return job_dict

    def get_skills(self):
        '''

        :return:
        '''
        skills_extracted = dict(self.skill_extractor.extract_skills(self.jd))
        skills = []

        for key in skills_extracted.keys():
            skill_dict = dict(skills_extracted[key])
            for match in skill_dict["matches"]:
                skill_dict.update({"skill": key})
                skill_dict.update(match)
            del skill_dict['matches']
            skills.append(skill_dict)
        skills = list(set([sk['displayName'] for sk in skills]))
        return skills
