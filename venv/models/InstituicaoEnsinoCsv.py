class InstituicaoEnsinoCsv():
    def __init__(self, codigo, nome, co_uf, co_municipio, qt_mat_bas, qt_mat_prof, qt_mat_eja, qt_mat_esp, qt_mat_fund, qt_mat_inf, qt_mat_med, qt_mat_zr_na, qt_mat_zr_rur, qt_mat_zr_urb):
        self.codigo = codigo
        self.nome = nome
        self.co_uf = co_uf
        self.co_municipio = co_municipio
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_med = qt_mat_med
        self.qt_mat_zr_na = qt_mat_zr_na
        self.qt_mat_zr_rur = qt_mat_zr_rur
        self.qt_mat_zr_urb = qt_mat_zr_urb

    def to_json(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "co_uf": self.co_uf,
            "co_municipio": self.co_municipio,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_prof": self.qt_mat_prof,
            "qt_mat_eja": self.qt_mat_eja,
            "qt_mat_esp": self.qt_mat_esp,
            "qt_mat_fund": self.qt_mat_fund,
            "qt_mat_inf": self.qt_mat_inf,
            "qt_mat_med": self.qt_mat_med,
            "qt_mat_zr_na": self.qt_mat_zr_na,
            "qt_mat_zr_rur": self.qt_mat_zr_rur,
            "qt_mat_zr_urb": self.qt_mat_zr_urb
        }
