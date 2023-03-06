from io import BytesIO

import torch
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
device = "cpu"
# MODEL_ID = "runwayml/stable-diffusion-v1-5"
MODEL_ID = "CompVis/stable-diffusion-v1-4"
STARTING_IMAGE_PATH = "../../data/png/rations-emergency-6.png"
ENHANCED_IMAGE_PATH_PNG = STARTING_IMAGE_PATH.replace(".png", "_enhanced.png")

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(MODEL_ID)
pipe = pipe.to(device)
# let's download an initial image
#url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

#response = requests.get(url)
# image_file = iio.read('../data/comic/human_queen_1.png')
# init_image = Image.open('../data/jpeg/waterskin.jpeg').convert("RGB")
# DEFAULT_IMG = Image.open("../data/dnd/monsters/level1/rat-1_536_688_613.png")
DEFAULT_IMG = Image.open(STARTING_IMAGE_PATH).convert("RGB")

_height=536

_width=688
if DEFAULT_IMG.height != _height or DEFAULT_IMG.width != _width:
    DEFAULT_IMG.thumbnail([_width, _height])

prompt = "a family of real life rats having a picknick and eating with utensils, bokeh, photography –s 625 –q 2 –iw"
gandalf_prompt = "ultrarealistic, (old Bilbo Baggins with evil eyes, Lord of the Rings), dramatic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"
machete_prompt = "a sword attacking an evil rat, bokeh, photography –s 625 –q 2 –iw"
game_token = "a magical coin with lettering, highly detailed, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha"
game_token_2 = "a magical coin with lettering, highly detailed, concept art, smooth, sharp focus, bokeh, photography –s 625 –q 2 –iw"
coin_1 = "ultra detailed photograph of real life Psycho Bunny, bokeh, photography –s 625 –q 2 –iw"
evil_rat = "a sword attacking an evil rat , deep focus, d & d, fantasy, intricate, elegant, highly detailed, digital painting, artstation, concept art, matte, sharp focus, illustration, hearthstone, art by artgerm and greg rutkowski and alphonse mucha"
sword_rat_bane_1 = "A magical sword that does bonus damage to rats  in a magical forest, concept art, by Greg Rutkowski and John Collier and Albert Aublet and Krenz Cushart and Artem Demura and Alphonse Mucha, featured on cgsociety"
river_house = "a house next to a small stream  near a mountain, rocky roads, and early evening, with stars in the sky, realistic style, 4k!!!, octane render, trending on artstation, art by Artgerm"
jackal_attacking = "A jackal sttacking a small child playing on a dirt road with trees in the diatance  early in the morning light. there are neon signs. eerie, concept art. render. unreal engine. artstation. mood lighting. vfx. a fantasy digital painting by greg rutkowski, gaston bussiere, craig mullins, j. c. leyendecker."
emergency_rations_1 = "an air drop of food falling from an Amazon Blimp flying over snow capped mountains, bismuth black diamond, by Tooth Wu and wlop and beeple. a highly detailed epic cinematic concept art CG render digital painting artwork scene. By Greg Rutkowski, Ilya Kuvshinov, WLOP,"
steampunk_flying_food_1 = "a basket of food hovering above mountains with angles in the sky, cinematic lighting, insanely detailed, d & d, fantasy, intricate, elegant, highly detailed, digital painting, artstation, concept art, matte, sharp focus, illustration, hearthstone, art by artgerm and greg rutkowski"

pipe.safety_checker = lambda images, clip_input: (images, False)

images = pipe(prompt=steampunk_flying_food_1, image=DEFAULT_IMG, strength=.6, guidance_scale=.1, num_inference_steps=36).images

images[0].save(ENHANCED_IMAGE_PATH_PNG)
