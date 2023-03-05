from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
from transformers import AutoModel
MODEL_PATH = "/home/overlordx/PycharmProjects/imagine/models/models--my_diffuser/safety_checker"
prompt = ("fps radar-topview game map, flat shading, soft shadows, global illumination")

# model_id = "Kaludi/CSGO-Improved-Radar-Top-View-Map-Layouts"
# pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = AutoModel.from_pretrained(MODEL_PATH)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cpu")
# model_id = "../models/my_diffuser"
# MODEL_DIR = "/home/overlordx/PycharmProjects/imagine/models"
# model_id = "my_diffuser"
# new_roberta = AutoModel.from_pretrained('./saved')"

image = pipe(prompt, num_inference_steps=30).images[0]

image.save("./result.jpg")
