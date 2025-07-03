import streamlit as st
from utils import extract_text_from_pdf, generate_questions
import os
from dotenv import load_dotenv

load_dotenv()

st.title("📘 Concept Question Generator")

st.markdown("Upload a concept file (PDF), select number of questions (max 10), and click Generate.")

# Upload
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

# Number of questions
num_questions = st.slider("Select number of questions", min_value=1, max_value=10, value=5)

if uploaded_file is not None:
    # Extract content
    with st.spinner("Reading file..."):
        content = extract_text_from_pdf(uploaded_file)

    if st.button("Generate Questions"):
        with st.spinner("Generating questions using Groq..."):
            questions = generate_questions(content, num_questions)
            st.success("Questions generated!")
            for i, q in enumerate(questions, 1):
                st.markdown(f"**Q{i}:** {q}")
