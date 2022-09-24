
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.modelo_base import ModeloBase
from flask_app.utils.regex import REGEX_CORREO_VALIDO

class Usuario(ModeloBase):

    modelo = 'users'
    campos = ['first_name', 'last_name','email','pasword']

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pasword = data['pasword']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def buscar(cls, dato):
        query = "SELECT * FROM users WHERE email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL("esquema_login").query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = """UPDATE usuarios 
                        SET first_name = %(first_name)s,
                        SET last_name = %(last_name)s,
                        SET email = %(email)s,
                        SET password = %(password)s,
                        updated_at = NOW() 
                        created_at = NOW() 
                    WHERE id = %(id)s"""
        resultado = connectToMySQL("esquema_login").query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True

        is_valid = cls.validar_largo(data, 'first_name', 3)
        is_valid = cls.validar_largo(data, 'last_name', 3)

        if not REGEX_CORREO_VALIDO.match(data['email']):
            flash('El correo no es válido', 'error')
            is_valid = False

        if data['pasword'] != data['cpassword']:
            flash('las contraseñas no son iguales', 'error')
            is_valid = False

        if cls.validar_existe('email', data['email']):
            flash('el correo ya fue ingresado', 'error')
            is_valid = False

        return is_valid