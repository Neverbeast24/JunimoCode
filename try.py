#alphabet
alpha_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = 'abcdefghijklmnopqrstuvwxyz'
all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

#numbers
all_numbers = '0123456789'
zero = '0'
number = '123456789'

#alphanumeric and speacial symbols
punctuation_symbols = "!@#$%^&*()-_=+[]{"+ "}\|:;',<>./?" + '"'
alpha_num = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ascii_string = "!\#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
ascii = all_letters + punctuation_symbols + all_numbers

#operators 
arithmetic_ops = "+-*/%"
relational_ops = '><==!<=>=!='
logical_ops = '||&&!'
unary_ops = '++--'
assignment_ops = '=+=-=*=/='
op_delim = logical_ops + arithmetic_ops + relational_ops
negative = '~'

#others
newline = '\n'
tab = '\t'
whitespace = " "
terminator = "$"
comma = ','

dew_delim = whitespace + newline + '{'
string1_delim = whitespace + ascii_string
string2_delim = whitespace + comma + '+' + ')'
delim0 = whitespace + alpha_num + negative + '('
delim1 = whitespace + alpha_num + '"' + '('
delim3 = whitespace + all_numbers + '"'
delim4 = whitespace + all_numbers + '"'
comma_delim = whitespace + alpha_num + '"'
unary_delim = whitespace + all_letters + terminator
bool_delim = whitespace + terminator + comma + ')'
num_delim = arithmetic_ops + '(' + whitespace + comma  + relational_ops + ")]" + terminator
id_delim = newline + comma + whitespace + "=)[]<>!" + arithmetic_ops
spacebr_delim = whitespace + '('
break_delim = terminator + whitespace

#errors
error = []

#TOKENS

#reserved words
PLANTING = 'planting' #Start
PERFECTION = 'perfection' #End
PELICAN = 'pelican'

VOIDEGG = 'voidegg'
STRING = 'string'
CROP = 'crop'

#input and output statements
COLLECT = 'collect'
SHIP = 'ship' 
#conditional statements
STAR = 'star'
DEW = 'dew'
STARDEW = 'stardew'

#looping statements
FOR = 'for'
WHILE = 'while'

#loop control statements
BREAK = 'break'

#other statements
HARVEST = 'harvest'
CRAFT = 'craft'
FARMHOUSE = 'farmhouse'
TRUE = 'true'
FALSE = 'false'


#OPERATORS

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
#negative operator
NEG_OP = '~'
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
N_TAB = '\\t'
N_LINE = '\\n'
SHARP = '##'
Q_MARK = "\""
SQ_MARK = "\'"
SINGLELINE = '@}'
MULTILINE_OPEN = '@}~'
MULTILINE_CLOSE =  '~{@'
SEMICOLON = ';'
COLON = ':'
UNDERSCORE = "_"
NEWLINE= "\\n"
IN = ">>"
OUT = "<<"
#TILDE = "~"
LOG_OP = NOT_OP + AND_OP + OR_OP
REL_OP = [E_EQUAL , NOT_EQUAL , LESS_THAN , GREATER_THAN , LESS_THAN_EQUAL , GREATER_THAN_EQUAL]

#literals

IDENTIFIER = 'IDENTI'
COMMA = ','
SPACE = "space"
EOF = 'EOF'
COMMENT = "COMMENT"

class Error:
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

class DelimiterError(Error):
    def __init__(self,pos_start, pos_end, details, char):
        super().__init__(pos_start, pos_end, f"Invalid Delimiter for '{char}'", "Cause -> " + str(details))

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

class Lexer:
    
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx <= len(self.text)-1 else None

    def make_tokens(self):
        tokens = []
        errors = []
        
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '\n':
                tokens.append(Token(NEWLINE, "\\n"))
                self.advance()
            elif self.current_char in all_letters:
                token, error = self.make_word()
                if error:
                    errors.append(error)
                tokens.append(token)
            elif self.current_char in all_numbers:
                token, error = self.make_number()
                if error:
                    errors.append(error)
                tokens.append(token)
            elif self.current_char == '@':
                token, error = self.make_comment()
                if error:
                    errors.append(error)
                tokens.append(token)
            elif self.current_char == '"':
                token, error = self.make_string()
                if error:
                    errors.append(error)
                tokens.append(token)
            else:
                token, error = self.make_symbol()
                if error:
                    errors.append(error)
                tokens.append(token)
        
        tokens.append(Token(EOF, "EOF"))
        return tokens, errors
    
    # Handle reserved words and identifiers
    def make_word(self):
        word = ''
        while self.current_char is not None and self.current_char.isalpha():
            word += self.current_char
            self.advance()
        
        if word in RESERVED_WORDS:
            return Token(word.upper(), word), None
        elif word[0].isupper():
            return Token(IDENTIFIER, word), None
        else:
            return None, f"Invalid identifier: {word}. Identifiers must start with an uppercase letter."
    
    # Handle numeric literals (both integers and floats)
    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    return None, f"Invalid number format: {num_str}. Multiple decimal points are not allowed."
                dot_count += 1
            num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(INT, int(num_str)), None
        elif dot_count == 1:
            return Token(FLOAT, float(num_str)), None
        else:
            return None, f"Invalid number format: {num_str}."

    # Handle string literals
    def make_string(self):
        string = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()
        
        if self.current_char == '"':
            self.advance()  # Skip the closing quote
            return Token(STRING, string), None
        else:
            return None, "String literal not closed properly."

    # Handle comments (single-line and multi-line)
    def make_comment(self):
        if self.current_char == '@':
            self.advance()
            if self.current_char == '}':
                # Single-line comment
                while self.current_char != '\n':
                    self.advance()
                return Token(COMMENT, "Single-line comment"), None
            elif self.current_char == '}~':
                # Multi-line comment
                self.advance()
                comment_text = ''
                while self.current_char != '~{@':
                    comment_text += self.current_char
                    self.advance()
                self.advance()  # Skip ~{@
                return Token(COMMENT, "Multi-line comment"), None
            else:
                return None, "Invalid comment syntax."

    # Handle operators and reserved symbols
    def make_symbol(self):
        if self.current_char == '=':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, "=="), None
            return Token(ASSIGN, '='), None
        elif self.current_char == '+':
            self.advance()
            if self.current_char == '+':
                self.advance()
                return Token(INCREMENT, '++'), None
            elif self.current_char == '=':
                self.advance()
                return Token(PLUS_EQUAL, '+='), None
            return Token(PLUS, '+'), None
        elif self.current_char == '-':
            self.advance()
            if self.current_char == '-':
                self.advance()
                return Token(DECREMENT, '--'), None
            elif self.current_char == '=':
                self.advance()
                return Token(MINUS_EQUAL, '-='), None
            return Token(MINUS, '-'), None
        elif self.current_char == '*':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(MUL_EQUAL, '*='), None
            return Token(MUL, '*'), None
        elif self.current_char == '/':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(DIV_EQUAL, '/='), None
            return Token(DIV, '/'), None
        elif self.current_char == '%':
            self.advance()
            return Token(MODULUS, '%'), None
        elif self.current_char == '!':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(NOT_EQUAL, '!='), None
            return Token(NOT, '!'), None
        elif self.current_char == '<':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(LESS_EQUAL, '<='), None
            return Token(LESS_THAN, '<'), None
        elif self.current_char == '>':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(GREATER_EQUAL, '>='), None
            return Token(GREATER_THAN, '>'), None
        elif self.current_char == '&':
            self.advance()
            if self.current_char == '&':
                self.advance()
                return Token(AND_OP, '&&'), None
            return None, "Invalid logical operator. Did you mean '&&'?"
        elif self.current_char == '|':
            self.advance()
            if self.current_char == '|':
                self.advance()
                return Token(OR_OP, '||'), None
            return None, "Invalid logical operator. Did you mean '||'?"
        elif self.current_char == '$':
            self.advance()
            return Token(TERMINATOR, '$'), None
        elif self.current_char in '(){}[]':
            symbol = self.current_char
            self.advance()
            return Token(symbol, symbol), None
        else:
            return None, f"Illegal character: {self.current_char}"

