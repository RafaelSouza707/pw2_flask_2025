class Usuario():
    
    def __init__(self, id, nome, cpf, data_nascimento):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
    
    def __repr__(self):
        return ''

    def to_json_user(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento
        }
    