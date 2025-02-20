from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, RadioField, IntegerField, EmailField
from wtforms.validators import DataRequired, NumberRange

class ZodiacoForms(Form):
    nombre = StringField('Nombre', [
        DataRequired(message="Debe de llenarse el campo")
    ])
    apePat = StringField('Apellido Paterno', [
        DataRequired(message="Debe de llenarse el campo")
    ])
    apeMat = StringField('Apellido Materno', [
        DataRequired(message="Debe de llenarse el campo")
    ])
    dia = IntegerField('Día', [
        DataRequired(message="El campo día no puede estar vacio"),
        NumberRange(min=1, max=31, message="El día debe estar entre 1 y 31")
    ])
    mes = IntegerField('Mes', [
        DataRequired(message="El campo mes no puede estar vacio"),
        NumberRange(min=1, max=12, message="El mes debe estar entre 1 y 12")
    ])
    anio = IntegerField('Año', [
        DataRequired(message="El campo año no puede estar vacio"),
        NumberRange(min=1900, max=2100, message="El año debe estar entre 1900 y 2100")
    ])
    sexo = RadioField('Sexo', [
        DataRequired(message="Selecciona tu sexo")
        ],choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])