import importlib
import os
import pathlib
import time
from io import BytesIO
import numpy as np
import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
from numpy import ndarray

# load the pipeline
device = "cpu"
model_id = "CompVis/stable-diffusion-v1-4"
# BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker")+"/imagine/"
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker") + "/imagine/"


class Img2Img:
    def __init__(self, _template_img, _prompt, _new_file_path=None, _pipe=None):
        if type(_template_img) is str:
            image_path = BASE_PATH + _template_img
            self.template_img = Image.open(image_path).convert("RGB")
        elif type(_template_img) is ndarray:
            self.template_img = self.numpy2pil(_template_img)
        self.prompt = _prompt
        if _pipe is None:
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)
            self.pipe = self.pipe.to(device)
            self.pipe.safety_checker = lambda images, clip_input: (images, False)
        else:
            self.pipe = _pipe
        if _new_file_path is None:
            self.NEW_FILE_PATH = BASE_PATH+"png/img2img_enhanced.png"
        else:
            self.NEW_FILE_PATH = BASE_PATH+_new_file_path
        # init_image.thumbnail([480, 640])
        prompt = "an antique copper coin on a wooden table, bokeh, photography –s 625 –q 2 –iw"
        gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"


    def get_enhanced_image(self):
        image = self.pipe(prompt=self.prompt, image=self.template_img, strength=.9, guidance_scale=.1).images[0]
        time.sleep(1)
        image.save(self.NEW_FILE_PATH)
        return self.NEW_FILE_PATH

    def numpy2pil(self, np_array: np.ndarray) -> Image:
        """
        Convert an HxWx3 numpy array into an RGB Image
        """

        assert_msg = 'Input shall be a HxWx3 ndarray'
        assert isinstance(np_array, np.ndarray), assert_msg
        assert len(np_array.shape) == 3, assert_msg
        assert np_array.shape[2] == 3, assert_msg

        img = Image.fromarray(np_array, 'RGB')
        return img

def main():
    prompt = "a copper coin on a wooden table, concept art, 8k"
    image_path = "data/dnd/coins/cp/copper-1-coin.png"
    output_path = "data/dnd/coins/cp/copper-1-coin_enhanced.png"

    # image = Image.open(BASE_PATH+"dnd/armor/knight-armor.jpg")
    img2img = Img2Img(_template_img=image_path,
                          _new_file_path=output_path,
                          _prompt=prompt)
    new_image_path = img2img.get_enhanced_image()
    print(new_image_path)
    # image.save("./img2img_xyzzy.png")

if __name__ == "__main__":
    main()
