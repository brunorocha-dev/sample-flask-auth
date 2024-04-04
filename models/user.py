from database import db
# Vai permitir as autenticações dos usuários(a classe UserMixin existe várias funções)
from flask_login import UserMixin 
# Classe vai ser herdada de outra classe do BD Model(Flask e SQLAlchemy vai reconhecer que é algo mapeado)
# Herança múltipla -> vai ter tudo da Model e UserMixin
class User(db.Model, UserMixin):
    # id(int), username(text), password(text)
    id = db.Column(db.Integer, primary_key=True) # Chave única
    username = db.Column(db.String(80), nullable=False, unique=True) # limitando as minhas caracteres / Não aceita valor em branco com a propriedade nullabe / valor única.
    password = db.Column(db.String(80), nullable=False, unique=False)