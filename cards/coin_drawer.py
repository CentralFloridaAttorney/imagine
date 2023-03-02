import os
import random

import pandas
import torch
from diffusers import StableDiffusionPipeline
MODEL_ID = "CompVis/stable-diffusion-v1-4"
DEVICE = "cpu"
BASE_DIR = "../data/"
COLLECTION_NAME = "dnd/coins/"
LAST_INDEX = 0
INFERENCE_STEPS = 25
PROMPT_STRENGTH = 10.0
# 1 inch at 300dpi
HEIGHT = 536
WIDTH = 688

# coin_data has the following columns:
# name, file_name, type, quantity, description, equivalent, prompt
COIN_DATA = pandas.read_excel(BASE_DIR + "xls/coin_data.xls")
GENERATOR = torch.Generator(device=DEVICE).manual_seed(480984)
styles = pandas.read_csv("../data/txt/artist_styles")
styles = styles.fillna("professional")
rnd_style = random.randint(0, len(styles))
pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to(DEVICE)
for row in range(LAST_INDEX, len(COIN_DATA), 1):
    coin_type = COIN_DATA.iloc[row, 2]
    if not os.path.exists(BASE_DIR + "/" + COLLECTION_NAME + "/" + coin_type):
        os.makedirs(BASE_DIR + "/" + COLLECTION_NAME + "/" + coin_type)
    prompt = COIN_DATA.iloc[row, 6]
    image = pipe(prompt, generator=GENERATOR, height=HEIGHT, width=WIDTH, num_inference_steps=INFERENCE_STEPS).images[0]
    file_name = COIN_DATA.iloc[row, 1]
    image.save(BASE_DIR + "/" + COLLECTION_NAME + "/" + coin_type + "/" + file_name + "_" + str(HEIGHT) + "_" + str(WIDTH) + "_" + str(rnd_style) + ".png")
