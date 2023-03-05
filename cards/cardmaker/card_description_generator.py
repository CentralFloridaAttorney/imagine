from transformers import GPT2Tokenizer, GPT2LMHeadModel

model_name = "pranavpsv/gpt2-genre-story-generator"
# model_name = "rjbownes/Magic-The-Generating"

tokenizer = GPT2Tokenizer.from_pretrained(model_name)

model = GPT2LMHeadModel.from_pretrained(model_name)

from transformers import pipeline


story_gen = pipeline("text-generation", model=model_name)
print(story_gen("farmer has a problem with rats eating grain and is offering .", max_length=500))
9
# result = model("What is happening to the skeleton?", max_length=30, num_return_sequences=5)
# print(result)