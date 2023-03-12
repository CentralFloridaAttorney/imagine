import tkinter
from tkinter import filedialog, Label, Entry, Menu, Text, Button, END

import pandas
from PIL import Image, ImageTk
from huggingface.cardmaker.image_generator import ImageGenerator

from token_maker import TokenMaker

COL_NAME = 0
COL_WEIGHT = 1
COL_QUANTITY = 2
COL_IMAGE_PATH = 3
# from PIL import Image, ImageFont, ImageTk


# BASE_DIR = "../"
PROJECT_DIR = "../../data/"
# COIN_DATA = pandas.read_excel("../data/xls/coin_data.xls")
# DEFAULT_IMAGE = "./background.png"
DEFAULT_IMAGE_PATH = PROJECT_DIR + "dnd/monsters/skeletons/skeleton-warrior-1_536_688_143_333.png"
COLLECTION_NAME = "dnd/"
XLS_FILE_PATH = PROJECT_DIR + "xls/official_coin_data.xls"


# FONT_TYPE = ImageFont.truetype("../data/ttf/arial.ttf", 24)


class TokenMakerGUI:
    def __init__(self, master):
        # self.prompt_generator = PromptGenerator()
        self.xls_project_data = PROJECT_DIR + "xls/official_coin_data.xls"

        self.coin_photo = None
        self.card_maker = None
        self.root = master
        # self.master.title('CoinCardMaker')
        # Create a menubar
        self.menubar = Menu(self.root)
        # Buttons
        self.previous_index_btn = Button(self.root, text="Previous", command=self.previous_index)
        self.previous_index_btn.grid(row=0, column=0, rowspan=1, padx=5, pady=5)
        self.index = Entry(self.root)
        self.index.insert(0, "0")
        self.index.grid(row=0, column=1, rowspan=1, padx=5, pady=5)
        self.next_index_btn = Button(self.root, text="Next", command=self.next_index)
        self.next_index_btn.grid(row=0, column=2, rowspan=1, padx=5, pady=5)
        self.btn_show_image = Button(self.root, text="Show Image", command=self.open_image_window)
        self.btn_show_image.grid(row=1, column=0, rowspan=1, padx=5, pady=5)
        self.open_file_button = Button(self.root, text="Open Item Image", command=self.open_image)
        self.open_file_button.grid(row=1, column=1, rowspan=1, padx=5, pady=5)
        self.btn_make_token = Button(self.root, text='Make Token', command=self.make_token)
        self.btn_make_token.grid(row=1, column=3, rowspan=1, padx=5, pady=5)
        self.load_xls_btn = Button(self.root, text="Load XLS", command=self.load_xls)
        self.load_xls_btn.grid(row=2, column=0, rowspan=1, padx=5, pady=5)
        self.generate_image_btn = Button(self.root, text="Generate Image", command=self.generate_image)
        self.generate_image_btn.grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        self.copy_last_card_btn = Button(self.root, text="Copy Current", command=self.copy_token)
        self.copy_last_card_btn.grid(row=2, column=2, rowspan=1, padx=5, pady=5)
        # Data Fields
        iterations_label = Label(self.root, text="Iterations: ")
        iterations_label.grid(row=14, column=0, rowspan=1, padx=5, pady=5)
        self.iterations = Entry(self.root)
        self.iterations.grid(row=14, column=1, rowspan=1, padx=5, pady=5)
        self.iterations.insert(0, 20)
        name_label = Label(self.root, text="Name: ")
        name_label.grid(row=15, column=0, rowspan=1, padx=5, pady=5)
        self.name = Entry(self.root)
        self.name.grid(row=15, column=1, rowspan=1, padx=5, pady=5)
        file_name_label = Label(self.root, text="File Name: ")
        file_name_label.grid(row=16, column=0, rowspan=1, padx=5, pady=5)
        self.file_name = Entry(self.root)
        self.file_name.grid(row=16, column=1, rowspan=1, padx=5, pady=5)
        collection_name_label = Label(self.root, text="Collection Name: ")
        collection_name_label.grid(row=17, column=0, rowspan=1, padx=5, pady=5)
        self.collection_name = Entry(self.root)
        self.collection_name.grid(row=17, column=1, rowspan=1, padx=5, pady=5)
        quantity_label = Label(self.root, text="Quantity: ")
        quantity_label.grid(row=18, column=0, rowspan=1, padx=5, pady=5)
        self.quantity = Entry(self.root)
        self.quantity.grid(row=18, column=1, rowspan=1, padx=5, pady=5)
        equivalent_label = Label(self.root, text="Equivalents: ")
        equivalent_label.grid(row=19, column=0, rowspan=1, padx=5, pady=5)
        self.equivalents = Entry(self.root)
        self.equivalents.grid(row=19, column=1, rowspan=1, padx=5, pady=5)

        # Create the dropdown menu
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label='New Card', command=self.copy_token)
        self.filemenu.add_command(label='Cut', command=lambda: root.focus_get().event_generate("<<Cut>>"))
        self.filemenu.add_command(label='Copy', command=lambda: root.focus_get().event_generate("<<Copy>>"))
        self.filemenu.add_command(label='Paste', command=lambda: root.focus_get().event_generate("<<Paste>>"))
        # Add the file menu to the menubar
        self.menubar.add_cascade(label='Edit', menu=self.filemenu)
        # Configure the menu with the root window as parent
        self.root.config(menu=self.menubar)

        self.ITEM_DATA = self.load_xls()
        card_file_path = DEFAULT_IMAGE_PATH.replace(".png", "_card.png")
        self.card_file_path = card_file_path

        self.image_file_path = Label(self.root, text=DEFAULT_IMAGE_PATH)
        self.image_file_path.grid(row=0, column=6, rowspan=1, padx=5, pady=5)

        description_label = Label(self.root, text="Description: ")
        description_label.grid(row=1, column=6, rowspan=1, padx=5, pady=5)
        self.description = Text(self.root, height=10)
        self.description.grid(row=2, column=6, rowspan=10, padx=5, pady=5)

        prompt_label = Label(self.root, text="Prompt: ")
        prompt_label.grid(row=4, column=9, rowspan=1, padx=5, pady=5)
        self.prompt = Text(self.root, height=10)
        self.prompt.grid(row=13, column=6, rowspan=10, padx=5, pady=5)

        # coin image
        self.img = Image.open(DEFAULT_IMAGE_PATH)
        self.coin_photo = ImageTk.PhotoImage(self.img)
        self.coin_image_panel = Label(master, image=self.coin_photo)
        self.coin_image_panel.grid(row=23, column=6, rowspan=100, padx=5, pady=5)

        # card image
        # self.card_img = self.make_card()
        # self.card_photo = ImageTk.PhotoImage(self.card_img)
        # self.card_image_panel = Label(master, image=self.card_photo)
        # self.card_image_panel.grid(row=0, column=2, rowspan=20, padx=5, pady=5)
        self.root.bind('<Return>', self.update_xls)
        self.update_data_gui()

    def update_item_data(self):
        # quantity, name, weight, image_path
        self.ITEM_DATA.iloc[int(self.index.get()), 0] = str(self.name.get())
        self.ITEM_DATA.iloc[int(self.index.get()), 1] = str(self.file_name.get())
        self.ITEM_DATA.iloc[int(self.index.get()), 2] = str(self.collection_name.get())
        self.ITEM_DATA.iloc[int(self.index.get()), 3] = str(self.quantity.get())
        self.ITEM_DATA.iloc[int(self.index.get()), 4] = str(self.description.get("1.0", END).replace("\n", ""))
        self.ITEM_DATA.iloc[int(self.index.get()), 5] = str(self.equivalents.get())
        self.ITEM_DATA.iloc[int(self.index.get()), 6] = str(self.prompt.get("1.0", END).replace("\n", ""))
        self.ITEM_DATA.iloc[int(self.index.get()), 7] = self.image_file_path["text"]
        self.save_xls()

    def update_image_gui(self):
        self.update_coin_image(self.ITEM_DATA.iloc[int(self.index.get()), COL_IMAGE_PATH])
        # self.update_card_image()

    def update_xls(self, event):
        self.update_item_data()

    def make_token(self):
        # token_maker = TokenMaker(_image_file_path=self.image_file_path["text"],
        #                        _name=self.name.get(),
        #                        _type=self.collection_name.get(),
        #                        _quantity=self.quantity.get(),
        #                        _equivalents=self.equivalents.get(),
        #                        _description=self.description.get("1.0", END),
        #                        _output_file_path=self.card_file_path)

        token_maker = TokenMaker(_image_file_path=self.image_file_path)
        token_maker.open_card_window(self.root)

    def generate_image(self):

        collection_name = COLLECTION_NAME + str(self.collection_name.get())
        image_prompt = self.prompt.get("1.0", END) + ", bokeh, photography –s 625 –q 2 –iw"
        item_image_generator = ImageGenerator(
            _prompt=image_prompt,
            _collection_name=collection_name,
            _file_name=self.file_name.get(), )
        item_image_generator.open_generator_window(self.root)
        # item_image_file_path = item_image_generator.get_image(_seed=415423, _style=123,_iterations=self.iterations.get())

        # self.update_coin_image(item_image_file_path)
        # self.update_card_image()

        # self.ITEM_DATA.iloc[int(self.index.get()), 7] = item_image_file_path
        # self.image_file_path["text"] = item_image_file_path
        # self.save_xls()
        # self.update_coin_image(item_image_file_path)

    def open_image_window(self):
        new_window = tkinter.Toplevel(self.root)
        image_path = self.ITEM_DATA.iloc[int(self.index.get()), COL_IMAGE_PATH]
        new_window.title(str(self.name.get()))
        img = Image.open(image_path)
        coin_photo = ImageTk.PhotoImage(img)
        coin_image_panel = Label(new_window, image=coin_photo)
        coin_image_panel.image = coin_photo
        coin_image_panel.pack()
        new_window.mainloop()

    def copy_token(self):
        current_row = int(self.index.get())
        data_frame = self.ITEM_DATA.loc[current_row]
        new_row = data_frame.copy().transpose()

        # Insert Dict to the dataframe using DataFrame.append()
        # new_row = {'Courses': 'Hyperion', 'Fee': 24000, 'Duration': '55days', 'Discount': 1800}
        df2 = self.ITEM_DATA.append(new_row, ignore_index=True)

        self.ITEM_DATA = df2
        print("new_card done!")

    def next_index(self):
        current_index = int(self.index.get())
        if (current_index + 1) < len(self.ITEM_DATA):
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

    def load_xls(self):
        self.ITEM_DATA = pandas.read_excel(XLS_FILE_PATH)
        return self.ITEM_DATA

    def save_xls(self):
        self.ITEM_DATA.to_excel(XLS_FILE_PATH, index=False)

    def get_token_image(self):
        token_maker = TokenMaker(_image_file_path=self.image_file_path["text"],
                                 _top_text=self.name.get(),
                                 _type=self.collection_name.get(),
                                 _quantity=self.quantity.get(),
                                 _equivalents=self.equivalents.get(),
                                 _description=self.description.get("1.0", END),
                                 _output_file_path=self.card_file_path)
        token_image = token_maker.get_token()
        print("get_token_image done!")
        return token_image

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('image files', '.png')], initialdir=PROJECT_DIR)
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

        self.ITEM_DATA.iloc[int(self.index.get()), 7] = path
        # self.image_file_path.delete('1.0', END)
        # self.image_file_path.insert('1.0', path)
        self.image_file_path["text"] = path
        self.save_xls()
        self.open_image_window()
        print("open_image done!")
        self.update_image_gui()

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

    def update_data_gui(self):
        self.name.delete(0, END)
        self.name.insert(0, self.ITEM_DATA.iloc[int(self.index.get()), 0])
        self.file_name.delete(0, END)
        self.file_name.insert(0, self.ITEM_DATA.iloc[int(self.index.get()), 3])
        self.collection_name.delete(0, END)
        self.collection_name.insert(0, self.ITEM_DATA.iloc[int(self.index.get()), 2])
        self.quantity.delete(0, END)
        self.quantity.insert(0, self.ITEM_DATA.iloc[int(self.index.get()), 2])
        self.description.delete('1.0', END)
        self.description.insert('1.0', self.ITEM_DATA.iloc[int(self.index.get()), 4])
        self.equivalents.delete(0, END)
        self.equivalents.insert(0, self.ITEM_DATA.iloc[int(self.index.get()), 5])
        self.prompt.delete('1.0', END)
        self.prompt.insert('1.0', self.ITEM_DATA.iloc[int(self.index.get()), 6])
        self.image_file_path["text"] = self.ITEM_DATA.iloc[int(self.index.get()), 3]

    def update_card_image(self):
        self.card_img = self.make_card()
        self.card_photo = ImageTk.PhotoImage(self.card_img)
        self.card_image_panel.configure(image=self.card_photo)
        self.card_image_panel.image = self.card_photo
        print("update_card_image done!")

    def update_coin_image(self, _image_path):
        try:
            self.img = Image.open(_image_path)
            self.coin_photo = ImageTk.PhotoImage(self.img)
            self.coin_image_panel.configure(image=self.coin_photo)
            self.coin_image_panel.image = self.coin_photo
        except FileNotFoundError:
            self.open_image()
            self.update_image_gui()


root = tkinter.Tk()
TokenMakerGUI(root)
root.mainloop()
