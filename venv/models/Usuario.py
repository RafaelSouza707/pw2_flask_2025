class Usuario():
    
    def __init__(self, id, nome, cpf, nascimento):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
    
    def __repr__(self):
        return ''

    def to_json_user(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "nascimento": self.nascimento
        }
    