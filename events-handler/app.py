# print("Hola Mundo desde Python, saludos!!!")
from flask import Flask, request, render_template, url_for, jsonify, session
from werkzeug.utils import redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

app.secret_key = 'llave_secreta'


# http://localhost:5000/
@app.route('/')
def inicio():
    if 'username' in session:
        return f'usuario loggeado {session["username"]}'
    return 'usuario no loggeado'
    # app.logger.debug('mensaje debug')
    app.logger.info(f'entramos al path {request.path}')
    # app.logger.warn('mensaje warn')
    # app.logger.error('mensaje error')
    return 'Hello, from Flask!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        session['username'] = usuario
        return redirect(url_for('inicio'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('inicio'))


@app.route('/saludar/<nombre>')
def saludar(nombre):
    return f'Saludos {nombre}'


@app.route('/edad/<int:age>')
def show_age(age):
    return f'Tu edad es: {age + 1}'


@app.route('/mostrar/<nombre>', methods=['GET', 'POST'])
def show_name(nombre):
    return render_template('mostrar.html', nombre=nombre)


@app.route('/redireccionar')
def redireccionar():
    return redirect(url_for('show_name', nombre='Juan'))


@app.route('/salir')
def salir():
    return abort(404)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', error=error), 404


fruits = [{"corres": "j@gmail.com", "pass": 1}, {"corres": "m@gmail.com", "pass": 1},
          {"corres": "a@gmail.com", "pass": 1}, {"corres": "b@gmail.com", "pass": 1}]


@app.route('/api/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_json(nombre):
    valores = {'nombre': nombre, 'methodo_http': request.method}
    return jsonify(fruits)


def delete_nombre(lista, correo):
    return lista['corres'] != correo


def filtro_nombre(lista, correo):
    return lista['corres'] == correo
    # lista_filtrada = []
    # for i in lista :
    #     print(i)
    #     if i['corres'] == correo :
    #         lista_filtrada.append(i)
    # return lista_filtrada


@app.route('/api/mostrando/<nombre>', methods=['GET', 'POST'])
def mostrando_json(nombre):
    global fruits
    # valores = {'nombre': nombre, 'methodo_http': request.method}
    # fruits.append(nombre)
    # x = filtro_nombre(fruits, nombre)
    x = list(filter(lambda item: delete_nombre(item, nombre), fruits))
    fruits = x
    return jsonify(fruits)


@app.route('/api/actualizar/<correo>/<pwd>', methods=['GET', 'POST'])
def actualizando_json(correo, pwd):
    global fruits
    lista_filtrada = []
    for i in fruits:
        print(i)
        if i['corres'] == correo:
            lista_filtrada.append({'corres': correo, 'pass': int(pwd)})
        else:
            lista_filtrada.append(i)
    fruits = lista_filtrada
    return jsonify(fruits)
