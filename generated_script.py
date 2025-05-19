from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, Add, Pluck, Length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    def Multiply (A,B):
        Product = (A*B)
        return Product
    def Add (A,B):
        Product = (A+B)
        return Product
    def Minus (A,B):
        Product = (A-B)
        return Product
    def Divide (A,B):
        Product = (A/B)
        return Product
    custom_print("Multiply - 1 \n")
    custom_print("Add - 2 \n")
    custom_print("Minus - 3 \n")
    custom_print("Divide- 4 \n")
    Choice =  custom_input("Enter decision: ")
    A =  custom_input("Enter num1: ")
    B =  custom_input("Enter num2: ")
    if (Choice==1):
        custom_print("Total is: ",Multiply(A,B))
    elif (Choice==2):
        custom_print("Total is: ",Add(A,B))
    elif (Choice==3):
        custom_print("Total is: ",Minus(A,B))
    elif (Choice==4):
        custom_print("Total is: ",Divide(A,B))
    else:
        custom_print("Invalid")
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.extract_tb(e.__traceback__)
    print('-------------')
    print(f'Runtime Error: {e}')
    for frame in tb:
        _, line_number, func_name, text = frame
        if func_name == '<module>':
            func_name = 'pelican()'
        try:
            print(f'File <{func_name}>, line {line_map[str(line_number)]}')
            index = int(line_map[str(line_number)])
            print(f'{lines[index-1]}')
        except:
            pass