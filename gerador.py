import re
import jinja2
import numpy as np
from faker import Faker
from numbers import Number
from ranimegen.animegen import RandomAnime

date_regex = "^[0-9]{4}-[0-9]{2}-[0-9]{2}"
class Sql_table:
    attributes: dict
    table_name: str
    sql_data : str

    def __init__(self, attributes=None, table_name=None) -> None:
        self.attributes = attributes
        self.table_name = table_name    
        self.sql_data = str()

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

        for i in range(datasize):
            s = str()
            items = data_model.items()
            for _, value in items:
                element = value()
                # print(element)
                if (isinstance(element, Number)): s += f'{element}'
                elif (re.search(date_regex, str(element))): s += f"TO_DATE('{element}', 'YYYY-MM-DD')"
                else: s += f"'{element}'"

                if (i != len(items)-1): s += ', '
            
            sql_statement = template.render(tabela = table_name, campos = tuple(list(data_model.keys())), dados=s)
            self.sql_data += sql_statement
            if (verbose == True): print(sql_statement)
    
    # Gera um arquivo
    def generate_sql_file(self, filename):
        with open(filename, "r") as f:
            f.write(self.sql_data)
        

f = Faker('pt_BR')

sex = lambda: np.random.choice(['M', 'F'])
num = lambda: np.random.randint(1,1000)
tipo = lambda: np.random.choice(['Normal', 'Publicador'])
# Usuário

# ! modifique aqui os campos
user_table = {
    # 'email': f.email,
    'CPF': f.cpf,
    'nome_usuario': f.name,
    'sexo': sex,
    'd_nasc': f.date_of_birth,
    'end_cep': f.postcode,
    'end_num': num,
    'tipo': tipo
}

table_name = "Usuario"
populate = "INSERT INTO {{ tabela }}{{ campos }} VALUES ({{ dados }});\n"
template = jinja2.Template(populate)

sql_generator = Sql_table()
DATASIZE = 100

sql_generator.generate_data(
    DATASIZE,       # <- Insira aqui a quantidade de dados a serem gerados
    user_table,     # <- Insira aqui a tarefa dos usuários
    template,       # <- Insira aqui o template carregado do jinja
    table_name,     # <- Insira aqui o nome da tabela a ser gerada
    verbose=True    # <- Insira aqui se a execução da tabela terá o print
)

# Gerador 


# Obra
async def random_anime_name():
    gen = RandomAnime()
    myinfo = await gen.suggestanime()
    
    return myinfo['data'][0]['attributes']['slug']


obra_table = {
    "id_obra": np.random([1, int(1e10000)]),
    "nome_obra": random_anime_name,
    "autor": None,
    "nota": None,
    "desenhista": None,
    "diretor": None,
    "eh_anime": None,
    "eh_manga": None,
    "cpf": None,
}







