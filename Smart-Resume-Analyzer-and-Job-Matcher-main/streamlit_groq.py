import os
from groq import Groq
from dotenv import load_dotenv
import serpapi
from PyPDF2 import PdfReader
from groq import Groq
import os

PDF_FILE_PATH=r" "


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def extract_text_from_pdf_with_pypdf2():
    loc = PDF_FILE_PATH
    reader = PdfReader(loc)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print(text)
    return text

def evaluate_resume(prompt, conversation_history):
    conversation_history.append({"role": "user", "content": prompt})

    full_prompt = "\n".join([message["content"] for message in conversation_history])

    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": full_prompt
        }
    ],
    model="llama3-8b-8192",
    max_tokens=1024
    )


    result = response.choices[0].message.content

    conversation_history.append({"role": "system", "content": result})

    return conversation_history, result


def job_seek_fun(Job_Role):
    load_dotenv()
    jobSeek = []
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    job_client_search = serpapi.Client(api_key=SERP_API_KEY)
    results_ = job_client_search.search(
        {
            "engine": "google_jobs",
            "q": Job_Role,
            "location": "New York, NY",
            "chips": "date_posted:month",
        }
    )
    
    if 'jobs_results' in results_:
        jobSeek.append( ["Job Title", "Company Name", "Location"])
        for job_result in results_["jobs_results"]:
            # Extract details separately
            job_title = job_result.get("title", "N/A")
            company_name = job_result.get("company_name", "N/A")
            location = job_result.get("location", "N/A")
            jobSeek.append([job_title,company_name,location])
    else:
        jobSeek.append("None Found")

    return jobSeek


def llm_prompt(job_role, job_description, resume_content):

    prompts = [
        f"Evaluate the following resume for job role: {job_role} with job description: {job_description}:\n\n{resume_content}"
    ]


    results, conversation_history = [], []
    for prompt in prompts:
        conversation_history, result = evaluate_resume(prompt, conversation_history)
        results.append(result)
    
    
    conversation_history = []
    prompt = (
        f"For this resume:\n\n{resume_content}\n\nWhat is the best role (only one word)"
    )
    _, Job_Role = evaluate_resume(prompt, conversation_history)
    print('******************************')
    recc_jobs = job_seek_fun(Job_Role)
    print(recc_jobs)

    main_summary=results[0]

    print('******************************')
    print(main_summary)

    return main_summary,result,recc_jobs
