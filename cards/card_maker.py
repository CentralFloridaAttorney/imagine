import tkinter as tk
from tkinter import filedialog, Label, Entry, Menu, Text, Button

from PIL import Image, ImageTk, ImageFont, ImageDraw

BASE_DIR = "../data/"


class CardMakerGUI:
    def __init__(self, master):
        # display = ImageTk.PhotoImage(Image.open(BASE_DIR+"png/default_item.png"))
        # label = Label(image=display)
        # label.pack()
        self.card_maker = None
        self.master = master
        master.title('CardMaker')

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
        weight_label = tk.Label(root, text="Weight: ")
        weight_label.grid(row=1, column=0, rowspan=1, padx=5, pady=5)
        self.weight = Entry(master)
        self.weight.grid(row=1, column=1, rowspan=1, padx=5, pady=5)
        description_label = tk.Label(root, text="Description: ")
        description_label.grid(row=2, column=0, rowspan=1, padx=5, pady=5)
        self.description = Entry(master)
        self.description.grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        type_label = tk.Label(root, text="Type: ")
        type_label.grid(row=3, column=0, rowspan=1, padx=5, pady=5)
        self.type = Entry(master)
        self.type.grid(row=3, column=1, rowspan=1, padx=5, pady=5)
        damage_label = tk.Label(root, text="Damage: ")
        damage_label.grid(row=4, column=0, rowspan=1, padx=5, pady=5)
        self.damage = Entry(master)
        self.damage.grid(row=4, column=1, rowspan=1, padx=5, pady=5)
        range_label = tk.Label(root, text="Range: ")
        range_label.grid(row=5, column=0, rowspan=1, padx=5, pady=5)
        self.range = Entry(master)
        self.range.grid(row=5, column=1, rowspan=1, padx=5, pady=5)
        properties_label = tk.Label(root, text="Properties: ")
        properties_label.grid(row=6, column=0, rowspan=1, padx=5, pady=5)
        self.properties = Entry(master)
        self.properties.grid(row=6, column=1, rowspan=1, padx=5, pady=5)
        self.open_file_button = Button(master, text="Open Item Image", command=self.open_image)
        self.open_file_button.grid(row=7, column=0, rowspan=1, padx=5, pady=5)
        self.btn_make_card = Button(root, text='Make Card', command=self.make_card)
        self.btn_make_card.grid(row=8, column=0, rowspan=1, padx=5, pady=5)
        self.insert_button = Button(master, text="Insert", command=self.insert_text_area)





    def make_card(self):
        card_image = self.card_maker.make_card()
        print("make_card done!")
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('image files', '.png')], initialdir=BASE_DIR)
        self.card_maker = Cardmaker(_item_image=Image.open(file_path),
                                    _name=self.name.get(), _weight=self.weight.get(), _description=self.description.get(),
                                    _type=self.type.get(), _damage=self.damage.get(), _range=self.range.get(), _properties=self.properties.get())
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
    def __init__(self, _item_image=None, _background=None,
                 _name="Rations", _weight="2 lb.", _type="", _damage="", _range="", _properties="",
                 _description="Rations consist of dry foods suitable for extended Travel, including jerky, dried fruit, hardtack, and nuts."):
        if _item_image is None:
            self.item_image = Image.open(BASE_DIR + "dnd/equipment/rations/536_688_559.png").convert("RGBA")
        else:
            self.item_image = _item_image.convert("RGBA")
        if _background is None:
            self.background = Image.open(BASE_DIR + "png/card_template_v001.png").convert("RGBA")
        else:
            self.background = _background.convert("RGBA")
        self.name = _name
        self.weight = _weight
        self.type = _type
        self.damage = _damage
        self.range = _range
        self.properties = _properties
        self.description = _description
    def make_card(self):
        self.background.paste(self.item_image, (31, 36), mask=self.item_image)
        import textwrap
        font_type = ImageFont.truetype(BASE_DIR + "ttf/arial.ttf", 24)
        foreground = (0,0,0,255)
        draw = ImageDraw.Draw(self.background)
        draw.text((34, 5), self.name, font=font_type, fill=foreground)
        draw.text((46, 970), "Weight: " + self.weight, font=font_type, fill=foreground)
        novo = textwrap.wrap(self.description, width=64)
        for row in range(0, len(novo), 1):
            y_position = 650+(36*row)
            # font = ImageFont.load_default()

            draw.text((46, y_position), novo[row], font=font_type, fill=foreground)
        # Displaying the image
        self.background.save("output/"+self.name+".png")
        print("make_card done!")


root = tk.Tk()
CardMakerGUI(root)
root.mainloop()
