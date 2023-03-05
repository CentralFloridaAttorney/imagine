# Example of usage
from transformers import pipeline

story_gen = pipeline("text-generation", "pranavpsv/gpt2-genre-story-generator")
print(story_gen("<BOS> <superhero> I flew through the air"))
