from openai import OpenAI
import config  # Ensure config.py contains your OPENAI_API_KEY

client = client = OpenAI(api_key=config.OPENAI_API_KEY)

client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt="Say this is a test",
  max_tokens=7,
  temperature=0
)