# this file makes printable sheets for cards and tokens
import importlib
import os.path

import cv2 as cv
import pandas
import pkg_resources
from PIL import ImageDraw, ImageFont, Image
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker")+"/imagine/"

FOREGROUND = (0, 0, 0, 255)
MAX_WIDTH = 2432
MAX_HEIGHT = 3300
# PIXELS_INCH = 600
A4_300_PPI = (2480, 3508)
A4_600_PPI = (4960, 7016)
FONT_TYPE = ImageFont.truetype(BASE_PATH+"data/ttf/arial.ttf", 36)
IMAGE_STANDARD = (512, 512)
BACKGROUND_DIMENSIONS = (600, 600)
NUM_COLS = 8
class TokenMaker:
    # tokens are images scaled to 1 inch based on a given number of pixels
    def __init__(self, _image_file_path=None, _name="Default Token", _weight="1.5", _pixels_inch=600):
        self.pixels_inch = _pixels_inch
        # self.coin_sheet_data = pandas.read_excel(BASE_PATH+"data/xls/official_coin_data.xls")
        # self.background = Image.open(TOKEN_SHEET_BLANK_FILE_PATH).convert("RGBA")
        if _image_file_path is None:
            self.image = Image.new("RGBA", IMAGE_STANDARD, (128, 128, 255))
        else:
            self.image = Image.open(BASE_PATH+_image_file_path).convert("RGBA")
        self.width, self.height = self.image.size
        # this will make each image 1 inch wide for 300 dpi
        # self.item_scale = self.pixels_inch/self.width
        # self.resized_image = self.image.resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        # self.sized_image = self.image.resize((scaled_width, scaled_width))
        print("SheetMaker.__init__ done!")

    def get_token(self, _background_image=None, _item_image=None, _top_text="top", _bottom_text="bottom"):
        # add the image to the token
        if _background_image is None:
            background_image = Image.new("RGBA", (self.pixels_inch, self.pixels_inch), (128, 128, 255))
        else:
            background_image = Image.open(BASE_PATH+_background_image)
        background_image = background_image.resize(size=BACKGROUND_DIMENSIONS)
        background_width, background_height = background_image.size
        if _item_image is None:
            item_image = self.image.convert("RGBA")
        else:
            if type(_item_image) is str:
                item_image = Image.open(BASE_PATH+_item_image)
            else:
                item_image = _item_image
        # scale and place image on token
        image_width, image_height = item_image.size
        image_width_scale = image_width / background_width
        image_height_scale = image_height / background_height
        item_image = item_image.resize(size=(int(image_width*image_width_scale), int(image_height*image_height_scale)))
        edge_margin = 88
        # draw the item_image and text elements of the token
        background_image.paste(item_image, (edge_margin, edge_margin), mask=item_image)
        draw = ImageDraw.Draw(background_image)
        start_y = self.get_start_y(_string=_top_text, _image=background_image)
        draw.text((start_y, edge_margin/2.75), text=_top_text, font=FONT_TYPE, fill=FOREGROUND)
        start_y = self.get_start_y(_bottom_text, background_image)
        draw.text((start_y, background_height-(edge_margin/1.25)), _bottom_text, font=FONT_TYPE, fill=FOREGROUND)
        print("TokenMaker().get_token done!")
        return background_image

    def get_start_y(self, _string, _image):
        font_width, font_height = FONT_TYPE.getsize(_string)
        image_width, image_height = _image.size
        start_y = ((image_width-font_width)/2)+10
        return start_y

    def make_sheet(self, _image=None, _num_rows=1):
        if _image is None:
            image = self.image
        else:
            image = _image
        token_image = self.get_token(_item_image=image, _top_text="5 Copper Coins", _bottom_text=".1 lb.")
        PIXELS_INCH = 600
        edge_margin = 32
        image_width, image_height = token_image.size
        background = Image.new("RGBA", A4_600_PPI, (255, 255, 255, 1))
        for row in range(_num_rows):
            for column in range(0, NUM_COLS, 1):
                background.paste(image, (edge_margin+(image_width*column), edge_margin+(image_height*row)), mask=image)

        return background

def main():
    token_maker = TokenMaker()
    image = token_maker.get_token()
    image.save("./token_xyzzy.png")
    # token_image = sheet_maker.get_token()
    # sheet_file_path = IMAGE_FILE_PATH.replace(".png", "_sheet.png")
    # sheet_maker.add_resized_images()
    # token_sheet.save(sheet_file_path)
    # sheet_maker.background.save(DEFAULT_OUTPUT_PATH)
    print("main done!")

def test_make_sheet():
    # token_maker = TokenMaker(_image_file_path="data/dnd/templates/tokens/coins-2.png")
    # image = token_maker.get_token(_top_text="5 Copper Coins", _bottom_text=".1 lb.", _background_image="data/dnd/templates/tokens/background-3.png")

    token_maker = TokenMaker()
    image = token_maker.get_token(_item_image="data/dnd/templates/tokens/coins-2.png", _top_text="5 Copper Coins", _bottom_text=".1 lb.", _background_image="data/dnd/templates/tokens/background-3.png")

    image.save("./token_xyzzy.png")
    # token_sheet = token_maker.make_sheet()
    token_sheet = token_maker.make_sheet(image)
    token_sheet.save("./token_sheet_xyzzy.png")

if __name__ == "__main__":
    # main()
    test_make_sheet()
