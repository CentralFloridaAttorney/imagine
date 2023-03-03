import torch
from diffusers import StableDiffusionPipeline

# model_id = "ogkalu/Comic-Diffusion"
model_id = "CompVis/stable-diffusion-v1-4"

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

# prompt = "a highly detailed epic cinematic concept art CG render digital painting artwork costume design: young Megan Fox as a well-kept neat student in Hogwart's School Robes and  magic wand, reading a book."
# prompt += " 24mm portrait photography, hard rim lighting photography--beta --ar 2:3  --beta --upbeta"
# prompt += "octane render, excellent composition, cinematic atmosphere, dynamic dramatic cinematic lighting, aesthetic, very inspirational, arthouse"
warrior_prompt = "medium shot looking into camera, portrait photo of the Wildwood Ranger Chief, warhammer, serious eyes, 50mm portrait, photography, hard rim lighting photography –ar 2:3 –beta –upbeta"
warroir_prompt_2 = "full length photo of dwayne johnson as a warrior, highly detailed, 4 k, hdr, highly detailed, sharp focus, high resolution, award – winning photo"
gandalf_prompt = "ultrarealistic, (real demon, Lord of the Rings, cinematic lighting, award winning photo, no color, 80mm lense –beta –upbeta –upbeta"
cozy_room = "the living room of a cozy wooden house with a fireplace, at night, interior design, d & d concept art, d & d wallpaper, warm, digital art. art by james gurney and larry elmore."

knight = "redshift style, painted portrait of a paladin, masculine, mature, handsome, upper body, grey and silver, fantasy, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by gaston bussiere and alphonse mucha"
bear = "anthropomorphic, half man half asian black bear, black bear samurai, Moon Bear Samurai, epic, samurai, stunning 3d render inspired art by Renato muccillo and Andreas Rocha and Johanna Rupprecht + symmetry + natural volumetric lighting, 8k octane beautifully detailed render, post-processing, highly detailed, intricate complexity, epic composition, magical atmosphere, cinematic lighting + masterpiece, trending on artstation"
castle = "a medieval fortress overlooking a cliff with a glowing night sky from an upward angle, party of orcs standing guard, style arcane tv series, style of Harry Potter, trending on art station"
castle_goth = "A epic fantasy portrait of a cute goth woman, castle setting, horror movie lightning, intricate, elegant, highly detailed, digital painting, artstation, concept art, matte, sharp focus, illustration, art by Artgerm and Greg Rutkowski and Alphonse Mucha"
image = pipe(castle, height=512, width=512, generator=generator, num_inference_steps=50).images[0]

image.save("../data/comic_dnd_2/party_20.png")
