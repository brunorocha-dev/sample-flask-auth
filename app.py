from flask import Flask, jsonify, request
from models.user import User
from database import db 
from flask_login import LoginManager

app = Flask(__name__)
# Configurações para o flask: (proteger as informações armazenadas)
app.config["SECRET_Key"] = "your_secret_key"
# URI - Caminho aonde o banco vai ser conectado SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
# view login

#  ‘ session ‘ ← Conexão ativa

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        #login
        # Recuperando registros de usuário na base de dados.
        user = User.query.filter_by(username=username).first()
        # verificação -> se ta existindo usuário e se a senha ta a mesma do Postman.
        if user and user.password == password:
            return jsonify ({"message": "Autenticação realizada com sucesso"}), 200
         
    return jsonify ({"message": "Credenciais inválidas"}), 400

@app.route("/hello-world", methods=["GET"])
def hello_word():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)