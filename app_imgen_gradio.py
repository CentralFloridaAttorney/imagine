import os

import gradio as gr
from diffusers import StableDiffusionImg2ImgPipeline

from huggingface.image_generator import ImageGenerator
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


def update_gallery():
    pass


def image2image(_prompt, _image):
    img2img = Img2Img(_template_img=_image,
                      _prompt=_prompt)
    image_path = img2img.get_enhanced_image()
    return image_path


def generate_image():
    _prompt = "male halfling bard, scar on face,paying a guitar, in a field , national geographic, portrait, photo, photography –s 625 –q 2 –iw 3"
    collection_name = "dnd/monsters"
    file_name = "new-bard-1"
    card_image_generator = ImageGenerator(_prompt=prompt.value, _collection_name=collection.value, _file_name=file_name)
    image_path = card_image_generator.get_image(_iterations=20, _style=245, _seed=639)
    return image_path


with gr.Blocks() as demo:
    with gr.Row():
        text1 = gr.Textbox(label="t1")
        slider2 = gr.Textbox(label="s2")
        drop3 = gr.Dropdown(["a", "b", "c"], label="d3")
    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            prompt = gr.Textbox(label="Prompt")
            collection = gr.Textbox(label="Collection", placeholder="data/dnd/classes/fighter")

        with gr.Column(scale=2, min_width=600):
            img1 = gr.Image()
            img2 = gr.Image()
            btn = gr.Button("Generate Image").style(full_width=True)
            btn.click(generate_image, inputs=[prompt], outputs=[img2])

demo.launch()
