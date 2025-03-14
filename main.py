from flask import Flask, render_template, request
import forms
import forms_zodiaco
from datetime import datetime
from flask import g #Crear variables globales
from flask import flash #Enviar mensajes Flash tipo alertas
from flask_wtf.csrf import CSRFProtect


app=Flask(__name__)
app.secret_key='esta es una clave secreta'
csrf = CSRFProtect()

#Manejo de errores de tipo 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    g.nombre='Mario'
    print("before 1")

app.after_request
def after_request(response):
    print("after 1")
    return response

@app.route("/")
def index():
    titulo="IDGS801"
    lista=["Pedro", "Juan", "Mario"]
    return render_template("index.html",titulo=titulo,lista=lista)

@app.route("/alumnos", methods=["POST", "GET"])
def alumnos():
    print("Alumno {}".format(g.nombre))
    mat = ''
    nom = ''
    ape = ''
    email = ''
    alumno_clase = forms.UserForm(request.form)
    if request.method == "POST" and alumno_clase.validate():
        mat = alumno_clase.matricula.data
        ape = alumno_clase.apellido.data
        nom = alumno_clase.nombre.data
        email = alumno_clase.email.data
        mensaje='Bienvenido {}'.format(nom)
        flash(mensaje)
    return render_template("Alumnos.html", form=alumno_clase,mat=mat,nom=nom,ape=ape,email=email)


def obtener_signo_zodiaco_chino(anio):
    signos = ["Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey", "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"]
    while anio >= 12:  
        anio -= 12  
    return signos[anio]
#Sección para el Zodiaco Chino
@app.route("/zodiaco", methods=["POST", "GET"])
def zodiaco():
    nombre =''
    apePat = ''
    apeMat = ''
    dia = ''
    mes = ''
    anio = ''
    sexo = ''
    signo_zodiaco = ''
    edad = ''
    
    zodiaco_clase = forms_zodiaco.ZodiacoForms(request.form)
    if request.method == "POST" and zodiaco_clase.validate():
        nombre = zodiaco_clase.nombre.data
        apePat = zodiaco_clase.apePat.data
        apeMat = zodiaco_clase.apeMat.data
        dia = zodiaco_clase.dia.data
        mes = zodiaco_clase.mes.data
        anio = zodiaco_clase.anio.data
        sexo = zodiaco_clase.sexo.data
        
        try:
            dia = int(dia)
            mes = int(mes)
            anio = int(anio)

            fecha_actual = datetime.now()
            edad = fecha_actual.year - anio
            if (mes > fecha_actual.month) or (mes == fecha_actual.month and dia > fecha_actual.day):
                edad -= 1
            signo_zodiaco = obtener_signo_zodiaco_chino(int(anio))
        except ValueError:
            edad = 0
            signo_zodiaco = "Fecha no válida"
        
    
    return render_template("zodiaco_chino.html", form=zodiaco_clase, nombre=nombre, 
                        apePat=apePat, apeMat=apeMat, dia=dia, mes=mes, anio=anio, sexo=sexo, edad=edad, signo_zodiaco=signo_zodiaco)
    
        


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
    csrf.init_app(app)
    app.run(debug=True, port=3000)