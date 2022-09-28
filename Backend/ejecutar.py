from ts import TIPO_VAR, Simbolo, TIPO_DATO, RetornoType
from expresiones import *
from instrucciones import *
import Generador3D as Gen3D
import ts as TS
import math
from Generador3D import Generador3D

def guardarFunciones(instrucciones, ts):
    if instrucciones != None:
        for instr in instrucciones:
            if isinstance(instr,Funcion): guardar_funcion(instr,ts) 
            #elif isinstance(instr, CrearStruct): guardar_struct(instr,ts)

def guardar_funcion(instr,ts):
    ts.agregarFuncion(instr)

def procesar_instrucciones(instr, ts, Generador3D) :
    if isinstance(instr, Imprimir) : return procesar_imprimir(instr, ts, Generador3D)

def procesar_imprimir(instr, ts, Generador3D):
    CODIGO_SALIDA = ""

    valorExpresion = resolverExpresion(instr.cad, ts, Generador3D)

    temp1 = Generador3D.obtenerTemporal()
    caracter = Generador3D.obtenerTemporal()
    etqCiclo = Generador3D.obtenerEtiqueta()
    etqSalida = Generador3D.obtenerEtiqueta()
    etqAuxiliar = Generador3D.obtenerEtiqueta()
    #etqAuxiliar2 = Generador3D.obtenerEtiqueta()

    CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR CADENA*/\n"
    CODIGO_SALIDA += valorExpresion.codigo
    CODIGO_SALIDA += f'{temp1} = {valorExpresion.temporal};\n'
    CODIGO_SALIDA += f'{etqCiclo}: \n'
    CODIGO_SALIDA += f'{caracter} = Heap[(int){temp1}];\n'

    #CODIGO_SALIDA += f'if({caracter} != 1 ) goto {etqAuxiliar};\n'
    #CODIGO_SALIDA += f'     {temp1} = {temp1} + 1;\n'
    #CODIGO_SALIDA += f'     {caracter} = Heap[(int){temp1}];\n'
    #CODIGO_SALIDA += f'     printf(\"%d\", (int){caracter}); \n'
    #CODIGO_SALIDA += f'     {temp1} = {temp1} + 1;\n'
    #CODIGO_SALIDA += f'     goto {etqCiclo}; \n'

    CODIGO_SALIDA += f'{etqAuxiliar}: \n'
    CODIGO_SALIDA += f'if({caracter} == 0) goto {etqSalida};\n' \
                     f'     printf(\"%c\",(int) {caracter});\n' \
                     f'     {temp1} = {temp1} + 1;\n' \
                     f'     goto {etqCiclo};\n'

    CODIGO_SALIDA += f'{etqSalida}:\n'
    CODIGO_SALIDA += f'printf(\"%c\",(int)10);\n'

    return CODIGO_SALIDA

def resolverExpresion(exp, ts, Generador3D):
    if isinstance(exp, ExpresionDobleComilla): return resolverCadena(exp, Generador3D)


def resolverCadena(exp, Generador3D):
    CODIGO_SALIDA = ""
    retorno = RetornoType()

    temp2 = Generador3D.obtenerTemporal()
    CODIGO_SALIDA += f'{temp2} = H;\n'

    for caracter in exp.val:
        valor = ord(caracter)
        CODIGO_SALIDA += f'Heap[H] ={valor};\n'
        CODIGO_SALIDA += f'H = H + 1;\n'

    CODIGO_SALIDA += f'Heap[H] = 0;\n'
    CODIGO_SALIDA += f'H = H+1;\n'

    retorno.iniciarRetorno(CODIGO_SALIDA, "", temp2, exp.tipo)
    return retorno

#def procesar_instrucciones(instrucciones, ts) :
#    ## lista de instrucciones recolectadas
#    consola = 'Ejecutando...'
#    if instrucciones != None:
#        for instr in instrucciones :
#            if isinstance(instr, Imprimir) : consola += procesar_imprimir(instr, ts)
#            elif isinstance(instr,Definicion): procesar_definicion(instr,ts)        
#            elif isinstance(instr,Asignacion): procesar_asignacion(instr,ts) 
#            elif isinstance(instr,Funcion): guardar_funcion(instr,ts)
#            elif isinstance(instr, CrearStruct): guardar_struct(instr,ts)
#            elif isinstance(instr, AsignacionStruct): 
#                nval = resolver_expresion(instr.exp,ts)
#                ts.asignarStructData(instr.id,instr.lid,nval)
#            elif isinstance(instr,Push): 
#                dd = resolver_expresion(instr.dato,ts)
#                ts.push(instr.id,dd)
#            elif isinstance(instr,Remove): 
#                dd = resolver_expresion(instr.dato,ts)
#                if dd.val >= 0:
#                    ts.remove(instr.id,dd.val) 
#            elif isinstance(instr,Insert): 
#                ub = resolver_expresion(instr.ubicacion,ts)
#                dato = resolver_expresion(instr.dato,ts)
#                if ub.val >= 0:
#                    ts.insert(instr.id,ub.val,dato)  
#            elif isinstance(instr,AsignacionVec): 
#                dat = resolver_expresion(instr.exp,ts)
#                dd = []
#                for n in instr.ubicacion:
#                    num = resolver_expresion(n,ts)
#                    if num.tipo == TIPO_DATO.INT64 and num.val >= 0:
#                        dd.append(num.val)
#                    else:
#                        print('Error: Necesita un entero positivo')
#                ts.actualizarVec(instr.id,dd,dat)  
#            elif isinstance(instr, If):                                                             
#                res = procesar_if(instr,ts)
#                consola += res['consola']
#                if res['break'].br or res['continue'].br or res['return'].br:
#                    return {'consola': consola,'break': res['break'], 'continue':res['continue'], 'return':res['return']}
#            elif isinstance(instr,IfElse):                                                   # Ya
#                res = procesar_ifelse(instr,ts)
#                consola += res['consola']
#                if res['break'].br or res['continue'].br or res['return'].br:
#                    return {'consola': consola,'break': res['break'], 'continue':res['continue'], 'return':res['return']}
#            elif isinstance(instr,While): 
#                res = procesar_while(instr,ts) 
#                consola += res['consola']
#                if res['return'].br:
#                    return {'consola': consola,'break': res['break'], 'continue':res['continue'], 'return':res['return']}                                                     
#            elif isinstance(instr,Llamado):
#                res = procesar_llamado(instr,ts)
#                consola += res['consola']                 
#            elif isinstance(instr,Match):                                                           
#                res = procesar_match(instr,ts)
#                consola += res['consola']
#                if res['break'].br or res['continue'].br or res['return'].br:
#                    return {'consola': consola,'break': res['break'], 'continue':res['continue'], 'return':res['return']}
#            elif isinstance(instr,ForIn): 
#                res = procesar_for(instr,ts)
#                consola += res['consola']
#                if res['return'].br:
#                    return {'consola': consola,'break': res['break'], 'continue':res['continue'], 'return':res['return']}  
#            elif isinstance(instr,Loop): 
#                res = procesar_loop(instr,ts)
#                consola += res['consola']
#                if res['return'].br:
#                    return {'consola': consola,'break': res['break'], 'continue':res['continue'], 'return':res['return']}  
#            elif isinstance(instr,Break): return {'consola': consola, 'break': instr, 'continue' : Continue(False), 'return': Return(False)}
#            elif isinstance(instr,Continue): return {'consola': consola,'break': Break(False), 'continue' : Continue(True), 'return': Return(False)}
#            elif isinstance(instr, Return):
#                exp = resolver_expresion(instr.data,ts) 
#                return {'consola': consola,'break': Break(False), 'continue' : Continue(False), 'return': Return(True,exp)}
#
#    return {'consola': consola, 'break':Break(False), 'continue' : Continue(False), 'return': Return(False)}
#
#def procesar_for(instr,ts):
#    ts_local = TS.TablaDeSimbolos(ts.simbolos, ts.funciones)
#    rango = resolver_expresion(instr.rango,ts)
#    consolaaux = ""
#    if isinstance(rango, ExpresionVec) or isinstance(rango, ExpresionArray):
#        for exp in rango.val:
#            simbolo = TS.Simbolo(instr.id,TIPO_VAR.INMUTABLE,TIPO_DATO.VOID,resolver_expresion(exp,ts_local))
#            ts_local.agregarSimbolo(simbolo)
#
#            res = procesar_instrucciones(instr.instrucciones, ts_local)      
#            consolaaux += res['consola'][13:]
#
#            if res['break'].br or res['return'].br:
#                return {'consola': consolaaux,'break': Break(False), 'continue' : Continue(False), 'return': res['return']}
#
#        return {'consola': consolaaux,'break': Break(False), 'continue' : Continue(False), 'return': Return(False)}
#    else:
#        return "Error -> Rango no permintido en for"
#
#def procesar_loop(instr,ts):
#    ts_local = TS.TablaDeSimbolos(ts.simbolos, ts.funciones)
#    consolaaux = ""
#    while True:
#        res = procesar_instrucciones(instr.instrucciones, ts_local)      
#        consolaaux += res['consola'][13:]
#
#        if res['break'].br or res['return'].br:
#            return {'consola': consolaaux,'break': Break(False), 'continue' : Continue(False), 'return': res['return']}
#
#def procesar_match(instr,ts):
#    val = resolver_expresion(instr.exp,ts)
#    for opcion in instr.opciones:
#        if opcion.coincidencias == TIPO_DATO.VOID:
#            res = procesar_instrucciones(opcion.instrucciones,ts)
#            return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'], 'return':res['return']}
#        else:
#            for coincidencia in opcion.coincidencias:
#                cc = resolver_expresion(coincidencia,ts)
#                if val.tipo == cc.tipo and val.val == cc.val:
#                    res = procesar_instrucciones(opcion.instrucciones,ts)
#                    return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'], 'return':res['return']}
#    
#    return {'consola': '', 'break':Break(False), 'continue' : Continue(False) , 'return':Return(False)}
#
#def procesar_llamado(instr,ts):
#    funcion = ts.obtenerFuncion(instr.id)
#
#    ts_local = TS.TablaDeSimbolos(simbolos={},funciones=ts.funciones, structs=ts.structs)
#
#    if len(instr.parametros) == len(funcion.parametros):
#        imut = []
#        for num in range(len(funcion.parametros)):
#            if isinstance(instr.parametros[num],ParI):
#                val = resolver_expresion(instr.parametros[num].par, ts)
#                imut.append([instr.parametros[num].par.id,funcion.parametros[num].id])
#            else:
#                val = resolver_expresion(instr.parametros[num], ts)
#            nsimbolo = Simbolo(funcion.parametros[num].id,funcion.parametros[num].tipo_var, funcion.parametros[num].tipo_dato,val)
#            ts_local.agregarSimbolo(nsimbolo)
#
#        res = procesar_instrucciones(funcion.instrucciones,ts_local)
#
#        for n in imut:
#            procesar_asignacion(Asignacion(n[0],resolver_expresion(ExpresionIdentificador(n[1]),ts_local)),ts)
#
#        return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'] , 'return': res['return']}
#    else:
#        print("Error en cantidad de Parametros")
#        return "Error en cantidad de Parametros"
#
#def guardar_funcion(instr,ts):
#    ts.agregarFuncion(instr)
#
#def guardar_struct(instr,ts):
#    nuevoS = TS.Struct(instr.id,instr.parametros)
#    ts.agregarStruct(nuevoS)
#
#def procesar_while(instr, ts):
#    val = resolver_expresion(instr.exp, ts)
#    if val.tipo == TIPO_DATO.BOOLEAN:
#        ts_local = TS.TablaDeSimbolos(ts.simbolos, ts.funciones)
#        consolaaux = ""
#        while resolver_expresion(instr.exp, ts_local).val :  
#            res = procesar_instrucciones(instr.instrucciones, ts_local)      
#            consolaaux += res['consola'][13:]
#
#            if res['break'].br or res['return'].br:
#                return {'consola': consolaaux,'break': Break(False), 'continue' : Continue(False), 'return': res['return']}
#        
#        return {'consola': consolaaux,'break': Break(False), 'continue' : Continue(False), 'return': Return(False)}
#    else:
#        return "Error -> While necesita un bool"
#
#def procesar_ifelse(instr, ts):
#    val = resolver_expresion(instr.exp, ts)
#    if val.tipo == TIPO_DATO.BOOLEAN:
#        if val.val:
#            ts_local = TS.TablaDeSimbolos(ts.simbolos, ts.funciones)
#            res = procesar_instrucciones(instr.instrIfVerdadero, ts_local)
#            return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'], 'return': res['return']}
#        else:
#            if isinstance(instr.instrIfFalso, If) or isinstance(instr.instrIfFalso, IfElse):
#                ts_local = TS.TablaDeSimbolos(ts.simbolos)
#                res = procesar_instrucciones([instr.instrIfFalso], ts_local)
#                return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'], 'return': res['return']}
#            else:
#                ts_local = TS.TablaDeSimbolos(ts.simbolos)
#                res = procesar_instrucciones(instr.instrIfFalso, ts_local)
#                return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'], 'return': res['return']}
#    else:
#        return "Error -> Debe de ser expresion booleana"
#
#def procesar_if(instr, ts):
#    val = resolver_expresion(instr.exp, ts)
#    if val.tipo == TIPO_DATO.BOOLEAN:
#        if val.val:
#            ts_local = TS.TablaDeSimbolos(ts.simbolos, ts.funciones)
#            res = procesar_instrucciones(instr.instrucciones, ts_local)
#            return {'consola': res['consola'][13:], 'break':res['break'], 'continue':res['continue'] , 'return': res['return']}
#        else:
#            return {'consola': '', 'break':Break(False), 'continue': Continue(False), 'return': Break(False)}
#    else:
#        return "Error -> Debe de ser expresion booleana"
#
#def procesar_imprimir(instr, ts) :
#    if(len(instr.parametros)==0):
#        cadena = resolver_expresion(instr.cad, ts).val
#        if type(cadena) == type('string'):
#            cadena = cadena.replace('\\n','\n')
#        return '\n> ' + cadena
#    else:
#        cadena = resolver_expresion(instr.cad, ts).val
#        cadena = cadena.replace('\\n','\n')
#        cad_aux = ""
#        error = False
#        for param in instr.parametros:
#            aux = resolver_expresion(param, ts)
#            aux = to_text(aux,ts)
#
#            escribir = True
#            primero = False
#            for c in cadena:
#                if(escribir):
#                    if(c == "{" and not primero):
#                        escribir = False
#                    else:
#                        cad_aux += c
#                else:
#                    if(c == "}"):
#                        escribir = True
#                        primero = True
#                        cad_aux = cad_aux + aux
#                    elif(c == "{"):
#                        escribir = True
#                        cad_aux = cad_aux + "{{"
#                        error = False
#                        primero = False
#                    elif(c != " "):
#                        error = True
#                        cad_aux = "> Error dentro de {}"
#                        break
#
#            cadena = cad_aux
#            cad_aux = ""    
#
#            if(error):
#                break
#
#        return '\n> ' + cadena
#
#def resolver_expresion(exp, ts):
#    if isinstance(exp, ExpresionRelacionalBinaria):
#        exp1 = resolver_expresion(exp.exp1, ts)
#        exp2 = resolver_expresion(exp.exp2, ts)
#        if(exp1.tipo == exp2.tipo):
#            if exp.operador == OPERACION_LOGICA.MAYOR_QUE : return ExpresionLogicaTF(exp1.val > exp2.val, TIPO_DATO.BOOLEAN)
#            if exp.operador == OPERACION_LOGICA.MENOR_QUE : return ExpresionLogicaTF(exp1.val < exp2.val, TIPO_DATO.BOOLEAN)
#            if exp.operador == OPERACION_LOGICA.IGUAL : return ExpresionLogicaTF(exp1.val == exp2.val, TIPO_DATO.BOOLEAN)
#            if exp.operador == OPERACION_LOGICA.DIFERENTE : return ExpresionLogicaTF(exp1.val != exp2.val, TIPO_DATO.BOOLEAN)
#            if exp.operador == OPERACION_LOGICA.MAYORIGUAL : return ExpresionLogicaTF(exp1.val >= exp2.val, TIPO_DATO.BOOLEAN)
#            if exp.operador == OPERACION_LOGICA.MENORIGUAL : return ExpresionLogicaTF(exp1.val <= exp2.val, TIPO_DATO.BOOLEAN)
#        else:
#            return ExpresionDobleComilla("Error -> No son del mismo tipo", TIPO_DATO.STRING)
#    elif isinstance(exp, ExpresionLogicaBinaria):
#        exp1 = resolver_expresion(exp.exp1, ts)
#        exp2 = resolver_expresion(exp.exp2, ts)
#        if(exp1.tipo == TIPO_DATO.BOOLEAN and exp2.tipo == TIPO_DATO.BOOLEAN):
#            if exp.operador == OPERACION_LOGICA.OR : return ExpresionLogicaTF(exp1.val or exp2.val, TIPO_DATO.BOOLEAN)
#            if exp.operador == OPERACION_LOGICA.AND : return ExpresionLogicaTF(exp1.val and exp2.val, TIPO_DATO.BOOLEAN)
#        else:
#            return ExpresionDobleComilla("Error -> No son del tipo boolean", TIPO_DATO.STRING)
#    elif isinstance(exp, ExpresionNot):
#        exp1 = resolver_expresion(exp.exp, ts)
#        if(exp1.tipo == TIPO_DATO.BOOLEAN):
#            return ExpresionLogicaTF(not exp1.val, TIPO_DATO.BOOLEAN)
#        else:
#            return ExpresionDobleComilla("Error -> No son de tipo boolean", TIPO_DATO.STRING)
#    elif isinstance(exp, ExpresionBinaria) :
#        
#        exp1 = resolver_expresion(exp.exp1, ts)
#        exp2 = resolver_expresion(exp.exp2, ts)
#
#        if((exp1.tipo == TIPO_DATO.INT64 and exp2.tipo == TIPO_DATO.INT64 ) or (exp1.tipo == TIPO_DATO.FLOAT64 and exp2.tipo == TIPO_DATO.FLOAT64 )):
#            if exp.operador == OPERACION_ARITMETICA.MAS : return ExpresionNumero(exp1.val + exp2.val,exp1.tipo)
#            if exp.operador == OPERACION_ARITMETICA.MENOS : return ExpresionNumero(exp1.val - exp2.val,exp1.tipo)
#            if exp.operador == OPERACION_ARITMETICA.POR : return ExpresionNumero(exp1.val * exp2.val,exp1.tipo)
#            if exp.operador == OPERACION_ARITMETICA.DIVIDIDO : 
#                if exp1.tipo == TIPO_DATO.INT64 :
#                    return ExpresionNumero(math.trunc(exp1.val / exp2.val),exp1.tipo)
#                else:
#                    return ExpresionNumero(exp1.val / exp2.val,exp1.tipo)
#            if exp.operador == OPERACION_ARITMETICA.MODULO : return ExpresionNumero(exp1.val % exp2.val,exp1.tipo)  
#        elif exp1.tipo == TIPO_DATO.STRING and exp2.tipo == TIPO_DATO.ISTRING:
#            return ExpresionDobleComilla(exp1.val + exp2.val,TIPO_DATO.STRING)
#        else:
#            print(exp1.tipo,exp2.tipo)
#            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
#        
#    elif isinstance(exp, ExpresionPotencia) :
#        exp1 = resolver_expresion(exp.exp1, ts)
#        exp2 = resolver_expresion(exp.exp2, ts)
#
#        if((exp1.tipo == TIPO_DATO.INT64 and exp2.tipo == TIPO_DATO.INT64 ) or (exp1.tipo == TIPO_DATO.FLOAT64 and exp2.tipo == TIPO_DATO.FLOAT64 )):
#            if(exp1.tipo == exp.tipo):
#                return ExpresionNumero(exp1.val ** exp2.val, exp.tipo)
#            else:
#                return ExpresionDobleComilla("Error -> No es del tipo correcto", TIPO_DATO.STRING)
#        else:
#            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
#                  
#    elif isinstance(exp, ExpresionNegativo) :
#        exp = resolver_expresion(exp.exp, ts)
#        if(exp.tipo == TIPO_DATO.INT64 or exp.tipo == TIPO_DATO.FLOAT64):
#            return ExpresionNumero(exp.val*-1,exp.tipo)
#        else:
#            return ExpresionDobleComilla("Error -> No se puede operar", TIPO_DATO.STRING)
#    elif isinstance(exp, ExpresionIf):
#        cond = resolver_expresion(exp.exp,ts)
#        if cond.tipo == TIPO_DATO.BOOLEAN:
#            if cond.val:
#                return resolver_expresion(exp.instrIfVerdadero,ts)
#            else:
#                return resolver_expresion(exp.instrIfFalso,ts)
#        else:
#            return ExpresionDobleComilla("Error -> Expresion If Necesita boolean", TIPO_DATO.STRING)
#    elif isinstance(exp, ExpresionMatch):
#        val = resolver_expresion(exp.exp,ts)
#        for opcion in exp.opciones:
#            if opcion.coincidencias == TIPO_DATO.VOID:
#                return resolver_expresion(opcion.instrucciones,ts)
#            else:
#                for coincidencia in opcion.coincidencias:
#                    cc = resolver_expresion(coincidencia,ts)
#                    if cc.tipo == val.tipo and cc.val == val.val:
#                        return resolver_expresion(opcion.instrucciones,ts)
#        
#        print("No hay coincidencias")
#        return ExpresionDobleComilla("No hay coincidencias", TIPO_DATO.STRING)
#    elif isinstance(exp, ExpresionLoop):
#        ts_local = TS.TablaDeSimbolos(ts.simbolos, ts.funciones)
#        while True:
#            res = procesar_instrucciones(exp.intrucciones, ts_local)
#            if res['break'].br:
#                return resolver_expresion(res['break'].data,ts_local)
#    elif isinstance(exp,ToString):
#        val = resolver_expresion(exp.dato,ts)
#        return ExpresionDobleComilla(to_text(val,ts),TIPO_DATO.STRING)
#    elif isinstance(exp,Abs):
#        val = resolver_expresion(exp.dato,ts)
#        if val.tipo == TIPO_DATO.INT64 or val.tipo == TIPO_DATO.FLOAT64:
#            return ExpresionNumero(abs(val.val), val.tipo)
#        else:
#            return ExpresionDobleComilla("No se puede realizar la funcion abs.", TIPO_DATO.STRING)
#    elif isinstance(exp,Sqrt):
#        val = resolver_expresion(exp.dato,ts)
#        if val.tipo == TIPO_DATO.INT64 or val.tipo == TIPO_DATO.FLOAT64:
#            return ExpresionNumero(math.sqrt(val.val), TIPO_DATO.FLOAT64)
#        else:
#            return ExpresionDobleComilla("No se puede realizar la funcion sqrt.", TIPO_DATO.STRING)
#    elif isinstance(exp, Casteo):         
#        return casteo(exp,ts)
#    elif isinstance(exp,ExpresionRango):
#        inicio = resolver_expresion(exp.inicio,ts)
#        fin = resolver_expresion(exp.fin,ts)
#        if inicio.tipo == TIPO_DATO.INT64 and fin.tipo == TIPO_DATO.INT64:
#            vec = []
#            for i in range(inicio.val,fin.val):
#                vec.append(ExpresionNumero(i,TIPO_DATO.INT64))
#            
#            return ExpresionVec(vec,TIPO_DATO.VOID)
#        else:
#            print("Error -> Tipo incorrecto en rango")
#    elif isinstance(exp, Llamado):
#        res = procesar_llamado(exp,ts)
#        return res['return'].data
#    elif isinstance(exp, ExpresionNumero) or isinstance(exp, ExpresionLogicaTF) or isinstance(exp, ExpresionDobleComilla) or isinstance(exp,ExpresionCaracter):
#        return exp
#    elif isinstance(exp,ExpresionArray):
#        dato = []   
#        if type(exp.val) == type([]):
#            for i in exp.val:
#                dato.append(resolver_expresion(i,ts))
#        elif isinstance(exp.val,ValoresRepetidos):
#            cant = resolver_expresion(exp.val.cant,ts)
#            if cant.tipo == TIPO_DATO.INT64:
#                val = []
#                dato = resolver_expresion(exp.val.dato,ts)
#                for i in range(0,cant.val):
#                    val.append(dato)
#                return ExpresionArray(val, TIPO_DATO.VOID)
#        else:
#            dato.append(resolver_expresion(exp.val,ts))
#        return ExpresionArray(dato,TIPO_DATO.VOID)
#    elif isinstance(exp, ExpresionIdentificador) :
#        return ts.obtenerSimbolo(exp.id).valor
#    elif isinstance(exp,ExpresionVec):
#        dato = []   
#        if type(exp.val) == type([]):
#            for i in exp.val:
#                dato.append(resolver_expresion(i,ts))
#        elif isinstance(exp.val,ValoresRepetidos):
#            cant = resolver_expresion(exp.val.cant,ts)
#            if cant.tipo == TIPO_DATO.INT64:
#                val = []
#                dato = resolver_expresion(exp.val.dato,ts)
#                for i in range(0,cant.val):
#                    val.append(dato)
#                return ExpresionVec(val, TIPO_DATO.VOID,resolver_expresion(exp.capacity,ts))
#        else:
#            dato.append(resolver_expresion(exp.val,ts))
#        return ExpresionVec(dato,TIPO_DATO.VOID,resolver_expresion(exp.capacity,ts))
#    elif isinstance(exp,Len):
#        val = resolver_expresion(exp.dato,ts)
#        return ExpresionNumero(len(val.val),TIPO_DATO.INT64)
#    elif isinstance(exp,ExpresionIdVectorial):
#        dd = []
#        for n in exp.ubicacion:
#            num = resolver_expresion(n,ts)
#            if num.tipo == TIPO_DATO.INT64 and num.val >= 0:
#                dd.append(num.val)
#            else:
#                dd.append(0)
#                print('Error: Necesita un entero positivo')
#        return ts.obtenerSimboloV(exp.id, dd)
#    elif isinstance(exp,Remove):
#        dd = resolver_expresion(exp.dato,ts)
#        if dd.val >= 0:
#            return ts.remove(exp.id,dd.val) 
#    elif isinstance(exp,Contains):
#        dd = resolver_expresion(exp.dato,ts)
#        return ExpresionLogicaTF(ts.contains(exp.id,dd),TIPO_DATO.BOOLEAN )
#    elif isinstance(exp,Capacity):
#        return ExpresionNumero(ts.capacity(exp.id),TIPO_DATO.INT64 )
#    elif isinstance(exp,ExpresionStruct):
#        refStruct = ts.obtenerStruct(exp.tipo)
#        if refStruct != None:
#            for i in range(len(exp.val)):
#                if refStruct.parametros[i].id == exp.val[i].id:
#                    val = resolver_expresion(exp.val[i].dato,ts)                 
#                    if val.tipo == refStruct.parametros[i].tipo:
#                        exp.val[i].dato = val
#                    else:
#                       print('Tipo de parametro en struct incorrecto', val.tipo, refStruct.parametros[i].tipo)
#                       return
#                else:
#                    print('Parametro en struct incorrecto')     
#                    return     
#            return exp
#        else:
#            print('Ese Struct no existe')
#    elif isinstance(exp, AccesoStruc):
#        return ts.obtenerStructData(exp.id,exp.parametro)
#    else :
#        if exp != None:
#            print('Error: Expresión no válida')
#            print(exp)
#
#def casteo(exp,ts):
#    val = resolver_expresion(exp.dato,ts) 
#
#    if val.tipo == exp.casteo:
#        return val
#    elif val.tipo == TIPO_DATO.INT64 and exp.casteo == TIPO_DATO.FLOAT64:
#        return ExpresionNumero(val.val, TIPO_DATO.FLOAT64)
#    elif val.tipo == TIPO_DATO.FLOAT64 and exp.casteo == TIPO_DATO.INT64:
#        return ExpresionNumero(math.trunc(val.val), TIPO_DATO.INT64)
#    elif val.tipo == TIPO_DATO.CHAR and exp.casteo == TIPO_DATO.INT64:
#        return ExpresionNumero( ord(val.val), TIPO_DATO.INT64)
#    
#    return ExpresionDobleComilla("Error -> No se puede realizar casteo", TIPO_DATO.STRING)
#
#def procesar_definicion(instr, ts): 
#     
#    val = resolver_expresion(instr.dato, ts)  
#    if type(val.val) == type([]) and type(val.tipo) != type('string'):
#        cc = None
#        if val.capacity != None:
#            cc = resolver_expresion(val.capacity,ts).val
#        simbolo = TS.Simbolo(instr.id,instr.tipo_var,instr.tipo_dato,val,cc)
#    else:
#        simbolo = TS.Simbolo(instr.id,instr.tipo_var,instr.tipo_dato,val)
#    ts.agregarSimbolo(simbolo)
#
#
#def comprobar_vector(vector,ts,tipo):
#    for n in vector:
#        if resolver_expresion(n,ts).tipo != tipo:
#            return False
#    
#    return True
#
#def to_text(valor,ts):
#    if(isinstance(valor, ExpresionLogicaTF)):
#        if(valor.val):
#           return "true"
#        else:
#           return "false"
#    elif isinstance(valor,ExpresionVec) or isinstance(valor,ExpresionArray):
#        tt = '['
#        cc = 0
#        for v in valor.val:
#            tt += to_text(v,ts) + ', '
#            cc += 1
#        if cc > 0:
#            tt = tt[:-2]
#        tt += ']'
#        return tt
#    elif type(valor) == type([]):
#        tt = '['
#        for v in valor:
#            tt += to_text(v,ts) + ', '
#        tt = tt[:-2]
#        tt += ']'
#        return tt
#    else:
#        return str(valor.val)
#
#def procesar_asignacion(instr,ts):
#    val = resolver_expresion(instr.exp, ts)
#    ts.actualizarSimbolo(instr.id, val)