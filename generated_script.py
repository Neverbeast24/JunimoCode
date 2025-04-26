from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, Add, Pluck, Length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    A =  custom_input("Enter number: ")
    Fib = []
    if (A==0):
        Add(Fib,0)
    elif (A==1):
        Add(Fib,0)
    else:
        Add(Fib,0)
        Add(Fib,1)
        Int = 2
        while (Int<A): 
            Next = (Fib[(Int-1)]+Fib[(Int-2)])
            Add(Fib)
            Int+=1
    Index = (A-1)
    while (Index>=0): 
        custom_print(Fib[Index]," ")
        Index = (Index-1)
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