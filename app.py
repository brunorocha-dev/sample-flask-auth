from flask import Flask, jsonify, request
from models.user import User
from database import db 
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
# Configurações para o flask: (proteger as informações armazenadas)
app.config["SECRET_KEY"] = "your_secret_key"
# URI - Caminho aonde o banco vai ser conectado SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
# view login
login_manager.login_view = "login"
#  ‘ session ‘ ← Conexão ativa

@login_manager.user_loader
def load_user(user_id): # nenhum valor for fornecido para callback quando a função load_user é chamada, o valor de callback será None.
    return User.query.get(user_id)

# Recebendo as credenciais no corpo da requisição
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        #login
        # Recuperando registros de usuário na base de dados.
        user = User.query.filter_by(username=username).first()
        # verificação -> se ta existindo usuário e se a senha cadastrada bate a mesma do Postman.
        if user and user.password == password:
            login_user(user) # Autenticação
            print(current_user.is_authenticated) # Armazena se esse usuário está autenticado, imprimindo na tela
            return jsonify ({"message": "Autenticação realizada com sucesso"}), 200
         
    return jsonify ({"message": "Credenciais inválidas"}), 400

@app.route("/hello-world", methods=["GET"])
def hello_word():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)