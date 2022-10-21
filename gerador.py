from datetime import datetime
import jinja2
import numpy as np
from numbers import Number
from faker import Faker

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

sex = lambda: np.random.choice([0, 1])

user_table = {
    'sexo': sex,
    'email': f.email,
    'nome': f.name,
    'd_nasc': f.date_of_birth,
    'CPF': f.cpf
}

Usuario = Sql_table(
    attributes=user_table,
    table_name='Usuario'
)

Usuario.generate_fields()

populate = "INSERT INTO {{ tabela }}{{ campos }} VALUES ({{ dados }});\n"
template = jinja2.Template(populate)

for i in range(20):
    s = str()
    items = Usuario.attributes.items()
    for i, (key, item) in enumerate(items):
        element = Usuario.attributes[key]()
        if (isinstance(element, Number)): s += f'{element}'
        else: s += f'"{element}"'

        if (i != len(items)-1): s += ', '
            
    print(template.render(tabela = Usuario.table_name, campos = Usuario.generate_fields(), dados=s))



