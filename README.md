
# MVP Pescaria — Backend

Projeto desenvolvido para o MVP da disciplina
Desenvolvimento Full Stack Básico da PUC-Rio.

## Objetivo

Disponibilizar informações sobre espécies de peixes
e permitir o registro de relatos de pescarias.

## Tecnologias

- Python e Flask
- SQLite
- Swagger / OpenAPI
- brModelo (projeto Conceitual e Lógico mais código ref p/ modelo físico)

## Modelagem do Banco de Dados

O banco possui duas tabelas: Peixe e Pescaria.

O relacionamento é de 1:N:
um peixe pode estar associado a vários registros de pescarias,
mas cada pescaria pertence a um único peixe.

[Documentação da modelagem](docs/modelagem-banco.md)

[Script SQLite](sql/schema.sql)
