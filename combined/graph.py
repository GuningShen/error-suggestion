import math
import pandas as pd

class Node:

    def __init__(self, program, frequency = 1, error='None') -> None:
        ''' 
        Args:
            program (String): Program that Node represents
            frequency (int): amount of times in data command proceeds parent_command
           
            command (dict): Full commands with frequencies to be used by parent nodes
            children (dict): dict of children nodes, key command, value Node
        '''
        
        self.program = program
        self.frequency = frequency
        self.error = error
        self.commands = {} # key cmd, value frequency
        self.children = {}

def error_window(df):
    # get a list of unparsed command history
    unparsed_full_command_list = df["full_command"].to_list()
    unparsed_command_list = df["command"].to_list()
    unparsed_error_list = df["stderr"].to_list()

    # get a list of 3 full command before and after each error
    unparsed_error_window = get_command_window(unparsed_full_command_list, unparsed_command_list, unparsed_error_list)
    return unparsed_error_window

def get_command_window(full_command_list, short_command_list, error_list, window_size=5):
    command_collection = [];
    for i in range(len(full_command_list)):
        if (not pd.isna(error_list[i])) and (error_list[i] != 'None'):
            w = []
            for j in range(i, i+window_size):
                if (j >= 0 | j < len(full_command_list)):
                    if (j == i):
                        command_tuple = tuple((full_command_list[j], short_command_list[j], error_list[i]))
                    else:
                        command_tuple = tuple((full_command_list[j], short_command_list[j], 'None'))
                    w.append(command_tuple);
            
            command_collection.append(w)
    
    return command_collection

def construct_graph(error_window, error_dict={}):

    cur_node = None
    child_node = None
    
    # First loop gets one command window
    for i in range(len(error_window)):
        
        error = error_window[i][0][2]
        first_cmd = error_window[i][0][1]

        if error_dict.get(error) is None:
            cur_node = Node(program=first_cmd, error=error)
            error_dict[error] = cur_node
        else:
            cur_node = error_dict.get(error)
            cur_node.frequency += 1
        
        if cur_node.commands.get(first_cmd) is None:
            cur_node.commands[first_cmd] = 1
        else:
            cur_node.commands[first_cmd] += 1

        for cmd in range(1, 3):
            program = error_window[i][cmd][1]
            full_program = error_window[i][cmd][0]

            if cur_node.children.get(program) is None:
                child_node = Node(program = program)
                cur_node.children[program] = child_node
            else:
                child_node = cur_node.children.get(program)
                child_node.frequency += 1
            
            if child_node.commands.get(full_program) is None:
                child_node.commands[full_program] = 1
            else:
                child_node.commands[full_program] += 1
            
            cur_node = child_node
        
    return error_dict


def solution_prediction(error, graph):
    cur_node = None
    child_node = None

    if graph.get(error) is None:
        return 'Not supported';
    else:
        cur_node = graph.get(error)
        
        max_frequency = -math.inf
        next_command = ''
        for child in cur_node.children:
            child_node = cur_node.children[child]
            freq = child_node.frequency
            if freq > max_frequency:
                max_frequency = freq
                next_command = child_node.program

        return next_command