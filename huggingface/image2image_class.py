import os
import time
from io import BytesIO

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
device = "cpu"
model_id = "CompVis/stable-diffusion-v1-4"
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker")+"/imagine/"


class Img2Img:
    def __init__(self, _template_img, _prompt, _new_file_path, _pipe=None):
        self.template_img = _template_img
        self.prompt = _prompt
        if _pipe is None:
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)
            self.pipe = self.pipe.to(device)
            self.pipe.safety_checker = lambda images, clip_input: (images, False)
        else:
            self.pipe = _pipe
        # let's download an initial image
        #url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

        #response = requests.get(url)
        # image_file = iio.read('../data/comic/human_queen_1.png')
        # ORIG_FILE_PATH = '../data/dnd/coins/cp/copper-1-coin.png'
        # self.ORIG_FILE_PATH = BASE_PATH+_template_img_path
        # init_image = Image.open(self.ORIG_FILE_PATH).convert("RGB")
        # self.NEW_FILE_PATH = self.ORIG_FILE_PATH.replace(".png", "_enhanced_1.png")
        self.NEW_FILE_PATH = BASE_PATH+_new_file_path
        # init_image.thumbnail([480, 640])

        prompt = "an antique copper coin on a wooden table, bokeh, photography –s 625 –q 2 –iw"
        gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"


    def get_enhanced_image(self):
        image = self.pipe(prompt=self.prompt, image=self.template_img, strength=.9, guidance_scale=.1).images[0]
        time.sleep(1)
        image.save(self.NEW_FILE_PATH)
        return image

def main():
    prompt = "a copper coin on a wooden table, concept art, 8k"
    output_path = "data/dnd/coins/cp/copper-1-coin_enhanced.png"
    image = Image.open(BASE_PATH+"data/dnd/coins/cp/copper-1-coin.png")
    image2image = Img2Img(_template_img=image,
                          _new_file_path=output_path,
                          _prompt=prompt)


if __name__ == "__main__":
    main()
