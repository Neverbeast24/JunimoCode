def custom_input(prompt = ''): 
    value_str = input(prompt)
    
    # Check for integer
    if value_str.isdigit() or (value_str[0] in ('-', '+') and value_str[1:].isdigit()):
        return int(value_str)
    
    # Check for float
    try:
        float_value = float(value_str)
        # Check if it is a float representation
        if '.' in value_str or 'e' in value_str or 'E' in value_str:
            return float_value
    except ValueError:
        pass
    
    # If neither, return as string
    return value_str

def load_dict_from_file(filename):
    my_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            my_dict[key] = value
    # with open(filename, 'w') as file:
    #     file.write('')
    return my_dict

def read_list_from_file(filename):
    my_list = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line == '\n':
                my_list.append('\n')
            else:
                my_list.append(line.strip('\n'))
    return my_list

def custom_print(*args):
    result = []
    for value in args:
        if value is None:
            result.append("void")
        elif value is True:
            result.append("true")
        else:
            result.append(str(value))
    print("".join(result), end = '')

def append(List, value):
    if value == 'true':
        List.append(True)
    else:

    # print("List: ", List)
    # print("value:", value)
        List.append(value)
    # print("new list: ", List)
    return List

def remove(List,value):
    try:
        
        List.remove(value)
    except ValueError:
        raise ValueError(f"Value {value} not found in list.")
    return List

def remove_at_index(List,index):
    try:
        del List[index]
    except IndexError:
        raise IndexError(f"Index {index} is out of range.")
    return List

def length(item):
    length_val = len(item)
    return length_val

class void:
    def __repr__(self) -> str:
        return "void"