import time
from io import BytesIO

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
device = "cpu"
model_id = "CompVis/stable-diffusion-v1-4"
# model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)
pipe = pipe.to(device)
# let's download an initial image
#url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

#response = requests.get(url)
# image_file = iio.read('../data/comic/human_queen_1.png')
ORIG_FILE_PATH = '../data/dnd/coins/cp/copper-1-coin.png'
init_image = Image.open(ORIG_FILE_PATH).convert("RGB")
NEW_FILE_PATH = ORIG_FILE_PATH.replace(".png", "_enhanced_1.png")

# init_image.thumbnail([480, 640])

prompt = "an antique copper coin on a wooden table, bokeh, photography –s 625 –q 2 –iw"
gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"
pipe.safety_checker = lambda images, clip_input: (images, False)

image = pipe(prompt=prompt, image=init_image, strength=.2, guidance_scale=.9).images[0]
time.sleep(1)
image.save(NEW_FILE_PATH)
