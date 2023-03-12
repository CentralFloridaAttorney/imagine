import os

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from huggingface.tokenmaker.token_maker import TokenMaker

IMAGE_DIMENSIONS = (512, 512)
DEFAULT_COLOR = (128, 128, 255)
MODEL_ID = "CompVis/stable-diffusion-v1-4"
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker") + "/imagine/"
OUTPUT_DIR = BASE_PATH+"tokens/"


st.title("Make Token from Image")
item_image = st.file_uploader("Choose an image for the template", type="png")
if item_image is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(item_image.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    st.session_state.template_image = im_pil
    st.image(im_pil, channels="BGR")


def make_token():
    image = st.session_state.template_image
    top = st.session_state.top_text
    bottom = st.session_state.bottom_text
    token_maker = TokenMaker(_image_file=image,
                             _top_text=top,
                             _bottom_text=bottom)
    token_image = token_maker.get_token()
    token_image.save(fp=BASE_PATH)
    st.image(token_image)
    print("app_tokenmaker.make_token() done!")


def print_value():
    print("done")


st.session_state.top_text = 'xyxxy'

if "template_image" not in st.session_state:
    st.session_state['template_image'] = Image.new("RGB", IMAGE_DIMENSIONS, (128, 128, 255))

with st.sidebar.form(key='top_text_form'):
    text_input = st.text_input(label='Enter Top Text')
    st.session_state.top_text = text_input
    submit_button = st.form_submit_button(label='Submit', on_click=print_value)

with st.sidebar.form(key='bottom_text_form'):
    text_input = st.text_input(label='Enter Bottom Text')
    st.session_state.bottom_text = text_input
    submit_button = st.form_submit_button(label='Submit', on_click=print_value)

with st.sidebar.form(key="make_token_form"):
    submit_button = st.form_submit_button(label='Make Token', on_click=make_token)

st.text(st.session_state)
