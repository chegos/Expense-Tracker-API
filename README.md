# 💰 Expense Tracker API

API RESTful desenvolvida em Python com Flask para gerenciamento de despesas pessoais, com autenticação segura via JWT.

---

## 🚀 Sobre o Projeto

O **Expense Tracker API** permite que usuários se cadastrem, façam login e gerenciem suas despesas de forma segura e organizada.

Cada usuário possui seus próprios dados, garantindo isolamento e segurança das informações.

---

## ⚙️ Tecnologias Utilizadas

* Python 3
* Flask
* Flask SQLAlchemy
* Flask JWT Extended
* SQLite

---

## 🔐 Funcionalidades

* Cadastro de usuário (Sign Up)
* Login com autenticação JWT
* Criação de despesas
* Listagem de despesas
* Atualização de despesas
* Exclusão de despesas
* Filtros por período:

  * Última semana
  * Último mês
  * Últimos 3 meses
  * Intervalo personalizado

---

## 📁 Estrutura do Projeto

```
expense-api/
│
├── app.py
├── database.db
└── README.md
```

---

## 🛠️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/chegos/expense-api.git
cd expense-api
```

---

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

---

### 3. Ative o ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 4. Instale as dependências

```bash
pip install flask flask_sqlalchemy flask_jwt_extended
```

---

### 5. Execute a aplicação

```bash
python app.py
```

---

### 6. Acesse a API

```
http://127.0.0.1:5000
```

---

## 🧪 Testando a API (Postman)

### 🔹 Criar usuário

**POST** `/signup`

```json
{
  "username": "luis",
  "password": "123"
}
```

---

### 🔹 Login

**POST** `/login`

```json
{
  "username": "luis",
  "password": "123"
}
```

📌 Retorna:

```
access_token
```

---

### 🔹 Criar despesa

**POST** `/expenses`

Header:

```
Authorization: Bearer SEU_TOKEN
```

Body:

```json
{
  "title": "Mercado",
  "amount": 150,
  "category": "Groceries"
}
```

---

### 🔹 Listar despesas

**GET** `/expenses`

---

### 🔹 Atualizar despesa

**PUT** `/expenses/{id}`

---

### 🔹 Deletar despesa

**DELETE** `/expenses/{id}`

---

## 🔎 Filtros disponíveis

| Filtro          | Endpoint                                              |
| --------------- | ----------------------------------------------------- |
| Última semana   | `/expenses?filter=week`                               |
| Último mês      | `/expenses?filter=month`                              |
| Últimos 3 meses | `/expenses?filter=3months`                            |
| Personalizado   | `/expenses?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` |

---

## 🔒 Autenticação

A API utiliza JWT (JSON Web Token).

Após o login, inclua o token em todas as requisições protegidas:

```
Authorization: Bearer SEU_TOKEN
```

---

## 📌 Categorias disponíveis

* Groceries
* Leisure
* Electronics
* Utilities
* Clothing
* Health
* Others

---

## 📈 Melhorias futuras

* Criptografia de senha (bcrypt)
* Paginação de resultados
* Deploy em cloud (Render / Railway)
* Documentação com Swagger
* Uso de migrations (Flask-Migrate)

---

## 👨‍💻 Autor

Luis Rodrigues
📍 São José dos Campos - SP
🔗 GitHub: https://github.com/chegos


---

## ⭐ Contribuição

Sinta-se à vontade para contribuir com melhorias!

---

## 📄 Licença

Este projeto está sob a licença MIT.
