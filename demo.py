from dotenv import load_dotenv
load_dotenv() 

import streamlit as st 
import os 
from PIL import Image 
import google.generativeai as genai

genai.configure(api_key=os.getenv("google_api"))
model = genai.GenerativeModel('gemini-pro-vision')

def get_response_gemini(input, image_data , user_prompt):
    response = model.generate_content([input.image[0], user_prompt])
    return response.text

def input_image_details(uploaded_file): 
    if uploaded_file is not None: 
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            'mime_type':uploaded_file.type, 
            'data':bytes_data
        }]
        return image_parts
    else: 
        raise FileNotFoundError('file not uploaded!')

st.header('MultiLangugage Invoice extractor')

input = st.text_input('Input Prompt', key = 'input')
uploaded_file = st.file_uploader('Image', type = ['jpg','jpeg','png'])

if uploaded_file is not None:
    image = Image.open()
    st.image(image, caption = 'Uploaded File', use_coloumn_width = True) 

sub = st.button('Tell me about the invoice')
input_prompt = """ You are an expert in understanding invoices. We will upload an image as a invoice and you will 
have an answer any question based on the uploaded invoice message"""

if sub: 
    with st.spinner('wait your answer is being generated'): 
        image_data = input_image_details()
        response = get_response_gemini (input_prompt, image_data, input)
        st.subheader('The response is')
        st.text_area(label="", value=response, height= 500)

