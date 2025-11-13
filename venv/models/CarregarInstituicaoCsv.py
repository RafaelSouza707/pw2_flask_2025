import csv
from models.InstituicaoEnsinoCsv import InstituicaoEnsinoCsv

def _safe_int(value):
    """Converte valores numéricos do CSV em int, mesmo se vierem vazios ou com espaços."""
    try:
        return int(str(value).strip() or 0)
    except (ValueError, TypeError):
        return 0

def carregarInstituicaoCsv(CAMINHO_INSTITUICOES):
    instituicoes = []
    with open(CAMINHO_INSTITUICOES, "r", encoding="latin1") as f:
        leitor = csv.DictReader(f, delimiter=';')

        for linha in leitor:
            codigo = linha.get("CO_ENTIDADE")
            nome = linha.get("NO_ENTIDADE")

            # ignora linhas inválidas (sem código ou nome)
            if not codigo or not nome:
                continue

            instituicoes.append(
                InstituicaoEnsinoCsv(
                    codigo=codigo,
                    nome=nome,
                    co_uf=_safe_int(linha.get("CO_UF")),
                    co_municipio=_safe_int(linha.get("CO_MUNICIPIO")),
                    qt_mat_bas=_safe_int(linha.get("QT_MAT_BAS")),
                    qt_mat_prof=_safe_int(linha.get("QT_MAT_PROF")),
                    qt_mat_eja=_safe_int(linha.get("QT_MAT_EJA")),
                    qt_mat_esp=_safe_int(linha.get("QT_MAT_ESP")),
                    qt_mat_fund=_safe_int(linha.get("QT_MAT_FUND")),
                    qt_mat_inf=_safe_int(linha.get("QT_MAT_INF")),
                    qt_mat_med=_safe_int(linha.get("QT_MAT_MED")),
                    qt_mat_zr_na=_safe_int(linha.get("QT_MAT_ZR_NA")),
                    qt_mat_zr_rur=_safe_int(linha.get("QT_MAT_ZR_RUR")),
                    qt_mat_zr_urb=_safe_int(linha.get("QT_MAT_ZR_URB")),
                )
            )

    print(f"Total de instituições CSV carregadas: {len(instituicoes)}")
    return instituicoes
