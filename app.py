
"""API REST do projeto Guia do Pescador."""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint




app = Flask(__name__)
# Permite que o frontend acesse a API.
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do Swagger UI
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Guia do Pescador"}
)

app.register_blueprint(
    swagger_blueprint,
    url_prefix=SWAGGER_URL
)


# Localiza o banco SQLite dentro do projeto.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "pescaria.db"


@app.get("/peixes")
def listar_peixes():
    """Lista os peixes e permite buscar pelo nome."""
    nome = request.args.get("nome", "").strip()

    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row

    try:
        sql = "SELECT * FROM Peixe"
        parametros = []

        if nome:
            sql += " WHERE nome_peixe LIKE ?"
            parametros.append(f"%{nome}%")

        sql += " ORDER BY nome_peixe"

        cursor = conexao.execute(sql, parametros)
        peixes = [dict(peixe) for peixe in cursor.fetchall()]

        return jsonify(peixes), 200

    finally:
        conexao.close()

@app.get("/peixes/<int:id_peixe>")
def detalhar_peixe(id_peixe):
    """Consulta os detalhes de um peixe pelo ID."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row

    try:
        sql = "SELECT * FROM Peixe WHERE id_peixe = ?"
        cursor = conexao.execute(sql, (id_peixe,))
        peixe = cursor.fetchone()

        if peixe is None:
            return jsonify({"erro": "Peixe não encontrado"}), 404

        return jsonify(dict(peixe)), 200

    finally:
        conexao.close()


@app.get("/peixes/<int:id_peixe>/pescarias")
def listar_pescarias(id_peixe):
    """Lista os relatos de pescaria de um peixe."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row

    try:
        sql = """
            SELECT *
            FROM Pescaria
            WHERE id_peixe = ?
            ORDER BY data DESC
        """
        cursor = conexao.execute(sql, (id_peixe,))
        pescarias = cursor.fetchall()

        return jsonify([dict(p) for p in pescarias]), 200

    finally:
        conexao.close()


@app.post("/pescarias")
def cadastrar_pescaria():
    """Cadastra um novo relato de pescaria."""
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "JSON inválido"}), 400

    obrigatorios = [
        "id_peixe",
        "nome_pescador",
        "isca_utilizada",
        "data",
        "local"
    ]

    for campo in obrigatorios:
        if dados.get(campo) is None or dados[campo] == "":
            return jsonify({
                "erro": f"Campo obrigatório: {campo}"
            }), 400

    conexao = sqlite3.connect(DB_PATH)

    try:
        cursor = conexao.execute(
            "SELECT id_peixe FROM Peixe WHERE id_peixe = ?",
            (dados["id_peixe"],)
        )

        if cursor.fetchone() is None:
            return jsonify({
                "erro": "Peixe não encontrado"
            }), 404

        sql = """
            INSERT INTO Pescaria (
                nome_pescador,
                isca_utilizada,
                data,
                local,
                observacao,
                id_peixe
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        valores = (
            dados["nome_pescador"],
            dados["isca_utilizada"],
            dados["data"],
            dados["local"],
            dados.get("observacao"),
            dados["id_peixe"]
        )

        cursor = conexao.execute(sql, valores)
        conexao.commit()

        return jsonify({
            "mensagem": "Pescaria cadastrada com sucesso",
            "id_pescaria": cursor.lastrowid
        }), 201

    finally:
        conexao.close()


@app.delete("/pescarias/<int:id_pescaria>")
def excluir_pescaria(id_pescaria):
    """Exclui um relato de pescaria pelo ID."""
    conexao = sqlite3.connect(DB_PATH)

    try:
        sql = "DELETE FROM Pescaria WHERE id_pescaria = ?"
        cursor = conexao.execute(sql, (id_pescaria,))

        if cursor.rowcount == 0:
            return jsonify({
                "erro": "Pescaria não encontrada"
            }), 404

        conexao.commit()

        return jsonify({
            "mensagem": "Pescaria excluída com sucesso"
        }), 200

    finally:
        conexao.close()


if __name__ == "__main__":
    app.run(debug=True)
