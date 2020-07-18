from token import *

headers = ['#include <iostream>\n', 'using namespace std; \n']
main = 'int main() {\n'
close_main = 'return 0; } \n'

def printfun(array, t):
    array.append('cout<<')
    for pos in range(len(t)):
        if t[pos].value == 'end':
            break
        array.append(t[pos].value)
    array.append('<<endl;')


def translate(text):
    list_values = list()
    for t in text:
        for c in t:
            list_values.append(c.value)

    if 'main' in list_values:
        file = headers
        file.append(main)

        pos = list_values.index('main')
    else:
        file = headers
        file.append(main)
        for t in text:
            prev = 0
            for c in range (len(t)):
                if t[c].type == 'INT' or t[c].type == 'FLOAT':
                    file.append(str(t[c].value))
                elif t[c].type == 'ENDLINE':
                    if prev and (prev.value == '{' or prev.value == '}'):
                        pass
                    else:
                        file.append(';')
                elif t[c].grammar_val == 'elif':
                    file.append('else if')
                elif t[c].grammar_val == 'print':
                    printfun(file, t[c+1:])
                    break
                else:
                    file.append(t[c].value)
                file.append(' ')
                prev = t[c]
            file.append('\n')
        file.append(close_main)

        outFile = open("program.cpp", "w")
        for f in file:
            outFile.write(f)
        outFile.close()