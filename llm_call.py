from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI() 

response = client.responses.create(model='gpt-5.4-mini',
                                   input="Who is the prime minister of india")

print(response.output_text)

