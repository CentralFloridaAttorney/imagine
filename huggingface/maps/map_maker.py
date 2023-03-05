from diffusers import StableDiffusionPipeline

pipeline = StableDiffusionPipeline.from_pretrained('baruga/ancient-maps')
map_1 = [
    "a top down map of a medium town, streets are in grid pattern, large empty parking lots connected to a major highway"]
map_2 = [
    'vintage rpg map, satellite view of a small tropical island, 3 encounter locations connected by a wooded trail,'
    'by Gustave Doré and Edmund Dulac, black and white, trending artstation, vector graphics:1.6',
    'tilt-shift:-0.5']

FILE_NAME = "map_2.png"
image = pipeline(prompt=map_2,
                 num_inference_steps=10,
                 height=512,
                 width=512).images[0]
image.save("./1_" + FILE_NAME)
image.save(".,/data/2_" + FILE_NAME)
image.save(".,/../3_" + FILE_NAME)
image.save("../../data/4_" + FILE_NAME)
