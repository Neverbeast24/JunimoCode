from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, append, remove, length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    def Multiply (Val1,Val2):
        Product = (Val1*Val2)
        return Product
    def Divide (Val1,Val2):
        Quotient = (Val1*Val2)
        return Quotient
    def Add (A,B):
        Sum = (A+B)
        return Sum
    def Subtract (A,B):
        Difference = (A-B)
        return Difference
    A =  custom_input("Enter first number: ")
    B =  custom_input("Enter second number: ")
    Product = Multiply(A,B)
    Quotient = Divide(A,B)
    Sum = Add(A,B)
    Difference = Subtract(A,B)
    custom_print("Product: ",Product)
    custom_print("\n")
    custom_print("Quotient: ",Quotient)
    custom_print("\n")
    custom_print("Sum:  ",Sum)
    custom_print("\n")
    custom_print("Difference:  ",Difference)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb = traceback.extract_tb(e.__traceback__)
    print('-------------')
    print(f'Runtime Error: {e}')
    for frame in tb:
        _, line_number, func_name, text = frame
        if func_name == '<module>':
            func_name = 'galaxy()'
        try:
            print(f'File <{func_name}>, line {line_map[str(line_number)]}')
            index = int(line_map[str(line_number)])
            print(f'{lines[index-1]}')
        except:
            pass