from io import BytesIO

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
device = "cpu"
# MODEL_ID = "runwayml/stable-diffusion-v1-5"
MODEL_ID = "CompVis/stable-diffusion-v1-4"

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(MODEL_ID)
pipe = pipe.to(device)
# let's download an initial image
#url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

#response = requests.get(url)
# image_file = iio.read('../data/comic/human_queen_1.png')
# init_image = Image.open('../data/jpeg/waterskin.jpeg').convert("RGB")
# DEFAULT_IMG = Image.open("../data/dnd/monsters/level1/rat-1_536_688_613.png")
DEFAULT_IMG = Image.open("./templates/coin-medium-2.png").convert("RGB")

_height=536

_width=688
DEFAULT_IMG.thumbnail([_width, _height])

prompt = "a family of real life rats having a picknick and eating with utensils, bokeh, photography –s 625 –q 2 –iw"
gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"
machete_prompt = "a  highly detailed sword attacking an giant evil rat with glowing eyes, bokeh, photography –s 625 –q 2 –iw"
game_token = "a magical coin with lettering, highly detailed, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha"
game_token_2 = "a magical coin with lettering, highly detailed, concept art, smooth, sharp focus, bokeh, photography –s 625 –q 2 –iw"
coin_1 = "realistc photograph of an ancient coin with a hole in the middle   surrounded by flowing flowers. mountains and trees. professional digital art, artstation, photorealistic, octane render, unreal engine 5, 8k, concept art, cinematographic, color redshift render, digital Art, Smooth gradients, depth of field, shot on Canon Camera"
pipe.safety_checker = lambda images, clip_input: (images, False)

images = pipe(prompt=coin_1, image=DEFAULT_IMG, strength=.6, guidance_scale=25.5, num_inference_steps=35).images

images[0].save('./cards/coin_medium_3.jpeg')
