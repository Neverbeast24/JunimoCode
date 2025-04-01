import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
import tkinter as tk
from itertools import count
from ctypes import windll
from strings_arrows import *

# Register custom fonts
windll.gdi32.AddFontResourceW("Fonts\Stardew-Valley-Regular.ttf")
windll.gdi32.AddFontResourceW("Fonts\StardewValley.ttf")

# Initialize sound library
mixer.init()

# Load sound effects
click_sound = mixer.Sound("Interface/bigSelect.wav")
hover_sound = mixer.Sound("Interface/select.wav")
background_music = r"BackgroundMusic/ConcernedApe - Stardew Valley OST - 01 Stardew Valley Overture.mp3"
# background_music = r"Ambience\fall_day.wav"
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

#alphabet
alpha_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyz'
all_letters = alpha + alpha_capital

#numbers
zero = '0'
number = '123456789'
all_numbers = zero + number

#alphanumeric and special symbols
punctuation_symbols = "~!@#$%^&*(}-_=+[]{)\|:;',<>./?+\""
alpha_num = all_letters + all_numbers 
ascii = all_letters + punctuation_symbols + all_numbers
ascii_string = "!@#$%^&*()-_=+[]{" + "}\|:;',<>./?+~" + all_letters + all_numbers
ascii_comment = all_letters + all_numbers + "~!@#$%^&*(-_=+[]{)\|:;',<>./?+\""
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
openparenthesis_delim = whitespace + alpha_num + negative + '('  + '"' + ')' + newline_delim + '!' + '+' + '-' ','
closingparenthesis_delim = whitespace  + ')' + '{' + '&' + '|' + TERMINATOR + arithmetic_ops + relational_ops + ','
end_delim = whitespace + newline_delim
opensquare_delim = whitespace + all_numbers + '"' + ']' + alpha_capital
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
ARITH_OP = [PLUS, MINUS, MUL, DIV, MODULUS]

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
        result  = f'{self.error_name}: {self.details}\n'
        fileDetail = f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        errorDetail, arrowDetail = string_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result, fileDetail, errorDetail, arrowDetail
        # return (
        #     f"Invalid Syntax: {self.details}\n"
        #     f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}\n"
        #     f"{self.pos_start.ftxt}\n"
        #     f"{' ' * (self.pos_start.col)}^"
        # )

class IllegalCharError(Error):
    #the lexer comes across a character it doesn't support
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character ', details)

class DelimiterError(Error):
    def __init__(self,pos_start, pos_end, details, char):
        super().__init__(pos_start, pos_end, f"Invalid Delimiter for '{char}'", "Cause -> " + str(details))
        
class InvalidSyntaxError(Error):
    def __init__(self,pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance (self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Token:
    def __init__(self, token, value=None, pos_start=None, pos_end=None):
        self.token = token
        self.value = value
    
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end
    
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
                    errors.append(f"Error at line: {self.pos.ln + 1}. Invalid word: '{ident}' - Not a reserved word or a valid identifier.")

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
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' == '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", (, ["])
                        continue
                    if self.current_char not in (delim1):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' == '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", (, ["])
                        continue
                    tokens.append(Token(E_EQUAL, "==", pos_start = self.pos)) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' = '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", (, ["])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' = '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", (, ["])
                        continue
                    tokens.append(Token(EQUAL, "=", pos_start = self.pos)) #for == symbol

            elif self.current_char == '~':
                self.advance()
                if self.current_char in all_numbers:
                    result, error = self.make_number()
                    result = Token(result.token, "~" + str(result.value), pos_start = self.pos)
                    tokens.append(result)  
                else:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '. Expected:  123456789"])
                    
            elif self.current_char == '<': #relational operator
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(LESS_THAN_EQUAL, "<=", pos_start = self.pos)) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' < '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in (delim0):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' < '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(LESS_THAN, "<", pos_start = self.pos))


            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(GREATER_THAN_EQUAL, ">=", pos_start = self.pos))
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' > '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' > '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(GREATER_THAN, ">", pos_start = self.pos))


            elif self.current_char == '+': #mathematical operator (+, -, *, /, %)
                self.advance()
                if self.current_char == '=': #for += symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' += '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    if self.current_char not in (delim3):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' += '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    tokens.append(Token(PLUS_EQUAL, "+=", pos_start = self.pos)) #for == symbol

                elif self.current_char == '+': #for ++ incre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ++ '. Cause: ' {self.current_char} '. Expected: whitespace, all letters, terminator, ) "])
                        continue
                    if self.current_char not in (unary_delim) or self.current_char.isspace():
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ++ '. Cause: ' {self.current_char} '. Expected: whitespace, all letters, terminator, ) "])
                        continue
                    tokens.append(Token(INCRE, "++", pos_start = self.pos)) #for == symbol
                else:

                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' + '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", (, ["])
                        continue

                    if self.current_char not in (delim1):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' + '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", (, ["])
                        continue

                    tokens.append(Token(PLUS, "+", pos_start = self.pos)) #for == symbol



            elif self.current_char == '-':
                self.advance()
                if self.current_char == '=': #for -=symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    if self.current_char not in delim3:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    tokens.append(Token(MINUS_EQUAL, "-=", pos_start = self.pos))
                elif self.current_char == '-': #for -- decre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. Expected: whitespace, all letters, TERMINATOR, ) "])
                        continue
                    if self.current_char not in (unary_delim):
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. Expected: whitespace, all letters, TERMINATOR, ) "])
                        continue
                    tokens.append(Token(DECRE, "--", pos_start = self.pos))

                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' - '. Cause: ' {self.current_char} ' . Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' - '. Cause: ' {self.current_char} ' . Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(MINUS, "-", pos_start = self.pos))

            elif self.current_char == '*':
                self.advance()
                if self.current_char == "=":
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                    if self.current_char not in delim3:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    tokens.append(Token(MUL_EQUAL, "*=", pos_start = self.pos))
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' * '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' * '. Cause: ' {self.current_char} ' . Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(MUL, "*", pos_start = self.pos))



            elif self.current_char == '/':
                self.advance()
                if self.current_char == '=': #for /= symbol

                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    if self.current_char not in delim3:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, ( "])
                        continue
                    tokens.append(Token(DIV_EQUAL, "/=", pos_start = self.pos))
                else:
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' / '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' / '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(DIV, "/", pos_start = self.pos))

            elif self.current_char == '%':
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' % '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                    continue
                if self.current_char not in delim0:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' % '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                    continue
                tokens.append(Token(MODULUS, "%", pos_start = self.pos))

            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == '=':
                    self.advance()
                    pos_start = self.pos.copy()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' != '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", ( "])
                        continue
                    if self.current_char not in delim2:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!=' )])
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' != '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, \", ( "])
                        continue
                    print("appending !=: ", self.current_char)
                    tokens.append(Token(NOT_EQUAL, "!=", pos_start = self.pos)) #for != symbol
                else:
                    if self.current_char == None:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. Expected: ( "])
                        continue
                    if self.current_char not in "(":
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. Expected: ( "])
                        continue
                    tokens.append(Token(NOT_OP, "!", pos_start = self.pos))

            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' && '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' && '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
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
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' || '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    if self.current_char not in delim0:
                        errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' || '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative operator, (, [ "])
                        continue
                    tokens.append(Token(OR_OP, "||", pos_start = self.pos))
                else:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Please enter a valid symbol! User typed: & .Did you mean && ?"])

            elif self.current_char == '"': #string 1 and string 2 delim conflict # added str1 and 2 = string_delim
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' \" '. Cause: ' {self.current_char} '. Expected: whitespace, comma, +, ), alphanumeric, negative operator, (, [ "])
                    continue
                if self.current_char not in string_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' \" '. Cause: ' {self.current_char} '. Expected: whitespace, comma, +, ), alphanumeric, negative operator, (, [ "])
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
                                    f"Error at line: {self.pos.ln + 1}. Invalid character '{self.current_char}' in multi-line comment. Expected only ASCII or {comment2_delim}."
                                )

                            comment_content += self.current_char
                            self.advance()

                        # If loop ends without finding {{@, report an error
                        else:
                            errors.append(f"Error at line: {self.pos.ln + 1}. Unclosed multi-line comment. Expected '{{@' to close.")
                            errors.append(f"Error at line: {self.pos.ln + 1}. Invalid Delimiter for Single-line Comment. Expected: {comment1_delim}")
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
                                    f"Error at line: {self.pos.ln + 1}. Expected only ASCII or {comment1_delim}."
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
                    errors.append(f"Error at line: {self.pos.ln + 1}. Invalid use of '@'. Cause: '{self.current_char}'. Expected: '}}' for multi-line comment start or '@}}'.")
                    continue

            elif self.current_char == '(': #other operator
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative, (,), quotation mark "])
                    continue
                if self.current_char not in openparenthesis_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, negative, (,), quotation mark"])
                    continue
                tokens.append(Token(LPAREN, "(", pos_start = self.pos))
            elif self.current_char == ')':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ) '. Cause: ' {self.current_char} '. Expected: whitespace, ')', open curly bracket, '&', '|', dollar sign, arithmetic operators, relational operators "])
                    continue
                if self.current_char not in closingparenthesis_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ) '. Cause: ' {self.current_char} '. Expected: whitespace, ')', open curly bracket, '&', '|', dollar sign, arithmetic operators, relational operators "])
                    continue
                tokens.append(Token(RPAREN, ")", pos_start = self.pos))
            elif self.current_char == '[':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, quotation mark, close square bracket"])
                    continue
                if self.current_char not in opensquare_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. Expected: whitespace, all numbers, quotation mark, close square bracket"])
                    continue
                tokens.append(Token(SLBRACKET, "[", pos_start = self.pos))
            elif self.current_char == ']':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. Expected: dollar sign, whitespace, close parenthesis"])
                    continue
                if self.current_char not in closesquare_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. Expected: dollar sign, whitespace, close parenthesis "])
                    continue
                tokens.append(Token(SRBRACKET, "]", pos_start = self.pos))
            # Handling '{' (opening curly bracket)
            elif self.current_char == '{':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. Expected: \' \', alphanumeric characters or newline "])
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. Expected: \' \', alphanumeric characters or newline "])
                    continue
                tokens.append(Token(CLBRACKET, "{", pos_start = self.pos))
            elif self.current_char == '}':
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(CRBRACKET, "}", pos_start = self.pos))
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for 'closing curly bracket'. Cause: ' {self.current_char} '. Expected: \' \', alphanumeric characters or newline "])
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
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' , '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, quotation mark "])
                    continue
                if self.current_char not in comma_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' , '. Cause: ' {self.current_char} '. Expected: whitespace, alphanumeric, quotation mark "])
                    continue
                tokens.append(Token(COMMA, ",", pos_start = self.pos))

            elif self.current_char == "$":

                self.advance()
                if self.current_char == None:
                    tokens.append(Token(TERMINATOR, "$", pos_start = self.pos))
                    continue
                if self.current_char not in end_delim:
                    errors.extend([f"Error at line: {self.pos.ln + 1}. Invalid delimiter for ' $ '. Cause: ' {self.current_char} '. Expected: space or newline "])
                    continue
                tokens.append(Token(TERMINATOR, "$", pos_start = self.pos))
            else:
                errors.append(f"Error at line: {self.pos.ln + 1}. Illegal character: {self.current_char}")
                self.advance()

        tokens.append(Token(EOF, "EOF", pos_start = self.pos))
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
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for add! Cause: {self.current_char}. Expected: open parenthesis'])
                                return [], errors
                            if self.current_char in '(':
                                return Token(ADD, "add", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num: #double check this
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for add! Cause: {self.current_char}. Expected: open parenthesis'])
                                self.advance()
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
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for break! Cause: {self.current_char} Expected: dollar sign, whitespace'])
                                    return [], errors
                                if self.current_char in break_delim: #double check this
                                    return Token(BREAK, "break", pos_start = self.pos), errors
                                # elif self.current_char in break_delim:
                                #     continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for break! Cause: {self.current_char} Expected: dollar sign, whitespace'])
                                    self.advance()
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
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for collect! Cause: {self.current_char} Expected: open parenthesis'])
                                        return [], errors
                                    if self.current_char in '(':
                                        return Token(COLLECT, "collect", pos_start = self.pos), errors
                                    # elif self.current_char in alpha_num: #double check this
                                    #     continue
                                    else:
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for collect! Cause: {self.current_char} Expected: open parenthesis'])
                                        self.advance()
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
                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for craft! Cause: {self.current_char}. Expected: space " " '])
                            return [], errors
                        if self.current_char in spacepr_delim or self.current_char.isspace():
                            return Token(CRAFT, "craft", pos_start = self.pos), errors
                        # elif self.current_char in alpha_num:
                        #     continue
                        else:
                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for craft! Cause: {self.current_char}. Expected: space " " '])
                            self.advance()
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
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for crop! Cause: {self.current_char}. Expected: space " " '])
                                return [], errors
                            if self.current_char in whitespace or self.current_char.isspace():
                                return Token(CROP, "crop", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num: #double check this
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for crop! Cause: {self.current_char}. Expected: space " " '])
                                self.advance()
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
                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for dew! Cause: {self.current_char} Expected: whitespace, newline, open curly bracket '])
                            return [], errors
                        if self.current_char in dew_delim:
                            return Token(DEW, "dew", pos_start = self.pos), errors
                        # elif self.current_char in alpha_num: #double check this
                        #     continue
                        else:
                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for dew! Cause: {self.current_char} Expected: whitespace, newline, open curly bracket '])
                            self.advance()
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
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for false! Cause: {self.current_char}. Expected: whitespace, newline, open curly bracket  '])
                                    return [], errors
                                if self.current_char in bool_delim:
                                    return Token(FALSE, "false", pos_start = self.pos), errors
                                # elif self.current_char in alpha_num:
                                #     continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for false! Cause: {self.current_char}. Expected: whitespace, newline, open curly bracket  '])
                                    self.advance()
                                    return [], errors

                        elif self.current_char == "l": #FOR = FALL
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for fall! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                return [], errors
                            if self.current_char in spacepr_delim:
                                return Token(FALL, "fall", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for fall! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                self.advance()
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
                                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for farmhouse! Cause: {self.current_char}. Expected: whitespace '])
                                                    return [], errors
                                                if self.current_char in whitespace or self.current_char.isspace():
                                                    return Token(FARMHOUSE, "farmhouse", pos_start = self.pos), errors
                                                # elif self.current_char in alpha_num:
                                                #     continue
                                                else:
                                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for farmhouse! Cause: {self.current_char}. Expected: whitespace '])
                                                    self.advance()
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
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for harvest! Cause: {self.current_char}. Expected: whitespace, open parenthesis, dollar sign'])
                                            return [], errors
                                        if self.current_char  in spacepr_delim + TERMINATOR:
                                            return Token(HARVEST, "harvest", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for harvest! Cause: {self.current_char}. Expected: whitespace, open parenthesis, dollar sign'])
                                            self.advance()
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
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for next! Cause: {self.current_char}. Expected: whitespace or dollar sign '])
                                return [], errors
                            if self.current_char in break_delim:
                                return Token(NEXT, "next", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pelican! Cause: {self.current_char}. Expected: open parenthesis '])
                                self.advance()
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
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pelican! Cause: {self.current_char}. Expected: open parenthesis '])
                                            return [], errors
                                        if self.current_char in '(':
                                            return Token(PELICAN, "pelican", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pelican! Cause: {self.current_char}. Expected: open parenthesis '])
                                            self.advance()
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
                                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for perfection! Cause: {self.current_char}. Expected: dollar sign, whitespace'])
                                                        return [], errors
                                                    if self.current_char in break_delim:
                                                        return Token(PERFECTION, "perfection", pos_start = self.pos), errors
                                                    # elif self.current_char in alpha_num:
                                                    #     continue
                                                    else:
                                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for perfection! Cause: {self.current_char}. Expected: dollar sign, whitespace'])
                                                        self.advance()
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
                                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for planting! Cause: {self.current_char}. Expected: dollar sign, whitespace '])
                                                return [], errors
                                            if self.current_char in break_delim:
                                                return Token(PLANTING, "planting", pos_start = self.pos), errors
                                            # elif self.current_char in alpha_num:
                                            #     continue
                                            else:
                                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for planting! Cause: {self.current_char}. Expected: dollar sign, whitespace '])
                                                self.advance()
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
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pluck! Cause: {self.current_char}. Expected: open parenthesis'])
                                    return [], errors
                                if self.current_char in '(':
                                    return Token(PLUCK, "pluck", pos_start = self.pos), errors
                                # elif self.current_char in alpha_num:
                                #     continue
                                else:
                                    errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for pluck! Cause: {self.current_char}. Expected: open parenthesis'])
                                    self.advance()
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
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for ship! Cause: {self.current_char}. Expected: open parenthesis'])
                                return [], errors
                            if self.current_char in '(':
                                return Token(SHIP, "ship", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for ship! Cause: {self.current_char}. Expected: open parenthesis'])
                                self.advance()
                                return [], errors
                            
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
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for star! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
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
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for stardew! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                            return [], errors
                                        if self.current_char in spacepr_delim:
                                            return Token(STARDEW, "stardew", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for stardew! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                            self.advance()
                                            return [], errors
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for ! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                self.advance()
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
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for true! Cause: {self.current_char}. Expected: whitespace, dollar sign, close parenthesis, comma, close square bracket'])
                                return [], errors
                            if self.current_char in bool_delim:
                                return Token(TRUE, "true", pos_start = self.pos), errors
                            # elif self.current_char in alpha_num:
                            #     continue
                            else:
                                errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for true! Cause: {self.current_char}. Expected: whitespace, dollar sign, close parenthesis, comma, close square bracket'])
                                self.advance()
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
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for voidegg! Cause: {self.current_char}. Expected: whitespace, dollar sign, close parenthesis, comma, close square bracket '])
                                            return [], errors
                                        if self.current_char in bool_delim:
                                            return Token(VOIDEGG, "voidegg", pos_start = self.pos), errors
                                        # elif self.current_char in alpha_num:
                                        #     continue
                                        else:
                                            errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for voidegg! Cause: {self.current_char}. Expected: whitespace, dollar sign, close parenthesis, comma, close square bracket'])
                                            self.advance()
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
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for winter! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                        return [], errors
                                    if self.current_char in spacepr_delim:
                                        return Token(WINTER, "winter", pos_start = self.pos), errors
                                    # elif self.current_char in alpha_num:
                                    #     continue
                                    else:
                                        errors.extend([f'Error at line: {self.pos.ln + 1}. Invalid delimiter for winter! Cause: {self.current_char}. Expected: whitespace, open parenthesis'])
                                        self.advance()
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
            return None, f"Error at line: {self.pos.ln + 1}. Invalid identifier start: '{ident[0]}'. Word '{ident}' must start with an uppercase letter. "

        # Ensure no invalid characters are present
        if not all(c.isalnum() or c == "_" for c in ident):
            return None, f"Error at line: {self.pos.ln + 1}. Invalid character in word '{ident}'. Identifiers must be alphanumeric or underscores."

        # Ensure the next character is a valid delimiter
        if self.current_char is not None and self.current_char not in id_delim:
            return None, f"Error at line: {self.pos.ln + 1}. Invalid delimiter after word '{ident}'. Found: '{self.current_char}. Expected: {id_delim}."

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
            errors.append(f"Error at line: {self.pos.ln + 1}. Expected quotation mark!")
            return string, errors

#NODES
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self) -> str:
        return f'{self.tok}'
    

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self. right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'

#PARSE RESULT

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        
        return res
    
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#PARSER
    
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.perfection = False
        self.is_pelican = False
        self.in_loop = False
        self.in_condition = False
        self.in_fall = False
        self.in_farmhouse = False

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    #* parse takes the list of tokens then  decides which functions to execute based on the token
    def parse(self):
        res =  []
        error = []

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
                
            

        # * basically yung parse lang pero walang form

        while True:
            # if self.current_tok.token == SEMICOLON:
            #     print("semicolon")
            #     self.advance()
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
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected craft, or pelican, or farmhouse!"))

                break
            else:
                self.advance()
                
            if self.current_tok.token == SINGLELINE:
            
                self.advance()
                while self.current_tok.token != NEWLINE:
                    self.advance()
                self.advance()
        
            
                     
            #VAR DECLARATION  DAT MAY GLOBAL
            if self.current_tok.token in FARMHOUSE:
                if self.is_pelican == True:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please declare global variables before pelican!"))
                    break
                else:
                    self.advance() 
                
                    if self.current_tok.token in CROP: 
                        self.in_farmhouse = True
                        crop, crop_error = self.crop_dec()
                        if crop_error:
                            error.extend(crop_error)
                            break
                        #res.append(var)
                        #self.advance()
                        
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign from crop dec parse!"))
                        else:
                            self.advance()
                            self.in_farmhouse = False
                            res.append(["SUCCESS from global declaration!"])
                    else:
                        print("check", self.current_tok)
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid global variable declaration!"))
                        break

            # ? pwede i-bring back pag need specific
            # if self.current_tok.token in VAR:
            #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid global declaration!"))
            #     break
            
            

            #functions
            if self.current_tok.token == CRAFT:
                if self.is_pelican == True:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please declare craft before pelican!"))
                    break
                else:
                    craft_res, craft_error = self.init_craft()

                    if craft_error:
                        for err in craft_error:
                            error.append(err)
                        return res, error
                    else:
                        res.extend(craft_res)

            # -- this is the main body of our function! 
            # * also i call body() here
            if self.current_tok.token == PELICAN:
                if self.is_pelican == True:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Only one pelican function allowed!"))
                    return res, error

                self.is_pelican = True
                g_res, g_error = self.pelican()

                if g_error:
                    for err in g_error:
                        error.append(err)
                    break
                else:
                    res.extend(g_res)

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



        return res, error
    
    #* controls what happens when the compiler encounters the galaxy token
    def pelican(self):
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
                    craft_res, craft_error = self.body()
                    
                    if craft_error:
                        for err in craft_error:
                            error.append(err)
                        return [], error
                    else:
                        for f_res in craft_res:
                            res.extend(f_res)
                            
                        
                        if self.current_tok.token != CRBRACKET:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly brackets in pelican!"))
                            
                        else:
                            res.append("SUCCESS from PELICAN!")
                            self.advance()
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Pelican definition missing!"))
                    self.advance()
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis for pelican!"))   
        #form add(a, b)
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parentheses for parameters!"))
            return res, error
        # okay here we need to wrap this in a parseResult
        return res, error

    #* body controls the user defined functions as well as the main function
    def body(self):
        res =  []
        error = []

        
        # * basically yung parse lang pero walang form

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
                # if self.current_tok.token == SEMICOLON:
                #     print("semicolon")
                #     self.advance()
                if self.current_tok.token == NEWLINE:
                    self.advance()

                #not working yung INTEGER
                if self.current_tok.token in INTEGER:
                    res = self.expr()

                #--INITIALIZATION OF IDENTIFIERS
                if self.current_tok.token == IDENTIFIER:
                    self.advance()
                    #-- if it's a function call
                    if self.current_tok.token == LPAREN:
                        c_craft, call_craft_error = self.call_craft()
                        #self.advance()
                        if call_craft_error:
                            error.extend(call_craft_error)
                            break
                        else:
                            self.advance()
                            if self.current_tok.token in TERMINATOR:
                                res.append(c_craft)
                                self.advance()
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign in call craft!"))
                    elif self.current_tok.token == SLBRACKET:
                        self.advance()
                        if self.current_tok.token in (IDENTIFIER, INTEGER):
                            val, err = self.assign_val2([PLUS, MINUS, MUL,DIV,MODULUS])
                            if err:
                                error.append(err)
                            print("don: ", self.current_tok)
                            if self.current_tok.token == SRBRACKET:
                                self.advance()
                                if self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL or self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:

                                    assign, a_error = self.init_crop()
                                    
                                    
                                    if a_error:
                                        error.append(a_error)
                                        return res, error
                                    else:
                                        #self.advance()
                                        if self.current_tok.token != TERMINATOR:
                                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign! from init crop"))
                                            return res, error
                                        else:
                                            res.append(assign)
                                            self.advance()
                            else:
                                print("heres the error")
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ] !"))
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier!"))
                            

                        
                    #-- if we assign a value to it but not declaring it        
                    # so this is a = 1+3; 
                    elif self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL or self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:

                        assign, a_error = self.init_crop()
                        
                         
                        if a_error:
                            error.extend(a_error)
                            return res, error
                        else:
                            #self.advance()
                            if self.current_tok.token != TERMINATOR:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign! from init crop"))
                                return res, error
                            else:
                                res.append(assign)
                                self.advance()
                        
                    #-- if we increment it
                    elif self.current_tok.token == INCRE:
                        self.advance()
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(["SUCCESS from unary post increment"])
                            self.advance()
                    #-- if we decrement it
                    elif self.current_tok.token == DECRE:
                        self.advance()
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(["SUCCESS from unary post decrement"])
                            self.advance()
                    # -- else no other operation for it
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected assignment operator, increment, decrement, or call craft!"))
                        return [], error

                if self.current_tok.token == INCRE:
                    self.advance()
                    if self.current_tok.token == IDENTIFIER:
                        self.advance()
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(["SUCCESS from unary pre increment"])
                            self.advance()
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid unary statement!"))

                if self.current_tok.token == DECRE:
                    self.advance()
                    if self.current_tok.token == IDENTIFIER:
                        self.advance()
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                        else:
                            res.append(["SUCCESS from unary pre decrement"])
                            self.advance()
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid unary statement!"))
                #LOOPS
                if self.current_tok.token in FALL:
                    print("[DEBUG] pumasok sa fall")
                    self.advance()
                    fall_res, fall_error = self.fall_stmt()

                    if fall_error:
                        error.extend(fall_error)
                        break
                    else:
                        for fall_res in fall_res:
                            res.append(fall_res)
                            #self.advance()
                    
                #   winter_stmt   --here  
                if self.current_tok.token in WINTER:
                    self.advance()
                    if self.current_tok.token != LPAREN:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected (!"))
                        return res, error
                    w_res, w_error = self.star_winter_condition()
                    if w_error:
                        for err in w_error:
                            for e in err:
                                error.append(e)
                        return res, error
                    else:
                        if self.current_tok.token == CLBRACKET:
                            self.advance()
                            if self.in_condition == True:
                                self.in_condition = False
                            self.in_loop = True
                            w_result, w_err = self.body()
                            if w_err:
                                for err in w_err:
                                    error.append(err)
                                return [], error
                            else:
                                for w in w_result:
                                    res.append(w)
                                if self.current_tok.token != CRBRACKET:
                                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket for winter!"))
                                    return [], error
                                else:
                                    self.in_loop = False
                                    self.advance()
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected scope for winter!"))
                
                    # Handle list statements
                if self.current_tok.token in ADD:
                    add_res, add_error = self.add_stmt()
                    if add_error:
                        error.extend(add_error)
                        break
                    else:
                        res.extend(add_res)
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign after 'add'!"))
                        else:
                            self.advance()
                
                if self.current_tok.token in PLUCK:
                    pluck_res, pluck_error = self.pluck_stmt()
                    if pluck_error:
                        error.extend(pluck_error)
                        break
                    else:
                        res.extend(pluck_res)
                        if self.current_tok.token != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign after 'pluck'!"))
                        else:
                            self.advance()
                if self.current_tok.token == BREAK:
                    print("current break: ", self.current_tok)
                    self.advance()
                    if self.in_loop == True and self.in_condition == True:
                        
                        if self.current_tok.token == TERMINATOR:
                            self.advance()
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign from break!"))

                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Break not in valid scope!"))
                        self.advance()

                if self.current_tok.token == NEXT: # not yet implemented on docs
                    print("current next: ", self.current_tok)
                    self.advance()
                    if self.in_loop == True and self.in_condition == True:
                        if self.current_tok.token == TERMINATOR:
                            res.append(["SUCCESS from next"])
                            self.advance()
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign from next!"))

                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "next not in valid scope!"))
                        self.advance()

                #CONDITIONAL
                if self.current_tok.token in STAR:
                    print("FOUND STAR")
                    self.in_condition = True
                    star_res, star_error = self.star_stmt()
                    #self.advance() 
                    if star_error:
                        error.extend(star_error)
                        break
                    else:
                        for star_res in star_res:
                            res.append(star_res)
                            #self.advance()
                            self.in_condition = False
                        

                if self.current_tok.token in DEW:
                    dew_res, dew_error = self.dew_stmt()
                    self.advance()

                    if dew_error:
                        error.extend(dew_error)
                        break
                    else:
                        for dew_res in dew_res:
                            res.append(dew_res)
                        self.advance()

                #INPUT OUTPUT 
                if self.current_tok.token in SHIP: 
                    ship_res, ship_error = self.ship_stmt() 
                    #self.advance()
                    if ship_error:
                        error.extend(ship_error)
                        break
                    else:
                        print('SHIP!: ', self.current_tok)
                        
                        if self.current_tok.token  != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign in ship!"))
                            return res, error
                        else:  
                            res.append(["SUCCESS from SHIP"])
                            self.advance()
                            
                if self.current_tok.token in COLLECT:
                    print("[DEBUG] pumasok dito sa collect")
                    collect_res, collect_error = self.collect_stmt() 
                    if collect_error:
                        error.extend(collect_error)
                        break
                    else:
                        print('COLLECT!: ', self.current_tok)
                        if self.current_tok.token  != TERMINATOR:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign in collect!"))
                            return res, error
                        else:  
                            res.append(["SUCCESS from COLLECT"])
                            self.advance()

                        
                # VAR DECLARATION            
                if self.current_tok.token in CROP: 
                    var, crop_error = self.crop_dec()
                    if crop_error:
                        error.extend(crop_error)
                        print("crop error")
                        break
                    #res.append(var)
                    #self.advance()
                    
                    if self.current_tok.token != TERMINATOR:
                        print("check crop dec", self.current_tok)
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign, comma, +, -, *, /, %"))
                        return res, error
                    else:
                        self.advance()
                        print('SUCCESS FROM VARIABLE DEC')
                        res.append(["SUCCESS from variable declaration!"])
                
                
                if self.current_tok.token in CRAFT:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "You can't declare a function within a function!"))
                    break
                
                if self.current_tok.token == HARVEST:
                    self.advance()
                    print("HARVEST CHAR: ", self.current_tok)
                    if self.current_tok.token != INTEGER and self.current_tok.token != LPAREN and self.current_tok.token != IDENTIFIER and self.current_tok.token != TRUE and self.current_tok.token != FALSE and self.current_tok.token != STRING and self.current_tok.token != VOIDEGG and self.current_tok.token != FLOAT and self.current_tok.token != None:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, identifier, left parenthesis, true, false, string or voidegg!"))
                        break
                    else:
                        # self.advance()
                        harvest, err = self.assign_val()
                        if err:
                            for e in err:
                                #error.append(err)
                                error.append(e)
                                return res, error
                            
                        else:
                            # res.append("SUCCESS from harvest")
                            # return res, error
                            if self.current_tok.token != TERMINATOR:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
                                return res, error
                            else:
                                print("is pelican?: ", self.is_pelican)
                                if self.is_pelican == True:
                                    print("in harvest body")
                                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Can't call harvest in pelican!"))
                                    return res, error
                                else:
                                    res.append(["SUCCESS! from harvest"])
                                    self.advance()
                        
                if self.current_tok.token == PERFECTION:
                    self.advance()
                    if self.current_tok.token == TERMINATOR:
                        self.perfection = True
                        #self.advance()
                        return res, error
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Dollar sign expected for 'perfection'!"))

                if self.current_tok.token == CRBRACKET:
                    break

                if self.current_tok.token == EOF:
                    # error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "INVALID MAIN SCOPE"))
                    break
            
            else:
                print("[DEBUG]",self.current_tok)
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected crop, collect, ship, identifier, star, ++, --, winter, dew, stardew"))
                break


        return res, error
    
    # * checks if the current token's a valid statement in body
    def is_statement(self):
        if self.current_tok.token == BREAK or self.current_tok.token == SINGLELINE or self.current_tok.token == COMMENT or self.current_tok.token == NEWLINE or self.current_tok.token in INTEGER or self.current_tok.token == IDENTIFIER or self.current_tok.token in FALL or self.current_tok.token in WINTER or self.current_tok.token in WINTER or self.current_tok.token in SHIP or self.current_tok.token in STAR or self.current_tok.token in DEW or self.current_tok.token in COLLECT or self.current_tok.token in CROP or self.current_tok.token in HARVEST or self.current_tok.token in CRAFT or self.current_tok.token in CRBRACKET or self.current_tok.token in EOF or self.current_tok.token == INCRE or self.current_tok.token == DECRE  or self.current_tok.token == COMMENT or self.current_tok.token == MULTILINE_OPEN or self.current_tok.token == MULTILINE_CLOSE or self.current_tok.token ==PERFECTION:
            return True
        else:
            return False

    #* initialize a variable
    def init_crop(self):
        
        res = []
        error = []
        
        if self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL:
            # -- pag equal or plus equal lang pwede string
            
            self.advance()
            
            assign, err = self.assign_val()
            if err:
                #error.append(err)
                for e in err:
                    error.append(e)
                
            else:
                res.append("SUCCESS from assign")
                return res, error
        elif self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:
            #-- use assign val pero bawal dapat sa string
            
            self.advance()
            # todo dapat arithmetic values lang to since assignment yung ginagawa
            # should be assign, err = self.assign_val2(PLUS, MINUS, MUL, DIV, MODULUS)
            assign, err = self.assign_val2([PLUS, MINUS, MUL, DIV, MODULUS])
            

            if err:
                for e in err:
                    error.append(e)
                
            else:
                res.append("SUCCESS! from assign")
                    
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected assignment operator!"))
        return res, error
    
    #*declare a variable
    def crop_dec(self):
        res = []
        error = []
        # -- token when entering this function is 'var'
        self.advance()

        # -- if the user doesnt type an identiifier after 'var'
        if self.current_tok.token != IDENTIFIER:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
        else:
            self.advance()
            if self.current_tok.token == EQUAL or self.current_tok.token == COMMA:
                if self.current_tok.token == EQUAL:
                    print("Error crop: ", self.current_tok)
                    # -- USED SELF ASSIGN VAL 1
                    self.advance()
                    assign,err = self.assign_val()
                    if err:
                        for e in err:
                            error.append(e)
                        
                    else:
                        #self.advance()
                        if self.current_tok.token == COMMA:
                            comma, c_error = self.crop_dec()
                            
                            if c_error:
                                for err in c_error:
                                    error.append(err)
                            else:
                                for c in comma:
                                    res.append(c)
                    
                elif self.current_tok.token == COMMA:
                    if self.in_fall == False:
                        comma, c_error = self.crop_dec()
                        
                        if c_error:
                            for err in c_error:
                                error.append(err)
                        else:
                            for c in comma:
                                res.append(c)
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid  condition!"))
            elif self.current_tok.token == TERMINATOR:
                res.append("SUCCESS from variable declaration")
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected equal, comma or dollar sign!"))

        return res, error
    
    #* assign a value of a variable
    # -- may string, and boolean here, id, num, void, also paren support, used in =
    def assign_val(self):
        res = []
        error = []
        print("pumasok sa assign val: ", self.current_tok)
        if self.current_tok.token == STRING:
            print("PUMASOK SA UNANG STRING: ", self.current_tok)
            self.advance()
            
            # If next token is PLUS, proceed with concat handling
            while self.current_tok.token == PLUS:
                self.advance()
                print("pumasok sa string concat: ", self.current_tok)

                if self.current_tok.token == STRING or self.current_tok.token == IDENTIFIER:
                    self.advance()
                else:
                    error.append(InvalidSyntaxError(
                        self.current_tok.pos_start, 
                        self.current_tok.pos_end, 
                        "Expected identifier or string after '+'!"
                    ))
                    return res, error

            # Error: If after a string there's another operator that is NOT plus
            if self.current_tok.token in (MINUS, DIV, MODULUS, MUL, E_EQUAL , NOT_EQUAL , LESS_THAN , GREATER_THAN , LESS_THAN_EQUAL , GREATER_THAN_EQUAL, NOT_OP, AND_OP, OR_OP ):
                error.append(InvalidSyntaxError(
                    self.current_tok.pos_start, 
                    self.current_tok.pos_end, 
                    "Only '+' is allowed for string concatenation!"
                ))
                return res, error

            return res, error


        elif self.current_tok.token == INTEGER or self.current_tok.token == FLOAT or self.current_tok.token == IDENTIFIER:
            n_res, n_error = self.assign_val2([PLUS, MINUS, DIV, MODULUS, MUL])

            if n_error:
                for err in n_error:
                    error.append(err)
            else:
                res.append("Success form ident assign!")

            return res, error
        
        elif self.current_tok.token == LPAREN:
            
            n_res, n_error = self.assign_val2([PLUS, MINUS, DIV, MODULUS, MUL])

            if n_error:
                for err in n_error:
                    

                    error.append(err)
            else:
                
                res.append("Success form ident assign!")
        
        elif self.current_tok.token == TRUE:
            self.advance()
            return res, error
        elif self.current_tok.token == FALSE:
            self.advance()
            return res, error
        
        
        # Check for collect statement
        elif self.current_tok.token == COLLECT:
            print(f"[DEBUG] Collect statement detected.")
            self.advance()

            # Ensure opening parenthesis
            if not self.current_tok or self.current_tok.token != LPAREN:
                error.append(InvalidSyntaxError(
                    getattr(self.current_tok, 'pos_start', "Unknown"),
                    getattr(self.current_tok, 'pos_end', "Unknown"),
                    "Expected '(' after 'collect'!"
                ))
                return res, error

            self.advance()
            print(f"[DEBUG] Opening parenthesis detected: {self.current_tok.token}")
            # Ensure string prompt
            if not self.current_tok or self.current_tok.token != STRING:
                error.append(InvalidSyntaxError(
                    getattr(self.current_tok, 'pos_start', "Unknown"),
                    getattr(self.current_tok, 'pos_end', "Unknown"),
                    "Expected a prompt string inside 'collect'!"
                ))
                return res, error

            prompt_message = self.current_tok.token
            print(f"[DEBUG] Prompt message identified: {prompt_message}")
            res.append(f"Collect statement with prompt: {prompt_message}")
            
            self.advance()

            # Ensure closing parenthesis
            if not self.current_tok or self.current_tok.token != RPAREN:
                error.append(InvalidSyntaxError(
                    getattr(self.current_tok, 'pos_start', "Unknown"),
                    getattr(self.current_tok, 'pos_end', "Unknown"),
                    "Expected ')' to close 'collect' statement!"
                ))
                return res, error
            
            print(f"[DEBUG] Closing parenthesis detected: {self.current_tok.token}")
            self.advance()
            return res, error
        
        elif self.current_tok.token == SLBRACKET:
            print("INIT LIST")
            l_res, l_err = self.init_list()
            if l_err:
                for err in l_err:
                    error.append(err)
            else:
                res.append("Success list init!")
                self.advance()
        elif self.current_tok.token == VOIDEGG:
            self.advance()
            return res, error
        elif self.current_tok.token == INCRE or self.current_tok.token == DECRE:
            if self.in_farmhouse == True:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, true, false, void, string, [ "))
                return res, error
            self.advance()
            if self.current_tok.token != IDENTIFIER:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier!"))
            else:
                self.advance()

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier, number, boolean, string, list, or void!"))
    
        return res, error
        
    
    def assign_val2(self, ops):
        res = []
        error = []
        num =  []

        
        if self.current_tok.token == INTEGER or self.current_tok.token == FLOAT or self.current_tok.token == IDENTIFIER or self.current_tok.token == STRING:
            if self.current_tok.token in (INTEGER, FLOAT):
                num.append(self.current_tok.token)
            if self.current_tok.token == INTEGER or self.current_tok.token == FLOAT or self.current_tok.token == STRING:
                self.advance()

                if self.current_tok.token not in ops:
                    return res, error
                check, err = self.num_loop(num, ops)
                print("after num loop: ", self.current_tok)
                if err:
                    # print("FOUND AN ERROR IN NUM LOOP")    
                    for e in err:
                        error.append(e)
                        # print('error in num loop: ', e.as_string())
                    # print("i'll return the num loop now")
                    # print("error list: ", error)
                    #self.advance()
                    return [], error
                else:
                    # print("checked")
                    # #self.advance()
                    # print("after checked: ", self.current_tok)
                    res.append(["okay yung num loop!"])
                return res, error
                
                
                
            elif self.current_tok.token == IDENTIFIER:
                # print("assign val 2 ident")
                # print("first value in assign val is an identifier")
                self.advance()
                if self.in_farmhouse == True:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, true, false, voidegg, string, [ "))
                    return res, error
                if self.current_tok.token == LPAREN:
                    if self.in_farmhouse == True:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Cannot call craft in farmhouse declaration/initialization!"))
                        return res, error
                    # print("we assigned a function call to a variable")
                    c_craft, call_craft_error = self.call_craft()
                    # print("token after call form in assign val: ", self.current_tok.token)
                    #self.advance()
                    # print('call form result in assign val:', c_form)
                    if call_craft_error:
                        print("ERROR IN VALL CRAFT") 
                        for err in call_craft_error:
                            error.append(err)
                        
                    else:
                        self.advance()
                        print("FOUND CRAFT CALL OPERAND HERE: ", self.current_tok)
                        if self.current_tok.token in (MUL, DIV, PLUS, MINUS, MODULUS):
                            # -- USED SELF.ASSIGN_VAL()
                            self.advance()
                            check, err = self.assign_val2([MUL, DIV, PLUS, MINUS, MODULUS])
                            print("token after form arith: ", self.current_tok)
                            if  err:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!!"))

                            else:
                                res.append("Success craft ident assign!")
                        return res, error
                elif self.current_tok.token == SLBRACKET:
                    # print("assign val 2 list")
                    #TODO LIST
                    print("you got a list")
                    self.advance()
                    print("after list: ", self.current_tok)
                    list, err = self.assign_val2([PLUS, MINUS, MUL, DIV, MODULUS])
                    # print('after list index: ', self.current_tok)
                    # print("list: ", err)
                    if err:
                        #error.append(err)
                        for e in err:
                            error.append(e)
                        #return res, error
                    else:
                        if self.current_tok.token != SRBRACKET:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing bracket for list!"))
                        else:
                            # print("Sucess from assign list")
                            self.advance()
                            num, err = self.num_loop()
                            if err:
                                error.append(err)
                            else:
                                res.append("Success form ident assign!")
                # elif self.current_tok.token in (INCRE, DECRE):
                #     if self.in_universe == True:
                #         error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, true, false, void, string, [ "))
                #         return res, error
                #     #self.advance()
                    
                #     res.append("success unary init")
                #     self.advance()
                #     ########
                else:
                    # print('FIRST OPERAND IS AN IDENTIFIER')
                    num, err = self.num_loop()
                    if err:
                        error.append(err)
                    else:
                        res.append("Success form ident assign!")

        elif self.current_tok.token == LPAREN:
            print("PARENTHESIS IN ASSIGN")
            self.advance()
            if self.current_tok.token == RPAREN:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier or left parenthesis!"))   
            else:
                check, err = self.assign_val2([PLUS, MINUS, DIV, MUL, MODULUS])
            #self.advance()
                
                if err:
                    error.append(err)
                    

                else:
                    if self.current_tok.token == RPAREN:
                        print("found closing")
                        self.advance()
                        
                        if self.current_tok.token in (PLUS, MINUS, DIV, MUL, MODULUS):
                            print("found operator  after paren")
                            self.advance()
                            num, err = self.assign_val2([PLUS, MINUS, DIV, MUL, MODULUS])
                            if  err:
                                for e in err:
                                    error.append(e)

                            else:
                                res.append("Success form ident assign!")

                        return res, error
                        
                            
                        #return True
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
        # elif self.current_tok.token == INCRE or self.current_tok.token == DECRE:
        #     self.advance()
        #     if self.current_tok.token != IDENTIFIER:
        #         error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier!"))
        #     else:
        #         self.advance()
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, identifier or left parenthesis!"))
    
        return res, error

    
    def add_stmt(self):
        res = []
        error = []

        print(f"[DEBUG] Starting add_stmt with token: {self.current_tok.token}")

        # Parse `add` keyword
        self.advance()
        if self.current_tok.token != LPAREN:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after 'add'!"))
            return res, error

        self.advance()
        print(f"[DEBUG] Parsing add parameters, token: {self.current_tok.token}")

        # First token must be IDENTIFIER
        if self.current_tok.token == IDENTIFIER:
            res.append(self.current_tok.token)
            self.advance()
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier as the first argument in 'add'!"))
            return res, error

        # Must have a comma next
        if self.current_tok.token != COMMA:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ',' after identifier in 'add'!"))
            return res, error

        self.advance()

        # Now expect a valid second argument (list value: number or literal)
        if self.current_tok.token in (INTEGER, FLOAT, IDENTIFIER, STRING, TRUE, FALSE):
            res.append(self.current_tok.token)
            self.advance()
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected a list value after ',' in 'add'!"))
            return res, error

        # Closing parenthesis
        if self.current_tok.token != RPAREN:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' to close 'add' statement!"))
            return res, error

        res.append("Success from add")
        self.advance()

        return res, error

    
    def pluck_stmt(self):
        res = []
        error = []

        print(f"[DEBUG] Starting pluck_stmt with token: {self.current_tok.token}")

        # Parse `pluck` keyword
        self.advance()
        if self.current_tok.token != LPAREN:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after 'pluck'!"))
            return res, error

        self.advance()
        print(f"[DEBUG] Parsing pluck parameters, token: {self.current_tok.token}")

        # Parse the first identifier
        if self.current_tok.token == IDENTIFIER:
            res.append(self.current_tok.token)
            self.advance()
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected an identifier in 'pluck'!"))
            return res, error

        # Parse additional comma-separated values
        while self.current_tok.token == COMMA:
            self.advance()
            if self.current_tok.token in (IDENTIFIER, STRING, INTEGER, FLOAT, TRUE, FALSE):
                res.append(self.current_tok.token)
                self.advance()
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected a valid value after ',' in 'pluck'!"))
                return res, error

        # Parse closing parenthesis
        if self.current_tok.token != RPAREN:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' to close 'pluck' statement!"))
            return res, error

        res.append("Success from pluck")
        self.advance()

        return res, error

 
    def num_loop(self, check = [], ops = []):
        res = []
        error = []
        ops_string = ""
        #num = []
        # print("current tok in num loop: ", self.current_tok)
        while self.current_tok.token in (PLUS, MINUS, DIV, MUL, MODULUS):
            ops_string += self.current_tok.token
            self.advance()
            if self.current_tok.token in (INTEGER, FLOAT, IDENTIFIER):
                self.advance()
                if self.current_tok.token in (INTEGER, FLOAT):
                    # print("found NUMBER")
                    check.append(self.current_tok.token)
                elif self.current_tok.token == SLBRACKET:
                    self.advance()
                    print("num loop slbracket")
                    if self.current_tok.token in (IDENTIFIER, INTEGER):
                        # self.advance()
                        var, err = self.assign_val2([PLUS, MINUS, DIV, MUL, MODULUS])
                        if err:
                            error.append(err)
                        if self.current_tok.token in SRBRACKET:
                            print("found srbracket")
                            self.advance()
                        else:
                            print('no ]')
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ]"))
                    else:
                        print("no ] 1")
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ]"))


            elif self.current_tok.token == LPAREN:
                # print("found a left paren in num loop")
                self.advance()

                if self.current_tok.token == RPAREN:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier, number, or open parenthesis!"))
                    
                num, err = self.assign_val2([PLUS, MINUS, DIV, MUL, MODULUS])
                # print("CURRENT TOKEN AFTER PARENTHESIS ASSIGN VAL CALL IN NUM LOOP: ", self.current_tok)
                if self.current_tok.token != RPAREN:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parethesis in arithmetic expression!"))
                    
                else:
                    # print("found closing")
                    self.advance()
                    
                        
                    if self.current_tok.token in (PLUS, MINUS, DIV, MUL, MODULUS):
                        # print("found operator  after paren in num loop: ",  self.current_tok)
                        self.advance()
                        num, err = self.assign_val2(ops)
                        if  err:
                            for e in err:
                                error.append(e)
                        else:
                            return res, error

                    return res, error
                

            elif self.current_tok.token == STRING:
                # print("check:", check)
                # print("there's a string here")
                if "-" in ops_string or "/" in ops_string or "%" in ops_string or "*" in ops_string:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected + !"))
                    # print("ERROR IN STRING OPS")
                elif INTEGER in check or FLOAT in check:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Cannot concat string with number!"))
                    # print("ERROR IN STRING OPS")
                    return res, error
                else:
                    # print("advanced after string found")
                    self.advance()


            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier!"))
                return res, error

        
            # else:
            #     return False
        # print("end the num lop value: ", self.current_tok)
        return res, error
          

    #* DECLARING A CRAFT OR SUBFUNCTION
    def init_craft(self):
        res = []
        error = []

        print(f"[DEBUG] Starting init_craft with token: {self.current_tok.token if self.current_tok else 'None'}")

        # Advance to check for craft identifier
        self.advance()
        if self.current_tok.token == IDENTIFIER:
            print(f"[DEBUG] Craft name found: {self.current_tok.token}")
            self.advance()

            # Check for either '(' or '[' after the function name
            if self.current_tok.token == LPAREN:
                print(f"[DEBUG] Found opening parenthesis: {self.current_tok.token}")
                self.advance()

                # Check if the function has parameters or is empty
                if self.current_tok.token == RPAREN:
                    print("[DEBUG] Empty parameter list using '()' detected")
                    self.advance()  # Move past the closing parenthesis
                else:
                    # Expecting parameters in the form of 'crop Identifier'
                    while self.current_tok.token == CROP:
                        print("[DEBUG] Found 'crop' keyword in parameters")
                        self.advance()

                        # Ensure crop is followed by an identifier
                        if self.current_tok.token == IDENTIFIER:
                            print(f"[DEBUG] Found identifier after 'crop': {self.current_tok.token}")
                            self.advance()
                        else:
                            error.append(InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected identifier after 'crop' in parameter list!"
                            ))
                            return res, error

                        # Handle comma-separated parameters
                        if self.current_tok.token == COMMA:
                            print(f"[DEBUG] Found comma, processing next parameter")
                            self.advance()
                        elif self.current_tok.token == RPAREN:
                            break  # End of parameter list
                        else:
                            error.append(InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ',' or ')' in parameter list!"
                            ))
                            return res, error

                    # Ensure closing parenthesis ')'
                    if self.current_tok.token != RPAREN:
                        error.append(InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected closing parenthesis in craft parameters!"
                        ))
                        return res, error
                    else:
                        print(f"[DEBUG] Found closing parenthesis: {self.current_tok.token}")
                        self.advance()

            elif self.current_tok.token == SLBRACKET:  # Allow `[]` as an empty parameter placeholder
                print(f"[DEBUG] Found empty parameter list notation '['")
                self.advance()

                # Ensure closing bracket `]`
                if self.current_tok.token == SRBRACKET:
                    print(f"[DEBUG] Found closing bracket for empty list parameter: {self.current_tok.token}")
                    self.advance()
                else:
                    error.append(InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ']' after '[' for empty parameter list!"
                    ))
                    return res, error

            else:
                error.append(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '(' or '[' after craft identifier!"
                ))
                return res, error

            # Check for opening curly bracket '{'
            if self.current_tok.token == CLBRACKET:
                print(f"[DEBUG] Found opening curly bracket: {self.current_tok.token}")
                self.advance()

                # Skip any newlines
                while self.current_tok.token == NEWLINE:
                    self.advance()
                    print("[DEBUG] Skipping newlines before craft body")

                # Process the body of the craft
                craft_res, craft_error = self.body()
                if craft_error:
                    print("[DEBUG] Error inside the craft body")
                    error.extend(craft_error)
                    return [], error
                else:
                    print("[DEBUG] Successfully processed craft body")
                    res.extend(craft_res)

                # Ensure closing curly bracket '}'
                if self.current_tok.token != CRBRACKET:
                    error.append(InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected closing curly bracket in craft definition!"
                    ))
                    return res, error
                else:
                    print(f"[DEBUG] Found closing curly bracket: {self.current_tok.token}")
                    self.advance()
                    res.append("SUCCESS from CRAFT!")
            else:
                error.append(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected opening curly bracket for craft body!"
                ))
                return res, error
        else:
            error.append(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected craft identifier!"
            ))
            return res, error

        return res, error


    
    # * INITIALIZE A LIST
    def init_list(self):
        res = []
        error = []
        #-- so una muna yung SLBRACKET
        self.advance()
        if self.current_tok.token == IDENTIFIER or self.current_tok.token == INTEGER or self.current_tok.token == STRING or self.current_tok.token == TRUE or self.current_tok.token == FALSE or self.current_tok.token == FLOAT:
        
            self.advance()
            if self.current_tok.token == COMMA:
                #if comma yung current, find identifier, next, then if comma, next, and repeat
                a_error = self.list_literal()
                if a_error:
                     
                    error.extend(a_error)
                
                else:
                    if self.current_tok.token != SRBRACKET:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing square bracket or comma!"))
                        self.advance()
                    else: 

                        res.append(["SUCCESS from list init!"])
                            
            elif self.current_tok.token == SRBRACKET:
                res.append(["SUCCESS from init list!"])
                    
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected comma or ]"))

        elif self.current_tok.token == SRBRACKET:
            
            res.append(["SUCCESS from list  init!"])         

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, f"Expected number, identifier, string, true, or false"))


        return res, error
    
    #* CALLING A CRAFT
    def call_craft(self):
        res = []
        error = []
        
        self.advance()
        print("FUNC CALL TOK: ", self.current_tok)
        if self.current_tok.token == IDENTIFIER or self.current_tok.token == INTEGER or self.current_tok.token == STRING or self.current_tok.token == TRUE or self.current_tok.token == FALSE or self.current_tok.token == FLOAT or self.current_tok.token == VOIDEGG:
            print("tok after ident: ", self.current_tok)
            
            val, err = self.assign_val2([PLUS,MINUS, DIV, MUL, MODULUS])
            if err:
                error.append(err)
            if self.current_tok.token == COMMA:
                #if comma yung current, find identifier, next, then if comma, next, and repeat
                a_error = self.arguments()
                if a_error:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, identifier, true, false, or string after commna!"))
                
                else:
                    if self.current_tok.token != RPAREN:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                        self.advance()
                    else: 

                        res.append(["SUCCESS from function call!"])
                 
            print(f"[DEBUG] In call_craft(), current token before RPAREN check: {self.current_tok.token}")
            if self.current_tok.token == RPAREN:
                print(f"[DEBUG] Matched RPAREN correctly")
                res.append(["SUCCESS from function call!"])
            else:
                print(f"[DEBUG] DID NOT match RPAREN, got: {self.current_tok.token}")
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))

    
        elif self.current_tok.token == RPAREN:
            print("rparen found")
            res.append(["SUCCESS from function call!"])         

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier, number, string, boolean, ), or void!"))

        return res, error
    
    def arguments (self):
        error = False
        while self.current_tok.token  == COMMA:
            self.advance()
            if self.current_tok.token == IDENTIFIER or self.current_tok.token == INTEGER or self.current_tok.token == STRING or self.current_tok.token == TRUE or self.current_tok.token == FALSE or self.current_tok.token==FLOAT or self.current_tok.token == VOIDEGG :
                self.advance()
            else:
                #error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                error = True
        return error
    
    def list_literal (self):
        res = []
        error = []
        #error = False
        print("pumasok sa list literal: ", self.current_tok)
        while self.current_tok.token  == COMMA:
            self.advance()
            if self.current_tok.token == IDENTIFIER or self.current_tok.token == INTEGER or self.current_tok.token == STRING or self.current_tok.token == TRUE or self.current_tok.token == FALSE or self.current_tok.token==FLOAT :
                print("PASOK SA LOOP: ", self.current_tok)
                self.advance()
                print("after ng loop: ", self.current_tok)
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier, number, string, or boolean value!"))

        return error

    def comma(self):
        res = []
        error = []
        #error = False
        while self.current_tok.token  == COMMA:
            self.advance()
            if self.current_tok.token == CROP:
                self.advance()
                if self.current_tok.token == IDENTIFIER:
                    self.advance()
                else:
                    #error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier "))

            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected crop "))
                
                
        return res, error
    
    #*LOOPING STATEMENTS
    def fall_stmt(self):
        res = []
        error = []
        #TODO create 
        if self.current_tok.token == LPAREN:
            self.advance()
            crop, crop_error = self.if_first_condition()
            print("[DEBUG] ok na sa first condition")
            if crop_error:
                error.extend(crop_error)
                return res, error
            else:
                #self.advance()
                #TODO relational operator
                rel, rel_error = self.fall_rel()
                # ! DITO DAPAT YUNG SEMICOLON
                if rel_error:
                    error.extend(rel_error)
                    return res, error
                else:
                    #TODO unary and assignment
                        #self.advance()
                    if self.current_tok.token == TERMINATOR:
                        #res.append(["SUCCESS from "])
                        self.advance()
                        print("ok na sa second condition")
                        #return res, error
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign from 2nd condition!"))
                        return res, error
                    
                    # * nasa identifier tayo rn
                    rel2, rel2_error = self.star_iteration()
                    #nasa r paren tayo if ever nag assign value tayo sa iteration
                    #self.advance()
                    if rel2_error:
                        error.extend(rel2_error)
                        return res, error
                    else:
                        #self.advance()
                        # print("success 3rd condition")
                        # print("after success 3rd condition:" , self.current_tok)
                        if self.current_tok.token != RPAREN:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis for FALL!"))
                        else:
                            self.advance()
                            # print("success condition")
                            #TODO FORCE SCOPE
                            if self.current_tok.token == CLBRACKET:
                                if self.in_condition == True:
                                    self.in_condition = False
                                self.in_loop = True
                                self.advance()
                                fall_res, fall_error = self.body()
                                # print(" res: ", res)
                                if fall_error:
                                    print("THERES  AN ERROR INSIDE THE FORCE SCOPE")
                                    for err in fall_error:
                                        error.append(err)
                                    return [], error
                                else:
                                    for f_res in fall_res:
                                        res.append(f_res)
                                        # print("f res: ", f_res)
                                    res.append([f"SUCCESS from FALL"])
                                    self.advance()
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid  scope!"))
        return res, error

    # -- need a function for the var dec of 
    def if_crop_dec(self):
        res = []
        error = []
        # -- token when entering this function is 'var'
        self.advance()

        # -- if the user doesnt type an identiifier after 'var'
        if self.current_tok.token != IDENTIFIER:
            print("bro put an identifier!")
            print("current tok: ", self.current_tok.token)
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
        else:
            # print("u good")
            self.advance()
            
            if self.current_tok.token == EQUAL:
                # print("value after equal: ", self.current_tok)
                # -- USED SELF ASSIGN VAL 2 kasi number lang
                self.advance()
                assign,err = self.assign_val2([PLUS, MINUS, MUL, DIV, MODULUS])
                if err:
                    for e in err:
                        error.append(e)
                    
                else:
                    #self.advance()
                    # print("CURRENT TOKEN FROM VAR DEC INIT: ", self.current_tok)
                    res.append("success init first statement ")
                
            
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected = !"))

            #res.append("SUCCESS! from variable declaration")


        return res, error
    
    #-- need ng init function for  lang
    def fall_init_crop(self):
        res = []
        error = []
        if self.current_tok.token == EQUAL:
            print("in init crop")
            self.advance()
            assign, err = self.assign_val2([PLUS, MINUS, DIV, MUL, MODULUS])
            print("assign: ", err)
            if err:
                #error.append(err)
                for e in err:
                    error.append(e)


            else:
                # semicolon current char
                if self.current_tok.token != TERMINATOR:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign after first statement"))
                else:    
                    res.append(" first condition")
                    self.advance()
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected = !"))

        return res, error
    # combine lang  init and var
    def if_first_condition(self):
        res = []
        error = []
        if self.current_tok.token == CROP:
            # print("this is a var token")
            crop, crop_error = self.if_crop_dec()
            if crop_error:
                error.extend(crop_error)
                return res, error
            #res.append(var)
            #self.advance()
            # print("current token from var dec parse: ", self.current_tok)
            
            if self.current_tok.token != TERMINATOR:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected dollar sign!"))
            else:
                self.advance()
                res.append([" first condition"])
        elif self.current_tok.token == "Identifier":
            self.advance()
            init_res, init_err = self.fall_init_crop()
            if init_err:
                error.extend(init_err)
            else:
                res.append([" first condition init"])
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid  condition!"))

        return res, error   
         
    # -- need relational for 
    def fall_rel(self):
        res = []
        error = []
        if self.current_tok.token == NOT_OP:
            self.advance()
            if self.current_tok.token != LPAREN:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please enclose the relation operation in parenthesis!"))
        if self.current_tok.token == LPAREN:
            print("found lparen")
            self.advance()
            f_rel, f_err = self.fall_rel()
            if f_err:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid relational operation!"))
                return res, error
            else:
                print("sucess for 2nd rel in paren: ", self.current_tok)
                if self.current_tok.token == RPAREN:
                    res.append("lparen good")
                    self.advance()
                    return res, error
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                    return res, error


        elif self.current_tok.token == IDENTIFIER:
            self.advance()
            if self.current_tok.token in (E_EQUAL , NOT_EQUAL , LESS_THAN , GREATER_THAN , LESS_THAN_EQUAL , GREATER_THAN_EQUAL):
                self.advance()
                if self.current_tok.token in (INTEGER, FLOAT, IDENTIFIER, LPAREN):
                
                    n_res, n_error = self.assign_val2([PLUS, MINUS, DIV, MUL, MODULUS])
                    # print("assign val in arith rel op left in 3: ", self.current_tok.token)
                    if n_error:
                        for err in n_error:
                            error.append(err)
                        return res, error
                    #self.advance()

                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier, or lparen!"))
                    print("error operand: ", self.current_tok)
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected <, >, <=, >=, !=  "))
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid  loop!"))
            print("error operand: ", self.current_tok)


        return res, error

    # -- need unary statement for 
    def star_iteration(self):
        res = []
        error = []
        #--INITIALIZATION OF IDENTIFIERS
        if self.current_tok.token == IDENTIFIER:
            self.advance()
            #-- if we assign a value to it but not declaring it           
            if self.current_tok.token == PLUS_EQUAL or self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:
                print("initialize the variable")
                assign, a_error = self.init_crop()

                if a_error:
                    error.extend(a_error)
                    
                else:
                    #self.advance()
                    return res, error
            #-- if we increment it
            elif self.current_tok.token == INCRE:
                self.advance()
                return res, error
            #-- if we decrement it
            elif self.current_tok.token == DECRE:
                self.advance()
                return res, error
            # -- else no other operation for it
            else:
                print('INVALID IDENT OPERATION')
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected --, ++, +=, -=, *=, /="))
                return [], error
        elif self.current_tok.token == INCRE:
            self.advance()
            if self.current_tok.token == IDENTIFIER:
                self.advance()
                
                return res, error
            
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after increment!"))

        elif self.current_tok.token == DECRE:
            self.advance()
            if self.current_tok.token == IDENTIFIER:
                self.advance()
                return res, error
                    
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifierafter decrement!"))

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier, ++, or --"))
        

        return res, error


    def winter(self):
        res = []
        error = []
        print("first token in winter: ", self.current_tok)
        
        if self.current_tok.token == LPAREN:
            self.advance()
            if self.current_tok.token == IDENTIFIER:
                self.advance()
                if self.current_tok.token == E_EQUAL or self.current_tok.token == LESS_THAN or self.current_tok.token == GREATER_THAN or self.current_tok.token == GREATER_THAN_EQUAL or self.current_tok.token == LESS_THAN_EQUAL or self.current_tok.token == NOT_EQUAL:
                    self.advance()
                    if self.current_tok.token == INTEGER or self.current_tok.token == FLOAT or self.current_tok.token == IDENTIFIER or self.current_tok.token == STRING:
                        self.advance()
                        if self.current_tok.token == RPAREN:
                            res.append('SUCCESS from winter!')
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis! winter"))

                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier! winter"))
                        
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected relational operator!"))

            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier for winter!"))

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected condition for winter!"))

        return res, error
        
    def ship_stmt(self):
        res = []
        error = []

        print(f"[DEBUG] Starting ship_stmt with token: {self.current_tok.token if self.current_tok else 'None'}")

        self.advance()  # Skip 'ship'
        if not self.current_tok or self.current_tok.token != LPAREN:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after 'ship'!"))
            return res, error

        res.append(self.current_tok.token)
        self.advance()

        expecting_arg = True

        while self.current_tok:
            if self.current_tok.token == RPAREN:
                if expecting_arg:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Trailing comma without argument in ship()!"))
                    return res, error
                res.append(self.current_tok.token)
                self.advance()
                break

            if expecting_arg:
                if self.current_tok.token in (
                    STRING, TRUE, FALSE, IDENTIFIER, INTEGER, FLOAT,
                    LPAREN, SLBRACKET, VOIDEGG, COLLECT
                ):
                    print(f"[DEBUG] Parsing argument using assign_val: {self.current_tok.token}")
                    val_tokens, val_errors = self.assign_val()
                    if val_errors:
                        error.extend(val_errors)
                        return res, error
                    res.extend(val_tokens)
                    expecting_arg = False
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                    f"Unexpected token in ship() arguments: {self.current_tok.token}"))
                    return res, error

            elif self.current_tok.token == COMMA:
                print(f"[DEBUG] Comma found")
                res.append(self.current_tok.token)
                self.advance()
                expecting_arg = True

            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                f"Expected ',' or ')' after argument, got: {self.current_tok.token}"))
                return res, error

        # # ✅ Terminator $
        # if self.current_tok.token == TERMINATOR:
        #     print(f"[DEBUG] Found terminator")
        #     res.append(self.current_tok.token)
        #     self.advance()
        # else:
        #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '$' after 'ship' statement!"))
        #     return res, error

        print(f"[DEBUG] Completed parsing ship statement: {res}")
        return res, error

    
    #*CONDITIONAL
    #FUNC FOR IF, ELSE, ELSEIF
    def star_stmt(self):
        print("IN STAR STATEMENT")
        res = []
        error = []
        self.advance()
        if self.current_tok.token == LPAREN:
            self.advance()
            c_ces, c_error = self.star_winter_condition()
            if c_error:
                for err in c_error:
                    error.append(err)
            else:
                
                if self.current_tok.token == RPAREN:
                    self.advance()
                
                    # if self.current_tok.token == NEWLINE:
                    #     self.advance()
                    if self.current_tok.token == CLBRACKET:
                        self.advance()
                        star_res, star_error = self.body()
                        # print("if res: ", res)
                        if star_error:
                            print("THERES  AN ERROR INSIDE THE STAR SCOPE")
                            for err in star_error:
                                error.append(err)
                            return [], error
                        else:
                            # print("successful if!")
                            for star_res in star_res:
                                res.append(star_res)
                                # print("f res: ", f_res)
                            res.append([f"SUCCESS from star"])
                            self.advance()

                            while self.current_tok.token == STARDEW: #elseif
                                if self.current_tok.token in STARDEW:
                                    # print("this is an elif statement")
                                    stardew_res, stardew_error = self.stardew_stmt()
                                    #self.advance()

                                    if stardew_error:
                                        # for err in elif_error:
                                        #     error.append(err)
                                        for err in stardew_error:
                                            error.append(err)

                                    else:
                                        for stardew_res in stardew_res:
                                            res.append(stardew_res)
                                            # print("current token from elseif parse: ", self.current_tok)
                                        #self.advance()
                            # print("token after last elseif: ", self.current_tok)
                            if self.current_tok.token == DEW:
                                # print('ELSE FOUND')
                                dew_res, dew_error = self.dew_stmt()
                                    #self.advance()

                                if dew_error:
                                    # for err in elif_error:
                                    #     error.append(err)
                                    for err in dew_error:
                                        error.append(err)

                                else:
                                    for dew_res in dew_res:
                                        res.append(dew_res)
                                        # print("current token from else parse: ", self.current_tok)
                            #self.advance()
                        
                            return res, error
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected { !"))
                        
                    #res.append(["SUCCESS FROM IF"]) 
                    
                else:
                    print("error star stmt: ", self.current_tok)
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis! Multiple relational operators ('==' or '!=' or >= or <= or > or <) are not allowed in a single expression."))
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Exepected left paren!"))

        return res, error
    
    def stardew_stmt(self):
        res = []
        error = []
        self.advance()
        if self.current_tok.token == LPAREN:
            self.advance()
            c_ces, c_error = self.star_winter_condition()
            if c_error:
                for err in c_error:
                    error.append(err)
            else:
                if self.current_tok.token == RPAREN:
                    self.advance()
                    # if self.current_tok.token == NEWLINE:
                    #     self.advance()
                    if self.current_tok.token == CLBRACKET:
                        self.advance()
                        star_res, star_error = self.body()
                        # print("elif res: ", res)
                        if star_error:
                            print("THERES  AN ERROR INSIDE THE STARDEW SCOPE")
                            for err in star_error:
                                error.append(err)
                            return [], error
                        else:
                            # print("successful elif!")
                            for f_res in star_res:
                                res.append(f_res)
                                # print("f res: ", f_res)
                            res.append(["SUCCESS from elif"])
                            self.advance()
                            # if self.current_tok.token in ELSEIF:
                            #     print("this is an elif statement")
                            #     elif_res, elif_error = self.elif_stmt()
                            #     #self.advance()

                            #     if elif_error:
                            #         # for err in elif_error:
                            #         #     error.append(err)
                            #         error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid elif condition!"))

                            #     else:
                            #         for fres in elif_res:
                            #             res.append(fres)
                            #             print("current token from elseif parse: ", self.current_tok)
                            #         self.advance()
                            # return res, error
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected { !"))
                        
                    #res.append(["SUCCESS FROM IF"]) 
                    
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected (!"))

        return res, error
    
    def dew_stmt(self):
        res = []
        error = []
        self.advance()
        # print("IN ELSE STMT: ", self.current_tok)
        if self.current_tok.token != CLBRACKET:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected { !"))
        else:
            self.advance()
            dew_res, dew_error = self.body()
            # print("if res: ", res)
            if dew_error:
                print("THERES  AN ERROR INSIDE THE IF SCOPE")
                for err in dew_error:
                    error.append(err)
                return [], error
            else:
                # print("successful else!")
                for f_res in dew_res:
                    res.append(f_res)
                    # print("f res: ", f_res)
                res.append(["SUCCESS from else"])
                self.advance()
                
                            
                #next is yung new line, curly brackerts and stamements
        return res, error

    def star_winter_condition(self):
        res = []
        error = []
        # print("IN IF WHIRL NOW")
        if self.current_tok.token == NOT_OP:
            # print("found not op in if whirl condition")
            self.advance()
            if self.current_tok.token != LPAREN:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parenthesis for relational after not operator!"))
                return res, error
        if self.current_tok.token == LPAREN:
            self.advance()
            if self.current_tok.token == NOT_OP:
                self.advance()
                if self.current_tok.token != LPAREN:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parenthesis for relational after not operator!"))
                    return res, error
            if self.current_tok.token == RPAREN:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier or left parentheis!"))
                return res, error

            c_ces, c_error = self.star_winter_condition()
            if c_error:
                for err in c_error:
                    error.append(err)
            else:
                if self.current_tok.token == RPAREN:
                    
                    self.advance()
                    if self.current_tok.token in LOG_OP:
                        self.advance()
                        c_ces, c_error = self.star_winter_condition()
                        if c_error:
                            for err in c_error:
                                error.append(err)
                        else:
                            if self.current_tok.token == RPAREN:
                                res.append("SUCCESS FROM CONDITION") 
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                    else:
                        res.append("SUCCESS FROM CONDITION")       
                        return res, error
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
        elif self.current_tok.token in (IDENTIFIER, INTEGER, FLOAT, STRING) : 
            if self.current_tok.token in (INTEGER, FLOAT, IDENTIFIER, STRING):
                if self.current_tok.token in (INTEGER, FLOAT, IDENTIFIER):
                    n_res, n_error = self.assign_val2([PLUS, MINUS, MUL, DIV, MODULUS])
                    # print("assign val in arith rel op left 1: ", self.current_tok)
                    if n_error:
                        # print("ERROR IN assign val in arith rel op left")
                        for err in n_error:
                            error.append(err)
                        return res, error
                    # print("going to check the value now: ", self.current_tok)
                    #self.advance()
                if self.current_tok.token in (IDENTIFIER, STRING):
                    print("IDENTIFIER/STRING DETECTED: ", self.current_tok)
                    self.advance()
                    if self.current_tok.token in IDENTIFIER:
                        # ✅ Handle Concatenation Using `assign_val2()`
                        if self.current_tok.token == PLUS:
                            print("CONCATENATION DETECTED: Passing to assign_val2()", self.current_tok)
                            n_res, n_error = self.assign_val2([PLUS, MINUS, MUL, DIV, MODULUS]) # Ensure `+` only for concatenation
                            if n_error:
                                for err in n_error:
                                    error.append(err)
                                return res, error  
                            return res, error  # ✅ Valid Concatenation
                    else:
                        comparison_seen = False
                        # ✅ Fully Process Concatenation Before `==`
                        while self.current_tok.token == PLUS:
                            self.advance()
                            
                            # Ensure valid concatenation: Only Strings and Identifiers can be concatenated
                            if self.current_tok.token not in (STRING, IDENTIFIER):
                                error.append(InvalidSyntaxError(
                                    self.current_tok.pos_start, self.current_tok.pos_end,
                                    "Invalid concatenation: Strings can only be concatenated with other strings or identifiers."
                                ))
                                return res, error  

                            # ✅ Advance after valid concatenation
                            self.advance()

                        # ✅ Now, Process Comparison Operators (`==`, `!=`)
                        if self.current_tok.token in (E_EQUAL, NOT_EQUAL):
                            if comparison_seen:
                                error.append(InvalidSyntaxError(
                                    self.current_tok.pos_start, self.current_tok.pos_end,
                                    "Only one '==' or '!=' is allowed in a star condition."
                                ))
                                return res, error

                            comparison_seen = True
                            self.advance()

                            # Validate type of right-hand operand
                            if self.current_tok.token in (INTEGER, FLOAT, TRUE, FALSE):
                                error.append(InvalidSyntaxError(
                                    self.current_tok.pos_start, self.current_tok.pos_end,
                                    "Cannot compare string to number or boolean using '==' or '!='."
                                ))
                                return res, error
                            elif self.current_tok.token not in (STRING, IDENTIFIER):
                                error.append(InvalidSyntaxError(
                                    self.current_tok.pos_start, self.current_tok.pos_end,
                                    "Expected a string or identifier on the right side of comparison."
                                ))
                                return res, error

                            self.advance()

                            # ✅ Handle optional string concatenation
                            while self.current_tok.token == PLUS:
                                self.advance()
                                if self.current_tok.token not in (STRING, IDENTIFIER):
                                    error.append(InvalidSyntaxError(
                                        self.current_tok.pos_start, self.current_tok.pos_end,
                                        "Only strings or identifiers can be concatenated."
                                    ))
                                    return res, error
                                self.advance()

                            # ✅ BLOCK any chained comparisons like == "2" > 0
                            if self.current_tok.token in REL_OP:
                                error.append(InvalidSyntaxError(
                                    self.current_tok.pos_start, self.current_tok.pos_end,
                                    "Invalid chained comparison."
                                ))
                                return res, error

                        else: 
                            if self.current_tok.token in (AND_OP, OR_OP):
                                print("LOGICAL OPERATOR DETECTED WITHOUT COMPARISON OPERATOR: ", self.current_tok)
                                self.advance()
                                c_ces, c_error = self.star_winter_condition()
                                if c_error:
                                    for err in c_error:
                                        error.append(err)
                                    return res, error  
                                return res, error 
                            if self.current_tok.token == RPAREN:
                                return res, error
                            else:
                                error.append(InvalidSyntaxError(
                                    self.current_tok.pos_start, self.current_tok.pos_end,
                                    "Expected '==' or '!=' relational operator before logical operator!"
                                ))
                                print("Nandito error star_winter: ", self.current_tok)
                                return res, error  
        
            if self.current_tok.token in REL_OP:
                self.advance()
                if self.current_tok.token in (IDENTIFIER, INTEGER, FLOAT, TRUE, STRING, FALSE):
                    if self.current_tok.token == TRUE:
                        self.advance()
                    elif self.current_tok.token == FALSE:
                        self.advance()
                    elif self.current_tok.token in (INTEGER, FLOAT, IDENTIFIER, STRING):
                        #TODO RECURSIVE CALL SA IF WHIRL CONDITION
                        c_ces, c_error = self.star_winter_condition()
                        if c_error:
                            print("ERROR IN LEFT SIDE")
                            for err in c_error:
                                error.append(err)
                        else:
                            # print("REL OP TOKEN: ", self.current_tok)
                            if self.current_tok.token == RPAREN:
                                return res, error
                elif self.current_tok.token in LPAREN:
                    #TODO RECURSIVE CALL SA IF WHIRL CONDITION
                    n_res, n_error = self.assign_val2()
                    # print("assign val in arith rel op left 2: ", self.current_tok.token)
                    if n_error:
                        # print("ERROR IN assign val in arith rel op left")
                        for err in n_error:
                            error.append(err)
                        return res, error
                         
                       
                else:
                    print("star wingter condition: ", self.current_tok)
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number or identifier! whirl condition"))
            elif self.current_tok.token in LOG_OP:
                print("LOG OP FOUND")
                self.advance()
                
                if self.current_tok.token in (IDENTIFIER, INTEGER, FLOAT):

                    c_ces, c_error = self.star_winter_condition()
                    if c_error:
                        print('error after log op')
                        for err in c_error:
                            error.append(err)
                        
                    
                    else:
                        print("SUCCESS NAMAN YUNG RIGHT SIDE: ", self.current_tok)
                        if self.current_tok.token == RPAREN:
                            
                            #self.advance()
                            
                            res.append("SUCCESS FROM CONDITION")       
                            return res, error
                        else:
                            print("R PAREN NOT FOUND")
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid if condition!"))
                elif self.current_tok.token == LPAREN:
                    self.advance()
                    if self.current_tok.token == NOT_OP:
                        self.advance()
                    c_ces, c_error = self.star_winter_condition()
                    if c_error:
                        for err in c_error:
                            error.append(err)
                    else:
                        if self.current_tok.token == RPAREN:
                            
                            self.advance()
                            if self.current_tok.token in LOG_OP:
                                self.advance()
                                c_ces, c_error = self.star_winter_condition()
                                if c_error:
                                    for err in c_error:
                                        error.append(err)
                                else:
                                    if self.current_tok.token == RPAREN:
                                        res.append("SUCCESS FROM CONDITION") 
                                    else:
                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                            else:
                                res.append("SUCCESS FROM CONDITION")       
                                return res, error
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                #------------------
                else:
                    print("error 2nd part")
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected left paren or identifier!"))
            elif self.current_tok.token == RPAREN:
                res.append("SUCCESS from if condition")
                return res, error 
            else:
                print("ETO YUNG ERROR: ", self.current_tok)
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected logical operator or relational operator or arithmetic operator or right parenthesis!"))
                return res, error
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected number, identifier, or left paren!"))
        
        return res, error

    #?PARSE RESULT ARE HERE
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        
        # if tok.token in STRING:
        #     return res.success(tok.value)
        
        # if tok.token in IDENTIFIER:
        #     return res.success(tok.token)
        
        if tok.token in (PLUS, MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        if tok.token in (INTEGER, FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.token == LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.token == RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))
        #return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float"))
    
    def term(self):
        return self.bin_op(self.factor, (MUL, DIV))
    
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

    def expr(self):
        return self.bin_op(self.term, (PLUS, MINUS))
    
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
   
    #func is rule (expr or term)
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func()) #instead of self.factor() or self.term()
        if res.error:
            return res

        while self.current_tok.token in ops: #instead of (MUL, DIV)
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func()) #instead of self.factor() or self.term()
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

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
       
  

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    # Create a new list excluding spaces or lists
    tokens = [item for item in tokens if not (isinstance(item, list) or item.token == SPACE)]
    
    print("TOKENS: ", tokens)
    
    parser = Parser(tokens)
    result, parseError = parser.parse()
    

    return parser, parseError # result check

class StardewLexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Junimo Code Lexical Analyzer")
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
        self.line_numbers.tag_configure("first_line", spacing1=25)  # Adjust first-line spacing

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
        self.line_numbers = tk.Text(self.code_frame, width=4, padx=3, takefocus=0, fg="#ffe9db",
                                     bg="#8f3901", highlightthickness=0, state=tk.DISABLED)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_input.pack(padx=10, pady=10)
        # self.code_input.configure(yscrollcommand=self.sync_scrollbars)
        # self.line_numbers.configure(yscrollcommand=self.sync_scrollbars)
        #image for Lexical Analyzer Button/Button
        self.analyze_button = Image.open("Images\Lexical.png")
        self.resize_analyze_button = self.analyze_button.resize((200,50))
        self.analyze_button_picture = ImageTk.PhotoImage(self.resize_analyze_button)
        self.image_analyze_button = tk.Button(image=self.analyze_button_picture, borderwidth=0, command=self.analyze_code_with_sound)
        self.image_analyze_button.place(x=200, y=920)

        #image for Clear Analyzer Button/Button
        self.semantic_button = Image.open("Images\Clear.png")
        self.resize_semantic_button = self.semantic_button.resize((200,50))
        self.semantic_button_picture = ImageTk.PhotoImage(self.resize_semantic_button)
        self.image_semantic_button = tk.Button(image=self.semantic_button_picture, borderwidth=0, command=self.clear_input_with_sound)
        self.image_semantic_button.place(x=450, y=920)

        #image for Undo Button/Button
        self.syntax_button = Image.open("Images\Syntax.png") #placeholder for syntax button
        self.resize_syntax_button = self.syntax_button.resize((200,50))
        self.syntax_button_picture = ImageTk.PhotoImage(self.resize_syntax_button)
        self.image_syntax_button = tk.Button(image=self.syntax_button_picture, borderwidth=0, command=self.syntax_analyzer_with_sound)
        self.image_syntax_button.place(x=710, y=920)


        #Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Verdana", 14), fieldbackground="#ffe9db", rowheight=25)  # Change font for Treeview
        style.configure("Treeview.Heading", font=("Verdana", 16), background="#d88e41", foreground="#ffe9db")  # Change font for headings

        # Token Table
        self.token_frame = ctk.CTkFrame(self.root, fg_color="#8f3901", corner_radius=10)
        self.token_frame.place(x=830, y=50)

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
        self.terminal_frame = ctk.CTkFrame(self.root, width=200, height=100, fg_color="#8f3901", corner_radius=10)
        self.terminal_frame.place(x=100, y=800)
        self.terminal_output = ctk.CTkTextbox(self.terminal_frame, width=700, height=85,
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

    def analyze_code_with_sound(self):
        mixer.Sound.play(click_sound)
        self.analyze_code()

    def clear_input_with_sound(self):
        mixer.Sound.play(click_sound)
        self.clear_input()

    def syntax_analyzer_with_sound(self):
        mixer.Sound.play(click_sound)
        self.syntax_analyzer()


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
            print(f"[DEBUG] Total Errors Found: {len(errors)}")  # Debugging: Ensure all errors exist
            for err in errors:
                print(f"[DEBUG] Processing Error: {err}")  # Debugging: Print each error
                self.terminal_output.insert(tk.END, f"{err}\n")  # Ensure all errors are displayed
        else:
            self.terminal_output.insert(tk.END, "Sucess from Lexical.\n")


            
    def clear_input(self):
        """Clear the code input box"""
        self.code_input.delete("1.0", tk.END)

    def syntax_analyzer(self): # syntax button
        
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
            syntax_result, syntax_error = run("<junimo code>", code)
            if syntax_error:
                print(f"[DEBUG] Syntax Errors Encountered: {syntax_error}")  # Debugging
                for err in syntax_error:
                    print(f"[DEBUG] Raw Error Object: {err}")  # Debug each error object
                    if isinstance(err, list):  # If error is a list, iterate further
                        for e in err:
                            formatted_error = (
                                "\n".join(e.as_string()) if isinstance(e.as_string(), tuple) else e.as_string()
                            )
                            print(f"[DEBUG] Formatted Nested Error: {formatted_error}")
                            self.terminal_output.insert(tk.END, formatted_error + "\n")
                    else:  # Process individual errors
                        formatted_error = (
                            "\n".join(err.as_string()) if isinstance(err.as_string(), tuple) else err.as_string()
                        )
                        print(f"[DEBUG] Formatted Error: {formatted_error}")
                        self.terminal_output.insert(tk.END, formatted_error + "\n")


                # for err in syntax_error:
                #     print(f"[DEBUG] Processing syntax error: {err}")  # Debugging: Print raw error object
                    
                #     if isinstance(err, list):  # If error is a list, iterate through its elements
                #         for sub_err in err:
                #             if hasattr(sub_err, "as_string") and callable(sub_err.as_string):
                #                 formatted_error = sub_err.as_string()
                                
                #                 # Ensure it's a single string, not a tuple
                #                 if isinstance(formatted_error, tuple):
                #                     formatted_error = "\n".join(formatted_error)

                #                 print(f"[DEBUG] Formatted Error: {formatted_error}")  # Debugging
                #                 self.terminal_output.insert(tk.END, formatted_error + "\n")
                #             else:
                #                 error_message = f"Error: {str(sub_err)}"
                #                 print(f"[DEBUG] Fallback Error: {error_message}")  # Debugging
                #                 self.terminal_output.insert(tk.END, error_message + "\n")
                #     else:  # If error is a single object
                #         if hasattr(err, "as_string") and callable(err.as_string):
                #             formatted_error = err.as_string()
                            
                #             # Ensure it's a single string, not a tuple
                #             if isinstance(formatted_error, tuple):
                #                 formatted_error = "\n".join(formatted_error)

                #             print(f"[DEBUG] Formatted Error: {formatted_error}")  # Debugging
                #             self.terminal_output.insert(tk.END, formatted_error + "\n")
                #         else:
                #             error_message = f"Error: {str(err)}"
                #             print(f"[DEBUG] Fallback Error: {error_message}")  # Debugging
                #             self.terminal_output.insert(tk.END, error_message + "\n")

            else:
                
                # for res in syntax_result:
                self.terminal_output.insert(tk.END, "Success from Syntax")
                # errors_text.insert(tk.END, "SUCCESS")


if __name__ == "__main__":
    root = ctk.CTk()
    app = StardewLexerGUI(root)
    root.mainloop()
