from models.InstituicaoEnsino import InstituicaoEnsino
import json 

def carregarInstituicao(CAMINHO_INSTITUICOES):
    with open(CAMINHO_INSTITUICOES, "r", encoding="utf-8") as f:
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