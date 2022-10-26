from lib2to3.refactor import RefactoringTool
from tkinter import NE
from turtle import clone
from xml.dom import IndexSizeErr
from ts import Simbolo, TIPO_DATO, TIPO_VAR, RetornoType
from expresiones import *
from instrucciones import *
import ts as TS

def guardarFunciones(instrucciones, ts):
    if instrucciones != None:
        for instr in instrucciones:
            if isinstance(instr,Funcion): guardar_funcion(instr,ts) 
            #elif isinstance(instr, CrearStruct): guardar_struct(instr,ts)

def guardar_funcion(instr,ts):
    ts.agregarFuncion(instr)

def procesar_instrucciones(instr, ts, Generador3D, etiquetaInicio = "", etiquetaSalida = "") :
    if isinstance(instr, Imprimir) : return procesar_imprimir(instr, ts, Generador3D)
    elif isinstance(instr, Definicion) : return procesar_definicion(instr, ts, Generador3D)
    elif isinstance(instr, AsignacionVec): return procesarAsignacionVec(instr, ts, Generador3D)
    elif isinstance(instr, Asignacion) : return procesar_asignacion(instr, ts, Generador3D)
    elif isinstance(instr, If): return procesar_if(instr,ts,Generador3D, etiquetaInicio, etiquetaSalida)
    elif isinstance(instr, IfElse): return procesar_if_else(instr,ts,Generador3D, etiquetaInicio, etiquetaSalida)
    elif isinstance(instr, ForIn): return procesar_for(instr,ts,Generador3D)
    elif isinstance(instr, While): return procesar_while(instr,ts,Generador3D)
    elif isinstance(instr, Loop): return procesar_loop(instr,ts,Generador3D)
    elif isinstance(instr, Break): return procesar_break(etiquetaSalida)
    elif isinstance(instr, Continue): return procesar_continue(etiquetaInicio)
    elif isinstance(instr, Llamado): return procesar_llamado(instr, ts, Generador3D).codigo
    elif isinstance(instr, Return): return procesar_return(instr, ts, Generador3D)
    elif isinstance(instr, Match): return procesar_match(instr, ts, Generador3D, etiquetaInicio, etiquetaSalida)

def procesarAsignacionVec(instr, ts, Generador3D):
    CODIGO_SALIDA = ""

    instanciaArreglo = ts.obtenerSimbolo(instr.id)

    if instanciaArreglo != None:
        if instanciaArreglo.tipo_dato == TIPO_DATO.ARRAY or instanciaArreglo.tipo_dato == TIPO_DATO.VECTOR:
            
            temp1 = Generador3D.obtenerTemporal()
            temp2 = Generador3D.obtenerTemporal()
            etiqueta = Generador3D.obtenerEtiqueta()
            etiqueta2 = Generador3D.obtenerEtiqueta()

            if instanciaArreglo.isRef:
                CODIGO_SALIDA = "/* ACCESO A UN ARREGLO REF*/\n"
                CODIGO_SALIDA += f"{temp1} = {instanciaArreglo.direccionRelativa};\n"
                CODIGO_SALIDA += f"{temp2} = Stack[(int) {temp1}]; \n"
            else:
                CODIGO_SALIDA = "/* ACCESO A UN ARREGLO */\n"
                CODIGO_SALIDA += f"{temp1} = S + {instanciaArreglo.direccionRelativa};\n"
                CODIGO_SALIDA += f"{temp2} = Stack[(int) {temp1}]; \n"
            
            listaDimensionesCompiladas = compilarDimensiones(instr, ts, Generador3D) 

            for expr in listaDimensionesCompiladas:
                CODIGO_SALIDA += expr.codigo + "\n"

            resultado = accederAPosicionParaAsignacion(listaDimensionesCompiladas, temp2, ts, Generador3D)

            CODIGO_SALIDA += resultado.codigo + "\n"

            exp = resolverExpresion(instr.exp, ts,Generador3D)
            CODIGO_SALIDA += exp.codigo + "\n"

            CODIGO_SALIDA += f"Heap[(int) {resultado.temporal}] = {exp.temporal};\n"

            CODIGO_SALIDA += f"\ngoto {etiqueta2};\n"
            CODIGO_SALIDA = CODIGO_SALIDA.replace("salida_arreglo_x",etiqueta)
            CODIGO_SALIDA += f"{etiqueta}:\n"

            CODIGO_SALIDA += f'printf("%c", 66); //B\n' \
                             f'printf("%c", 111); //o\n' \
                             f'printf("%c", 117); //u\n' \
                             f'printf("%c", 110); //n\n' \
                             f'printf("%c", 100); //d\n' \
                             f'printf("%c", 115); //s\n' \
                             f'printf("%c", 69); //E\n' \
                             f'printf("%c", 114); //r\n' \
                             f'printf("%c", 114); //r\n' \
                             f'printf("%c", 111); //o\n' \
                             f'printf("%c", 114); //r\n' \
                             f'printf("%c", 10);\n'

            CODIGO_SALIDA += f"{etiqueta2}:\n"


    return CODIGO_SALIDA

def accederAPosicionParaAsignacion(listaExpresiones, temporal, ts, Generador3D):
    CODIGO_SALIDA = "/*ACCEDIENDO A X POSICION*/\n"
  
    expresionX: RetornoType = listaExpresiones.pop(0)

    temp1 = Generador3D.obtenerTemporal()
    temp2 = Generador3D.obtenerTemporal()
    temp3 = Generador3D.obtenerTemporal()
    


    CODIGO_SALIDA += f"{temp1} = Heap[(int) {temporal}]; /*OBTENIENDO TAMAÑO DE ARREGLO*/\n "
    CODIGO_SALIDA += f" if ({expresionX.temporal} < 0) goto salida_arreglo_x;\n"
    CODIGO_SALIDA += f" if ({expresionX.temporal} >= {temp1}) goto salida_arreglo_x;\n"
    CODIGO_SALIDA += f"{temp2} = {temporal} + 1;\n"
    CODIGO_SALIDA += f"{temp3} = {temp2} + {expresionX.temporal};\n"
    

    retorno = RetornoType()
    if(len(listaExpresiones)> 0):
        temp4 = Generador3D.obtenerTemporal()
        CODIGO_SALIDA += f"{temp4} = Heap[(int) {temp3}];\n"
        resultado =  accederAPosicionParaAsignacion(listaExpresiones,temp4,ts, Generador3D)
        CODIGO_SALIDA += resultado.codigo
        retorno.iniciarRetorno(CODIGO_SALIDA,"",resultado.temporal,None)
    else:
        retorno.iniciarRetorno(CODIGO_SALIDA,"",temp3,None)

    return retorno

def procesar_match(instr, ts, Generador3D, etiquetaInicio, etiquetaFin):
    CODIGO_SALIDA = ""
    INSTRUCCIONES = ""

    exp = resolverExpresion(instr.exp, ts, Generador3D)

    CODIGO_SALIDA += exp.codigo + "\n"

    CODIGO_SALIDA += "/* MATCH */\n"

    etiquetaSalida = Generador3D.obtenerEtiqueta()

    for opcionMatch in instr.opciones:
        nEti = Generador3D.obtenerEtiqueta()

        if opcionMatch.coincidencias == TIPO_DATO.VOID:
            CODIGO_SALIDA += f'goto {nEti};\n'
        else:
            for coincidencia in opcionMatch.coincidencias:
                coin = resolverExpresion(coincidencia, ts, Generador3D)

                if coin.tipo == exp.tipo:
                    CODIGO_SALIDA += coin.codigo + "\n"
                    CODIGO_SALIDA += f'if ({exp.temporal} == {coin.temporal}) goto {nEti};\n'
        
        
        INSTRUCCIONES += f'{nEti}:\n'
        INSTRUCCIONES += generarC3DInstrucciones(opcionMatch.instrucciones, ts, Generador3D, etiquetaInicio, etiquetaFin) + "\n"
        INSTRUCCIONES += f'goto {etiquetaSalida};\n'
    

    CODIGO_SALIDA += INSTRUCCIONES
    
    CODIGO_SALIDA += f'{etiquetaSalida}:\n'

    return CODIGO_SALIDA

def procesar_return(instr, ts, Generador3D):
    CODIGO_SALIDA = ""
    if instr.data is None:
        return "goto SECCION_N_RETORNO; \n"
    else:
        resultadoExpresion = resolverExpresion(instr.data, ts, Generador3D)
        CODIGO_SALIDA += resultadoExpresion.codigo + "\n"

        temporal = Generador3D.obtenerTemporal()
        CODIGO_SALIDA += f"{temporal} = S + 0; \n"
        CODIGO_SALIDA += f"Stack[ (int) {temporal}] = {resultadoExpresion.temporal}; \n"
        return CODIGO_SALIDA

def procesar_llamado(instr, ts, Generador3D):
    RETORNO = RetornoType()
    CODIGO_SALIDA = ""

    if ts.existeFuncion(instr.id):
        funcion = ts.obtenerFuncion(instr.id)

        CODIGO_SALIDA += f"/* LLAMADA A FUNCION {instr.id}*/\n"
        ENTORNO_FUNCION = TS.TablaDeSimbolos(simbolos={},funciones=ts.funciones, structs=ts.structs)

        puntero_entorno_nuevo = Generador3D.obtenerTemporal()
        CODIGO_SALIDA += f"{puntero_entorno_nuevo} = S + {len(ts.simbolos)};\n"

        codigoParametros = ejecutarParametros(funcion, ENTORNO_FUNCION, instr.parametros, ts, puntero_entorno_nuevo, Generador3D)

        verificar_funcion_generada(ENTORNO_FUNCION, funcion, Generador3D)

        CODIGO_SALIDA += codigoParametros
        CODIGO_SALIDA += f"\nS = S + {len(ts.simbolos)};\n"
        CODIGO_SALIDA += f"{instr.id}();\n"
        CODIGO_SALIDA += f"S = S - {len(ts.simbolos)};\n"

        TEMPORAL = Generador3D.obtenerTemporal()
        TEMPORAL2 = Generador3D.obtenerTemporal()

        CODIGO_SALIDA += f"\n/* RETURN */\n{TEMPORAL} = S + {len(ts.simbolos)};\n"
        CODIGO_SALIDA += f"{TEMPORAL} = S + {len(ts.simbolos)};\n"
        CODIGO_SALIDA += f"{TEMPORAL2} = Stack[ (int) {TEMPORAL}];\n"

        retorno = RetornoType()
        retorno.iniciarRetorno(CODIGO_SALIDA,"",TEMPORAL2,funcion.tipo_dato)
        return retorno

    return RETORNO

def ejecutarParametros(funcion, ENTORNO_FUNCION, parametros, entornoQueLlamo, puntero_entorno_nuevo, Generador3D):
    if len(funcion.parametros) != len(parametros):
        return ""
    else:
        CODIGO_SALIDA = ""
        for i in range(len(parametros)):
            parametro = funcion.parametros[i]
            expresion_tomada = parametros[i]

            if isinstance(expresion_tomada, ParI):
                print("Es &mut", parametro.id)
                expresionResuelta = resolverIdentificador(expresion_tomada.par, entornoQueLlamo,Generador3D, isRef = True)
                nuevaDefinicion = Definicion(parametro.id,parametro.tipo_var, parametro.tipo_dato, expresionResuelta)
                CODIGO_SALIDA += procesar_definicion(nuevaDefinicion,ENTORNO_FUNCION, Generador3D, puntero_entorno_nuevo, isRef=True)
            else:
                expresionResuelta = resolverExpresion(expresion_tomada, entornoQueLlamo,Generador3D)
                nuevaDefinicion = Definicion(parametro.id,parametro.tipo_var, parametro.tipo_dato, expresionResuelta)
                CODIGO_SALIDA += procesar_definicion(nuevaDefinicion,ENTORNO_FUNCION, Generador3D, puntero_entorno_nuevo)

        return CODIGO_SALIDA

def verificar_funcion_generada(ENTORNO_FUNCION, funcion, Generador3D):
    if not funcion.generada:
        funcion.generada = True
        ENTORNO_FUNCION.sustituirFuncion(funcion) 
        
        resultadoFuncion = procesar_funcion(funcion, ENTORNO_FUNCION, Generador3D)
        Generador3D.agregarFuncion(resultadoFuncion)

def procesar_funcion(funcion, ts, Generador3D):
    CODIGO_SALIDA = ""
    ETIQUETA_RETURN = Generador3D.obtenerEtiqueta()

    CODIGO_SALIDA += f"void {funcion.id}() {{ \n"

    for instruccion in funcion.instrucciones:
        CODIGO_SALIDA += procesar_instrucciones(instruccion, ts, Generador3D)

    CODIGO_SALIDA = CODIGO_SALIDA.replace("SECCION_N_RETORNO", ETIQUETA_RETURN)

    CODIGO_SALIDA += f'{ETIQUETA_RETURN}: \n'
    CODIGO_SALIDA += f'return; \n'
    CODIGO_SALIDA += f'}}\n'
    return CODIGO_SALIDA

def procesar_continue(etiquetaInicio):
    CODIGO = ""
    if etiquetaInicio != "":
        CODIGO = "goto " + etiquetaInicio + ";\n"
    return CODIGO

def procesar_break(etiquetaSalida):
    CODIGO = ""
    if etiquetaSalida != "":
        CODIGO = "goto " + etiquetaSalida + ";\n"
    
    return CODIGO

def procesar_for(instr,ts,Generador3D):
    CODIGO_SALIDA = ""

    rango = resolverExpresion(instr.rango, ts, Generador3D)

    if rango.tipo == TIPO_DATO.ARRAY or rango.tipo == TIPO_DATO.VECTOR:
        
        cont = Generador3D.obtenerTemporal()
        max = Generador3D.obtenerTemporal()

        temp2 = Generador3D.obtenerTemporal()
        temp3 = Generador3D.obtenerTemporal()
        temp4 = Generador3D.obtenerTemporal()

        etiquetaInicio = Generador3D.obtenerTemporal()
        etiquetaCod = Generador3D.obtenerTemporal()
        etiquetaFin = Generador3D.obtenerTemporal()

        CODIGO_SALIDA += rango.codigo

        CODIGO_SALIDA += "/* Sentencia For In */\n"

        CODIGO_SALIDA += f'{cont} = 0;\n'
        CODIGO_SALIDA += f"{max} = Heap[(int) {rango.temporal}]; /*OBTENIENDO TAMAÑO DE ARREGLO*/\n "

        CODIGO_SALIDA += f'{etiquetaInicio}:\n'

        #nuevoAcceso = ExpresionId

        #nuevaDefinicion = Definicion(instr.id,TIPO_VAR.MUTABLE, TIPO_DATO.VOID, expresionResuelta)
        #CODIGO_SALIDA += procesar_definicion(nuevaDefinicion,ENTORNO_FOR, Generador3D, puntero_entorno_nuevo)
        
        CODIGO_SALIDA += f'if ({cont} < {max}) goto {etiquetaCod};\n' \
                         f'goto {etiquetaFin};\n'

        CODIGO_SALIDA += f'{etiquetaCod}:\n'

        CODIGO_SALIDA += f"{temp2} = {rango.temporal} + 1;\n"
        CODIGO_SALIDA += f"{temp3} = {temp2} + {cont};\n"
        CODIGO_SALIDA += f"{temp4} = Heap[(int) {temp3}];\n"

        temp1 = Generador3D.obtenerTemporal() 

        retornoAux = RetornoType()
        retornoAux.iniciarRetorno("","",temp4, rango.tipo2)

        direccionRelativa = len(ts.simbolos)

        CODIGO_SALIDA += f"/* ASIGNANDO VARIABLE  {instr.id}*/\n"
        CODIGO_SALIDA += f'{temp1} = S + {direccionRelativa};\n'
        CODIGO_SALIDA += f'Stack[(int) {temp1}] = {temp4};\n' 

        simboloAux = Simbolo(instr.id,TIPO_VAR.MUTABLE, TIPO_DATO.VOID, retornoAux, direccionRelativa)
        ts.agregarSimbolo(simboloAux)

        CODIGO_SALIDA += generarC3DInstrucciones(instr.instrucciones, ts, Generador3D, etiquetaInicio, etiquetaFin)

        CODIGO_SALIDA += f'\n{cont} = {cont} + 1;\n'

        CODIGO_SALIDA += f'\ngoto {etiquetaInicio};\n'

        CODIGO_SALIDA += f'{etiquetaFin}:\n'

    return CODIGO_SALIDA

def procesar_while(instr,ts,Generador3D):
    CODIGO_SALIDA = ""

    valorExpresion = resolverExpresion(instr.exp,ts, Generador3D)

    if valorExpresion.tipo == TIPO_DATO.BOOLEAN:
        etiquetaInicio = Generador3D.obtenerEtiqueta()
        etiquetaCod = Generador3D.obtenerEtiqueta()
        etiquetaFin = Generador3D.obtenerEtiqueta()

        CODIGO_SALIDA += "/* CICLO WHILE */\n"
        CODIGO_SALIDA += f'{etiquetaInicio}:\n'
        CODIGO_SALIDA += valorExpresion.codigo + "\n"

        CODIGO_SALIDA += f'if ({valorExpresion.temporal} == 1) goto {etiquetaCod};\n' \
                         f'goto {etiquetaFin};\n'
        
        CODIGO_SALIDA += f'{etiquetaCod}:\n'

        CODIGO_SALIDA += generarC3DInstrucciones(instr.instrucciones, ts, Generador3D, etiquetaInicio, etiquetaFin)

        CODIGO_SALIDA += f'\ngoto {etiquetaInicio};\n'

        CODIGO_SALIDA += f'{etiquetaFin}:\n'

    else:
        print("Error -> While necesita un booleano")

    return CODIGO_SALIDA

def procesar_loop(instr,ts,Generador3D):
    CODIGO_SALIDA = ""

    etiquetaInicio = Generador3D.obtenerEtiqueta()
    etiquetaFin = Generador3D.obtenerEtiqueta()

    CODIGO_SALIDA += "/* CICLO LOOP */\n"
    CODIGO_SALIDA += f'{etiquetaInicio}:\n'

    CODIGO_SALIDA += generarC3DInstrucciones(instr.instrucciones, ts, Generador3D, etiquetaInicio, etiquetaFin)

    CODIGO_SALIDA += f'\ngoto {etiquetaInicio};\n'

    CODIGO_SALIDA += f'{etiquetaFin}:\n'

    return CODIGO_SALIDA

def procesar_if(instr,ts,Generador3D, etiquetaInicio, etiquetaSalida):
    CODIGO_SALIDA = ""

    ETIQUETA_SALIDA = Generador3D.obtenerEtiqueta()

    etiquetaVerdadera = Generador3D.obtenerEtiqueta()
    etiquetaFalso = Generador3D.obtenerEtiqueta()

    expresionCondicion = resolverExpresion(instr.exp, ts, Generador3D)
    
    if expresionCondicion.tipo == TIPO_DATO.BOOLEAN:
        CODIGO_SALIDA += "/* INSTRUCCION IF*/\n"
        CODIGO_SALIDA += expresionCondicion.codigo
        CODIGO_SALIDA += f'if ({expresionCondicion.temporal} == 1) goto {etiquetaVerdadera};\n'
        CODIGO_SALIDA += f'goto {ETIQUETA_SALIDA};\n'
        CODIGO_SALIDA += f'{etiquetaVerdadera}: \n'
        CODIGO_SALIDA += generarC3DInstrucciones(instr.instrucciones, ts, Generador3D, etiquetaInicio, etiquetaSalida)
        CODIGO_SALIDA += f' goto {ETIQUETA_SALIDA};\n'
        CODIGO_SALIDA += f'{etiquetaFalso}:\n'

        CODIGO_SALIDA+= f'{ETIQUETA_SALIDA}: \n'
    else:
        print("Error -> if necesita booleano")

    return CODIGO_SALIDA

def procesar_if_else(instr,ts,Generador3D, etiquetaInicio, etiquetaSalida):
    CODIGO_SALIDA = ""

    ETIQUETA_SALIDA = Generador3D.obtenerEtiqueta()

    etiquetaVerdadera = Generador3D.obtenerEtiqueta()
    etiquetaFalso = Generador3D.obtenerEtiqueta()

    expresionCondicion = resolverExpresion(instr.exp, ts, Generador3D)
    
    if expresionCondicion.tipo == TIPO_DATO.BOOLEAN:
        CODIGO_SALIDA += "/* INSTRUCCION IF*/\n"
        CODIGO_SALIDA += expresionCondicion.codigo
        CODIGO_SALIDA += f'\nif ({expresionCondicion.temporal} == 1) goto {etiquetaVerdadera};\n'
        CODIGO_SALIDA += f'goto {etiquetaFalso};\n'
        CODIGO_SALIDA += f'{etiquetaVerdadera}: \n'
        CODIGO_SALIDA += generarC3DInstrucciones(instr.instrIfVerdadero, ts, Generador3D, etiquetaInicio, etiquetaSalida)
        CODIGO_SALIDA += f' goto {ETIQUETA_SALIDA};\n'
        CODIGO_SALIDA += f'{etiquetaFalso}: \n'

        if isinstance(instr.instrIfFalso, If) or isinstance(instr.instrIfFalso, IfElse):
            CODIGO_SALIDA += procesar_instrucciones(instr.instrIfFalso, ts, Generador3D, etiquetaInicio, etiquetaSalida)
        else:
            CODIGO_SALIDA += generarC3DInstrucciones(instr.instrIfFalso, ts, Generador3D, etiquetaInicio, etiquetaSalida)

        CODIGO_SALIDA+= f'{ETIQUETA_SALIDA}: \n'
    else:
        print("Error -> if necesita booleano")

    return CODIGO_SALIDA

def generarC3DInstrucciones(lista, ts, Generador3D, etiquetaInicio, etiquetaSalida):
    CODIGO_SALIDA = ""
    for instr in lista :
        CODIGO_SALIDA += procesar_instrucciones(instr, ts, Generador3D, etiquetaInicio, etiquetaSalida)

    return CODIGO_SALIDA

def procesar_asignacion(instr, ts, Generador3D):
    valorExpresion = resolverExpresion(instr.exp,ts,Generador3D)
    simbolo = ts.obtenerSimbolo(instr.id)
    nn = ts.actualizarSimbolo(instr.id, valorExpresion)
    CODIGO_SALIDA = ""
    if nn != None:
        
        temp1 = Generador3D.obtenerTemporal()

        SEGMENTO_MEMORIA = "Stack"

        CODIGO_SALIDA += f"/* ASIGNANDO VARIABLE  {instr.id}*/\n"
        CODIGO_SALIDA += valorExpresion.codigo + '\n'
        CODIGO_SALIDA += f'{temp1} = S + {simbolo.direccionRelativa};\n'
        CODIGO_SALIDA += f'{SEGMENTO_MEMORIA}[(int) {temp1}] = {valorExpresion.temporal};\n'      

    return CODIGO_SALIDA

def procesar_definicion(instr, ts, Generador3D, nuevoPuntero = "", isRef = False):
    CODIGO_SALIDA = ""


    if isinstance(instr.dato, RetornoType):
        valorExpresion = instr.dato
    else:
        valorExpresion = resolverExpresion(instr.dato,ts,Generador3D)

    tamanioEntorno = len(ts.simbolos)
    nsimbolo = Simbolo(instr.id,instr.tipo_var,instr.tipo_dato,valorExpresion,tamanioEntorno)

    nn = ts.agregarSimbolo(nsimbolo)

    if nn != None:
        
        temp1 = Generador3D.obtenerTemporal()

        PUNTERO_ENTORNO = "S"
        SEGMENTO_MEMORIA = "Stack"

        if nuevoPuntero != "":
            PUNTERO_ENTORNO = nuevoPuntero

        CODIGO_SALIDA += "/* DECLARACIÓN DE UNA VARIABLE */\n"
        CODIGO_SALIDA += valorExpresion.codigo + '\n'
        CODIGO_SALIDA += f'{temp1} = {PUNTERO_ENTORNO} + {tamanioEntorno}; \n'
        CODIGO_SALIDA += f'{SEGMENTO_MEMORIA}[(int) {temp1}] = {valorExpresion.temporal};\n'

    return CODIGO_SALIDA

def procesar_imprimir(instr, ts, Generador3D):

    cadena = instr.cad.val
    #cadena = cadena.replace('\\n','\n')
    contador = 0
        
    CODIGO_SALIDA_TOT = ""

    sep = cadena.split("{}")

    if len(sep) > 1 and len(instr.parametros) > 0:
        for cad in sep:
            if cad != "":
                CODIGO_SALIDA = ""
                retorno = RetornoType()
                temp2 = Generador3D.obtenerTemporal()
                CODIGO_SALIDA += f'{temp2} = H;\n'

                for caracter in cad:
                    valor = ord(caracter)
                    CODIGO_SALIDA += f'Heap[H] ={valor};\n'
                    CODIGO_SALIDA += f'H = H + 1;\n'

                CODIGO_SALIDA += f'Heap[H] = 0;\n'
                CODIGO_SALIDA += f'H = H+1;\n'

                retorno.iniciarRetorno(CODIGO_SALIDA, "", temp2, instr.cad.tipo)

                CODIGO_SALIDA = ""

                temp1 = Generador3D.obtenerTemporal()
                caracter = Generador3D.obtenerTemporal()
                etqCiclo = Generador3D.obtenerEtiqueta()
                etqSalida = Generador3D.obtenerEtiqueta()
                etqAuxiliar = Generador3D.obtenerEtiqueta()
                #etqAuxiliar2 = Generador3D.obtenerEtiqueta()

                CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR CADENA*/\n"
                CODIGO_SALIDA += retorno.codigo
                CODIGO_SALIDA += f'{temp1} = {retorno.temporal};\n'
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
                CODIGO_SALIDA_TOT += CODIGO_SALIDA 

            if contador < len(instr.parametros):
                CODIGO_SALIDA = ""
                paraminprint = resolverExpresion(instr.parametros[contador], ts, Generador3D)
                if paraminprint.tipo == TIPO_DATO.INT64 or paraminprint.tipo == TIPO_DATO.USIZE:
                    CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR ENTERO*/\n"
                    CODIGO_SALIDA += paraminprint.codigo
                    CODIGO_SALIDA += f'\nprintf(\"%d\", (int){paraminprint.temporal}); \n'

                elif paraminprint.tipo == TIPO_DATO.FLOAT64:
                    CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR DECIMAL*/\n"
                    CODIGO_SALIDA += paraminprint.codigo
                    CODIGO_SALIDA += f'\nprintf(\"%f\", (float){paraminprint.temporal}); \n'
                elif paraminprint.tipo == TIPO_DATO.STRING or paraminprint.tipo == TIPO_DATO.ISTRING:

                    temp1 = Generador3D.obtenerTemporal()
                    caracter = Generador3D.obtenerTemporal()
                    etqCiclo = Generador3D.obtenerEtiqueta()
                    etqSalida = Generador3D.obtenerEtiqueta()
                    etqAuxiliar = Generador3D.obtenerEtiqueta()

                    CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR CADENA*/\n"
                    CODIGO_SALIDA += paraminprint.codigo
                    CODIGO_SALIDA += f'{temp1} = {paraminprint.temporal};\n'
                    CODIGO_SALIDA += f'{etqCiclo}: \n'
                    CODIGO_SALIDA += f'{caracter} = Heap[(int){temp1}];\n'

                    CODIGO_SALIDA += f'{etqAuxiliar}: \n'
                    CODIGO_SALIDA += f'if ({caracter} == 0) goto {etqSalida};\n' \
                                    f'     printf(\"%c\",(char) {caracter});\n' \
                                    f'     {temp1} = {temp1} + 1;\n' \
                                    f'     goto {etqCiclo};\n'

                    CODIGO_SALIDA += f'{etqSalida}:\n'
                elif paraminprint.tipo == TIPO_DATO.CHAR:
                    temp1 = Generador3D.obtenerTemporal()
                    caracter = Generador3D.obtenerTemporal()

                    CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR CHAR*/\n"
                    CODIGO_SALIDA += paraminprint.codigo
                    CODIGO_SALIDA += f'{temp1} = {paraminprint.temporal};\n'
                    CODIGO_SALIDA += f'{caracter} = Heap[(int){temp1}];\n'
                    CODIGO_SALIDA += f'printf(\"%c\",(int) {caracter});\n'

                elif paraminprint.tipo == TIPO_DATO.BOOLEAN:
                    CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR BOOLEAN*/\n"
                    CODIGO_SALIDA += paraminprint.codigo
                    CODIGO_SALIDA += f'\nprintf(\"%d\", (int){paraminprint.temporal}); \n'
                elif paraminprint.tipo == TIPO_DATO.ARRAY or paraminprint.tipo == TIPO_DATO.VECTOR:
                    CODIGO_SALIDA += "/* IMPRIMIENDO UN ARREGLO/\n"
                    CODIGO_SALIDA += paraminprint.codigo

                    CODIGO_SALIDA += imprimirArreglo(paraminprint, ts, Generador3D)

                else:
                    print("No se puede imprimir: ", paraminprint.tipo)

                CODIGO_SALIDA_TOT += CODIGO_SALIDA 
            contador += 1           
        CODIGO_SALIDA_TOT += f'printf(\"%c\",(int)10);\n'
    else:
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
        CODIGO_SALIDA_TOT = CODIGO_SALIDA
    return CODIGO_SALIDA_TOT

def imprimirArreglo(exp, ts, Generador3D):

    temp1 = Generador3D.obtenerTemporal()
    temp2 = Generador3D.obtenerTemporal()
    cont = Generador3D.obtenerTemporal()

    CODIGO_SALIDA = ""

    CODIGO_SALIDA += f"{temp1} = Heap[(int) {exp.temporal}]; /*OBTENIENDO TAMAÑO DE ARREGLO*/\n "
    CODIGO_SALIDA += f"{temp2} = {exp.temporal} + 1;\n"
    CODIGO_SALIDA += f"{cont} =  1;\n"

    CODIGO_SALIDA += imprimirArrayRecursivo(len(exp.valor.valor), exp.tipo2, temp2, temp1, Generador3D, cont)    

    return CODIGO_SALIDA

def imprimirArrayRecursivo(cont, tipo, temp2, temp1, Generador3D, contador):
    CODIGO_SALIDA = ""

    etiquetaInicio = Generador3D.obtenerEtiqueta()
    etiquetaFin = Generador3D.obtenerEtiqueta()
    etiquetaNext = Generador3D.obtenerEtiqueta()

    if cont == 1:
        CODIGO_SALIDA += f'printf(\"%c\",(int)91);\n'
        CODIGO_SALIDA += f'{etiquetaInicio}:\n'
        CODIGO_SALIDA += f'if ({contador} > {temp1}) goto {etiquetaFin};\n'

        if tipo == TIPO_DATO.INT64 or tipo == TIPO_DATO.USIZE:
            temp3 = Generador3D.obtenerTemporal()
            CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR ENTERO*/\n"
            CODIGO_SALIDA += f'{temp3} = Heap[(int){temp2}];'
            CODIGO_SALIDA += f'\nprintf(\"%d\", (int){temp3}); \n'
        elif tipo == TIPO_DATO.FLOAT64:
            temp3 = Generador3D.obtenerTemporal()
            CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR DECIMAL*/\n"
            CODIGO_SALIDA += f'{temp3} = Heap[(int){temp2}];'
            CODIGO_SALIDA += f'\nprintf(\"%f\", (float){temp3}); \n'
        elif tipo == TIPO_DATO.STRING or tipo == TIPO_DATO.ISTRING:

            temp3 = Generador3D.obtenerTemporal()
            caracter = Generador3D.obtenerTemporal()
            etqCiclo = Generador3D.obtenerEtiqueta()
            etqSalida = Generador3D.obtenerEtiqueta()
            etqAuxiliar = Generador3D.obtenerEtiqueta()

            CODIGO_SALIDA += "/* IMPRIMIENDO UN VALOR CADENA*/\n"
            CODIGO_SALIDA += f'{temp3} = Heap[(int){temp2}];'
            CODIGO_SALIDA += f'{etqCiclo}: \n'
            CODIGO_SALIDA += f'{caracter} = Heap[(int){temp3}];\n'

            CODIGO_SALIDA += f'{etqAuxiliar}: \n'
            CODIGO_SALIDA += f'if ({caracter} == 0) goto {etqSalida};\n' \
                            f'     printf(\"%c\",(char) {caracter});\n' \
                            f'     {temp3} = {temp3} + 1;\n' \
                            f'     goto {etqCiclo};\n'

            CODIGO_SALIDA += f'{etqSalida}:\n'

        CODIGO_SALIDA += f'if ({contador} == {temp1}) goto {etiquetaNext};\n'
        CODIGO_SALIDA += f'printf(\"%c\",(int)44);\n'
        CODIGO_SALIDA += f'printf(\"%c\",(int)32);\n'

        CODIGO_SALIDA += f'{etiquetaNext}:\n'
        CODIGO_SALIDA += f'{contador} = {contador} + 1;\n' \
                        f'{temp2} = {temp2} + 1;\n' \
                        f'goto {etiquetaInicio};\n'

        CODIGO_SALIDA += f'{etiquetaFin}:\n'
        CODIGO_SALIDA += f'printf(\"%c\",(int)93);\n'
    else:
        CODIGO_SALIDA += f'printf(\"%c\",(int)91);\n'
        
        CODIGO_SALIDA += f'{etiquetaInicio}:\n'
        CODIGO_SALIDA += f'if ({contador} > {temp1}) goto {etiquetaFin};\n'

        temp11 = Generador3D.obtenerTemporal()
        temp22 = Generador3D.obtenerTemporal()
        contadoraux = Generador3D.obtenerTemporal()

        CODIGO_SALIDA += f"{temp11} = Heap[(int) {temp2}]; /*OBTENIENDO TAMAÑO DE ARREGLO*/\n "
        CODIGO_SALIDA += f"{temp22} = {temp2} + 1;\n"
        CODIGO_SALIDA += f"{contadoraux} = 1;\n"


        CODIGO_SALIDA += imprimirArrayRecursivo(cont -1, tipo, temp22, temp11, Generador3D,contadoraux)

        CODIGO_SALIDA += f'if ({contador} == {temp1}) goto {etiquetaNext};\n'
        CODIGO_SALIDA += f'printf(\"%c\",(int)44);\n'
        CODIGO_SALIDA += f'printf(\"%c\",(int)32);\n'

        CODIGO_SALIDA += f'{etiquetaNext}:\n'
        CODIGO_SALIDA += f'{contador} = {contador} + 1;\n' \
                        f'{temp2} = {temp2} + 1;\n' \
                        f'goto {etiquetaInicio};\n'

        CODIGO_SALIDA += f'{etiquetaFin}:\n'

        CODIGO_SALIDA += f'printf(\"%c\",(int)93);\n'

    return CODIGO_SALIDA

def resolverExpresion(exp, ts, Generador3D):
    if isinstance(exp, ExpresionDobleComilla): return resolverCadena(exp, Generador3D)
    elif isinstance(exp,ExpresionCaracter): return resolverChar(exp,Generador3D)
    elif isinstance(exp, ToString): return resolverToString(exp,ts, Generador3D)
    elif isinstance(exp, ExpresionNumero): return resolverNumero(exp, Generador3D)
    elif isinstance(exp, ExpresionLogicaTF): return resolverBooleano(exp, Generador3D)
    elif isinstance(exp, ExpresionNot): return resolverNot(exp,ts, Generador3D)
    elif isinstance(exp, ExpresionNegativo): return resolverNumeroNegativo(exp, Generador3D)
    elif isinstance(exp, ExpresionBinaria): return resolverExpresionBinaria(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionIdentificador): return resolverIdentificador(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionRelacionalBinaria): return resolverOpRelacion(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionLogicaBinaria): return resolverOpLogica(exp, ts, Generador3D)
    elif isinstance(exp, Abs): return resolverValorAbsoluto(exp, ts, Generador3D)
    elif isinstance(exp, Sqrt): return resolverSqrt(exp, ts, Generador3D)
    elif isinstance(exp, Casteo): return resolverCasteo(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionPotencia): return resolverPotencia(exp, ts, Generador3D)
    elif isinstance(exp, Llamado): return procesar_llamado(exp,ts,Generador3D)
    elif isinstance(exp, ExpresionArray): return resolverArray(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionIdVectorial): return AccesoArreglo(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionRango): return resolverRango(exp, ts, Generador3D)
    elif isinstance(exp, Len): return resolverLen(exp, ts, Generador3D)
    elif isinstance(exp, ExpresionIf): return resolverExpresionIf(exp, ts, Generador3D)

def resolverExpresionIf(exp, ts, Generador3D):
    retorno = RetornoType()

    CODIGO_SALIDA = ""

    ETIQUETA_SALIDA = Generador3D.obtenerEtiqueta()

    etiquetaVerdadera = Generador3D.obtenerEtiqueta()
    etiquetaFalso = Generador3D.obtenerEtiqueta()

    expresionCondicion = resolverExpresion(exp.exp, ts, Generador3D)

    res = Generador3D.obtenerTemporal()
    
    if expresionCondicion.tipo == TIPO_DATO.BOOLEAN:
        CODIGO_SALIDA += "/* EXPRESION IF*/\n"
        CODIGO_SALIDA += expresionCondicion.codigo
        CODIGO_SALIDA += f'\nif ({expresionCondicion.temporal} == 1) goto {etiquetaVerdadera};\n'
        CODIGO_SALIDA += f'goto {etiquetaFalso};\n'
        CODIGO_SALIDA += f'{etiquetaVerdadera}: \n'
        
        resVer = resolverExpresion(exp.instrIfVerdadero, ts, Generador3D)

        CODIGO_SALIDA += resVer.codigo + "\n"
        CODIGO_SALIDA += f'{res} = {resVer.temporal};\n'

        CODIGO_SALIDA += f' goto {ETIQUETA_SALIDA};\n'
        CODIGO_SALIDA += f'{etiquetaFalso}: \n'

        if isinstance(exp.instrIfFalso, ExpresionIf):
            ifelse = resolverExpresionIf(exp.instrIfFalso, ts, Generador3D)
            CODIGO_SALIDA += ifelse.codigo + "\n"
            CODIGO_SALIDA += f'{res} = {ifelse.temporal};\n'
        else:
            resFalso = resolverExpresion(exp.instrIfFalso, ts, Generador3D)

            CODIGO_SALIDA += resFalso.codigo + "\n"
            CODIGO_SALIDA += f'{res} = {resFalso.temporal};\n'

        CODIGO_SALIDA+= f'{ETIQUETA_SALIDA}: \n'

        print(resVer.tipo)
        retorno.iniciarRetorno(CODIGO_SALIDA, "", res, resVer.tipo)
    else:
        print("Error -> Expresion If necesita booleano")

    return retorno

def resolverValoresRepetidos(exp,ts,Generador3D):
    retorno = RetornoType()
    CODIGO_FINAL = ""

    data = resolverExpresion(exp.val.dato, ts, Generador3D)
    cant = resolverExpresion(exp.val.cant, ts, Generador3D)

    if cant.tipo == TIPO_DATO.INT64 or cant.tipo == TIPO_DATO.USIZE:

        listaDimensiones = [1]
        tipo = data.tipo

        CODIGO_FINAL += data.codigo + "\n"
        CODIGO_FINAL += cant.codigo + "\n"

        temp1 = Generador3D.obtenerTemporal()
        temp2 = Generador3D.obtenerTemporal()
        index = Generador3D.obtenerTemporal()

        etiquetaInit = Generador3D.obtenerEtiqueta()
        etiquetaFin = Generador3D.obtenerEtiqueta()

        CODIGO_FINAL += f"{temp1} = H;/*Posicion de referencia en HEAP*/\n"    
        
        CODIGO_FINAL += f"H = H + 1;  \n"
        CODIGO_FINAL += f"H = H + {cant.temporal};  \n"
        CODIGO_FINAL += f"Heap[(int) {temp1} ] = {cant.temporal}; /*Valor que almacena el tamaño*/\n"
        CODIGO_FINAL += f'{index} = 1;\n'

        CODIGO_FINAL += "/* VALORES REPETIDOS */\n"

        CODIGO_FINAL += f'{etiquetaInit}:\n'

        if (data.valor != None):
            CODIGO_FINAL += "/* referenciando a un sub-arreglo*/\n"
            CODIGO_FINAL += data.codigo +"\n"
            CODIGO_FINAL += f"{temp2} = {temp1} + {index};\n"
            CODIGO_FINAL += f"Heap[(int) {temp2}] = {data.temporal};\n"
            listaDimensiones.extend(data.valor)  # ALMACENAR EL TAMAÑO DE UNA DIMENSION
            tipo = data.tipo2
        else:
            CODIGO_FINAL += "/* almacenando un valor String, bool, int o float */\n"
            CODIGO_FINAL += data.codigo + "\n"
            CODIGO_FINAL += f"{temp2} = {temp1} + {index};\n"
            CODIGO_FINAL += f"Heap[(int) {temp2}] = {data.temporal};\n"

        CODIGO_FINAL += f'if ({index} == {cant.temporal}) goto {etiquetaFin}; \n'
        CODIGO_FINAL += f'{index} = {index} + 1;\n' \
                        f'goto {etiquetaInit};\n'

        CODIGO_FINAL += f'{etiquetaFin}:\n'

        retorno.iniciarRetorno(CODIGO_FINAL, "", temp1, TIPO_DATO.ARRAY, listaDimensiones, tipo )

    return retorno

def resolverLen(exp, ts, Generador3D):
    retorno = RetornoType()
    CODIGO = ""

    vv = resolverExpresion(exp.dato, ts, Generador3D)

    if vv.tipo == TIPO_DATO.ARRAY or vv.tipo == TIPO_DATO.VECTOR:
        temp1 = Generador3D.obtenerTemporal()

        CODIGO += vv.codigo + "\n"

        CODIGO += "/* LEN */\n"
        CODIGO += f"{temp1} = Heap[(int) {vv.temporal}]; /*OBTENIENDO TAMAÑO DE ARREGLO*/\n "

        retorno.iniciarRetorno(CODIGO, "", temp1, TIPO_DATO.INT64)
    else:
        print("No se puede obtener Len de: ", vv.tipo)

    return retorno

def resolverRango(exp, ts, Generador3D):
    retorno = RetornoType()
    CODIGO = ""

    inicio = resolverExpresion(exp.inicio, ts, Generador3D)
    fin = resolverExpresion(exp.fin, ts, Generador3D)

    if inicio.tipo == TIPO_DATO.INT64 and fin.tipo == TIPO_DATO.INT64:

        temp1 = Generador3D.obtenerTemporal()
        temp2 = Generador3D.obtenerTemporal()
        cont = Generador3D.obtenerTemporal()
        contAux = Generador3D.obtenerTemporal()
        
        etiquetaInicio = Generador3D.obtenerEtiqueta()
        etiquetaCod = Generador3D.obtenerEtiqueta()
        etiquetaFin = Generador3D.obtenerEtiqueta()

        CODIGO += inicio.codigo + "\n"
        CODIGO += fin.codigo + "\n"
        CODIGO += "/* GENERANDO RANGO */\n"

        CODIGO += f"{temp1} = H; /*Posicion de referencia en HEAP*/\n"
        CODIGO += f"{temp2} = {temp1};\n"

        CODIGO += f"{cont} = {inicio.temporal};\n"
        CODIGO += f"{contAux} = 0;\n"

        CODIGO += f'{etiquetaInicio}:\n'
        CODIGO += f'if ({cont}<{fin.temporal}) goto {etiquetaCod};\n' \
                  f'goto {etiquetaFin};\n'

        CODIGO += f'{etiquetaCod}:\n'

        CODIGO += f'{temp2} = {temp2} + 1;\n' \
                  f'Heap[(int){temp2}] = {cont};\n'


        CODIGO += f'{cont} = {cont} + 1;\n' \
                  f'{contAux} = {contAux} + 1;\n' \
                  f'goto {etiquetaInicio};\n'

        CODIGO += f'{etiquetaFin}:\n'

        CODIGO += f'Heap[(int){temp1}] = {contAux};\n'
        CODIGO += f'H = H + 1;\n'
        CODIGO += f'H = H + {contAux};\n'
        

        retorno.iniciarRetorno(CODIGO, "", temp1, TIPO_DATO.ARRAY, [1], inicio.tipo)
    return retorno

def AccesoArreglo(exp, ts, Generador3D):
    retorno = RetornoType()

    instanciaArreglo = ts.obtenerSimbolo(exp.id)

    if instanciaArreglo != None:
        if instanciaArreglo.tipo_dato == TIPO_DATO.ARRAY or instanciaArreglo.tipo_dato == TIPO_DATO.VECTOR:
            temp1 = Generador3D.obtenerTemporal()
            temp2 = Generador3D.obtenerTemporal()
            etiqueta = Generador3D.obtenerEtiqueta()
            etiqueta2 = Generador3D.obtenerEtiqueta()

            if instanciaArreglo.isRef:
                CODIGO_SALIDA = "/* ACCESO A UN ARREGLO REF*/\n"
            else:
                CODIGO_SALIDA = "/* ACCESO A UN ARREGLO*/\n"

            CODIGO_SALIDA += f"{temp1} = S + {instanciaArreglo.direccionRelativa};\n"
            CODIGO_SALIDA += f"{temp2} = Stack[(int) {temp1}]; \n"

            #if len(self.listaExpresiones) != len(instanciaArreglo.dimensiones):
            #    return  RetornoType()

            listaExpresionesCompiladas = compilarDimensiones(exp, ts, Generador3D)        

            valorAux = instanciaArreglo.valor

            while type(valorAux) != type([]):
                valorAux = valorAux.valor

            esArray = len(listaExpresionesCompiladas) < len(valorAux)

            for expr in listaExpresionesCompiladas:
                CODIGO_SALIDA += expr.codigo + "\n"

            resultado = accederAPosicion(listaExpresionesCompiladas, temp2, ts, Generador3D)

            CODIGO_SALIDA += resultado.codigo
            CODIGO_SALIDA += f"\ngoto {etiqueta2};\n"
            CODIGO_SALIDA = CODIGO_SALIDA.replace("salida_arreglo_x",etiqueta)
            CODIGO_SALIDA += f"{etiqueta}:\n"

            CODIGO_SALIDA += f'printf("%c", 66); //B\n' \
                             f'printf("%c", 111); //o\n' \
                             f'printf("%c", 117); //u\n' \
                             f'printf("%c", 110); //n\n' \
                             f'printf("%c", 100); //d\n' \
                             f'printf("%c", 115); //s\n' \
                             f'printf("%c", 69); //E\n' \
                             f'printf("%c", 114); //r\n' \
                             f'printf("%c", 114); //r\n' \
                             f'printf("%c", 111); //o\n' \
                             f'printf("%c", 114); //r\n' \
                             f'printf("%c", 10);\n'
            CODIGO_SALIDA += f'{resultado.temporal} = 0;\n'

            CODIGO_SALIDA += f"{etiqueta2}:\n"

            if esArray:
                instanciaArreglo.valor.valor = [1]
                retorno.iniciarRetorno(CODIGO_SALIDA,"",resultado.temporal, instanciaArreglo.valor.tipo,valor=instanciaArreglo.valor, tipo2 = instanciaArreglo.valor.tipo2)
            else:   
                retorno.iniciarRetorno(CODIGO_SALIDA,"",resultado.temporal, instanciaArreglo.valor.tipo2)

    return retorno

def accederAPosicion(listaExpresiones, temporal, ts, Generador3D):
    CODIGO_SALIDA = "/*ACCEDIENDO A X POSICION*/\n"
  
    expresionX: RetornoType = listaExpresiones.pop(0)

    temp1 = Generador3D.obtenerTemporal()
    temp2 = Generador3D.obtenerTemporal()
    temp3 = Generador3D.obtenerTemporal()
    temp4 = Generador3D.obtenerTemporal()


    CODIGO_SALIDA += f"{temp1} = Heap[(int) {temporal}]; /*OBTENIENDO TAMAÑO DE ARREGLO*/\n "
    CODIGO_SALIDA += f" if ({expresionX.temporal} < 0) goto salida_arreglo_x;\n"
    CODIGO_SALIDA += f" if ({expresionX.temporal} >= {temp1}) goto salida_arreglo_x;\n"
    CODIGO_SALIDA += f"{temp2} = {temporal} + 1;\n"
    CODIGO_SALIDA += f"{temp3} = {temp2} + {expresionX.temporal};\n"
    CODIGO_SALIDA += f"{temp4} = Heap[(int) {temp3}];\n"

    retorno = RetornoType()
    if(len(listaExpresiones)> 0):
        resultado =  accederAPosicion(listaExpresiones,temp4,ts, Generador3D)
        CODIGO_SALIDA += resultado.codigo
        retorno.iniciarRetorno(CODIGO_SALIDA,"",resultado.temporal,None)
    else:
        retorno.iniciarRetorno(CODIGO_SALIDA,"",temp4,None)

    return retorno

def compilarDimensiones(exp, ts, Generador3D):
    dimensiones = []
    for expresion in exp.ubicacion:
        retornoExpr = resolverExpresion(expresion, ts, Generador3D)
        if retornoExpr.tipo == TIPO_DATO.INT64 or retornoExpr.tipo == TIPO_DATO.USIZE:
            dimensiones.append(retornoExpr)
        else:
            break
    return  dimensiones

def resolverArray(exp, ts, Generador3D):

    if isinstance(exp.val, ValoresRepetidos):
        return resolverValoresRepetidos(exp,ts,Generador3D)

    retorno = RetornoType()
    CODIGO_FINAL = ""

    listaDimensiones = []
    temp1 = Generador3D.obtenerTemporal()
    temp2 = Generador3D.obtenerTemporal()
    index = Generador3D.obtenerTemporal()

    CODIGO_FINAL += f"{temp1} = H;/*Posicion de referencia en HEAP*/\n"

    exee = resolver_expresionesCompiladas(exp, ts, Generador3D)
    expresionesCompiladas = exee[0]
    tipo = exee[1]

    listaDimensiones.append(len(expresionesCompiladas)) # ALMACENAR EL TAMAÑO DE UNA DIMENSION
    CODIGO_FINAL += f"H = H + {len(expresionesCompiladas) + 1};  \n"
    CODIGO_FINAL += f"Heap[(int) {temp1} ] = {len(expresionesCompiladas)}; /*Valor que almacena el tamaño*/\n"
    CODIGO_FINAL += f'{index} = 1;\n'
    #index = 1

    primero = True
    for expr in expresionesCompiladas:
        if (expr.valor != None):
            CODIGO_FINAL += "/* referenciando a un sub-arreglo*/\n"
            CODIGO_FINAL += expr.codigo +"\n"
            CODIGO_FINAL += f"{temp2} = {temp1} + {index};\n"
            CODIGO_FINAL += f"Heap[(int) {temp2}] = {expr.temporal};\n"
            if(primero):
                listaDimensiones.extend(expr.valor)  # ALMACENAR EL TAMAÑO DE UNA DIMENSION
                primero = False
            tipo = expr.tipo2
        else:
            CODIGO_FINAL += "/* almacenando un valor String, bool, int o float */\n"
            CODIGO_FINAL += expr.codigo + "\n"
            CODIGO_FINAL += f"{temp2} = {temp1} + {index};\n"
            CODIGO_FINAL += f"Heap[(int) {temp2}] = {expr.temporal};\n"
        CODIGO_FINAL += f'{index} = {index} + 1; \n'
        #index += 1
    
    retorno.iniciarRetorno(CODIGO_FINAL, "", temp1, TIPO_DATO.ARRAY, listaDimensiones, tipo)
    return retorno

def resolver_expresionesCompiladas(exp, ts, Generador3D):
    expresiones = []

    contador = 0
    tipo = TIPO_DATO.VOID

    for data in exp.val:
        resultadoExpr = resolverExpresion(data,ts,Generador3D)
        #Verificando tipo
        if contador == 0:
            tipo = resultadoExpr.tipo
        else:
            if (tipo != resultadoExpr.tipo):
                return []
        contador += 1
        expresiones.append(resultadoExpr)
    return [expresiones, tipo]

def resolverPotencia(exp, ts, Generador3D):
    RETORNO = RetornoType()
    CODIGO = ""
    exp1 = resolverExpresion(exp.exp1, ts, Generador3D)
    exp2 = resolverExpresion(exp.exp2, ts, Generador3D)

    if((exp1.tipo == TIPO_DATO.INT64 and exp2.tipo == TIPO_DATO.INT64 ) or (exp1.tipo == TIPO_DATO.FLOAT64 and exp2.tipo == TIPO_DATO.FLOAT64 )):
        if(exp1.tipo == exp.tipo):
            res = Generador3D.obtenerTemporal()
            cont = Generador3D.obtenerTemporal()

            etiquetaInicio = Generador3D.obtenerEtiqueta()
            etiquetaCod = Generador3D.obtenerEtiqueta()
            etiquetaSalida = Generador3D.obtenerEtiqueta()

            CODIGO += exp1.codigo + "\n"
            CODIGO += exp2.codigo + "\n"

            CODIGO += "/* POTENCIA */\n"
            CODIGO += f'{res} = 1;\n' \
                      f'{cont} = {exp2.temporal};\n\n'
            
            CODIGO += f'{etiquetaInicio}:\n' \
                      f'if ({cont} > 0) goto {etiquetaCod};\n' \
                      f'goto {etiquetaSalida};\n'
            
            CODIGO += f'{etiquetaCod}:\n' \
                      f'    {res} = {res} * {exp1.temporal};\n' \
                      f'    {cont} = {cont} - 1;\n' \
                      f'    goto {etiquetaInicio};\n'
            
            CODIGO += f'{etiquetaSalida}:'

            RETORNO.iniciarRetorno(CODIGO,"",res,exp.tipo)
        else:
            print("Error -> No es del tipo correcto")
    else:
        print("Error -> No se puede operar Potencia con: ", exp1.tipo, exp2.tipo)

    return RETORNO

def resolverNot(exp,ts, Generador3D):
    CODIGO_SALIDA = ""
    retorno = RetornoType()

    valorExpresion = resolverExpresion(exp.exp, ts, Generador3D)

    if valorExpresion.tipo == TIPO_DATO.BOOLEAN:
        etiquetaVerdadera = Generador3D.obtenerEtiqueta()
        etiquetaFalsa = Generador3D.obtenerEtiqueta()
        etiquetaSalida = Generador3D.obtenerEtiqueta()
        CODIGO_SALIDA += "/* NOT */\n"
        CODIGO_SALIDA += valorExpresion.codigo
        CODIGO_SALIDA += f'if ({valorExpresion.temporal} == 1) goto {etiquetaVerdadera};\n'
        CODIGO_SALIDA += f'goto {etiquetaFalsa};\n'
        CODIGO_SALIDA += f'{etiquetaVerdadera}: {valorExpresion.temporal} = 0;\n'\
                         f'goto {etiquetaSalida};\n'
        CODIGO_SALIDA += f'{etiquetaFalsa}: {valorExpresion.temporal} = 1;\n'
        CODIGO_SALIDA += f'{etiquetaSalida}:\n'

        retorno.iniciarRetorno(CODIGO_SALIDA,"",valorExpresion.temporal,valorExpresion.tipo)
    else:
        print("Not necesita un booleano")

    return retorno

def resolverOpRelacion(exp, ts, Generador3D):
    RETORNO = RetornoType()

    CODIGO_SALIDA = ""

    izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
    der3D = resolverExpresion(exp.exp2, ts, Generador3D)


    CODIGO_SALIDA += "/* OPERACION RELACIONAL */\n"
    CODIGO_SALIDA += izq3D.codigo + "\n"
    CODIGO_SALIDA += der3D.codigo + "\n"

    if (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.FLOAT64 and der3D.tipo == TIPO_DATO.FLOAT64) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.USIZE) or (izq3D.tipo == TIPO_DATO.BOOLEAN and der3D.tipo == TIPO_DATO.BOOLEAN)or (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.USIZE) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.INT64):
        etiquetaVerdadera = Generador3D.obtenerEtiqueta()
        etiquetaFalsa = Generador3D.obtenerEtiqueta()
        etiquetaSalida = Generador3D.obtenerEtiqueta()

        temp = Generador3D.obtenerTemporal()

        CODIGO_SALIDA += f'if ({izq3D.temporal} {obtenerSimbolo(exp)} {der3D.temporal}) goto {etiquetaVerdadera};\n'
        CODIGO_SALIDA += f'goto {etiquetaFalsa}; \n'
    
        CODIGO_SALIDA += f'{etiquetaVerdadera}: \n' \
                         f' {temp} = 1;\n' \
                         f' goto {etiquetaSalida};\n'

        CODIGO_SALIDA += f'{etiquetaFalsa}: \n' \
                         f' {temp} = 0;\n'

        CODIGO_SALIDA += f'{etiquetaSalida}:\n'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",temp, TIPO_DATO.BOOLEAN)
        RETORNO.etiquetaV = etiquetaVerdadera
        RETORNO.etiquetaF = etiquetaFalsa


    return RETORNO

def resolverOpLogica(exp, ts, Generador3D):
    if exp.operador == OPERACION_LOGICA.AND: return operacionAnd(exp, ts, Generador3D)
    elif exp.operador == OPERACION_LOGICA.OR: return operacionOr(exp, ts, Generador3D)
    else: print("Error -> Operación lógica no reconocida.")

def operacionAnd(exp, ts, Generador3D):
    CODIGO_SALIDA = ""
    RETORNO = RetornoType()

    izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
    der3D = resolverExpresion(exp.exp2, ts, Generador3D)

    if (izq3D.tipo == TIPO_DATO.BOOLEAN and der3D.tipo == TIPO_DATO.BOOLEAN):
        temporal = Generador3D.obtenerTemporal()
        etiquetaVerdadero = Generador3D.obtenerEtiqueta()
        etiquetaFalso = Generador3D.obtenerEtiqueta()
        etiquetaSalida = Generador3D.obtenerEtiqueta()
        etiquetaVaux = Generador3D.obtenerEtiqueta()

        CODIGO_SALIDA += izq3D.codigo + "\n"
        CODIGO_SALIDA += der3D.codigo + "\n"

        CODIGO_SALIDA += "/* OPERACION AND */\n"

        CODIGO_SALIDA += f'if ({izq3D.temporal} == 1) goto {etiquetaVaux};\n' \
                        f'goto {etiquetaFalso};\n'
        CODIGO_SALIDA += f'{etiquetaVaux}:\n'
        CODIGO_SALIDA += f'if ({der3D.temporal} == 1) goto {etiquetaVerdadero};\n' \
                        f'goto {etiquetaFalso};\n'

        CODIGO_SALIDA += f'{etiquetaVerdadero}:\n' \
                        f'{temporal} = 1;\n' \
                        f'goto {etiquetaSalida};\n'

        CODIGO_SALIDA += f'{etiquetaFalso}:\n' \
                        f'{temporal} = 0;\n'

        CODIGO_SALIDA += f'{etiquetaSalida}:\n'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",temporal,TIPO_DATO.BOOLEAN)
    return RETORNO

def operacionOr(exp, ts, Generador3D):
    CODIGO_SALIDA = ""
    RETORNO = RetornoType()

    izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
    der3D = resolverExpresion(exp.exp2, ts, Generador3D)

    if (izq3D.tipo == TIPO_DATO.BOOLEAN and der3D.tipo == TIPO_DATO.BOOLEAN):
        temporal = Generador3D.obtenerTemporal()
        etiquetaVerdadero = Generador3D.obtenerEtiqueta()
        etiquetaFalso = Generador3D.obtenerEtiqueta()
        etiquetaSalida = Generador3D.obtenerEtiqueta()
        etiquetaVaux = Generador3D.obtenerEtiqueta()

        CODIGO_SALIDA += izq3D.codigo + "\n"
        CODIGO_SALIDA += der3D.codigo + "\n"

        CODIGO_SALIDA += "/* OPERACION OR */\n"

        CODIGO_SALIDA += f'if ({izq3D.temporal} == 1) goto {etiquetaVerdadero};\n' \
                        f'goto {etiquetaVaux};\n'
        CODIGO_SALIDA += f'{etiquetaVaux}:\n'
        CODIGO_SALIDA += f'if ({der3D.temporal} == 1) goto {etiquetaVerdadero};\n' \
                        f'goto {etiquetaFalso};\n'

        CODIGO_SALIDA += f'{etiquetaVerdadero}:\n' \
                        f'{temporal} = 1;\n' \
                        f'goto {etiquetaSalida};\n'

        CODIGO_SALIDA += f'{etiquetaFalso}:\n' \
                        f'{temporal} = 0;\n'

        CODIGO_SALIDA += f'{etiquetaSalida}:\n'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",temporal,TIPO_DATO.BOOLEAN)
    return RETORNO

def obtenerSimbolo(exp):
        match exp.operador:
            case OPERACION_LOGICA.MAYOR_QUE:
                return '>'
            case OPERACION_LOGICA.MENOR_QUE:
                return '<'
            case OPERACION_LOGICA.MAYORIGUAL:
                return '>='
            case OPERACION_LOGICA.MENORIGUAL:
                return '<='
            case OPERACION_LOGICA.AND:
                return '&&'
            case OPERACION_LOGICA.OR:
                return '||'
            case OPERACION_LOGICA.DIFERENTE:
                return '!='
            case OPERACION_LOGICA.IGUAL:
                return '=='

def resolverBooleano(exp, Generador3D):
    CODIGO_SALIDA = ""
    retorno = RetornoType()

    temp2 = Generador3D.obtenerTemporal()
    if exp.val == True:
        CODIGO_SALIDA += f'{temp2} = 1;'
    else:
        CODIGO_SALIDA += f'{temp2} = 0;'

    retorno.iniciarRetorno(CODIGO_SALIDA, "", temp2, exp.tipo)

    return retorno

def resolverNumero(exp, Generador3D):
    CODIGO_SALIDA = ""
    retorno = RetornoType()
    temp1 = Generador3D.obtenerTemporal()
    CODIGO_SALIDA += f'{temp1} = {exp.val};'
    retorno.iniciarRetorno(CODIGO_SALIDA,"", temp1, exp.tipo)
    return retorno

def resolverNumeroNegativo(exp, Generador3D):
    if exp.exp.tipo == TIPO_DATO.INT64 or exp.exp.tipo == TIPO_DATO.FLOAT64:
        CODIGO_SALIDA = ""
        retorno = RetornoType()
        temp1 = Generador3D.obtenerTemporal()
        CODIGO_SALIDA += f'{temp1} = {(exp.exp.val * -1)};'
        retorno.iniciarRetorno(CODIGO_SALIDA,"", temp1, exp.exp.tipo)
        return retorno
    else:
        print("No se puede operar")

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

def resolverChar(exp, Generador3D):
    CODIGO_SALIDA = ""
    retorno = RetornoType()

    temp2 = Generador3D.obtenerTemporal()
    CODIGO_SALIDA += f'{temp2} = H;\n'

    caracter = exp.val[0]
    valor = ord(caracter)
    CODIGO_SALIDA += f'Heap[H] ={valor};\n'
    CODIGO_SALIDA += f'H = H + 1;\n'

    retorno.iniciarRetorno(CODIGO_SALIDA, "", temp2, exp.tipo)

    return retorno

def resolverToString(exp, ts, Generador3D):
    retorno = RetornoType()

    valorExpresion = resolverExpresion(exp.dato, ts, Generador3D)

    if valorExpresion.tipo == TIPO_DATO.ISTRING or valorExpresion.tipo == TIPO_DATO.STRING:
        retorno.iniciarRetorno(valorExpresion.codigo, "", valorExpresion.temporal, TIPO_DATO.STRING)

    return retorno

def resolverIdentificador(exp, ts, Generador, isRef = False):
    simbolo = ts.obtenerSimbolo(exp.id)

    retorno = RetornoType()
    CODIGO_SALIDA = ""

    if simbolo != None:
        TEMP1 = Generador.obtenerTemporal()
        TEMP2 = Generador.obtenerTemporal()

        CODIGO_SALIDA += f"/* ACCEDIENDO A VARIABLE  {exp.id}*/\n"
        CODIGO_SALIDA += f'{TEMP1} = S + {simbolo.direccionRelativa};\n'
        CODIGO_SALIDA += f'{TEMP2} = Stack[(int) {TEMP1}];\n'

        retorno.iniciarRetorno(CODIGO_SALIDA,"",TEMP2,simbolo.tipo_dato,valor=simbolo.valor ,tipo2= simbolo.valor.tipo2)
    
    return retorno

def resolverExpresionBinaria(exp, ts, Generador3D):
    if exp.operador == OPERACION_ARITMETICA.MAS: return operacionSuma(exp, ts, Generador3D)
    elif exp.operador == OPERACION_ARITMETICA.MENOS: return operacionResta(exp, ts, Generador3D)
    elif exp.operador == OPERACION_ARITMETICA.POR: return operacionMulti(exp, ts, Generador3D)
    elif exp.operador == OPERACION_ARITMETICA.DIVIDIDO: return operacionDivi(exp, ts, Generador3D)
    elif exp.operador == OPERACION_ARITMETICA.MODULO: return operacionModulo(exp, ts, Generador3D)

def operacionModulo(exp, ts, Generador3D):
    CODIGO_SALIDA = ""
    RETORNO = RetornoType()

    izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
    der3D = resolverExpresion(exp.exp2, ts, Generador3D)

    TEMP1 = Generador3D.obtenerTemporal()

    if (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.USIZE):

        CODIGO_SALIDA += izq3D.codigo +"\n"
        CODIGO_SALIDA += der3D.codigo +"\n"
        CODIGO_SALIDA += f'{TEMP1} = (int){izq3D.temporal} % (int){der3D.temporal};\n'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.INT64)
    elif izq3D.tipo == TIPO_DATO.FLOAT64 and der3D.tipo == TIPO_DATO.FLOAT64:

        CODIGO_SALIDA += izq3D.codigo +"\n"
        CODIGO_SALIDA += der3D.codigo +"\n"
        CODIGO_SALIDA += f'{TEMP1} = (int){izq3D.temporal} % (int){der3D.temporal};\n'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.FLOAT64)

    return  RETORNO

def operacionDivi(exp, ts, Generador3D):

    CODIGO_SALIDA = ""
    RETORNO = RetornoType()

    izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
    der3D = resolverExpresion(exp.exp2, ts, Generador3D)

    etiquetaV= Generador3D.obtenerEtiqueta()
    etiquetaF= Generador3D.obtenerEtiqueta()
    etiquetaSalida = Generador3D.obtenerEtiqueta()

    TEMP1 = Generador3D.obtenerTemporal()

    CODIGO_SALIDA += izq3D.codigo +"\n"
    CODIGO_SALIDA += der3D.codigo +"\n"

    CODIGO_SALIDA += f'if({der3D.temporal} != 0) goto {etiquetaV};\n' \
                     f'goto {etiquetaF};\n'

    CODIGO_SALIDA += f'{etiquetaV}:\n'
    CODIGO_SALIDA += f'{TEMP1} = {izq3D.temporal} / {der3D.temporal};\n' \
                     f'goto {etiquetaSalida};\n'

    CODIGO_SALIDA += f'{etiquetaF}:\n'

    CODIGO_SALIDA += f'printf("%c",77); //M\n'\
                     f'printf("%c",97); //a\n'\
                     f'printf("%c",116); //t\n'\
                     f'printf("%c",104); //h\n'\
                     f'printf("%c",69); //E\n'\
                     f'printf("%c",114); //r\n'\
                     f'printf("%c",114); //r\n'\
                     f'printf("%c",111); //o\n'\
                     f'printf("%c",114); //r\n' \
                     f'printf("%c",10);\n'

    CODIGO_SALIDA += f'{TEMP1} = 0;\n'

    CODIGO_SALIDA += f'{etiquetaSalida}:\n'

    if (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.USIZE):
        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.INT64)
    elif izq3D.tipo == TIPO_DATO.FLOAT64 and der3D.tipo == TIPO_DATO.FLOAT64:
        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.FLOAT64)

    return  RETORNO

def operacionMulti(exp, ts, Generador3D):

        CODIGO_SALIDA = ""
        RETORNO = RetornoType()

        izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
        der3D = resolverExpresion(exp.exp2, ts, Generador3D)

        TEMP1 = Generador3D.obtenerTemporal()

        if (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.USIZE):

            CODIGO_SALIDA += izq3D.codigo +"\n"
            CODIGO_SALIDA += der3D.codigo +"\n"
            CODIGO_SALIDA += f'{TEMP1} = {izq3D.temporal} * {der3D.temporal};\n'

            RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.INT64)
        elif izq3D.tipo == TIPO_DATO.FLOAT64 and der3D.tipo == TIPO_DATO.FLOAT64:

            CODIGO_SALIDA += izq3D.codigo +"\n"
            CODIGO_SALIDA += der3D.codigo +"\n"
            CODIGO_SALIDA += f'{TEMP1} = {izq3D.temporal} * {der3D.temporal};\n'

            RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.FLOAT64)

        return  RETORNO

def operacionResta(exp, ts, Generador3D):
    RETORNO = RetornoType()
    CODIGO_SALIDA = ""

    izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
    der3D = resolverExpresion(exp.exp2, ts, Generador3D)

    TEMP1 = Generador3D.obtenerTemporal()

    if (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.USIZE) or (izq3D.tipo == TIPO_DATO.FLOAT64 and der3D.tipo == TIPO_DATO.FLOAT64):

        CODIGO_SALIDA += izq3D.codigo +"\n"
        CODIGO_SALIDA += der3D.codigo +"\n"
        CODIGO_SALIDA += f'{TEMP1} = {izq3D.temporal} - {der3D.temporal};\n'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,izq3D.tipo)

    return  RETORNO

def operacionSuma(exp, ts, Generador3D):

        CODIGO_SALIDA = ""
        RETORNO = RetornoType()

        izq3D = resolverExpresion(exp.exp1, ts, Generador3D)
        der3D = resolverExpresion(exp.exp2, ts, Generador3D)

        TEMP1 = Generador3D.obtenerTemporal()

        if (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.USIZE and der3D.tipo == TIPO_DATO.INT64) or (izq3D.tipo == TIPO_DATO.INT64 and der3D.tipo == TIPO_DATO.USIZE):

            CODIGO_SALIDA += izq3D.codigo +"\n"
            CODIGO_SALIDA += der3D.codigo +"\n"
            CODIGO_SALIDA += f'{TEMP1} = {izq3D.temporal} + {der3D.temporal};\n'

            RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.INT64)

        elif izq3D.tipo == TIPO_DATO.FLOAT64 and der3D.tipo == TIPO_DATO.FLOAT64:

            CODIGO_SALIDA += izq3D.codigo +"\n"
            CODIGO_SALIDA += der3D.codigo +"\n"
            CODIGO_SALIDA += f'{TEMP1} = {izq3D.temporal} + {der3D.temporal};\n'

            RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP1,TIPO_DATO.FLOAT64)

        elif izq3D.tipo == TIPO_DATO.STRING and der3D.tipo == TIPO_DATO.ISTRING:
            TEMP2 = Generador3D.obtenerTemporal()

            CODIGO_SALIDA += izq3D.codigo
            CODIGO_SALIDA += der3D.codigo
            CODIGO_SALIDA += f'{TEMP2} = H;\n'
            CODIGO_SALIDA += operacionConcatenar(izq3D, ts, Generador3D)
            CODIGO_SALIDA += operacionConcatenar(der3D, ts, Generador3D)
            CODIGO_SALIDA += f'Heap[H] = 0;\n'
            CODIGO_SALIDA += f'H = H + 1;\n'

            RETORNO.iniciarRetorno(CODIGO_SALIDA,"",TEMP2,TIPO_DATO.STRING)
        else:
            print("Error -> No se puede operar Suma con:", izq3D.tipo, der3D.tipo)

        return  RETORNO

def resolverValorAbsoluto(exp, ts, Generador3D):
    CODIGO_SALIDA = ""
    RETORNO = RetornoType()

    valorExpresion = resolverExpresion(exp.dato, ts, Generador3D)

    if valorExpresion.tipo == TIPO_DATO.INT64 or valorExpresion.tipo == TIPO_DATO.FLOAT64:
        etiquetaVerdadera = Generador3D.obtenerEtiqueta()
        etiquetaFalsa = Generador3D.obtenerEtiqueta()
        etiquetaSalida = Generador3D.obtenerEtiqueta()
        temporal = Generador3D.obtenerTemporal()

        CODIGO_SALIDA += valorExpresion.codigo + "\n"
        CODIGO_SALIDA += "/* VALOR ABSOLUTO */\n"
        CODIGO_SALIDA += f'if ({valorExpresion.temporal}<0) goto {etiquetaVerdadera};\n' \
                         f'goto {etiquetaFalsa};\n'
        
        CODIGO_SALIDA += f'{etiquetaVerdadera}:\n' \
                         f'{temporal} = {valorExpresion.temporal} * -1;\n' \
                         f'goto {etiquetaSalida};\n'
        
        CODIGO_SALIDA += f'{etiquetaFalsa}:\n' \
                         f'{temporal} = {valorExpresion.temporal};\n'
        
        CODIGO_SALIDA += f'{etiquetaSalida}:'

        RETORNO.iniciarRetorno(CODIGO_SALIDA,"",temporal,valorExpresion.tipo)

    return RETORNO

def resolverSqrt(exp, ts, Generador3D):
    CODIGO = ""
    RETORNO = RetornoType()

    valorExpresion = resolverExpresion(exp.dato, ts, Generador3D)

    if valorExpresion.tipo == TIPO_DATO.INT64 or valorExpresion.tipo == TIPO_DATO.FLOAT64 or valorExpresion.tipo == TIPO_DATO.USIZE:
        etiquetaInicio = Generador3D.obtenerEtiqueta()
        etiquetaCod = Generador3D.obtenerEtiqueta()
        etiquetaFin = Generador3D.obtenerEtiqueta()

        sqrt = Generador3D.obtenerTemporal()
        tmp = Generador3D.obtenerTemporal()

        tmp1 = Generador3D.obtenerTemporal()
        tmp2 = Generador3D.obtenerTemporal()
        tmp3 = Generador3D.obtenerTemporal()

        CODIGO += valorExpresion.codigo + "\n"
        CODIGO += "/* RAIZ CUADRADA */\n"
        CODIGO += f'{sqrt} = {valorExpresion.temporal} / 2;\n'
        CODIGO += f'{tmp} = 0;\n'

        CODIGO += f'{etiquetaInicio}: \n' \
                  f'    if ({sqrt} != {tmp}) goto {etiquetaCod};\n' \
                  f'    goto {etiquetaFin};\n' \
                  f'{etiquetaCod}:\n' \
                  f'    {tmp} = {sqrt};\n' \
                  f'    {tmp1} = {valorExpresion.temporal} / {tmp};\n' \
                  f'    {tmp2} = {tmp1} + {tmp};\n' \
                  f'    {tmp3} = {tmp2} / 2;\n' \
                  f'    {sqrt} = {tmp3};\n'\
                  f'    goto {etiquetaInicio};\n'
        
        CODIGO += f'{etiquetaFin}:\n'

        RETORNO.iniciarRetorno(CODIGO,"", sqrt, valorExpresion.tipo)

    return RETORNO

def operacionConcatenar(expresionRetorno, ts, Generador3D):
    CODIGO_SALIDA = ""

    etiquetaCiclo = Generador3D.obtenerEtiqueta()
    etiquetaSalida = Generador3D.obtenerEtiqueta()
    CARACTER = Generador3D.obtenerTemporal()

    CODIGO_SALIDA += f'{etiquetaCiclo}: \n'
    CODIGO_SALIDA += f'{CARACTER} = Heap[(int){expresionRetorno.temporal}];\n'
    CODIGO_SALIDA += f'if ( {CARACTER} == 0) goto {etiquetaSalida};\n'
    CODIGO_SALIDA += f'     Heap[H] = {CARACTER};\n'
    CODIGO_SALIDA += f'     H = H + 1;\n'
    CODIGO_SALIDA += f'     {expresionRetorno.temporal} = {expresionRetorno.temporal} + 1;\n'
    CODIGO_SALIDA += f'     goto {etiquetaCiclo};\n'
    CODIGO_SALIDA += f'{etiquetaSalida}:\n'
    return CODIGO_SALIDA

def resolverCasteo(exp, ts, Generador3D):
    valorExpresion = resolverExpresion(exp.dato, ts, Generador3D)

    if valorExpresion.tipo == exp.casteo:
        return valorExpresion
    elif valorExpresion.tipo == TIPO_DATO.INT64 and exp.casteo == TIPO_DATO.FLOAT64:
        valorExpresion.tipo == TIPO_DATO.FLOAT64
        return valorExpresion
    elif valorExpresion.tipo == TIPO_DATO.INT64 and exp.casteo == TIPO_DATO.USIZE:
        valorExpresion.tipo == TIPO_DATO.USIZE
        return valorExpresion
    elif valorExpresion.tipo == TIPO_DATO.FLOAT64 and exp.casteo == TIPO_DATO.INT64:
        valorExpresion.tipo == TIPO_DATO.INT64
        return valorExpresion
    elif valorExpresion.tipo == TIPO_DATO.CHAR and exp.casteo == TIPO_DATO.INT64:
        valorExpresion.tipo == TIPO_DATO.INT64
        return valorExpresion
    else:
        print("No se puede hacer casteo", valorExpresion.tipo , exp.casteo)
    
    return RetornoType()
