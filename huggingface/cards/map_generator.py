from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch

prompt = (
"fps radar-topview game map, flat shading, soft shadows, global illumination")

model_id = "Kaludi/CSGO-Improved-Radar-Top-View-Map-Layouts"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

image = pipe(prompt, num_inference_steps=30).images[0]

image.save("./result.jpg")
