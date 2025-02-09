import streamlit as st
from google.cloud import speech
import os
import io
import base64
import requests
from openai import OpenAI
from langchain_openai import ChatOpenAI
import json

st.set_page_config(page_title='sunlo', page_icon=":globe_with_meridians:", initial_sidebar_state="expanded", layout='wide') 

# st.markdown("""
#     <style>
#         .st-emotion-cache-1kyxreq {
#             overflow-wrap: break-word !important;
#             white-space: normal !important;
#             word-break: break-word !important;
#         }
#     </style>
# """, unsafe_allow_html=True)

st.title("Miles Apart, Stay Informed—Accurate Medical Updates for Your Family.")
st.write("Welcome! This is a tool that helps you keep a record of your medical conversations without missing any details. Just record your conversation, click the button below and we will do the rest.")

api_key = st.text_input(label='Enter API Key Here:', type='password')
audio_value = st.audio_input("When you're ready, click the record button and start speaking!")


if st.button("Listen and generate report"):

    # Create the model object
    # llm = ChatOpenAI(
    #     model="gpt-4o-audio-preview",  # Specifying the model
    #     temperature=0,  # Controls randomness in the output
    #     max_tokens=None,  # Unlimited tokens in output (or specify a max if needed)
    #     timeout=None,  # Optional: Set a timeout for requests
    #     max_retries=2,  # Number of retries for failed requests,
    #     openai_api_key=api_key
    # )

    # content = audio_value.read()
    # encoded_string = base64.b64encode(content).decode()
    #the path of your audio file
#     file_name = "interaction2.wav"
#     with io.open(file_name, "rb") as audio_file:
#         content = audio_file.read()
#         #audio = speech.RecognitionAudio(content=content)

#     encoded_string = base64.b64encode(content).decode()
#     old_prompt = """Transcribe the following audio first. The, give me a summary like a medical report. Include the transcription as well."""
    
#     new_prompt = """Your task is to transcribe the audio provided to you. The audio is an interaction between a doctor and a patient. So there will be medical jargon in the conversation. \
#         Make sure that you get those medical terms and other details accurate. 
#         Your transcription will be used by a doctor to make future decisions and should have this format ->
#         Doctor : 
#         Patient : 
#         With each line tagged according to the speaker. Both this should all be in separate lines according to the conversation. Return the transcription in a markdown format. \
#         Your summary should be in the form of a medical report and should have this format -> 
        
#         Todays Date : 
#         Patient Name : 
#         Patient DOB : 

#         Introduction : This should be a brief introduction of the patient and the reason for the visit (paragraph)
#         Medical History : This should include any past medical history that the patient has (paragraph)
#         Diagnosis : This should include the diagnosis of the patient (paragraph)
#         Treatment : This should include the treatment plan for the patient (paragraph)
        
#         Return the summary report in a markdown format. 

#         You might not find all the details in every conversation. In that case, just write NA. Don't try to make stuff up.
       
#         Your final response should include both the transcription and the summary as a JSON object with the keys "transcription" and "summary" respectively.
        
#         Both transcription and summary should be in a markdown format. Make sure they are in a markdown format. 
        
#         Stick to this format at all times!
# """
#     messages = [
#     (
#         "human",
#         [
#             {"type": "text", "text": new_prompt},
#             {"type": "input_audio", "input_audio": {"data": encoded_string, "format": "wav"}},
#         ],
#     )
#     ]

#     s = llm.invoke(messages).content

#     print(s)

#     json_str = s[s.find('{'):s.rfind("}")+1] #find the first { and the last } and get the string in between

    json_str = r"""{
  "transcription": "```markdown\nDoctor : Would it be okay if we ask you a few questions?\nPatient : Yeah, that's fine.\nDoctor : I'm just gonna verify your first and last name. If you could tell me your first name for me?\nPatient : It's Lori.\nDoctor : Alright, and last name?\nPatient : Smith.\nDoctor : And your birthdate?\nPatient : August 1st, 1974.\nDoctor : And what do you prefer to be called?\nPatient : You can just call me Lori.\nDoctor : It's nice to meet you.\nPatient : Thank you, it's nice to meet you.\nDoctor : So, Lori was admitted last night with an asthma exacerbation. During the night you had a couple of breathing treatments, correct?\nPatient : Yes.\nDoctor : Are you feeling better since the breathing treatment?\nPatient : Yeah.\nDoctor : They also gave her some prednisone as well during the night. So, the plan hopefully is to have you discharged later today if you continue to feel better. Do you have any questions for us so far?\nPatient : Am I getting any more treatments before I leave?\nDoctor : So they have another treatment scheduled in about an hour for you. If things get worse before then, you can give us a call and we'll certainly be back in and we can reassess the situation then. Do you mind if we listen to your lungs at all?\nPatient : No, go ahead, that's fine.\nDoctor : How's your breathing right now?\nPatient : It's better than it was.\nDoctor : Any pain at all anywhere?\nPatient : No.\nDoctor : I'm just gonna go ahead and take a listen here. If you could take some nice deep breaths for me, okay?\n```\n",
  "summary": "```markdown\nTodays Date : NA\nPatient Name : Lori Smith\nPatient DOB : August 1st, 1974\n\nIntroduction : Lori Smith was admitted last night due to an asthma exacerbation. She received a couple of breathing treatments during the night.\n\nMedical History : NA\n\nDiagnosis : Asthma exacerbation.\n\nTreatment : Lori was given breathing treatments and prednisone during the night. The plan is to discharge her later today if she continues to feel better. Another treatment is scheduled in about an hour, and her condition will be reassessed if it worsens.\n```\n"
}"""
    # try:
    result = json.loads(json_str)
    if "summary" in result and "transcription" in result:

        # t, s  = st.columns(2)
        # with t:
        with st.container(height = 500):
            st.subheader("Your Conversation:")
            transcription = result['transcription']
            st.markdown(transcription)
        with st.container(height = 300): 
            st.subheader("Report:")
            summary = result['summary']
            st.markdown(summary)
    else:
        st.error("Something went wrong. Please try again later.",icon="🚨")
    # except:
    #     st.error("Something went wrong. Please try again later.",icon="🚨")

