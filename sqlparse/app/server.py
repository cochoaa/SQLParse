from flask import Flask, render_template,send_from_directory,request, jsonify
from statamentService import select_converter
import os
app = Flask(__name__)
# app.add_url_rule('/favicon.ico',
#                  redirect_to=url_for('static', filename='img/favicon.png'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    data = {
        'titulo': 'Programa Automatico de Procesamiento Unificado'
    }
    return render_template('index.html', data=data)

@app.route('/converter')
def conveter():
    data = {
        'titulo': 'Converter',
        'querys_input': '',
        'querys_output': ''
    }
    return render_template('converter_statament.html', data=data)

@app.route('/api/converter',methods=['POST'])
def api_conveter():
    data_input = request.get_json()
    list_stataments=select_converter(data_input.get('querys_input'))
    data_output = {
        'queries_output': list_stataments
    }
    return jsonify(data_output)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000,debug=True)
