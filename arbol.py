from tabla import *
from prettytable import PrettyTable


def insert_array(array):
    ret_str = ''
    for value in array:
        ret_str += (value + ' ')

    return ret_str


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
        header = ['Pila', 'Entrada', 'Operacion', 'Agregar']
        self.t = PrettyTable(header)
        self.elem = list()

    def op1(self, pivote, literales, tabla):

        if pivote :
            tabla.append('1')
            tabla.append(literales)
            self.elem.append(tabla)

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
                    nnodes[i].siguiente = nnodes[i+1]

            nodes = list(reversed(nnodes))
            pivote.hijos = nodes

            return pivote


    def op2(self, pivote, tabla):

        if pivote == 0 or pivote is None:
            return None
        if pivote.siguiente is not None:
            if 'lambda' not in tabla[0]:
                ntabla = tabla
                ntabla.append('2')
                ntabla.append('')
                self.elem.append(ntabla)
            return pivote.siguiente
        if pivote.padre is not None:

            return self.op2(pivote.padre, tabla)
        return None

    def op3(self, pivote, tabla):
        ntabla = list()
        if pivote :
            ntabla = tabla

            ntabla.append('3')
            ntabla.append('lambda')

            self.elem.append(ntabla)
            pivote.hijos.append('lambda')

            return self.op2(pivote.padre, tabla[0:-2])


    def crearArbol(self, cadena):
        print("Creando árbol: ")
        tokens = Queue()
        entrada = Queue()

        for c in cadena:
            if c.grammar_val != 'end':
                tokens.enqueue(c)
                entrada.enqueue(c.grammar_val)
        entrada.enqueue('$')
        tokens.enqueue('$')
        pila = ['$']
        pila.append(self.g.estadoInicial)
        node1 = Nodo()
        node1.val = self.g.estadoInicial
        node1.padre = 0
        curr_node = node1
        self.root = node1

        list2 = list()
        list2.append(insert_array(pila))
        list2.append(insert_array(entrada.items))
        list2.append('')
        list2.append('')
        self.elem.append(list2)
        token_ant = 0

        while not entrada.isEmpty() and len(pila) > 0:
            #print("Cola: ", entrada.items)
            #print('Pila: ', pila)
            n_list = list()

            n_list.append(insert_array(pila))
            n_list.append(insert_array(entrada.items))

            if entrada.items[-1] == pila[-1]:
                token_ant = tokens.items[-1]
                entrada.dequeue()
                tokens.dequeue()
                pila.pop()
                n_list[0] = insert_array(pila)
                n_list[1] = insert_array(entrada.items)
                if curr_node == 0:
                    break
                curr_node = self.op2(curr_node,n_list)
            else:
                if pila[-1] == 'lambda':
                    pila.pop()
                res = self.g.findInTAS(pila[-1],entrada.items[-1])
                tam = len(res)

                if tam > 0 :
                    pila.pop()
                    res = res[::-1]
                    literales = list()
                    flag = False
                    flag2 = False

                    for i in range(tam):
                        if(res[i] != 'lambda'):

                            flag = True
                            pila.append(res[i])
                            literales.append(res[i])
                            n_list[0] = insert_array(pila)
                            n_list[1] = insert_array(entrada.items)

                        else:


                            n_list[0] = insert_array(pila)
                            curr_node = self.op3(curr_node, n_list)


                    if flag:


                        if curr_node :
                            curr_node = self.op1(curr_node, literales, n_list)

                            curr_node = curr_node.hijos[-1]
                else:
                    if len(pila) > 1:
                        newT = token_ant
                        print(tokens.items[-1])
                        self.g.log.addError('3', newT)
                        self.g.log.panicMode()
                    else:
                        self.g.log.addError('2', tokens.items[-1])
                        self.g.log.panicMode()
                    break



        if len(pila) == 1 and len(entrada.items) == 1:
            if pila[0] == '$' and entrada.items[0] == '$':
                n_list = list()

                entrada.dequeue()
                pila.pop()

        var = 0
        if len(pila) == 0:
            var = 1

        if entrada.isEmpty() and var:
            print(colored("Válida", 'green'))

        else:
            print(colored("No válida", 'red'))

        return entrada.isEmpty() and var

    def imprimirArbol(self):
        print("IMPRIMIENDO ÁRBOL: ")
        for e in self.elem:
            self.t.add_row(e)

        print(self.t)
