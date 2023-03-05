import os

import pandas
import torch
from diffusers import StableDiffusionPipeline
BASE_DIR = "../data/"
COLLECTION_NAME = "dnd/equipment/test"
# STYLE_LIST = [26, 29, 1267, 313, 940]
# STYLE_LIST = [233, 743, 124, 845, 1235, 657, 666]
# STYLE_LIST = [123, 145, 167, 188, 199]
# STYLE_LIST = [318, 329, 333, 347, 351, 369, 375, 388, 391]
# STYLE_LIST = [412, 427, 439, 444, 452, 468, 483, 499]
STYLE_LIST = [516, 529, 537, 541, 559, 563, 571, 583, 591]   # indices for styles to be used
STYLE_ROW = 1
LAST_INDEX = 1
INFERENCE_STEPS = 20
PROMPT_STRENGTH = 14.0
HEIGHT = 536
WIDTH = 688
test = "OD&D A (Mystara) 1989/08 Dawn of the Emperors [Book One: The Dungeon Master's Sourcebook] 58 Monster Zzonga-Bush Zzonga-Bush, bokeh, photography –s 625 –q 2 –iw"
data_file = pandas.read_excel(BASE_DIR+"xls/equipment_data.xls")
equipment_prompt = ""
for row in range(LAST_INDEX, len(data_file), 1):
    equipment_name = data_file.iloc[row, 0]
    equipment_name = equipment_name.replace(" ", "_")
    # COLLECTION_NAME = "dnd/equipment/test"
    COLLECTION_NAME = "dnd/equipment/" + equipment_name
    equipment_weight = data_file.iloc[row, 1]
    equipment_prompt = equipment_name
    # Edit the line below
    THIS_BASE_PROMPT = equipment_prompt
    # DO NOT CHANGE THE CODE BELOW
    THIS_BASE_PROMPT += "on a wooden table, bokeh, photography –s 625 –q 2 –iw"  # edit this_base_prompt
    GENERATOR = torch.Generator(device="cpu").manual_seed(345)
    styles = pandas.read_csv("../data/txt/artist_styles")
    styles = styles.fillna("professional")
    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe.safety_checker = lambda images, clip_input: (images, False)
    pipe = pipe.to(device)
    if not os.path.exists(BASE_DIR + "/" + COLLECTION_NAME):
        os.makedirs(BASE_DIR + "/" + COLLECTION_NAME)
    prompt = THIS_BASE_PROMPT + ", style " + styles.iloc[STYLE_LIST[STYLE_ROW], 0]
    image = pipe(prompt, generator=GENERATOR, height=HEIGHT, width=WIDTH, num_inference_steps=INFERENCE_STEPS).images[0]
    image.save(BASE_DIR + "/" + COLLECTION_NAME + "/" + str(HEIGHT) + "_" + str(WIDTH) + "_" + str(STYLE_LIST[STYLE_ROW]) + ".png")
