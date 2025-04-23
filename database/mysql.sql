

-- Criação da tabela 'admin'
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    ong TEXT NOT NULL
);

-- Criação da tabela 'doadores'
CREATE TABLE IF NOT EXISTS doadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    senha TEXT NOT NULL
);

-- Criação da tabela 'campanhas'
CREATE TABLE IF NOT EXISTS campanhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    titulo TEXT NOT NULL, 
    descricao TEXT NOT NULL, 
    meta_financeira TEXT NOT NULL, 
    meta_itens TEXT NOT NULL, 
    data_inicio DATE,
    status TEXT NOT NULL,
    data_fim DATE
);

-- Criação da tabela 'categorias'
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL
);

-- Criação da tabela 'doacoes'
CREATE TABLE IF NOT EXISTS doacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id_doador INTEGER NOT NULL,
    id_campanha INTEGER NOT NULL,
    tipo_doacao TEXT NOT NULL,
    tipo_item TEXT,  
    quantidade INTEGER,  
    valor REAL, 
    data_doacao DATE NOT NULL,
    FOREIGN KEY (id_doador) REFERENCES doadores(id),
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
);

-- Criação da tabela 'relatorios'
CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id_campanha INTEGER,
    data_referencia DATE,
    total REAL,
    total_itens_doados INTEGER NOT NULL,
    meta_comparativo TEXT NOT NULL,
    FOREIGN KEY (id_campanha) REFERENCES campanhas(id)
);