import sqlite3
from models.CarregarUsuarios import carregarUsuarios
from models.CarregarInstituicaoJson import carregarInstituicaoJson
from models.CarregarInstituicaoCsv import carregarInstituicaoCsv

DATABASE_NAME = "censoescolar.db"
CAMINHO_USUARIOS = "dados/dadosusuarios.json"
CAMINHO_INSTITUICOESJSON = "dados/dadosinstituicoes.json"
CAMINHO_INSTITUICOESCSV = "dados/microdados_ed_basica_2023.csv"


def create_tables():
    print("Iniciando criação do banco de dados...")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Cria as tabelas a partir do schema.sql
    with open('schema.sql', encoding="utf-8") as f:
        print("Criando as tabelas...")
        conn.executescript(f.read())

    instituicoesJson = carregarInstituicaoJson(CAMINHO_INSTITUICOESJSON)
    print("Inserindo instituições do JSON...")
    for i in instituicoesJson:
        cursor.execute("""
            INSERT INTO tb_instituicao (
                codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_esp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (i.codigo, i.nome, i.co_uf, i.co_municipio, i.qt_mat_bas, i.qt_mat_prof, i.qt_mat_esp))
    conn.commit()

    instituicoesCsv = carregarInstituicaoCsv(CAMINHO_INSTITUICOESCSV)
    print("Inserindo instituições do CSV...")
    for i in instituicoesCsv:
        cursor.execute("""
            INSERT INTO tb_instituicao_csv (
                codigo, nome, co_uf, co_municipio,
                qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp,
                qt_mat_fund, qt_mat_inf, qt_mat_med,
                qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            i.codigo, i.nome, i.co_uf, i.co_municipio,
            i.qt_mat_bas, i.qt_mat_prof, i.qt_mat_eja, i.qt_mat_esp,
            i.qt_mat_fund, i.qt_mat_inf, i.qt_mat_med,
            i.qt_mat_zr_na, i.qt_mat_zr_rur, i.qt_mat_zr_urb
        ))
    conn.commit()

    # === INSERIR USUÁRIOS ===
    users = carregarUsuarios(CAMINHO_USUARIOS)
    print("Inserindo usuários padrões...")
    for u in users:
        cursor.execute(
            "INSERT INTO tb_usuario (nome, cpf, nascimento) VALUES (?, ?, ?)",
            (u.nome, u.cpf, u.nascimento)
        )
    conn.commit()

    print("Fechando conexão...")
    conn.close()


if __name__ == "__main__":
    create_tables()
