from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, append, remove, length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    def RightTriangle ():
        custom_print("   *\n")
        custom_print("  ***\n")
        custom_print(" *****\n")
        custom_print("*******\n")
        return None
    def Square ():
        custom_print("****\n")
        custom_print("****\n")
        custom_print("****\n")
        custom_print("****\n")
        return None
    def Rectangle ():
        custom_print("*******\n")
        custom_print("*******\n")
        custom_print("*******\n")
        return None
    def InvertedRightTriangle ():
        custom_print("****\n")
        custom_print("***\n")
        custom_print("**\n")
        custom_print("*\n")
        return None
    def IsoscelesTriangle ():
        custom_print("   *\n")
        custom_print("  ***\n")
        custom_print(" *****\n")
        custom_print("*******\n")
        return None
    custom_print("Choose a shape:\n")
    custom_print("1 - Right Triangle\n")
    custom_print("2 - Square\n")
    custom_print("3 - Rectangle\n")
    custom_print("4 - Inverted Right Triangle\n")
    custom_print("5 - Isosceles Triangle\n")
    Choice =  custom_input("Enter choice (1-5): ")
    if (Choice==1):
        RightTriangle()
    elif (Choice==2):
        Square()
    elif (Choice==3):
        Rectangle()
    elif (Choice==4):
        InvertedRightTriangle()
    elif (Choice==5):
        IsoscelesTriangle()
    else:
        custom_print("Invalid Choice!")
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