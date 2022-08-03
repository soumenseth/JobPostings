from flask import Flask, render_template, request, redirect, url_for, make_response
from WebApp import app
import os
import json
from collections import Counter
import pandas as pd
from Utils import *
from Path import *


@app.route('/')
@app.route('/home')
def home_page():
    job_postings = read_json(LINKEDIN_PARSED_JOBS_DATA_PATH)
    return render_template('home.html', job_postings=job_postings[5:15])


@app.route('/job-positions')
def job_positions():
    jobs = read_json(LINKEDIN_PARSED_JOBS_DATA_PATH)
    job_pos = [jb["job_position"] for jb in jobs]
    jobs_counter = Counter(job_pos)

    df_jobs = pd.DataFrame.from_dict(jobs_counter, orient='index').reset_index().sort_values(by=0, ascending=False)
    df_jobs.rename(columns={'index': 'position', 0: 'count'}, inplace=True)
    df_jobs.reset_index(drop=True,inplace=True)
    return render_template('job-positions.html', tables=[df_jobs.to_html()], titles=df_jobs.columns.tolist())


@app.route('/skills')
def skills():
    jobs = read_json(LINKEDIN_PARSED_JOBS_DATA_PATH)
    langs = read_json(PROGRAMMING_LANGUAGES_PATH)
    skills_position = sum([jb["skills"] for jb in jobs], [])
    langs_position = [sp for sp in skills_position if sp in langs]
    skills_position = [sp for sp in skills_position if sp not in langs]

    skills_counter = Counter(skills_position)
    df_skills = pd.DataFrame.from_dict(skills_counter, orient='index').reset_index().sort_values(by=0, ascending=False)
    df_skills.rename(columns={'index': 'Skill', 0: 'Jobs count'}, inplace=True)
    df_skills.reset_index(drop=True, inplace=True)

    langs_counter = Counter(langs_position)
    df_langs = pd.DataFrame.from_dict(langs_counter, orient='index').reset_index().sort_values(by=0, ascending=False)
    df_langs.rename(columns={'index': 'Programming Languages', 0: 'Jobs count'}, inplace=True)
    df_langs.reset_index(drop=True, inplace=True)
    return render_template('job-skills.html',
                           skill_tables=[df_skills.to_html()],
                           skill_titles=df_skills.columns.tolist(),
                           langs_tables=[df_langs.to_html()],
                           langs_titles=df_langs.columns.tolist())

@app.route('/degrees')
def degrees():
    jobs = read_json(LINKEDIN_PARSED_JOBS_DATA_PATH)
    degrees_position = sum([jb["degrees"] for jb in jobs], [])

    degrees_counter = Counter(degrees_position)
    df_degrees = pd.DataFrame.from_dict(degrees_counter, orient='index').reset_index().sort_values(by=0, ascending=False)
    df_degrees.rename(columns={'index': 'Degree', 0: 'Jobs count'}, inplace=True)
    df_degrees.reset_index(drop=True, inplace=True)

    return render_template('job-degrees.html',
                           degree_tables=[df_degrees.to_html()],
                           degree_titles=df_degrees.columns.tolist())