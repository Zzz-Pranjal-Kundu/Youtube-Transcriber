import streamlit as st
from dotenv import load_dotenv
load_dotenv() #Load all env variables
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi #responsible for getting idea of the video and extract the video transcript using the video url

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a Youtube Video summarizer, You will be taking the\
    transcript text and summarizing the entire video and providing\
    the important summary in points within 250 words. \
    Please provide the summary of the text given here: """

#get trancript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1] #https://www.youtube.com/watch?v=HFfXvfFe9F8 here content after = is video id
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript+=" "+i["text"]
        return transcript
    
    except Exception as e:
        raise e

#Summarization of transcript using google gemini
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

#STREAMLIT APP
st.title("Youtube video notes Extracter")
youtube_link=st.text_input("Enter YouTube Video Link: ")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)
    if(transcript_text):
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes:")
        st.write(summary)
st.write("Developed by Pranjal Kundu Graphic Era Hill University, Dehradun")