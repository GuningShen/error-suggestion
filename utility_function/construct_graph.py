from graph import Node

def adjust_session(session, frequencies = []):
    if len(session) == 2:
        if session[0] == session[1]:
            session = [session[0]]
            frequencies = [2]
        else:
            frequencies = [1] * len(session)
    elif len(session) == 3:
        if session[0] == session[1] and session[0] == session[2]:
            session = session[:1]
            frequencies = [3]
        else:
            frequencies = [1] * len(session)
    elif len(session) == 4:
        if session[0] == session[2] and session[1] == session[3]:
            session = [session[0], session[1]]
            frequencies = [2, 2]
        else:
            frequencies = [1] * len(session)
    elif len(session) == 5:
        if session[0] == session[1] and session[0] == session[2]:
            session = [session[0], session[3], session[4]]
            frequencies = [3, 1, 1]
        elif session[0] == session[2] and session[1] == session[3]:
            session = [session[0], session[1], session[4]]
            frequencies = [2, 2, 1]
        else:
            frequencies = [1] * len(session)
    else:
        frequencies = [1] * len(session)

    return session, frequencies

def construct_graph(command_list, command_dict={}):

    filter_empty = lambda x: (len(x) > 0)
    cur_node = None
    child_node = None
    
    for session in command_list:
        # remove commands of length 0 ( not good to modify list within loop )
        session = list(filter(filter_empty, session))

        try: 
            first_cmd = session[0]
        except Exception as inst:
            print(session)
            continue

        program = session[0].split()[0]

        # change this to frequency array of length program
        # and add frequency based on index to it    
        freq_addition = []
        session, freq_addition = adjust_session(session=session)

        if command_dict.get(program) is None:
            cur_node = Node(program=program, frequency=freq_addition[0])
            command_dict[program] = cur_node 
        else:
            cur_node = command_dict.get(program)
            cur_node.frequency += freq_addition[0]
        
        # what does this do?
        if cur_node.commands.get(first_cmd) is None:
            cur_node.commands[first_cmd] = freq_addition[0]
        else:
            cur_node.commands[first_cmd] += freq_addition[0]

        for cmd in range(1, len(session)):

            # remove
            if cmd >= len(freq_addition):
                    print(session, len(session))
                    print(freq_addition, len(freq_addition))

            if session[cmd].isprintable() is False:
                break
            else:
                program = session[cmd].split()[0]

            if cur_node.children.get(program) is None:
                child_node = Node(program = program, frequency=freq_addition[cmd])
                cur_node.children[program] = child_node
            else:
                child_node = cur_node.children.get(program)
                child_node.frequency += freq_addition[cmd]
            
            # ?????
            if child_node.commands.get(session[cmd]) is None:
                child_node.commands[session[cmd]] = freq_addition[cmd]
            else:
                child_node.commands[session[cmd]] += freq_addition[cmd]
            
            cur_node = child_node
        
    return command_dict

def get_prediction(command_list: list[str], graph, result_size=5, graph_depth=4):
    if len(command_list) == 0:
        return None

    commands = command_list[:graph_depth]
    # should be labeled last command
    last_command = command_list[graph_depth]

    if len(commands) == 0:
        return None, [-1]

    program = commands[0].split()[0]

    frequencies = []
    
    if graph.get(program) is None:
        frequencies.append(-1)
        return None, frequencies
    else:
        node = graph[program]
        frequencies.append(node.frequency)

    for command in commands[1:]:
        program = command.split()[0]
        if node.children.get(program) is not None:
            node = node.children[program]
            frequencies.append(node.frequency)
        else:
            frequencies.append(-1)
            return None, frequencies
    
    # last frequency if it has it
    next_program = last_command.split()[0]

    if node.children.get(next_program) is not None:
        frequencies.append(node.children[next_program].frequency)
    else:
        frequencies.append(-1)
    
    # previous command should be command_list[depth-1]
    return node.get_prediction(previous_command=command_list[graph_depth-1], num_to_return=result_size), frequencies