from flask import Flask, request, jsonify
from models.CarregarInstituicaoJson import carregarInstituicaoJson
from models.CarregarInstituicaoCsv import carregarInstituicaoCsv
from models.CarregarUsuarios import carregarUsuarios

from models.InstituicaoEnsinoJson import InstituicaoEnsinoJson
#from models.CarregarInstituicaoCsv import InstituicaoEnsinoCsv
from models.Usuario import Usuario

from models.SalvarObjeto import salvar_objeto
import sqlite3

app = Flask(__name__)

# Codigo, nome, codigo_uf, codigo_municipio, todos os qt_mat

# Carregar lista com usuarios
CAMINHO_USUARIOS = "dados/dadosusuarios.json"
usuarios = carregarUsuarios(CAMINHO_USUARIOS)

# Carregar lista com instituições do JSON.
CAMINHO_INSTITUICOES = "dados/dadosinstituicoes.json"
instituicoesEnsino = carregarInstituicaoJson(CAMINHO_INSTITUICOES)

#Carregar lista com instituições do CSV.
CAMINHO_INSTITUICOESSCV = "dados/microdados_ed_basica_2023.csv"
instituicoesEnsinoCsv = carregarInstituicaoCsv(CAMINHO_INSTITUICOESSCV)

# Rota inicial
@app.get("/")
def index():
    return '{"versao":"2.0.0"}', 200

# === Start Users ===
"""
@app.get("/usuarios")
def getUsuarios():
    lista_usuarios = [user.to_json_user() for user in usuarios]
    return lista_usuarios, 200
"""

@app.get("/usuarios")
def getUsuarios():
    conn = sqlite3.connect("censoescolar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf, nascimento FROM tb_usuario")
    usuarios = [
        {"id": l[0], "nome": l[1], "cpf": l[2], "nascimento": l[3]}
        for l in cursor.fetchall()
    ]
    conn.close()
    return jsonify(usuarios), 200

"""
@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    user = next((u for u in usuarios if u.id == id), None)
    if user is None:
        return jsonify({"erro": "Usuário não encontrado."}), 404
    listUsersById = usuarios[id].to_json_user()
    return jsonify(listUsersById), 200
"""

@app.get("/usuarios/<int:id>")
def getUsuariosById(id: int):
    conn = sqlite3.connect("censoescolar.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, cpf, nascimento FROM tb_usuario WHERE id = ?", (id,)
    )
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        return jsonify({"erro": "Usuário não encontrado."}), 404
    
    user = {"id": linha[0], "nome": linha[1], "cpf": linha[2], "nascimento": linha[3]}
    return jsonify(user), 200


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
    if "nascimento" in dados:
        user.nascimento = dados["nascimento"]

    salvar_objeto(CAMINHO_USUARIOS, [u.to_json_user() for u in usuarios])
    return jsonify(user.to_json_user()), 200


@app.post("/usuarios")
def postUsers():
    data = request.get_json()

    novoUser = Usuario(
        id=data.get('id'),
        nome=data.get('nome'),
        cpf=data.get('cpf'),
        nascimento=data.get('nascimento')
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
"""
@app.get("/instituicoesensino") 
def getInstituicoesEnsino():
    lista_serial = [inst.to_json() for inst in instituicoesEnsino]
    return lista_serial, 200
"""

@app.get("/instituicoesensino")
def getInstituicoesEnsinoJSOn():
    conn = sqlite3.connect("censoescolar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_esp FROM tb_instituicao")
    instituicoesEnsino = [
        {"id": i[0], "codigo": i[1], "nome": i[2], "co_uf": i[3], "co_municipio": i[4], "qt_mat_bas": i[5], "qt_mat_prof": i[6], "qt_mat_esp": i[7]}
        for i in cursor.fetchall()
    ]
    conn.close()
    return jsonify(instituicoesEnsino), 200



@app.get("/instituicoesensinocsv")
def getInstituicoesEnsinoCSV():
    conn = sqlite3.connect("censoescolar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp, qt_mat_fund, qt_mat_inf, qt_mat_med, qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb FROM tb_instituicao_csv")
    instituicoesEnsinocsv = [
        {"id": i[0], "": i[1], "nome": i[2], "co_uf": i[3], "co_municipio": i[4], "qt_mat_bas": i[5], "qt_mat_prof": i[6], "qt_mat_eja": i[7], "qt_mat_esp": i[8], "qt_mat_fund": i[9], "qt_mat_inf": i[10], "qt_mat_med": i[11], "qt_mat_zr_na": i[12], "qt_mat_zr_rur": i[13], "qt_mat_zr_urb": i[14]}
        for i in cursor.fetchall()
    ]
    conn.close()
    return jsonify(instituicoesEnsinocsv), 200


"""
@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    inst = next((i for i in instituicoesEnsino if i.codigo == id), None)
    if inst is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    ieDict = inst.to_json()
    return jsonify(ieDict), 200
"""


@app.get("/instituicoesensino/<int:id>")
def getInstituicoesEnsinoById(id: int):
    conn = sqlite3.connect("censoescolar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_esp FROM tb_instituicao WHERE codigo = ?", (id,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    
    instituicao = {"id": linha[0], "codigo": linha[1], "nome": linha[2], "co_uf": linha[3], "co_municipio": linha[4], "qt_mat_bas": linha[5], "qt_mat_prof": linha[6], "qt_mat_esp": linha[7]}
    return jsonify(instituicao), 200


@app.get("/instituicoesensinocsv/<codigo>")
def getInstituicaoByCodigo(codigo: str):
    conn = sqlite3.connect("censoescolar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp, qt_mat_fund, qt_mat_inf, qt_mat_med, qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb FROM tb_instituicao_csv WHERE codigo = ?", (codigo,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        return jsonify({"erro": "Instituição não encontrada"}), 404
    
    instituicoes = { "id": linha[0], "codigo": linha[1], "nome": linha[2], "co_uf": linha[3], "co_municipio": linha[4], "qt_mat_bas": linha[5], "qt_mat_prof": linha[6], "qt_mat_eja": linha[7], "qt_mat_esp": linha[8], "qt_mat_fund": linha[9], "qt_mat_inf": linha[10], "qt_mat_med": linha[11], "qt_mat_zr_na": linha[12], "qt_mat_zr_rur": linha[13], "qt_mat_zr_urb": linha[14]}
    return jsonify(instituicoes), 200


@app.post("/instituicoesensino")
def postInstituicoes():
    dados = request.get_json()
    nova = InstituicaoEnsinoJson(
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
