# MVP Pescaria — Backend

Projeto desenvolvido para o MVP da disciplina Desenvolvimento Full Stack Básico da PUC-Rio.

## Objetivo

Disponibilizar informações sobre espécies de peixes e permitir o registro de relatos de pescarias.

A aplicação permite consultar peixes, visualizar suas características, iscas recomendadas e dicas de pesca, além de cadastrar e consultar relatos associados a cada espécie.

## Tecnologias

- Python e Flask
- SQLite
- Swagger / OpenAPI
- Flask-CORS
- brModelo (modelagem conceitual e lógica, além de código de referência para o modelo físico)
- DB Browser for SQLite

## Modelagem do Banco de Dados

O banco possui duas tabelas: **Peixe** e **Pescaria**.

O relacionamento é de 1:N: um peixe pode estar associado a vários registros de pescarias, mas cada pescaria pertence a um único peixe.

A tabela `Pescaria` possui a chave estrangeira `id_peixe`, que referencia a chave primária da tabela `Peixe`.

- [Documentação da modelagem](docs/modelagem-banco.md)
- [Script SQLite](sql/schema.sql)

## Integridade Referencial

As conexões com o SQLite são centralizadas na função `conectar_banco()`, localizada no arquivo `app.py`.

Essa função é responsável por abrir a conexão com o banco, configurar o retorno dos registros utilizando `sqlite3.Row` e ativar a verificação das chaves estrangeiras por meio de `PRAGMA foreign_keys = ON`.

Essa configuração ajuda a impedir que relatos de pescarias sejam associados a peixes inexistentes.



## API REST

O backend disponibiliza cinco rotas:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/peixes` | Lista os peixes e permite buscar por nome |
| GET | `/peixes/<id_peixe>` | Consulta os detalhes de um peixe |
| GET | `/peixes/<id_peixe>/pescarias` | Lista os relatos associados a um peixe |
| POST | `/pescarias` | Cadastra um novo relato |
| DELETE | `/pescarias/<id_pescaria>` | Exclui um relato pelo ID |


## Integração com o Frontend

A API utiliza Flask-CORS para permitir requisições realizadas pelo frontend desenvolvido em HTML, CSS e JavaScript.

O frontend será mantido em um repositório separado e consumirá as rotas REST disponibilizadas pelo backend.

## Documentação e Testes

A documentação interativa da API está disponível pelo Swagger UI:

`http://127.0.0.1:5000/swagger`

Foram realizados testes das operações principais, incluindo:

- Consulta de peixes e seus detalhes, com retorno HTTP 200.
- Cadastro de relato de pescaria, com retorno HTTP 201.
- Consulta do relato cadastrado, com retorno HTTP 200.
- Exclusão de relato de teste, com retorno HTTP 200.
- Verificação da integridade referencial no SQLite, sem violações identificadas.
- Verificação da comunicação CORS, com retorno HTTP 200 e cabeçalho de permissão de origem.

## Execução Local

Com as dependências instaladas no ambiente virtual, execute o backend a partir de sua pasta:

`python app.py`

A API ficará disponível em:

`http://127.0.0.1:5000`

O servidor Flask está configurado para desenvolvimento local, não para utilização em produção.

## Observações

Este projeto possui finalidade acadêmica e prioriza uma implementação simples, organizada e funcional.

A exclusão de relatos não exige autenticação nesta versão do MVP. Essa é uma limitação conhecida da aplicação.