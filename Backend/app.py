from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from instrucciones import Llamado
from Generador3D import Generador3D

import gramatica as g
import ts as TS
import ejecutar as Ejecutar

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "<h1>Hola Mundo x20000 vez</h1>"

@app.route("/compilar",methods=['POST'])
def ejecutar():
  codigo = request.json['codigo']

  instrucciones = g.parse(codigo)
  ts_global = TS.TablaDeSimbolos()
  Generador3DInstancia = Generador3D()
  

  Ejecutar.guardarFunciones(instrucciones, ts_global)

  if ts_global.existeFuncion("main"):
    instrucciones = ts_global.obtenerFuncion("main").instrucciones
    for instr in instrucciones:
      Generador3DInstancia.agregarInstruccion(Ejecutar.procesar_instrucciones(instr, ts_global, Generador3DInstancia))
  else:
    salida = "No Existe Función Main."
  
  salida = Generador3DInstancia.generarMain()
  objeto = {
            'Mensaje': salida
        }

  return jsonify(objeto)


if __name__ == "__main__":
    app.run(debug=True)