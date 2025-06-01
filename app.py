from flask import Flask, request, jsonify; 
from lex import realizar_analisis_lexico, realizar_analisis_sintactico, ejecutar_codigo
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Leer el contenido del archivo HTML
def get_html_content():
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
        </head>
        <body>
            <h1>Error: No se encontró el archivo index.html</h1>
            <p>Asegúrate de que el archivo index.html esté en el mismo directorio que app.py</p>
        </body>
        </html>
        """

@app.route('/')
def home():
    """Ruta principal que sirve el archivo HTML"""
    html_content = get_html_content()
    return render_template_string(html_content)

@app.route('/lexico', methods=['POST'])
def analisis_lexico():
    """Ruta para el análisis léxico"""
    try:
        data = request.get_json()
        if not data or 'codigo' not in data:
            return jsonify({'error': 'No se proporcionó código para analizar'}), 400
        
        codigo = data['codigo']
        resultado = realizar_analisis_lexico(codigo)
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error': f'Error en el análisis léxico: {str(e)}'}), 500

@app.route('/sintactico', methods=['POST'])
def analisis_sintactico():
    """Ruta para el análisis sintáctico"""
    try:
        data = request.get_json()
        if not data or 'codigo' not in data:
            return jsonify({'error': 'No se proporcionó código para analizar'}), 400
        
        codigo = data['codigo']
        resultado = realizar_analisis_sintactico(codigo)
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error': f'Error en el análisis sintáctico: {str(e)}'}), 500

@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    """Ruta para ejecutar código"""
    try:
        data = request.get_json()
        if not data or 'codigo' not in data:
            return jsonify({'error': 'No se proporcionó código para ejecutar'}), 400
        
        codigo = data['codigo']
        resultado = ejecutar_codigo(codigo)
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error': f'Error en la ejecución: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📝 Asegúrate de que index.html esté en el mismo directorio")
    print("🌐 El servidor estará disponible en: http://localhost:5000")
    
    # Verificar si existe el archivo HTML
    if os.path.exists('index.html'):
        print("✅ Archivo index.html encontrado")
    else:
        print("⚠️  Advertencia: No se encontró index.html")
    
    app.run(debug=True, host='0.0.0.0', port=5000)