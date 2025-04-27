from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, Add, Pluck, Length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    custom_print("Enter 5 numbers to sort:\n")
    N1 =  custom_input("Number 1: ")
    N2 =  custom_input("Number 2: ")
    N3 =  custom_input("Number 3: ")
    N4 =  custom_input("Number 4: ")
    N5 =  custom_input("Number 5: ")
    Swapped = 1
    Temp = 0
    while (Swapped==1): 
        Swapped = 0
        if (N1>N2):
            Temp = N1
            N1 = N2
            N2 = Temp
            Swapped = 1
        if (N2>N3):
            Temp = N2
            N2 = N3
            N3 = Temp
            Swapped = 1
        if (N3>N4):
            Temp = N3
            N3 = N4
            N4 = Temp
            Swapped = 1
        if (N4>N5):
            Temp = N4
            N4 = N5
            N5 = Temp
            Swapped = 1
    custom_print("Ascending: ",N1," ",N2," ",N3," ",N4," ",N5)
    custom_print("\nDescending: ",N5," ",N4," ",N3," ",N2," ",N1)
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