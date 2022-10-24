import re
import jinja2
import numpy as np
import pandas as pd
from faker import Faker
from numbers import Number
from collections import defaultdict
from ranimegen.animegen import RandomAnime

date_regex = "^[0-9]{4}-[0-9]{2}-[0-9]{2}"
class Sql_table:
    attributes: dict
    table_name: str
    sql_data : str
    tabelas: dict

    def __init__(self, attributes=None, table_name=None) -> None:
        self.attributes = attributes
        self.table_name = table_name    
        self.sql_data = str()
        self.tabelas = dict()

    # Gera um campo
    def generate_fields(self):
        s = '('
        keys = self.attributes.keys()
        for i, key in enumerate(keys):
            s += (key + (', ' if i != len(keys)-1 else ''))
        s += ')'
        return s

    # Gera uma lista de campos
    def generate_data(self, datasize, data_model, template, table_name, verbose=False):
        if table_name == None: table_name = self.table_name

        df_dict = defaultdict(list)
        for _ in range(datasize):
            s = str()
            items = data_model.items()
            for k, (key, value) in enumerate(items):
                element = value()
                # print(element)
                if (isinstance(element, Number)): s += f'{element}'
                elif (re.search(date_regex, str(element))): s += f"TO_DATE('{element}', 'YYYY-MM-DD')"
                else: s += f"'{element}'"

                df_dict[key].append(element)

                s += (',' if (k < len(items)-1) else '')
            
            def generate_fields(termos):
                st = '('
                for i, campo in enumerate(termos):
                    st += campo
                    st += "," if i < len(termos)-1 else ""
                st += ')'
                return st
                
            sql_statement = template.render(tabela = table_name, campos = generate_fields(data_model.keys()), dados=s) + '\n'
            self.sql_data += sql_statement
            if (verbose == True): print(sql_statement)

        if verbose == True: print(pd.DataFrame(df_dict))
        self.tabelas[table_name] = pd.DataFrame(df_dict)
        return self.sql_data
    
    # Gera um arquivo
    def generate_sql_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.sql_data)
        
    def generate_from_dataframe(self, df):
        
        pass

f = Faker('pt_BR')
populate = "INSERT INTO {{ tabela }}{{ campos }} VALUES ({{ dados }});\n"
template = jinja2.Template(populate)
DATASIZE = 10
sql_generator = Sql_table()

animesrjal = 'Naruto OnePiece DBZ Bleach DeathNote AttackOnTitan BokuNoHeroAcademia BokuNoPico KaguyaSama HunterxHunter Pokemon Gintama MobPsycho100 SpyXFamily ToLoveRu ChainsawMan Megalobox InazumaEleven AssassinationClassroom'.split()
animesjm = 'Naruto OnePiece DBZ Bleach DeathNote AttackOnTitan BokuNoHeroAcademia BokuNoPico CavaleirosDoZodiaco SamuraiX'.split()
todos_animes = list(set(animesjm + animesrjal))

sex = lambda: np.random.choice(['M', 'F'])
num = lambda: np.random.randint(1,1000)
tipo = lambda: np.random.choice(['Normal', 'Publicador'])

# Selo
from random import choice, randint

generator = RandomAnime()
all_genre = generator.genres

# Precisa tiar as repetições na mão!
gera_selo = lambda: "MELHOR ANIME/MANGA - " + choice(all_genre)

selo_table = {
    "nome_selo": gera_selo
}

sql_generator.generate_data(
    3,
    selo_table,
    template,
    "Selo",
    verbose=True
)

# Categoria
num_cat = lambda: randint(100, 1000)
nome_cat = lambda: choice(all_genre)

cat_table = {
    "id_categoria": num_cat,
    "nome_categoria": nome_cat
}

sql_generator.generate_data(
    DATASIZE,
    cat_table,
    template,
    "Categoria",
    verbose=True
)

# Personagem
personagem_table = {
    "id_personagem": num_cat,
    "nome_personagem": lambda: f.name().split()[0] + " " + f.name().split()[1]
}

sql_generator.generate_data(
    DATASIZE,
    personagem_table,
    template,
    "Personagem",
    verbose=True
)

# Dublador

dublador_table = {
    "id_dublador": num_cat,
    "nome_dublador": lambda: f.name().split()[0] + " " + f.name().split()[1]
}

sql_generator.generate_data(
    DATASIZE,
    dublador_table,
    template,
    "Dublador",
    verbose=True
)

# Usuário
user_table = {
    'cpf': f.cpf,
    'nome_usuario': f.name,
    'sexo': sex,
    'd_nasc': f.date_of_birth,
    'end_cep': f.postcode,
    'end_num': num,
    'tipo': tipo
}

sql_generator.generate_data(
    DATASIZE * 20,       # <- Insira aqui a quantidade de dados a serem gerados
    user_table,     # <- Insira aqui a tarefa dos usuários
    template,       # <- Insira aqui o template carregado do jinja
    "Usuario",     # <- Insira aqui o nome da tabela a ser gerada
    verbose=True    # <- Insira aqui se a execução da tabela terá o print
)

df = sql_generator.tabelas['Usuario']
# Obra
obra_table = {
    "id_obra": num_cat,
    "nome_obra": lambda: choice(todos_animes),
    "autor": f.name,
    "nota": lambda: randint(0, 10),
    "desenhista": f.name,
    "diretor":  f.name,
    "eh_anime": lambda: randint(0, 1),
    "eh_manga": lambda: randint(0, 1),
    "cpf": lambda: df[df['tipo'] == 'Publicador']['cpf'].sample().values[0]
}

sql_generator.generate_data(
    DATASIZE,
    obra_table,
    template,
    "Obra",
    verbose=True
)

# Episódio
episodio_table = {
    "titulo": lambda: f.sentence(nb_words=5, variable_nb_words=True),
    "id_obra": lambda: choice(sql_generator.tabelas['Obra']['id_obra']),
    "numero": lambda: randint(1, 100) 
}

sql_generator.generate_data(
    DATASIZE * 2,
    episodio_table,
    template,
    "Episodio",
    verbose=True
)

# Emails
# lambda: choice(sql_generator.tabelas['Usuario']['cpf']) = choice(sql_generator.tabelas['Usuario']['cpf'])

emails_table = {
    "cpf": lambda: choice(sql_generator.tabelas['Usuario']['cpf']),
    "email": lambda: f.email()
}

sql_generator.generate_data(
    DATASIZE * 3,
    emails_table,
    template,
    "Emails",
    verbose=True
)

# Tem
# lambda: choice(sql_generator.tabelas['Personagem']['id_personagem']) = choice(sql_generator.tabelas['Personagem']['id_personagem'])
# lambda: choice(sql_generator.tabelas['Dublador']['id_dublador']) = choice(sql_generator.tabelas['Dublador']['id_dublador'])
# lambda: choice(sql_generator.tabelas['Episodio']['numero']) = choice(sql_generator.tabelas['Episodio']['numero'])

tem_table = {
    "id_obra": lambda: choice(sql_generator.tabelas['Obra']['id_obra']),
    "numero": lambda: choice(sql_generator.tabelas['Episodio']['numero']),
    "id_personagem": lambda: choice(sql_generator.tabelas['Personagem']['id_personagem']),
    "id_dublador": lambda: choice(sql_generator.tabelas['Dublador']['id_dublador'])
}

sql_generator.generate_data(
    DATASIZE,
    tem_table,
    template,
    "Tem",
    verbose=True
)


# Amizade
amizade_table = {
    "cpf_convidado": lambda: choice(sql_generator.tabelas['Usuario']['cpf']),
    "cpf_convidador": lambda: choice(sql_generator.tabelas['Usuario']['cpf'])
}

sql_generator.generate_data(
    DATASIZE,
    amizade_table,
    template,
    "Amizade",
    verbose=True
)

# Assiste

assiste_table = {
    "cpf": lambda: choice(sql_generator.tabelas['Usuario']['cpf']),
    "id_obra": lambda: choice(sql_generator.tabelas['Obra']['id_obra']),
    "data_visto": f.date
}

sql_generator.generate_data(
    DATASIZE,
    assiste_table,
    template,
    "Assiste",
    verbose=True
)

ganhou_table = {
    "id_obra": lambda: choice(sql_generator.tabelas['Obra']['id_obra']),
    "id_categoria": lambda: choice(sql_generator.tabelas['Categoria']['id_categoria']),
    "nome_selo": lambda: choice(sql_generator.tabelas['Selo']['nome_selo'])
}

sql_generator.generate_data(
    DATASIZE,
    ganhou_table,
    template,
    "Ganhou",
    verbose=True
)

sql_generator.generate_sql_file("insercoes.sql")



