import pandas
import torch
from diffusers import StableDiffusionPipeline
model_id = "CompVis/stable-diffusion-v1-4"

# model_id = "../models/my_diffuser"
CACHE_DIR = "/home/overlordx/PycharmProjects/imagine/models"
# model_id = "CompVis/stable-diffusion-v1-4"
# model_id = "../models/models--CompVis--stable-diffusion-v1-4/snapshots/3857c45b7d4e78b3ba0f39d4d7f50a2a05aa23d4/model_index.json"
# model_id = "../models/imagine_model/"
# device = "cuda"
device = "cpu"
styles = pandas.read_csv("../data/txt/artist_styles")
num_rows = len(styles)
# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)


pipe = StableDiffusionPipeline.from_pretrained(model_id, cache_dir=CACHE_DIR)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to(device)

# prompt = "a photo of an astronaut riding a horse on mars"
# prompt_2 = "female cleric athletic body type standing behind a skinny male magic user casting a fireball by Boris Vallejo, diablo, warcraft, Character design, dramatic, highly detailed, photorealistic, portrait, photo, photography –s 625 –q 2 –iw 3, sharp focus, art by John Collier and Krenz Cushart"
# prompt_3 = "medium shot side profile portrait photo of warrior princess in the style of megan fox, tribal panther make up, blue on red, looking away, serious eyes, 50mm portrait, photography, hard rim lighting photography –ar 2:3 –beta –upbeta"
prompt_4 = "a man and woman in the style of Thomas Kinkade,landscape art,painter"

BASE_PROMPT = "a man and woman in the style of "
styles = pandas.read_csv("../data/txt/artist_styles")
styles.fillna("detailed")
num_rows = len(styles)
# image dimensions must be a multiple of 8
for row in range (8, num_rows-1, 1):
    constructed_prompt = BASE_PROMPT
    row_value = styles.iloc[row]
    constructed_prompt = constructed_prompt + " " + row_value
    image = pipe(constructed_prompt, height=64, width=64).images[0]
    # image.save("man_woman_style_" + str(row) + ".png")
    image.save("../data/man_woman/man_woman_" + str(row) + ".png")


#image = pipe(prompt_4).images[0]

# image.save("man_woman_style_1.png")
# image.save("../data/man_woman/man_woman_style_2.png")
