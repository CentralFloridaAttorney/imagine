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
DEFAULT_IMG = Image.open("./templates/machette-1.png")

DEFAULT_IMG.thumbnail([512, 512])

prompt = "a family of real life rats having a picknick and eating with utensils, bokeh, photography –s 625 –q 2 –iw"
gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"
machete_prompt = "a handmade machete with a leather handle"


pipe.safety_checker = lambda images, clip_input: (images, False)

images = pipe(prompt=prompt, image=DEFAULT_IMG, strength=.4, guidance_scale=1.5, num_inference_steps=25).images

images[0].save('../data/jpeg/machete_v000.jpeg')
