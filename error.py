from token import *
from termcolor import colored

class DiccionarioError:
    def __init__(self):
        self.dict_errores = {
            "0": "Operador inválido",
            "1": "Número Inválido",
            "2": "Operador inválido",
            "3": "Expresión no válida",
            "4": "Cantidad incorrecta de paréntesis",
            "5": "Cantidad incorrecta de llaves",
            "6": "No corresponde al tipo de la variable",
            "7": "Variable no declarada anteriormente",
            "8": "El nombre de la variable es un keyword",
            "9": "Se esperaba un int",
            "10": "Se esperaba un float"
        }
        self.dict_warning = {
            "0" : "Número mayor a 65535"
        }

class Log:
    __instance__ = None

    def __init__(self, d):
        if Log.__instance__ is None:
            Log.__instance__ = self
            self.errores = d.dict_errores
            self.warnings = d.dict_warning
            self.listaerrores = list()
            self.listawarnings = list()

        else:
            raise Exception(colored("Ya existe una clase Log", 'red'))

    @staticmethod
    def get_instance():
        if not Log.__instance__:
            Log()
        return Log.__instance__


    def addError(self, codigo, token = 0):

        self.listaerrores.append(codigo)
        self.listaerrores.append(token)

    def addWarning(self, codigo):
        self.listawarnings.append(codigo)

    def print(self):
        print('')
        print(colored("LISTA DE ERRORES : ", 'magenta'))
        if len(self.listaerrores) == 0:
            print(colored(" - Vacía", 'green'))
        else:
            for e in range(len(self.listaerrores)-1) :
                print(colored("Error", 'red'), colored(self.listaerrores[e], 'red') ,colored(": ", 'red'), colored(self.errores.get(self.listaerrores[e]), 'red'))
                if type(self.listaerrores[e+1]) == Token:
                    print("- Linea : ", self.listaerrores[e+1].line)
                    print("- Posición :  ", self.listaerrores[e+1].start)
                    print("- Valor : ", self.listaerrores[e+1].value)
                elif self.listaerrores[e + 1] == None:
                    pass
                #else:
                    #print("- Linea : ", self.listaerrores[e + 1])
                e+= 1

        print('')

        print(colored("LISTA DE WARNINGS : ", 'magenta'))
        if len(self.listawarnings) == 0:
            print(colored(" - Vacía", 'green'))
        else:
            for e in range(len(self.listawarnings)):
                print(colored("Warning", 'red'), colored(self.listawarnings[e], 'red'), colored(": ", 'red'),
                      colored(self.warnings.get(self.listawarnings[e]), 'red'))

                e += 1

    def panicMode(self):
        self.print()
        exit()

