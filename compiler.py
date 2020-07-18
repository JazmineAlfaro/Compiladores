from arbol import *
from lexer import Lexer
from error import *
from termcolor import colored
from source_to_source import *

de = DiccionarioError()
log1 = Log(de)
grammar_list = list()

def create_gramar(file, log, inicial, name):
    print(name)
    g = Gramatica(inicial, log)
    with open(file) as f:
        g1 = f.read().splitlines()
    if g.cargar(g1):
        print(colored("La gramática se cargó exitosamente", 'green'))
    else:
        print(colored("No se pudo cargar la gramática", 'red'))
    grammar_list.append(g)
    g.crearTabla()
    g.imprimirTabla()


create_gramar('grammar.txt', log1, 'program', colored('Gramática 1', 'blue'))
create_gramar('grammar2.txt', log1, 'program', colored('Gramática 2', 'blue'))
create_gramar('functions.txt', log1, 'program', colored('Gramática 3', 'blue'))

file1 = open('test.txt', 'r')
Lines = file1.readlines()
token_list1 = list()
all_tokens = list()
# Analizador Léxico
for t in Lines:
    linea = Lines.index(t)

    l = Lexer(t, log1, linea)

    if t == '}':

        pass
    print(colored("TOKENS: ", 'yellow'))
    token_list = l.generate_tokens()
    for tl1 in token_list :
        print(tl1)
    all_tokens.append(token_list)
    token_list1 += token_list

new_lexer = Lexer(token_list1, log1, 0)
new_lexer.verify_code()

for lt in all_tokens:
    flag = False
    for gs in grammar_list:
        if lt[0].value == '}':
            flag = True
            break
        elif gs.validarCadena(lt):
            flag = True
            gs.log.print()
            a = ArbolSintactico(gs)
            a.crearArbol(lt)
            a.imprimirArbol()
            break

    if not flag:
        print(colored("No se acepta en ninguna gramática", 'red'))
        exit()

print(colored("Código válido", 'green'))
translate(all_tokens)
print(colored('Código traducido', 'green'))