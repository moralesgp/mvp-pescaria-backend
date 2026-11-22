
"""API REST do projeto Guia do Pescador."""

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
