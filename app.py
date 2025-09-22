import streamlit as st
from google import genai
import tempfile

PROMPT = """
\n\nUsing the Air Force Tongue and Quill, Review the following MFR and list the points of 
improvement that it needs in bullet points. The //SIGNED// that the MFR contains
replaces the signature in the mfr and should be kept. I want you to only use
the tongue and quill to grade the MFR. Be deterministic and don't be too wordy. Also,
cite section and the page of the tongue and quill that you are referring to.\n\n
"""
GEMINI_API = st.secrets["GEMINI_API"]


def Generate_Review(MFR):
    MFR = upload_to_gemini(MFR)

    st.subheader("Review:")
    gemini = st.empty()
    gemini.write("Successfully Uploaded! Reviewing the MFR...\n\n")

    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            TAQ,
            PROMPT,
            MFR,
        ],
    )
    return gemini.write(result.text)

def upload_to_gemini(uploaded_file):
    # Save upload to a real file
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Upload using file path (SDK infers mime type from suffix)
    return client.files.upload(file=tmp_path)


st.set_page_config(page_title="MFR Reviewer", page_icon="📝", layout="centered")

client = genai.Client(api_key=GEMINI_API)

# Upload the MFR format template and the MFR to be reviewed
TAQ = client.files.upload(file="tongue_and_quill.pdf")


mfr = st.file_uploader("Upload MFR", type="pdf", accept_multiple_files=False)

if mfr is not None:
    Generate_Review(mfr)