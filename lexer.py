from token import Token
KEYWORDS = ['int', 'float', 'string', 'def', 'if', 'elif', 'else', 'print', 'return']
compare = ['<=', '>=', '==', '!=']
other = ['=', '>', '<']
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
SPECIAL = '+-*/{}(); '
OPERATOR = '+-/*'
DIGITS = '0123456789'
T_INT = 'INT'
T_FLOAT = 'FLOAT'
T_OP = 'OPERATOR'
T_LPAR = 'LPAR'
T_RPAR = 'RPAR'
T_EOF = 'EOF'
T_LBRA = 'LBRA'
T_RBRA = 'RBRA'
T_SC = 'SEMICOLON'
T_KEY = 'KEYWORD'
T_STR = 'STRING'
T_EL = 'ENDLINE'
T_EQ = 'EQUAL'
T_COMP1 = 'EQTO'
T_COMP2 = 'GREATER'
T_GEQ = 'GREATEREQ'
T_COMP3 = 'LOWER'
T_LEQ = 'LOWEREQ'
T_DIFF = "DIFFERENT"
T_UND = "UNDEFINED"

class Lexer:
    def __init__(self, text, log1, l):
        self.text = text
        self.current_char = None
        self.position = 0
        self.flag = False
        self.log = log1
        self.line = l

    def generate_tokens(self):
        tokens = []
        pos = 0
        line = 0
        lpar = 0
        rpar = 0
        while pos < len(self.text) :
            curr_char = self.text[pos]
            if curr_char in DIGITS:
                tokens.append(self.make_number(pos, line))
            elif curr_char in ALPHABET:
                tokens.append(self.make_string(pos, line))
            elif curr_char == "+":
                tokens.append(Token(T_OP, '+', line, pos, pos, '+'))
            elif curr_char == "-":
                tokens.append(Token(T_OP, '-', line, pos, pos, '-'))
            elif curr_char == " " :
                pass
            elif curr_char =='\n' :
                tokens.append(Token(T_EL, 'end', line, pos, pos, 'end'))
            elif curr_char == "*":
                tokens.append(Token(T_OP, '*', line, pos, pos, '*'))
            elif curr_char == "/":
                tokens.append(Token(T_OP, '/', line, pos, pos, '/'))
            elif curr_char == "(":
                lpar += 1
                tokens.append(Token(T_LPAR, '(', line, pos, pos, '('))
            elif curr_char == ")":
                rpar += 1
                tokens.append(Token(T_RPAR, ')', line, pos, pos, ')'))
            elif curr_char == "{":
                tokens.append(Token(T_LBRA, '{', line, pos, pos, '{'))
            elif curr_char == "}":
                tokens.append(Token(T_RBRA, '}', line, pos, pos, '}'))
            elif curr_char == ";":
                tokens.append(Token(T_SC, ';', line, pos, pos, ';'))
            elif curr_char == "=":
                if self.text[pos + 1] == '=':
                    tokens.append(Token(T_COMP1, '==', line, pos, pos + 1, '=='))
                    pos += 1
                else:
                    tokens.append(Token(T_EQ, '=', line, pos, pos, '='))
            elif curr_char == ">":
                if self.text[pos + 1] == '=':
                    tokens.append(Token(T_GEQ, '>=', line, pos, pos + 1, '>='))
                    pos += 1
                else:
                    tokens.append(Token(T_COMP2, '>', line, pos, pos, '>'))
            elif curr_char == "<":
                if self.text[pos + 1] == '=':
                    tokens.append(Token(T_LEQ, '<=', line, pos, pos + 1, '<='))
                    pos += 1
                else:
                    tokens.append(Token(T_COMP3, '<', line, pos, pos, '<'))
            elif curr_char == "!":
                if self.text[pos + 1] == '=':
                    tokens.append(Token(T_DIFF, '!=', line, pos, pos + 1, '!='))
                    pos += 1
            else:
                tokens.append(Token(T_UND, curr_char, line, pos, pos, 'UND'))

            if self.flag:
                self.flag = False
                pos = self.position

            else:
                pos += 1

        if rpar != lpar:
            self.log.addError('4',line)
            self.log.print()
            self.log.panicMode()

        return tokens

    def make_number(self, pos, line):
        num_str = ''
        dot_count = 0
        cur_pos = 0
        for i in range(pos, len(self.text)):
            if self.text[i] == ".":
                if dot_count == 1:
                    cur_pos = i
                    break
                dot_count += 1
                num_str += '.'
            elif self.text[i] == ' ' or self.text[i] == '\n' or self.text[i] in OPERATOR:
                cur_pos = i
                break
            elif self.text[i].isalpha():
                self.log.addError('1', line)
                self.log.print()
                self.log.panicMode()
            else:
                num_str += self.text[i]
                cur_pos = i

        self.position = cur_pos
        self.flag = True
        if dot_count == 0:
            return Token(T_INT, int(num_str), line, pos, cur_pos, 'num')
        else:
            return Token(T_FLOAT, float(num_str), line, pos, cur_pos, 'num' )

    def make_string(self, pos, line):
        str = ''
        cur_pos = 0
        for i in range(pos, len(self.text)):
            if self.text[i] in SPECIAL or self.text[i] in other or self.text[i] == '\n':
                cur_pos = i
                break
            else:
                str += self.text[i]
                cur_pos = i

        self.position = cur_pos
        self.flag = True
        if str in KEYWORDS:
            return Token(T_KEY, str, line,  pos, cur_pos - 1, str )
        else:
            return Token(T_STR, str, line, pos , cur_pos -1, 'id')

    def verify_code(self):
        lpar = 0
        rpar = 0
        lbra = 0
        rbra = 0
        var = list()
        prev = 0
        keyword = 0
        for t in self.text:
            if prev and prev.type == 'KEYWORD' and t.type == 'KEYWORD':
                self.log.addError('8', 0)
                self.log.panicMode()
            elif t.type == 'KEYWORD':
                keyword = t.value
            elif t.value == '=':
                var.append(prev.value)
            elif prev and prev.value == '=' :
                '''print(t)
                print(t.type)
                print(keyword.upper())
                print(var)
                '''
                if t.value in var:
                    t.type = 'VAR'
                    pass
                elif t.value not in var and t.type != keyword.upper():
                    if t.type == 'INT' and keyword.upper() == 'FLOAT':
                        self.log.addError('9', t.line)
                        self.log.panicMode()
                    elif t.type == 'FLOAT' and keyword.upper() == 'INT':
                        self.log.addError('10', t.line)
                        self.log.panicMode()
                    else :
                        self.log.addError('7', t.line)
                        self.log.panicMode()
                elif t.type != keyword.upper():
                    self.log.addError('6', t.line)
                    self.log.panicMode()
            elif t.value == '(':
                lpar += 1
            elif t.value == ')':
                rpar += 1
            elif t.value == '{':
                lbra += 1
            elif t.value == '}':
                rbra += 1
            prev = t

        if rpar != lpar:
            self.log.addError('4')
            self.log.panicMode()
        elif lbra != rbra:
            self.log.addError('5')
            self.log.panicMode()