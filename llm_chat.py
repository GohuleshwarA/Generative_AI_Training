from llm_call import client

History=[] #Consider memory of LLM

while True:

    user_prompt = input("user:")

    History.append({"role":"user",
                    "content":user_prompt})

    if user_prompt=="Stop":
        print("AI :"+ "Thank You")
        break

    response = client.responses.create(model='gpt-5.4-mini',
                                       input=History)

    History.append({"role":"assistant",
                    "response":response})
    
    print("AI :"+ response.output_text)


    