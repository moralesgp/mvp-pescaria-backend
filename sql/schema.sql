
CREATE TABLE Peixe (
    id_peixe INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_peixe VARCHAR(100) NOT NULL,
    tipo_agua VARCHAR(10) NOT NULL,
    regiao VARCHAR(150) NOT NULL,
    isca_natural VARCHAR(200),
    dicas TEXT NOT NULL,
    descricao TEXT,
    isca_artificial VARCHAR(200)
);


CREATE TABLE Pescaria (
    id_pescaria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_pescador VARCHAR(100) NOT NULL,
    isca_utilizada VARCHAR(150) NOT NULL,
    data DATE NOT NULL,
    local VARCHAR(150) NOT NULL,
    observacao TEXT,
    id_peixe INTEGER NOT NULL,
    FOREIGN KEY (id_peixe) REFERENCES Peixe(id_peixe)
);
