from itertools import count
from ctypes import windll
from strings_arrows import *
import ast
import parser_syntax


#alphabet
alpha_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyz'
all_letters = alpha + alpha_capital

#numbers
zero = '0'
number = '123456789'
all_numbers = zero + number

#alphanumeric and special symbols
punctuation_symbols = "-!@#$%^&*(}-_=+[]{)\|:;',<>./?+\""
alpha_num = all_letters + all_numbers 
ascii = all_letters + punctuation_symbols + all_numbers
ascii_string = "!@#$%^&*()-_=+[]{" + "}\|:;',<>./?+-" + all_letters + all_numbers
ascii_comment = all_letters + all_numbers + "-!@#$%^&*(-_=+[]{)\|:;',<>./?+\""
#operators
arithmetic_ops = "+-*/%"
relational_ops = '><==!<=>=!='
logical_ops = '||&&!'
unary_ops = '++--'
assignment_ops = '=+=-=*=/='
op_delim = logical_ops + arithmetic_ops + relational_ops
negative = '-'

#others
whitespace = " "
TERMINATOR = "$"
NEWTAB = '\\t'
newline_delim = '\n'
NEWLINE = "\\n"
COMMA = ','
SINGLELINE = '@}'
MULTILINE_OPEN = '@}' + '}'
MULTILINE_CLOSE =  '{' + '{@'
COMMENT = "COMMENT"
DOLLARSIGN ="$"

comma_delim = whitespace + alpha_num + '"'
dew_delim = whitespace + newline_delim + '{'
string1_delim = whitespace + ascii_string + newline_delim + '"'
string2_delim = whitespace + COMMA + '+' + ')'
string_delim = string1_delim + string2_delim
delim0 = whitespace + alpha_num + negative + '(' + '['
delim1 = whitespace + alpha_num + '"' + '(' + '['+  negative
delim2 = whitespace + alpha_num + '"' + '(' + negative
delim3 = whitespace + all_numbers + '('

unary_delim = whitespace + all_letters + TERMINATOR + ')'
bool_delim = whitespace + TERMINATOR + COMMA + ')' + ']'
num_delim = arithmetic_ops + ']' + ')' + '(' + '[' + whitespace + COMMA + relational_ops + TERMINATOR
id_delim = COMMA + whitespace + "=" + ")" + "[" + "]" + "<" + ">" + "!" + "(" + arithmetic_ops + TERMINATOR # newline
spacepr_delim = whitespace + '('
pr_delim = '('
break_delim = TERMINATOR + whitespace
openparenthesis_delim = whitespace + alpha_num + negative + '('  + '"' + ')' + newline_delim + '!' + '+' + '-' + ','
closingparenthesis_delim = whitespace  + ')' + '{' + '&' + '|' + TERMINATOR + arithmetic_ops + relational_ops + ',' + ']'
end_delim = whitespace + newline_delim
opensquare_delim = whitespace + all_numbers + '"' + ']' + alpha_capital + negative
closesquare_delim = whitespace + TERMINATOR + ')' + ','
negative_delim = alpha_capital + all_numbers + '('

comment1_delim = whitespace + ascii_comment
comment2_delim = whitespace + newline_delim + ascii

#errors
error = []

#TOKENS
ENTITY = 'entity'
#reserved words
PLANTING = 'planting' #Start
PERFECTION = 'perfection' #End

CROP = 'crop'
FARMHOUSE = 'farmhouse'
VOIDEGG = 'voidegg'

TRUE = 'true'
FALSE = 'false'

#conditional statements
STAR = 'star'
DEW = 'dew'
STARDEW = 'stardew'

#looping statements
FALL = 'fall'
WINTER = 'winter'
# do while loop

#loop control statements
BREAK = 'break'
NEXT = 'next'

#input and output statements
COLLECT = 'collect'
SHIP = 'ship'

HARVEST = 'harvest'

ADD = 'add'
PLUCK = 'pluck'
PELICAN = 'pelican'
CRAFT = 'craft'

#assignment operators | done
EQUAL = '='
PLUS_EQUAL = '+='
MINUS_EQUAL = '-='
MUL_EQUAL = '*='
DIV_EQUAL = '/='
#unary operators | done
INCRE = '++'
DECRE = '--'
NEGATIVE = '-'
#relational operators | done
E_EQUAL = '=='
NOT_EQUAL = '!='
LESS_THAN = '<'
GREATER_THAN = '>'
LESS_THAN_EQUAL = '<='
GREATER_THAN_EQUAL = '>='
#mathematical operators | done
PLUS = '+' #it can also use in string operator
MINUS = '-'
MUL = '*'
DIV = '/'
MODULUS = '%'
#logical operators
NOT_OP = '!'
AND_OP = '&&'
OR_OP = '||'

#other symbols
LPAREN = '('
RPAREN = ')'
SLBRACKET = '['
SRBRACKET = ']'
CLBRACKET = '{'
CRBRACKET = '}'

LOG_OP = NOT_OP + AND_OP + OR_OP
REL_OP = [E_EQUAL , NOT_EQUAL , LESS_THAN , GREATER_THAN , LESS_THAN_EQUAL , GREATER_THAN_EQUAL]

#literals

IDENTIFIER = 'Identifier'
STRING = "StrLit"
EOF = 'EOF'

INTEGER = 'IntLit'
FLOAT = 'FloatLit'
SPACE = 'Space'

#Base error class for all error types
class Error: # do not change
    #Stores error start and end position, name, and descriptive message
    def __init__ (self,pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self. details = details

    #Stores metadata: where error occurred, what type, and explanation
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n' #Method to format the error as a string for display
        fileDetail = f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}' # Header: error type and its reason
        errorDetail, arrowDetail = string_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) # Shows source file and line number of error
        return result, fileDetail, errorDetail, arrowDetail # Returns the error message as a string uses helper to get code snippet and pointer to error (^ underline)

#Specialized error when the lexer finds an unsupported character
#Inherits from Error class
class IllegalCharError(Error):
    #the lexer comes across a character it doesn't support
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character ', details)

#Specialized error when the lexer finds an invalid delimiter
#Raised when a wrong character follows a token (e.g., add@ instead of add()
#Custom message includes the token and cause
class DelimiterError(Error):
    def __init__(self,pos_start, pos_end, details, char):
        super().__init__(pos_start, pos_end, f"Invalid Delimiter for '{char}'", "Cause -> " + str(details))

#Raised by the parser when grammar is broken
#Inherits from Error
class InvalidSyntaxError(Error):
    def __init__(self,pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

#Raised during interpreter execution
#Includes positional metadata and explanation
#not used, semantic error yung nagamit
class RTError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        

    def as_string(self): 
        result  = self.generate_traceback()
        result_name = f"{self.error_name}: {self.details}"
        #result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        errorDetail, arrowDetail = string_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result, result_name, '\n'+ errorDetail
        #return result

    def generate_traceback(self):
        result = []
        pos = self.pos_start
        # print("pos and ctx: ", self.pos_start, " ", self.context)
        result.insert(0, f'File <Junimo Code>, line {str(self.pos_start.ln + 1)}') # Returns full visual error (traceback, message, and visual arrows)
        return result
    def print_error(self):
        print( f"details: {self.details}, pos start and end: {self.pos_start}, {self.pos_end}")\

#Almost identical to RTError, but used for semantic rules (e.g., type mismatch, undefined vars)
#Format and methods are reused for consistency
class SemanticError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Semantic Error', details)
        

    def as_string(self):
        result  = self.generate_traceback()
        result_name = f"{self.error_name}: {self.details}"
        #result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        errorDetail, arrowDetail = string_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result, result_name, '\n'+ errorDetail
        #return result

    def generate_traceback(self):
        result = []
        pos = self.pos_start
        # print("pos and ctx: ", self.pos_start, " ", self.context)
        
        
        result.insert(0, f'File <Junimo Code>, line {str(self.pos_start.ln + 1)}') 
        

        return result
    def print_error(self):
        print( f"details: {self.details}, pos start and end: {self.pos_start}, {self.pos_end}")
# Tracks the location of characters 
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx # overall character index in the file
        self.ln = ln # line number 
        self.col = col # column number \
        self.fn = fn # file name
        self.ftxt = ftxt # file text

    def advance (self, current_char=None): # Moves the position forward by one character (called as lexer reads input)
        self.idx += 1 #  Increment index
        self.col += 1

        if current_char == "\n": #If newline, go to next line and reset column to 0
            self.ln += 1
            self.col = 0

        return self # Allows chaining (e.g., pos.advance().advance())
    def copy(self): # Returns a copy of the current position
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt) # Used to save current location before advancing further (important for tokens and errors)

class Token: # Token class to represent a single token in the source code
    def __init__(self, token, value=None, pos_start=None, pos_end=None): # Constructor to initialize token type, value, and position
        self.token = token # Token type 
        self.value = value # Token value 
        
        # token: type (e.g., PLUS, CROP, IDENTIFIER)
        # value: value (e.g., 5, "hello", "crop")
        # pos_start: start position of the token
        # pos_end: end position of the token
    
        if pos_start: # If start position is provided, set start and end positions
            self.pos_start = pos_start.copy() # Use a copy to avoid mutating the original
            self.pos_end = pos_start.copy() # Advance it by one character to get the pos_end
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end # Allows overriding pos_end manually
            
    def matches(self, type_, value): # checks if a token matches both type and value 
        return self.token == type_ and self.value == value
    
    def __repr__(self):
        if self.value: return f'{self.value} : {self.token}' # If value exists: value : token_type
        return f'{self.token}' # Else: just show token type


#LEXER

class Lexer:

    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance() 

    def peek(self): # Returns the next character without moving the position (ithink not)
        next_idx = self.pos.idx + 1
        return self.text[next_idx] if next_idx < len(self.text) else None

    def advance(self): # Moves one character forward.
        self.pos.advance(self.current_char)
        # current char is the current pos if the pos is less than the length of the text
        self.current_char = self.text[self.pos.idx] if self.pos.idx <= len(self.text)-1 else None

    def make_tokens(self): # Core loop to scan current_char and build a list of tokens (tokens) and errors (errors).

        tokens = []
        errors = []
        string = ""

        while self.current_char is not None: #loop scanning the current_char
            """ if self.current_char in special_chars:
                errors.extend([f"Invalid symbol: {self.current_char}"])
                self.advance() """
            # if self.current_char in '\t':
            #     tokens.append(Token(NEWTAB, "\\t", pos_start = self.pos))
            #     self.advance()
            if self.current_char  == '\n':
                tokens.append(Token(NEWLINE, "\\n", pos_start = self.pos))
                self.advance()
            elif self.current_char.isspace():
                # Handle spaces explicitly
                while self.current_char is not None and self.current_char.isspace():
                    if self.current_char == " ":
                        tokens.append(Token(SPACE, "\" \"", pos_start = self.pos))
                    self.advance()
            elif self.current_char in alpha:
                result, error = self.make_word()

                if error:
                    errors.extend(error)

                tokens.append(result)
            elif self.current_char.isupper():  # Check for identifiers or reserved words
                ident = self.current_char
                self.advance()

                # Collect the full identifier
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
                    ident += self.current_char
                    self.advance()

                # Validate identifier or reserved word
                result, error = self.make_ident(ident)
                if result:
                    tokens.append(Token(IDENTIFIER, result, pos_start = self.pos))
                else:
                    # If it's neither a reserved word nor a valid identifier, it's invalid
                    errors.append(f"Error at line: {self.pos.ln + 1}. Invalid word: '{ident}'")

            elif self.current_char.isalpha():  # Likely invalid word starting with a lowercase letter
                ident = self.current_char
                self.advance()

                # Collect the full invalid word
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
                    ident += self.current_char
                    self.advance()

            elif self.current_char in all_numbers:
                result, error = self.make_number()
                errors.extend(error)

                if self.current_char == None or self.current_char == EOF:
                    errors.append(f"Error at line: {self.pos.ln + 1}. Invalid delimiter for {result.value}. Cause: ' {self.current_char} '.")
                else:
                    tokens.append(result)

            elif self.current_char == "\"":  # Handle string literals
                string, error = self.make_string()
                errors.extend(error)
                if string:
                    tokens.append(Token(STRING, string, pos_start = self.pos))  # Append the full string as a token
                else:
                    # Handle unknown/invalid characters
                    errors.append(f"Error at line: {self.pos.ln + 1}. Unrecognized character: {self.current_char}")
                    self.advance()
            #from here to ++
            elif self.current_char == '=': #assignment operator (=, +=, -=, *=, /=, ==)
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None: # positional error tracking 
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' == '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in (delim1):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' == '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(E_EQUAL, "==", pos_start = self.pos)) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' = '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' = '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(EQUAL, "=", pos_start = self.pos)) #for == symbol

            # elif self.current_char == '-':
            #     self.advance()
            #     if self.current_char in all_numbers:
            #         result, error = self.make_number()
            #         #result = Token(result.token, result.value * -1, pos_start, self.pos)
            #         result = Token(result.token, result.value * -1, pos_start = self.pos)
            #         tokens.append(result)  

            #     else:
            #         errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} '. 123456789"])

            elif self.current_char == '<': #relational operator
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(LESS_THAN_EQUAL, "<=", pos_start = self.pos)) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' < '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in (delim0):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' < '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(LESS_THAN, "<", pos_start = self.pos))


            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(GREATER_THAN_EQUAL, ">=", pos_start = self.pos))
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' > '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' > '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(GREATER_THAN, ">", pos_start = self.pos))


            elif self.current_char == '+': #mathematical operator (+, -, *, /, %)
                self.advance()
                if self.current_char == '=': #for += symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' += '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in (delim3):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' += '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(PLUS_EQUAL, "+=", pos_start = self.pos)) #for == symbol

                elif self.current_char == '+': #for ++ incre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ++ '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in (unary_delim) or self.current_char.isspace():
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ++ '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(INCRE, "++", pos_start = self.pos)) #for == symbol
                else:

                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' + '. Cause: ' {self.current_char} '. "])
                        continue

                    if self.current_char not in (delim1):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' + '. Cause: ' {self.current_char} '. "])
                        continue

                    tokens.append(Token(PLUS, "+", pos_start = self.pos)) #for == symbol



            elif self.current_char == '-':
                self.advance()
                if self.current_char == '=': #for -=symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim3:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(MINUS_EQUAL, "-=", pos_start = self.pos))
                elif self.current_char == '-': #for -- decre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in (unary_delim):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(DECRE, "--", pos_start = self.pos))
                elif self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' - '. Cause: ' {self.current_char} '. "])
                    continue
                else:
                    # CASE: negative number
                    if self.current_char in all_numbers:
                        print("current char negative: ", self.current_char)
                        result, error = self.make_number()
                        result = Token(result.token, result.value * -1, pos_start=self.pos)
                        tokens.append(result)
                    
                    # CASE: binary minus (e.g., A - B)
                    elif self.current_char in delim0:
                        tokens.append(Token(MINUS, "-", pos_start=self.pos))

                    # CASE: invalid delimiter
                    else:
                        errors.append(
                            f"Error at line: {self.pos.ln + 1}. Invalid delimiter for '-' operator. "
                            f"Cause: '{self.current_char}' "
                        )
                        continue
                    

            elif self.current_char == '*':
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. "])
                    if self.current_char not in delim3:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(MUL_EQUAL, "*=", pos_start = self.pos))
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' * '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' * '. Cause: ' {self.current_char} ' . "])
                        continue
                    tokens.append(Token(MUL, "*", pos_start = self.pos))



            elif self.current_char == '/':
                self.advance()
                if self.current_char == '=': #for /= symbol

                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim3:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(DIV_EQUAL, "/=", pos_start = self.pos))
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' / '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' / '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(DIV, "/", pos_start = self.pos))

            elif self.current_char == '%':
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' % '. Cause: ' {self.current_char} '. "])
                    continue
                if self.current_char not in delim0:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' % '. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(MODULUS, "%", pos_start = self.pos))

            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == '=':
                    self.advance()
                    pos_start = self.pos.copy()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' != '. Cause: ' {self.current_char} '.  "])
                        continue
                    if self.current_char not in delim2:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!=' )])
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' != '. Cause: ' {self.current_char} '.  "])
                        continue
                    print("appending !=: ", self.current_char)
                    tokens.append(Token(NOT_EQUAL, "!=", pos_start = self.pos)) #for != symbol
                else:
                    if self.current_char == None:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(NOT_OP, "!", pos_start = self.pos))

            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' && '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' && '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(AND_OP, "&&", pos_start = self.pos))

                else:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Please enter a valid symbol! User typed: & .Did you mean && ?"])
                    #self.advance()
            elif self.current_char == '|': #return error
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' || '. Cause: ' {self.current_char} '. "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' || '. Cause: ' {self.current_char} '. "])
                        continue
                    tokens.append(Token(OR_OP, "||", pos_start = self.pos))
                else:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Please enter a valid symbol! User typed: & .Did you mean && ?"])

            elif self.current_char == '"': #string 1 and string 2 delim conflict # added str1 and 2 = string_delim
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' \" '. Cause: ' {self.current_char} '.  "])
                    continue
                if self.current_char not in string_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' \" '. Cause: ' {self.current_char} '.  "])
                    continue
                tokens.append(Token(STRING, "\" \"", pos_start = self.pos))
            # add closing ' " ' for string

            elif self.current_char == "@":
                self.advance()

                # Single-line comment (@})
                if self.current_char == "}":
                    self.advance()

                    # Check if the next character is also `}` (part of `@}}` for multi-line comment)
                    if self.current_char == "}":  # Multi-line comment start
                        self.advance()
                        comment_content = ""

                        # Parse until the closing sequence {{@
                        while self.current_char is not None:
                            # Check for the closing sequence "{{@"
                            if self.current_char == "{" and self.peek() == "{" and self.text[self.pos.idx + 2] == "@":
                                self.advance()  # Advance past '{'
                                self.advance()  # Advance past '{'
                                self.advance()  # Advance past '@'
                                
                                # Remove leading and trailing whitespaces and newlines
                                comment_content = comment_content.replace("\n", "").replace("\r", "")
                                
                                # Add tokens for a valid multi-line comment
                                tokens.append(Token(MULTILINE_OPEN, "@}" + "}", pos_start = self.pos))
                                tokens.append(Token(COMMENT, comment_content.strip(), pos_start = self.pos))
                                tokens.append(Token(MULTILINE_CLOSE, "{"+ "{@", pos_start = self.pos))
                                break

                            # Append the current character to the comment content
                            if not (self.current_char.isascii() or self.current_char in comment2_delim):
                                errors.append(
                                    f"Error at line: {self.pos.ln + 1}. Invalid character '{self.current_char}' in multi-line comment."
                                )

                            comment_content += self.current_char
                            self.advance()

                        # If loop ends without finding {{@, report an error
                        else:
                            errors.append(f"Error at line: {self.pos.ln + 1}. Unclosed multi-line comment. Expected '{{@' to close.")
                            errors.append(f"Error at line: {self.pos.ln + 1}. Invalid Delimiter for Single-line Comment. ")
                            # Do not add tokens for incomplete or invalid multi-line comments
                            return tokens, errors  # Exit after reporting the errors

                    else:  # Single-line comment
                        comment_content = ""

                        # Capture the content for the single-line comment
                        while self.current_char is not None and self.current_char != "\n":  # Stop at newline_delim or EOF
                            # Validate the character
                            if not (self.current_char.isascii() or self.current_char in comment1_delim):
                                errors.append(
                                    f"Error at line: {self.pos.ln + 1}. Invalid character '{self.current_char}' in single-line comment. "
                                    f"Error at line: {self.pos.ln + 1}. "
                                )

                            comment_content += self.current_char
                            self.advance()

                        # If there are errors in the single-line comment, do not add it to the tokens
                        if errors:
                            continue

                        # Add tokens for single-line comment
                        tokens.append(Token(SINGLELINE, "@}", pos_start = self.pos))
                        tokens.append(Token(COMMENT, comment_content.strip(), pos_start = self.pos))

                        # Continue parsing other tokens after the single-line comment ends
                        continue

                # Handle invalid `@` usage
                else:
                    errors.append(f"Error at line: {self.pos.ln + 1}. Invalid use of '@'. Cause: '{self.current_char}'. ")
                    continue

            elif self.current_char == '(': #other operator
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ( '. Cause: ' {self.current_char} '.  "])
                    continue
                if self.current_char not in openparenthesis_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(LPAREN, "(", pos_start = self.pos))
            elif self.current_char == ')':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ) '. Cause: ' {self.current_char} '. "])
                    continue
                if self.current_char not in closingparenthesis_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ) '. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(RPAREN, ")", pos_start = self.pos))
            elif self.current_char == '[':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. "])
                    continue
                if self.current_char not in opensquare_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(SLBRACKET, "[", pos_start = self.pos))
            elif self.current_char == ']':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ] '. Cause: ' {self.current_char} '."])
                    continue
                if self.current_char not in closesquare_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(SRBRACKET, "]", pos_start = self.pos))
            # Handling '{' (opening curly bracket)
            elif self.current_char == '{':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. "])
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(CLBRACKET, "{", pos_start = self.pos))
            elif self.current_char == '}':
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(CRBRACKET, "}", pos_start = self.pos))
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for 'closing curly bracket'. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(CRBRACKET, "}", pos_start = self.pos))

            elif self.current_char == "\"":
                string, error = self.make_string()
                tokens.append(Token(STRING, f"{string}", pos_start = self.pos))
                self.advance()

                errors.extend(error)
            elif self.current_char == ',':

                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' , '. Cause: ' {self.current_char} '.  "])
                    continue
                if self.current_char not in comma_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' , '. Cause: ' {self.current_char} '.  "])
                    continue
                tokens.append(Token(COMMA, ",", pos_start = self.pos))

            elif self.current_char == "$":

                self.advance()
                if self.current_char == None:
                    tokens.append(Token(TERMINATOR, "$", pos_start = self.pos))
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' $ '. Cause: ' {self.current_char} '. "])
                    continue
                tokens.append(Token(TERMINATOR, "$", pos_start = self.pos))
            else:
                errors.append(f"Error at line: {self.pos.ln + 1}. Illegal character: {self.current_char}")
                self.advance()

        tokens.append(Token(EOF, "EOF", pos_start = self.pos))
        return tokens, errors

    def make_number(self): # Returns the corresponding Token with type int or float
        dec_count = 0
        num_count = 0
        num_str = ''
        dot_count = 0
        errors = []

        while self.current_char is not None and self.current_char in all_numbers + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    errors.append(f"Error at line: {self.pos.ln + 1}. Invalid character '{self.current_char}' in number. Decimal point already found!")
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_count += 1
                num_str += self.current_char
            self.advance()

        # Check if there are letters after the number
        if self.current_char is not None and self.current_char.isalpha():
            errors.append(f"Error at line: {self.pos.ln + 1}. Invalid delimiter for number: {num_str}")
            if errors:
                return [], errors

        # Validate the next character using `num_delim`
        if self.current_char is not None and self.current_char not in num_delim:
            errors.append(
                f"Error at line: {self.pos.ln + 1}. Invalid delimiter '{self.current_char}' after number '{num_str}'. "
                f"Error at line: {self.pos.ln + 1}. Expected one of: {num_delim}"
            )
            if errors:
                return [], errors

        # Determine if the token is an integer or a float
        if dot_count == 0:
            return Token(INTEGER, int(num_str), pos_start = self.pos), errors
        else:
            return Token(FLOAT, float(num_str), pos_start = self.pos), errors


    # reserved words
    #takes in the input character by character then translates them into words then tokens
    def make_word(self):
        print("make word character: ", self.current_char)
        ident = ""
        ident_count = 0
        errors = []

        while self.current_char != None:

            # # Collect characters for the word
            # while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            #     ident += self.current_char
            #     self.advance()

            # # Check for reserved words using existing logic (defined handlers for each word)
            # token, error = self.make_ident(ident)
            # if error:
            #     errors.append(error)
            #     return None, errors
            if self.current_char == "a": #ADD
                    ident += self.current_char
                    self.advance()
                    ident_count += 1 #not used
                    if self.current_char == "d":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for add! Cause: {self.current_char}. '])
                                return [], errors
                            if self.current_char in '(':
                                return Token(ADD, "add", pos_start = self.pos), errors 
                            # elif self.current_char in alpha_num: #double check this
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for add! Cause: {self.current_char}. '])
                                return [], errors

            elif self.current_char == "b": #BREAK
                if ident_count == 10:
                    break
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "r":
                    if ident_count == 10:
                        break
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "e":
                        if ident_count == 10:
                            break
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "a":
                            if ident_count == 10:
                                break
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "k":
                                if ident_count == 10:
                                    break
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for break! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char in break_delim: #double check this
                                    return Token(BREAK, "break", pos_start = self.pos), errors
                                elif self.current_char in break_delim:
                                    continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for break! Cause: {self.current_char}'])
                                    return [], errors

            elif self.current_char == "c": #COLLECT
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "l":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "c":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "t":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1

                                    if self.current_char == None:
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for collect! Cause: {self.current_char} '])
                                        return [], errors
                                    if self.current_char in '(':
                                        return Token(COLLECT, "collect", pos_start = self.pos), errors
                                    # elif self.current_char in alpha_num: #double check this
                                    #     continue
                                    else:
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for collect! Cause: {self.current_char} '])
                                        return [], errors

                elif self.current_char == "r": #CRAFT
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "a":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "f":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "t":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for craft! Cause: {self.current_char}.  '])
                                    return [], errors
                                if self.current_char in spacepr_delim:
                                    return Token(CRAFT, "craft", pos_start = self.pos), errors
                                # elif self.current_char in alpha_num:
                                #     continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for craft! Cause: {self.current_char}.  '])
                                    return [], errors

                    elif self.current_char == "o": #CROP
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "p":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for crop! Cause: {self.current_char}.  '])
                                return [], errors
                            if self.current_char in whitespace or self.current_char.isspace():
                                return Token(CROP, "crop", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num: #double check this
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for crop! Cause: {self.current_char}.  '])
                                return [], errors

            elif self.current_char == "d": #DEW
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "e":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "w":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1

                        if self.current_char == None:
                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for dew! Cause: {self.current_char} '])
                            return [], errors
                        if self.current_char in dew_delim:
                            return Token(DEW, "dew", pos_start = self.pos), errors
                        # elif self.current_char in alpha_num: #double check this
                        #     continue
                        else:
                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for dew! Cause: {self.current_char} '])
                            return [], errors

            elif self.current_char == "f": #FALSE, FOR
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "s":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for false! Cause: {self.current_char}.  '])
                                    return [], errors
                                if self.current_char in bool_delim:
                                    return Token(FALSE, "false", pos_start = self.pos), errors
                                # elif self.current_char in alpha_num:
                                #     continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for false! Cause: {self.current_char}.  '])
                                    return [], errors

                        elif self.current_char == "l": #FOR = FALL
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for fall! Cause: {self.current_char}. '])
                                return [], errors
                            if self.current_char in spacepr_delim:
                                return Token(FALL, "fall", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for fall! Cause: {self.current_char}. '])
                                return [], errors

                    elif self.current_char == "r": #FARMHOUSE
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "m":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "h":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "o":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "u":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == "s":
                                            ident += self.current_char
                                            self.advance()
                                            ident_count += 1
                                            if self.current_char == "e":
                                                ident += self.current_char
                                                self.advance()
                                                ident_count += 1

                                                if self.current_char == None:
                                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for farmhouse! Cause: {self.current_char}.  '])
                                                    return [], errors
                                                if self.current_char in whitespace or self.current_char.isspace():
                                                    return Token(FARMHOUSE, "farmhouse", pos_start = self.pos), errors
                                                # elif self.current_char in alpha_num:
                                                #     continue
                                                else:
                                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for farmhouse! Cause: {self.current_char}.  '])
                                                    return [], errors

            elif self.current_char == "h": #HARVEST
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "r":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "v":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "s":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "t":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == None:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for harvest! Cause: {self.current_char}. '])
                                            return [], errors
                                        if self.current_char  in spacepr_delim + TERMINATOR:
                                            return Token(HARVEST, "harvest", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for harvest! Cause: {self.current_char}. '])
                                            return [], errors
            elif self.current_char == "n": #PELICAN, PERFECTION, PLANTING
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "e":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "x":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "t":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for next! Cause: {self.current_char}. '])
                                return [], errors
                            if self.current_char in break_delim:
                                return Token(NEXT, "next", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for next! Cause: {self.current_char}. '])
                                return [], errors
            elif self.current_char == "p": #PELICAN, PERFECTION, PLANTING
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "e":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "c":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "a":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "n":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1

                                        if self.current_char == None:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pelican! Cause: {self.current_char}.  '])
                                            return [], errors
                                        if self.current_char in '(':
                                            return Token(PELICAN, "pelican", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pelican! Cause: {self.current_char}.  '])
                                            return [], errors

                    elif self.current_char == "r": #PERFECTION
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "f":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "c":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "t":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == "i":
                                            ident += self.current_char
                                            self.advance()
                                            ident_count += 1
                                            if self.current_char == "o":
                                                ident += self.current_char
                                                self.advance()
                                                ident_count += 1
                                                if self.current_char == "n":
                                                    ident += self.current_char
                                                    self.advance()
                                                    ident_count += 1
                                                    if self.current_char == None:
                                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for perfection! Cause: {self.current_char}.'])
                                                        return [], errors
                                                    if self.current_char in break_delim:
                                                        return Token(PERFECTION, "perfection", pos_start = self.pos), errors
                                                    # elif self.current_char in alpha_num:
                                                    #     continue
                                                    else:
                                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for perfection! Cause: {self.current_char}.'])
                                                        return [], errors

                elif self.current_char == "l": #PLANTING #check here
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "a":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "n":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "t":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "i":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "n":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == "g":
                                            ident += self.current_char
                                            self.advance()
                                            ident_count += 1
                                            if self.current_char == None:
                                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for planting! Cause: {self.current_char}. '])
                                                return [], errors
                                            if self.current_char in break_delim:
                                                return Token(PLANTING, "planting", pos_start = self.pos), errors
                                            # elif self.current_char in alpha_num:
                                            #     continue
                                            else:
                                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for planting! Cause: {self.current_char}. '])
                                                return [], errors
                    elif self.current_char == "u":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "c":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "k":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pluck! Cause: {self.current_char}. '])
                                    return [], errors
                                if self.current_char in '(':
                                    return Token(PLUCK, "pluck", pos_start = self.pos), errors
                                # elif self.current_char in alpha_num:
                                #     continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pluck! Cause: {self.current_char}. '])
                                    return [], errors

            elif self.current_char == "s": #SHIP, STAR, STARDEW
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "h":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "p":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for ship! Cause: {self.current_char}. '])
                                return [], errors
                            if self.current_char in '(':
                                return Token(SHIP, "ship", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for ship! Cause: {self.current_char}. '])

                elif self.current_char == "t": #STAR
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "a":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "r":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for star! Cause: {self.current_char}.'])
                                return [], errors
                            if self.current_char in spacepr_delim:
                                return Token(STAR, "star", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            elif self.current_char == "d": #inde ko ma-gets paano mapasok tong stardew sa 
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "e":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "w":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == None:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for stardew! Cause: {self.current_char}.'])
                                            return [], errors
                                        if self.current_char in spacepr_delim:
                                            return Token(STARDEW, "stardew", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for stardew! Cause: {self.current_char}.'])
                                            return [], errors
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for ! Cause: {self.current_char}.'])
                                return [], errors

            elif self.current_char == "t": #TRUE
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "r":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "u":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for true! Cause: {self.current_char}.'])
                                return [], errors
                            if self.current_char in bool_delim:
                                return Token(TRUE, "true", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for true! Cause: {self.current_char}.'])
                                return [], errors

            elif self.current_char == "v": #VOIDEGG
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "g":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "g":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == None:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for voidegg! Cause: {self.current_char}. '])
                                            return [], errors
                                        if self.current_char in bool_delim:
                                            return Token(VOIDEGG, "voidegg", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for voidegg! Cause: {self.current_char}.'])
                                            return [], errors

            elif self.current_char == "w": #WHILE
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "i":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "n":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "t":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "r":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == None:
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for winter! Cause: {self.current_char}.'])
                                        return [], errors
                                    if self.current_char in pr_delim or self.current_char.isspace():
                                        return Token(WINTER, "winter", pos_start = self.pos), errors
                                    # elif self.current_char in alpha_num:
                                    #     continue
                                    else:
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for winter! Cause: {self.current_char}.'])
                                        return [], errors


            elif self.current_char.isalpha() and self.current_char.islower():
                print("END LOOP CHARACTER: ", self.current_char)
                ident = self.current_char
                self.advance()
                # while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
                #     ident += self.current_char
                #     self.advance()
                # errors.append(f"Lexical error: Invalid word '{ident}': Not a reserved word or valid identifier. Identifiers must start with an uppercase letter.")

            else:
                print("ELSE NON ALPHANUMERIC: ", self.current_char)
                # Process the identifier when a non-alphanumeric character is encountered
                result, error = self.make_ident(ident)
                if error:
                    errors.extend(error)
                if result:
                    return Token(IDENTIFIER, result, pos_start = self.pos), errors
                break

            # Handle the final case where identifier is completed
            if ident:
                print("IF IDENT!")
                result, error = self.make_ident(ident)
                if error:
                    errors.append(error)
                    return [], errors
                elif result:
                    return Token(IDENTIFIER, result, pos_start = self.pos), errors

            if not ident:
                errors.extend(f"Error at line: {self.pos.ln + 1}. Identifier is empty or invalid.")
            return Token(IDENTIFIER, ident, pos_start = self.pos), errors

    def make_ident(self, ident):
        """
        Validates whether the given word is a valid identifier or reserved word.
        """
        errors = []

        # Ensure the first letter is uppercase
        if not ident[0].isupper():
            print(f"NASA LOOB NG MAKE IDENT YUNG ERROR: {self.current_char}")
            return None, f"Error at line: {self.pos.ln + 1}. Invalid start: '{ident[0]}'.  "

        # Ensure no invalid characters are present
        if not all(c.isalnum() or c == "_" for c in ident):
            return None, f"Error at line: {self.pos.ln + 1}. Invalid character in word '{ident}'. Identifiers must be alphanumeric or underscores."

        # Ensure the next character is a valid delimiter
        if self.current_char is not None and self.current_char not in id_delim:
            return None, f"Error at line: {self.pos.ln + 1}. Invalid delimiter after word '{ident}'. Found: '{self.current_char}. "

        return ident, None

    def make_string(self):
        pos_start = self.pos.copy()
        string = "\""
        errors = []
        self.advance()

        while self.current_char is not None and self.current_char != "\"":
            string += self.current_char
            self.advance()

        if self.current_char == "\"":
            string += "\""  # Add the closing quotation mark
            self.advance()
            return string, errors

        else:
            errors.append(f"Error at line: {self.pos.ln + 1}. Expected closing quotation mark!")
            return string, errors

#NODES AST node classes
class IdentifierNode: # Represents variable names (identifiers)
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end # Stores the token and its start/end positions for error reporting
    
    def __repr__(self):
        return f'{self.tok}' # Custom display of node
    
class NumberNode: # Represents numeric literals (int/float)
    def __init__(self, tok): 
        self.notted= False # notted allows tracking if a ! (not) is applied
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'NumberNode: value: {self.tok.value}' # Easy printing for debugging
    
class PreUnaryNode: # Both represent unary operations ++A or A++
    def __init__(self, tok, operation = None, adjust_by = 1):
        self.tok = tok # tok: the target variable
        self.operation = operation # operation: the operation to be performed
        self.adjust_by = adjust_by # adjust_by: the amount to adjust the variable by (default is 1)

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def get_level(self): # get_level: calculates the level of the node in the tree
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # print_tree: prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'PreUnaryNode')
        print(spaces + '    - ', f"name: {self.tok.crop_name_tok.value}")
        print(spaces + '    - ', f"operation: {self.operation}")

    def __repr__(self):   
        return f"PreUnaryNode: operation: '{self.operation}', identifier: '{self.tok.crop_name_tok.value}'"
    
class PostUnaryNode:
    def __init__(self, tok, operation = None, adjust_by = 1):
        self.tok = tok
        self.operation = operation
        self.adjust_by = adjust_by

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'PostUnaryNode')
        print(spaces + '    - ', f"name: {self.tok.crop_name_tok.value}")
        print(spaces + '    - ', f"operation: {self.operation}")

    def __repr__(self):   
        return f"PostUnaryNode: identifier: '{self.tok.crop_name_tok.value}', operation: '{self.operation}',"
    
class StringNode: # Represents string literals
    def __init__(self, tok): 
        self.notted = False # notted allows tracking if a ! (not) is applied
        self.tok = tok # tok: the token representing the string

        self.pos_start = self.tok.pos_start # Stores the token and its start/end positions for error reporting
        self.pos_end = self.tok.pos_end # Stores the token and its start/end positions for error reporting

    def __repr__(self):
        return f'{self.tok}' # Custom display of node 

class BooleanNode: # Represents boolean literals (true/false)
    def __init__(self, tok, value = 0): 
        self.notted = False # notted allows tracking if a ! (not) is applied
        self.tok = tok # tok: the token representing the boolean value
        if self.tok.token == FALSE: 
            self.value = 0
        else:
            self.value = 1

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'
class ListNode: # ListNode: Represents a list definition (e.g., Fib = [0, 1])
    def __init__(self, crop_name, items = [] ): 
        self.crop_name = crop_name
        self.items = items
        self.pos_start = self.crop_name.pos_start
        self.pos_end = self.crop_name.pos_end
        self.clear_items()
    def clear_items(self): # clear_items: Initializes the list of items
        self.items = []
    def add_item(self, token): # add_item: Adds an item to the list
        self.items.append(token)

    def __repr__(self) -> str: 
        return f"ListNode: {self.items}" 

class ListCallNode: # ListCallNode: Represents a list call (e.g., Fib[0])
    def __init__(self, crop_name, index=0 ): 
        self.crop_name = crop_name
        self.index = index
        self.pos_start = self.crop_name.pos_start
        self.pos_end = self.crop_name.pos_end
    def added_to(self, other): # added_to: Handles addition operation
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        

    def subbed_by(self, other): # subbed_by: Handles subtraction operation
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        

    def multed_by(self, other): # multed_by: Handles multiplication operation
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        

    def dived_by(self, other): # dived_by: Handles division operation
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
    def modulo(self, other): # modulo: Handles modulo operation
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        
    def get_comparison_eq(self, other): # get_comparison_eq: Handles equality comparison ==
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)

    def get_comparison_ne(self, other): #  get_comparison_ne: Handles inequality comparison !=
        
        return Number(1), None 

    def get_comparison_lt(self, other): # get_comparison_lt: Handles less than comparison <
        return Number(1), None

    def get_comparison_gt(self, other): # get_comparison_gt: Handles greater than comparison >
        return Number(1), None

    def get_comparison_lte(self, other): # get_comparison_lte: Handles less than or equal to comparison <=
        return Number(1), None

    def get_comparison_gte(self, other): # get_comparison_gte: Handles greater than or equal to comparison >= 
        return Number(1), None

    def anded_by(self, other): # anded_by: Handles logical AND operation
        return Number(1), None

    def ored_by(self, other): # ored_by: Handles logical OR operation
        return Number(1), None

    def notted(self): # notted: Handles logical NOT operation
        return Number(1), None
    def is_true(self): # is_true: Checks if the node is true
        return False
    def set_pos(self, pos_start=None, pos_end=None): 
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    # def add_item(self, token):
    #     self.items.append(token)

    def __repr__(self) -> str:
        return f"ListCallNode: {self.crop_name}, index: {self.index}"
class VoidNode:
    def __init__(self, tok): 
        self.tok = tok # Represents a void value 
        
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    def __repr__(self) -> str:
        return "void"
    
class CropAccessNode: 
    def __init__(self, crop_name_tok): # Represents accessing a variable 
        self.parent = None
        self.crop_name_tok = crop_name_tok  # Token that stores the name of the variable being accessed

        self.pos_start = self.crop_name_tok.pos_start
        self.pos_end = self.crop_name_tok.pos_end

    def get_ln(self):    # Returns the line number of this node 
        return self.pos_start.ln+1

class CropAssignNode: 
    def __init__(self, crop_name_tok, value_node): # Used for assignments like `A = 5`
        self.parent = None # Parent node reference in AST
        self.prompt = None  # for `collect()` input 
        self.crop_name_tok = crop_name_tok # Token that stores the name of the variable being assigned
        self.value_node = value_node # Value being assigned to the variable 
        self.pos_start = self.crop_name_tok.pos_start 
        self.pos_end = self.value_node.pos_end

    def get_ln(self):
        return self.pos_start.ln+1

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'CropAssignNode')
        print(spaces + '    - ', f"parent: {self.parent}")
        print(spaces + '    - ', f"name: {self.crop_name_tok.value}")
        print(spaces + '    - ', f"value: {self.value_node}")
        
        

class CropInitNode: # Used for initializing a variable with an operation (e.g., `A += 5`)
    def __init__(self, crop_name_tok, value_node, operation = Token(EQUAL, "=")): # Represents the operation to be performed
        self.crop_name_tok = crop_name_tok
        self.value_node = value_node
        self.operation = operation
        self.pos_start = crop_name_tok.pos_start
        self.pos_end = crop_name_tok.pos_end
 
    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'CropInitNode')
        print(spaces + '    - ', f"name: {self.crop_name_tok}")
        print(spaces + '    - ', f"operation: {self.operation}")
        print(spaces + '    - ', f"value: {self.value_node}")

class CropDecNode: # Used for declaring a variable without initialization (e.g., `A`)
    def __init__(self, crop_name_tok=None, collect_node=None): # Represents a variable declaration
        self.parent = None
        self.crop_name_tok = crop_name_tok.value
        self.value_node = VoidNode(crop_name_tok) # void node to indicate no value assigned

        self.pos_start = crop_name_tok.pos_start
        self.pos_end = crop_name_tok.pos_end

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'CropDecNode')
        print(spaces + '    - ', f"name: {self.crop_name_tok}")
        print(spaces + '    - ', f"value: {self.value_node}")

class HarvestCallNode: # Used for harvesting a crop (e.g., `harvest A`)
    def __init__(self, value_node): #  value_node is the expression or variable being returned
        self.parent = None
        self.value_node = value_node # Holds the AST node representing the return value
        self.value = None  # Will hold the computed value later (during interpretation)
        print('harvest call value node: ', value_node)
        if isinstance(value_node, RTResult): # if the value_node is a result object
            self.pos_start = self.value_node.value.pos_start # 
            self.pos_end = self.value_node.value.pos_end
        elif isinstance(value_node, BinOpNode): # For arithmetic expressions
            self.pos_start = self.value_node.pos_start
            self.pos_end = self.value_node.pos_end
        elif isinstance(value_node, CropAccessNode): # For simple variable references
            self.pos_start = self.value_node.crop_name_tok.pos_start
            self.pos_end = self.value_node.crop_name_tok.pos_end
        elif isinstance(value_node, CraftCallNode):  # For function call results
            value_node.parent = self.parent
            self.pos_start = self.value_node.identifier.pos_start
            self.pos_end = self.value_node.identifier.pos_end
        else: # assume it's a literal token (number/string)
            self.pos_start = self.value_node.tok.pos_start
            self.pos_end = self.value_node.tok.pos_end

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'HarvestCall')
        print(spaces + '    - ', f"parent: {self.parent}")
        print(spaces + '    - ', f"value/s: {self.value_node}")
        
class ShipNode: 
    def __init__(self, body, ship_tok= None): # Represents an output
        self.ship_tok = ship_tok  # Token for the keyword 'ship'
        self.parent = None
        self.body = body # List of AST nodes to output
        # self.list_of_nodes = list_of_nodes
        self.pos_start = ship_tok.pos_start
        self.pos_end = ship_tok.pos_end
    
    def add_child(self, node): # For visual tree printing
        node.parent = self
        # self.body.append(node)

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        for item in self.body:
            self.add_child(item)
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'ShipNode')
        print(spaces + '    - ', f"parent: {self.parent}")
        print(spaces + '    - ', f"value/s: {self.body}")

class CollectNode:  # Represents input
    def __init__(self, variable_node, prompt) -> None: 
        self.pos_end = variable_node.pos_end # Position tracking
        self.parent = None
        self.prompt = prompt # String prompt shown to the user
        # this should be a CropAccessNode
        self.variable_node = variable_node 

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging 
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'CollectNode')
        print(spaces + '    - ', f"value/s: {self.variable_node}, {self.variable_node}")
    
class BinOpNode: # Binary operation node A + B
    def __init__(self, left_node, op_tok, right_node):
        self.parent = None
        self.notted = False # If used under a NOT operation
        self.left_node = left_node
        self.op_tok = op_tok # Token like '+', '-',
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'BinOpNode({type(self.left_node)}, {self.op_tok}, {self.right_node})'

class UnaryOpNode: # Represents a unary operation ! -
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.node.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'
    
class CraftCallNode:  # Represents function call  Add(1, 2)
    def __init__(self, identifier = None) -> None:
        self.parent = None
        self.identifier = identifier # Function name token
        self.parameters = [] # Arguments passed to the function
        self.pos_end = self.identifier.pos_end 
        self.pos_start = self.identifier.pos_start
        self.value = None # Value returned by the function
    def added_to(self, other): # Handles addition operation
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        

    def subbed_by(self, other): # Handles subtraction operation 
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation) 
        

    def multed_by(self, other): # Handles multiplication operation
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        

    def dived_by(self, other): # Handles division operation
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
    def modulo(self, other): # Handles modulo operation
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)
        
    def get_comparison_eq(self, other): # Handles equality comparison ==
        
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)

    def get_comparison_ne(self, other): # Handles inequality comparison !=
        
        return Number(1), None

    def get_comparison_lt(self, other): # Handles less than comparison <
        return Number(1), None

    def get_comparison_gt(self, other): # Handles greater than comparison >
        return Number(1), None

    def get_comparison_lte(self, other): # Handles less than or equal to comparison <=
        return Number(1), None

    def get_comparison_gte(self, other): # Handles greater than or equal to comparison >=
        return Number(1), None

    def anded_by(self, other): # Handles logical AND operation
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)

    def ored_by(self, other): # Handles logical OR operation
        return Number(1), None # Returns a Number object and None (placeholder for actual implementation)

    def notted(self): # Handles logical NOT operation
        return Number(1), None 

    def add_param(self, node):# Adds a parameter to the function call
        self.parameters.append(node) # Adds parameter AST node to the call

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        self.pos_end = self.identifier.pos_end
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'craftCallNode')
        print(spaces + '    - ', f"parent : {self.parent}")
        print(spaces + '    - ', f"identifier : {self.identifier}")
        print(spaces + '    - ', f"parameters : {self.parameters}")
    
    def __repr__(self) -> str: # Custom display of node
        return f"craftCallNode, name: {self.identifier}, parameters: {self.parameters}, parent: {self.parent}"
    
class StarNode: 
    def __init__(self, cases, dew_case, ): # Initializes a star node with multiple conditions and a dew cases
        self.parent = None # Points to the parent AST node
        #cases should be a a list of tuples with conditions, statements
        self.cases = cases
        self.dew_case = dew_case 
        self.body = []  # Holds child nodes
        self.pos_start = self.cases[0][0].pos_start # Start position comes from the first condition node
        
    def add_child(self, node): # Helper to track parent for each child node
        node.parent = self
        self.body.append(node)

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, f"StarNode")
        print( "  "+ prefix, f"parent: {self.parent}")
        for item in self.cases:  # Loop through each (condition, statements) pair
            for j in item:
                if not isinstance(j, list):
                    print( "  "+ prefix, f"condition : {j} ")
                else: # Second element = list of statements for this case
                    print( "  "+ prefix, f"condition statements: ")
                    for stmt in j:
                        self.add_child(stmt)
                        stmt.print_tree()
        print( "  "+ prefix, f"dew cases: {self.dew_case} ") # Print dew cases
        
class WinterNode: # while loop
    def __init__(self, condition): # Takes the loop condition expression
        self.parent = None
        #cases should be a a list of tuples with conditions, statements
        self.condition = condition
        self.body = []
        self.pos_start = self.condition.pos_start # Used for error reporting

    def add_child(self, node):  # Set parent and store in body
        node.parent = self
        self.body.append(node)
 
    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, f"WinterNode")
        print( "  "+ prefix, f"parent: {self.parent}")
        print( "  "+ prefix, f"condition: {self.condition}")
        print( "  "+ prefix, f"body: ")
        for item in self.body:
            item.print_tree()

class FallNode:
    def __init__(self, condition) -> None:  # Takes the middle condition part only at init
        self.parent = None
        self.variable = None # crop a = 10, a = 10 First part = initialization 
        self.condition = None # a <100 Second part = condition
        self.unary = None # --a Third part= update
        self.body = [] 
        self.condition = condition
        self.pos_start = self.condition.pos_start
    
    def add_child(self, node): # helper to track parent for each child node
        node.parent = self
        self.body.append(node)

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        # self.pos_start = self.condition.pos_start
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, f"FallNode")
        print( "  "+ prefix, f"parent: {self.parent}")
        print( "  "+ prefix, f"1st statement: {self.variable}")
        print( "  "+ prefix, f"2nd statement: {self.condition}")
        print( "  "+ prefix, f"3rd statement: {self.unary}")
        print("  "+ prefix, f"body: ")
        for item in self.body:
            # self.add_child(item)
            item.print_tree()
            
class NextNode:   # Represents a continue statement in loops
    def __init__(self, tok) -> None: # Takes the token for the continue statement
        self.tok = tok # Token for 'next'
        self.pos_start = self.tok.pos_start 
        self.pos_end = self.tok.pos_end
    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'NextNode')
        print(spaces + '    - ', f"value: {self.tok.value}")
        
class BreakNode: # Represents a break statement in loops
    def __init__(self, tok) -> None: #Takes the token for the break statement
        self.tok = tok # Token for 'break'
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def get_level(self): #returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, 'BreakNode')
        print(spaces + '    - ', f"value: {self.tok.value}")
    

#INTERPRETER CLASS FOR SEMANTIC [Runtime wrapper for semantic analysis or interpreter]
class RTResult:
    def __init__(self):
        self.value = None #Will store result value 
        self.error = None # If any runtime error occurs

    def register(self, res):  #Inherits value or error from another RTResult
        if res.error: self.error = res.error
        return res.value

    def success(self, value):  #Used when an evaluation is successful
        self.value = value
        return self

    def failure(self, error): #uused when evaluation fails
        self.error = error
        return self


#PARSE RESULT (2nd part of the parser)
#It can either be a successful parse with a node or an error
class ParseResult:
    def __init__(self):
        self.error = None # Stores parsing error (if any)
        self.node = None # Stores the AST node produced (if parsing is successful)

    # helps track errors while retrieving values from parsing or interpretation
    def register(self, res): # Inherits value or error from another ParseResult 
        if isinstance(res, ParseResult): # If input is another ParseResult
            if res.error: # pag may error 
                self.error = res.error # raise the error
            return res.node # return the node
        
        return res #return raw value
    
    def success(self, node):
        self.node = node # Set the resulting node on success
        return self # Return self for chaining

    def failure(self, error):
        self.error = error # Set the parsing error
        return self # Return self for chaining

# ast start
class Program:
    def __init__(self, symbol_table = None):
        #has farmhouse declarations
        #has functions
        #has main
        self.parent = None
        self.body = [] #store nodes in pelican() or main 
        self.errors = [] # undeclared variables, mismatch parameter and argument, undeclared function call etc.. all collected errors for the program
        self.symbol_table = symbol_table # global declaration
        self.functions = [] #functions list of all declared craft() functions
        
    # def add_variables(self,name, node):
    #     self.context.symbol_table.set(name, node.value)

    def add_child(self, node):
        node.parent = self  # Set parent for proper tree structure
        self.body.append(node) # Add the node to program body
    
    def error(self, error):
        self.errors.append(error) # Add an error to the list
    

    def display(self): # For printing the program tree
        print("Program: ")
        if self.body:
            for item in self.body: # Print each node in the main body
                item.print_tree()
        else:
            print("WALANG PELICAN")
                
    #laman ng Program body is CropAssignNode/s, craftNode/s, PelicanNode
    
class CraftNode:
    def __init__(self, identifier) -> None:
        #parent should be program lang
        self.parent = None # Parent node reference in AST
        self.identifier =identifier # Function name token
        self.body = [] # Body statements
        self.parameters = [] # Function parameters
        self.symbol_table = None # Symbol table for local variables
        self.errors = [] # Any semantic/syntax errors
        self.called = False # Flag to check if the function has been called
        
    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, f"Craft")
        print( "  "+ prefix, f"parent: {self.parent}")
        print( "  "+ prefix, f"identifier: {self.identifier}")
        print( "  "+ prefix, f"parameters: ")
        for item in range(len(self.parameters)):
            print( spaces + '      -', f"parameter {item}: {self.parameters[item]}, {self.parameters[item].crop_name_tok}")

        print( "  "+ prefix, f"body: ")
        if self.body:
            for child in self.body:
                child.print_tree()
        
    def add_child(self, node):
        node.parent = self
        self.body.append(node)

class PelicanNode:
    def __init__(self, symbol_table = None) -> None: # Takes the symbol table for local variables
        self.parent = None # Parent node reference in AST
        self.body = [] # List of child nodes
        self.errors = [] # errors list
        self.context = None # Context for local variables
        self.symbol_table = symbol_table # Symbol table for local variables
        # self.pos_start = self.body[0].pos_start
        

    def get_level(self): # Returns the level of the node in the AST
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self): # Prints the tree structure for debugging
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix, f"Pelican")
        print( "  "+ prefix, f"parent: {self.parent}")

        print( "  "+ prefix, f"body: ")
        if self.body:
            for child in self.body:
                if isinstance(child, ParseResult):
                    print("child: ",child.node)
                else:
                    print("child: ",child)
                child.print_tree()
        
    def add_child(self, node):
        node.parent = self
        self.body.append(node)
        
#PARSER
# 2nd version of the parser instead na sa tokens, AST/nodes na ang pinapasa 
# Defines the parser that converts tokens into an Abstract Syntax Tree (AST)
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens # Initializes with a list of tokens.
        self.tok_idx = -1 # Sets current index to -1 (will advance immediately to 0)
        self.advance() 
        # Flags to track parsing state (e.g., to detect multiple pelican() declarations or correct block nesting)
        self.perfection = False
        self.is_pelican = False
        self.in_loop = False
        self.in_condition = False
        self.in_fall = False
        self.in_farmhouse = False

    def advance(self): # Moves to the next token and updates self.current_tok
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    #* parse takes the list of tokens then  decides which functions to execute based on the token
    def parse(self):
        res =  [] # List to store the resulting nodes
        error = []  # List to store any errors encountered during parsing
    
        program = Program() # The main function that builds the AST from token list.
        
        while self.current_tok.token == NEWLINE:
            self.advance()
            
        if self.current_tok.token == SINGLELINE:
            
            self.advance()
            while self.current_tok.token != NEWLINE:
                self.advance()
            self.advance()
        if self.current_tok.token == MULTILINE_OPEN:
            while self.current_tok.token != MULTILINE_CLOSE:
                self.advance()
        
        # Check for the 'planting' keyword to start the program
        # If not found, raise an error
        while self.current_tok.token != PLANTING:
            self.advance()
            if self.current_tok.token == EOF:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Type 'planting' start the program!"))
                return res, error
        
        if self.current_tok.token != PLANTING:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Type 'planting' start the program!"))
            return [], error
        else:
            self.advance()
            if self.current_tok.token != TERMINATOR:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Dollar Sign!"))
                return [], error
            else:
                self.advance()
                
            

        # * basically yung parse lang pero walang craft

        while True: # Loop continues until EOF or perfection$ is found

            if self.current_tok.token == MULTILINE_OPEN:
                while self.current_tok.token != MULTILINE_CLOSE:
                    self.advance()
                    if self.current_tok.token == EOF:
                        break
                self.advance()
                
            if self.current_tok.token != SINGLELINE and self.current_tok.token != EOF and self.current_tok.token != NEWLINE and self.current_tok.token != SINGLELINE and self.current_tok.token != FARMHOUSE and self.current_tok.token != CRAFT and self.current_tok.token != PELICAN and self.current_tok.token != MULTILINE_OPEN and self.current_tok.token != MULTILINE_CLOSE and self.current_tok.token != PERFECTION and self.current_tok.token !=  COMMENT:
                if self.is_pelican == True:
                    
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected perfection!"))
                else:
                    print("ERROR: ", self.current_tok)
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected craft, or pelican, or farmhouse!"))

                break
            else:
                self.advance()
                
            if self.current_tok.token == SINGLELINE:
            
                self.advance()
                while self.current_tok.token != NEWLINE:
                    self.advance()
                self.advance()
        
            
            # HARVEST SYNTAX         
            #HARVEST DECLARATION  DAT MAY GLOBAL
            if self.current_tok.token in FARMHOUSE:
                if self.is_pelican == True:
                    program.error(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please declare global variables before pelican!"))
                    break
                else:
                    self.advance() 
                
                    if self.current_tok.token in CROP: 
                        if self.current_tok.matches(CROP, 'crop'):
                            print("GLOBAL FARMHOUSE")
                            multiple, farmhouse_error = self.crop_dec()
                            if farmhouse_error:
                                print("FARMHOUSE ERROR")
                                program.error(farmhouse_error)
                            else:
                                program.add_child(multiple)
                                
                        while self.current_tok.token == COMMA:
                            multiple, farmhouse_error = self.crop_dec()
                            if farmhouse_error:
                                program.error(farmhouse_error)
                            else:
                                program.add_child(multiple)
                                if self.current_tok.token == TERMINATOR:
                                    break
                        
                        if self.current_tok.token != TERMINATOR:
                            program.error(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign after crop declaration!"))
                        
                        else:
                            self.advance()

            #functions
            # craft for subfunctions
            # craft syntax creates a CraftNode AST
            if self.current_tok.token == CRAFT:
                print("FOUND CRAFT1")
                if self.is_pelican == True:
                    program.error(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please declare craft before pelican!"))
                    break
                else:
                    self.advance()
                    
                    craft_node = CraftNode(self.current_tok)
                    craft_node.parent = program
                    self.advance()
                    
                    self.advance()
                    
                    if self.current_tok.token == CROP:
                        if self.current_tok.matches(CROP, 'crop'):
                            craft_result, craft_error = self.crop_dec()
                            if craft_error:
                                craft_node.errors.extend(craft_error)
                            else:
                                craft_node.parameters.append(craft_result)
                                if self.current_tok.token == RPAREN:
                                    self.advance()
                                
                                while self.current_tok.token == COMMA:
                                    self.advance()
                                    craft_result, craft_error = self.crop_dec()
                                    if craft_error:
                                        craft_node.errors.extend(craft_error)
                                    else:
                                        craft_node.parameters.append(craft_result)
                                        if self.current_tok.token == RPAREN:
                                            self.advance()
                                if self.current_tok.token == CLBRACKET:
                                    self.advance()
                                    
                                    result, body_error = self.body()
                                    if body_error:
                                        print("CRAFT NODE BODY ERROR")
                                        craft_node.errors = body_error
                                    
                                    for item in result:
                                        craft_node.add_child(item)
                                    
                                    program.add_child(craft_node)
                                    
                                    while self.current_tok.token == NEWLINE:
                                        self.advance()
                                    
                                    while self.current_tok.token != NEWLINE:
                                        self.advance()  
                                        
                                    # self.advance()
                                    # return program
                                    
                    if self.current_tok.token == RPAREN:
                        self.advance()
                        self.advance()
                        result, body_error = self.body()
                        if body_error:
                            craft_node.errors = body_error
                        for item in result:
                            craft_node.add_child(item)
                        
                        program.add_child(craft_node)
                        self.advance()
                        
                        

            # -- this is the main body of our function! 
            # * also i call body() here
            # main function
            # pelican syntax creates a PelicanNode AST
            if self.current_tok.token == PELICAN:
                print("found pelican node")
                self.advance()
                self.advance()
                pelican_node = PelicanNode()
                
                if self.is_pelican == True:
                    program.error(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Pelican function already declared!, Only one pelican function is allowed!"))
                    return program
                self.advance()
                
                if self.current_tok.token == CLBRACKET:
                    print("found curly bracket")
                    self.advance()
                    result, body_error = self.body()
                    # print("RESULT: ", result.node)
                    if body_error:
                        pelican_node.errors = body_error
                    
                    for item in result:
                        pelican_node.add_child(item)
                        
                    program.add_child(pelican_node)
                    self.advance()
                    return program
                else:
                    print("DI NAKIKITA YUNG BRACKET: ", self.current_tok)
            
            # end of program
            # perfection syntax
            if self.current_tok.token == PERFECTION:
                self.advance()
                if self.current_tok.token == TERMINATOR:
                    self.perfection = True
                    if self.is_pelican == False:
                        print("[DEBUG] Current Token: ", self.current_tok)
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "No pelican function found!"))
                        self.advance()
                        return res, error
                    else:
                        return res, error
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Dollar sign expected for 'perfection'!"))
            
            # if self.current_tok.token == CRBRACKET:
            #     break

            if self.current_tok.token == EOF:
                # error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "INVALID MAIN SCOPE"))
                break

        if self.current_tok.token == EOF:
            if self.perfection ==  True:
                return res, error
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'perfection' to end the program!"))
                return res, error



        return program
    # main function definition
    #* controls what happens when the compiler encounters the pelican token
    def pelican(self):
        result = ParseResult()
        res = []
        error = []
        self.advance()
        
        if self.current_tok.token == LPAREN:
            self.advance()
            
            if self.current_tok.token == RPAREN:
                self.advance()
                if self.current_tok.token in NEWLINE:
                    self.advance()
                if self.current_tok.token == CLBRACKET:
                    
                    self.advance()

                    while self.current_tok.token == NEWLINE:
                        self.advance()
                    # -- okay so here we call body
                    # TODO here we need to wrap it in a parseResult
                    # remember ParseResult has an error and a node
                    # maybe here try ko muna extract yung ast? then yung error separate
                            
                    craft_res = self.body()
                    
                        
                    if self.current_tok.token != CRBRACKET:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly brackets in pelican!"))
                        
                    else:
                        
                        self.advance()
                        return result.success(craft_res)
                    
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Pelican definition missing!"))
                    self.advance()
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis for pelican!"))   
        #craft Add(A, B)
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parentheses for parameters!"))
            return res, error
        # okay here we need to wrap this in a parseResult
        print("RESULT craft from pelican: ", result)
        return result.success(craft_res)

    # body of the function, definition
    #* body controls the user defined functions as well as the main function
    def body(self):
        print("CURRENT TOKEN IN BODY: ", self.current_tok)
        res =  []
        error = []
        # while self.current_tok.token != NEWLINE:
        #     self.advance()
        
        # * basically yung parse lang pero walang craft

        while True:
            if self.is_statement():
                if self.current_tok.token == MULTILINE_OPEN:
                    while self.current_tok.token != MULTILINE_CLOSE:
                        self.advance()
                        if self.current_tok.token == EOF:
                            break
                    self.advance()
                if self.current_tok.token == SINGLELINE:
                    self.advance()
                    while self.current_tok.token != NEWLINE:
                        self.advance()
                if self.current_tok.token == NEWLINE:
                    self.advance()
                
                #--INITIALIZATION OF IDENTIFIERS Add first parameter to the function call if it's a number, string, bool, void, or identifier
                if self.current_tok.token in INTEGER:
                    res = self.expr() 
                if self.current_tok.token == IDENTIFIER:
                    print("FOUND AN IDENTIFIER!: ", self.current_tok)
                    crop_name = self.current_tok
                    self.advance()
                    #-- if it's a function call
                    if self.current_tok.token == LPAREN:
                        craft_call = CraftCallNode(crop_name) #Start creating a function call AST node
                        self.advance()
                        if self.current_tok.token in (INTEGER, FLOAT):
                            print("NUMBER ARGUMENT: ", self.current_tok)
                            craft_call.add_param(NumberNode(self.current_tok))
                            self.advance()
                        elif self.current_tok.token == STRING:
                            craft_call.add_param(StringNode(self.current_tok))
                            self.advance()
                        elif self.current_tok.token in (TRUE, FALSE):
                            craft_call.add_param(BooleanNode(self.current_tok))
                            self.advance()
                        elif self.current_tok.token == VOIDEGG:
                            craft_call.add_param(VoidNode(self.current_tok))
                            self.advance()
                        elif self.current_tok.token == IDENTIFIER:
                            craft_call.add_param(CropAccessNode(self.current_tok))
                            self.advance()
                        
                        while self.current_tok.token == COMMA:
                            self.advance()
                            if self.current_tok.token in (INTEGER, FLOAT):
                                craft_call.add_param(NumberNode(self.current_tok))
                                self.advance()
                            elif self.current_tok.token == STRING:
                                craft_call.add_param(StringNode(self.current_tok))
                                self.advance()
                            elif self.current_tok.token in (TRUE, FALSE):
                                craft_call.add_param(BooleanNode(self.current_tok))
                                self.advance()
                            elif self.current_tok.token == VOIDEGG:
                                craft_call.add_param(VoidNode(self.current_tok))
                                self.advance()
                            elif self.current_tok.token == IDENTIFIER:
                                
                                print("ident craft")
                                craft_call.add_param(CropAccessNode(self.current_tok))
                                self.advance()
                            
                        self.advance()
                        res.append(craft_call) # Add the function call node to the result list
                        self.advance()
                
                    elif self.current_tok.token == SLBRACKET: # if it's a list call
                        self.advance()
                        if self.current_tok.token in (IDENTIFIER, INTEGER):
                            print("DEBUG: pumasok sa SLBRACKET")
                            index = self.expr()
                            index = index.node
                            print("[DEBUG] after: ", self.current_tok) 
                            if self.current_tok.token == SRBRACKET:
                                self.advance()
                                if self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL or self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:
                                    init_var, init_error = self.crop_init(crop_name)
                                    init_vacrope_tok = ListCallNode(crop_name, index)
                                    res.append(init_var)
                                    self.advance()
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing square bracket ']'"))
                        else: 
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier or number!"))
                    
                    # create the function of crop initialization
                    elif self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL or self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:
                        init_crop, init_error = self.crop_init(crop_name)
                        res.append(init_crop)
                        self.advance()
                            
                    #-- if we increment it
                    elif self.current_tok.token == INCRE:
                        operation = self.current_tok
                        self.advance()
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(PostUnaryNode(CropAccessNode(crop_name), operation))
                            self.advance()
                    #-- if we decrement it
                    elif self.current_tok.token == DECRE:
                        operation = self.current_tok
                        self.advance()
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(PostUnaryNode(CropAccessNode(crop_name), operation))
                            self.advance()
                    # -- else no other operation for it
                    else:
                        
                        print("[DEBUG] error token: ", self.current_tok)
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected assignment operator, increment, decrement, or call craft!"))
                        return [], error
                    
                if self.current_tok.token in (INCRE, DECRE):
                    operation = self.current_tok
                    self.advance()
                    if self.current_tok.token == IDENTIFIER:
                        identifier = self.current_tok
                        self.advance()

                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(PreUnaryNode(CropAccessNode(identifier), operation))
                            self.advance()
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid unary statement!"))


                #LOOPS
                # for loop (fall)
                if self.current_tok.token in FALL: # Parse Junimo Code's fall loop syntax and append its AST node
                    print("IN FALL")
                    self.advance()
                    print("before fall stmt: ", self.current_tok)
                    fall_res = self.fall_stmt()
                    print("[DEBUG] end of fall: ", self.current_tok)
                    self.advance()
                    print("[DEBUG] end of fall: ", self.current_tok)
                    self.advance()
                    res.append(fall_res)
                    
                #   winter_stmt (while loop)  
                if self.current_tok.token in WINTER: # Parse Junimo Code's winter loop syntax and append its AST node
                    result = self.winter_stmt()
                    res.append(result)
                    self.advance()
                
                # break statement
                if self.current_tok.token == BREAK: # Parse Junimo Code's break statement syntax and append its AST node
                    break_node = BreakNode(self.current_tok)
                    self.advance()
                    #;
                    res.append(break_node)
                    self.advance()
                        
                # continue statement (double check this with other files if implemented already)
                if self.current_tok.token == NEXT: # Parse Junimo Code's continue statement syntax and append its AST node
                    next_node = NextNode(self.current_tok)
                    self.advance()
                    #;
                    res.append(next_node)
                    self.advance()

                #CONDITIONAL
                # star (if)
                if self.current_tok.token in STAR: # Parse Junimo Code's star statement syntax and append its AST node
                    print("FOUND STARR")
                   
                    self.in_condition = True

                    self.advance()
                    print("current token in star: ", self.current_tok)
                    if self.current_tok.token != LPAREN:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '('"))
                        return res, error
                    self.advance()
                    star_res, star_err = self.star_expr() # TypeError: cannot unpack non-iterable ParseResult object
                    print("DONE STAR EXPR")
                    if star_err:
                        # error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ETO MALI"))
                        print("STAR ERR: ", star_err[0].as_string())
                        return res, error
                    # if if_res.error:
                    #     print("if res error: ", if_res.error.as_string())
                    #self.advance() 
                    print("STAR RES: ", star_res)
                    res.append(star_res)

                #INPUT OUTPUT 
                # COLLECT
                if self.current_tok.token in COLLECT:  # Parse Junimo Code's collect statement syntax and append its AST node
                    
                    self.advance()
                    # (
                    self.advance()
                    #we're expecting a variable
                    res.append(CollectNode(CropAccessNode(self.current_tok)))
                    self.advance()
                    # $
                    self.advance()
                # SHIP OUTPUT    
                if self.current_tok.token in SHIP: # Parse Junimo Code's ship statement syntax and append its AST node
                    print()
                    ship_tok = self.current_tok # Store the token for AST use
                    #need a list to store all the outputs
                    list_of_nodes = [] # List to store the nodes
                    result = ParseResult()  # Handle parsing results 
                    self.advance()
                    self.advance()
                    #this is for <<
                    # self.advance()
                    expr = result.register(self.expr())  # Parse a general expression (number, identifier, function call, parentheses, etc.) and propagate errors into 'result'
                    list_of_nodes.append(expr) # Append the expression node to the list
                    # self.advance()
                    # self.advance()
                    print("current token in ship: ", self.current_tok)
                    while self.current_tok.token == ",":
                        self.advance()
                        print("after comma loop: ", self.current_tok)
                        if self.current_tok.token != INTEGER and self.current_tok.token != LPAREN and self.current_tok.token != IDENTIFIER and self.current_tok.token != TRUE and self.current_tok.token != FALSE and self.current_tok.token != STRING and self.current_tok.token != VOIDEGG and self.current_tok.token != FLOAT:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, identifier, left parenthesis, true, false, string or void!"))
                            print("DI OKAY YUNG")
                            break
                        else:
                            expr = result.register(self.expr())  # Parse a general expression (number, identifier, function call, parentheses, etc.) and propagate errors into 'result'
                            list_of_nodes.append(expr) # Append the expression node to the list
                            # self.advance()
                            # i should append this to a list
                            # print(list_of_nodes)
                        # print("last token in loop: ", self.current_tok)
                    
                    res.append(ShipNode(list_of_nodes, ship_tok)) # Append the ship node to the result list
                    self.advance()
                    self.advance()
                    self.advance()
                    # self.advance()
                    # self.advance()


                        
                # CROP DECLARATION            
                if self.current_tok.token in CROP:  # Parse Junimo Code's crop statement syntax and append its AST node
                    if self.current_tok.matches(CROP, 'crop'):
                        craft_result, craft_error = self.crop_dec()   # Call crop_dec() to parse a declaration like crop A
                        print("TOKEN AFTER CROP DEC: ", self.current_tok)
                        if craft_error:
                            print("ERROR AFTER CROP DEC")
                            error.append(craft_error)
                            return res, error
                        else:
                            # self.advance()
                            res.append(craft_result) # Append the crop declaration node to the result list
                            print("CROP DEC RESULT: ", self.current_tok)
                            self.advance()
                           
                            while self.current_tok.token == COMMA:  # Handle multiple crop declarations
                                #self.advance()
                                #we advanced kasi nasa crop tau rn
                                craft_result, craft_error = self.crop_dec() 
                                
                                if craft_error:
                                    error.append(craft_error)
                                else:
                                    
                                    res.append(craft_result)
                                    if self.current_tok.token == RPAREN:
                                        self.advance()

                            if self.current_tok.token == TERMINATOR:
                                self.advance()
                
                # function for subfunctions
                if self.current_tok.token in CRAFT: 
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "You can't declare a function within a function!"))
                    break # Craft function declarations inside pelican or another craft are disallowed
                
                # harvest statement (return)
                if self.current_tok.token == HARVEST: # Parse Junimo Code's harvest statement syntax and append its AST node
                    result = ParseResult()
                    self.advance()
                    if self.current_tok.token != INTEGER and self.current_tok.token != LPAREN and self.current_tok.token != IDENTIFIER and self.current_tok.token != TRUE and self.current_tok.token != FALSE and self.current_tok.token != STRING and self.current_tok.token != VOIDEGG and self.current_tok.token != FLOAT:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, identifier, left parenthesis, true, false, string or voidegg!"))
                        break
                    else:
                        expr = result.register(self.expr()) # Parse as expression if starting with a number
                        if result.error: 
                            return res
                        self.advance()

                        # i want to store this in thepelican node
                        res.append(HarvestCallNode(expr)) # Append the harvest node to the result list
                        print("EXPR HARVEST: ", type(expr)) 
                        # if sub_func == True:
                        #     self.advance()
                        # else:
                        #     self.advance()
                        self.advance()
                        # self.advance()
                        print("[DEBUG] current val after harvest: ", self.current_tok)
                        return res, error
                        # return res, error
                        
                # perfection (end statement)
                if self.current_tok.token == PERFECTION:
                    self.advance()
                    if self.current_tok.token == TERMINATOR:
                        self.perfection = True
                        #self.advance()
                        return res, error
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Dollar sign expected for 'perfection'!"))

                if self.current_tok.token == CRBRACKET: # Stops parsing when the closing curly } or end-of-file is encountered
                    break

                if self.current_tok.token == EOF: 
                    # error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "INVALID MAIN SCOPE"))
                    break
            
            else:
                print("ERROR IN BODY TOKEN: ", self.current_tok)
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected crop, collect, ship, identifier, star, ++, --, fall, winter, }"))
                break

        return res, error
    
    def crop_dec(self):
        self.advance()
        print("current token in crop dec: ", self.current_tok)
        if self.current_tok.token != IDENTIFIER:
            return None, InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            )
        
        # Token(IDENTIFIER: a)
        crop_name = self.current_tok # Store identifier token
        list_node = ListNode(crop_name) # Create an empty list node for possible list assignment
        # print("crop name: ", crop_name)
        #res.register_advancement()
        self.advance()
        print("this is current variable: ", crop_name)
        if self.current_tok.token == EQUAL:
            print("FOUND AN EQUAL IN CROP DEC")
            #res.register_advancement()
            self.advance()
            # this only gets the node from expr, not the ParserResult
            # so NumberNode lang tong expr
            # todo if number, plus, minus, identifier, use expr
            print("current token before expr: ", self.current_tok)
            if self.current_tok.token in (PLUS, MINUS, IDENTIFIER, INTEGER, FLOAT, LPAREN, STRING, VOIDEGG, INCRE, DECRE, NEGATIVE, TRUE, FALSE):
                
                expr = self.expr()
                # print("we dont have an error in expr")
                # print("current token after expr: ", self.current_tok)
                # print("expr: ", type(expr.node))
                print("current token after expr: ", self.current_tok)
                print("EXPR NODE: ", expr.node)
                return CropAssignNode(crop_name, expr.node), None
            # check if it's crop a = [1, 3, true]
            if self.current_tok.token == SLBRACKET:
                # print("assigning a list")
                self.advance()
                if self.current_tok.token in (IDENTIFIER, INTEGER, FLOAT, TRUE, FALSE, STRING):
                    expr = self.expr()
                    # print("we dont have an error in expr")
                    # print("current token after first token list: ", self.current_tok)
                    # print("expr: ", type(expr.node))
                    list_node.add_item(expr.node)
                    
                    while self.current_tok.token == COMMA:
                        # print("setting list inside comma loop")
                        self.advance()
                        expr = self.expr()
                        # print("we dont have an error in expr")
                        # print("current token after expr: ", self.current_tok)
                        # print("expr: ", type(expr.node))
                        list_node.add_item(expr.node)
                    # print("token after comma loop:", self.current_tok)
                if self.current_tok.token == SRBRACKET:
                    print('found srbracket')
                    self.advance()
                    print(list_node.items)
                    return CropAssignNode(crop_name, list_node), None
                
            if self.current_tok.token == COLLECT:
                print("found collect in crop dec!")
                self.advance()
                #(
                self.advance()
                #STRING
                prompt = self.current_tok
                self.advance()
                # self.advance()
                print("current token after collect: ", self.current_tok)
                self.advance()
                print("crop name: ", crop_name, self.current_tok)
                #CropDecNode value: Collect(node)
                
                return CropAssignNode(crop_name, CollectNode(CropAccessNode(crop_name), prompt)), None

        else:
            print("found a comma in crop dec!: ", self.current_tok)
            if self.current_tok.token == COMMA:
                return CropAssignNode(crop_name, VoidNode(self.current_tok)), None
                #return result.success(CropDecNode(crop_name))
            elif self.current_tok.token == RPAREN:
                return CropAssignNode(crop_name, VoidNode(self.current_tok)), None
                #return result.success(CropDecNode(crop_name))
            elif self.current_tok.token == TERMINATOR:
                return CropAssignNode(crop_name, VoidNode(self.current_tok)), None
            else:
                
                print("found error in variable_declaration")
                return None, InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ), ', ' or ;!")
                #append a ParseResult instance sa list
                # res.append(result.success(CropDecNode(crop_name)))
                #self.advance()

    def crop_init(self, crop_name):
        #test
        # self.advance()
        print("Crop init: ", self.current_tok)  
        if self.current_tok.token == EQUAL:
            print("found equal")
            operation = self.current_tok
        elif self.current_tok.token == PLUS_EQUAL:
            print("found plus equal")
            operation = self.current_tok
        elif self.current_tok.token == MINUS_EQUAL:
            operation = self.current_tok
        elif self.current_tok.token == MUL_EQUAL:
            operation = self.current_tok
        elif self.current_tok.token == DIV_EQUAL:
            operation = self.current_tok
        # todo assignment operators

        self.advance()
        print("current token after equal: ", self.current_tok)
        if self.current_tok.token in (PLUS, MINUS, IDENTIFIER, INTEGER, FLOAT, LPAREN, STRING, VOIDEGG, TRUE, FALSE):
            expr = self.expr()
            return CropInitNode(crop_name, expr.node), None
        # check if it's crop a = [1, 3, true]
        if self.current_tok.token == SLBRACKET:
            list_node = ListNode(crop_name)
            
            self.advance()
            print("token after left bracket: ", self.current_tok)
            if self.current_tok.token in (IDENTIFIER, INTEGER, FLOAT, TRUE, FALSE, STRING):
                expr = self.expr()
                list_node.add_item(expr.node)
                
                while self.current_tok.token == COMMA:
                    self.advance()
                    expr = self.expr()
                    
                    list_node.add_item(expr.node)
            elif self.current_tok.token == SRBRACKET:
                self.advance()
                # print(list_node.items)
                print("[DEBUG] list node init: ", list_node.items)
                # self.advance()
                print("[DEBUG] tok after srbracket: ", self.current_tok)
                return CropInitNode(crop_name, list_node, operation), None
        if self.current_tok.token == COLLECT:
            print("found collect in crop init!")
            self.advance()
            #(
            self.advance()
            #STRING
            prompt = self.current_tok
            self.advance()
            # self.advance()
            print("current token after collect: ", self.current_tok)
            self.advance()
            print("crop name: ", crop_name, self.current_tok)
            #CropDecNode value: Collect(node)
            return CropInitNode(crop_name, CropAccessNode(crop_name)), None
        # todo assignment operators
        
        
    # * checks if the current token's a valid statement in body
    def is_statement(self):
        if self.current_tok.token == BREAK or self.current_tok.token == SINGLELINE or self.current_tok.token == COMMENT or self.current_tok.token == NEWLINE or self.current_tok.token in INTEGER or self.current_tok.token == IDENTIFIER or self.current_tok.token in FALL or self.current_tok.token in WINTER or self.current_tok.token in WINTER or self.current_tok.token in SHIP or self.current_tok.token in STAR or self.current_tok.token in DEW or self.current_tok.token in COLLECT or self.current_tok.token in CROP or self.current_tok.token in HARVEST or self.current_tok.token in CRAFT or self.current_tok.token in CRBRACKET or self.current_tok.token in EOF or self.current_tok.token == INCRE or self.current_tok.token == DECRE  or self.current_tok.token == COMMENT or self.current_tok.token == MULTILINE_OPEN or self.current_tok.token == MULTILINE_CLOSE or self.current_tok.token ==PERFECTION:
            return True
        else:
            return False
    
    #*LOOPING STATEMENTS
    # fall loop (for loop)
    def fall_stmt(self):
        #return a list of []
        print("FALL STATEMENT: ", self.current_tok)
        #TODO create fall
        if self.current_tok.token == LPAREN:
            self.advance()
            if self.current_tok.token == CROP:
                if self.current_tok.matches(CROP, 'crop'):
                    cropdec_result, cropdec_error = self.crop_dec()
                    if cropdec_error:
                        print("found error in: ", cropdec_error.as_string())
                        
                    else:
                        # print("no error in fall crop dec: ", self.current_tok)
                        
                        if self.current_tok.token == TERMINATOR:
                            fall_node_variable = cropdec_result
                            self.advance()
            elif self.current_tok.token == IDENTIFIER:
                crop_name = self.current_tok
                self.advance()
                # = 
                self.advance()
                #assign value dapat
                if self.current_tok.token in (PLUS, MINUS, IDENTIFIER, INTEGER, FLOAT, LPAREN):
                    expr = self.expr()
                    #self.advance()
                    fall_node_variable = CropInitNode(crop_name, expr.node)
                    self.advance()

                            # -----------------------------
            #call expr here
            if self.current_tok.token in (PLUS, MINUS, IDENTIFIER, INTEGER, FLOAT, LPAREN):
                condition = self.own_if_expr()
                #sobrang buried nya sa ParseResult hahaha
                fall_node_condition = condition.node.node
                fall_node = FallNode(fall_node_condition)
                fall_node.variable = fall_node_variable
                if self.current_tok.token == TERMINATOR:
                    self.advance()
                    # here na yung unary node
                    
                    if self.current_tok.token == IDENTIFIER:
                        unary = PostUnaryNode(CropAccessNode(self.current_tok))
                        self.advance()
                        if self.current_tok.token in (INCRE, DECRE):
                            unary.operation = self.current_tok
                            fall_node.unary = unary
                            self.advance()
                            #;
                            self.advance()
                            #)
                            # self.advance()
                            # # {
                            self.advance()
                            # call body
                    fall_node.unary = unary
                    print("fall body: ", self.current_tok)
                    result, body_error = self.body()
                    for item in result:
                        fall_node.add_child(item)
                    # fall_node.body = result
                    self.advance()
                    return fall_node

    #*conditional statements  
    def star_expr(self):
        res = ParseResult() # Create a ParseResult object to store result or errors
        cases = [] # List to store cases
        dew_case = [] # List to store dew cases
        errors = [] # List to store errors

        condition = res.register(self.own_if_expr()) # Parse the condition expression 
        if res.error:  # If error occurred during parsing the condition
            print("[DEBUG] error in condition")
            return [], errors
        condition = condition.node # Unpack AST node from ParseResult
        self.advance() # {
        print("[DEBUG] token after condition: ", self.current_tok) 
        if self.current_tok.token != CLBRACKET: # Check if the next token is {
            print ("err { 1")
            errors.append(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected { "
            ))
            return [], errors

        self.advance()
        print("BEFORE GOING INTO BODY: ", self.current_tok)
        result, body_error = self.body()
        #need to append it to cases as a tuple of (condition, [body result])
        cases.append((condition, result))
        if body_error:
            errors.append(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Error in body "
            ))
            print("BODY ERROR: ", body_error[0].as_string())
            return [], errors
        
        #return result.success(if_res_body)
        if res.error: 
            return [], errors
        
        #self.advance()
        #self.advance()
        #self.advance()
        while self.current_tok.token == NEWLINE:
            self.advance()
        self.advance()
        while self.current_tok.token == STARDEW:
            self.advance()
            self.advance()
            stardew_condition = res.register(self.own_if_expr()) # Parse condition
            stardew_condition = stardew_condition.node
            if res.error: 
                return [], errors

            self.advance()


            if self.current_tok.token != CLBRACKET:
                print("[DEBUG] err { 2")
                errors.append(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected { "
                ))
                return [], errors
            self.advance() 
            #todo need to append this its body
            result, body_error = self.body() # Parse body of stardew
            #need to append it to cases as a tuple of (condition, [body result])
            cases.append((stardew_condition, result))
            self.advance()
            #self.advance()
            

        if self.current_tok.token == DEW:
            # res.register_advancement()
            self.advance()
            # {
            self.advance()
            result, body_error = self.body() 
            for item in result: 
                dew_case.append(item)  # Add statements to else branch
            
            #return result.success(if_res_body)
            
                
            self.advance()

        self.advance()
        
        return StarNode(cases, dew_case), errors # Return AST node for the full if-elseif-else structure
    
    def winter_stmt(self):
        # cases = []
        self.advance()
        self.advance()
        condition = self.own_if_expr().node # Parse the condition expression

        condition = condition.node # Unpack AST node from ParseResult
        winter_node = WinterNode(condition) # Create AST node for the while-loop
        winter_node.condition = condition # Set the condition for the while-loop
        self.advance()
        #{
        self.advance()


        if self.in_condition == True: # Reset condition tracking state
            self.in_condition = False
        self.in_loop = True # Set state flag that we're parsing inside a loop
        result, body_error = self.body() # Parse the body of the while-loop

        
        for item in result: # Iterate through the parsed body statements
            winter_node.add_child(item) # Add each statement to the while-loop node
        

        if body_error:
            for i in body_error:
                print("[DEBUG] error in body if: ", i.as_string())
        # print("cases so far: ", cases)
        return winter_node # Return the while-loop node with its body statements
        
    def own_if_expr(self): # Result container
        res = ParseResult() # Create a ParseResult object to store result or errors 
        node =  self.bin_op(self.comp_expr, (AND_OP, OR_OP))# Parse expression with logical AND/OR operators
        return res.success(node) # Return the result of the expression parsing
         
    
    def arith_expr(self): # Parse + and - arithmetic operations
        node = self.bin_op(self.term, (PLUS, MINUS)) # Parse expression with + and - operators
        return node # Return the result of the expression parsing
    
    def comp_expr(self): # Parse comparison operations
        # print("comp expr first item: ", self.current_tok)
        res = ParseResult() # Create a ParseResult object to store result or errors

        if self.current_tok.matches(NOT_OP, '!'): # Check for NOT operator
            # print("comp expr not op")
            op_tok = self.current_tok # Store the NOT operator token
            # res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())  # Parse the expression to negate
            if res.error: 
                # print("error after not")
                return res
            if node.notted == True: # Flip its "not" state
                node.notted = False
            else:
                node.notted = True
                
            return res.success(node)
        # print("value after ! comp expr: ", self.current_tok)
        # Parse arithmetic comparison: <, >, <=, >=, ==, !=
        node = res.register(self.bin_op(self.arith_expr, (LESS_THAN, GREATER_THAN, LESS_THAN_EQUAL, 
        GREATER_THAN_EQUAL, E_EQUAL, NOT_EQUAL )))
        # print("token after arith expr: ", self.current_tok)
        
        if res.error:
            print("[DEBUG] arith error in comp expr")
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(' or 'NOT'"
            ))

        return res.success(node)
    
    

    #?PARSE RESULT ARE HERE
    def factor(self):
        # print("factor current tok: ", self.current_tok)
        res = ParseResult() # Create a ParseResult object to store result or errors
        tok = self.current_tok # Store the current token
        
        if tok.token in STRING: # If the current token is a string, advance and return a StringNode
            res.register(self.advance())
            return res.success(StringNode(tok))
        
        if tok.token in TRUE: # If the current token is TRUE, advance and return a BooleanNode
            res.register(self.advance())
            return res.success(BooleanNode(tok))

        if tok.token in FALSE: # If the current token is FALSE, advance and return a BooleanNode
            res.register(self.advance())
            return res.success(BooleanNode(tok))
        
        if tok.token in VOIDEGG: # If the current token is VOIDEGG, advance and return a VoidNode
            res.register(self.advance())
            return res.success(VoidNode(tok))

       
        
        # if tok.token in IDENTIFIER:
        #     return res.success(IdentifierNode(tok)) 
        
        if tok.token in (INCRE, negative, DECRE): # If the current token is an increment or decrement operator
            operation = self.current_tok # Store the operator token
            res.register(self.advance()) # 
            identifier = self.current_tok
            # If current token is a prefix operator, advance and recursively parse the next factor
            factor = res.register(self.factor()) # Wrap the factor in a PreUnaryNode with the corresponding operator
            if res.error: return res
            return res.success(PreUnaryNode(CropAccessNode(identifier), operation)) # If successful, return a node like ++A

        if tok.token in (INTEGER, FLOAT): #Basic numeric values wrapped as NumberNode
            res.register(self.advance())    
            return res.success(NumberNode(tok))
        
        
        if self.current_tok.token == IDENTIFIER: 
            print('found length: ', self.current_tok)
            #comment
            crop_name = self.current_tok
            self.advance() # Store identifier name and advance
            # print("next length: ",)
            if self.current_tok.token == LPAREN: # Function call: A(1, "hi")
                craft_call = CraftCallNode(tok) # Create a CraftCallNode and parse each parameter with correct type node
                self.advance()
                #look for 1, "string", true, false, void Repeated for each supported parameter type
                if self.current_tok.token in (INTEGER, FLOAT):
                    print("found number in craft call: ", self.current_tok)
                    craft_call.add_param(NumberNode(self.current_tok)) #Parse and add each parameter node
                    self.advance()
                elif self.current_tok.token == STRING:
                    craft_call.add_param(StringNode(self.current_tok)) # Parse and add each parameter node
                    self.advance()
                elif self.current_tok.token in (TRUE, FALSE):
                    craft_call.add_param(BooleanNode(self.current_tok)) # Parse and add each parameter node
                    self.advance()
                elif self.current_tok.token == VOIDEGG:
                    craft_call.add_param(VoidNode(self.current_tok)) # Parse and add each parameter node
                    self.advance()
                elif self.current_tok.token == IDENTIFIER: 
                    print("ident craft")
                    crop_name = self.current_tok
                    # self.advance()
                    # if self.current_tok.token == SLBRACKET:
                    #     print("list!")
                    #     self.advance()
                    #     index = self.expr()
                    #     index = index.node
                    #     print("after index: ", self.current_tok )
                    #     self.advance()
                    #     craft_call.add_param(ListCallNode(CropAccessNode(crop_name), index))
                    # index = self.expr()
                    # index = index.node
                   
                    expr = self.expr()
                    expr = expr.node
                    
                    craft_call.add_param(expr)
                    print("craft call add param: ", self.current_tok)
                    # self.advance()
                
                while self.current_tok.token == COMMA: # Loop through all arguments in the function call
                    print("found comma in craft call")
                    self.advance()
                    if self.current_tok.token in (INTEGER, FLOAT):
                        craft_call.add_param(NumberNode(self.current_tok))
                        self.advance()
                    elif self.current_tok.token == STRING:
                        craft_call.add_param(StringNode(self.current_tok))
                        self.advance()
                    elif self.current_tok.token in (TRUE, FALSE):
                        craft_call.add_param(BooleanNode(self.current_tok))
                        self.advance()
                    elif self.current_tok.token == VOIDEGG:
                        craft_call.add_param(VoidNode(self.current_tok))
                        self.advance()
                    elif self.current_tok.token == IDENTIFIER:
                        print("ident craft")
                        
                        
                        expr = self.expr()
                        expr = expr.node
                        craft_call.add_param(expr)

                            # craft_call.add_param(CropAccessNode(crop_name))
                #this should be a ) token
                self.advance()
                # self.advance()
                #this is a semicolon
                
                
                return res.success(craft_call)
            elif self.current_tok.token == SLBRACKET: # List access: A[1]
                # print("in list factor")
                self.advance()
                # index[3-1]
                # index = self.current_tok
                index = self.expr() # Parse an expression inside square brackets for list indexing
                if index.error: # If error occurred during parsing the expression
                    print("error in list cond")
                index = index.node # Unpack AST node from ParseResult
                self.advance() 
                return res.success(ListCallNode(CropAccessNode(crop_name), index)) # Return a ListCallNode with the crop name and index
            if self.current_tok.token in (INCRE, DECRE): # If followed by ++ or --, return a PostUnaryNode
                return res.success(PostUnaryNode(CropAccessNode(tok), self.current_tok)) # 
            else:
                return res.success(CropAccessNode(tok)) # Basic variable access without function or indexing
        
        elif tok.token == LPAREN: # Grouped expressions (A + B)
            res.register(self.advance()) 
            # print("value after lparen: ", self.current_tok)
            expr = res.register(self.comp_expr()) # Handle parenthesized expression recursively with comp_expr
            if res.error: return res
            print("after lparen expr: ", self.current_tok)
            if self.current_tok.token == RPAREN:
                res.register(self.advance()) # Ensure proper closing ) and return the grouped expression node
                return res.success(expr)
            else:
                print("error after lparen")
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        #return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float"))
    
    def term(self): # Handles multiplication, division, and modulo operations (higher precedence than addition)
        return self.bin_op(self.factor, (MUL, DIV, MODULUS)) # Build a binary expression tree using factor() as base and given operators.
    
        #really this means:
        '''
        def bin_op(self, func, ops):
            left = factor()

            while self.current_tok in ops: # ops instead of (MUL, DIV)
                op_tok = self.current_tok
                right = factor()
                left = BinOpNode(left, op_tok, right)

            return left
            
        '''

    def expr(self): # Handles addition and subtraction (lower precedence than term())
        
        return self.bin_op(self.term, (PLUS, MINUS)) # Uses term() as base level and processes + and - operators

        #todo add string expr
        #really this means:
        '''
        def bin_op(self, func, ops):
            left = term()

            while self.current_tok in ops: #ops instead of (PLUS, MINUS)
                op_tok = self.current_tok
                right = term()
                left = BinOpNode(left, op_tok, right)

            return left
            
        '''
   
    #func is rule (expr or term) builds binary expression tree
    # A - B / 4
    def bin_op(self, func, ops): # helper for building binary operator trees
        # print("func: ", func)
        # print("bin op current tok: ", self.current_tok)
        res = ParseResult()
        # print('first token in bin op: ', self.current_tok.token)
        left = res.register(func()) #instead of self.factor() or self.term() 
        #NumberNode
        if res.error:
            print("error in left node: ", res.error.as_string())
            return res
        while self.current_tok.token in ops: #instead of (MUL, DIV)
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func()) #instead of self.factor() or self.term()
            if res.error:
                print("error in right node")
                return res
            left = BinOpNode(left, op_tok, right) 
            # (left=NumberNode op_tok = + right = NumberNode)

        return res.success(left)
    
####################
#* INTERPRETER (checking if the node is valid - semantic)
class Interpreter:
    #eto yung kinocall natin sa run
    # 
    # automatic na malalagay yung name ng node kaya ganyan yung method_name
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_Program(self, node, symbol_table): 

        for item in node.body:
            if isinstance(item, CropAssignNode):
                value = self.visit(item, symbol_table)
                if value.error:
                    node.errors.append(value.error)

                symbol_table.set(item.crop_name_tok.value, value.value)
                print("global variables: ", symbol_table.symbols)
            elif isinstance(item, CraftNode):
                item.symbol_table = SymbolTable(f"<craft {item.identifier}>")
                item.symbol_table.parent = symbol_table
                node.functions.append(item)
                for i in item.parameters:
                    item.symbol_table.set(i.crop_name_tok.value, i)
                print("functions: ", node.functions)
                # for i in item.body:
                #     value = self.visit(i, item.symbol_table)
                #     if value.error:
                #         print("error in pelican()")
                #         node.errors.append(value.error)
            elif isinstance(item, PelicanNode):
                
                # pelican_context.parent_entry_pos = node.body[0].pos_start
                item.symbol_table = SymbolTable("<pelican()>")
                item.symbol_table.parent = symbol_table
                for i in item.body:
                    i.parent = item
                    value = self.visit(i, item.symbol_table)
                    if value.error:
                        print("error in pelican()")
                        node.errors.append(value.error)

        # print ("global symbols: ", )
        return node

    def visit_CraftCallNode(self, node, symbol_table):
        craft_call_node = node
        craft_ident =  node.identifier.value
        res = RTResult()
        # print("node parent:  ", node.parent)
        while node.parent:
            node = node.parent
        # print("node:  ", node)
        if isinstance(node, CraftCallNode):
            # print("found craft call")
            pass
        for item in node.functions:
            
            if item.identifier.value == craft_ident:
                # print("function is declared")
                item.called = True
                print("FUNCTION NAME: ", item.identifier.value)
                print("FUNCTION called?: ", item.called)
                if len(item.parameters) == len(craft_call_node.parameters):
                    # print("valid number of params")
                    #here we need to assign the value of params to the value of the craft call param to to the value of the function
                    # ah so we can set the value of test(crop a, var b) crop a to "hello"
                    #current item should be assigned to the symbol table of the parameter's function
            
                    for i in range(len(item.parameters)):
                        param_item = item.parameters[i]
                        param_call_node = craft_call_node.parameters[i]
                        # print('param call node: ', param_call_node)
                        # Visit the parameter in the function call to resolve its value
                        param_value = self.visit(param_call_node, symbol_table)
                        if param_value.error:
                            print("error in calling param")
                            return res.failure(param_value.error)
                        # print("param value: ", param_value.value)

                        # Assign the value to the corresponding parameter in the symbol table
                        item.symbol_table.set(param_item.crop_name_tok.value, param_value.value)
                        # print(f"symbol table of the called param {i}: ", craft_call_node.parent.symbol_table.symbols)
                        
                    item.called = True
                    for i in item.body:
                        # print("item in the called craft: ", i)
                        # if isinstance(i, HarvestCallNode):
                        #     # print("found harvesst call in called craft")
                        #     value = self.visit(i, item.symbol_table)
                        #     # print("harvest symbol table: ", item.symbol_table.symbols)
                        #     # print("value of harvest call: ", value.value)
                        #     if value.error:
                        #         return res.failure(value.error)
                        #     # print("node.value craft call: ", node.val)
                        #     # i.value = value.value
                            
                        #     craft_call_node.value = value.value
                        #     break
                        value = self.visit(i, item.symbol_table)
                        
                        if value.error:
                            print("error in pelican()")
                            node.errors.append(value.error)
                    return res.success(craft_call_node)
                else:
                    print("invalid number of params")
                    return res.failure(SemanticError(
                craft_call_node.pos_start, craft_call_node.pos_end,
                f"\ncraft '{craft_ident}' takes {len(item.parameters)} parameters, received {len(craft_call_node.parameters)} arguments ",
            ))
        if craft_ident == "Add" or craft_ident == "Pluck" or craft_ident == "Length":
            return res.success(craft_call_node)
        return res.failure(SemanticError(
                craft_call_node.pos_start, craft_call_node.pos_end,
                f"\n '{craft_ident}' is not defined",
            ))

    def visit_CropAccessNode(self, node, symbol_table):
        # print("in crop access node")
        res = RTResult()

        crop_name = node.crop_name_tok.value
        value = symbol_table.get(crop_name)
        # print("value crop access: ", value)
        # print("crop access symbol table: ", symbol_table.symbols)
        
        if not value and value != 0 and not isinstance(value, list):
            # print("couldnt find variable")
            if symbol_table.parent:
                # print("theres a parent: ", symbol_table.parent.symbols)
                value = symbol_table.parent.get(crop_name)
                if not value and value != 0:
                    # print("theres no value")
                    return res.failure(SemanticError(
                node.pos_start, node.pos_end,
                f"\n'{crop_name}' is not defined in {symbol_table.name}"
            ))
                value = value.copy().set_pos(node.pos_start, node.pos_end)
                return res.success(value)
            return res.failure(SemanticError(
                node.pos_start, node.pos_end,
                f"\n'{crop_name}' is not defined",
            ))
        # print(f"value type {value}, {type(value)}")
        # value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)


    def visit_HarvestCallNode(self, node, symbol_table):
        res = RTResult()
        # print("harvest call value node: ", node.value_node)
        # print("visit harvest: ", symbol_table.symbols)
        node.value_node.parent = node
        value = self.visit(node.value_node, symbol_table)
        # print('value in harvest call: ', (value.error))
        if value.error:
            return res.failure(value.error)
        node.value = value
        
        return res.success(value)
    
    def visit_ShipNode(self, node, context):
        res = RTResult()
        values = []
        for item in node.body:
            # print("item in ship: ", item)
            # if isinstance(item, CraftCallNode):
            #     item.parent = node.parent
            item.parent = node
            # print("item: ", item)
            # print("item parent: ", item.parent)
            value = self.visit(item, context)
            
            # print("value type: ", type(value))
            if value.error:
                value.error.print_error()
                # print("item.pos_end: ", item.pos_end)
                
                value.error.print_error()
                return value
                # return res.failure(value.error)
            values.append(value.value)
        return res.success(values)
    
    def visit_CollectNode(self, node, context):
        # print("collect parent: ", node.parent)
        # print("variable node: ", node.variable_node)
        res = RTResult()
        value = self.visit(node.variable_node, context)
        if value.error:
            print("ERROR IN COLLECTNODE")
            return res.failure(value.error)
        # print("value collect: ", value.value)
        # print("paren symbol table collect before setting: ", node.parent.symbol_table.symbols)
        print("CROP NAME TOk: ", node.variable_node.crop_name_tok)
        context.set(node.variable_node.crop_name_tok, value.value)
        # print("paren symbol table collect: ", node.parent.symbol_table.symbols)
        return res.success(node)
    # identifier: a

    
    def visit_CropAssignNode(self, node, symbol_table):
        print("in crop assign node: ", node.crop_name_tok)
        print("Node value: ", node.value_node)
        res = RTResult()
        crop_name = node.crop_name_tok.value
        symbol_table.set(crop_name, Number(0))
        if isinstance(node.value_node, CraftCallNode):
            # print("assigning a function")
            node.value_node.parent = node.parent
        if isinstance(node.value_node, BinOpNode):
            # print("assigning a function")
            node.value_node.parent = node.parent
        if isinstance(node.value_node, ListNode):
            pass
        if isinstance(node.value_node, CollectNode):
            print("Value is Collect Node")
            # symbol_table.set(crop_name, node.value_node.prompt)
        else:
            # print("ASSIGNED A LIST")
            # node.value_node.parent = node.parent
            value = res.register(self.visit(node.value_node, symbol_table))
            symbol_table.set(crop_name, value)
        
        # print("value of list : ", value)
        # print(f"assign value type {value}: {type(value)}")
        if res.error: 
            print("error var assign")
            return res

        
        # print("symbol table var assign: ", symbol_table.symbols)
        #returns rtresult
        return res.success(node)
    
    
    def visit_CropInitNode(self, node, symbol_table):
        res = RTResult()
        if isinstance(node.crop_name_tok, ListCallNode):

            crop_name = node.crop_name_tok.crop_name.value
            value = symbol_table.get(crop_name)
            if not value and value != 0 and not isinstance(value, list):
                print("couldnt find variable")
                return res.failure(SemanticError(
                    node.pos_start, node.pos_end,
                    f"\n'{crop_name}' is not defined",
                ))
        else:
            crop_name = node.crop_name_tok.value
            value = symbol_table.get(crop_name)
            if not value and value != 0:
                print("couldnt find variable")
                return res.failure(SemanticError(
                    node.pos_start, node.pos_end,
                    f"\n'{crop_name}' is not defined",
                ))      
        # print("in crop assign node: ", node.crop_name_tok)
        res = RTResult()
        # crop_name = node.crop_name_tok.value
        if isinstance(node.value_node, CraftCallNode):
            # print("assigning a function")
            node.value_node.parent = node.parent
        if isinstance(node.value_node, ListNode):
            print("ASSIGNED A LIST")
            # node.value_node.parent = node.parent
        value = res.register(self.visit(node.value_node, symbol_table))
        # print("value of a: ", type(value))
        # print(f"assign value type {value}: {type(value)}")
        if res.error: return res

        symbol_table.set(crop_name, value)
        
        #returns rtresult
        return res.success(value)

    def visit_CropDecNode(self, token, context):
        res = RTResult()
        crop_name = token.crop_name_tok
        # print("crop name: ", crop_name)
        #value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        
        context.set(crop_name, Void(None).set_context(context).set_pos(token.pos_start, token.pos_end))
        
        # return res.value
        return RTResult().success(
            Number(crop_name).set_context(context).set_pos(token.pos_start, token.pos_end)
        )
    # -- visit_VoidNode
    def visit_VoidNode(self, node, context):
        return RTResult().success(
            Void(value = None).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, symbol_table):
        res = RTResult()
        list_res = []
        for item in node.items:
            value = self.visit(item, symbol_table)
            if value.error:
                return res.failure(value.error)
            list_res.append(value.value)
        # print("list res: ", list_res)
        # print("found list")
        return res.success(list_res)
    
    def visit_ListCallNode(self, node, symbol_table):
        res = RTResult()
        value = self.visit(node.crop_name, symbol_table)
        if value.error:
            return res.failure(value.error)
        return res.success(node)

    def visit_NumberNode(self, node, context):
        
        return RTResult().success(
            Number(node.tok.value)
        )
    
    def visit_StringNode(self, node, context):
        # print("found string node")
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_BooleanNode(self, node, symbol_table):
        # print("found boolean node")
        res = RTResult()
        if node.value == 0:
            return(res.success(
                SemanticFalse(node)
                ))
        else:
            return(res.success(
                SemanticTrue(node)
                ))
        
    def visit_PostUnaryNode(self, node, symbol_table):
        # print("found post unary")
        res = RTResult()
        value = self.visit(node.tok, symbol_table)
        if value.error:
            return res.failure(value.error)
        return res.success(value)
    def visit_PreUnaryNode(self, node, symbol_table):
        # print("found post unary")
        res = RTResult()
        value = self.visit(node.tok, symbol_table)
        if value.error:
            return res.failure(value.error)
        return res.success(value)
    def visit_BinOpNode(self, node, context):
        # print("bin op parent", node.parent)
        res = RTResult()
        # if isinstance(item, CraftCallNode):
        #     item.parent = node.parent
        if isinstance(node.left_node, CraftCallNode) or isinstance(node.left_node, BinOpNode):
            node.left_node.parent = node.parent
        left = res.register(self.visit(node.left_node, context))
        # print("left of Bin op: ", type(left))
        if res.error: return res
        if isinstance(node.right_node, CraftCallNode) or isinstance(node.right_node, BinOpNode):
            node.right_node.parent = node.parent
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        # check natin if yung left factor natin number, pag hindi error dapat
        # print("type of left: ", type(left))
        # if not isinstance(left, Number):
        #     return res.failure(RTError(
        #             node.pos_start, node.pos_end,
        #             f"Invalid value: '{left}' type: {type(left)} in operation",
        #             context
        #         ))

        if node.op_tok.token == PLUS:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
           
            result, error = left.added_to(right)
            
        elif node.op_tok.token == MINUS:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number) or not isinstance(left, Number):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation({node.op_tok.token}) between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.subbed_by(right)
        elif node.op_tok.token == MUL:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number) and not isinstance(left, Number) and not isinstance(right, Void) and not isinstance(left, Void):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation({node.op_tok.token}) between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.multed_by(right)
        elif node.op_tok.token == DIV:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number) and not isinstance(left, Number)and not isinstance(left, Void)and not isinstance(right, Void):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation({node.op_tok.token}) between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.dived_by(right)
        elif node.op_tok.token == MODULUS:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number) or not isinstance(left, Number):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation({node.op_tok.token}) between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.modulo(right)
        elif node.op_tok.token == E_EQUAL:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(left, Number) and not isinstance(left, String):
            #         print("right in e_equal is not a number")
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation between {left} and type:{type(right)}:{right}',
            #     ))
            
            # print("found e_eq: ", type(left))
            print("LEFT TYPE: ", type(left))
            if isinstance(left, Token):
                print("TOKEN LEFT: ", left)
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.token == NOT_EQUAL:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            
            result, error = left.get_comparison_ne(right)
            
        elif node.op_tok.token == LESS_THAN:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number) or not isinstance(left, Number) and not isinstance(left, Void):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.token == GREATER_THAN:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            print("LEFT: ", left)
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.token == LESS_THAN_EQUAL:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number)or not isinstance(left, Number):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.token == GREATER_THAN_EQUAL:
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number)or not isinstance(left, Number):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(AND_OP, '&&'):
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.anded_by(right)
        elif node.op_tok.matches(OR_OP, '||'):
            if isinstance(left or right, list):
                list_res = RTResult()
                return list_res.success(Number(1))
            # if not isinstance(right, Number):
            #         return res.failure(RTError(
            #         node.pos_start, node.pos_end,
            #         f'Invalid operation between {left} and type:{type(right)}:{right}',
            #     ))
            result, error = left.ored_by(right)
        
        if error:
            return res.failure(error)
        else:
            
            final = res.success(result.set_pos(node.pos_start, node.pos_end))
            # print('final: ', final.value)
            return res

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.token == MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
    def visit_FallNode(self, node, symbol_table):
        res = RTResult()
        value = self.visit(node.variable, symbol_table)
        if value.error:
            return res.failure(value.error)
        for item in node.body:
            val = self.visit(item, symbol_table)
            if val.error:
                return res.failure(val.error)
        return res.success(value)
    
    def visit_WinterNode(self, node, symbol_table):
        # print("found a winter node")
        res = RTResult()
        # print("winter condition: ", node.condition)
        node.condition.parent = node
        condition_value = res.register(self.visit(node.condition, symbol_table))
        # print("condition value: ", condition_value)
        if res.error: 
            # print("error in visit node")
            return res

        if condition_value.is_true():
            # print("found true condition: ", condition_value)
            for item in node.body:
                expr_value = self.visit(item, symbol_table)
                if expr_value.error:
                    print("error 1")
                    return res.failure(expr_value.error)
                if isinstance(item, HarvestCallNode):
                    # print("harvest call in winter")
                    return res.success(HarvestCallNode(expr_value))
                
                if res.error: 
                    print("error 2")
                    return res
            return res.success(node)

    def visit_StarNode(self, node, context):
        list_of_ship = []
        res = RTResult()
        # print("node.cases: ", node.cases)
        print("node body: ", node.body)
        for condition, expr in node.cases:
            # print("visiting nodes now")
            condition.parent = node
            condition_value = res.register(self.visit(condition, context))
            print("condition value: ", condition_value)
            if res.error: 
                print("error in visit star node")
                return res

            if condition_value.is_true():
                # print("found true condition: ", condition_value)
                for item in expr:
                    expr_value = res.register(self.visit(item, context))
                    if isinstance(item, HarvestCallNode):
                        # print("return call in if")
                        return res.success(HarvestCallNode(expr_value))
                    if isinstance(item, ShipNode):
                        # print("ship in if")
                        list_of_ship.append(ShipNode(expr_value, item.ship_tok))
                    # print("expr in if node: ", expr)
                    '''
                    res.append(result.success(HarvestCallNode(expr)))
                    '''
                    if res.error: 
                        return res
                return res.success(list_of_ship)
        for i in node.body:
            i.parent = node.parent
            value = res.register(self.visit(i, i.parent.symbol_table))
            if res.error:
                print("error in pelican()")
                # node.errors.append(value.error)
                return res
        # print("floating")
        if node.dew_case:
            # print("we have an else case")
            for item in node.dew_case:
                dew_value = res.register(self.visit(item, context))
                if isinstance(item, HarvestCallNode):
                    # print("return call in if")
                    # print("else value type: ", type(dew_value))
                    return res.success(HarvestCallNode(dew_value))
                if isinstance(item,ShipNode):
                    # print("ship in else")
                    return res.success(ShipNode(dew_value, item.ship_tok))
            if res.error: return res
            return res.success(dew_value)

        return res.success(None)
    def visit_NextNode(self, node, symbol_table):
        res = RTResult()
        return res.success(node)
    def visit_BreakNode(self, node, symbol_table):
        res = RTResult()
        return res.success(node)
class Void: # checking if the value is void, chinecheck na yung meaning ng void
    def __init__(self, value=None):
        self.value = 'void'
        self.set_pos()
        self.set_context()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self
    def added_to(self, other):
        return Number(1).set_context(self.context), None

    def subbed_by(self, other):
        
        return Number(1).set_context(self.context), None
        

    def multed_by(self, other):
        
        return Number(1).set_context(self.context), None
        

    def dived_by(self, other):
        
        return Number(1).set_context(self.context), None
        
    def modulo(self, other):
        
        return Number(1).set_context(self.context), None
        
    def get_comparison_eq(self, other):
        
        return Number(1).set_context(self.context), None

    def get_comparison_ne(self, other):
        
        return Number(1).set_context(self.context), None

    def get_comparison_lt(self, other):
        
        return Number(1).set_context(self.context), None

    def get_comparison_gt(self, other):
        
        return Number(1), None

    def get_comparison_lte(self, other):
       
        return Number(1).set_context(self.context), None

    def get_comparison_gte(self, other):
        
        return Number(1).set_context(self.context), None

    def anded_by(self, other):
        
        return Number(1).set_context(self.context), None

    def ored_by(self, other):
       
        return Number(1).set_context(self.context), None

    def notted(self):
        return Number(1).set_context(self.context), None
    
    def copy(self):
        copy = Void(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return "void"

class SemanticTrue: # check if the value is true / boolean
    def __init__(self, node, value=None):
        self.value = value
        self.pos_start = node.tok.pos_start
        self.pos_end = node.tok.pos_end
        # self.set_pos()
        # self.set_context()
    def is_true(self):
        return True
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    def added_to(self, other):
        return Number(1), None
        

    def subbed_by(self, other):
        
        return Number(1), None
        

    def multed_by(self, other):
        
        return Number(1), None
        

    def dived_by(self, other):
        return Number(1), None
    def modulo(self, other):
        
        return Number(1), None
        
    def get_comparison_eq(self, other):
        
        return Number(1), None

    def get_comparison_ne(self, other):
        
        return Number(1), None

    def get_comparison_lt(self, other):
        return Number(1), None

    def get_comparison_gt(self, other):
        return Number(1), None

    def get_comparison_lte(self, other):
        return Number(1), None

    def get_comparison_gte(self, other):
        return Number(1), None

    def anded_by(self, other):
        return Number(1), None

    def ored_by(self, other):
        return Number(1), None

    def notted(self):
        return Number(1), None
    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        copy = SemanticTrue(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
class SemanticFalse: # check if the value is false / boolean
    def __init__(self, node, value=None):
        self.value = value
        self.pos_start = node.tok.pos_start
        self.pos_end = node.tok.pos_end
        # self.set_pos()
        # self.set_context()
    def added_to(self, other):
        return Number(1), None
        

    def subbed_by(self, other):
        
        return Number(1), None
        

    def multed_by(self, other):
        
        return Number(1), None
        

    def dived_by(self, other):
        return Number(1), None
    def modulo(self, other):
        
        return Number(1), None
        
    def get_comparison_eq(self, other):
        
        return Number(1), None

    def get_comparison_ne(self, other):
        
        return Number(1), None

    def get_comparison_lt(self, other):
        return Number(1), None

    def get_comparison_gt(self, other):
        return Number(1), None

    def get_comparison_lte(self, other):
        return Number(1), None

    def get_comparison_gte(self, other):
        return Number(1), None

    def anded_by(self, other):
        return Number(1), None

    def ored_by(self, other):
        return Number(1), None

    def notted(self):
        return Number(1), None
    def is_true(self):
        return False
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        copy = SemanticFalse(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        
        return Number(1).set_context(self.context), None
        # return None, RTError(
        #             other.pos_start, other.pos_end,
        #             f'{other} added to number',
                    
        #         )

    def subbed_by(self, other):
        return Number(1).set_context(self.context), None
                

    def multed_by(self, other):
        return Number(1).set_context(self.context), None

    def dived_by(self, other):
        return Number(1).set_context(self.context), None

    def modulo(self, other):
        return Number(1).set_context(self.context), None
    def get_comparison_eq(self, other):
        return Number(1).set_context(self.context), None

    def get_comparison_ne(self, other):
        
        return Number(1).set_context(self.context), None

    def get_comparison_lt(self, other):
        return Number(1).set_context(self.context), None

    def get_comparison_gt(self, other):
        return Number(1).set_context(self.context), None

    def get_comparison_lte(self, other):
        
        return Number(1).set_context(self.context), None

    def get_comparison_gte(self, other):
        return Number(1).set_context(self.context), None

    def anded_by(self, other):
        return Number(1).set_context(self.context), None

    def ored_by(self, other):
        return Number(1).set_context(self.context), None

    def notted(self):
        return Number(1).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return str(self.value)
    
class String:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def concat(self, other):
        # if isinstance(other, String) or isinstance(other, CraftCallNode):
        #     string = ''
        #     # string += self.value
        #     # string += other.value
        return String(self.value).set_context(self.context), None
        # return None, RTError(
        #             other.pos_start, other.pos_end,
        #             f"Invalid value '{other}', type: {type(other)} concatenated with string",
                    
        #         )

    def get_comparison_eq(self, other):
        
        return String(str(self.value)).set_context(self.context), None
        
    def get_comparison_ne(self, other):
        return String(str(self.value)).set_context(self.context), None
    def added_to(self, other):
        
        return String(1).set_context(self.context), None
        

    def subbed_by(self, other):
        if isinstance(other, Number)or isinstance(other, Void):
            return Number(self.value - other.value).set_context(self.context), None
        return None, RTError(
                    other.pos_start, other.pos_end,
                    f'{other} subtracted from number',
                    self.context
                )

    def multed_by(self, other):
        if isinstance(other, Number) or isinstance(other, Void):
            return Number(self.value * other.value).set_context(self.context), None
        return None, RTError(
                    other.pos_start, other.pos_end,
                    f'Number  multiplied by {other}',
                    
                )

    def dived_by(self, other):
        if isinstance(other, Number)or isinstance(other, Void):
            # if other.value == 0:
            #     return None, RTError(
            #         other.pos_start, other.pos_end,
            #         'Division by zero',
                    
            #     )
            return Number(1).set_context(self.context), None
        else:
            return None, RTError(
                    other.pos_start, other.pos_end,
                    f'Number divided by {other} ',
                    self.context
                )    

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(1).set_context(self.context), None


    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(1).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(1), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(1).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(1).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(1).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(1).set_context(self.context), None

    def is_true(self):
        return self.value != 0
     
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    # def __repr__(self):
    #     return str(self.value)
    

        
# class Context:
#     def __init__(self, display_name, parent=None):
#         self.display_name = display_name
#         self.parent = parent
#         self.symbol_table = SymbolTable()

#######################################
# SYMBOL TABLE
#######################################

class SymbolTable: # keep track of the variables
    def __init__(self, name = None):
        self.symbols = {}
        self.parent = None
        self.name = name

    def set_parent(self, node):
        self.parent = node

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


#RUN THE PROGRAM
#this will go to main


def run(fn, text):
    # print("running")
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    # Create a new list excluding spaces or lists
    tokens = [item for item in tokens if not (isinstance(item, list) or item.token == SPACE)]
    # for item in tokens:
    #     if isinstance(item, list):
    #         tokens.remove(item)
    # todo parser_syntax parser
    parser = Parser(tokens)
    print('PARSER TOKENS: ', parser.tokens)

    # todo semantic parser
    ast = parser.parse()
    print("AST: ", ast)
    # print(ast[1][0].as_string()) #dito raw error
    # print("ast: ", ast)
    #ast is a Program instance
    # print("ast body: ", ast.body)
    ast.display() # ast yung nirereturn ng parser, ast is a Program instance, yung Program may display method-- yun yung nag pprint sa terminal
    #ast is a Program instance
    # -- return ast
    #here i need to visit the ast nodes hahaha
    
    interpreter = Interpreter()
    symbol_table = SymbolTable("<Junimo Code>") # gawa ng symbol table
    # context.symbol_table = global_symbol_table
    symbol_table.symbols = {} #initialize empty symbol table
    ast.symbol_table = symbol_table # yung Program instance may symbol_table na property
    res = interpreter.visit(ast, symbol_table)
    #ast is a Program instance
    # for every node sa ast, ivivisit natin siya
    # tapos each node has a child, ivivisit den natin yun
    # Program
        # FarmhouseNode
        # CraftNode
        # PelicanNode
            # ShipNode
    
    if res.errors:
        print("found error in program")
        print("found error: ", res.errors)
        for error in res.errors:
            print(error.as_string())
        return res, res.errors
    return res, None

'''
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    #return tokens, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result.value, result.error
'''
       
  

# def run(fn, text):
#     lexer = Lexer(fn, text)
#     tokens, error = lexer.make_tokens()
    
#     # Create a new list excluding spaces or lists
#     tokens = [item for item in tokens if not (isinstance(item, list) or item.token == SPACE)]
    
#     print("TOKENS: ", tokens)
    
#     parser = Parser(tokens)
#     result, parseError = parser.parse()
    

#     return result, parseError

import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
import tkinter as tk
from itertools import count
from PIL import Image, ImageTk  # Import Pillow
from pathlib import Path
from tkinter import filedialog
import parser_syntax
import lexer
import os
import sys
import subprocess
import semantic
from nodes1 import convert_text_file_to_python_and_execute
from pathlib import Path
from ctypes import windll

# Register custom fonts
windll.gdi32.AddFontResourceW("Stardew-Valley-Regular.ttf")
windll.gdi32.AddFontResourceW("StardewValley.ttf")

# Initialize sound library
mixer.init()

# Load sound effects
click_sound = mixer.Sound("Interface/bigSelect.wav")
hover_sound = mixer.Sound("Interface/select.wav")
delete_sound = mixer.Sound("Interface/bigDeSelect.wav")
output_sound = mixer.Sound("Interface/newRecipe.wav")
#background_music = r"BackgroundMusic/ConcernedApe - Stardew Valley OST - 01 Stardew Valley Overture.mp3"
background_music = r"Ambience\fall_day.wav"
# Stardew Valley-themed colors
BACKGROUND_COLOR = "#F5F5DC"  # Soft beige for Stardew Valley theme
TEXT_COLOR = "#3B200E"  # Brown text for title and content
BUTTON_COLOR = "#8B7355"  # Wooden Button-like
HOVER_COLOR = "#6FA3EF"  # Blue hover effect for buttons
TABLE_COLOR = "#D9C2A6"  # Inventory-like background
TERMINAL_COLOR = "#F5F5DC"  # Softer beige for terminal

# Font settings
TITLE_FONT = ("Stardew Valley Regular", 48)  # Large title font
PIXEL_FONT = ("Verdana", 12, "bold" )  # Font for other UI elements

# Paths for assets
background_image_path = r"Images\background.png"

#Cursor
junimo_cursor = "Stardew_Cursor.xpm" #Not Yet Working ; Maganda sana na-additional kaechosan.


class StardewLexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Junimo Code")
        self.root.geometry("1920x1200")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.code = None

        # Play background music
        mixer.music.load(background_music)
        mixer.music.play(loops=-1)

        # Set theme for CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # Setup UI elements
        self.setup_background()
        self.setup_widgets()


    def setup_background(self):
        # Load and stretch the background image
        bg_image = Image.open(background_image_path)
        bg_image = bg_image.resize((1920, 1200), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Place the background image on canvas
        self.canvas = tk.Canvas(self.root, width=1920, height=1200, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.canvas.pack(fill="both", expand=True)
        self.bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        
    def update_line_numbers(self):
        """Synchronize line numbers with text lines in the code_input box."""
        # Enable editing for the line number widget
        self.line_numbers.configure(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)

        # Get the number of lines in the code_input
        code = self.code_input.get("1.0", tk.END)
        self.code = code
        lines = code.split("\n")  # Count lines

        # Add line numbers for each line
        for i in range(1, len(lines) + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

        # Ensure the line numbers are aligned with the text
        self.line_numbers.configure(state=tk.DISABLED)

        # Align the font size with the code_input
        self.line_numbers.configure(font=("Verdana", 11))  # Set font and size

        # Adjust spacing to add margin or padding
        self.line_numbers.configure(spacing1=3.5)  # Default spacing for all lines
        self.line_numbers.tag_configure("first_line", spacing1=18)  # Adjust first-line spacing

        # Apply custom alignment for the first line
        self.line_numbers.tag_add("first_line", "1.0", "1.end")
        self.line_numbers.tag_configure("center", justify="center")  # Center-align numbers
        self.line_numbers.tag_add("center", "1.0", "end")

        # Update the scroll synchronization
        self.line_numbers.yview_moveto(self.code_input.yview()[0])
        self.code_input.configure(font=("Verdana", 12))  # Match font size
 # Match font size
    # Match font size
           
    def sync_scrollbars(self, *args):
        try:
            # Synchronize the scroll position of the line numbers with the code input
            self.line_numbers.yview_moveto(self.code_input.yview()[0])
            self.code_input.yview(*args)
        except Exception as e:
            print(f"Error syncing scrollbars: {e}")


    def setup_widgets(self):
        # Input box for code
        self.code_frame = ctk.CTkFrame(self.root, width=300, height=600, fg_color="#8f3901", corner_radius=10) #width and height of the outline box
        self.code_frame.place(x=100, y=94) #x and y for input box
        self.code_input = ctk.CTkTextbox(self.code_frame, width=660, height=500, #width and height of the box
                                         font=("Verdana", 12),
                                         fg_color="#ffe9db",
                                         text_color=TEXT_COLOR,
                                         wrap="word")
        self.code_input.configure(spacing1=3.5)
        # Insert placeholder text
        self.placeholder_text = "Code will be placed here...\n"
        self.code_input.insert(tk.END, self.placeholder_text)
                        # Bind to update line numbers dynamically
        self.code_input.bind("<KeyRelease>", lambda event: self.update_line_numbers())
        self.code_input.bind("<MouseWheel>", lambda event: self.update_line_numbers())

 # Error at line numbers
        self.line_numbers = tk.Text(self.code_frame, width=4, padx=2, takefocus=0, fg="#ffe9db",
                                     bg="#8f3901", highlightthickness=0, state=tk.DISABLED)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_input.pack(padx=10, pady=5)
        # self.code_input.configure(yscrollcommand=self.sync_scrollbars)
        # self.line_numbers.configure(yscrollcommand=self.sync_scrollbars)

       
        #image for Lexical Analyzer Button/Button
        self.analyze_button = Image.open("Images/Lexical.png")
        self.resize_analyze_button = self.analyze_button.resize((200,50))
        self.analyze_button_picture = ImageTk.PhotoImage(self.resize_analyze_button)
        self.image_analyze_button = tk.Button(image=self.analyze_button_picture, borderwidth=0, command=self.analyze_code_with_sound)
        self.image_analyze_button.place(x=300, y=850)  #x and y for lexical
        
        #image for Semantic Analyzer Button/Button
        self.semantic_button = Image.open("Images/Semantic.png")
        self.resize_semantic_button = self.semantic_button.resize((200,50))
        self.semantic_button_picture = ImageTk.PhotoImage(self.resize_semantic_button)
        self.image_semantic_button = tk.Button(image=self.semantic_button_picture, borderwidth=0, command=self.semantic_input_with_sound)
        self.image_semantic_button.place(x=300, y=780) #x and y for semantic

        #image for Syntax Button
        self.syntax_button = Image.open("Images/Syntax.png") #placeholder for syntax button
        self.resize_syntax_button = self.syntax_button.resize((200,50))
        self.syntax_button_picture = ImageTk.PhotoImage(self.resize_syntax_button)
        self.image_syntax_button = tk.Button(image=self.syntax_button_picture, borderwidth=0, command=self.syntax_analyzer_with_sound)
        self.image_syntax_button.place(x=600, y=850) #x and y for syntax button

        #image for Output Button
        self.output_code_button = Image.open("Images/Output.png") #placeholder for output button
        self.resize_output_button = self.output_code_button.resize((200,50))
        self.output_button_picture = ImageTk.PhotoImage(self.resize_output_button)
        self.image_output_button = tk.Button(image=self.output_button_picture, borderwidth=0, command=self.output_with_sound)
        self.image_output_button.place(x=600, y=780) #x and y for output button ito lang pala dear

        #image for Clear Button
        self.clear_button = Image.open("Images/Clear.png")
        self.resize_clear_button = self.clear_button.resize((40,40))
        self.clear_button_picture = ImageTk.PhotoImage(self.resize_clear_button)
        self.image_clear_button = tk.Button(image=self.clear_button_picture, borderwidth=0, command=self.clear_input_with_sound)
        self.image_clear_button.place(x=920, y=72) #may differ in 1920x1200 resolution, x and y for clear buttons

        #image for Undo Button
        self.undo_button = Image.open("Images/Undo.png")
        self.resize_undo_button = self.undo_button.resize((40,40))
        self.undo_button_picture = ImageTk.PhotoImage(self.resize_undo_button)
        self.image_undo_button = tk.Button(image=self.undo_button_picture, borderwidth=0, command=self.undo_input_with_sound)
        self.image_undo_button.place(x=967, y=72) #may differ in 1920x1200 resolution, x and y for clear buttons

        #image for Redo Button
        self.redo_button = Image.open("Images/Redo.png")
        self.resize_redo_button = self.redo_button.resize((40,40))
        self.redo_button_picture = ImageTk.PhotoImage(self.resize_redo_button)
        self.image_redo_button = tk.Button(image=self.redo_button_picture, borderwidth=0, command=self.undo_input_with_sound)
        self.image_redo_button.place(x=873, y=72) #may differ in 1920x1200 resolution, x and y for redo buttons

        #image for Import Button
        self.import_button = Image.open("Images/Import.png")
        self.resize_import_button = self.import_button.resize((40,40))
        self.import_button_picture = ImageTk.PhotoImage(self.resize_import_button)
        self.image_import_button = tk.Button(image=self.import_button_picture, borderwidth=0, command=self.import_input_with_sound)
        self.image_import_button.place(x=826, y=72) #may differ in 1920x1200 resolution, x and y for export buttons

        #image for Save Button
        self.save_button = Image.open("Images/Save.png")
        self.resize_save_button = self.save_button.resize((40,40))
        self.save_button_picture = ImageTk.PhotoImage(self.resize_save_button)
        self.image_save_button = tk.Button(image=self.save_button_picture, borderwidth=0, command=self.save_input_with_sound)
        self.image_save_button.place(x=779, y=72) #may differ in 1920x1200 resolution, x and y for save buttons

        #image for New Button
        self.new_button = Image.open("Images/New.png")
        self.resize_new_button = self.new_button.resize((40,40))
        self.new_button_picture = ImageTk.PhotoImage(self.resize_new_button)
        self.image_new_button = tk.Button(image=self.new_button_picture, borderwidth=0, command=self.new_input_with_sound)
        self.image_new_button.place(x=732, y=72) #may differ in 1920x1200 resolution, x and y for new buttons



        #Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Verdana", 14), fieldbackground="#ffe9db", rowheight=25)  # Change font for Treeview
        style.configure("Treeview.Heading", font=("Verdana", 16), background="#d88e41", foreground="#ffe9db")  # Change font for headings

        # Token Table
        self.token_frame = ctk.CTkFrame(self.root, fg_color="#8f3901", corner_radius=10)
        self.token_frame.place(x=830, y=50) #x and y for the table

        self.token_tree = ttk.Treeview(self.token_frame, columns=("Index", "Lexeme", "Token"), show='headings',
                                       height=40)
        self.token_tree.heading("Index", text="Index")
        self.token_tree.heading("Lexeme", text="Lexeme")
        self.token_tree.heading("Token", text="Token")
        self.token_tree.column("Index", width=120, anchor="center")
        self.token_tree.column("Lexeme", width=440, anchor="center")
        self.token_tree.column("Token", width=230, anchor="center")
        self.token_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Terminal Output
        self.terminal_frame = ctk.CTkFrame(self.root, width=200, height=600, fg_color="#8f3901", corner_radius=10)
        self.terminal_frame.place(x=100, y=735) #x and y for terminal
        self.terminal_output = ctk.CTkTextbox(self.terminal_frame, width=700, height=150,
                                              font=PIXEL_FONT,
                                              fg_color="#ffe9db",
                                              text_color="red",
                                              wrap="word")
        self.terminal_output.insert(tk.END, "Errors will be displayed here...\n")
        self.terminal_output.pack(padx=10, pady=2)

    def place_widgets(self):
        # Dynamically position widgets
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        self.canvas.config(width=width, height=height)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((width, height), Image.LANCZOS))
        self.canvas.itemconfig(self.bg, image=self.bg_photo)

        # Input code frame
        self.code_frame.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.5)

        # Buttons
        self.image_analyze_button.place(relx=0.05, rely=0.7, relwidth=0.1, relheight=0.05)
        self.image_clear_button.place(relx=0.17, rely=0.7, relwidth=0.1, relheight=0.05)
        self.image_undo_button.place(relx=0.29, rely=0.7, relwidth=0.1, relheight=0.05)

        # Token table
        self.token_frame.place(relx=0.5, rely=0.1, relwidth=0.45, relheight=0.5)

        # Terminal output
        self.terminal_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.15)

    def on_resize(self, event):
        self.place_widgets()

 # Sound Effects

    def analyze_code_with_sound(self):
        mixer.Sound.play(click_sound)
        self.analyze_code()

    def semantic_input_with_sound(self):
        mixer.Sound.play(click_sound)
        self.semantic_analyzer()

    def syntax_analyzer_with_sound(self):
        mixer.Sound.play(click_sound)
        self.syntax_analyzer()

    def clear_input_with_sound(self):
        mixer.Sound.play(delete_sound)
        self.clear_input()

    def undo_input_with_sound(self):
        mixer.Sound.play(delete_sound)
        self.undo_input()

    def output_with_sound(self):
        mixer.Sound.play(output_sound)
        self.output_button()
        
    def import_input_with_sound(self):
        try:
            mixer.Sound.play(click_sound)
        except Exception as e:
            print(f"Sound error: {e}")
        self.import_file()

    def save_input_with_sound(self):
        try:
            mixer.Sound.play(click_sound)
        except Exception as e:
            print(f"Sound error: {e}")
        self.save_file()

    def new_input_with_sound(self):
        try:
            mixer.Sound.play(click_sound)
            self.new_file() # Optional delay to let sound play
        except Exception as e:
            print(f"Error: {e}")

    def new_file(self):
        subprocess.Popen([sys.executable, sys.argv[0]], shell=True)
        self.destroy()

    def import_file(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.code_input.delete("1.0", tk.END)  # Clear existing content
                    self.code_input.insert(tk.END, content)  # Insert file content
                    self.update_line_numbers()  # Optional: update line numbers
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to load file:\n{e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Code As"
        )

        if file_path:
            try:
                content = self.code_input.get("1.0", tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file:\n{e}")


    def analyze_code(self): #lexer button

        # Clear previous tokens and errors
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete("1.0", tk.END)

        # Get code from input box and handle any extra newline at the end
        code = self.code_input.get("1.0", tk.END).rstrip("\n")  # Remove the trailing newline
        lines = code.splitlines()  # Split code into lines for easier indexing
        
        # Do not strip the code; keep all spaces intact
        lexer = Lexer("<input>", code)
        tokens, errors = lexer.make_tokens()

        # Configure Treeview tags row background
        self.token_tree.tag_configure("all_rows", background="#ffe9db")  # Light blue background

        # Display tokens in the treeview with row numbers
        row_number = 1
        for token in tokens:
            if isinstance(token, Token):  # Ensure it's a valid token object
                lexeme = token.value if token.value is not None else token.token
                # Check for spaces as errors
                if token.token == "SPACE":
                    self.terminal_output.insert(tk.END, f"Error: Unexpected whitespace at line {row_number}\n")
                # Check for newlines as tokens
                elif token.token == "NEWLINE":
                    lexeme = "\\n"  # Display as "\n" in the table for clarity
                row_tag = "odd_row" if row_number % 2 == 1 else "even_row"
                self.token_tree.insert("", tk.END, values=(row_number, lexeme, token.token), tags=("all_rows",))
                row_number += 1

        if errors:
            self.terminal_output.insert(tk.END, "\n".join(errors) + "\n")
        else:
            self.terminal_output.insert(tk.END, "Sucess from Lexical\n")
            
    def clear_input(self):
        """Clear the code input box"""
        self.code_input.delete("1.0", tk.END)
        
    def output_button(self): #added for the undo button feature
        input_text = self.code_input.get("1.0", "end-1c")  # Fetch input text
        list_text = input_text.split("\n")  # Split input into lines

        # Run the Lexer
        lexer = Lexer("<stdin>", input_text)
        lexer_result, lexer_errors = lexer.make_tokens()

        # Ensure that token lists do not contain nested lists
        lexer_result = [item for item in lexer_result if not (isinstance(item, list) or item.token == SPACE)]

        # Clear previous UI output
        self.terminal_output.delete("1.0", tk.END)
        self.token_tree.delete(*self.token_tree.get_children())

        # Display lexer output in the token tree view
        count = 0
        for token in lexer_result:
            if isinstance(token, Token):  # Ensure it's a valid token object
                count += 1
                lexeme = token.value if token.value is not None else token.token
                self.token_tree.insert("", tk.END, values=(count, lexeme, token.token))

        # Display Lexer Errors
        if lexer_errors:
            for err in lexer_errors:
                self.terminal_output.insert(tk.END, err + "\n")
            return  # Stop execution if lexer errors exist

        
        # Run the Parser and obtain the AST
        syntax_result, syntax_error = parser_syntax.run("<junimo code>", self.code)
        if syntax_error:
            # self.terminal_output.insert(tk.END, syntax_error.details)
            # for err in syntax_error:
            #     self.terminal_output.insert(tk.END, err.as_string())
            for err in syntax_error:
                if isinstance(err, list):
                    for e in err:
                        errorResult, fileDetail, arrowDetail, arrows = e.as_string()
                        self.terminal_output.insert(tk.END, errorResult)
                        self.terminal_output.insert(tk.END, fileDetail)
                        self.terminal_output.insert(tk.END, arrowDetail)
                        self.terminal_output.insert(tk.END, arrows)
                        # errors_text.insert(tk.END, arrows)
                else:
                    errorResult, fileDetail, arrowDetail, arrows = err.as_string()
                    self.terminal_output.insert(tk.END, errorResult)
                    self.terminal_output.insert(tk.END, fileDetail)
                    self.terminal_output.insert(tk.END, arrowDetail)
                    self.terminal_output.insert(tk.END, arrows)
                    # errors_text.insert(tk.END, arrows)
            return

        # new_parser = Parser(lexer_result)
        # ast = new_parser.parse()
        
        # # print ("AST: ", ast)
        # # Display AST in Debug Mode
        # ast.display()

        # # Prepare for Interpretation
        # interpreter = Interpreter()
        # symbol_table = SymbolTable("<Junimo Code>")  # Match program name
        # symbol_table.symbols = {}
        # ast.symbol_table = symbol_table


        # # If successful, display success message
        # self.terminal_output.insert(tk.END, "Success from Semantic\n")


        semantic_result, error = semantic.run("<stdin>", input_text)
        # print("semantic res: ", semantic_result)
        if error:
            for err in error:
                errorResult, fileDetail, arrowDetail = err.as_string()
                for e in errorResult:
                    self.terminal_output.insert(tk.END, e)
                    # print(e)

                self.terminal_output.insert(tk.END, fileDetail)
                # print(errorResult)
                # print(arrowDetail.strip())
                # print(fileDetail)
                # no_wp = arrowDetail.replace("\t", "").replace("\n", "").replace("\r", "")
                # print(no_wp)
                # print(fileDetail)
                self.terminal_output.insert(tk.END, arrowDetail)
                return
        # self.terminal_output.insert(tk.END, "Success from Semantic")
        python_file = "generated_script.py"
        transpiler_result = convert_text_file_to_python_and_execute(semantic_result, python_file)
        # return 

    def syntax_analyzer(self): # syntax button
        
        def flatten_errors(errors): # Recursive flattening of error lists, para sa mga nested lists na errors
            flat = []
            for err in errors:
                if isinstance(err, list):
                    flat.extend(flatten_errors(err))  # Recursive flatten
                elif err is not None:
                    flat.append(err)
            return flat
        # Clear previous tokens and errors
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.terminal_output.delete("1.0", tk.END)

        # Get code from input box and handle any extra newline at the end
        code = self.code_input.get("1.0", tk.END).rstrip("\n")  # Remove the trailing newline
        lines = code.splitlines()  # Split code into lines for easier indexing
        
        # Do not strip the code; keep all spaces intact
        lexer = Lexer("<input>", code)
        tokens, errors = lexer.make_tokens()

        # Configure Treeview tags row background
        self.token_tree.tag_configure("all_rows", background="#ffe9db")  # Light blue background

        # Display tokens in the treeview with row numbers
        row_number = 1
        for token in tokens:
            if isinstance(token, Token):  # Ensure it's a valid token object
                lexeme = token.value if token.value is not None else token.token
                # Check for spaces as errors
                if token.token == "SPACE":
                    self.terminal_output.insert(tk.END, f"Error: Unexpected whitespace at line {row_number}\n")
                # Check for newlines as tokens
                elif token.token == "NEWLINE":
                    lexeme = "\\n"  # Display as "\n" in the table for clarity
                row_tag = "odd_row" if row_number % 2 == 1 else "even_row"
                self.token_tree.insert("", tk.END, values=(row_number, lexeme, token.token), tags=("all_rows",))
                row_number += 1

        if errors:
            self.terminal_output.insert(tk.END, "\n".join(errors) + "\n")
        else:
            # self.terminal_output.insert(tk.END, "No errors found.\n")
            # If lexer is successful, run syntax parser
            syntax_result, syntax_error = parser_syntax.run("<junimo code>", code)
            if syntax_error:
                # self.terminal_output.insert(tk.END, syntax_error.details)
                # for err in syntax_error:
                #     self.terminal_output.insert(tk.END, err.as_string())
                for err in flatten_errors(syntax_error):
                    if isinstance(err, list):
                        for e in err:
                            errorResult, fileDetail, arrowDetail, arrows = e.as_string()
                            self.terminal_output.insert(tk.END, errorResult)
                            self.terminal_output.insert(tk.END, fileDetail)
                            self.terminal_output.insert(tk.END, arrowDetail)
                            self.terminal_output.insert(tk.END, arrows)
                            # errors_text.insert(tk.END, arrows)
                    else:
                        errorResult, fileDetail, arrowDetail, arrows = err.as_string()
                        self.terminal_output.insert(tk.END, errorResult)
                        self.terminal_output.insert(tk.END, fileDetail)
                        self.terminal_output.insert(tk.END, arrowDetail)
                        self.terminal_output.insert(tk.END, arrows)
                        # errors_text.insert(tk.END, arrows)
            else:

                # for res in syntax_result:
                self.terminal_output.insert(tk.END, "Success from Syntax")
                # errors_text.insert(tk.END, "SUCCESS")

    def semantic_analyzer(self):  # Semantic button
        input_text = self.code_input.get("1.0", "end-1c")  # Fetch input text
        list_text = input_text.split("\n")  # Split input into lines

        # Run the Lexer
        lexer = Lexer("<stdin>", input_text)
        lexer_result, lexer_errors = lexer.make_tokens()

        # Ensure that token lists do not contain nested lists
        lexer_result = [item for item in lexer_result if not (isinstance(item, list) or item.token == SPACE)]

        # Clear previous UI output
        self.terminal_output.delete("1.0", tk.END)
        self.token_tree.delete(*self.token_tree.get_children())

        # Display lexer output in the token tree view
        count = 0
        for token in lexer_result:
            if isinstance(token, Token):  # Ensure it's a valid token object
                count += 1
                lexeme = token.value if token.value is not None else token.token
                self.token_tree.insert("", tk.END, values=(count, lexeme, token.token))

        # Display Lexer Errors
        if lexer_errors:
            for err in lexer_errors:
                self.terminal_output.insert(tk.END, err + "\n")
            return  # Stop execution if lexer errors exist

        
        # Run the Parser and obtain the AST
        syntax_result, syntax_error = parser_syntax.run("<junimo code>", self.code)
        if syntax_error:
            # self.terminal_output.insert(tk.END, syntax_error.details)
            # for err in syntax_error:
            #     self.terminal_output.insert(tk.END, err.as_string())
            for err in syntax_error:
                if isinstance(err, list):
                    for e in err:
                        errorResult, fileDetail, arrowDetail, arrows = e.as_string()
                        self.terminal_output.insert(tk.END, errorResult)
                        self.terminal_output.insert(tk.END, fileDetail)
                        self.terminal_output.insert(tk.END, arrowDetail)
                        self.terminal_output.insert(tk.END, arrows)
                        # errors_text.insert(tk.END, arrows)
                else:
                    errorResult, fileDetail, arrowDetail, arrows = err.as_string()
                    self.terminal_output.insert(tk.END, errorResult)
                    self.terminal_output.insert(tk.END, fileDetail)
                    self.terminal_output.insert(tk.END, arrowDetail)
                    self.terminal_output.insert(tk.END, arrows)
                    # errors_text.insert(tk.END, arrows)
            return

        # new_parser = Parser(lexer_result)
        # ast = new_parser.parse()
        
        # # print ("AST: ", ast)
        # # Display AST in Debug Mode
        # ast.display()

        # # Prepare for Interpretation
        # interpreter = Interpreter()
        # symbol_table = SymbolTable("<Junimo Code>")  # Match program name
        # symbol_table.symbols = {}
        # ast.symbol_table = symbol_table


        # # If successful, display success message
        # self.terminal_output.insert(tk.END, "Success from Semantic\n")


        semantic_result, error = semantic.run("<stdin>", input_text)
        # print("semantic res: ", semantic_result)
        if error:
            for err in error:
                errorResult, fileDetail, arrowDetail = err.as_string()
                for e in errorResult:
                    self.terminal_output.insert(tk.END, e)
                    # print(e)

                self.terminal_output.insert(tk.END, fileDetail)
                # print(errorResult)
                # print(arrowDetail.strip())
                # print(fileDetail)
                # no_wp = arrowDetail.replace("\t", "").replace("\n", "").replace("\r", "")
                # print(no_wp)
                # print(fileDetail)
                self.terminal_output.insert(tk.END, arrowDetail)
                return
        self.terminal_output.insert(tk.END, "Success from Semantic")    
        return 
        
                # iffeed sa transpiler
    # def run_transpiler():
    #     input_text_str = input_text.get("1.0", "end-1c")
    #     list_text = input_text_str.split("\n")
    #     clear_text_file()
    #     write_list_to_file('get_line.txt', list_text)
    #     # print("list text: ", list_text)
    #     # Run lexer
    #     lexer_result, lexer_error = lexer.run("<stdin>", input_text_str)
    #     # Display lexer output
    #     output_text.delete(0, tk.END)
    #     token_text.delete(0, tk.END)
    #     count = 0
    #     for item in lexer_result:
    #         count += 1
    #         if item:
    #             output_text.insert(tk.END, "%s.\t   %s" % (count,item.value))
    #             token_text.insert(tk.END,  "%s.\t   %s" % (count,item.token))

    #     # Display lexer errors
    #     errors_text.delete(0, tk.END)
    #     # Display lexer errors if any, otherwise proceed to run the parser
    #     if lexer_error:
    #         for err in lexer_error:
    #             errors_text.insert(tk.END, err)
    #     else:
    #         # Run the parser if lexer is successful
    #         syntax_result, syntax_error = parser1.run("<junimo code>", input_text_str)
    #         if syntax_error:
    #             for err in syntax_error:
    #                 if isinstance(err, list):
    #                     for e in err:
    #                         errorResult, fileDetail, arrowDetail, arrows = e.as_string()
    #                         errors_text.insert(tk.END, errorResult)
    #                         errors_text.insert(tk.END, fileDetail)
    #                         errors_text.insert(tk.END, arrowDetail)
    #                         # errors_text.insert(tk.END, arrows)
    #                 else:
    #                     errorResult, fileDetail, arrowDetail, arrows = err.as_string()
    #                     errors_text.insert(tk.END, errorResult)
    #                     errors_text.insert(tk.END, fileDetail)
    #                     errors_text.insert(tk.END, arrowDetail)
    #                     # errors_text.insert(tk.END, arrows)
    #         else:
    #             # If no syntax errors, run the transpiler
    #             semantic_result, semantic_error = semantic.run("<stdin>", input_text_str)
    #             if semantic_error:
    #                 for err in semantic_error:
    #                     errorResult, fileDetail, arrowDetail = err.as_string()
    #                     # errors_text.insert(tk.END, errorResult)
    #                     for e in errorResult:
    #                         errors_text.insert(tk.END, e)
    #                     errors_text.insert(tk.END, fileDetail)
    #                     errors_text.insert(tk.END, arrowDetail)
    #             else:
    #                 # Transpile and execute the code
    #                 python_file = "generated_script.py"
    #                 transpiler_result = convert_text_file_to_python_and_execute(semantic_result, python_file)
    #                 # if transpiler_result:
    #                 #     errors_text.insert(tk.END, transpiler_result)
if __name__ == "__main__":
    root = ctk.CTk()
    app = StardewLexerGUI(root)
    root.mainloop()


