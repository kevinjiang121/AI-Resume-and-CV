from openai import OpenAI
import config 

# Initialize the OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

def openai_assistant_call(prompt, name):

    # Send a message to the thread with the user-provided prompt
    message = client.beta.threads.messages.create(
        thread_id=config.THREAD_ID,
        role="user",
        content=prompt
    )
    
    # Create and poll a run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=config.THREAD_ID,
        assistant_id=config.ASSISTANT_ID,
        instructions="Address user as " + name + ". Help with Resume and Cover Letter request"
    )
    
    # Check run status and print response
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=config.THREAD_ID
        )
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        print(response)
    else:
        print(run.status)

def get_thread_history(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    thread_list = list()
    for threads in thread_messages:
        thread_list.append(threads.content[0].text.value)
    print(thread_list)

# Example of calling the function with a user-provided prompt
if __name__ == "__main__":
    user_prompt = input("Enter your prompt for ChatGPT: ")
    openai_assistant_call(user_prompt, "John")
    # get_thread_history(config.THREAD_ID)
