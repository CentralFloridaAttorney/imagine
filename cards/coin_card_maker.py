import tkinter as tk
from tkinter import filedialog, Label, Entry, Menu, Text, Button, END

import pandas
from PIL import Image, ImageFont, ImageDraw, ImageTk

BASE_DIR = "../"
COIN_DATA = pandas.read_excel(BASE_DIR + "data/xls/coin_data.xls")
DEFAULT_IMAGE = "../data/dnd/coins/cp/copper-1_536_688_1827.png"

class CoinCardMakerGUI:
    def __init__(self, master):
        # display = ImageTk.PhotoImage(Image.open(BASE_DIR+"png/default_item.png"))
        # label = Label(image=display)
        # label.pack()
        self.photo_img = None
        self.card_maker = None
        self.master = master
        master.title('CoinCardMaker')

        # Create a menubar
        menubar = Menu(root)
        self.name_label = Label(text="Item Name:", fg="Red", font=("Helvetica", 18))
        self.name_field = Entry()
        # Create the dropdown menu
        self.filemenu = Menu(menubar)
        self.filemenu.add_command(label='Cut', command=lambda: root.focus_get().event_generate("<<Cut>>"))
        self.filemenu.add_command(label='Copy', command=lambda: root.focus_get().event_generate("<<Copy>>"))
        self.filemenu.add_command(label='Paste', command=lambda: root.focus_get().event_generate("<<Paste>>"))

        # Add the file menu to the menubar
        menubar.add_cascade(label='Edit', menu=self.filemenu)

        # Configure the menu with the root window as parent
        master.config(menu=menubar)
        self.textfield = Entry(master)
        self.textarea = Text(master)
        name_label = tk.Label(root, text="Name: ")
        name_label.grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        self.name = Entry(master)
        self.name.grid(row=0, column=1, rowspan=1, padx=5, pady=5)
        file_name_label = tk.Label(root, text="File Name: ")
        file_name_label.grid(row=1, column=0, rowspan=1, padx=5, pady=5)
        self.file_name = Entry(master)
        self.file_name.grid(row=1, column=1, rowspan=1, padx=5, pady=5)
        type_label = tk.Label(root, text="Type: ")
        type_label.grid(row=2, column=0, rowspan=1, padx=5, pady=5)
        self.type = Entry(master)
        self.type.grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        quantity_label = tk.Label(root, text="Quantity: ")
        quantity_label.grid(row=3, column=0, rowspan=1, padx=5, pady=5)
        self.quantity = Entry(master)
        self.quantity.grid(row=3, column=1, rowspan=1, padx=5, pady=5)
        equivalent_label = tk.Label(root, text="Equivalents: ")
        equivalent_label.grid(row=5, column=0, rowspan=1, padx=5, pady=5)
        self.equivalents = Entry(master)
        self.equivalents.grid(row=5, column=1, rowspan=1, padx=5, pady=5)
        index_label = tk.Label(root, text="Index: ")
        index_label.grid(row=7, column=0, rowspan=1, padx=5, pady=5)
        self.index = Entry(master)
        self.index.insert(0, "0")
        self.index.grid(row=7, column=1, rowspan=1, padx=5, pady=5)
        self.open_file_button = Button(master, text="Open Item Image", command=self.open_image)
        self.open_file_button.grid(row=9, column=0, rowspan=1, padx=5, pady=5)
        self.image_file_path = Text(master)
        self.image_file_path.grid(row=9, column=1, rowspan=1, padx=5, pady=5)


        self.btn_make_card = Button(root, text='Make Card', command=self.make_card)
        self.btn_make_card.grid(row=10, column=0, rowspan=1, padx=5, pady=5)
        self.load_xls_btn = Button(master, text="Load XLS", command=self.load_xls)
        self.load_xls_btn.grid(row=11, column=0, rowspan=1, padx=5, pady=5)

        description_label = tk.Label(root, text="Description: ")
        description_label.grid(row=12, column=0, rowspan=1, padx=5, pady=5)
        self.description = Text(master, height=5)
        self.description.grid(row=12, column=1, rowspan=5, padx=5, pady=5)

        prompt_label = tk.Label(root, text="Prompt: ")
        prompt_label.grid(row=18, column=0, rowspan=1, padx=5, pady=5)
        self.prompt = Text(master, height=5)
        self.prompt.grid(row=18, column=1, rowspan=5, padx=5, pady=5)

        self.previous_index_btn = Button(master, text="Previous", command=self.previous_index)
        self.previous_index_btn.grid(row=24, column=0, rowspan=1, padx=5, pady=5)
        self.next_index_btn = Button(master, text="Next", command=self.next_index)
        self.next_index_btn.grid(row=24, column=1, rowspan=1, padx=5, pady=5)
        self.COIN_DATA = self.load_xls()
        self.img = Image.open(DEFAULT_IMAGE)
        self.photo_img = ImageTk.PhotoImage(self.img)
        self.image_panel = Label(master, image=self.photo_img)
        self.image_panel.grid(row=25, column=1, rowspan=1, padx=5, pady=5)
        self.update_gui()

    def next_index(self):
        current_index = int(self.index.get())
        if (current_index + 1) < len(self.COIN_DATA):
            self.index.delete(0, END)
            self.index.insert(0, (current_index + 1))
            self.update_gui()
        print("next_index done")

    def previous_index(self):
        current_index = int(self.index.get())
        if (current_index - 1) > -1:
            self.index.delete(0, END)
            self.index.insert(0, (current_index - 1))
            self.update_gui()
    print("previous)_index done!")

    def update_gui(self):
        if int(self.index.get()) < len(COIN_DATA):
            self.name.delete(0, END)
            self.name.insert(0, COIN_DATA.iloc[int(self.index.get()), 0])
            self.file_name.delete(0, END)
            self.file_name.insert(0, COIN_DATA.iloc[int(self.index.get()), 1])
            self.type.delete(0, END)
            self.type.insert(0, COIN_DATA.iloc[int(self.index.get()), 2])
            self.quantity.delete(0, END)
            self.quantity.insert(0, COIN_DATA.iloc[int(self.index.get()), 3])
            self.description.delete('1.0', END)
            self.description.insert('1.0', COIN_DATA.iloc[int(self.index.get()), 4])
            self.equivalents.delete(0, END)
            self.equivalents.insert(0, COIN_DATA.iloc[int(self.index.get()), 5])
            self.prompt.delete('1.0', END)
            self.prompt.insert('1.0', COIN_DATA.iloc[int(self.index.get()), 6])
            self.image_file_path.delete('1.0', END)
            self.image_file_path.insert('1.0', COIN_DATA.iloc[int(self.index.get()), 7])
            self.img = Image.open(BASE_DIR+self.image_file_path.get('1.0'))
            self.photo_img = ImageTk.PhotoImage(self.img)
            self.image_panel.configure(image=self.photo_img)
            self.image_panel.image = self.photo_img

    def load_xls(self):
        return pandas.read_excel(BASE_DIR + "data/xls/coin_data.xls")

    def make_card(self):
        card_image = self.card_maker.make_card()
        print("make_card done!")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('image files', '.png')], initialdir=BASE_DIR+"data/dnd/")
        # trim the file_path
        p = file_path.split('/')
        counter = 0
        while True:
            if p[counter] == 'data':
                break
            counter += 1
        path = '/' + '/'.join(p[counter:])
        path = path[1:]
        self.image_file_path.delete('1.0', END)
        self.image_file_path.insert('1.0', path)
        self.update_gui()
        self.card_maker = Cardmaker(_item_image=self.img,
                                    _name=self.name.get(),
                                    _type=self.type.get(),
                                    _quantity=self.quantity.get(),
                                    _equivalents=self.equivalents.get(),
                                    _description=self.description.get("1.0", END))
        print("open_image done!")

    def insert_text_area(self):
        self.insert_text(self.textfield, self.textarea)

    @staticmethod
    def insert_text(source, destination):
        destination.insert(1.0, source.get())

    def cut_text(self):
        self.textarea.event_generate("<<Cut>>")

    def copy_text(self):
        self.textarea.event_generate("<<Copy>>")

    def paste_text(self):
        self.textarea.event_generate("<<Paste>>")


class Cardmaker:
    def __init__(self,
                 _item_image=None,
                 _background=None,
                 _name="Copper",
                 _type="cp",
                 _quantity="1",
                 _equivalents="1cp",
                 _description="1 Copper coin."):
        if _item_image is None:
            self.item_image = Image.open(BASE_DIR + "data/dnd/equipment/rations/536_688_559.png").convert("RGBA")
        else:
            self.item_image = _item_image.convert("RGBA")
            self.item_image.convert()
            # self.item_image = _item_image.convert("RGBA")
        if _background is None:
            self.background = Image.open(BASE_DIR + "data/png/card_template_v001.png").convert("RGBA")
        else:
            self.background = _background.convert("RGBA")
        self.name = _name
        self.type = _type
        self.quantity = _quantity
        self.equivalents = _equivalents
        self.description = _description

    def make_card(self):
        self.background.paste(self.item_image, (31, 36), mask=self.item_image)
        import textwrap
        font_type = ImageFont.truetype(BASE_DIR + "ttf/arial.ttf", 24)
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
        self.background.save("data/output/" + self.name + ".png")
        print("make_card done!")


root = tk.Tk()
CoinCardMakerGUI(root)
root.mainloop()
