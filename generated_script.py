from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, append, remove, length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    a = void()
    custom_print("please input the length of your number: ")
    a = custom_input()
    num_list = []
    i = 0
    while (i<a): 
        num = void()
        custom_print("input num ",i,": ")
        num = custom_input()
        append(num_list,num)
        i+=1
    custom_print("please input the number to check: ")
    check = void()
    check = custom_input()
    add = 0
    i = 0
    while (i<a): 
        add += ((num_list[i]*num_list[i])*num_list[i])
        i+=1
    if add==check:
        custom_print("it is an armstrong number!")
    else:
        custom_print("not an armstrong")
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