# Example of usage
from transformers import pipeline

story_gen = pipeline("text-generation", "pranavpsv/gpt2-genre-story-generator")
print(story_gen("<BOS> <Trading Card Description> Write a 400 word description of a 1st level magic user."))
