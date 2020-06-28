from sys import stdin, stdout

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
    def __init__(self,ei):
        self.producciones = []
        self.noterminales = set()
        self.tabla = []
        self.tas = {}
        self.estadoInicial = ei

    def cargar(self, text):
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

    def llenarEstaticamente(self):
        E = {'(':['T', 'Ep'],
            'num': ['T', 'Ep'],
             'id': ['T', 'Ep']}
        Ep = {'+': ['+', 'T', 'Ep'],
              '-': ['-', 'T', 'Ep'],
              ')': ['lambda'],
              '$': ['lambda']}
        T = {'(': ['F', 'Tp'],
             'num': ['F', 'Tp'],
             'id': ['F', 'Tp']}
        Tp = {'+': ['lambda'],
              '-': ['lambda'],
              '*': ['*', 'F', 'Tp'],
              '/': ['/', 'F', 'Tp'],
              ',': ['lambda'],
              '$': ['lambda']}

        F = {'(': ['(E)'],
             'num': ['num'],
             'id': ['id']}

        self.tabla.append(E)
        self.tabla.append(Ep)
        self.tabla.append(T)
        self.tabla.append(Tp)
        self.tabla.append(F)
        print(self.tabla.index(F))
        print(self.tabla)

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
            print(val)
            res = []
            primeros.append(self.getPrimero(val, res))
            print(res)

    def nodoDer(self, node, list):
        for p in self.producciones:
            if node in p.der:
                list.append(p)

    def getSiguiente(self, node, list, res):
        #print("Nodo: ",node)
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
            print(val)
            listap = []
            self.nodoDer(val,listap)
            #for i in range(0,len(listap)):
            #    listap[i].print()
            res = ['$']
            self.getSiguiente(val,listap, res)
            print(res)
        """
        listap = []
        self.nodoDer('T', listap)
        res = ['$']
        self.getSiguiente('T', listap, res)
        print(res)
        """

    def buscarProduccion(self, nnoterminal, nterminal):
        newproducciones = self.getProduccion(nnoterminal)

        print("NO TERMINAL: ", nnoterminal)
        print("TERMINAL : ", nterminal)
        print(newproducciones)
        tam = len(newproducciones)
        if tam == 1:
            return newproducciones[0]
        else:
            for j in range(0,len(newproducciones)):
                if nterminal in newproducciones[j]:
                    return newproducciones[j]


    def crearTabla(self):
        for nodoNt in self.noterminales:
            primeros = []
            self.getPrimero(nodoNt, primeros)
            result = []
            for nodoT in primeros:
                if nodoT != 'lambda':
                    result.append(nodoT)
                    result.append(self.buscarProduccion(nodoNt, nodoT))
                  #  if result[-1] == None:
                   #     result.append(self.buscarProduccion2(nodoNt, nodoT))
                    print("RESU: ", result)
                else:
                    siguientes = ['$']
                    lists = []
                    self.nodoDer(nodoNt, lists)
                    self.getSiguiente(nodoNt, lists, siguientes)
                    for nodoT2 in siguientes:
                        result.append(nodoT2)
                        result.append('lambda')
                self.tas[nodoNt] = result
        '''
        for i in self.tas:
            print(i)
            print(self.tas[i])
        '''


    def imprimirTabla(self):
        for key, value in self.tas.items():
            print("Key: ", key)
            print("Value: ", value)

    def findInTAS(self, exp, exp2):
        res_list = []
        #print("Buscar: ", exp , " ", exp2)
        for nt, val in self.tas.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
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
        print("Validando cadena: ")
        entrada = Queue()
        cadena2 = cadena.split(" ")
        for c in cadena2:
            entrada.enqueue(c)
        entrada.enqueue('$')
        #print(entrada.items)
        pila = ['$']
        pila.append(self.estadoInicial)



        while not entrada.isEmpty() and len(pila) > 0:
            print("Cola: ", entrada.items)
            print('Pila: ', pila)
            if entrada.items[-1] == pila[-1]:
                entrada.dequeue()
                pila.pop()
            else:
                aux = pila.pop()
                res = self.findInTAS(aux,entrada.items[-1])
                tam = len(res)
                res = res[::-1]
                for i in range(tam):
                    if(res[i] != 'lambda'):
                        pila.append(res[i])

            var = 0
            if len(pila) == 0:
                var = 1
        #print("Cola: ", entrada.items)
        #print('Pila: ', pila)

        if entrada.isEmpty() and var:
            print("Válida")
        else:
            print("No válida")


        return entrada.isEmpty() and var

class Nodo:
    def __init__(self):
        self.val = ''
        self.hijos = list()
        self.padre = None
        self.siguiente = None

    def print(self):
        print('Valor: ', self.val)
        print('- Hijos: ',len(self.hijos))
        print('- Padre')
        if(self.padre == None):
            print("- Raiz")
        else:
            self.padre.print()

class ArbolSintactico:
    def __init__(self, gramatica):
        self.root = 0
        self.g = gramatica

    def op1(self, pivote, literales):
        nodes = list()
        for i in range(len(literales)):
            child = Nodo()
            child.val = literales[i]
            child.padre = pivote
            nodes.append(child)
        tam = len(nodes)

        nnodes = list(reversed(nodes))
        for i in range(tam):
            if i < tam-1:
                #print("Valor : ")
                #print(nnodes[i].val)
                nnodes[i].siguiente = nnodes[i+1]
                #print("Siguiente: ")
                #print(nodes[i].siguiente.val)

        nodes = list(reversed(nnodes))
        pivote.hijos = nodes



        return pivote


    def op2(self, pivote):
        if pivote == 0 or pivote is None:
            return None
        if pivote.siguiente is not None:
            return pivote.siguiente
        if pivote.padre is not None:
            return self.op2(pivote.padre)
        return None

    def op3(self, pivote):
        pivote.hijos.append('lambda')
        return self.op2(pivote.padre)

    def crearArbol(self, input):
        entrada = Queue()
        cadena2 = input.split(" ")
        for c in cadena2:
            entrada.enqueue(c)
        entrada.enqueue('$')
        pila = ['$']
        pila.append(g.estadoInicial)
        node1 = Nodo()
        node1.val = g.estadoInicial
        node1.padre = 0
        curr_node = node1

        while not entrada.isEmpty() and len(pila) > 0:
            print("Cola: ", entrada.items)
            print('Pila: ', pila)

            if entrada.items[-1] == pila[-1]:
                entrada.dequeue()
                pila.pop()
                if curr_node == 0:
                    break
                curr_node = self.op2(curr_node)
            else:
                aux = pila.pop()
                res = g.findInTAS(aux,entrada.items[-1])
                tam = len(res)
                res = res[::-1]
                literales = list()
                flag = False
                flag2 = False
                print("NODO: ", curr_node.val)
                for i in range(tam):
                    print(res[i])
                    if(res[i] != 'lambda'):
                        flag = True
                        pila.append(res[i])
                        literales.append(res[i])
                    else:
                        print("Operacion 3")
                        curr_node = self.op3(curr_node)

                if flag:
                    print("Operacion 1")
                    curr_node = self.op1(curr_node, literales)


                    curr_node = curr_node.hijos[-1]



            var = 0
            if len(pila) == 0:
                var = 1
        #print("Cola: ", entrada.items)
        #print('Pila: ', pila)

        if entrada.isEmpty() and var:
            print("Válida")
        else:
            print("No válida")

        return entrada.isEmpty() and var





lines = int(input("Ingrese la cantidad de líneas: "))
grammar_input = []
for i in range(lines):
    grammar_input.append(stdin.readline())

g = Gramatica('if_stmt')
#g = Gramatica('if_stmt')
if g.cargar(grammar_input):
    print("La gramática se cargó exitosamente")
else:
    print("No se pudo cargar la gramática")
#g.getProducciones()
#g.getProduccion("T")
#g.getPrimeros()
g.crearTabla()
print(" ")


#a = ArbolSintactico(g)
#a.crearArbol("id + id * id")
#print(g.tas.keys())
g.imprimirTabla()
#print(g.validarCadena("id + id * id"))
print(g.validarCadena("if ( cond1 ) { num + num ; } else { num - num ; }"))
#print(g.validarCadena("num + num ;"))

''' Ejemplo de la entrada del programa
7
E := T Ep
Ep := + T Ep
Ep := - T Ep
Ep := lambda
T := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F := ( E ) | num | id


5
E := T Ep
Ep := + T Ep | lambda
T := F Tp
Tp := * F Tp  | lambda
F := ( E ) | id

5
if_stmt := if ( cond ) { expr ; } opt_elif opt_else
opt_elif := elif ( cond ) { expr ; } opt_elif 
opt_elif := lambda
opt_else := else { expr ; } 
opt_else := lambda
cond := cond1
expr := a + b

16
if_stmt := if ( cond ) { expr ; } opt_elif opt_else
opt_elif := elif ( cond ) { expr ; } opt_elif 
opt_elif := lambda
opt_else := else { expr ; }
opt_else := lambda
cond := cond1
expr := ar_oper
ar_oper := exp2 expp
expp := + exp2 expp
expp := - exp2 expp
expp := lambda
exp2 := exp3 exp2p
exp2p := * exp3 exp2p
exp2p := / exp3 exp2p
exp2p := lambda
exp3 := num | ( ar_oper )

'''

