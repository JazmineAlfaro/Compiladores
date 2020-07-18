from sys import stdin, stdout
from token import *
from prettytable import PrettyTable
from termcolor import colored

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Produccion:
    izq = ""
    der = []

    def __init__(self, izq, der):
        self.izq = izq
        self.der = der

    def print(self):
        print(self.izq, " -> " ,self.der)

class Gramatica:
    def __init__(self,ei, log1):
        self.producciones = []
        self.noterminales = set()
        self.tabla = []
        self.tas = {}
        self.estadoInicial = ei
        self.log = log1

    def cargar(self, text):
        print("CARGANDO GRAMÁTICA")
        for i in range(0, len(text) ):

            if '|' in text[i]:
                temp_prod = text[i].split('|')
                nter = ""
                for i in range(0, len(temp_prod) ):
                    aux = temp_prod[i].split()
                    if i == 0:
                        nter = aux[0]
                        self.producciones.append(Produccion(nter, aux[2:]))
                        self.noterminales.add(nter)
                    else:
                        self.producciones.append(Produccion(nter, aux))
                        self.noterminales.add(nter)
            else:
                temp_prod = text[i].split()

                if temp_prod[1] == ":=":
                    self.producciones.append(Produccion(temp_prod[0], temp_prod[2:]))
                    self.noterminales.add(temp_prod[0])

                else:
                    return 0
        return 1

    def getProducciones(self):
        for i in range(0, len(self.producciones)):
            self.producciones[i].print()

    def getProduccion(self, izq):
        res = []
        for i in range(0, len(self.producciones)):
            if self.producciones[i].izq == izq:
                res.append(self.producciones[i].der)
                #print(self.producciones[i].der)
        return res

    def getPrimero(self, node, res=[]):
        list = self.getProduccion(node)

        if len(list) == 1:
            if list[0][0] in self.noterminales:
                self.getPrimero(list[0][0], res)
            else:
                res.append(list[0][0])
        else:
            for i in range(0, len(list)):
                if list[i][0] in self.noterminales:
                    self.getPrimero(list[i][0], res)
                    break
                else:
                    res.append(list[i][0])


    def getPrimeros(self):
        for val in self.noterminales:
            primeros = []
            res = []
            primeros.append(self.getPrimero(val, res))


    def nodoDer(self, node, list):
        for p in self.producciones:
            if node in p.der:
                list.append(p)

    def getSiguiente(self, node, list, res):
        if node :
            for i in range(0,len(list)):
                tam = len(list[i].der)
                nodo = list[i].izq
                idx = list[i].der.index(node)

                if idx == tam-2:
                    if list[i].der[idx+1] not in self.noterminales:
                        res.append(list[i].der[idx+1])

                    else:
                        #print("Tercera regla")
                        auxprimeros = []
                        self.getPrimero(list[i].der[idx+1], auxprimeros)
                        #print ("Primeros de ", list[i].der[idx+1])
                        #print(auxprimeros)
                        if 'lambda' in auxprimeros:
                            idxlambda = auxprimeros.index('lambda')
                            auxprimeros.pop(idxlambda)
                            newnode = list[i].izq
                            newlist = []
                            self.nodoDer(newnode,newlist)
                            self.getSiguiente(newnode,newlist,auxprimeros)
                            res += auxprimeros
                            break
                        else:
                            res += auxprimeros
                            break
                elif idx == tam-1:
                    #print("Segunda regla")
                    auxlist = []
                    resList = []
                    self.nodoDer(nodo, auxlist)
                    self.getSiguiente(nodo,auxlist, resList)
                    res += resList
                    break




    def getSiguientes(self):

        for val in self.noterminales:

            listap = []
            self.nodoDer(val,listap)
            #for i in range(0,len(listap)):
            #    listap[i].print()
            res = ['$']
            self.getSiguiente(val,listap, res)


    def buscarProduccion(self, nnoterminal, nterminal):
        newproducciones = self.getProduccion(nnoterminal)

        tam = len(newproducciones)

        if tam == 1:
            return newproducciones[0]
        else:
            for j in range(0,len(newproducciones)):
                if nterminal in newproducciones[j]:
                    return newproducciones[j]


    def crearTabla(self):
        print("CREANDO TABLA : ")
        try:
            for nodoNt in self.noterminales:
                primeros = []
                self.getPrimero(nodoNt, primeros)
                result = []
                for nodoT in primeros:
                    if nodoT != 'lambda':
                        result.append(nodoT)
                        result.append(self.buscarProduccion(nodoNt, nodoT))

                    else:
                        siguientes = ['$']
                        lists = []
                        self.nodoDer(nodoNt, lists)

                        self.getSiguiente(nodoNt, lists, siguientes)


                        for nodoT2 in siguientes:
                            result.append(nodoT2)
                            result.append('lambda')
                    self.tas[nodoNt] = result
            print(colored("Se creó la tabla correctamente", 'green'))
        except:
            print(colored("No se pudo crear la tabla", 'red'))

    def imprimirTabla(self):
        print('')
        print("IMPRIMIENDO TAS :")
        terminales = set()
        for key, value in self.tas.items():
            for i in range(len(value)):
                if i%2 == 0:
                    terminales.add(value[i])

        header = list(terminales)
        header.insert(0, "No terminales")

        t = PrettyTable(header)

        for key, value in self.tas.items():
            nt = ['-'] * (len(header) -1)
            nt.insert(0, key)
            pos = 0
            for i in range(len(value)):
                if (i%2 == 0):
                    pos = header.index(value[i])

                else:
                    nt[pos] = value[i]
            t.add_row(nt)

        print(t)

    def findInTAS(self, exp, exp2):
        res_list = []
        #print("Buscar: ", exp , " ", exp2)
        for nt, val in self.tas.items():
            if nt == exp:
                prod2 = val
                #print(val)
                for s in range(len(prod2)):
                    #print('S: ', s)
                    if prod2[s] == exp2:
                        res = prod2[s+1]
                        #print("RESULTADO: ", res)
                        #print("RESULTADO: ",type(res))
                        if type(res) == str:
                            #print("Entra")
                            res_list.append(res)
                        elif type(res) == list and len(res)==1:
                            #print("LISTA TAM !")
                            if type(res[0]) == list:
                                for i in range(len(res[0])):
                                    res_list.append(res[0][i])
                            elif type(res[0] == str):
                                res_list.append(res[0])
                        else:
                            for i in range(len(res)):
                                res_list.append(res[i])
        return(res_list)


    def validarCadena(self, cadena):
        print('')
        string = str()
        for c in cadena:
            if c.grammar_val != 'end':
                string += c.grammar_val + ' '

        print("VALIDANDO CADENA: ", colored(string, 'cyan'))
        tokens = Queue()
        entrada = Queue()
        for c in cadena:
            if c.grammar_val != 'end':
                tokens.enqueue(c)
                entrada.enqueue(c.grammar_val)
        entrada.enqueue('$')
        tokens.enqueue('$')
        #print(entrada.items)
        pila = ['$']
        pila.append(self.estadoInicial)
        token_ant = 0


        while not entrada.isEmpty() and len(pila) > 0:
            # PARA IMPRIMIR
           # print("Cola: ", entrada.items)
            #print('Pila: ', pila)

            if entrada.items[-1] == pila[-1]:
                token_ant = tokens.items[-1]
                entrada.dequeue()
                tokens.dequeue()
                pila.pop()
            else:
                res = self.findInTAS(pila[-1],entrada.items[-1])
                tam = len(res)
                if tam > 0:
                    pila.pop()
                    res = res[::-1]
                    for i in range(tam):
                        if(res[i] != 'lambda'):
                            pila.append(res[i])
                else:
                    break


            var = 0
            if len(pila) == 0:
                var = 1


        if entrada.isEmpty() and var:
            print(colored("Cadena válida", 'green'))
        else:

            print(colored("Cadena no válida", 'red'))


        return entrada.isEmpty() and var