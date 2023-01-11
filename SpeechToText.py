from ibm_watson import SpeechToTextV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pandas import json_normalize
from dotenv import load_dotenv
import streamlit as st
import os

def configure():
    load_dotenv()

configure()

authenticator = IAMAuthenticator(os.getenv('iam_apikey_s2t'))
s2t = SpeechToTextV1(authenticator=authenticator)
s2t.set_service_url(os.getenv('url_s2t'))
final_result = ""
st.markdown("<h1 style='text-align: center;'> Speech To Text Converter</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)

audio_file = st.file_uploader("Upload Your Mp3 Audio File", type=['mp3'])

def convertTotext(audio_file):
    final_text=""
    try:
        response = s2t.recognize(audio=audio_file, content_type='audio/mp3')
        results_normalized = json_normalize(response.result['results'],"alternatives")
        for i in enumerate(results_normalized.index):
            recognized_text=response.result['results'][i[0]]["alternatives"][0]["transcript"]
            final_text = final_text + recognized_text
        return final_text
    except:
        print("None")
        final_text = final_text + "Unaudible"
        return final_text

if audio_file:
    st.audio(audio_file)
    st.warning("PROCESSING..............")
    final_result = convertTotext(audio_file)
    st.success("DONE")
    with st.form("Result"):
        result = st.text_area("Converted Text", value=final_result)
        download_Btn = st.form_submit_button("Download")
        st.info("Download will be saved in C Drive Downloads")
        if download_Btn:
            envir_var = os.environ
            usr_loc = envir_var.get('USERPROFILE')
            loc = usr_loc+"\Downloads\\transcript.txt"
            with open(loc, 'w') as file:
                file.write(result)
                st.success("DONE")
