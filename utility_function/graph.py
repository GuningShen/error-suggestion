import pprint
pp = pprint.PrettyPrinter(indent = 4)

class Node:

    def __init__(self, program, frequency = 1) -> None:
        ''' 
        Args:
            program (String): Program that Node represents
            frequency (int): amount of times in data command proceeds parent_command
           
            command (dict): Full commands with frequencies to be used by parent nodes
            children (dict): dict of children nodes, key command, value Node
        '''
        
        self.program = program
        self.frequency = frequency
        self.commands = {} # key cmd, value frequency
        self.children = {}

    # take children with the X highest frequencies
    # cut off the program
    # Remove previous_command parameter
    def get_prediction(self, previous_command, num_to_return = 5) -> str:
        
        child_nodes = list(self.children.values())
        # don't need this sort
        child_nodes.sort(key = lambda node: node.frequency)
        # get all child_nodes commands into one dict to sort
        command_dicts = {}
        for i in range(len(child_nodes)): 
            command_dicts.update(child_nodes[i].commands)

        # no need to sort this here since already sorting at end
        # comment this out later before commit
        # potential_commands = sorted(command_dicts.items(), key=lambda item : item[1], reverse=True)
        potential_commands = command_dicts.items()
        
        #fuzzy match now with command parameter
        #print(potential_commands)
        return_command = 'None'
        highest_score = 0

        potential_commands_scored = {}

        for potential_command in potential_commands:

            # fuzzy_score = fuzz.ratio(previous_command, potential_command[0])

            #set ratio to 1 incase no match; intent of fuzzy ratio is to match with args
            # if fuzzy_score == 0:
            #     fuzzy_score = 1

            # cur_score = int((.5 * fuzzy_score) * potential_command[1])
            cur_score = potential_command[1]

            potential_commands_scored[potential_command[0]] = cur_score

            
            if (cur_score > highest_score):
                return_command = potential_command[0]
                highest_score = cur_score

        return sorted(potential_commands_scored.items(), key=lambda item : item[1], reverse=True)[:num_to_return]