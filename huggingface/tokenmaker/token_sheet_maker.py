# this file makes printable sheets for cards and tokens
import pandas
from PIL import ImageDraw, ImageFont, Image
BASE_PATH = "../../data/"

TOKEN_BACKGROUND_PATH = BASE_PATH + "dnd/templates/tokens/token-yellow-edge-1.png"

FONT_TYPE = ImageFont.truetype(BASE_PATH + "ttf/arial.ttf", 36)
IMAGE_FILE_PATH_1 = BASE_PATH + "dnd/templates/tokens/token_plus_1.png"
IMAGE_FILE_PATH_2 = BASE_PATH + "dnd/templates/tokens/token_plus_2.png"
IMAGE_FILE_PATH_3 = BASE_PATH + "dnd/templates/tokens/token_plus_3.png"
IMAGE_FILE_PATH_4 = BASE_PATH + "dnd/templates/tokens/token_plus_4.png"
IMAGE_FILE_PATH_5 = BASE_PATH + "dnd/templates/tokens/token_plus_5.png"
IMAGE_FILE_PATH_5 = BASE_PATH + "dnd/templates/tokens/token_plus_5.png"
IMAGE_FILE_PATH_5 = BASE_PATH + "dnd/templates/tokens/token_plus_5.png"
IMAGE_FILE_PATH_5 = BASE_PATH + "dnd/templates/tokens/token_plus_5.png"


"copper-1_536_688_1827.png"
DEFAULT_COIN_DATA_XLS_PATH = BASE_PATH + "xls/official_coin_data.xls"
COIN_FILE_PATH_0 = BASE_PATH + "dnd/coins/cp/copper-1_536_688_1827.png"
COIN_FILE_PATH_1 = BASE_PATH + "dnd/coins/cp/copper-5_536_688_111_card.png"
COIN_FILE_PATH_2 = BASE_PATH + "dnd/coins/sp/silver-1_536_688_1827.png"
COIN_FILE_PATH_3 = BASE_PATH + "dnd/templates/tokens/token_plus_4.png"
COIN_FILE_PATH_4 = BASE_PATH + "dnd/coins/ep/electrum-1_536_688_50.png"
COIN_FILE_PATH_5 = BASE_PATH + "dnd/templates/tokens/token_plus_5.png"
COIN_FILE_PATH_6 = BASE_PATH + "dnd/coins/gp/gold-1_536_688_918.png"
COIN_FILE_PATH_7 = BASE_PATH + "dnd/templates/tokens/token_plus_5.png"
COIN_FILE_PATH_8 = BASE_PATH + "dnd/coins/pp/platinum-1_536_688_249.png"
COIN_FILE_PATH_9 = BASE_PATH + "dnd/coins/pp/platinum-25_536_688_148.png"

TOKEN_SHEET_BLANK_FILE_PATH = BASE_PATH + "dnd/templates/token_sheet_blank.png"
DEFAULT_OUTPUT_PATH = BASE_PATH + "dnd/templates/plus_counters.png"
FOREGROUND = (0, 0, 0, 255)

MAX_WIDTH = 2432
MAX_HEIGHT = 3300
PIXELS_INCH = 600

class SheetMaker:
    def __init__(self, _image_file_path=IMAGE_FILE_PATH_1):
        self.coin_sheet_data = pandas.read_excel(DEFAULT_COIN_DATA_XLS_PATH)
        self.background = Image.open(TOKEN_SHEET_BLANK_FILE_PATH).convert("RGBA")
        self.image = Image.open(_image_file_path).convert("RGBA")
        self.width, self.height = self.image.size
        # this will make each image 1 inch wide for 300 dpi
        self.item_scale = PIXELS_INCH/self.width
        self.resized_image = self.image.resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        # self.sized_image = self.image.resize((scaled_width, scaled_width))
        print("SheetMaker.__init__ done!")

    def add_resized_images(self):
        image_1 = Image.open(IMAGE_FILE_PATH_1).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        image_2 = Image.open(IMAGE_FILE_PATH_2).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        image_3 = Image.open(IMAGE_FILE_PATH_3).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        image_4 = Image.open(IMAGE_FILE_PATH_4).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        image_5 = Image.open(IMAGE_FILE_PATH_5).convert("RGBA").resize(size=(int(self.item_scale*self.width), int(self.item_scale*self.height)))
        current_image = image_1
        for column in range(0, 8, 1):
            for row in range(0, 11, 1):
                y_pos = PIXELS_INCH * column
                x_pos = PIXELS_INCH * row
                if row < 4:
                    current_image = image_1
                elif row < 6:
                    current_image = image_2
                elif row < 8:
                    current_image = image_3
                elif row < 9:
                    current_image = image_4
                elif row > 9:
                    current_image = image_5

                self.background.paste(current_image, (y_pos, x_pos), mask=current_image)

    def make_coin_sheet(self):

        # image_token = self.get_token(2)
        # image_token.save("./image_token.png")

        # add the image to the token
        _edge_margin = 32
        background_image = Image.open(TOKEN_BACKGROUND_PATH)
        background_width, background_height = background_image.size
        image_path = str(self.coin_sheet_data.loc[3]["image_path"])
        item_image = Image.open(image_path).convert("RGBA")

        # scale image to token
        image_width, image_height = item_image.size
        image_width_scale = background_width / (image_width + (_edge_margin*6))
        image_height_scale = image_height / (background_height + (_edge_margin*12))
        item_image = item_image.resize(size=(int(image_width*image_width_scale), int(image_height*image_height_scale)))
        background_image.paste(item_image, (_edge_margin*2, _edge_margin*3), mask=item_image)
        draw = ImageDraw.Draw(background_image)

        # add quantity and name to top of token
        _quant_name = str(int(self.coin_sheet_data.loc[3]["quantity"]))
        _quant_name = _quant_name + " " + str(self.coin_sheet_data.loc[3]["name"])
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

        background_image.save("./this_image_xyzzy.png")
        print("done!")

    def get_token(self, _sheet_index=0):

        # add the image to the token
        _edge_margin = 32
        background_image = Image.open(TOKEN_BACKGROUND_PATH)
        background_width, background_height = background_image.size
        image_path = str(self.coin_sheet_data.loc[_sheet_index]["image_path"])
        _token_path = image_path.replace(".png", "_token.png")
        _token_path = image_path.replace(".jpeg", "_token.jpeg")
        _token_path = image_path.replace(".jpg", "_token.jpg")
        item_image = Image.open(image_path).convert("RGBA")

        # scale and place image on token
        image_width, image_height = item_image.size
        image_width_scale = background_width / (image_width + (_edge_margin*6))
        image_height_scale = image_height / (background_height + (_edge_margin*12))
        item_image = item_image.resize(size=(int(image_width*image_width_scale), int(image_height*image_height_scale)))
        background_image.paste(item_image, (_edge_margin*2, _edge_margin*3), mask=item_image)
        draw = ImageDraw.Draw(background_image)

        # add quantity and name to top of token
        _quant_name = str(int(self.coin_sheet_data.loc[_sheet_index]["quantity"]))
        _quant_name = _quant_name + " " + str(self.coin_sheet_data.loc[_sheet_index]["name"])
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

        background_image.save(_token_path)
        print("done!")
        return background_image

    def get_start_y(self, _string, _image):
        font_width, font_height = FONT_TYPE.getsize(_string)
        image_width, image_height = _image.size
        start_y = ((image_width-font_width)/2)+10
        return start_y


def main():
    sheet_maker = SheetMaker()
    sheet_maker.make_coin_sheet()
    # token_image = sheet_maker.get_token()
    # sheet_file_path = IMAGE_FILE_PATH.replace(".png", "_sheet.png")
    # sheet_maker.add_resized_images()
    # token_sheet.save(sheet_file_path)
    # sheet_maker.background.save(DEFAULT_OUTPUT_PATH)
    print("main done!")


if __name__ == "__main__":
    main()
