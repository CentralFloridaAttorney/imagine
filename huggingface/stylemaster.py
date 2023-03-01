import os

import pandas
import torch
from diffusers import StableDiffusionPipeline

# image variables
default_pre_modifiers = "concept art of"
default_main_subject = "Basic long sword, professional, "
default_post_modifiers = ", highly detailed, Hyper realistic 4d model, HDR, UHD, 64K"
# path variables
default_collection = "equipment/short_sword/"
default_base_dir = "../data/dnd/"
# model variables
MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cpu"


class StyleMaster:
    def __init__(self, _base_dir=default_base_dir, _collection_name=default_collection,
                 _main_subject=default_main_subject, _pre_modifiers=default_pre_modifiers,
                 _post_modifiers=default_post_modifiers):
        self.BASE_PROMPT = _pre_modifiers + " *" + _main_subject + " subject*, " + _post_modifiers
        self.BASE_DIR = _base_dir
        self.COLLECTION_NAME = _collection_name
        self.BASE_PATH = _base_dir + _collection_name + _main_subject
        if not os.path.exists(self.BASE_PATH):
            os.makedirs(self.BASE_PATH)
        self.pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID)
        self.pipe.safety_checker = lambda images, clip_input: (images, False)
        self.pipe = self.pipe.to(DEVICE)
        style_csv = pandas.read_csv("../data/txt/artist_styles")
        self.STYLE_LIST = style_csv["Artist"].to_list()
        self.INFERENCE_STEPS = 50
        self.PROMPT_STRENGTH = 25.0
        self.HEIGHT = 512
        self.WIDTH = 512

    def get_image(self, _style_number=145, _seed=1000):
        prompt = self.BASE_PROMPT + ", style " + self.STYLE_LIST[_style_number]

        generator = torch.Generator(device=DEVICE).manual_seed(_seed)
        image = self.pipe(prompt, generator=generator, height=self.HEIGHT, width=self.WIDTH,
                          num_inference_steps=self.INFERENCE_STEPS,
                          guidance_scale=self.PROMPT_STRENGTH).images[0]
        image.save(
            self.BASE_PATH + "/" + str(self.HEIGHT) + "_" + str(self.WIDTH) + "_" + str(_style_number) + ".png")
        return image


def main():
    style_master = StyleMaster(_main_subject="basic long sword")
    image = style_master.get_image(_style_number=444)
    image = style_master.get_image(_style_number=555)

    print("main done!")


if __name__ == "__main__":
    main()
