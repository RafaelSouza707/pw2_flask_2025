import sqlite3
from models.CarregarUsuarios import carregarUsuarios
from models.CarregarInstituicao import carregarInstituicao

DATABASE_NAME = "censoescolar.db"
CAMINHO_USUARIOS = "dados/dadosusuarios.json"
CAMINHO_INSTITUICOES = "dados/dadosinstituicoes.json"



def create_tables():
    print("Iniciando criação")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    with open('schema.sql') as f:
        print("Criando as tabelas")
        conn.executescript(f.read())
    

    instituicoes = carregarInstituicao(CAMINHO_INSTITUICOES)
    print("Inserindo instituições padrões")
    for i in instituicoes:
        cursor.execute(
            "INSERT INTO tb_instituicao(codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_esp) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (i.codigo, i.nome, i.co_uf, i.co_municipio, i.qt_mat_bas, i.qt_mat_prof, i.qt_mat_esp) 
        )
    conn.commit()

    users = carregarUsuarios(CAMINHO_USUARIOS)
    print("Inserindo usuários padrões")
    for u in users:
        cursor.execute(
            "INSERT INTO tb_usuario (nome, cpf, nascimento) VALUES (?, ?, ?)", 
            (u.nome, u.cpf, u.nascimento)
        )
    conn.commit()

    print("Fechar conexão")
    conn.close()


if __name__ == "__main__":
    create_tables()