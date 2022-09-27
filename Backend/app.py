from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from instrucciones import Llamado

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

  #Ejecutar.guardarFunciones(instrucciones, ts_global)

  #consola = Ejecutar.procesar_instrucciones([Llamado("main",[])], ts_global)['consola']

  objeto = {
            'Mensaje': 'En Progreso'
        }

  return jsonify(objeto)


if __name__ == "__main__":
    app.run(debug=True)