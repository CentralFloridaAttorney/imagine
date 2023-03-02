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
LAST_INDEX = 4
INFERENCE_STEPS = 20
PROMPT_STRENGTH = 14.0
HEIGHT = 536
WIDTH = 688
# BASE_PROMPT = "centered gold coin, dungeons and dragons, world of warcraft, RAW photo, *subject*, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3"
# gold_coin = "transparent background, Photorealistic image of a gold coin with Dragon stamped on the face of the coin, elvish language lettering along edge of coin. Hyperrealistic octane render HD highly detailed 8k. --beta --upbeta --upbeta"
# gold_coin_2 = "Photorealistic image of a gold coin with Dragon stamped on the face of the coin, 8K, --beta --upbeta --upbeta"
# silver_coin_1 = "Photorealistic image, a silver coin, clean,RAW photo, *subject*, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3"
# BASE_PROMPT = "A realistic image of 2 people in love, mood cheerful,"
# BASE_PROMPT = "A realistic image of a man and woman in love, mood cheerful,"
# silver_coin_2 = "Photorealistic Silver coin with bust of Queen Elizabeth in the center, clean, RAW photo,"
# copper_coin_1 = "Realistic photograph of a Worn copper coin, RAW photo, *subject*, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3"
# torch_1 = "a wooden torch on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# block_tackle = "block and tackle system with two or more pulleys threaded by ropes or cables on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# backpack = "sturdy Leather Backpack, bokeh, photography –s 625 –q 2 –iw"
# mess_kit = "detailed mess kit displayed on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# tinderbox = "an antique tinderbox displayed on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# bedroll = "bedroll for camping on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# clothes = "Medieval peasant clothing, Pants, shirt, shoes, socks, underwear, belt, clothes folded on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# waterskin = "Medieval water flask cover in a leather, on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# rations = " small amount of cheese, dried meat, and Manchet bread on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# quiver = "highly detailed ceremonial quiver full of arrows on a wooden table, bokeh, photography –s 625 –q 2 –iw"
# rope = "hemp rope in a coil on a wooden table, bokeh, photography –s 625 –q 2 –iw"
test = "OD&D A (Mystara) 1989/08 Dawn of the Emperors [Book One: The Dungeon Master's Sourcebook] 58 Monster Zzonga-Bush Zzonga-Bush, bokeh, photography –s 625 –q 2 –iw"
data_file = pandas.read_excel(BASE_DIR+"xls/equipment_data.xls")
print("read xls")
equipment_name = data_file.iloc[0, 0]
equipment_name = equipment_name.replace(" ", "_")
# COLLECTION_NAME = "dnd/equipment/test"
COLLECTION_NAME = "dnd/equipment/" + equipment_name

equipment_weight = data_file.iloc[0, 1]
equipment_prompt = equipment_name + " " + str(equipment_weight)

equipment_prompt += "on a wooden table, bokeh, photography –s 625 –q 2 –iw"  # edit this_base_prompt
THIS_BASE_PROMPT = equipment_prompt

# DO NOT CHANGE THE CODE BELOW
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
for row_num in range(LAST_INDEX, len(STYLE_LIST), 1):
    prompt = THIS_BASE_PROMPT + ", style " + styles.iloc[STYLE_LIST[row_num], 0]
    image = pipe(prompt, generator=GENERATOR, height=HEIGHT, width=WIDTH, num_inference_steps=INFERENCE_STEPS).images[0]
    image.save(BASE_DIR + "/" + COLLECTION_NAME + "/" + str(HEIGHT) + "_" + str(WIDTH) + "_" + str(STYLE_LIST[row_num]) + ".png")
