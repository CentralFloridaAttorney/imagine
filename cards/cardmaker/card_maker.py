from PIL import ImageFont, ImageDraw, Image

DEFAULT_IMAGE_PATH = "../data/png/536_688_563.png"


class CardMaker:
    def __init__(self,
                 _image_file_path=DEFAULT_IMAGE_PATH,
                 _background=None,
                 _name="Copper",
                 _type="cp",
                 _quantity="1",
                 _equivalents="1cp",
                 _description="1 Copper coin.",
                 _card_file_path="../data/output/card/default_card.png"):
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
        self.card_file_path = _card_file_path

    def get_card(self):
        self.background.paste(self.item_image, (31, 36), mask=self.item_image)
        import textwrap
        font_type = ImageFont.truetype("../data/ttf/arial.ttf", 24)
        foreground = (0, 0, 0, 255)
        draw = ImageDraw.Draw(self.background)
        draw.text((34, 5), self.name, font=font_type, fill=foreground)
        draw.text((46, 970), "Equivalents: " + self.equivalents, font=font_type, fill=foreground)
        novo = textwrap.wrap(self.description, width=64)
        for row in range(0, len(novo), 1):
            y_position = 650 + (36 * row)
            # font = ImageFont.load_default()

            draw.text((46, y_position), novo[row], font=font_type, fill=foreground)
        # Displaying the image
        self.background.save(self.card_file_path)
        print("make_card done!")
        return self.background
