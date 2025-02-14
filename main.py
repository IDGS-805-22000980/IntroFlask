from flask import Flask, render_template, request

import forms

app=Flask(__name__)

@app.route("/")
def index():
    titulo="IDGS801"
    lista=["Pedro", "Juan", "Mario"]
    return render_template("index.html",titulo=titulo,lista=lista)

@app.route("/alumnos", methods=["POST", "GET"])
def alumnos():
    mat = ''
    nom = ''
    ape = ''
    email = ''
    alumno_clase = forms.UserForm(request.form)
    if request.method == "POST":
        mat = alumno_clase.matricula.data
        ape = alumno_clase.apellido.data
        nom = alumno_clase.nombre.data
        email = alumno_clase.email.data
        print('Nombre {}'.format(nom))
    return render_template("Alumnos.html", form=alumno_clase)

        


@app.route("/ejemplo1")
def ejemplo1():
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/Hola")
def hola():
    return "Hola Mundo!!"

@app.route("/user/<string:user>")
def user(user):
    return f"Hola, {user}!"

@app.route("/numero/<int:n>")
def numero(n):
    return f"El numero es: {n}"

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return f"El usuario es: {username} con id: {id}"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return f"La suma es: {n1+n2}"

@app.route("/default/")
@app.route("/default/<string:tem>")
def func1(tem='Juan'):
    return f"Hola, {tem}!"

@app.route("/form1/")
def form1():
    return '''
            <form>
            <label for="nombre">Nombre:</lable>
            <input type="text" id="nombre" name="nombre"> </input>
            </form>

            '''
@app.route("/OperasBas")
def operas():
    return render_template("OperasBas.html", n1="", n2="", operacion="", resultado="")

@app.route("/resultado", methods=["POST"])
def result():
    num1 = request.form.get("n1")
    num2 = request.form.get("n2")
    operacion = request.form.get("operacion")
    resultado = ""

    try:
        num1 = float(num1)
        num2 = float(num2)

        if operacion == "suma":
            resultado = num1 + num2
        elif operacion == "resta":
            resultado = num1 - num2
        elif operacion == "multiplicacion":
            resultado = num1 * num2
        elif operacion == "divicion":
            if num2 != 0:  # Verifica que no se divida por cero
                resultado = num1 / num2
            else:
                resultado = "Error: División por cero no permitida."
    except ValueError:
        resultado = "Error: Entrada no válida."

    # Renderiza la misma plantilla con los valores ingresados y el resultado
    return render_template("OperasBas.html", n1=request.form.get("n1"), n2=request.form.get("n2"), operacion=operacion, resultado=resultado)
    
    """
    if request.method == "POST":
        num1 = request.form.get("n1")
        num2 = request.form.get("n2")
        return "La multiplicación de {} x {} = {}".format(num1,num2, str(int(num1)*int(num2)))
"""


# Lógica para realizar la consulta del Cinépolis
class Personas:
    def __init__(self):
        self.historial = []
    
    def calcularTotal(self, boletos, tarjeta):
        if boletos <= 0:
            return 0 
        
        if boletos <= 2:
            cost = 12 * boletos
        elif boletos <= 5:
            cost = 12 * boletos * 0.90
        else:
            cost = 12 * boletos * 0.85
        
        if tarjeta == "si":
            cost *= 0.90 
        
        return round(cost, 2)

personas = Personas()

@app.route('/cinepolis', methods=['GET', 'POST'])
def cinepolis():
    mensaje = None
    nombre = ""
    cantidad_compradores = 0
    tarjeta = "no"
    cantidad_boletos = 0
    total = 0

    if request.method == "POST":
        nombre = request.form.get('nombre', "").strip()
        tarjeta = request.form.get('tarjeta', "no")

        try:
            cantidad_compradores = int(request.form.get('cantidad_compradores', 0))
            cantidad_boletos = int(request.form.get('cantidad_boletos', 0))
        except ValueError:
            mensaje = "Por favor, ingrese valores numéricos válidos."
            return render_template('cinepolis.html', mensaje=mensaje)

        if cantidad_compradores <= 0:
            mensaje = "Debe haber al menos un comprador."
        elif cantidad_boletos <= 0:
            mensaje = "Debe comprar al menos un boleto."
        else:
            max_boletos = cantidad_compradores * 7
            if cantidad_boletos > max_boletos:
                mensaje = f"Has excedido el número máximo de boletos permitidos ({max_boletos})."
            else:
                total = personas.calcularTotal(cantidad_boletos, tarjeta)
                personas.historial.append((nombre, total))

    return render_template(
        'cinepolis.html',
        mensaje=mensaje,
        nombre=nombre,
        cantidad_compradores=cantidad_compradores,
        tarjeta=tarjeta,
        cantidad_boletos=cantidad_boletos,
        total=total
    )


if __name__ == "__main__":
    app.run(debug=True, port=3000)