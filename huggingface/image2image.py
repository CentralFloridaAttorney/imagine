from io import BytesIO

import iio
import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
device = "cpu"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to(device)
# let's download an initial image
#url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

#response = requests.get(url)
# image_file = iio.read('../data/comic/human_queen_1.png')
init_image = Image.open('../data/jpeg/waterskin.jpeg').convert("RGB")


init_image.thumbnail([512, 512])

prompt = "a leather pouch on a wooden table, bokeh, photography –s 625 –q 2 –iw"
gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"
pipe.safety_checker = lambda images, clip_input: (images, False)

images = pipe(prompt=prompt, image=init_image, strength=.6, guidance_scale=10.5).images

images[0].save('../data/jpeg/waterskin_new.png')