'''
Install all required packages using
pip install -r requirements.txt

Run using
python main.py

'''

from loader import Load
from extract import tool_creation, call_agent

def out():
    resume="D:\SVCE\Chatgpt\Trials\\2127200501079.pdf"
    jd="D:\SVCE\Chatgpt\Trials\jd.txt"

    l = Load()
    resume_data = l.identify_and_load(resume)
    jd_data = l.identify_and_load(jd)

    tool_creation("resume", resume_data)
    tool_creation("job_description", jd_data)

    call_agent("Are the skills in job description and resume matching?")



if __name__=='__main__':
    out()


