import os
import gradio as gr

import cv2
import numpy as np
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

from huggingface.img2img import Img2Img

IMAGE_DIMENSIONS = (512, 512)
DEFAULT_COLOR = (128, 128, 255)
MODEL_ID = "CompVis/stable-diffusion-v1-4"
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker") + "/imagine/"


def get_pipe():
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(MODEL_ID)
    pipe = pipe.to("cpu")
    pipe.safety_checker = lambda images, clip_input: (images, False)
    return pipe


def image2image(_prompt, _image):
    img2img = Img2Img(_template_img=_image,
                      _prompt=_prompt)
    image_path = img2img.get_enhanced_image()
    return image_path


with gr.Blocks() as demo:
    BASE_DIR = './data/dnd/coins/cp/'
    images = []

    for path in os.listdir(BASE_DIR):
        if os.path.isfile(os.path.join(BASE_DIR, path)):
            if path.endswith(".png"):
                images.append(BASE_PATH+"data/dnd/coins/cp/" + path)
    print(images)


    with gr.Row():
        gr.Gallery(value=images)
    with gr.Row():
        text1 = gr.Textbox(label="t1")
        slider2 = gr.Textbox(label="s2")
        drop3 = gr.Dropdown(["a", "b", "c"], label="d3")
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            prompt = gr.Textbox(label="Prompt")
            text2 = gr.Textbox(label="prompt 2")
            inbtw = gr.Button("Between")
            text4 = gr.Textbox(label="prompt 1")
            text5 = gr.Textbox(label="prompt 2")
        with gr.Column(scale=2, min_width=600):
            img1 = gr.Image()
            img2 = gr.Image()

            btn = gr.Button("Generate Image").style(full_width=True)
            btn.click(image2image, inputs=[prompt, img1], outputs=[img2])



demo.launch()
