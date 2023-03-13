import os

import gradio as gr
BASE_PATH = os.path.dirname(__file__).rstrip("huggingface/tokenmaker") + "/imagine/"


with gr.Blocks() as demo:
    DATA_DIR = BASE_PATH + "data/dnd/coins/cp/"
    images = []

    for path in os.listdir(DATA_DIR):
        if os.path.isfile(os.path.join(DATA_DIR, path)):
            if path.endswith(".png"):
                images.append("./data/dnd/coins/cp/" + path)
    print(images)

    with gr.Tab("Make Image"):
        with gr.Row():
            gr.Gallery(value=images)
        with gr.Row():
            text1 = gr.Textbox(label="t1")
            slider2 = gr.Textbox(label="s2")
            drop3 = gr.Dropdown(["a", "b", "c"], label="d3")
        with gr.Row():
            with gr.Column(scale=1, min_width=600):
                text1 = gr.Textbox(label="prompt 1")
                text2 = gr.Textbox(label="prompt 2")
                inbtw = gr.Button("Between")
                text4 = gr.Textbox(label="prompt 1")
                text5 = gr.Textbox(label="prompt 2")
            with gr.Column(scale=2, min_width=600):
                img1 = gr.Image()
                btn = gr.Button("Go").style(full_width=True)


demo.launch()
