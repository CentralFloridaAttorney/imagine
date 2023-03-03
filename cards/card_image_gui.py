import time
import tkinter as tk
from tkinter import filedialog, Label, Entry, Menu, Text, Button, END

import pandas
from PIL import Image, ImageFont, ImageDraw, ImageTk
from transformers import pipeline

from cards import card_image_prompt_generator
from cards.card_image_generator import CardImageGenerator

# BASE_DIR = "../"
PROJECT_DIR = "data/dnd/"
DEFAULT_XLS = "../data/xls/coin_data.xls"
COIN_DATA = pandas.read_excel("../data/xls/coin_data.xls")
DEFAULT_IMAGE = "../data/dnd/coins/cp/copper-1_536_688_1827.png"
COLLECTION_NAME = "dnd/"
FONT_TYPE = ImageFont.truetype("../data/ttf/arial.ttf", 24)

class CoinCardMakerGUI:
    def __init__(self, master):
        # self.prompt_generator = PromptGenerator()
        self.coin_photo = None
        self.card_maker = None
        self.master = master
        # self.master.title('CoinCardMaker')
        # Create a menubar
        self.menubar = Menu(self.master)
        # Buttons
        self.previous_index_btn = Button(self.master, text="Previous", command=self.previous_index)
        self.previous_index_btn.grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        self.index = Entry(self.master)
        self.index.insert(0, "0")
        self.index.grid(row=0, column=1, rowspan=1, padx=5, pady=5)
        self.next_index_btn = Button(self.master, text="Next", command=self.next_index)
        self.next_index_btn.grid(row=0, column=2, rowspan=1, padx=5, pady=5)
        self.open_file_button = Button(self.master, text="Open Item Image", command=self.open_image)
        self.open_file_button.grid(row=1, column=0, rowspan=1, padx=5, pady=5)
        self.btn_make_card = Button(self.master, text='Make Card', command=self.open_card_window)
        self.btn_make_card.grid(row=1, column=1, rowspan=1, padx=5, pady=5)
        self.show_image_btn = Button(self.master, text="Show Image", command=self.open_image_window)
        self.show_image_btn.grid(row=1, column=2, rowspan=1, padx=5, pady=5)
        self.load_xls_btn = Button(self.master, text="Load XLS", command=self.load_xls)
        self.load_xls_btn.grid(row=2, column=0, rowspan=1, padx=5, pady=5)
        self.generate_image_btn = Button(self.master, text="Generate Image", command=self.generate_image)
        self.generate_image_btn.grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        self.copy_last_card_btn = Button(self.master, text="Copy Current", command=self.new_card)
        self.copy_last_card_btn.grid(row=2, column=2, rowspan=1, padx=5, pady=5)
        self.generate_prompts_btn = Button(self.master, text="Generate Prompt", command=self.open_prompts_window)
        self.generate_prompts_btn.grid(row=2, column=3, rowspan=1, padx=5, pady=5)
        # Data Fields
        iterations_label = tk.Label(self.master, text="Iterations: ")
        iterations_label.grid(row=4, column=0, rowspan=1, padx=5, pady=5)
        self.iterations = Entry(self.master)
        self.iterations.grid(row=4, column=1, rowspan=1, padx=5, pady=5)
        self.iterations.insert(0, 20)
        name_label = tk.Label(self.master, text="Name: ")
        name_label.grid(row=5, column=0, rowspan=1, padx=5, pady=5)
        self.name = Entry(self.master)
        self.name.grid(row=5, column=1, rowspan=1, padx=5, pady=5)
        file_name_label = tk.Label(self.master, text="File Name: ")
        file_name_label.grid(row=6, column=0, rowspan=1, padx=5, pady=5)
        self.file_name = Entry(self.master)
        self.file_name.grid(row=6, column=1, rowspan=1, padx=5, pady=5)
        collection_name_label = tk.Label(self.master, text="Collection Name: ")
        collection_name_label.grid(row=7, column=0, rowspan=1, padx=5, pady=5)
        self.collection_name = Entry(self.master)
        self.collection_name.grid(row=7, column=1, rowspan=1, padx=5, pady=5)
        quantity_label = tk.Label(self.master, text="Quantity: ")
        quantity_label.grid(row=8, column=0, rowspan=1, padx=5, pady=5)
        self.quantity = Entry(self.master)
        self.quantity.grid(row=8, column=1, rowspan=1, padx=5, pady=5)
        equivalent_label = tk.Label(self.master, text="Equivalents: ")
        equivalent_label.grid(row=9, column=0, rowspan=1, padx=5, pady=5)
        self.equivalents = Entry(self.master)
        self.equivalents.grid(row=9, column=1, rowspan=1, padx=5, pady=5)

        # Create the dropdown menu
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label='New Card', command=self.new_card)
        self.filemenu.add_command(label='Cut', command=lambda: root.focus_get().event_generate("<<Cut>>"))
        self.filemenu.add_command(label='Copy', command=lambda: root.focus_get().event_generate("<<Copy>>"))
        self.filemenu.add_command(label='Paste', command=lambda: root.focus_get().event_generate("<<Paste>>"))
        # Add the file menu to the menubar
        self.menubar.add_cascade(label='Edit', menu=self.filemenu)
        # Configure the menu with the root window as parent
        self.master.config(menu=self.menubar)


        self.COIN_DATA = self.load_xls()
        card_file_path = DEFAULT_IMAGE.replace(".png", "_card.png")
        self.card_file_path = card_file_path

        self.image_file_path = Label(self.master, text=DEFAULT_IMAGE)
        self.image_file_path.grid(row=0, column=6, rowspan=1, padx=5, pady=5)

        description_label = tk.Label(self.master, text="Description: ")
        description_label.grid(row=1, column=6, rowspan=1, padx=5, pady=5)
        self.description = Text(self.master, height=10)
        self.description.grid(row=2, column=6, rowspan=10, padx=5, pady=5)

        prompt_label = tk.Label(self.master, text="Prompt: ")
        prompt_label.grid(row=4, column=8, rowspan=1, padx=5, pady=5)
        self.prompt = Text(self.master, height=10)
        self.prompt.grid(row=12, column=6, rowspan=10, padx=5, pady=5)

        # coin image
        self.img = Image.open(DEFAULT_IMAGE)
        self.coin_photo = ImageTk.PhotoImage(self.img)
        self.coin_image_panel = Label(master, image=self.coin_photo)
        self.coin_image_panel.grid(row=22, column=6, rowspan=100, padx=5, pady=5)

        # card image
        # self.card_img = self.make_card()
        # self.card_photo = ImageTk.PhotoImage(self.card_img)
        # self.card_image_panel = Label(master, image=self.card_photo)
        # self.card_image_panel.grid(row=0, column=2, rowspan=20, padx=5, pady=5)
        self.master.bind('<Return>', self.update_xls)
        self.update_data_gui()

    def open_prompts_window(self):

        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(self.master)
        current_prompt = self.prompt.get("1.0", END)
        prompt_list = card_image_prompt_generator.generate(current_prompt)
        prompt_string = ""
        for row in range(0, len(prompt_list), 1):
            prompt_string += prompt_list[row] + " *** "

        revised_prompt_label = Text(new_window, font=('Helvetica bold',40))
        revised_prompt_label.insert("1.0", prompt_string)
        revised_prompt_label.pack()
        # revised_prompt_label.pack()
        # sets the geometry of toplevel

        # card_img = self.get_card_image()
        # card_image_path = self.image_file_path["text"].replace(".png", "_card.png")
        # card_img.save(card_image_path)
        # card_photo = ImageTk.PhotoImage(card_img)
        # card_image_panel = Label(new_window, image=card_photo)
        # card_image_panel.pack()

        new_window.mainloop()

    # function to open a new window
    # on a button click
    def open_card_window(self):

        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(self.master)

        # sets the title of the
        # Toplevel widget
        new_window.title(str(self.name.get()))

        # sets the geometry of toplevel

        card_img = self.get_card_image()
        card_image_path = self.image_file_path["text"].replace(".png", "_card.png")
        card_img.save(card_image_path)
        card_photo = ImageTk.PhotoImage(card_img)
        card_image_panel = Label(new_window, image=card_photo)
        card_image_panel.pack()
        new_window.mainloop()

    def open_image_window(self):
        new_window = tk.Toplevel(self.master)

        # sets the title of the
        # Toplevel widget
        new_window.title(str(self.name.get()))

        # sets the geometry of toplevel
        img = Image.open(self.image_file_path["text"])
        coin_photo = ImageTk.PhotoImage(img)
        coin_image_panel = Label(new_window, image=coin_photo)
        coin_image_panel.image = coin_photo
        coin_image_panel.pack()
        new_window.mainloop()

    def new_card(self):
        current_row = int(self.index.get())
        data_frame = self.COIN_DATA.loc[current_row]
        new_row = data_frame.copy().transpose()

        # Insert Dict to the dataframe using DataFrame.append()
        # new_row = {'Courses': 'Hyperion', 'Fee': 24000, 'Duration': '55days', 'Discount': 1800}
        df2 = self.COIN_DATA.append(new_row, ignore_index=True)

        self.COIN_DATA = df2
        print("new_card done!")

    def generate_image(self):
        collection_name = COLLECTION_NAME + str(self.collection_name.get())
        image_prompt = self.prompt.get("1.0", END) + ", bokeh, photography –s 625 –q 2 –iw"
        item_image_generator = CardImageGenerator(
            _prompt=image_prompt,
            _collection_name=collection_name,
            _file_name=self.file_name.get(), )
        item_image_file_path = item_image_generator.get_image(_seed=415423, _style=123,
                                                              _iterations=self.iterations.get())

        # self.update_coin_image(item_image_file_path)
        # self.update_card_image()

        self.COIN_DATA.iloc[int(self.index.get()), 7] = item_image_file_path
        # self.image_file_path.delete('1.0', END)
        # self.image_file_path.insert('1.0', item_image_file_path)
        self.image_file_path["text"] = item_image_file_path
        self.save_xls()
        self.update_coin_image(item_image_file_path)

    def update_image_gui(self):
        self.update_coin_image(self.image_file_path["text"])
        # self.update_card_image()

    def update_data_gui(self):
        self.name.delete(0, END)
        self.name.insert(0, self.COIN_DATA.iloc[int(self.index.get()), 0])
        self.file_name.delete(0, END)
        self.file_name.insert(0, self.COIN_DATA.iloc[int(self.index.get()), 1])
        self.collection_name.delete(0, END)
        self.collection_name.insert(0, self.COIN_DATA.iloc[int(self.index.get()), 2])
        self.quantity.delete(0, END)
        self.quantity.insert(0, self.COIN_DATA.iloc[int(self.index.get()), 3])
        self.description.delete('1.0', END)
        self.description.insert('1.0', self.COIN_DATA.iloc[int(self.index.get()), 4])
        self.equivalents.delete(0, END)
        self.equivalents.insert(0, self.COIN_DATA.iloc[int(self.index.get()), 5])
        self.prompt.delete('1.0', END)
        self.prompt.insert('1.0', self.COIN_DATA.iloc[int(self.index.get()), 6])
        self.image_file_path["text"] = self.COIN_DATA.iloc[int(self.index.get()), 7]

    def update_xls(self, event):
        self.update_coin_data()

    def next_index(self):
        current_index = int(self.index.get())
        if (current_index + 1) < len(self.COIN_DATA):
            self.index.delete(0, END)
            self.index.insert(0, (current_index + 1))
            self.update_data_gui()
            self.update_image_gui()
        print("next_index done")

    def previous_index(self):
        current_index = int(self.index.get())
        if (current_index - 1) > -1:
            self.index.delete(0, END)
            self.index.insert(0, (current_index - 1))
            self.update_data_gui()
            self.update_image_gui()
        print("previous index done!")

    def update_coin_data(self):
        self.COIN_DATA.iloc[int(self.index.get()), 0] = str(self.name.get())
        self.COIN_DATA.iloc[int(self.index.get()), 1] = str(self.file_name.get())
        self.COIN_DATA.iloc[int(self.index.get()), 2] = str(self.collection_name.get())
        self.COIN_DATA.iloc[int(self.index.get()), 3] = str(self.quantity.get())
        self.COIN_DATA.iloc[int(self.index.get()), 4] = str(self.description.get("1.0", END).replace("\n", ""))
        self.COIN_DATA.iloc[int(self.index.get()), 5] = str(self.equivalents.get())
        self.COIN_DATA.iloc[int(self.index.get()), 6] = str(self.prompt.get("1.0", END).replace("\n", ""))
        self.COIN_DATA.iloc[int(self.index.get()), 7] = self.image_file_path["text"]
        self.save_xls()

    def load_xls(self):
        return pandas.read_excel(DEFAULT_XLS)

    def save_xls(self):
        self.COIN_DATA.to_excel(DEFAULT_XLS, index=False)

    def get_card_image(self):
        card_maker = Cardmaker(_image_file_path=self.image_file_path["text"],
                               _name=self.name.get(),
                               _type=self.collection_name.get(),
                               _quantity=self.quantity.get(),
                               _equivalents=self.equivalents.get(),
                               _description=self.description.get("1.0", END),
                               _card_file_path=self.card_file_path)
        card_image = card_maker.get_card()
        print("make_card done!")
        return card_image

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('image files', '.png')], initialdir="../" + PROJECT_DIR)
        p = file_path.split('/')
        counter = 0
        while True:
            if p[counter] == 'data':
                break
            counter += 1
        path = '/' + '/'.join(p[counter:])
        path = path[1:]
        path = path.replace("\n", "")
        path = "../" + path
        # self.update_coin_image(path)
        # self.update_card_image()

        self.COIN_DATA.iloc[int(self.index.get()), 7] = path
        # self.image_file_path.delete('1.0', END)
        # self.image_file_path.insert('1.0', path)
        self.image_file_path["text"] = path
        self.save_xls()
        self.open_image_window()
        print("open_image done!")

    def update_coin_image(self, _image_path):
        self.img = Image.open(_image_path)
        self.coin_photo = ImageTk.PhotoImage(self.img)
        self.coin_image_panel.configure(image=self.coin_photo)
        self.coin_image_panel.image = self.coin_photo

    def update_card_image(self):
        # self.card_img = self.make_card()
        # self.card_photo = ImageTk.PhotoImage(self.card_img)
        # self.card_image_panel.configure(image=self.card_photo)
        # self.card_image_panel.image = self.card_photo
        print("update_card_image done!")

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
                 _image_file_path=DEFAULT_IMAGE,
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


root = tk.Tk()
CoinCardMakerGUI(root)
root.mainloop()
