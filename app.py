from flask import Flask, jsonify, request
from models.user import User
from database import db 
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

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
def load_user(user_id):
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
            return jsonify ({"message": "Autenticação realizada com sucesso"})
         
    return jsonify ({"message": "Credenciais inválidas"}), 400

# logout do usuário
@app.route("/logout", methods=["GET"]) 
# a partir daqui esta rota vai estar protegida.
@login_required 
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

# CRUD - Create
@app.route("/user", methods=["POST"]) 
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify ({"message": "Usuário cadastrado com sucesso!"})
        
    return jsonify ({"message": "Dados inválidos"}), 400

# CRUD - Read
@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    
    if user:
        return {"username": user.username}
    
    return jsonify({"message": "Usuário não encontrado!"}), 404

# CRUD - Update
@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)
    
    if user and data.get("password") :
        user.password = data.get("password")
        db.session.commit()
         
        return jsonify({"message": f"Usuário '{id_user}' atualizado com sucesso!"})
    
    return jsonify({"message": "Usuário não encontrado!"}), 404

    
@app.route("/hello-world", methods=["GET"])
def hello_word():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)