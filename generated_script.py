from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, Add, Pluck, Length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    def FloorDiv (A,B):
        Q = 0
        while (A>=B): 
            A = (A-B)
            Q = (Q+1)
        return Q
    def Modulo (A,B):
        Q = FloorDiv(A,B)
        R = (A-(Q*B))
        return R
    def Power (Base,Exponent):
        Result = 1
        I = 0
        while (I<Exponent): 
            Result = (Result*Base)
            I = (I+1)
        return Result
    Num =  custom_input("Enter a number: ")
    Original = Num
    Temp = Num
    Count = 0
    while (Temp>0): 
        Temp = FloorDiv(Temp,10)
        Count = (Count+1)
    Temp = Num
    Result = 0
    while (Temp>0): 
        Digit = Modulo(Temp,10)
        Pow = Power(Digit,Count)
        Result = (Result+Pow)
        Temp = FloorDiv(Temp,10)
    if Result==Original:
        custom_print("The number is an ARMSTRONG number.")
    else:
        custom_print("The number is NOT an Armstrong number.")
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