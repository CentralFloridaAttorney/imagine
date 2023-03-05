import tkinter as tk

from tkinter import Label

from PIL import ImageFont, ImageDraw, Image, ImageTk

DEFAULT_IMAGE_PATH = "../../../data/png/536_688_563.png"
FONT_TYPE = ImageFont.truetype("../../../data/ttf/arial.ttf", 24)


class Cardmaker:
    def __init__(self,
                 _image_file_path=DEFAULT_IMAGE_PATH,
                 _background=None,
                 _name="Copper",
                 _type="cp",
                 _quantity="1",
                 _equivalents="1cp",
                 _description="1 Copper coin.",
                 _output_file_path="./output/card/default_card.png"):
        if _image_file_path is None:
            self.item_image = Image.open("../data/dnd/equipment/rations/536_688_559.png").convert("RGBA")
        else:
            self.item_image = Image.open(_image_file_path).convert("RGBA")
            # self.item_image.convert()
            # self.item_image = _item_image.convert("RGBA")
        if _background is None:
            self.background = Image.open("../data/png/card_template_v001.png").convert("RGBA")
        else:
            self.background = _background.convert("RGBA")
        self.name = _name
        self.type = _type
        self.quantity = _quantity
        self.equivalents = _equivalents
        self.description = _description
        self.card_file_path = _output_file_path

    def get_card(self):
        self.background.paste(self.item_image, (31, 36), mask=self.item_image)
        import textwrap
        foreground = (0, 0, 0, 255)
        draw = ImageDraw.Draw(self.background)
        draw.text((34, 5), self.name, font=FONT_TYPE, fill=foreground)
        draw.text((46, 970), "Equivalents: " + self.equivalents, font=FONT_TYPE, fill=foreground)
        novo = textwrap.wrap(self.description, width=64)
        for row in range(0, len(novo), 1):
            y_position = 650 + (36 * row)
            # font = ImageFont.load_default()

            draw.text((46, y_position), novo[row], font=FONT_TYPE, fill=foreground)
        # Displaying the image
        self.background.save(self.card_file_path)
        print("make_card done!")
        return self.background

    def open_card_window(self, _tk_master):

        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(_tk_master)

        # sets the title of the
        # Toplevel widget
        new_window.title("Card Maker")

        # sets the geometry of toplevel

        card_img = self.get_card()
        card_image_path = self.card_file_path.replace(".png", "_card.png")
        card_img.save(card_image_path)
        card_photo = ImageTk.PhotoImage(card_img)
        card_image_panel = Label(new_window, image=card_photo)
        card_image_panel.pack()
        new_window.mainloop()


class TokenMaker:
    def __init__(self,
                 _image_file_path=DEFAULT_IMAGE_PATH,
                 _background=None,
                 _name="Copper",
                 _type="cp",
                 _quantity="1",
                 _equivalents="1cp",
                 _description="1 Copper coin.",
                 _output_file_path="../data/dnd/tokens/default_token.png"):
        if _image_file_path is None:
            self.item_image = Image.open("../data/dnd/equipment/rations/536_688_559.png").convert("RGBA")
        else:
            self.item_image = Image.open(_image_file_path).convert("RGBA")
            # self.item_image.convert()
            # self.item_image = _item_image.convert("RGBA")
        if _background is None:
            #self.background = Image.open("../data/png/card_template_v001.png").convert("RGBA")
            self.background = Image.open("../data/dnd/templates/coin-large-1.png").convert("RGBA")

        else:
            self.background = _background.convert("RGBA")
        self.name = _name
        self.type = _type
        self.quantity = _quantity
        self.equivalents = _equivalents
        self.description = _description
        self.card_file_path = _output_file_path

    def get_card(self):
        self.background.paste(self.item_image, (31, 36), mask=self.item_image)
        import textwrap
        foreground = (0, 0, 0, 255)
        draw = ImageDraw.Draw(self.background)
        draw.text((34, 5), self.name, font=FONT_TYPE, fill=foreground)
        draw.text((46, 970), "Equivalents: " + self.equivalents, font=FONT_TYPE, fill=foreground)
        novo = textwrap.wrap(self.description, width=64)
        for row in range(0, len(novo), 1):
            y_position = 650 + (36 * row)
            # font = ImageFont.load_default()

            draw.text((46, y_position), novo[row], font=FONT_TYPE, fill=foreground)
        # Displaying the image
        self.background.save(self.card_file_path)
        print("make_card done!")
        return self.background

    def open_card_window(self, _tk_master):

        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(_tk_master)

        # sets the title of the
        # Toplevel widget
        new_window.title("Card Maker")

        # sets the geometry of toplevel

        card_img = self.get_card()
        card_image_path = self.card_file_path.replace(".png", "_card.png")
        card_img.save(card_image_path)
        card_photo = ImageTk.PhotoImage(card_img)
        card_image_panel = Label(new_window, image=card_photo)
        card_image_panel.pack()
        new_window.mainloop()
