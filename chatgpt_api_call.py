# chatgpt_api_call.py

import os
from dotenv import load_dotenv
from openai import OpenAI  # Ensure this import is correct based on your OpenAI library usage
import load_template
import json
from read_experience import read_experience

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from environment variables
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def openai_assistant_call(prompt, name):
    """
    Sends a prompt to the OpenAI assistant and prints the response.

    Parameters:
    - prompt (str): The user's input prompt.
    - name (str): The name to address the user as in the assistant's response.
    """
    experience = str(read_experience())
    payload = prompt + " \n" + experience
    
    try:
        # Send a message to the thread with the user-provided prompt
        message = client.beta.threads.messages.create(
            thread_id=os.getenv('THREAD_ID'),
            role="user",
            content=payload
        )

        # Create and poll a run
        run = client.beta.threads.runs.create_and_poll(
            thread_id=os.getenv('THREAD_ID'),
            assistant_id=os.getenv('ASSISTANT_ID')
        )

        # Check run status and print response
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=os.getenv('THREAD_ID')
            )
            last_message = messages.data[0]
            response = last_message.content[0].text.value
            print(response)
        else:
            print(f"Run status: {run.status}")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_thread_history(thread_id):
    """
    Retrieves and prints the message history of a given thread.

    Parameters:
    - thread_id (str): The ID of the thread to retrieve messages from.
    """
    try:
        thread_messages = client.beta.threads.messages.list(thread_id)
        thread_list = [threads.content[0].text.value for threads in thread_messages]
        print(thread_list)
    except Exception as e:
        print(f"An error occurred while fetching thread history: {e}")

# Example of calling the function with a user-provided prompt
if __name__ == "__main__":
    print(read_experience())