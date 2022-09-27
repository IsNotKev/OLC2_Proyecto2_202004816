
reservadas = {
    'println': 'PRINTLN',
    'powf'   : 'POWF',
    'pow'    : 'POW',
    'i64'    : 'INT',
    'usize'  : 'USIZE',
    'f64'    : 'FLOAT',
    'bool'   : 'BOOLEAN',
    'char'   : 'CHAR',
    'str'    : 'ISTRING',
    'String' : 'STRING',
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'let'    : 'LET',
    'mut'    : 'MUT',
    'if'     : 'IF',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'for'    : 'FOR',
    'in'     : 'IN',
    'fn'     : 'FN',
    'match'  : 'MATCH',
    '_'      : 'DEFAULT',
    'to_string' : 'TOSTRING',
    'to_owned'  : 'TOOWNED',
    'abs'       : 'ABS',
    'sqrt'      : 'SQRT',
    'as'        : 'AS',
    'vec'       : 'VEC',
    'Vec'       : 'VVEC',
    'new'       : 'NEW',
    'loop'      : 'LOOP',
    'break'     : 'BREAK',
    'continue'  : 'CONTINUE',
    'return'    : 'RETURN',
    'len'       : 'LEN',
    'push'      : 'PUSH',
    'remove'    : 'REMOVE',
    'contains'  : 'CONTAINS',
    'insert'    : 'INSERT',
    'with_capacity' : 'WCAPACITY',
    'capacity'  : 'CAPACITY',
    'struct'    : 'STRUCT'
}

tokens  = [
    'PUNTO',
    'FLECHA',
    'FLECHAMATCH',
    'PTCOMA',
    'DOSPUNTOS',
    'COMA',
    'CORCHIZQ',
    'CORCHDER',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'MAYORIGUAL',
    'MENORIGUAL',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'OR',
    'O',
    'AND',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'ID',
    'ADMIR',
    'I' 
] + list(reservadas.values())

# Tokens
t_PUNTO     = r'\.'
t_FLECHA    = r'\-\>'
t_FLECHAMATCH = r'\=\>'
t_PTCOMA    = r';'
t_DOSPUNTOS = r':'
t_COMA      = r','
t_CORCHIZQ  = r'\['
t_CORCHDER  = r'\]'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MODULO    = r'%'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_OR        = r'\|\|'
t_O        = r'\|'
t_AND       = r'&&'
t_ADMIR     = r'!'
t_I         = r'&'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CARACTER(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')    # Check for reserved words
     return t

def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1

def t_COMENTARIOML(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print(f'Caracter no reconocido {t.value[0]!r} en la linea {t.lexer.lineno}')
    t.lexer.skip(1)

# Construyendo el analizador léxico
from ply import lex
lex.lex()

############################################# PARSER #######################################

#Precedencia
precedence = (
    ('left', 'OR', 'AND'),
    ('nonassoc','MAYQUE', 'MENQUE','MAYORIGUAL','MENORIGUAL','IGUALQUE','NIGUALQUE'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','MODULO'),
    ('right','UMENOS', 'NOT'),   
    )

from expresiones import *
from instrucciones import *
from ts import TIPO_DATO
from ts import TIPO_VAR

def p_init(t) :
    'inicio            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      :   imprimir_instr PTCOMA
                        |   definicion_instr PTCOMA
                        |   asignacion_instr PTCOMA
                        |   asignacion_vec PTCOMA
                        |   asignacion_struct PTCOMA
                        |   if_instr
                        |   while_instr
                        |   loop_instr
                        |   funcion_instr
                        |   llamado_instr PTCOMA
                        |   match_instr
                        |   break_instr PTCOMA
                        |   continue_instr PTCOMA
                        |   return_instr PTCOMA
                        |   for_instr
                        |   push_instr PTCOMA
                        |   remove_instr PTCOMA
                        |   insert_instr PTCOMA
                        |   crear_struct'''
    t[0] = t[1]

def p_asignacion_instr(t) :
    'asignacion_instr   : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3])

def p_crear_struct(t):
    'crear_struct       :   STRUCT ID LLAVIZQ struct_data LLAVDER'
    t[0] = CrearStruct(t[2],t[4])

def p_struct_data(t):
    'struct_data        :   struct_data COMA ID DOSPUNTOS tipos'
    t[1].append(StructParametro(t[3],t[5]))
    t[0] = t[1]

def p_struct_dataU(t):
    'struct_data        :   ID DOSPUNTOS tipos'
    t[0] = [StructParametro(t[1],t[3])]

def p_insert_instr(t):
    'insert_instr     :   ID PUNTO INSERT PARIZQ expresion COMA expresion PARDER'
    t[0] = Insert(t[1],t[5],t[7])

def p_asignacion_vec(t):
    'asignacion_vec     :   ID lista_corch IGUAL expresion'
    t[0] = AsignacionVec(t[1],t[2],t[4])

def p_asignacion_struct(t):
    'asignacion_struct     :   ID lids IGUAL expresion'
    t[0] = AsignacionStruct(t[1],t[2],t[4])

def p_remove_instr(t):
    'remove_instr       :   ID PUNTO REMOVE PARIZQ expresion PARDER'
    t[0] = Remove(t[1], t[5])

def p_push_instr(t):
    'push_instr       :   ID PUNTO PUSH PARIZQ expresion PARDER'
    t[0] = Push(t[1], t[5])

def p_return_instr(t):
    'return_instr       :   RETURN expresion'
    t[0] = Return(True, t[2])

def p_for_instr(t):
    'for_instr          :   FOR ID IN expresion statement'
    t[0] = ForIn(t[2],t[4],t[5])

def p_for_instrid(t):
    'for_instr          :   FOR ID IN ID statement'
    t[0] = ForIn(t[2],ExpresionIdentificador(t[4]),t[5])

def p_continue(t):
    'continue_instr     :   CONTINUE'
    t[0] = Continue(True)

def p_break(t):
    'break_instr        :   BREAK'
    t[0] = Break(True)

def p_break_ret(t):
    'break_instr        :   BREAK expresion'
    t[0] = Break(True,t[2])

def p_loop_instr(t):
    'loop_instr         :   LOOP statement'
    t[0] = Loop(t[2])

def p_match_instr(t):
    'match_instr        : MATCH expresion LLAVIZQ lismatch LLAVDER'
    t[0] = Match(t[2],t[4])

def p_match_instrid(t):
    'match_instr        : MATCH ID LLAVIZQ lismatch LLAVDER'
    t[0] = Match(ExpresionIdentificador(t[2]),t[4])

def p_match_instr_v(t):
    'match_instr        : MATCH expresion LLAVIZQ LLAVDER'
    t[0] = Match(t[2],[])

def p_match_instr_vid(t):
    'match_instr        : MATCH ID LLAVIZQ LLAVDER'
    t[0] = Match(ExpresionIdentificador(t[2]),[])

def p_llismatch(t):
    'lismatch          :   lismatch instrmatch'
    t[1].append(t[2])
    t[0] = t[1]

def p_lismatch(t):
    'lismatch           : instrmatch'
    t[0] = [t[1]]

def p_instrsmatch(t):
    'instrmatch         : listcoincidencia FLECHAMATCH statement'
    t[0] = OpcionMatch(t[1],t[3])

def p_instrmatch(t):
    'instrmatch         : listcoincidencia FLECHAMATCH instruccion_match COMA'
    t[0] = OpcionMatch(t[1],[t[3]])

def p_instrmatch_default(t):
    'instrmatch         :  DEFAULT FLECHAMATCH instruccion_match COMA'
    t[0] = OpcionMatch(TIPO_DATO.VOID,[t[3]])

def p_instrsmatch_default(t):
    'instrmatch         :  DEFAULT FLECHAMATCH statement'
    t[0] = OpcionMatch(TIPO_DATO.VOID,t[3])

# ACTUALIZAR INSTRUCCIONES :v
def p_instrdmatch(t):
    '''instruccion_match    :   imprimir_instr
                            |   definicion_instr
                            |   asignacion_instr
                            |   if_instr
                            |   while_instr
                            |   funcion_instr
                            |   llamado_instr
                            |   match_instr'''
    t[0] = t[1]

def p_expresion_id(t):
    'expresion     : ID'
    t[0] = ExpresionIdentificador(t[1])

def p_llistcoincidencia(t):
    'listcoincidencia   :   listcoincidencia O expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_listcoincidencia(t):
    'listcoincidencia   :  expresion'
    t[0] = [t[1]]

def p_llamado_instr(t):
    'llamado_instr      :   ID PARIZQ PARDER'
    t[0] = Llamado(t[1],[])

def p_llamado_instr_CP(t):
    'llamado_instr      :   ID PARIZQ llparams PARDER'
    t[0] = Llamado(t[1],t[3])

def p_lllamadoparams(t):
    'llparams           :   llparams COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_lllamadoparamsY(t):
    'llparams           :   llparams COMA I MUT ID'
    t[1].append(ParI(ExpresionIdentificador(t[5])))
    t[0] = t[1]

def p_llamadoparamsY(t):
    'llparams           :   I MUT ID'
    t[0] = [ParI(ExpresionIdentificador(t[3]))]

def p_llamadoparams(t):
    'llparams           :   expresion'
    t[0] = [t[1]]

def p_funcion_intr_SP(t):
    'funcion_instr    :   FN ID PARIZQ PARDER statement'
    t[0] = Funcion(t[2],[],TIPO_DATO.VOID,t[5])

def p_funcion_ctipo_intr_SP(t):
    'funcion_instr    :   FN ID PARIZQ PARDER FLECHA tipos statement'
    t[0] = Funcion(t[2],[],t[6],t[7])

def p_funcion_intr(t):
    'funcion_instr    :   FN ID PARIZQ fparam PARDER statement'
    t[0] = Funcion(t[2],t[4],TIPO_DATO.VOID,t[6])

def p_funcion_ctipo_intr(t):
    'funcion_instr    :   FN ID PARIZQ fparam PARDER FLECHA tipos statement'
    t[0] = Funcion(t[2],t[4],t[7],t[8])

def p_listafparams(t):
    'fparam         :       fparam COMA fparametro'
    t[1].append(t[3])
    t[0] = t[1]

def p_fparams(t):
    'fparam         :       fparametro'
    t[0] = [t[1]]

def p_fparametro(t):
    'fparametro     :       ID DOSPUNTOS tipos'
    t[0] = Parametro(t[1],t[3],TIPO_VAR.INMUTABLE)

def p_fparametroI(t):
    'fparametro     :       ID DOSPUNTOS I MUT tipos'
    t[0] = Parametro(t[1],t[5],TIPO_VAR.MUTABLE)

def p_fparametro_mut(t):
    'fparametro     :       MUT ID DOSPUNTOS tipos'
    t[0] = Parametro(t[2],t[4],TIPO_VAR.MUTABLE)

def p_while_instr(t) :
    'while_instr     : WHILE expresion statement'
    t[0] =While(t[2], t[3])

def p_if_instr(t) :
    'if_instr           : IF expresion statement'
    t[0] =If(t[2], t[3])

def p_if_else_instr(t) :
    'if_instr     : IF expresion statement ELSE statement'
    t[0] =IfElse(t[2], t[3], t[5])

def p_if_elseif_instr(t) :
    'if_instr     : IF expresion statement ELSE if_instr'
    t[0] =IfElse(t[2], t[3], t[5])

def p_statement(t):
    'statement          :   LLAVIZQ instrucciones LLAVDER'
    t[0] = t[2]

def p_statement_vacio(t):  
    'statement          :   LLAVIZQ LLAVDER'
    t[0] = []

def p_instruccion_definicionMT(t):
    '''definicion_instr :   LET MUT ID DOSPUNTOS tipos IGUAL expresion'''
    t[0] = Definicion(t[3],TIPO_VAR.MUTABLE, t[5],t[7])

def p_instruccion_definicionIT(t):
    '''definicion_instr :   LET ID DOSPUNTOS tipos IGUAL expresion'''
    t[0] = Definicion(t[2],TIPO_VAR.INMUTABLE, t[4], t[6])

def p_instruccion_definicionM(t):
    '''definicion_instr :   LET MUT ID IGUAL expresion'''
    t[0] = Definicion(t[3],TIPO_VAR.MUTABLE, TIPO_DATO.VOID, t[5])

def p_instruccion_definicionI(t):
    '''definicion_instr :   LET ID IGUAL expresion'''
    t[0] = Definicion(t[2],TIPO_VAR.INMUTABLE,TIPO_DATO.VOID,t[4])

def p_tiposInt(t):
    '''tipos            :   INT'''
    t[0] = TIPO_DATO.INT64

def p_tiposFloat(t):
    '''tipos            :   FLOAT'''
    t[0] = TIPO_DATO.FLOAT64

def p_tiposBool(t):
    '''tipos            :   BOOLEAN'''
    t[0] = TIPO_DATO.BOOLEAN

def p_tiposChar(t):
    '''tipos            :   CHAR'''
    t[0] = TIPO_DATO.CHAR

def p_tiposStr(t):
    '''tipos            :   STRING'''
    t[0] = TIPO_DATO.STRING

def p_tiposIStr(t):
    '''tipos            :   I ISTRING'''
    t[0] = TIPO_DATO.ISTRING

def p_tiposusize(t):
    '''tipos            :   USIZE'''
    t[0] = TIPO_DATO.USIZE

def p_tiposStruct(t):
    'tipos            :   ID'
    t[0] = t[1]

def p_tipoVec(t):
    'tipos              :   VVEC MENQUE tipos MAYQUE'  
    t[0] = TIPO_DATO.VOID

def p_tipo_array(t):
    'tipos         :   CORCHIZQ tipos PTCOMA expresion CORCHDER'
    t[0] = TIPO_DATO.VOID

def p_tipo_arrayun(t):
    'tipos         :   CORCHIZQ tipos CORCHDER'
    t[0] = TIPO_DATO.VOID

def p_instruccion_imprimir(t) :
    '''imprimir_instr     : PRINTLN ADMIR PARIZQ CADENA PARDER'''
    t[0] =Imprimir(ExpresionDobleComilla(t[4], TIPO_DATO.ISTRING),parametros=[])

def p_instruccion_imprimir_p(t) :
    '''imprimir_instr     : PRINTLN ADMIR PARIZQ CADENA pparam PARDER'''
    t[0] =Imprimir(ExpresionDobleComilla(t[4], TIPO_DATO.ISTRING), t[5])

def p_lpparam(t):
    '''pparam                : pparam COMA expresion'''
    t[1].append(t[3])
    t[0] = t[1]

def p_pparam(t):
    '''pparam                :  COMA expresion'''
    t[0] = [t[2]]

def p_expresion_binaria(t):
    '''expresion        : expresion MAS expresion
                        | expresion MENOS expresion
                        | expresion POR expresion
                        | expresion DIVIDIDO expresion
                        | expresion MODULO expresion'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
    elif t[2] == '%': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MODULO)

def p_expresion_potencia_I(t):
    'expresion : INT DOSPUNTOS DOSPUNTOS POW PARIZQ expresion COMA expresion PARDER'
    t[0] = ExpresionPotencia(t[6],t[8],TIPO_DATO.INT64)

def p_expresion_potencia_F(t):
    'expresion : FLOAT DOSPUNTOS DOSPUNTOS POWF PARIZQ expresion COMA expresion PARDER'
    t[0] = ExpresionPotencia(t[6],t[8],TIPO_DATO.FLOAT64)

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion : ENTERO'''
    t[0] = ExpresionNumero(t[1],TIPO_DATO.INT64)

def p_expresion_numberd(t):
    '''expresion : DECIMAL'''
    t[0] = ExpresionNumero(t[1],TIPO_DATO.FLOAT64)

def p_expresion_cadena(t) :
    'expresion     : CADENA'
    t[0] = ExpresionDobleComilla(t[1],TIPO_DATO.ISTRING)

def p_expresion_caracter(t) :
    'expresion     : CARACTER'
    t[0] = ExpresionCaracter(t[1],TIPO_DATO.CHAR)

def p_expresion_logicaT(t) :
    'expresion     : TRUE'
    t[0] = ExpresionLogicaTF(True, TIPO_DATO.BOOLEAN)

def p_expresion_logicaF(t) :
    'expresion    : FALSE'
    t[0] = ExpresionLogicaTF(False, TIPO_DATO.BOOLEAN)

def p_expresion_rango(t):
    'expresion      :   expresion PUNTO PUNTO expresion'
    t[0] = ExpresionRango(t[1],t[4])

def p_expresion_idvectorial(t):
    'expresion      :   ID lista_corch'
    t[0] = ExpresionIdVectorial(t[1],t[2])

def p_llidarray(t):
    'lista_corch    :   lista_corch CORCHIZQ expresion CORCHDER'
    t[1].append(t[3])
    t[0] = t[1]

def p_lidarray(t):
    'lista_corch    :   CORCHIZQ expresion CORCHDER'
    t[0] = [t[2]]

def p_expresion_relacional(t):
    '''expresion     :      expresion MAYQUE expresion
                        |   expresion MENQUE expresion
                        |   expresion IGUALQUE expresion
                        |   expresion NIGUALQUE expresion
                        |   expresion MAYORIGUAL expresion
                        |   expresion MENORIGUAL expresion
                        |   expresion OR expresion
                        |   expresion AND expresion''' 
    
    if t[2] == '>'    : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == '<'  : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == '==' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == '!=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.DIFERENTE)
    elif t[2] == '>=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MAYORIGUAL)
    elif t[2] == '<=' : t[0] = ExpresionRelacionalBinaria(t[1], t[3], OPERACION_LOGICA.MENORIGUAL)
    elif t[2] == '||'     : t[0] = ExpresionLogicaBinaria(t[1],t[3], OPERACION_LOGICA.OR)
    elif t[2] == '&&'   : t[0] = ExpresionLogicaBinaria(t[1],t[3], OPERACION_LOGICA.AND)

def p_expresion_logica_unaria(t):
    'expresion       :   ADMIR expresion %prec NOT'
    t[0] = ExpresionNot(t[2])

def p_expresion_init(t):
    '''expresion    :   expresion_if
                    |   expresion_match
                    |   expresion_vectorial
                    |   expresion_array
                    |   expresion_loop
                    |   llamado_instr
                    |   remove_instr'''
    t[0] = t[1]

def p_expresion_struct(t):
    'expresion      :   ID LLAVIZQ struct_dicc LLAVDER'
    t[0] = ExpresionStruct(t[1],t[3])

def p_struct_dicc(t):
    'struct_dicc    :   struct_dicc COMA ID DOSPUNTOS expresion'
    t[1].append(StructAtributo(t[3],t[5]))
    t[0] = t[1]

def p_struct_diccU(t):
    'struct_dicc    :   ID DOSPUNTOS expresion'
    t[0] = [StructAtributo(t[1],t[3])]

def p_expresion_accesoStruct(t):
    'expresion      :   ID lids'
    t[0] = AccesoStruc(t[1],t[2])

def p_expresion_llids(t):
    'lids       :  lids PUNTO ID'
    t[1].append(t[3])
    t[0] = t[1]

def p_expresion_lids(t):
    'lids       :   PUNTO ID'
    t[0] = [t[2]]

def p_expresion_len(t):
    'expresion      :   expresion PUNTO LEN PARIZQ PARDER'
    t[0] = Len(t[1])

def p_expresion_lenid(t):
    'expresion      :   ID PUNTO LEN PARIZQ PARDER'
    t[0] = Len(ExpresionIdentificador(t[1]))

def p_exp_contains(t):
    'expresion      :   ID PUNTO CONTAINS PARIZQ I expresion PARDER'
    t[0] = Contains(t[1],t[6])

def p_exp_capacity(t):
    'expresion      :   ID PUNTO CAPACITY PARIZQ PARDER'
    t[0] = Capacity(t[1])

def p_expresion_loop(t):
    'expresion_loop     :   LOOP statement'
    t[0] = ExpresionLoop(t[2])

def p_expresion_match(t):
    'expresion_match    :   MATCH expresion LLAVIZQ lmatchexp LLAVDER'
    t[0] = ExpresionMatch(t[2], t[4])

def p_expresion_matchid(t):
    'expresion_match    :   MATCH ID LLAVIZQ lmatchexp LLAVDER'
    t[0] = ExpresionMatch(ExpresionIdentificador(t[2]), t[4])

def p_llmatchexp(t):
    'lmatchexp          :   lmatchexp matchexp'
    t[1].append(t[2])
    t[0] = t[1]

def p_lmatchexp(t):
    'lmatchexp          :   matchexp'
    t[0] = [t[1]]

def p_matchexp(t):
    'matchexp           :   listcoincidencia FLECHAMATCH expresion COMA'
    t[0] = OpcionMatch(t[1],t[3])

def p_matchexp_default(t):
    'matchexp           :   DEFAULT FLECHAMATCH expresion COMA'
    t[0] = OpcionMatch(TIPO_DATO.VOID,t[3])

def p_expresion_if(t):
    'expresion_if      :       IF expresion statement_expresion ELSE statement_expresion'
    t[0] = ExpresionIf(t[2],t[3],t[5])

def p_expresion_if_elifid(t):
    'expresion_if      :       IF ID statement_expresion ELSE expresion_if'
    t[0] = ExpresionIf(ExpresionIdentificador(t[2]),t[3],t[5])

def p_expresion_if_elif(t):
    'expresion_if      :       IF expresion statement_expresion ELSE expresion_if'
    t[0] = ExpresionIf(t[2],t[3],t[5])

def p_statement_expresion(t):
    'statement_expresion    :   LLAVIZQ expresion LLAVDER'
    t[0] = t[2]

def p_to_string(t):
    '''expresion  :   expresion PUNTO TOSTRING PARIZQ PARDER
                    | expresion PUNTO TOOWNED PARIZQ PARDER'''
    t[0] = ToString(t[1])

def p_to_stringId(t):
    '''expresion  :   ID PUNTO TOSTRING PARIZQ PARDER
                    | ID PUNTO TOOWNED PARIZQ PARDER'''
    t[0] = ToString(ExpresionIdentificador(t[1]))

def p_abs(t):
    'expresion  :   expresion PUNTO ABS PARIZQ PARDER'
    t[0] = Abs(t[1])

def p_absid(t):
    'expresion  :   ID PUNTO ABS PARIZQ PARDER'
    t[0] = Abs(ExpresionIdentificador(t[1]))

def p_sqrt(t):
    'expresion  :   expresion PUNTO SQRT PARIZQ PARDER'
    t[0] = Sqrt(t[1])

def p_sqrtid(t):
    'expresion  :   ID PUNTO SQRT PARIZQ PARDER'
    t[0] = Sqrt(ExpresionIdentificador(t[1]))

def p_casteo(t):
    'expresion  :   expresion AS tipos'
    t[0] = Casteo(t[1],t[3])

def p_expresion_vector_vacio(t):
    'expresion_vectorial      :   VVEC DOSPUNTOS DOSPUNTOS NEW PARIZQ PARDER'
    t[0] = ExpresionVec([],TIPO_DATO.VOID)

def p_expresion_vec_wcapacity(t):
    'expresion_vectorial      :   VVEC DOSPUNTOS DOSPUNTOS WCAPACITY PARIZQ expresion PARDER'
    t[0] = ExpresionVec([],TIPO_DATO.VOID,t[6])

def p_expresion_vector(t):
    '''expresion_vectorial      :   VEC ADMIR CORCHIZQ lista_vectorial CORCHDER
                                |   VEC ADMIR CORCHIZQ valores_repetidos CORCHDER'''
    t[0] = ExpresionVec(t[4], TIPO_DATO.VOID)

def p_expresion_array(t):
    '''expresion_array      :   CORCHIZQ lista_vectorial CORCHDER
                            |   CORCHIZQ valores_repetidos CORCHDER'''
    t[0] = ExpresionArray(t[2], TIPO_DATO.VOID)

def p_expresion_valores_repetidos(t):
    'valores_repetidos          :   expresion PTCOMA expresion'
    t[0] = ValoresRepetidos(t[1],t[3])

def p_llista_vectorial(t):
    '''lista_vectorial    :   lista_vectorial COMA expresion'''
    t[1].append(t[3])
    t[0] = t[1]

def p_lista_vectorial(t):
    '''lista_vectorial    :   expresion'''
    t[0] = [t[1]]

# Error sintactico
def p_error(p):
    print(f'Error de sintaxis {p.value!r} en {p.lineno!r}')

from ply.yacc import yacc
parser = yacc(debug=True)


def parse(input) :
    return parser.parse(input)