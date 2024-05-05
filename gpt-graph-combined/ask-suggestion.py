from gpt import send_to_chatgpt, chat_window
from graph import error_window, construct_graph, solution_prediction
import os
import pandas as pd
import sys
import openai

def main():
    # Check if the file path argument is passed
    if len(sys.argv) < 3:
        print("Usage: python script.py <error_csv_file> <error_suggestion_file>")
        sys.exit(1)
    
    # Get the file path from the command line argument
    error_file_path = sys.argv[1]
    suggestion_file_path = sys.argv[2]
    
    # Read the CSV into a DataFrame
    try:
        error = pd.read_csv(error_file_path)
    except FileNotFoundError:
        print(f"File not found: {suggestion_file_path}")
        sys.exit(1)
    
    try:
        suggestion = pd.read_csv(suggestion_file_path)
    except FileNotFoundError:
        print(f"File not found: {suggestion_file_path}")
        sys.exit(1)

    # Compute graph solution
    solutions = pd.DataFrame()
    solutions["error"] = suggestion["error"]
    solutions["correct_response"] = suggestion["suggestion"]
    solutions['graph_prediction'] = [""] * len(suggestion)
    solutions['graph_accuracy'] = [0] * len(suggestion)
    solutions['chatgpt_prediction'] = [""] * len(suggestion)
    solutions['chatgpt_section'] = [""] * len(suggestion)
    solutions['chatgpt_accuracy'] = [0] * len(suggestion)

    graph_solution(error, suggestion, solutions)

    # Compute ChatGPT solution
    chatgpt_solution(error, suggestion, solutions)

    # Save the solutions to a CSV file
    output_file = "../output_data/solutions.csv"
    solutions.to_csv(output_file, index=False)

def graph_solution(error, suggestion, solutions):
    # Parse error file into error window
    err_window = error_window(error)
    # Construct the graph
    graph = construct_graph(err_window)
    
    # Predict the suggestion
    for i in range(len(suggestion)):
        prediction = solution_prediction(suggestion["error"][i], graph)
        accuracy = compute_accuracy(prediction, suggestion["suggestion"][i])
        solutions.loc[i, 'graph_prediction'] = prediction
        solutions.loc[i, 'graph_accuracy'] = accuracy

def chatgpt_solution(error, suggestion, solutions):
    ch_window = chat_window(error)
    
    # file_path = "../input_data/tutorial-noquiz.txt"
    # response = openai.File.create(
    # file=open(file_path, "rb"),
    # purpose="answers"
    # )

    # file_id = response['id']
    # print(f"Uploaded file ID: {file_id}")

    # Read the file content into a string
    # with open(file_path, "r") as file:
    #     bash_tutorial_content = file.read()

    # Send the error window to ChatGPT
    for i in range(len(suggestion)):
        prediction, section = send_to_chatgpt(ch_window[i])
        accuracy = compute_accuracy(prediction, suggestion["suggestion"][i])
        solutions.loc[i, 'chatgpt_prediction'] = prediction
        solutions.loc[i, 'chatgpt_section'] = section
        solutions.loc[i, 'chatgpt_accuracy'] = accuracy

def compute_accuracy(prediction, answer):
    # Check if the prediction is correct
    if prediction == answer:
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()