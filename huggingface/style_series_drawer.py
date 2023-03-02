import pandas
import torch
from diffusers import StableDiffusionPipeline
LAST_INDEX = 300
INFERENCE_STEPS = 25
PROMPT_STRENGTH = 12.0
BASE_PROMPT = "a battle between good and evil, religion, RAW photo, *subject*, (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3, "
# BASE_PROMPT = "A realistic image of 2 people in love, mood cheerful,"
# BASE_PROMPT = "A realistic image of a man and woman in love, mood cheerful,"
COLLECTION_NAME = "god_devil"
HEIGHT = 512
WIDTH = 512
GENERATOR = torch.Generator(device="cpu").manual_seed(-1)
styles = pandas.read_csv("../data/txt/artist_styles")
styles = styles.fillna("professional")
BASE_DIR = "../data/"
model_id = "CompVis/stable-diffusion-v1-4"
device = "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to(device)
for row_num in range(LAST_INDEX, len(styles), 1):
    prompt = BASE_PROMPT
    for column_num in range (0, len(styles.loc[row_num]), 1):
        new_part = ", " + styles.iloc[row_num, column_num]
        prompt += new_part
    image = pipe(prompt, generator=GENERATOR, height=HEIGHT, width=WIDTH, num_inference_steps=INFERENCE_STEPS, guidance_scale=PROMPT_STRENGTH).images[0]
    image.save(BASE_DIR + COLLECTION_NAME + "/" + COLLECTION_NAME + "_" + str(HEIGHT) + "_" + str(WIDTH) + "_" + str(row_num) + ".png")
