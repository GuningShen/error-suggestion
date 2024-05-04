import pandas as pd
from openai import OpenAI
import re

client = OpenAI()

error_list = []

def chat_window(df):
    unparsed_full_command_list = df["full_command"].to_list()
    unparsed_error_list = df["stderr"].to_list()

    # get a list of 3 full command before and after each error
    unparsed_error_window = get_command_window(unparsed_full_command_list, unparsed_error_list)
    return unparsed_error_window

def get_command_window(full_command_list, error_list, window_size=5):
    # extract previous 5 commands and the error command for each error
    # return a list of command windows that each contains a 5 previous commands and a error command
    # all commands are in the form of a tuple (full_command, error)

    command_collection = []
    for i in range(len(full_command_list)):
        if (not pd.isna(error_list[i])) and (error_list[i] != 'None'):
            w = []
            for j in range(i-window_size,i+1):
                if (j >= 0 | j < len(full_command_list)):
                    if (j == i):
                        command_tuple = tuple((full_command_list[j], error_list[i]))
                    else:
                        command_tuple = tuple((full_command_list[j], 'None'))
                    w.append(command_tuple);
            
            command_collection.append(w)
    return command_collection

def send_to_chatgpt(commands):

    messg = parse_error_msg(commands)
    print("----- openAI request -----")
    print(messg)

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Following this message, I will give you a sequence of commands and associated errors. For each command and error, I will also give you a history of commands executed before the error causing commands. Please indicate how they can fix the error based on the exercise that requires them to execute the associated command. Please provide one suggestion of a command on how to correct the error and enclose the command type (e.g. ls, cd, mkdir are command types) with angular brackets."},
            {"role": "user", "content": messg},
        ]
    )

    sugg = parse_suggestion(completion.choices[0].message.content)
    return sugg

def parse_error_msg(commands):
   
    # Extract the previous 5 commands
    previous_commands = commands[:-1]
    error_command = commands[-1]

    # Create sentences for the previous commands
    previous_commands_sentences = [
        f"Command {i + 1}: '{cmd}' executed successfully." for i, (cmd, status) in enumerate(previous_commands)
    ]

    # Create a sentence for the error command
    error_command_sentence = (
        f"Command {len(commands)}: '{error_command[0]}' failed with error: {error_command[1]}"
    )

    # Combine all sentences
    message = "Previous 5 commands were:\n" + "\n".join(previous_commands_sentences)
    message += "\n" + error_command_sentence

    return message


def parse_suggestion(messg):
    # parse the suggestion from the chatGPT response. Only extract part enclosed in angular brackets

    print("----- openAI response -----")
    print(messg)

    match = re.search(r'<(.*?)>', messg)

    if match:
        return match.group(1)
    else:
        return None