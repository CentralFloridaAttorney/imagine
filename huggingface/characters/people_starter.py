from diffusers import StableDiffusionPipeline

pipeline = StableDiffusionPipeline.from_pretrained('baruga/ancient-maps')
image = pipeline("detailed top-down professional map of ancient scottish hamlet, ").images[0]
image.save("./xyzzy_hamlet.png")
