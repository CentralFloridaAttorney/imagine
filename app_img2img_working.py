import os

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

from huggingface.image2image_class import Img2Img

IMAGE_DIMENSIONS = (512, 512)
DEFAULT_COLOR = (128, 128, 255)
MODEL_ID = "CompVis/stable-diffusion-v1-4"
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker") + "/imagine/"


@st.cache_resource
def get_pipe():
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(MODEL_ID)
    pipe = pipe.to("cpu")
    pipe.safety_checker = lambda images, clip_input: (images, False)
    return pipe


def image2image():
    img2img = Img2Img(_pipe=get_pipe(), _prompt=st.session_state.text_input,
                      _template_img=st.session_state.template_image,
                      _new_file_path="./enhanced_image.png")
    st.image(img2img.get_enhanced_image())


uploaded_file = st.file_uploader("Choose an image for the template", type="png")

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    st.session_state.template_image = im_pil

    st.image(im_pil, channels="BGR")
st.session_state.text_input = 'xyxxy'

if "template_image" not in st.session_state:
    st.session_state['template_image'] = Image.new("RGB", IMAGE_DIMENSIONS, (128, 128, 255))

with st.form(key='my_form'):
    text_input = st.text_input(label='Enter a prompt')
    st.session_state.text_input = text_input
    submit_button = st.form_submit_button(label='Submit', on_click=image2image)

st.write(st.session_state)
