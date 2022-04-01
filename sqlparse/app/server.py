from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Usage: http://<hostname>[:<prt>]/api/<url>"

if __name__ == '__main__':
    app.run(host="0.0.0.0")

@app.route("/api/restore")
def api(parameter):
    return 'Parametro: '+parameter