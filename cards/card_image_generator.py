import os
import random

import pandas
import torch
from PIL import ImageTk
from diffusers import StableDiffusionPipeline
import tkinter as tk

class CardImageGenerator:
    def __init__(self, _prompt="A copper coin.", _collection_name="dnd/coins/cp", _file_name="copper-1", _height=536, _width=688, _prompt_strength=.8):
        self.BASE_DIR = "../data/"
        self.COLLECTION_NAME = _collection_name
        self.PROMPT = _prompt
        self.file_name = _file_name
        # self.GENERATOR = torch.Generator(device="cpu").manual_seed(1096)
        self.styles = pandas.read_csv("../data/txt/artist_styles")
        self.styles = self.styles.fillna("professional")
        self.rnd_style = random.randint(0, len(self.styles))
        model_id = "CompVis/stable-diffusion-v1-4"
        # model_id = "volrath50/fantasy-card-diffusion"
        device = "cpu"
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
        self.pipe.safety_checker = lambda images, clip_input: (images, False)
        self.pipe = self.pipe.to(device)

        # STYLE_LIST = [26, 29, 1267, 313, 940]
        # STYLE_LIST = [233, 743, 124, 845, 1235, 657, 666]
        # STYLE_LIST = [123, 145, 167, 188, 199]
        # STYLE_LIST = [318, 329, 333, 347, 351, 369, 375, 388, 391]
        # STYLE_LIST = [412, 427, 439, 444, 452, 468, 483, 499]
        # STYLE_LIST = [516, 529, 537, 541, 559, 563, 571, 583, 591]   # indices for styles to be used
        # STYLE_ROW = 8
        self.LAST_INDEX = 0
        self.PROMPT_STRENGTH = _prompt_strength
        self.HEIGHT = _height
        self.WIDTH = _width
        self.file_directory = self.BASE_DIR + self.COLLECTION_NAME
        self.file_path = self.file_directory + "/" + self.file_name + "_" + str(self.HEIGHT) + "_" + str(self.WIDTH) + "_" + str(self.rnd_style) + ".png"

    def get_image(self, _seed=1000, _style=1002, _iterations=1):
        this_style = ", style "+self.styles.iloc[_style, 0]+":"+str(self.PROMPT_STRENGTH)
        GENERATOR = torch.Generator(device="cpu").manual_seed(_seed)
        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory)
        image = self.pipe(self.PROMPT+this_style, generator=GENERATOR, height=self.HEIGHT, width=self.WIDTH, num_inference_steps=int(_iterations)).images[0]
        image.save(self.file_path)
        print("card_image_generator saved image: " + self.file_path)
        return self.file_path

    def open_generator_window(self, _tk_root):

        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(_tk_root)

        # sets the title of the
        # Toplevel widget
        new_window.title("Image Generator")

        # sets the geometry of toplevel

        # card_img = self.get_card()
        # card_image_path = self.card_file_path.replace(".png", "_card.png")
        # card_img.save(card_image_path)
        # card_photo = ImageTk.PhotoImage(card_img)
        # card_image_panel = tk.Label(new_window, image=card_photo)
        # card_image_panel.pack()
        generator_btn = tk.Button(new_window, text='Generate Image', command=self.get_image(_iterations=25))
        generator_btn.pack
        new_window.mainloop()

