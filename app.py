import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from os import getenv

load_dotenv()
genai.configure(api_key=getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to generate cover letter
def generate_cover_letter(resume_text, job_description):
    prompt = f"Generate a cover letter based on the following resume:\n\n{resume_text}\n\nfor the following job description:\n\n{job_description}"
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Cover Letter Generator")

    # Check if session state exists, if not initialize it
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None

    # Upload resume PDF file
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    if uploaded_file is not None:
        st.write("Resume Uploaded Successfully!")

        # Extract text from the PDF file
        resume_text = extract_text_from_pdf(uploaded_file)

        # Store resume text in session state
        st.session_state.resume_text = resume_text

    # Get job description
    job_description = st.text_area("Enter job description:")

    # Generate button to start cover letter generation process
    if st.button("Generate Cover Letter"):
        with st.spinner("Your cover letter is being generated!! Hang Tight!"):
            # Generate cover letter if both resume and job description are provided
            if st.session_state.resume_text is not None and job_description:
                cover_letter = generate_cover_letter(st.session_state.resume_text, job_description)
                st.write("Generated Cover Letter:")
                st.write(cover_letter)

if __name__ == "__main__":
    main()