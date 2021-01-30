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


users = [{"email": "a@gmail.com", "pwd": 1}, {"email": "b@gmail.com", "pwd": 1},
         {"email": "c@gmail.com", "pwd": 1}, {"email": "d@gmail.com", "pwd": 1}]


@app.route('/api/mostrar/<nombre>', methods=['GET', 'POST'])
def mostrar_json(nombre):
    valores = {'nombre': nombre, 'methodo_http': request.method}
    return jsonify(users)


@app.route('/list-users', methods=['GET', 'POST'])
def list_users():
    global users
    return jsonify(users)


def filtro_nombre(lista, email):
    return lista['email'] == email
    # lista_filtrada = []
    # for i in lista :
    #     print(i)
    #     if i['email'] == email :
    #         lista_filtrada.append(i)
    # return lista_filtrada


@app.route('/user-details/<email>', methods=['GET', 'POST'])
def mostrando_json(email):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    x = list(filter(lambda item: filtro_nombre(item, email), users))
    return jsonify(x)


def delete_user(lista, email):
    return lista['email'] != email


@app.route('/delete-user/<email>', methods=['GET', 'POST'])
def delete_users(email):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    x = list(filter(lambda item: delete_user(item, email), users))
    users = x
    return jsonify(users)


@app.route('/update-pwd/<email>/<pwd>', methods=['GET', 'POST'])
def update_pwd(email, pwd):
    global users
    filtered_users = []
    for i in users:
        print(i)
        if i['email'] == email:
            filtered_users.append({'email': email, 'pwd': pwd})
        else:
            filtered_users.append(i)
    users = filtered_users
    return jsonify(users)
