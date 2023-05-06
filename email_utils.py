from bs4 import BeautifulSoup
import requests
import regex as re
import openai

openai.api_key = "API KEY"

email = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+[.][A-Za-z.]{2,}')

def get_emails(url):

    req = requests.get(url)

    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    emails = email.findall(str(soup.find('main')))
    emails = list(dict.fromkeys(emails))

    return emails

def get_research_template(prof, prof_uni, prof_topic, student_name, student_position, student_uni, student_topic):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Write a cold email to a professor named {prof} at {prof_uni} who is currently researching {prof_topic} from a student named {student_name}, who is a {student_position} at {student_uni}, asking for a position as a research assistant regarding {student_topic}"}
    ]
    )

    return completion.choices[0].message.content

print(get_emails(input("Please enter a url -> ")))

print(get_research_template("Ashton Anderson", "University of Toronto", "Artificial intelligence", "Robert Jordan", "first year student", "University of Waterloo", "Image classification"))