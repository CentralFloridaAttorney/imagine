# this file makes printable sheets for cards and tokens
import os.path

from PIL import ImageDraw, ImageFont, Image

BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker") + "/imagine/"

FOREGROUND = (0, 0, 0, 255)
MAX_WIDTH = 2432
MAX_HEIGHT = 3300
# PIXELS_INCH = 600
A4_300_PPI = (2480, 3508)
A4_600_PPI = (4960, 7016)
FONT_TYPE = ImageFont.truetype(BASE_PATH + "data/ttf/arial.ttf", 24)
IMAGE_STANDARD = (512, 512)
BACKGROUND_DIMENSIONS = (600, 600)
NUM_COLS = 8


class TokenMaker:
    # tokens are images scaled to 1 inch based on a given number of pixels
    def __init__(self, _image_file=None, _top_text="Default Token", _bottom_text="1.5", _pixels_inch=600):
        self.pixels_inch = _pixels_inch
        if _image_file is None:
            self.image = Image.new("RGBA", IMAGE_STANDARD, (128, 128, 255))
        else:
            if type(_image_file) is str:
                self.image = Image.open(BASE_PATH + _image_file).convert("RGBA")
            else:
                self.image = _image_file
        self.width, self.height = self.image.size
        self.top_text = _top_text
        self.bottom_text = _bottom_text
        print("SheetMaker.__init__ done!")

    def get_token(self, _background_image=None, _item_image=None, _top_text=None, _bottom_text=None):
        if _top_text is None:
            top_text = self.top_text
        else:
            top_text = _top_text
        if _bottom_text is None:
            bottom_text = self.bottom_text
        else:
            bottom_text = _bottom_text
        # add the image to the token
        if _background_image is None:
            background_image = Image.new("RGBA", (self.pixels_inch, self.pixels_inch), (128, 128, 255))
        else:
            background_image = Image.open(BASE_PATH + _background_image)
        background_image = background_image.resize(size=BACKGROUND_DIMENSIONS)
        background_width, background_height = background_image.size
        if _item_image is None:
            item_image = self.image.convert("RGBA")
        else:
            if type(_item_image) is str:
                item_image = Image.open(BASE_PATH + _item_image)
            else:
                item_image = _item_image
        # scale and place image on token
        image_width, image_height = item_image.size
        img_standard_width, img_standard_height = IMAGE_STANDARD
        image_width_scale = img_standard_width / image_width
        image_height_scale = image_height / img_standard_height
        item_image = item_image.resize(
            size=(int(image_width * image_width_scale), int(image_height * image_height_scale))).convert("RGBA")
        edge_margin = 44
        # center the image on the token
        image_y = int((background_height-image_height)/2)
        background_image.paste(item_image, (edge_margin, image_y), mask=item_image)
        draw = ImageDraw.Draw(background_image)
        start_y = self.get_start_y(_string=top_text, _image=background_image)
        draw.text((start_y, edge_margin / 2.75), text=top_text, font=FONT_TYPE, fill=FOREGROUND)
        start_y = self.get_start_y(bottom_text, background_image)
        draw.text((start_y, background_height - (edge_margin / 1.0)), bottom_text, font=FONT_TYPE, fill=FOREGROUND)
        print("TokenMaker().get_token done!")
        return background_image

    @staticmethod
    def get_start_y(_string, _image):
        font_width, font_height = FONT_TYPE.getsize(_string)
        image_width, image_height = _image.size
        start_y = ((image_width - font_width) / 2)
        return start_y

    def make_sheet(self, _image=None, _num_rows=1):
        if _image is None:
            image = self.image
        else:
            image = _image
        token_image = self.get_token(_item_image=image, _top_text="5 Copper Coins", _bottom_text=".1 lb.")
        edge_margin = 32
        image_width, image_height = token_image.size
        background = Image.new("RGBA", A4_600_PPI, (255, 255, 255, 1))
        for row in range(_num_rows):
            for column in range(0, NUM_COLS, 1):
                background.paste(image, (edge_margin + (image_width * column), edge_margin + (image_height * row)),
                                 mask=image)

        return background


def main():
    token_maker = TokenMaker()
    image = token_maker.get_token()
    image.save("./token_xyzzy.png")
    print("main done!")


def test_make_sheet_1():
    token_maker = TokenMaker()
    image = token_maker.get_token(_item_image="data/dnd/templates/tokens/coins-2.png", _top_text="5 Copper Coins",
                                  _bottom_text=".1 lb.", _background_image="data/dnd/templates/tokens/background-3.png")
    image.save("./token_xyzzy.png")
    token_sheet = token_maker.make_sheet(image)
    token_sheet.save("./token_sheet_xyzzy.png")


def test_make_sheet_2():
    token_maker = TokenMaker()
    image = token_maker.get_token(_item_image="data/dnd/monsters/level_1/jackal_attacking_v000.png", _top_text="Jackal",
                                  _bottom_text="35 lb.", _background_image="data/dnd/templates/tokens/background-3.png")
    image.save("./token_fireball_xyzzy.png")
    token_sheet = token_maker.make_sheet(image)
    token_sheet.save("./token_sheet_fireball_xyzzy_2.png")


if __name__ == "__main__":
    # main()
    test_make_sheet_1()
    test_make_sheet_2()
