# this file makes printable sheets for cards and tokens
import importlib
import os.path

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
FONT_TYPE = ImageFont.load_default()
IMAGE_STANDARD = (512, 386)
class TokenMaker:
    # tokens are images scaled to 1 inch based on a given number of pixels
    def __init__(self, _image_file_path="data/png/rations-emergency-2.png", _name="Default Token", _weight="1.5", _pixels_inch=600):
        self.pixels_inch = _pixels_inch
        self.coin_sheet_data = pandas.read_excel(BASE_PATH+"data/xls/official_coin_data.xls")
        # self.background = Image.open(TOKEN_SHEET_BLANK_FILE_PATH).convert("RGBA")
        self.image = Image.open(BASE_PATH+_image_file_path).convert("RGBA")
        self.width, self.height = self.image.size
        # this will make each image 1 inch wide for 300 dpi
        # self.item_scale = self.pixels_inch/self.width
        # self.resized_image = self.image.resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        # self.sized_image = self.image.resize((scaled_width, scaled_width))
        print("SheetMaker.__init__ done!")

    def get_token(self, _item_index=0, _background_image=None, _item_image=None):
        # add the image to the token
        _edge_margin = 32
        if _background_image is None:
            background_image = Image.new("RGBA", (self.pixels_inch, self.pixels_inch), (128, 128, 255))
        else:
            background_image = _background_image
        background_width, background_height = background_image.size

        image_path = str(self.coin_sheet_data.loc[_item_index]["image_path"])
        _token_path = image_path.replace(".png", "_token.png")
        _token_path = image_path.replace(".jpeg", "_token.jpeg")
        _token_path = image_path.replace(".jpg", "_token.jpg")
        tmp = "/home/overlordx/PycharmProjects/imagine/data/png/rations-emergency-1_enhanced.png"
        new = "/home/overlordx/PycharmProjects/imagine/data/png/rations-emergency-1_enhanced.png"
        item_image = Image.open(BASE_PATH+image_path).convert("RGBA")

        # scale and place image on token
        image_width, image_height = item_image.size
        image_width_scale = background_width / (image_width + (_edge_margin*6))
        image_height_scale = image_height / (background_height + (_edge_margin*12))
        item_image = item_image.resize(size=(int(image_width*image_width_scale), int(image_height*image_height_scale)))
        background_image.paste(item_image, (_edge_margin*2, _edge_margin*3), mask=item_image)
        draw = ImageDraw.Draw(background_image)

        # add quantity and name to top of token
        _quant_name = str(int(self.coin_sheet_data.loc[_item_index]["quantity"]))
        _quant_name = _quant_name + " " + str(self.coin_sheet_data.loc[_item_index]["name"])
        start_y = self.get_start_y(_string=_quant_name, _image=background_image)
        draw.text((start_y, _edge_margin), text=_quant_name, font=FONT_TYPE, fill=FOREGROUND)

        # row_images = []
        # row_images.append(Image.open(COIN_FILE_PATH_0).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_1).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_2).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_3).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_4).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_5).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_6).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_7).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_8).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        # row_images.append(Image.open(COIN_FILE_PATH_9).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height))))
        image_indices = [0,1,8,9,13,14,18,19,23,24]

        weight_text = str(self.coin_sheet_data.loc[3]["weight"]) + " lb."
        start_y = self.get_start_y(weight_text, background_image)
        draw.text((start_y, 440), weight_text, font=FONT_TYPE, fill=FOREGROUND)
        # background_image.save(BASE_PATH+_token_path)
        print("done!")
        return background_image

    def get_start_y(self, _string, _image):
        font_width, font_height = FONT_TYPE.getsize(_string)
        image_width, image_height = _image.size
        start_y = ((image_width-font_width)/2)+10
        return start_y

    def make_sheet(self, _image=None, _num_rows=1):
        if _image is None:
            _image = Image.new("RGBA", IMAGE_STANDARD, (128, 128, 255, 0))
        PIXELS_INCH = 600
        tokens_per_row = 8
        edge_margin = 32
        image_width, image_height = _image.size
        background = Image.new("RGBA", A4_600_PPI, (255, 255, 255, 1))
        for row in range(_num_rows):
            background.paste(_image, (edge_margin, edge_margin), mask=_image)

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
    token_maker = TokenMaker()
    image = token_maker.get_token()
    token_sheet = token_maker.make_sheet(image)
    token_sheet.save("./token_sheet_xyzzy.png")

if __name__ == "__main__":
    main()
    test_make_sheet()
