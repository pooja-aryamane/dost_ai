import streamlit as st
from google.cloud import speech
import os
import io
import base64
import requests
from openai import OpenAI
from langchain_openai import ChatOpenAI
import json

st.set_page_config(page_title='insync-ai', page_icon=":earth_asia:", initial_sidebar_state="expanded", layout='wide') 

# st.markdown("""
#     <style>
#         .st-emotion-cache-1kyxreq {
#             overflow-wrap: break-word !important;
#             white-space: normal !important;
#             word-break: break-word !important;
#         }
#     </style>
# """, unsafe_allow_html=True)

st.header("Keep your Family In-Sync with Medical Care, No Matter the Distance")
st.write("Let's get your conversation in writing. Click the button below, and we will do the rest.")

api_key = st.text_input(label='Enter API Key Here:', type='password')
audio_value = st.audio_input("When you're ready, click the record button and start speaking!")


if st.button("Start Listening"):

    #Create the model object
    llm = ChatOpenAI(
        model="gpt-4o-audio-preview",  # Specifying the model
        temperature=0,  # Controls randomness in the output
        max_tokens=None,  # Unlimited tokens in output (or specify a max if needed)
        timeout=None,  # Optional: Set a timeout for requests
        max_retries=2,  # Number of retries for failed requests,
        openai_api_key=api_key
    )

    content = audio_value.read()
    encoded_string = base64.b64encode(content).decode()

    old_prompt = """Transcribe the following audio first. The, give me a summary like a medical report. Include the transcription as well."""
    
    new_prompt = """Your task is to transcribe the audio provided to you. The audio is an interaction between a doctor and a patient. So there will be medical jargon in the conversation. \
        Make sure that you get those medical terms and other details accurate. 
        Your transcription will be used by a doctor to make future decisions and should have this format ->
        Doctor : 
        Patient : 
        With each line tagged according to the speaker. Both this should all be in separate lines according to the conversation. Return the transcription in a markdown format. \
        
        Your summary should be very detailed and in the form of a medical report and should have this format -> 
        
        Todays Date : 
        Patient Name : 
        Patient DOB : 

        Reason for visit : Detailed Paragraph
        Medical History : Medical History/Lifestyle (paragraph)
        Diagnosis : Diagnosis details (paragraph)
        Next Steps and Treatment : Treatment plan for the patient (paragraph)
          
        Return the summary report in a markdown format. 

        You might not find all the details in every conversation. In that case, just write NA. Don't try to make stuff up.
       
        Your final response should include both the transcription and the summary as a JSON object with the keys "transcription" and "summary" respectively.
        
        Both transcription and summary should be in a markdown format. Make sure they are in a markdown format. 
        
        Stick to this format at all times!
"""
    messages = [
    (
        "human",
        [
            {"type": "text", "text": new_prompt},
            {"type": "input_audio", "input_audio": {"data": encoded_string, "format": "wav"}},
        ],
    )
    ]

    s = llm.invoke(messages).content

    json_str = s[s.find('{'):s.rfind("}")+1] #find the first { and the last } and get the string in between

    # try:
    result = json.loads(json_str)

    # result = {'summary':'This is a summary',
    #           'transcription': 'This is a transcription.'}
    if "summary" in result and "transcription" in result:

        t, s  = st.tabs(['Summary','Detailed Transcription'])
        # with t:
        with t:
            #st.subheader("Your Conversation:")
            summary = result['summary']
            st.markdown(summary)
        with s: 
            #st.subheader("Report:")
            transcription = result['transcription']
            st.markdown(transcription)
    else:
        st.error("Something went wrong. Please try again later.",icon="🚨")
    # except:
    #     st.error("Something went wrong. Please try again later.",icon="🚨")

