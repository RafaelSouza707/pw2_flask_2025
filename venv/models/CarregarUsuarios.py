from models.Usuario import Usuario
import json 


def carregarUsuarios(CAMINHO_USUARIOS):
    with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    usuarios = []

    for item in dados:
        usuarios.append(
            Usuario(
                id=item.get("id"),
                nome=item.get("nome"),
                cpf=item.get("cpf"),
                data_nascimento=item.get("data_nascimento")
            )
        )
    return usuarios
