import openai
from os import environ

# Set the OpenAI API key from the environment variable
openai.api_key = environ.get('OPENAI_API_KEY')
client = openai.Client()