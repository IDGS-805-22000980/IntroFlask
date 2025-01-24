from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Word!, Si"

@app.route("/Hola")
def hola():
    return "Hola de nuevo"

if __name__ == "__main__":
    app.run(debug=True)
