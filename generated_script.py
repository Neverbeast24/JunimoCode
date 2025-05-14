from built_in import custom_input, custom_print, load_dict_from_file, read_list_from_file, void, Add, Pluck, Length
import sys
import traceback
line_map = load_dict_from_file('line_map.txt')
lines = read_list_from_file('get_line.txt')
try:
    def SumSquares (N):
        I = 1
        Sum = 0
        while (I<=N): 
            Sum = (Sum+(I*I))
            I = (I+1)
        return Sum
    def Fibonacci (Limit):
        A = 0
        B = 1
        Count = 0
        while (Count<Limit): 
            custom_print("\n",A)
            Temp = (A+B)
            A = B
            B = Temp
            Count = (Count+1)
        return 0
    def IsPrime (Num):
        I = 2
        IsPrime = 1
        while (I<Num): 
            if ((Num%I)==0):
                IsPrime = 0
                break
            I = (I+1)
        if (Num<=1):
            IsPrime = 0
        return IsPrime
    def Factorial (N):
        Fact = 1
        I = 1
        while (I<=N): 
            Fact = (Fact*I)
            I = (I+1)
        return Fact
    Choice =  custom_input("Choose an operation:\n1 = Sum of Squares\n2 = Fibonacci\n3 = Prime Check\n4 = Factorial\nYour choice: ")
    if (Choice==1):
        N =  custom_input("Enter a number: ")
        Result = SumSquares(N)
        custom_print("Sum of Squares is:",Result)
    if (Choice==2):
        N =  custom_input("Enter number of Fibonacci terms: ")
        Fibonacci(N)
    if (Choice==3):
        N =  custom_input("Enter a number to check if it's prime: ")
        Result = IsPrime(N)
        if (Result==1):
            custom_print("The number is prime.")
        else:
            custom_print("The number is not prime.")
    if (Choice==4):
        N =  custom_input("Enter a number to compute factorial: ")
        Result = Factorial(N)
        custom_print("Factorial is:",Result)
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