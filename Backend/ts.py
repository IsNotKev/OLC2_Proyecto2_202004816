from enum import Enum
from traceback import print_tb

class TIPO_DATO(Enum) :
    INT64 = 1
    FLOAT64 = 2
    BOOLEAN = 3
    STRING = 4
    ISTRING = 5
    CHAR = 6
    USIZE = 7
    VOID = 8
    VECTOR = 9
    ARRAY = 10

class TIPO_SIMBOLO(Enum):
    VAR = 1
    ARRAY = 2
    VECTOR = 3
    STRUCT = 4

class TIPO_VAR(Enum):
    MUTABLE = 1
    INMUTABLE = 2

class RetornoType:

    def __init__(self, tipo=TIPO_DATO.VOID, tipo2=TIPO_DATO.VOID, valor = None):
        self.codigo = ""
        self.etiqueta = ""
        self.temporal = ""
        self.tipo = tipo
        self.etiquetaV = ""
        self.etiquetaF = ""
        self.valor = valor
        self.tipo2 = tipo2

    def iniciarRetorno(self, codigo, etiqueta, temporal, tipo, valor = None, tipo2 = None):
        self.codigo = codigo
        self.temporal = temporal
        self.etiqueta = etiqueta
        self.tipo = tipo
        self.valor = valor
        self.tipo2 = tipo2

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo_var, tipo_dato,valor, direccionRelativa, capacity = None, isRef = False) :
        self.id = id
        self.tipo_var = tipo_var
        self.tipo_dato = tipo_dato
        self.valor = valor
        self.capacity = capacity
        self.direccionRelativa = direccionRelativa
        self.isRef = isRef

class Funcion():
    def __init__(self, id, parametros, instrucciones, tipo_dato, generada = False):
        self.id = id
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo_dato = tipo_dato
        self.generada = generada

class Struct():
    def __init__(self,id , parametros):
        self.id = id
        self.parametros = parametros

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}, funciones = {}, structs = {}) :
        self.simbolos = simbolos
        self.funciones = funciones
        self.structs = structs

    def obtenerStruct(self,id):
        if not id in self.structs :
            print('Error: struct ', id, ' no definida.')
            return None
        else:
            return self.structs[id]
    
    def asignarStructData(self, id, lid, nval):
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
            return None
        else:
            simboloAux = self.simbolos[id]
            for dat in simboloAux.valor.val:
                if dat.id == lid[0] and dat.dato.tipo == nval.tipo:
                    dat.dato = nval
                    self.simbolos[simboloAux.id] = simboloAux
                    return


    def obtenerStructData(self,id, lid):
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
            return None
        else:
            simbolo = self.simbolos[id]
            for dat in simbolo.valor.val:
                if dat.id == lid[0]:
                    if len(lid) > 1 :
                        return self.structDataRecursivo(dat.dato,lid)
                    else:
                        return dat.dato

    def structDataRecursivo(self, atributos, lid):
        lid.pop(0)
        for dat in atributos.val:
            if dat.id == lid[0]:
                if len(lid) > 1 :
                    return self.structDataRecursivo(dat.dato,lid)
                else:
                    return dat.dato



    def agregarStruct(self, struct):
        self.structs[struct.id] = struct

    def agregarSimbolo(self, simbolo) :
        if simbolo.valor != None:
            if simbolo.tipo_dato != TIPO_DATO.VOID:
                if simbolo.tipo_dato == simbolo.valor.tipo:        
                    self.simbolos[simbolo.id] = simbolo
                elif simbolo.tipo_dato == TIPO_DATO.USIZE and simbolo.valor.tipo == TIPO_DATO.INT64:
                    self.simbolos[simbolo.id] = simbolo
                else:                 
                    print('Error al asignar',simbolo.id, simbolo.valor.tipo, simbolo.tipo_dato)
                    return None
            else:
                simbolo.tipo_dato = simbolo.valor.tipo
                self.simbolos[simbolo.id] = simbolo

        else:
            self.simbolos[simbolo.id] = simbolo
        
        return self.simbolos[simbolo.id]
    
    def agregarFuncion(self, funcion):
        self.funciones[funcion.id] = funcion
    
    def obtenerFuncion(self, id):
        if not id in self.funciones :
            print('Error: funcion ', id, ' no definida.')
            return None
        else:
            return self.funciones[id]

    def existeFuncion(self,id):
        if not id in self.funciones :
            return False
        else:
            return True

    def sustituirFuncion (self,funcion):
        self.funciones[funcion.id] = funcion

    def obtenerSimbolo(self, id) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
            return None
        else:
            return self.simbolos[id]

    def obtenerSimboloV(self, id, ubicacion):
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else:
            if len(ubicacion) > 1:
                return self.simboloRecursivo((self.simbolos[id]).valor.val[ubicacion[0]] , ubicacion)
            else:
                return (self.simbolos[id]).valor.val[ubicacion[0]]  

    def simboloRecursivo(self,vec,ubicacion):
        if len(ubicacion) > 1:
            ubicacion.pop(0)
            return self.simboloRecursivo(vec.val[ubicacion[0]], ubicacion)
        else:
            return vec

    def capacity(self, id):
        simboloAux = self.obtenerSimbolo(id)
        if simboloAux.capacity != None:
            return simboloAux.capacity
        else:
            print('No tiene capacity')

    def push(self,id, dato):
        simboloAux = self.obtenerSimbolo(id)
        if type(simboloAux.valor.val) == type([]):
            simboloAux.valor.val.append(dato)
            self.simbolos[simboloAux.id] = simboloAux
        else:
            print('No es Vector para hacerle push')
    
    def remove(self,id, ubicacion):
        simboloAux = self.obtenerSimbolo(id)
        if type(simboloAux.valor.val) == type([]):
            aux = simboloAux.valor.val[ubicacion]
            simboloAux.valor.val.pop(ubicacion)
            self.simbolos[simboloAux.id] = simboloAux
            return aux
        else:
            print('No es Vector para hacerle remove')

    def insert(self,id,ubicacion,dato):
        simboloAux = self.obtenerSimbolo(id)
        if type(simboloAux.valor.val) == type([]):
            simboloAux.valor.val.insert(ubicacion,dato)
            self.simbolos[simboloAux.id] = simboloAux
        else:
            print('No es Vector para hacerle insert')

    def contains(self,id,dato):
        simboloAux = self.obtenerSimbolo(id)
        if type(simboloAux.valor.val) == type([]):
            for i in simboloAux.valor.val:
                if i.tipo == dato.tipo and i.val == dato.val:
                    return True
            return False
        else:
            print('No es Vector para hacerle push')

    def actualizarVec(self,id,ubicacion,nval):
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
        else :
            simboloAux = self.obtenerSimbolo(id)
            if len(ubicacion) > 1:
                u = ubicacion[0]
                simboloAux.valor.val[u] = self.resolv(simboloAux.valor.val[u], ubicacion, nval)
                self.simbolos[simboloAux.id] = simboloAux
            else:
                simboloAux.valor.val[ubicacion[0]]  = nval
                self.simbolos[simboloAux.id] = simboloAux
                     
    
    def resolv(self, val, ubicacion, nval):
        if len(ubicacion) > 1:
            ubicacion.pop(0)
            u = ubicacion[0]
            val.val[u] = self.resolv(val.val[u],ubicacion,nval)
            return val
        else:
            return nval
    

    def actualizarSimbolo(self, id, nval) :
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')
            return None
        else :
            simboloAux = self.obtenerSimbolo(id)
            if simboloAux.tipo_var == TIPO_VAR.MUTABLE:
                if nval.tipo == simboloAux.tipo_dato:
                    simboloAux.valor = nval               
                    self.simbolos[simboloAux.id] = simboloAux
                    return self.simbolos[simboloAux.id]
                elif simboloAux.tipo_dato == TIPO_DATO.USIZE and nval.tipo == TIPO_DATO.INT64:
                    simboloAux.valor = nval
                    self.simbolos[simboloAux.id] = simboloAux
                    return self.simbolos[simboloAux.id]
                else:
                    print('Error al asignar',id, nval.tipo)
                    return None
            else:
                print('No se puede actualizar una variable Inmutable')
                return None
    
    def obtenerTSimbolos(self):
        salida = {}

        cont = 0
        for clave in self.simbolos:
            aux = {}
            aux['id'] = self.simbolos[clave].id
            aux['tipo_dato'] = self.obtenerT(self.simbolos[clave].tipo_dato)
            aux['tipo_var'] = self.obtenerT(self.simbolos[clave].tipo_var)
            aux['entorno'] = "Main"
            salida['simbolo' + str(cont)] = aux
            cont += 1

        for funcion in self.funciones:
            aux = {}

            aux['id'] = self.funciones[funcion].id
            aux['tipo_dato'] = self.obtenerT(self.funciones[funcion].tipo_dato)
            aux['tipo_var'] = "Funci??n"
            aux['entorno'] = "Global"

            salida['simbolo' + str(cont)] = aux
            cont += 1

        return salida
    
    def obtenerT(self, tipo_dato):
        if tipo_dato == TIPO_DATO.ARRAY: return "Array"
        elif tipo_dato == TIPO_DATO.VECTOR: return "Vector"
        elif tipo_dato == TIPO_DATO.USIZE: return "Usize"
        elif tipo_dato == TIPO_DATO.INT64: return "I64"
        elif tipo_dato == TIPO_DATO.FLOAT64: return "F64"
        elif tipo_dato == TIPO_DATO.CHAR: return "Char"
        elif tipo_dato == TIPO_DATO.STRING: return "String"
        elif tipo_dato == TIPO_DATO.ISTRING: return "IString"
        elif tipo_dato == TIPO_DATO.BOOLEAN: return "Boolean"
        elif tipo_dato == TIPO_DATO.VOID: return "Void"
        elif tipo_dato == TIPO_VAR.MUTABLE: return "Variable Mutable"
        elif tipo_dato == TIPO_VAR.INMUTABLE: return "Variable Inmutable"
        else: return "Saber"