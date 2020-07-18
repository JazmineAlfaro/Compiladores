from token import *
from lexer import *

def find_pos(array, element):
    for i in range(len(array)):
        if array[i] == element:
            return i

    return -1



class Terminal:
    def __init__(self, val):
        self.label = val

    def interpret(self):
        return self.label


class Numero(Terminal):
    def __init__(self, val):
        super().__init__(val)


class Suma(Terminal):
    def __init__(self):
        super().__init__('+')


class Resta(Terminal):
    def __init__(self):
        super().__init__('-')


class Multiplicacion(Terminal):
    def __init__(self):
        super().__init__('*')


class Division(Terminal):
    def __init__(self):
        super().__init__('/')


class Lambda(Terminal):
    def __init__(self):
        super().__init__('lambda')


class NNTerminal:
    def __init__(self, val):
        self.label = val
        self.prod = dict()


class E(NNTerminal):
    def __init__(self, grammar):
        super().__init__('E')
        self.prod['T'] = None
        self.prod['Ep'] = None
        self.g = grammar

    def interpret(self, text):

        self.prod['T'] = T(self.g)
        self.prod['Ep'] = Ep(self.g)

        if type(text) == list and len(text) > 1:
            return self.prod['Ep'].interpret(text[0], text[1:])
        else:
            return self.prod['Ep'].interpret(text, '')


class Ep(NNTerminal):
    def __init__(self, grammar):
        super().__init__('Ep')
        self.prod['+'] = None
        self.prod['-'] = None
        self.prod['T'] = None
        self.prod['Ep'] = None
        self.prod['lambda'] = None
        self.g = grammar

    def interpret(self, anterior, text):

        self.prod['T'] = T(self.g)
        self.prod['Ep'] = Ep(self.g)

        valorT = self.prod['T'].interpret(anterior)
        if text == '':
            self.prod['lambda'] = Lambda()
        elif text[0] == '+':
            self.prod['+'] = Suma()
        elif text[0] == '-':
            self.prod['-'] = Resta()

        if self.prod['+'] is not None:
            self.prod['+'].interpret()
            if len(text) > 2:
                suma = valorT + self.prod['Ep'].interpret(text[1], text[2:])
            else:
                suma = valorT + self.prod['Ep'].interpret(text[1], '')

            return suma

        elif self.prod['-'] is not None:
            self.prod['-'].interpret()

            if len(text) > 2:
                resta = valorT - self.prod['Ep'].interpret(text[1], text[2:])
            else:
                resta = valorT - self.prod['Ep'].interpret(text[1], '')

            return resta

        elif self.prod['lambda'] is not None:
            self.prod['lambda'].interpret()
            return valorT



class T(NNTerminal):
    def __init__(self, grammar):
        super().__init__('T')
        self.prod['F'] = None
        self.prod['Tp'] = None
        self.g = grammar

    def interpret(self, text):
        self.prod['F'] = F(self.g)
        self.prod['Tp'] = Tp(self.g)

        if type(text) == list() and len(text) > 1:
            return self.prod['Tp'].interpret(text[0],text[1:])
        else:
            return self.prod['Tp'].interpret(text, '')


class Tp(NNTerminal):
    def __init__(self, grammar):
        super().__init__('Tp')
        self.prod['*'] = None
        self.prod['/'] = None
        self.prod['F'] = None
        self.prod['Tp'] = None
        self.prod['lambda'] = None
        self.g = grammar
    def interpret(self, anterior, text):
        self.prod['F'] = F(self.g)
        valorF = self.prod['F'].interpret(anterior)

        if text == '':
            self.prod['lambda'] = Lambda()
        elif text[0] == '*':
            self.prod['*'] = Multiplicacion()
        elif text[0] == '/':
            self.prod['/'] = Division()

        if self.prod['*'] is not None:
            self.prod['*'].interpret()
            if len(text) > 2:
                mult = valorF * self.prod['Tp'].interpret(text[1], text[2:])
            else:
                mult = valorF * self.prod['Tp'].interpret(text[1], '')
            return mult
        elif self.prod['/'] is not None:
            self.prod['/'].interpret()
            if len(text) > 2:
                div = valorF / self.prod['Tp'].interpret(text[1], text[2:])
            else:
                div = valorF / self.prod['Tp'].interpret(text[1], '')
            return div
        elif self.prod['lambda'] is not None:
            self.prod['lambda'].interpret()
            return valorF

class F(NNTerminal):
    def __init__(self, grammar):
        super().__init__('F')
        self.prod['('] = None
        self.prod['E'] = None
        self.prod[')'] = None
        self.prod['num'] = None
        self.g = grammar

    def interpret(self, text):


        if type(text) == int:
            self.prod['num'] = Numero(text)
        elif text[0] == '(':
            self.prod['E'] = E(self.g)

        if self.prod['E'] is not None:
            return
        elif self.prod['num'] != None:
            return self.prod['num'].interpret()



