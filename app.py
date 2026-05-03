from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'segredo_super_secreto'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Usuário já existe"}), 400

    user = User(
        username=data['username'],
        password=data['password']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado com sucesso"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()

    if not user or user.password != data['password']:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify(access_token=access_token), 200


@app.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.get_json()

    expense = Expense(
        title=data['title'],
        amount=data['amount'],
        category=data['category'],
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({"msg": "Gasto criado com sucesso"}), 201


@app.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()

    filter_type = request.args.get('filter')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Expense.query.filter_by(user_id=user_id)

    if filter_type == "week":
        date_limit = datetime.utcnow() - timedelta(days=7)
        query = query.filter(Expense.date >= date_limit)

    elif filter_type == "month":
        date_limit = datetime.utcnow() - timedelta(days=30)
        query = query.filter(Expense.date >= date_limit)

    elif filter_type == "3months":
        date_limit = datetime.utcnow() - timedelta(days=90)
        query = query.filter(Expense.date >= date_limit)

    elif start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Expense.date.between(start, end))
        except:
            return jsonify({"msg": "Formato de data inválido (YYYY-MM-DD)"}), 400

    expenses = query.all()

    result = []
    for e in expenses:
        result.append({
            "id": e.id,
            "title": e.title,
            "amount": e.amount,
            "category": e.category,
            "date": e.date.strftime("%Y-%m-%d")
        })

    return jsonify(result), 200


@app.route('/expenses/<int:id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    expense = Expense.query.get(id)

    if not expense or expense.user_id != user_id:
        return jsonify({"msg": "Gasto não encontrado"}), 404

    expense.title = data.get('title', expense.title)
    expense.amount = data.get('amount', expense.amount)
    expense.category = data.get('category', expense.category)

    db.session.commit()

    return jsonify({"msg": "Gasto atualizado com sucesso"}), 200


@app.route('/expenses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()

    expense = Expense.query.get(id)

    if not expense or expense.user_id != user_id:
        return jsonify({"msg": "Gasto não encontrado"}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({"msg": "Gasto deletado com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)
