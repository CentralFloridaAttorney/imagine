import cv2
import streamlit as st
import numpy as np


uploaded_file = st.file_uploader("Choose an image for the token", type="png")

if uploaded_file is not None:
	# Convert the file to an opencv image.
	file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
	opencv_image = cv2.imdecode(file_bytes, 1)

	# Now do something with the image! For example, let's display it:
	st.image(opencv_image, channels="BGR")


st.session_state.text_input = 'xyxxy'

with st.form(key='my_form'):
	text_input = st.text_input(label='Enter some text')
	st.session_state.text_input = text_input
	submit_button = st.form_submit_button(label='Submit')

st.write(st.session_state)
