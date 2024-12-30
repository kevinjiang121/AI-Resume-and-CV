import json
import random
from dotenv import load_dotenv
import random
import websocket_handler as wh

load_dotenv()

# Define the path to the JSON file
json_file_path = None

# Chat Call
def call_comfy_ui_chat(prompt_input, file_path):
    global json_file_path
    json_file_path = file_path
    input_index = get_index_of_nodes_chat()
    prompt_text_index = input_index[0]
    print("Chat Generation Request Recieved")
    with open(json_file_path, 'r') as file:
        prompt = json.load(file)

    prompt[prompt_text_index]["inputs"]["string"] =  prompt[prompt_text_index]["inputs"]["string"] + prompt_input

    chat = wh.get_files(prompt)
    return chat

def get_chat_output(prompt_input, file_path):
    chats = call_comfy_ui_chat(prompt_input, file_path)
    output_index = get_index_of_nodes_chat()[1]
    chat = chats[output_index][0]
    return chat

def get_index_of_nodes_chat():
    prompt = None
    output = None
    json_file_path = "Local LLM Layouts/Cover Letter.json"
    print(json_file_path)

    with open(json_file_path, 'r') as file:
        input_graph = json.load(file)
    
    for index, data in input_graph.items():
        print(data)
        if data["_meta"]["title"] == "User Prompt":
            prompt = index
        if data["_meta"]["title"] == "Show Text":
            output = index

    return prompt, output

if __name__ == "__main__":
    print(get_chat_output("Software Engineer position at Google", "Local LLM Layouts/Cover Letter.json"))