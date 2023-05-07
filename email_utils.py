from bs4 import BeautifulSoup
import pandas as pd
import requests
import regex as re
import cohere
import os
import json
from flask import Flask, jsonify, request, Response
app = Flask(__name__)

co = cohere.Client(os.environ['CO_API_KEY'])

email = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+[.][A-Za-z.]{2,}')
name = re.compile('[A-Z][a-zA-Z]')

@app.route("/api/v1/emails", methods=["POST"])
def get_emails():
    data = json.loads(request.data)
    url_format = re.compile("((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
    if not "url" in data:
      return "Invalid json data format"
    url = data['url']
    if not url_format.match(url):
      return "Invalid URL"
    req = requests.get(url)

    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    emails = email.findall(str(soup.find('main')))
    emails = list(dict.fromkeys(emails))
    emails.remove("arvind@cs.toronto.edu")
    emails.remove("rahulgk@cs.toronto.edu")
    emails.remove("sam@cs.toronto.edu")
    emails.remove("ningningxie@cs.toronto.edu")
    emails.remove("sharmin@cs.toronto.edu")
    emails.remove("sunk@cs.toronto.edu")
    emails.remove("swastik@cs.toronto.edu")
    emails.remove("nawiebe@cs.toronto.edu")

    return jsonify(emails)

@app.route("/api/v1/csv", methods=["POST"])
def generate_csv():
    data = json.loads(request.data) 
    names = data['names']
    emails = data['emails']
    if (not type(names) is list):
       return "Invalid names"
    if (not type(emails) is list):
       return "Invalid emails"
    size = len(emails)
    status = ["Not Applied" for i in range(size)]
    contacted = ["No" for i in range(size)]
    recruiters = { "names" : names, "emails": emails, "status": status, "contacted": contacted }
    
    df = pd.DataFrame(recruiters, columns=["names", "emails", "status", "contacted"]).set_index('names')
    if not os.path.isfile('recruiters.csv'):
      df.to_csv('recruiters.csv', header=['emails', 'status', 'contacted'])
    else: # else it exists so append without writing the header
      pass
      # df.to_csv('recruiters.csv', mode='a', header=False)

@app.route("/api/v1/csv") 
def getPlotCSV():
    if not os.path.isfile('recruiters.csv'):
        return None
    df = pd.read_csv('recruiters.csv')
    csv = df.to_csv()[1:]
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})


@app.route("/api/v1/research", methods=["POST"])
def get_research_template():
    data = json.loads(request.data)
    prof = data['prof']
    prof_uni = data['prof_uni']
    prof_topic = data['prof_topic']
    student_name = data['student_name']
    student_position = data['student_position']
    student_uni = data['student_uni']
    student_topic = data['student_topic']
    prompt = f"Write a cold outreach email to a professor named {prof} at {prof_uni} who is currently researching {prof_topic} from a student named {student_name}, who is a {student_position} at {student_uni}, asking if {prof} is interested in hiring {student_name} as a research assistant regarding {student_topic}. Do not generate emails or phone numbers. Only ask if they are open to hiring people"
    response = co.generate(
    model='command-xlarge-nightly',
    prompt=prompt,
    max_tokens=300,
    temperature=0.5,
    k=0,
    stop_sequences=[],
    return_likelihoods='NONE')

    return response.generations[0]

@app.route("/api/v1/internship", methods=["POST"])
def get_internship_template():
    data = json.loads(request.data)
    company_employee = data['company_employee']
    company_name = data['company_name']
    student_name = data['student_name']
    student_position = data['student_position']
    student_uni = data['student_uni']
    prompt = f"Write a cold outreach email to a person named {company_employee} at {company_name} from a student named {student_name}, who is a {student_position} at {student_uni}, asking if {company_name} is interested in hiring {student_name} as an intern. Do not generate emails or phone numbers. Only ask if they are open to hiring people"
    response = co.generate(
      model='command-xlarge-nightly',
      prompt=prompt,
      max_tokens=300,
      temperature=0.5,
      k=0,
      stop_sequences=[],
      return_likelihoods='NONE')

    return response.generations[0]


# TODO: Fix this function
@app.route("/api/v1/names", methods=["POST"])
def get_names():
    data = json.loads(request.data)
    url_format = re.compile("((http|https)://)(www.)?[a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)")
    if not "url" in data:
      return "Invalid json data format"
    url = data['url']
    if not url_format.match(url):
      return "Invalid URL"
    req = requests.get(url)

    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    names = []

    for div in soup.findAll('td'):
      try:
        names.append(div.find('a').contents[0])
      except:
        continue

    names = [i for i in names if not email.match(i)]

    return jsonify(names)
    
app.run(debug=True)

