from openai import OpenAI 

client = OpenAI(api_key='OPENAI_API_KEY')

response = client.responses.create(model='gpt-5.4-mini',input="Who is the prime minister of india",
                                   instructions="Consider you as a ChatBot",
                                   temperature=0,
                                   max_output_tokens=60) #llm

print(response.output_text)

