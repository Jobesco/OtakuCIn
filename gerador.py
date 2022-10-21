import jinja2
import numpy as np
from numbers import Number
from faker import Faker
import re

date_regex = "^[0-9]{4}-[0-9]{2}-[0-9]{2}"
class Sql_table:
    attributes: dict
    table_name: str

    def __init__(self, attributes, table_name) -> None:
        self.attributes = attributes
        self.table_name = table_name

    def generate_fields(self):
        s = '('
        keys = self.attributes.keys()
        for i, key in enumerate(keys):
            s += (key + (', ' if i != len(keys)-1 else ''))
        s += ')'
        return s

f = Faker('pt_BR')

sex = lambda: np.random.choice(['M', 'F'])
num = lambda: np.random.randint(1,1000)
tipo = lambda: np.random.choice(['Normal', 'Publicador'])

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

Usuario = Sql_table(
    attributes=user_table,
    table_name='Usuario' # ! modifique aqui o nome da tabela
)

DATASIZE = 100

Usuario.generate_fields()

populate = "INSERT INTO {{ tabela }}{{ campos }} VALUES ({{ dados }});\n"
template = jinja2.Template(populate)

for i in range(DATASIZE):
    s = str()
    items = Usuario.attributes.items()
    for i, (key, item) in enumerate(items):
        element = Usuario.attributes[key]()
        if (isinstance(element, Number)): s += f'{element}'
        elif (re.search(date_regex, str(element))): s += f"TO_DATE('{element}', 'YYYY-MM-DD')"
        else: s += f"'{element}'"

        if (i != len(items)-1): s += ', '
            
    print(template.render(tabela = Usuario.table_name, campos = Usuario.generate_fields(), dados=s))



