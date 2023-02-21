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
init_image = Image.open('../data/paintings/painting_1.png').convert("RGB")


init_image.thumbnail([512, 512])

prompt = "A realistic photograph of a crowded Manhattan Park"

images = pipe(prompt=prompt, image=init_image, strength=.6, guidance_scale=10.5).images
pipe.safety_checker = lambda images, clip_input: (images, False)

images[0].save("../data/paintings/painting_1a.png")