import torch
from diffusers import StableDiffusionPipeline

model_id = "ogkalu/Comic-Diffusion"
# model_id = "../models/my_diffuser"
MODEL_DIR = "/home/overlordx/PycharmProjects/imagine/models"
# model_id = "my_diffuser"

# Comic Diffusion was trained to use the following artstyles
# charliebo artstyle
# holliemengert artstyle
# marioalberti artstyle
# pepelarraz artstyle
# andreasrocha artstyle
# jamesdaly artstyle


# model_id = "../models/models--CompVis--stable-diffusion-v1-4/snapshots/3857c45b7d4e78b3ba0f39d4d7f50a2a05aa23d4/model_index.json"
#model_id = "../models/imagine_model/"
# device = "cuda"
device = "cpu"

# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = StableDiffusionPipeline.from_pretrained(model_id, cache_dir=MODEL_DIR)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to(device)
generator = torch.Generator(device).manual_seed(0)

# prompt = "a photo of an astronaut riding a horse on mars"
# prompt_2 = "female cleric athletic body collection_name standing behind a skinny male magic user casting a fireball by Boris Vallejo, diablo, warcraft, Character design, dramatic, highly detailed, photorealistic, portrait, photo, photography –s 625 –q 2 –iw 3, sharp focus, art by John Collier and Krenz Cushart"
# prompt_3 = "medium shot side profile portrait photo of warrior princess in the style of megan fox, tribal panther make up, blue on red, looking away, serious eyes, 50mm portrait, photography, hard rim lighting photography –ar 2:3 –beta –upbeta"
character_jazz = "very complex hyper-maximalist overdetailed cinematic bar in Manhattan beautiful young megan fox with long blond hair, 5 drunk men with beer vibrant high contrast, by andrei riabovitchev, tomasz alen kopera,moleksandra shchaslyva, peter mohrbacher, ambient occlusion, volumetric lighting, glamorous, professional studio lighting, hyper detailed"
jazz_1 = "comic strip text above a beautiful young megan fox with a perfect body and super realistic skin on legs and neck and long blond hair, Classy Manhattan Bar Saturday Night Fever with Famous people, ambient occlusion, volumetric lighting, glamorous, professional studio lighting, hyper detailed"
bar_1 = "realistic full color cinematic interior design, open plan, classy uptown bar, full wall of liquor behind a long wood bar, a beautiful young megan fox with a perfect body, bar stools, happy beautiful young people with alcoholic drinks in their hands, wooden floor, high ceiling, large steel windows viewing a city, glamorous, professional studio lighting"
bar_2 = "realistic full color cinematic a beautiful young megan fox with a perfect body, interior design, open plan, classy uptown bar, full wall of liquor behind a long wood bar, bar stools, happy beautiful young people with alcoholic drinks in their hands, wooden floor, high ceiling, large steel windows viewing a city, glamorous, professional studio lighting"
bar_3 = "a beautiful megan fox with perfect face crowded with people uptown bar full wall of liquor long wood bar with bar stools wooden floor high ceiling, verb people laughing and drinking, mood energetic, realistic skin on people, photography style long exposure, 4k"
ukraine_1 = "map of ukraine showing red in the areas of russian invasion and yellow showing areas of ukraine resistance, kyiv marked on the map, , –s 625 –q 2 –iw 3"
jazz_2 = "portrait of A  Beautiful WOMAN=Nikole Kidman: 50 AND Megan Fox: 50, street corner, new orleans, burbon street, mardi gras, holliemengert artstyle: 10, Detail ultrarealistic: 50"
demo_comic_1 = "f7u12 rage comic about CIA conspiracies"
prompt = "realistic photograph of a real Goddess Aphrodite wearing a dress in the style of Domenico Dolce and Stefano Gabbana, seductive mood, photographic quality, "
prompt += " futuristic, bladerunner, style George Lucas, speculative fiction film, "
prompt += " 24mm portrait photography, hard rim lighting photography--beta --ar 2:3  --beta --upbeta"

image = pipe(prompt, generator=generator, num_inference_steps=75).images[0]

image.save("../data/comic/future_1.png")
