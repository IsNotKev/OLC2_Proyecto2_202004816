import './App.css';

import React, { useRef } from "react";
import ReactDOM from "react-dom";

import Editor from "@monaco-editor/react";

function App() {

  const editorRef = useRef(null);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  function mostrarDatos(){
    alert("PROYECTO 2 \nOrganización de Lenguajes y Compiladores 2 \nKevin Steve Martinez Lemus - 202004816")
  }

  function compilar() {
    var obj = { 'codigo': editorRef.current.getValue() }

    if (editorRef.current.getValue() != ""){
      fetch(`http://localhost:5000/compilar`, {
      method: 'POST',
      body: JSON.stringify(obj),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      }
    })
      .then(res => res.json())
      .catch(err => {
        console.error('Error:', err)
        alert("Ocurrio un error, ver la consola")
      })
      .then(response => {
        document.getElementById('consola').textContent = response.Mensaje;
      })
    }else{
      alert("Escriba código para ejecutar.")
    }
    
  }

  return (
    <div className="App">
      <header className="App-header">

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style={{ width: '100%' }}>
          <div class="container-fluid">
            <a class="navbar-brand" href="#">DB Rust</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto mb-2 mb-lg-0">

                <li class="nav-item dropdown">
                  <a class="nav-link active" style={{ cursor: 'pointer' }} role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Compilador
                  </a>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }} onClick={compilar}>Compilar</a></li>
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }}>Optimizar por Mirilla</a></li>
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }}>Optimizar por bloques</a></li>
                  </ul>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" style={{ cursor: 'pointer' }} role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Reportes
                  </a>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }}>Reporte de tabla de símbolos</a></li>
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }}>Reporte de errores</a></li>
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }}>Reporte de base de datos existente</a></li>
                    <li><a class="dropdown-item" style={{ cursor: 'pointer' }}>Reporte de optimización</a></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a class="nav-link" style={{ cursor: 'pointer' }} onClick={mostrarDatos}>Acerca De</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className='row flex-grow-1' style={{ marginTop: '8%' }}>
          <Editor
            height="75vh"
            width="60vh"
            defaultValue="// Empieza con Rust
                          fn main(){
                            
                          }"
            onMount={handleEditorDidMount}
            className={'rounded-xl'}
            theme="vs-dark"
            options={{
              minimap: {
                enabled: false
              }
            }}
          />
          <textarea disabled style={{ width: '70vh', height: '75vh', background: 'black', color: 'white', fontSize: '13px' }} id="consola"></textarea>
        </div>

      </header>
    </div>
  );
}

export default App;
