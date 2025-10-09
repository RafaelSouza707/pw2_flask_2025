from flask import Flask, request, jsonify
from models.InstituicaoEnsino import InstituicaoEnsino
from models.Usuario import Usuario
import json 

app = Flask(__name__)

user0 = Usuario(000, "Rafael", "11122233344400", "18/07/2001")
user1 = Usuario(111, "Moura", "555666777888800", "10/07/2001")
user2 = Usuario(222,"Souza", "00011100011100", "22/07/2001")

listUsers = [user0, user1, user2]

ie = InstituicaoEnsino(
    "25000012", "EMEF JOAO ALVES",
    25, 
    "2501005", 
    779, 
    0, 
    104, 
    43
    )

instituicoesEnsino = [ie]

caminhoInstituicoes = "dados/dadosinstituicoes.json"

def carregarInstituicao(caminhoInstituicoes):
    with open(caminhoInstituicoes, "r", encoding="utf-8") as f:
        dados = json.load(f)

    instituicoes = []
    for item in dados:
        instituicoes.append(
            InstituicaoEnsino(
                codigo=item.get("codigo"),
                nome=item.get("nome"),
                co_uf=item.get("co_uf"),
                co_municipio=item.get("co_municipio"),
                qt_mat_bas=item.get("qt_mat_bas"),
                qt_mat_prof=item.get("qt_mat_prof"),
                qt_mat_eja=item.get("qt_mat_eja"),
                qt_mat_esp=item.get("qt_mat_esp")
            )
        )
    return instituicoes


@app.get("/")
def index():
    return '{"versao":"2.0.0"}', 200


@app.get("/usuarios")
def getUsuarios():
    lista_usuarios = [user.to_json_user() for user in listUsers]
    return lista_usuarios, 200


@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    listUsersById = listUsers[id].to_json_user()
    return jsonify(listUsersById), 200


@app.put("/usuarios/<int:id>")
def putUsersById(id: int):
    dados = request.get_json()

    user = listUsers[id]
    
    if "id" in dados:
        user.id = dados["id"]
    if "nome" in dados:
        user.nome = dados["nome"]
    if "cpf" in dados:
        user.cpf = dados["cpf"]
    if "data_nascimento" in dados:
        user.data_nascimento = dados["data_nascimento"]

    return jsonify(user.to_json_user()), 200


@app.post("/usuarios")
def setUsuarios():
    data = request.get_json()

    usuario = Usuario(
        id=data.get('id'),
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        data_nascimento=data.get('data_nascimento')
    )

    listUsers.append(usuario)

    lista_usuarios = [user.to_json_user() for user in listUsers]
    
    return lista_usuarios, 200
    


@app.get("/instituicoesensino") 
def getInstituicoesEnsino():
    lista_serial = [inst.to_json() for inst in instituicoesEnsino]
    return lista_serial, 200


@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    ieDict = instituicoesEnsino[id].to_json()
    return jsonify(ieDict), 200


if __name__ == '__main__':
    ieCarregadas = carregarInstituicao(caminhoInstituicoes)
    instituicoesEnsino.extend(ieCarregadas)
    
    app.run(debug=True)
