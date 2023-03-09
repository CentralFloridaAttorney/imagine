import random
import re

from transformers import pipeline, set_seed

gpt2_pipe = pipeline('text-generation', model='Gustavosta/MagicPrompt-Stable-Diffusion', tokenizer='gpt2')
with open("../../data/txt/ideas.txt", "r") as f:
    line = f.readlines()

MAX_WORDS = 70

def generate(starting_text):
    starting_text = starting_text.replace("\n", " ")
    seed = random.randint(100, 1000000)
    set_seed(seed)

    if starting_text == "":
        starting_text: str = line[random.randrange(0, len(line))].replace("\n", "").lower().capitalize()
        starting_text: str = re.sub(r"[,:\-–.!;?_]", '', starting_text)

    response = gpt2_pipe(starting_text, max_length=MAX_WORDS, num_return_sequences=5)
    response_list = []
    for x in response:
        resp = x['generated_text'].strip()
        if resp != starting_text and len(resp) > (len(starting_text) + 4) and resp.endswith((":", "-", "—")) is False:
            response_list.append(resp+'\n')

    return response_list



examples = []
for x in range(8):
    examples.append(line[random.randrange(0, len(line))].replace("\n", "").lower().capitalize())

print("done!")
