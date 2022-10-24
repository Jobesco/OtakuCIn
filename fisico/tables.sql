-- ENTIDADES REGULARES
CREATE TABLE Selo(
  nome_selo VARCHAR(50),
  CONSTRAINT pk_selo PRIMARY KEY (nome_selo)
);

CREATE TABLE Categoria(
  id_categoria NUMBER,
  nome_categoria VARCHAR(15),
  CONSTRAINT pk_categoria PRIMARY KEY (id_categoria)
);

CREATE TABLE Personagem(
  id_personagem NUMBER,
  nome_personagem VARCHAR(20),
  CONSTRAINT pk_personagem PRIMARY KEY (id_personagem)
);

CREATE TABLE Dublador(
  id_dublador NUMBER,
  nome_dublador VARCHAR(20),
  CONSTRAINT pk_dublador PRIMARY KEY (id_dublador)
);

CREATE TABLE Usuario(
  cpf VARCHAR(50),
  nome_usuario VARCHAR(50),
  sexo VARCHAR(1),
  CONSTRAINT check_sex CHECK (sexo = 'M' OR sexo = 'F'),
  d_nasc DATE,
  end_cep VARCHAR(50),
  end_num NUMBER,
  tipo VARCHAR(10),
  CONSTRAINT check_tipo CHECK (tipo = 'Normal' OR tipo = 'Publicador'),
  CONSTRAINT pk_usuario PRIMARY KEY (cpf)
);

CREATE TABLE Obra(
  id_obra NUMBER,
  nome_obra VARCHAR(50),
  autor VARCHAR(50),
  nota NUMBER,
  cpf VARCHAR(50) NOT NULL,
  desenhista VARCHAR(50),
  diretor VARCHAR(50),
  eh_anime NUMBER,
  CONSTRAINT check_eh_anime CHECK (eh_anime = 0 OR eh_anime = 1),
  eh_manga NUMBER,
  CONSTRAINT check_eh_manga CHECK (eh_manga = 0 OR eh_manga = 1),
  CONSTRAINT pk_obra PRIMARY KEY (id_obra),
  CONSTRAINT fk_usuario FOREIGN KEY (cpf) REFERENCES Usuario (cpf)
);

-- ENTIDADE FRACA
CREATE TABLE Episodio(
  titulo VARCHAR(50),
  id_obra NUMBER,
  numero NUMBER,
  CONSTRAINT pk_episodio PRIMARY KEY (id_obra, numero),
  CONSTRAINT fk_obra FOREIGN KEY (id_obra) REFERENCES Obra (id_obra)
);

CREATE TABLE Emails(
  cpf VARCHAR(50),
  email VARCHAR(50),
  CONSTRAINT pk_emails PRIMARY KEY (cpf, email),
  CONSTRAINT fk_emails FOREIGN KEY (cpf) REFERENCES Usuario (cpf)
);

-- ENTIDADE ASSOCIATIVA
CREATE TABLE Tem(
  id_obra NUMBER,
  numero NUMBER,
  id_personagem NUMBER,
  id_dublador NUMBER,
  CONSTRAINT pk_tem PRIMARY KEY (id_obra, numero, id_personagem),
  CONSTRAINT fk_obra_numero_tem FOREIGN KEY (id_obra, numero) REFERENCES Episodio (id_obra, numero),
  CONSTRAINT fk_personagem_tem FOREIGN KEY (id_personagem) REFERENCES Personagem (id_personagem),
  CONSTRAINT fk_dublador_tem FOREIGN KEY (id_dublador) REFERENCES Dublador (id_dublador)
);

-- Relações
CREATE TABLE Amizade(
  cpf_convidado VARCHAR(50) REQUIRED NOT NULL,
  cpf_convidador VARCHAR(50) REQUIRED NOT NULL,
  CONSTRAINT pk_amizade PRIMARY KEY (cpf_convidado, cpf_convidador),
  CONSTRAINT fk_convidado FOREIGN KEY (cpf_convidado) REFERENCES Usuario (cpf),
  CONSTRAINT fk_convidador FOREIGN KEY (cpf_convidador) REFERENCES Usuario (cpf)
);

CREATE TABLE Assiste(
 cpf VARCHAR(50),
 id_obra NUMBER,
 data_visto DATE,
 CONSTRAINT pk_assiste PRIMARY KEY (cpf, id_obra),
 CONSTRAINT fk_usuario_assiste FOREIGN KEY (cpf) REFERENCES Usuario (cpf),
 CONSTRAINT fk_obra_assiste FOREIGN KEY (id_obra) REFERENCES Obra (id_obra) 
);

CREATE TABLE Ganhou(
 id_obra NUMBER,
 id_categoria NUMBER,
 nome_selo VARCHAR(50),
 CONSTRAINT pk_ganhou PRIMARY KEY (id_obra,id_categoria, nome_selo),
 CONSTRAINT fk_obra_ganhou FOREIGN KEY (id_obra) REFERENCES Obra (id_obra),
 CONSTRAINT fk_categoria_ganhou FOREIGN KEY (id_categoria) REFERENCES Categoria (id_categoria),
 CONSTRAINT fk_nome_ganhou FOREIGN KEY (nome_selo) REFERENCES Selo (nome_selo)
);