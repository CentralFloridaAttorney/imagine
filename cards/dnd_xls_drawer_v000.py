import os
import random

import pandas
import torch
from diffusers import StableDiffusionPipeline

GENERATOR = torch.Generator(device="cpu").manual_seed(345)
styles = pandas.read_csv("../data/txt/artist_styles")
styles = styles.fillna("professional")
rnd_style = random.randint(0, len(styles))
model_id = "CompVis/stable-diffusion-v1-4"
device = "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to(device)
BASE_DIR = "../data/"
COLLECTION_NAME = "dnd/equipment/test"
# STYLE_LIST = [26, 29, 1267, 313, 940]
# STYLE_LIST = [233, 743, 124, 845, 1235, 657, 666]
# STYLE_LIST = [123, 145, 167, 188, 199]
# STYLE_LIST = [318, 329, 333, 347, 351, 369, 375, 388, 391]
# STYLE_LIST = [412, 427, 439, 444, 452, 468, 483, 499]
# STYLE_LIST = [516, 529, 537, 541, 559, 563, 571, 583, 591]   # indices for styles to be used
# STYLE_ROW = 8
LAST_INDEX = 2
INFERENCE_STEPS = 20
PROMPT_STRENGTH = 14.0
HEIGHT = 536
WIDTH = 688
data_file = pandas.read_excel(BASE_DIR+"xls/equipment_data.xls")
for row in range(LAST_INDEX, len(data_file), 1):
    equipment_name = data_file.iloc[row, 0]
    folder_name = equipment_name.replace(" ", "-")
    folder_name = equipment_name.replace(",", "-")
    COLLECTION_NAME = "dnd/equipment/" + folder_name
    # DO NOT CHANGE THE CODE BELOW
    if not os.path.exists(BASE_DIR + "/" + COLLECTION_NAME):
        os.makedirs(BASE_DIR + "/" + COLLECTION_NAME)
    prompt = data_file.iloc[row, 2]
    image = pipe(prompt, generator=GENERATOR, height=HEIGHT, width=WIDTH, num_inference_steps=INFERENCE_STEPS).images[0]
    image.save(BASE_DIR + "/" + COLLECTION_NAME + "/" + str(HEIGHT) + "_" + str(WIDTH) + "_" + str(rnd_style) + ".png")
