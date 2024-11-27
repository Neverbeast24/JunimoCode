import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

#alphabet
alpha_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyz'
all_letters = alpha + alpha_capital

#numbers
zero = '0'
number = '123456789'
all_numbers = zero + number

#alphanumeric and special symbols
punctuation_symbols = "!@#$%^&*(}-_=+[]{)\|:;',<>./?+\"" 
alpha_num = all_letters + all_numbers
ascii = all_letters + punctuation_symbols + all_numbers
ascii_string = "!@#$%^&*()-_=+[]{" + "}\|:;',<>./?+~" + all_letters + all_numbers
ascii_comment = all_letters + all_numbers + "!@#$%^&*(-_=+[]{)\|:;',<>./?+\"" 
#operators 
arithmetic_ops = "+-*/%"
relational_ops = '><==!<=>=!='
logical_ops = '||&&!'
unary_ops = '++--'
assignment_ops = '=+=-=*=/='
op_delim = logical_ops + arithmetic_ops + relational_ops
negative = '~'

#others
whitespace = " "
terminator = "$"
NEWTAB = '\\t'
NEWLINE = '\\n'
COMMA = ','
SINGLELINE = '@}'
MULTILINE_OPEN = f'@}}'
MULTILINE_CLOSE =  f'{{@'
COMMENT = "COMMENT"


dew_delim = whitespace + NEWLINE + '{'
comma_delim = whitespace + alpha_num + '"'
string1_delim = whitespace + ascii_string + NEWLINE + '"'
string2_delim = whitespace + COMMA + '+' + ')'
string_delim = string1_delim + string2_delim
delim0 = whitespace + alpha_num + negative + '(' + '['
delim1 = whitespace + alpha_num + '"' + '(' + '['+  negative
delim2 = whitespace + alpha_num + '"' + '(' + negative
delim3 = whitespace + all_numbers + '('

unary_delim = whitespace + all_letters + terminator
bool_delim = whitespace + terminator + COMMA + ')' + ']'
num_delim = arithmetic_ops + ']' + ')' + '(' + '[' + whitespace + COMMA + relational_ops + terminator
id_delim = NEWLINE + COMMA + whitespace + "=" + ")" + "[" + "]" + "<" + ">" + "!" + "(" + arithmetic_ops + terminator
spacepr_delim = whitespace + '('
break_delim = terminator + whitespace
openparenthesis_delim = whitespace + alpha_num + negative + '(' + '[' + '"' + ')'
closingparenthesis_delim = whitespace  + ')' + ']' + '{' + '&' + '|' + terminator + arithmetic_ops + relational_ops
end_delim = whitespace + NEWLINE
opensquare_delim = whitespace + all_numbers + '(' + '"' + ']'
closesquare_delim = whitespace + terminator + ')' 
negative_delim = alpha_capital + all_numbers + '('

comment1_delim = whitespace + ascii_comment
comment2_delim = whitespace + NEWLINE + ascii

#errors
error = []

#TOKENS

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

class Error: # do not change
    def __init__ (self,pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self. details = details

    def as_string(self): 
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    #the lexer comes across a character it doesn't support
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character ', details)
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance (self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
        
        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Token:
    def __init__(self, token, value=None):
        self.token = token
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.value} : {self.token}'
        return f'{self.token}'


#LEXER

class Lexer:
    
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        
    def peek(self):
        next_idx = self.pos.idx + 1
        return self.text[next_idx] if next_idx < len(self.text) else None

    def advance(self):
        self.pos.advance(self.current_char)
        # current char is the current pos if the pos is less than the length of the text
        self.current_char = self.text[self.pos.idx] if self.pos.idx <= len(self.text)-1 else None

    def make_tokens(self):
        
        tokens = []
        errors = []
        string = ""

        while self.current_char is not None:
            """ if self.current_char in special_chars:
                errors.extend([f"Invalid symbol: {self.current_char}"])
                self.advance() """
            if self.current_char in '\t':
                tokens.append(Token(NEWTAB, "\\t"))
                self.advance()
            elif self.current_char  == '\n':
                tokens.append(Token(NEWLINE, "\\n"))
                self.advance()
            elif self.current_char.isspace():
                # Handle spaces explicitly
                while self.current_char is not None and self.current_char.isspace():
                    if self.current_char == " ":
                        tokens.append(Token(SPACE, "\" \""))
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
                    tokens.append(Token(IDENTIFIER, result))
                else:
                    # If it's neither a reserved word nor a valid identifier, it's invalid
                    errors.append(f"Invalid word: '{ident}' - Not a reserved word or a valid identifier.")

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
                    errors.append(f"Invalid delimiter for {result.value}. Cause: ' {self.current_char} '.")
                else:
                    tokens.append(result)
                    
            elif self.current_char == "\"":  # Handle string literals
                string, error = self.make_string()
                errors.extend(error)
                if string:
                    tokens.append(Token(STRING, string))  # Append the full string as a token
                else:
                    # Handle unknown/invalid characters
                    errors.append(f"Unrecognized character: {self.current_char}")
                    self.advance()
            #from here to ++ 
            elif self.current_char == '=': #assignment operator (=, +=, -=, *=, /=, ==)
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '. Expected: {delim1} "])
                        continue
                    if self.current_char not in (delim1):
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '. Expected: {delim1} "])
                        continue
                    tokens.append(Token(E_EQUAL, "==")) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' = '. Cause: ' {self.current_char} '. Expected: {delim1} "])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' = '. Cause: ' {self.current_char} '. Expected: {delim1}"])
                        continue
                    tokens.append(Token(EQUAL, "=")) #for == symbol
                        
            elif self.current_char == '~':
                self.advance()
                if self.current_char is not None and self.current_char in negative_delim:
                    result, error = self.make_number()
                    result = Token(result.token, "~" + str(result.value))
                    tokens.append(result)  
                else:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '. Expected:  {number}"])
        
            elif self.current_char == '<': #relational operator
                self.advance()        
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. Expected:  {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. Expected:  {delim0} "])
                        continue
                    tokens.append(Token(LESS_THAN_EQUAL, "<=")) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' < '. Cause: ' {self.current_char} '. Expected:  {delim0} "])
                        continue
                    if self.current_char not in (delim0):
                        errors.extend([f"Invalid delimiter for ' < '. Cause: ' {self.current_char} '. Expected:  {delim0} "])
                        continue
                    tokens.append(Token(LESS_THAN, "<"))
                    
                  
            elif self.current_char == '>': 
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. {delim0} "])
                        continue
                    tokens.append(Token(GREATER_THAN_EQUAL, ">="))
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' > '. Cause: ' {self.current_char} '. {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' > '. Cause: ' {self.current_char} '. {delim0} "])
                        continue
                    tokens.append(Token(GREATER_THAN, ">"))
                    
                
            elif self.current_char == '+': #mathematical operator (+, -, *, /, %)
                self.advance()
                if self.current_char == '=': #for += symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' += '. Cause: ' {self.current_char} '. Expected:  {delim3}"])
                        continue
                    if self.current_char not in (delim3):
                        errors.extend([f"Invalid delimiter for ' += '. Cause: ' {self.current_char} '. Expected:  {delim3}"])
                        continue
                    tokens.append(Token(PLUS_EQUAL, "+=")) #for == symbol
                    
                elif self.current_char == '+': #for ++ incre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for '++'. Cause: ' {self.current_char} '. Expected: {unary_delim} "])
                        continue
                    if self.current_char not in (unary_delim):
                        errors.extend([f"Invalid delimiter for '++'. Cause: ' {self.current_char} '. Expected:  {unary_delim} "])
                        continue
                    tokens.append(Token(INCRE, "++")) #for == symbol
                else:
    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' + ' ! Cause: {self.current_char}. Expected: {delim1}"])
                        continue
                        
                    if self.current_char not in (delim1):
                        errors.extend([f"Invalid delimiter for ' + ' ! Cause: {self.current_char}. Expected: {delim1}"])
                        continue
                        
                    tokens.append(Token(PLUS, "+")) #for == symbol
                    
                        
                    
            elif self.current_char == '-': 
                self.advance()
                if self.current_char == '=': #for -=symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. Expected:  {delim3} "])
                        continue
                    if self.current_char not in delim3:
                        errors.extend([f"Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. Expected:  {delim3} "])
                        continue
                    tokens.append(Token(MINUS_EQUAL, "-=")) 
                elif self.current_char == '-': #for -- decre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. Expected: {unary_delim} "])
                        continue
                    if self.current_char not in (unary_delim):
                        errors.extend([f"Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. Expected:  {unary_delim} "])
                        continue
                    tokens.append(Token(DECRE, "--")) 
                
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} ' Expected:  {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} ' Expected:  {delim0} "])
                        continue
                    tokens.append(Token(MINUS, "-")) 
                
            elif self.current_char == '*': 
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. Expected:  {delim3} "])
                    if self.current_char not in delim3:
                        errors.extend([f"Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. Expected:  {delim3} "])
                        continue
                    tokens.append(Token(MUL_EQUAL, "*=")) 
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' * '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' * '. Cause: ' {self.current_char} ' Expected:  {delim0} "])
                        continue
                    tokens.append(Token(MUL, "*"))    
                        
                
                
            elif self.current_char == '/': 
                self.advance()
                if self.current_char == '=': #for /= symbol
                    
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. Expected:  {delim3} "])
                        continue
                    if self.current_char not in delim3:
                        errors.extend([f"Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. Expected:  {delim3} "])
                        continue
                    tokens.append(Token(DIV_EQUAL, "/="))
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' / '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' / '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    tokens.append(Token(DIV, "/"))
                
            elif self.current_char == '%':
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' % '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                    continue
                if self.current_char not in delim0:

                    errors.extend([f"Invalid delimiter for ' % '. Cause: ' {self.current_char} '. Expected: {delim0} "])

                    
                    continue
                tokens.append(Token(MODULUS, "%"))
                
            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == '=':  
                    self.advance()
                    pos_start = self.pos.copy()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' != '. Cause: ' {self.current_char} '. Expected: {delim2} "])
                        continue
                    if self.current_char not in delim2:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!=' )])
                        errors.extend([f"Invalid delimiter for ' != '. Cause: ' {self.current_char} '. Expected: {delim2} "])

                        continue
                    print("appending !=: ", self.current_char)

                    tokens.append(Token(NOT_EQUAL, "!=")) #for != symbol
                else:
                    if self.current_char == None:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    tokens.append(Token(NOT_OP, "!"))
                    
            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' && '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' && '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    tokens.append(Token(AND_OP, "&&"))
                    
                else:
                    errors.extend([f"Please enter a valid symbol! User typed: & .Did you mean && ?"])
                    #self.advance()
            elif self.current_char == '|': #return error
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' || '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Invalid delimiter for ' || '. Cause: ' {self.current_char} '. Expected: {delim0} "])
                        continue
                    tokens.append(Token(OR_OP, "||"))
                else:
                    errors.extend([f"Please enter a valid symbol! User typed: & .Did you mean && ?"])
                    
            elif self.current_char == '"': #string 1 and string 2 delim conflict # added str1 and 2 = string_delim
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' \" '. Cause: ' {self.current_char} '. Expected: {string_delim} "])
                    continue
                if self.current_char not in string_delim:
                    errors.extend([f"Invalid delimiter for ' \" '. Cause: ' {self.current_char} '. Expected: {string_delim} "])
                    continue
                tokens.append(Token(STRING, "\" \""))
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

                                # Add tokens for a valid multi-line comment
                                tokens.append(Token(MULTILINE_OPEN, "@}}"))
                                tokens.append(Token(COMMENT, comment_content.strip()))
                                tokens.append(Token(MULTILINE_CLOSE, "{{@"))
                                break

                            # Append the current character to the comment content
                            if not (self.current_char.isascii() or self.current_char in comment2_delim):
                                errors.append(
                                    f"Invalid character '{self.current_char}' in multi-line comment. Expected only ASCII or {comment2_delim}."
                                )

                            comment_content += self.current_char
                            self.advance()

                        # If loop ends without finding {{@, report an error
                        else:
                            errors.append(f"Unclosed multi-line comment. Expected '{{@' to close.")
                            errors.append(f"Invalid Delimiter for Single-line Comment. Expected: {comment1_delim}")
                            # Do not add tokens for incomplete or invalid multi-line comments
                            return tokens, errors  # Exit after reporting the errors

                    else:  # Single-line comment
                        comment_content = ""

                        # Capture the content for the single-line comment
                        while self.current_char is not None and self.current_char != "\n":  # Stop at newline or EOF
                            # Validate the character
                            if not (self.current_char.isascii() or self.current_char in comment1_delim):
                                errors.append(
                                    f"Invalid character '{self.current_char}' in single-line comment. "
                                    f"Expected only ASCII or {comment1_delim}."
                                )

                            comment_content += self.current_char
                            self.advance()

                        # If there are errors in the single-line comment, do not add it to the tokens
                        if errors:
                            continue

                        # Add tokens for single-line comment
                        tokens.append(Token(SINGLELINE, "@}"))
                        tokens.append(Token(COMMENT, comment_content.strip()))
                        
                        # Continue parsing other tokens after the single-line comment ends
                        continue

                # Handle invalid `@` usage
                else:
                    errors.append(f"Invalid use of '@'. Cause: '{self.current_char}'. Expected: '}}' for multi-line comment start or '@}}'.")
                    continue

            elif self.current_char == '(': #other operator
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: {openparenthesis_delim} "])
                    continue
                if self.current_char not in openparenthesis_delim:
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: {openparenthesis_delim}"])
                    continue
                tokens.append(Token(LPAREN, "("))
            elif self.current_char == ')':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ) '. Cause: ' {self.current_char} '. Expected: {closingparenthesis_delim} "])
                    continue
                if self.current_char not in closingparenthesis_delim:
                    errors.extend([f"Invalid delimiter for ' ) '. Cause: ' {self.current_char} '. Expected: {closingparenthesis_delim} "])
                    continue
                tokens.append(Token(RPAREN, ")"))
            elif self.current_char == '[':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. Expected: {opensquare_delim} "])
                    continue
                if self.current_char not in opensquare_delim:
                    errors.extend([f"Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. Expected: {opensquare_delim} "])
                    continue
                tokens.append(Token(SLBRACKET, "["))
            elif self.current_char == ']':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. Expected: {closesquare_delim} "])
                    continue
                if self.current_char not in closesquare_delim:
                    errors.extend([f"Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. Expected: {closesquare_delim} "])
                    continue
                tokens.append(Token(SRBRACKET, "]"))
            elif self.current_char == '{':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. Expected: space or newline "])
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. Expected: space or newline "])
                    continue
                tokens.append(Token(CLBRACKET, "{"))
            elif self.current_char == '}':
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(CRBRACKET, "}"))
                    errors.extend([f"Invalid delimiter for 'curly curly bracket'. Cause: ' {self.current_char} '. Expected: space or newline "])
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Invalid delimiter for 'closing curly bracket'. Cause: ' {self.current_char} '. Expected: space or newline "])
                    continue
                tokens.append(Token(CRBRACKET, "}"))
            
            elif self.current_char == "\"":
                string, error = self.make_string()
                tokens.append(Token(STRING, f"{string}"))
                self.advance()
                
                errors.extend(error)
            elif self.current_char == ',':
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' , '. Cause: ' {self.current_char} '. Expected: {comma_delim} "])
                    continue
                if self.current_char not in comma_delim:
                    errors.extend([f"Invalid delimiter for ' , '. Cause: ' {self.current_char} '. Expected: {comma_delim} "])
                    continue
                tokens.append(Token(COMMA, ","))
                
            elif self.current_char == "$":
                
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(terminator, "$"))
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Invalid delimiter for ' $ '. Cause: ' {self.current_char} '. Expected: space or newline "])
                    continue
                tokens.append(Token(terminator, "$"))
            else:
                errors.append(f"Illegal character: {self.current_char}")
                self.advance()
                
        tokens.append(Token(EOF, "EOF"))
        return tokens, errors       

    def make_number(self):
        dec_count = 0
        num_count = 0
        num_str = ''
        dot_count = 0
        errors = []

        while self.current_char is not None and self.current_char in all_numbers + '.':
            if self.current_char == '.':
                if dot_count == 1: 
                    errors.append(f"Invalid character '{self.current_char}' in number. Decimal point already found!")
                    break 
                dot_count += 1 
                num_str += '.'
            else:                
                num_count += 1
                num_str += self.current_char
            self.advance()

        # Check if there are letters after the number
        if self.current_char is not None and self.current_char.isalpha():
            errors.append(f"Invalid delimiter for number: {num_str}")    
            if errors:
                return [], errors
        
        # Validate the next character using `num_delim`
        if self.current_char is not None and self.current_char not in num_delim:
            errors.append(
                f"Invalid delimiter '{self.current_char}' after number '{num_str}'. "
                f"Expected one of: {num_delim}"
            )
            if errors:
                return [], errors

        # Determine if the token is an integer or a float
        if dot_count == 0:
            return Token(INTEGER, int(num_str)), errors
        else:
            return Token(FLOAT, float(num_str)), errors

       
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
                    ident_count += 1
                    if self.current_char == "d":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Invalid delimiter for add! Cause: {self.current_char}. Expected: ('])
                                return [], errors
                            if self.current_char in '(':
                                return Token(ADD, "add"), errors
                            elif self.current_char in alpha_num: #double check this
                                continue
                            else:
                                errors.extend([f'Invalid delimiter for add! Cause: {self.current_char}. Expected: ('])
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
                                    errors.extend([f'Invalid delimiter for break! Cause: {self.current_char} Expected: {break_delim}'])
                                    return [], errors
                                if self.current_char in break_delim: #double check this
                                    return Token(BREAK, "break"), errors
                                elif self.current_char in break_delim:
                                    continue
                                else:
                                    errors.extend([f'Invalid delimiter for break! Cause: {self.current_char} Expected: {break_delim}'])
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
                                        errors.extend([f'Invalid delimiter for collect! Cause: {self.current_char} Expected: ('])
                                        return [], errors
                                    if self.current_char in '(':
                                        return Token(COLLECT, "collect"), errors
                                    elif self.current_char in alpha_num: #double check this 
                                        continue
                                    else:
                                        errors.extend([f'Invalid delimiter for collect! Cause: {self.current_char} Expected: ('])
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
                            errors.extend([f'Invalid delimiter for craft! Cause: {self.current_char}. Expected: space " " '])
                            return [], errors
                        if self.current_char in whitespace or self.current_char.isspace():
                            return Token(CRAFT, "craft"), errors
                        elif self.current_char in alpha_num:
                            continue
                        else:
                            errors.extend([f'Invalid delimiter for craft! Cause: {self.current_char}. Expected: space " " '])
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
                                errors.extend([f'Invalid delimiter for crop! Cause: {self.current_char}. Expected: space " " '])
                                return [], errors
                            if self.current_char in whitespace or self.current_char.isspace():
                                return Token(CROP, "crop"), errors
                            elif self.current_char in alpha_num: #double check this
                                continue
                            else:
                                errors.extend([f'Invalid delimiter for crop! Cause: {self.current_char}. Expected: space " " '])
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
                            errors.extend([f'Invalid delimiter for dew! Cause: {self.current_char} Expected: {dew_delim}']) 
                            return [], errors
                        if self.current_char in dew_delim:
                            return Token(DEW, "dew"), errors
                        elif self.current_char in alpha_num: #double check this 
                            continue
                        else:
                            errors.extend([f'Invalid delimiter for dew! Cause: {self.current_char} Expected: {dew_delim}'])
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
                                    errors.extend([f'Invalid delimiter for false! Cause: {self.current_char}. Expected: {dew_delim} '])
                                    return [], errors
                                if self.current_char in bool_delim:
                                    return Token(FALSE, "false"), errors
                                elif self.current_char in alpha_num:
                                    continue
                                else:
                                    errors.extend([f'Invalid delimiter for false! Cause: {self.current_char}. Expected: {dew_delim} '])
                                    return [], errors
                        
                        elif self.current_char == "l": #FOR = FALL
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Invalid delimiter for fall! Cause: {self.current_char}. Expected: {spacepr_delim}'])
                                return [], errors
                            if self.current_char in spacepr_delim:
                                return Token(FALL, "fall"), errors
                            elif self.current_char in alpha_num:
                                continue
                            else:
                                errors.extend([f'Invalid delimiter for fall! Cause: {self.current_char}. Expected: {spacepr_delim}'])
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
                                                    errors.extend([f'Invalid delimiter for farmhouse! Cause: {self.current_char}. Expected: space " " '])
                                                    return [], errors
                                                if self.current_char in whitespace or self.current_char.isspace():                                               
                                                    return Token(FARMHOUSE, "farmhouse"), errors
                                                elif self.current_char in alpha_num:
                                                    continue
                                                else:
                                                    errors.extend([f'Invalid delimiter for farmhouse! Cause: {self.current_char}. Expected: space " " '])
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
                                            errors.extend([f'Invalid delimiter for harvest! Cause: {self.current_char}. Expected: {spacepr_delim + terminator}'])                                        
                                            return [], errors
                                        if self.current_char  in spacepr_delim + terminator:
                                            return Token(HARVEST, "harvest"), errors
                                        elif self.current_char in alpha_num:
                                            continue
                                        else:
                                            errors.extend([f'Invalid delimiter for harvest! Cause: {self.current_char}. Expected: {spacepr_delim + terminator}'])                                        
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
                                            errors.extend([f'Invalid delimiter for pelican! Cause: {self.current_char}. Expected: ( '])
                                            return [], errors
                                        if self.current_char in '(':
                                            return Token(PELICAN, "pelican"), errors 
                                        elif self.current_char in alpha_num:
                                            continue 
                                        else:                  
                                            errors.extend([f'Invalid delimiter for pelican! Cause: {self.current_char}. Expected: ( '])
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
                                                        errors.extend([f'Invalid delimiter for perfection! Cause: {self.current_char}. Expected: {break_delim}'])
                                                        return [], errors
                                                    if self.current_char in break_delim:
                                                        return Token(PERFECTION, "perfection"), errors
                                                    elif self.current_char in alpha_num:
                                                        continue
                                                    else:
                                                        errors.extend([f'Invalid delimiter for perfection! Cause: {self.current_char}. Expected: {break_delim}'])
                                                        return [], errors
                        
                elif self.current_char == "l": #PLANTING
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
                                                errors.extend([f'Invalid delimiter for planting! Cause: {self.current_char}. Expected: {break_delim} '])
                                                return [], errors
                                            if self.current_char in break_delim:
                                                return Token(PLANTING, "planting"), errors
                                            elif self.current_char in alpha_num:
                                                continue
                                            else:
                                                errors.extend([f'Invalid delimiter for planting! Cause: {self.current_char}. Expected: {break_delim} '])
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
                                    errors.extend([f'Invalid delimiter for pluck! Cause: {self.current_char}. Expected: ('])
                                    return [], errors
                                if self.current_char in '(':
                                    return Token(PLUCK, "pluck"), errors
                                elif self.current_char in alpha_num:
                                    continue
                                else:
                                    errors.extend([f'Invalid delimiter for pluck! Cause: {self.current_char}. Expected: ('])
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
                                errors.extend([f'Invalid delimiter for ship! Cause: {self.current_char}. Expected: ('])
                                return [], errors
                            if self.current_char in '(':
                                return Token(SHIP, "ship"), errors
                            elif self.current_char in alpha_num:
                                continue
                            else:
                                errors.extend([f'Invalid delimiter for ship! Cause: {self.current_char}. Expected: ('])
                                
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
                                errors.extend([f'Invalid delimiter for star! Cause: {self.current_char}. Expected: space or ('])
                                return [], errors
                            if self.current_char in spacepr_delim:
                                return Token(STAR, "star"), errors
                            elif self.current_char in alpha_num:
                                continue
                            elif self.current_char == "d": #inde ko ma-gets paano mapasok tong stardew sa star
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
                                            errors.extend([f'Invalid delimiter for stardew! Cause: {self.current_char}. Expected: {spacepr_delim} '])
                                            return [], errors
                                        if self.current_char in spacepr_delim:
                                            return Token(STARDEW, "stardew"), errors
                                        elif self.current_char in alpha_num:
                                            continue
                                        else:
                                            errors.extend([f'Invalid delimiter for stardew! Cause: {self.current_char}. Expected: {spacepr_delim}'])
                                            return [], errors
                            else:
                                errors.extend([f'Invalid delimiter for star! Cause: {self.current_char}. Expected: space or ('])
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
                                errors.extend([f'Invalid delimiter for true! Cause: {self.current_char}. Expected: {bool_delim} '])
                                return [], errors
                            if self.current_char in bool_delim:
                                return Token(TRUE, "true"), errors
                            elif self.current_char in alpha_num:
                                continue
                            else:
                                errors.extend([f'Invalid delimiter for true! Cause: {self.current_char}. Expected: {bool_delim} '])
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
                                            errors.extend([f'Invalid delimiter for voidegg! Cause: {self.current_char}. Expected: {bool_delim} '])
                                            return [], errors
                                        if self.current_char in bool_delim:
                                            return Token(VOIDEGG, "voidegg"), errors
                                        elif self.current_char in alpha_num:
                                            continue
                                        else:
                                            errors.extend([f'Invalid delimiter for voidegg! Cause: {self.current_char}. Expected: {bool_delim}'])
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
                                        errors.extend([f'Invalid delimiter for winter! Cause: {self.current_char}. Expected: {spacepr_delim}'])
                                        return [], errors
                                    if self.current_char in spacepr_delim:
                                        return Token(WINTER, "winter"), errors
                                    elif self.current_char in alpha_num:
                                        continue
                                    else:
                                        errors.extend([f'Invalid delimiter for winter! Cause: {self.current_char}. Expected: {spacepr_delim}'])
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
                    return Token(IDENTIFIER, result), errors
                break

            # Handle the final case where identifier is completed
            if ident:
                print("IF IDENT!")
                result, error = self.make_ident(ident)
                if error:
                    errors.append(error)
                    return [], errors
                elif result:
                    return Token(IDENTIFIER, result), errors

            if not ident:
                errors.extend("Identifier is empty or invalid.")
            return Token(IDENTIFIER, ident), errors

    def make_ident(self, ident):
        """
        Validates whether the given word is a valid identifier or reserved word.
        """
        errors = []

        # Ensure the first letter is uppercase
        if not ident[0].isupper():
            print(f"NASA LOOB NG MAKE IDENT YUNG ERROR: {self.current_char}")
            return None, f"Lexical error: Invalid identifier start: '{ident[0]}'. Word '{ident}' must start with an uppercase letter."

        # Ensure no invalid characters are present
        if not all(c.isalnum() or c == "_" for c in ident):
            return None, f"Lexical error: Invalid character in word '{ident}'. Identifiers must be alphanumeric or underscores."

        # Ensure the next character is a valid delimiter
        if self.current_char is not None and self.current_char not in id_delim:
            return None, f"Lexical error: Invalid delimiter after word '{ident}'. Found: '{self.current_char}. Expected: {id_delim}."

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
            errors.append("Expected closing quotation mark!")
            return string, errors

def run(fn, text):

    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error

class LexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Junimo Code Lexer")
        
        # Setup GUI layout
        self.setup_widgets()
        
    def setup_widgets(self):
        # Input box for code
        self.code_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=15)
        self.code_input.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Analyze Button
        self.analyze_button = tk.Button(self.root, text="Analyze Code", command=self.analyze_code)
        self.analyze_button.grid(row=1, column=0, padx=10, pady=10)

        # Treeview for tokens and lexemes (with row numbering)
        self.token_tree = ttk.Treeview(self.root, columns=("Row", "Lexeme", "Token"), show='headings')
        self.token_tree.heading("Row")
        self.token_tree.heading("Lexeme", text="Lexeme")
        self.token_tree.heading("Token", text="Token")
        self.token_tree.column("Row", width=50, anchor="center")  # Set column width for row numbers
        self.token_tree.column("Lexeme", width=200)
        self.token_tree.column("Token", width=200)
        self.token_tree.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # Error display
        self.error_output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=5, fg="red")
        self.error_output.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.error_output.insert(tk.END, "Errors will be displayed here...\n")
        self.error_output.config(state=tk.DISABLED)

    def analyze_code(self):
        # Clear previous tokens and errors
        for row in self.token_tree.get_children():
            self.token_tree.delete(row)
        self.error_output.config(state=tk.NORMAL)
        self.error_output.delete("1.0", tk.END)

        # Get code from input box
        code = self.code_input.get("1.0", tk.END)

        # Do not strip the code; keep all spaces intact
        lexer = Lexer("<input>", code)
        tokens, errors = lexer.make_tokens()

        # Display tokens in the treeview with row numbers
        row_number = 1
        for token in tokens:
            if isinstance(token, Token):  # Ensure it's a valid token object
                lexeme = token.value if token.value is not None else token.token
                self.token_tree.insert("", tk.END, values=(row_number, lexeme, token.token))
                row_number += 1

        # Display errors
        if errors:
            self.error_output.insert(tk.END, "\n".join(errors) + "\n")
        else:
            self.error_output.insert(tk.END, "No errors found.\n")

        self.error_output.config(state=tk.DISABLED)


# Example usage with GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = LexerGUI(root)
    root.mainloop()

    
# Completed the lexer