import cv2
import numpy as np
import streamlit as st
st.write(st.session_state)

if "token_name" not in st.session_state:
    st.session_state["token_name"] = "default"
name_input = st.text_input("Token Name")

if name_input:
    st.session_state['token_name'] = name_input
uploaded_file = st.file_uploader("Choose an image for the token", type="png")

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="BGR")



with st.form(key='my_form'):
    text_input = st.text_input(label='Enter Token Name')
    st.write(text_input)
    submit_button = st.form_submit_button(label='Submit')