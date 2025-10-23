from flask import Flask, request, jsonify
from models.InstituicaoEnsino import InstituicaoEnsino
from models.CarregarInstituicao import carregarInstituicao
from models.CarregarUsuarios import carregarUsuarios 
from models.Usuario import Usuario
from models.SalvarObjeto import salvar_objeto

app = Flask(__name__)

# Carregar lista com usuarios
CAMINHO_USUARIOS = "dados/dadosusuarios.json"
usuarios = carregarUsuarios(CAMINHO_USUARIOS)

# Carregar lista com instituições.
CAMINHO_INSTITUICOES = "dados/dadosinstituicoes.json"
instituicoesEnsino = carregarInstituicao(CAMINHO_INSTITUICOES)

# Rota inicial
@app.get("/")
def index():
    return '{"versao":"2.0.0"}', 200


# === Start Users ===
@app.get("/usuarios")
def getUsuarios():
    lista_usuarios = [user.to_json_user() for user in usuarios]
    return lista_usuarios, 200


@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    user = next((u for u in usuarios if u.id == id), None)
    if user is None:
        return jsonify({"erro": "Usuário não encontrado."}), 404
    listUsersById = usuarios[id].to_json_user()
    return jsonify(listUsersById), 200


@app.put("/usuarios/<int:id>")
def putUsersById(id: int):
    user = next((u for u in usuarios if u.id == id), None)
    if user is None:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    dados = request.get_json()
    
    if "id" in dados:
        user.id = dados["id"]
    if "nome" in dados:
        user.nome = dados["nome"]
    if "cpf" in dados:
        user.cpf = dados["cpf"]
    if "data_nascimento" in dados:
        user.data_nascimento = dados["data_nascimento"]

    salvar_objeto(CAMINHO_USUARIOS, [u.to_json_user() for u in usuarios])
    return jsonify(user.to_json_user()), 200


@app.post("/usuarios")
def postUsers():
    data = request.get_json()

    novoUser = Usuario(
        id=data.get('id'),
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        data_nascimento=data.get('data_nascimento')
    )
    usuarios.append(novoUser)
    salvar_objeto(CAMINHO_USUARIOS, [u.to_json_user() for u in usuarios])
    
    return jsonify(novoUser.to_json_user()), 200


@app.delete("/usuarios/<int:id>")
def deleteUsers(id: int):
    if id < 0 or id >= len(usuarios):
        return jsonify({"erro": "Usuário não encontrado"}), 404
    deletado = usuarios.pop(id)
    salvar_objeto(CAMINHO_USUARIOS, [user.to_json_user() for user in usuarios])
    return jsonify({"mensagem": "Usuário removido", "usuario": deletado.to_json_user()}), 200

# === End Users ===

# Start Instituições
@app.get("/instituicoesensino") 
def getInstituicoesEnsino():
    lista_serial = [inst.to_json() for inst in instituicoesEnsino]
    return lista_serial, 200


@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    inst = next((i for i in instituicoesEnsino if i.codigo == id), None)
    if inst is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    ieDict = inst.to_json()
    return jsonify(ieDict), 200


@app.post("/instituicoesensino")
def postInstituicoes():
    dados = request.get_json()
    nova = InstituicaoEnsino(
        codigo=dados.get("codigo"),
        nome=dados.get("nome"),
        co_uf=dados.get("co_uf"),
        co_municipio=dados.get("co_municipio"),
        qt_mat_bas=dados.get("qt_mat_bas"),
        qt_mat_prof=dados.get("qt_mat_prof"),
        qt_mat_eja=dados.get("qt_mat_eja"),
        qt_mat_esp=dados.get("qt_mat_esp")
    )
    instituicoesEnsino.append(nova)
    salvar_objeto(CAMINHO_INSTITUICOES, [i.to_json() for i in instituicoesEnsino])
    return jsonify(nova.to_json()), 201


@app.put("/instituicoesensino/<int:id>")
def putInstituicoesensino(id: int):
    id_inst = next((i for i in instituicoesEnsino if i.codigo == id), None)
    if id_inst is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    dados = request.get_json()
    inst = instituicoesEnsino[id]
    inst.codigo = dados.get("codigo", inst.codigo)
    inst.nome = dados.get("nome", inst.nome)
    inst.co_uf = dados.get("co_uf", inst.co_uf)
    inst.co_municipio = dados.get("co_municipio", inst.co_municipio)
    inst.qt_mat_bas = dados.get("qt_mat_bas", inst.qt_mat_bas)
    inst.qt_mat_prof = dados.get("qt_mat_prof", inst.qt_mat_prof)
    inst.qt_mat_eja = dados.get("qt_mat_eja", inst.qt_mat_eja)
    inst.qt_mat_esp = dados.get("qt_mat_esp", inst.qt_mat_esp)
    salvar_objeto(CAMINHO_INSTITUICOES, [i.to_json() for i in instituicoesEnsino])
    return jsonify(inst.to_json()), 200


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id: int):
    inst = next((i for i in instituicoesEnsino if i.codigo == id), None)
    if inst is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    deletada = instituicoesEnsino.pop(id)
    salvar_objeto(CAMINHO_INSTITUICOES, [i.to_json() for i in instituicoesEnsino])
    return jsonify({"mensagem": "Instituição removida", "instituicao": deletada.to_json()}), 200

# === End Instituições ===


if __name__ == '__main__':
    
    app.run(debug=True)
