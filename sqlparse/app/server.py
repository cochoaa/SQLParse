from flask import Flask, render_template,send_from_directory
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
        'titulo': 'Convesor de Sentencias SQL'
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
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000,debug=True)
