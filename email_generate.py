import os
import openai
openai.api_key = "API_KEY"

def get_research_template(prof, prof_uni, prof_topic, student_name, student_position, student_uni, student_topic):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Write a cold email to a professor named {prof} at {prof_uni} who is currently researching {prof_topic} from a student named {student_name}, who is a {student_position} at {student_uni}, asking for a position as a research assistant regarding {student_topic}"}
    ]
    )

    return completion.choices[0].message.content

print(get_research_template("Ashton Anderson", "University of Toronto", "Artificial intelligence", "Robert Jordan", "first year student", "University of Waterloo", "Image classification"))