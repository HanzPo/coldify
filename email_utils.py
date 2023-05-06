from bs4 import BeautifulSoup
import requests
import regex as re
import cohere

co = cohere.Client('')

email = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+[.][A-Za-z.]{2,}')
name = re.compile('^[\w\'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$')

def get_emails(url):

    req = requests.get(url)

    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    emails = email.findall(str(soup.find('main')))
    emails = list(dict.fromkeys(emails))

    return emails


def get_research_template(prof, prof_uni, prof_topic, student_name, student_position, student_uni, student_topic):
    response = co.generate(
  model='command-xlarge-nightly',
  prompt=f"Write a cold outreach email to a professor named {prof} at {prof_uni} who is currently researching {prof_topic} from a student named {student_name}, who is a {student_position} at {student_uni}, asking if {prof} is interested in hiring {student_name} as a research assistant regarding {student_topic}. Do not generate emails or phone numbers. Only ask if they are open to hiring people"
,
  max_tokens=300,
  temperature=0.9,
  k=0,
  stop_sequences=[],
  return_likelihoods='NONE')

    return response.generations[0].text

def get_names(url):
    req = requests.get(url)

    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    names = name.findall(str(soup.find('a')))
    names = list(dict.fromkeys(names))

    return names

# print(get_names(input("Please enter a url -> ")))

print(get_research_template("Alice Smith", "Toronto Metropolitan University", "artificial intelligence", "Bob Ross", "first year student", "Toronto Metropolitan University", "natural language processing"))