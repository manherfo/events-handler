# print("Hola Mundo desde Python, saludos!!!")
from flask import Flask, request, render_template, url_for, jsonify, session
from werkzeug.utils import redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = 'llave_secreta'
users = [
    {
        "email": "a@gmail.com",
        "name": "a",
        "pwd": 1,
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    },
    {
        "email": "b@gmail.com",
        "name": "b",
        "pwd": 1,
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    },
    {
        "email": "c@gmail.com",
        "name": "c",
        "pwd": 1,
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    },
    {
        "email": "d@gmail.com",
        "name": "d",
        "pwd": 1,
        "events": [
            {
                "name": "",
                "category": "",
                "place": "",
                "address": ""
            }
        ]
    }
]


def find_user(lista, email):
    return lista['email'] == email
    # lista_filtrada = []
    # for i in lista :
    #     print(i)
    #     if i['email'] == email :
    #         lista_filtrada.append(i)
    # return lista_filtrada


# http://localhost:5000/
@app.route('/')
def inicio():
    if 'username' in session:
        x = list(filter(lambda users_list: find_user(users_list, session["username"]), users))
        return jsonify(x)
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


@app.route('/salir')
def salir():
    return abort(404)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error404.html', error=error), 404


@app.route('/list-users', methods=['GET', 'POST'])
def list_users():
    global users
    return jsonify(users)


@app.route('/user-details/<email>', methods=['GET', 'POST'])
def user_details(email):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    x = list(filter(lambda users_list: find_user(users_list, email), users))
    return jsonify(x)


def delete_user(users_list, email):
    return users_list['email'] != email


@app.route('/delete-user/<email>', methods=['GET', 'POST'])
def delete_users(email):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    x = list(filter(lambda users_list: delete_user(users_list, email), users))
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
