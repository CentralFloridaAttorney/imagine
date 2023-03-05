import random
import re
import tkinter as tk
from transformers import pipeline, set_seed

gpt2_pipe = pipeline('text-generation', model='Gustavosta/MagicPrompt-Stable-Diffusion', tokenizer='gpt2')
with open("../data/txt/ideas.txt", "r") as f:
    line = f.readlines()


def generate(_starting_text="A large mound of dirt.", _tk_root=None):
    starting_text = _starting_text.replace("\n", " ")
    seed = random.randint(100, 1000000)
    set_seed(seed)
    if starting_text == "":
        starting_text: str = line[random.randrange(0, len(line))].replace("\n", "").lower().capitalize()
        starting_text: str = re.sub(r"[,:\-–.!;?_]", '', starting_text)
    response = gpt2_pipe(starting_text, max_length=(random.randint(67, 77)), num_return_sequences=5)
    response_list = []
    for x in response:
        resp = x['generated_text'].strip()
        if resp != starting_text and len(resp) > (len(starting_text) + 4) and resp.endswith((":", "-", "—")) is False:
            response_list.append(resp+'\n')
    if _tk_root is not None:
        new_window = tk.Toplevel(_tk_root)
        prompt_string = ""
        for row in range(0, len(response_list), 1):
            prompt_string += response_list[row] + " *** "
        revised_prompt_label = tk.Text(new_window, font=('Helvetica bold', 40))
        revised_prompt_label.insert("1.0", prompt_string)
        revised_prompt_label.pack()
        new_window.title("Example Prompts")
        new_window.mainloop()
    return response_list



examples = []
for x in range(8):
    examples.append(line[random.randrange(0, len(line))].replace("\n", "").lower().capitalize())

print("done!")
