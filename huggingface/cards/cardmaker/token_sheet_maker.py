# this file makes printable sheets for cards and tokens
from PIL import ImageDraw, ImageFont, Image

FONT_TYPE = ImageFont.truetype("../../data/ttf/arial.ttf", 24)
IMAGE_FILE_PATH_1 = "../../data/dnd/templates/tokens/token_plus_1.png"
IMAGE_FILE_PATH_2 = "../../data/dnd/templates/tokens/token_plus_2.png"
IMAGE_FILE_PATH_3 = "../../data/dnd/templates/tokens/token_plus_3.png"
IMAGE_FILE_PATH_4 = "../../data/dnd/templates/tokens/token_plus_4.png"
IMAGE_FILE_PATH_5 = "../../data/dnd/templates/tokens/token_plus_5.png"

TOKEN_SHEET_BLANK_FILE_PATH = "../../data/dnd/templates/token_sheet_blank.png"
DEFAULT_OUTPUT_PATH = "../../data/dnd/templates/plus_counters.png"
MAX_WIDTH = 2432
MAX_HEIGHT = 3300
PIXELS_INCH = 300

class SheetMaker:
    def __init__(self, _image_file_path=IMAGE_FILE_PATH_1):
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


def main():
    sheet_maker = SheetMaker()
    # token_image = sheet_maker.get_token()
    # sheet_file_path = IMAGE_FILE_PATH.replace(".png", "_sheet.png")
    sheet_maker.add_resized_images()
    # token_sheet.save(sheet_file_path)
    sheet_maker.background.save(DEFAULT_OUTPUT_PATH)
    print("main done!")


if __name__ == "__main__":
    main()
