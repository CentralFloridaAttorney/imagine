from diffusers import StableDiffusionPipeline

# model_id = "CompVis/stable-diffusion-v1-4"
# model_id = "../models/models--CompVis--stable-diffusion-v1-4/snapshots/3857c45b7d4e78b3ba0f39d4d7f50a2a05aa23d4/model_index.json"
model_id = "../models/imagine_model/"
# device = "cuda"
device = "cpu"

# pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.safety_checker = lambda images, clip_input: (images, False)
pipe = pipe.to(device)

# prompt = "a photo of an astronaut riding a horse on mars"
# prompt_2 = "female cleric athletic body type standing behind a skinny male magic user casting a fireball by Boris Vallejo, diablo, warcraft, Character design, dramatic, highly detailed, photorealistic, portrait, photo, photography –s 625 –q 2 –iw 3, sharp focus, art by John Collier and Krenz Cushart"
# prompt_3 = "medium shot side profile portrait photo of warrior princess in the style of megan fox, tribal panther make up, blue on red, looking away, serious eyes, 50mm portrait, photography, hard rim lighting photography –ar 2:3 –beta –upbeta"
character_jazz = "very complex hyper-maximalist overdetailed cinematic bar in Manhattan beautiful young megan fox with long blond hair, 5 drunk men with beer vibrant high contrast, by andrei riabovitchev, tomasz alen kopera,moleksandra shchaslyva, peter mohrbacher, ambient occlusion, volumetric lighting, glamorous, professional studio lighting, hyper detailed"
jazz_1 = "comic strip text above a beautiful young megan fox with a perfect body and super realistic skin on legs and neck and long blond hair, Classy Manhattan Bar Saturday Night Fever with Famous people, ambient occlusion, volumetric lighting, glamorous, professional studio lighting, hyper detailed"
bar_1 = "realistic full color cinematic interior design, open plan, classy uptown bar, full wall of liquor behind a long wood bar, a beautiful young megan fox with a perfect body, bar stools, happy beautiful young people with alcoholic drinks in their hands, wooden floor, high ceiling, large steel windows viewing a city, glamorous, professional studio lighting"
bar_2 = "realistic full color cinematic a beautiful young megan fox with a perfect body, interior design, open plan, classy uptown bar, full wall of liquor behind a long wood bar, bar stools, happy beautiful young people with alcoholic drinks in their hands, wooden floor, high ceiling, large steel windows viewing a city, glamorous, professional studio lighting"
bar_3 = "a beautiful megan fox with perfect face crowded with people uptown bar full wall of liquor long wood bar with bar stools wooden floor high ceiling, verb people laughing and drinking, mood energetic, realistic skin on people, photography style long exposure, 4k"
ukraine_1 = "map of ukraine showing red in the areas of russian invasion and yellow showing areas of ukraine resistance, kyiv marked on the map, , –s 625 –q 2 –iw 3"

# prompt = "anya taylor-joy, gal gadot, drunk dancing with nicole kidman, megan fox, beads, mardi gras, burbon street, street corner, Andy Warhol artstyle,portrait,pop art"
sorcerer_2 = "Photo of real life Sorcerer wearing robes and driving a harley motorcycle with a leather jacket short hair, leather jacket, new orleans, burbon street, warcraft, diablo, movie poster style"
# prompt = "Photo of real life Sorcerer, sitting on a harley motorcycle at an intersection with a red light, wearing jeans, leather jacket, short hair, metarie, louisiana, "
# prompt = "realistic photograph of a beautiful, Megan Fox: 50, Nicole Kidman: 50, perfect body realistic natural skin, sexy bikini, large natural breasts, standing on the beach looking at the sun rising in the distance, movie poster"
# prompt = "realistic photograph very complex hyper-maximalist overdetailed cinematic tribal darkfantasy portrait beautiful young dwarf queen goddess, "
# prompt = "A portrait of crowded manhattan park, many boys and girls playing frisby in the park and a person in the style Yoshitaka Amano,character designer, and the style of Thomas Kinkade,landscape art,painter, "
prompt = " A realistic photograph, country church surrounded by pine trees, automobiles parked under pine trees, background is a graveyard, 1955 Mississippi"
prompt += " rustic, families going to church, 1950's style clothing, wearing sunday best clothes, style tilt-shift, professional, hyper detailed, HDR, UHD, 8K"
# prompt += " 24mm portrait photography, studio lighting photography--beta --ar 2:3  --beta --upbeta"

image = pipe(prompt, num_inference_steps=50, guidance_scale=11.0).images[0]


image.save("../data/paintings/church_1.png")
