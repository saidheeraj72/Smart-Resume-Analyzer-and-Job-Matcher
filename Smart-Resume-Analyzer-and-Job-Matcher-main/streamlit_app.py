import streamlit as st
from streamlit_groq import llm_prompt, extract_text_from_pdf_with_pypdf2,PDF_FILE_PATH


st.set_page_config(page_title="Genz Hiring", layout="wide")

def process_text(text):
    """Process text by removing asterisks and applying formatting."""
    processed_text = text.replace('*', '')
    return processed_text


st.title("Smart Resume Analyzer and Job Matcher")

with st.container():
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        try:
            with open(PDF_FILE_PATH, "wb") as f:
                f.write(uploaded_file.read())

            text = extract_text_from_pdf_with_pypdf2()

            jobrole = st.text_input("Job Role")
            jobdesc = st.text_area("Job Description")

            if st.button("Generate Report"):
                if jobrole and jobdesc:
                    try:
                        main_summary, result_mod, JobSeek = llm_prompt(jobrole, jobdesc, text)

                        left = process_text(main_summary)
                        right = process_text(result_mod)
                        jobSeek = JobSeek

                        st.subheader("Report")
                        st.markdown(f"**Summary:** {left}")
                        st.markdown(f"**Modifications:** {right}")
                        if jobSeek[0]!="None Found":
                            st.subheader("Job Seek")
                            num_columns = len(jobSeek[0])
                            columns = st.columns(num_columns)

                            # Display the headers
                            for idx, header in enumerate(jobSeek[0]):
                                columns[idx].subheader(header)

                            # Display the rows
                            for row in jobSeek[1:]:
                                for idx, item in enumerate(row):
                                    columns[idx].write(item)
                        else:
                            st.markdown(f"**Job Seek:** {jobSeek[0]}")


                    except Exception as e:
                        st.error(f"An error occurred while generating the report: {e}")
                else:
                    st.warning("Please enter both Job Role and Job Description.")

        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")

