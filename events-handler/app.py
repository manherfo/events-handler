# print("Hola Mundo desde Python, saludos!!!")
from flask import Flask, request, render_template, url_for, jsonify, session
from werkzeug.utils import redirect
from werkzeug.exceptions import abort
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'llave_secreta'
users = [
    {
        "email": "a@gmail.com",
        "pwd": "1",
        "events": [
            {
                "name": "a",
                "category": "a",
                "place": "a",
                "address": "a"
            },
            {
                "name": "b",
                "category": "b",
                "place": "b",
                "address": "b"
            }
        ]
    },
    {
        "email": "b@gmail.com",
        "pwd": "1",
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
        "pwd": "1",
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
        "pwd": "1",
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


@app.route('/login/<email>', methods=['GET', 'POST'])
def login(email):
    if request.method == 'POST':
        session['username'] = email
        return redirect(url_for('inicio'))
    return render_template('login.html')


@app.route('/signup/<email>/<pwd>', methods=['GET', 'POST'])
@cross_origin()
def signup(email, pwd):
    global users
    new_user = {"email": email, "pwd": pwd, "events": []}
    users.append(new_user)
    return jsonify(users)


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
@cross_origin()
def user_details(email):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    x = list(filter(lambda users_list: find_user(users_list, email), users))
    return jsonify(x)


def validate_pwd(user, email, pwd):
    return user['pwd'] == pwd and user['email'] == email


@app.route('/validate-pwd/<email>/<pwd>', methods=['GET', 'POST'])
@cross_origin()
def validate_user(email,pwd):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    x = list(filter(lambda users_list: validate_pwd(users_list, email, pwd), users))
    return jsonify(x)


def delete_user(users_list, email):
    return users_list['email'] != email


@app.route('/delete-user/<email>', methods=['GET', 'POST'])
def delete_users(email):
    global users
    # valores = {'email': email, 'methodo_http': request.method}
    # users.append(email)
    # x = filtro_nombre(users, email)
    user = list(filter(lambda users_list: delete_user(users_list, email), users))
    users = user
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
    user = list(filter(lambda users_list: find_user(users_list, email), users))
    return jsonify(user)
