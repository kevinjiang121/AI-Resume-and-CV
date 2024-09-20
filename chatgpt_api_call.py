from openai import OpenAI
import config  

def get_chatgpt_response(prompt, model="gpt-3.5-turbo-instruct", max_tokens=120, temperature=0.05):
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    response = client.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    answer = response.choices[0].text.strip()
    return answer

user_prompt = input("Enter your prompt for ChatGPT: ")
if user_prompt:
    response = get_chatgpt_response(user_prompt)
    print("\nChatGPT's Response:")
    print("-------------------")
    print(response)
else:
    print("No prompt entered. Exiting.")