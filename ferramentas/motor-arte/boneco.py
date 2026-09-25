#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — desenho do boneco (v0.2 — anatomia refeita depois de ver a v0.1 "massinha").

Regras que o motor segue (é isto que dá a "qualidade"):
  · proporção: 5,5 cabeças de altura; ombro mais largo que a cintura; perna mais comprida que o tronco;
  · silhueta: cada peça tem CONTORNO escuro (o boneco lê bem em fundo claro ou escuro);
  · volume: brilho em cima/esquerda, sombra embaixo/direita, e sombra no chão sempre;
  · membros: manga (cor do uniforme) → pele; calção → pele da coxa → meia → chuteira;
  · número no peito, pequeno, com contorno.

Unidade (u): o boneco tem ~42u de altura e os PÉS ficam em (x, y) — assim ele "anda" pelo campo.
"""
import math

from motor_rb import Tela, cor, escurecer, clarear

POSES = {
    "parado":   dict(perna=6.0,   braco=13.0,  bob=0.0,  joelho=3.0,  tipo="parado"),
    "corrida0": dict(perna=32.0,  braco=32.0,  bob=-0.9, joelho=30.0, tipo="corrida"),
    "corrida1": dict(perna=6.0,   braco=12.0,  bob=0.4,  joelho=8.0,  tipo="corrida"),
    "corrida2": dict(perna=-32.0, braco=-32.0, bob=-0.9, joelho=30.0, tipo="corrida"),
    "corrida3": dict(perna=6.0,   braco=12.0,  bob=0.4,  joelho=8.0,  tipo="corrida"),
    "chute":    dict(perna=52.0,  braco=34.0,  bob=-0.4, joelho=-18.0, tipo="chute"),
    "comemora": dict(perna=10.0,  braco=158.0, bob=-1.6, joelho=12.0, tipo="comemora"),
}


class Kit:
    def __init__(self, camisa, calcao, meia, numero=9, pele="e8b98e", cabelo="2c1e16",
                 bota="191a1f", contorno="141922", listras=None, cabelo_tipo="curto"):
        self.camisa = cor(camisa)
        self.camisa_escura = escurecer(self.camisa, 0.32)
        self.calcao = cor(calcao)
        self.meia = cor(meia)
        self.pele = cor(pele)
        self.cabelo = cor(cabelo)
        self.bota = cor(bota)
        self.contorno = cor(contorno)
        self.numero = numero
        self.listras = cor(listras) if listras is not None else None   # listras verticais na camisa
        self.cabelo_tipo = cabelo_tipo                                  # curto | raspado | black | cacheado | calvo


# --------------------------------------------------------------------------- utilidades
def _peca(tela, a, b, largura, c, escurece=0.30, clareia=0.50):
    """Uma peça do corpo: contorno, corpo, sombra interna e brilho."""
    cont = cor("141922")
    tela.linha(a[0], a[1], b[0], b[1], largura + 1.9, cont)
    tela.linha(a[0], a[1], b[0], b[1], largura, c)
    d = largura * 0.26
    tela.linha(a[0] + d, a[1] + d, b[0] + d, b[1] + d, largura * 0.42, escurecer(c, escurece)[:3] + (120,))
    tela.linha(a[0] - d * 0.9, a[1] - d * 0.9, b[0] - d * 0.9, b[1] - d * 0.9, largura * 0.30,
               clarear(c, clareia)[:3] + (110,))


def _bolinha(tela, cx, cy, r, c):
    tela.circulo(cx, cy, r + 1.5, cor("141922"))
    tela.circulo(cx, cy, r, c)
    tela.circulo(cx - r * 0.28, cy - r * 0.30, r * 0.42, clarear(c, 0.5)[:3] + (105,))


# --------------------------------------------------------------------------- boneco
def desenhar(tela, x, y, u, kit, direcao="frente", pose="parado", numero=None):
    p = POSES.get(pose, POSES["parado"])
    perfil = direcao == "lado"
    costas = direcao == "costas"

    # esqueleto (em unidades): pés em y
    QY = -19.6 * u          # quadril
    SY = -30.4 * u          # ombros
    HY = -37.8 * u          # centro da cabeça
    RAIO_CABECA = 4.6 * u
    meia_cintura = 3.9 * u
    meia_ombro = 4.9 * u
    bob = p["bob"] * u

    def P(dx, dy):
        return (x + dx, y + dy + bob)

    # ---- sombra no chão (a peça que faz o boneco "pisar" no campo) ----
    tela.elipse(x + 0.5 * u, y + 0.9 * u, 7.6 * u, 2.5 * u, (0, 0, 0, 70))

    ombro_e = P(-meia_ombro, SY)
    ombro_d = P(meia_ombro, SY)
    quadril_e = P(-meia_cintura, QY)
    quadril_d = P(meia_cintura, QY)

    # ---- membros de trás (tom mais escuro = profundidade) ----
    def perna(sinal, perto):
        ang = p["perna"] * (1.0 if perfil else 0.42)
        if p["tipo"] == "chute" and sinal > 0:
            ang = p["perna"]
        if p["tipo"] in ("parado", "comemora"):
            ang = p["perna"] * (1.0 if perfil else 0.30)
        fator = 1.0 if perto else 0.86
        c_pele = kit.pele if perto else escurecer(kit.pele, 0.28)
        c_meia = kit.meia if perto else escurecer(kit.meia, 0.28)
        c_calcao = kit.calcao if perto else escurecer(kit.calcao, 0.24)
        q = (quadril_e if sinal < 0 else quadril_d)
        a1 = math.radians(ang)
        comp_coxa = 9.9 * u
        j = (q[0] + math.sin(a1) * comp_coxa, q[1] + math.cos(a1) * comp_coxa)   # joelho
        a2 = math.radians(ang + p["joelho"] * (1 if sinal > 0 else -0.55))
        comp_canela = 9.9 * u
        f = (j[0] + math.sin(a2) * comp_canela, j[1] + math.cos(a2) * comp_canela)  # pé
        # calção cobrindo o topo da coxa
        _peca(tela, (q[0], q[1] - 1.4 * u), (q[0] + math.sin(a1) * 4.6 * u * fator,
              q[1] + math.cos(a1) * 4.2 * u * fator), 4.2 * fator * u, c_calcao)
        # coxa (pele)
        _peca(tela, (q[0] + math.sin(a1) * 3.6 * u * fator, q[1] + math.cos(a1) * 3.6 * u * fator),
              j, 3.2 * fator * u, c_pele)
        # canela (meia, um pouco mais fina)
        _peca(tela, j, f, 2.9 * fator * u, c_meia)
        # chuteira
        comp = 5.2 * u * fator
        apoia = (not perfil)
        if apoia:
            tela.ret_arredondado(f[0] - 2.3 * u * fator, f[1] - 1.1 * u * fator, 4.6 * u * fator, 2.9 * u * fator, 1.1,
                                 cor("141922"))
            tela.ret_arredondado(f[0] - 1.9 * u * fator, f[1] - 0.8 * u * fator, 3.8 * u * fator, 2.2 * u * fator, 0.9,
                                 kit.bota)
            tela.ret(f[0] - 1.9 * u * fator, f[1] + 0.6 * u * fator, 3.8 * u * fator, 0.7 * u * fator,
                     clarear(kit.bota, 0.40)[:3] + (150,))
        else:
            tela.ret_arredondado(f[0] - 1.2 * u * fator, f[1] - comp * 0.40, 2.4 * u * fator, comp, 1.1, cor("141922"))
            tela.ret_arredondado(f[0] - 0.8 * u * fator, f[1] - comp * 0.34, 1.7 * u * fator, comp * 0.9, 0.8, kit.bota)
        return f

    def braco(sinal, perto):
        ang = p["braco"] * (1.0 if perfil else 0.80)
        if p["tipo"] in ("parado",):
            ang = p["braco"] * (1.0 if perfil else 0.75)
        if p["tipo"] == "comemora":
            ang = 158.0 if perfil else (158.0 if sinal > 0 else -150.0)
        fator = 1.0 if perto else 0.88
        c_camisa = kit.camisa if perto else escurecer(kit.camisa, 0.26)
        c_pele = kit.pele if perto else escurecer(kit.pele, 0.26)
        o = (ombro_e if sinal < 0 else ombro_d)
        a1 = math.radians(ang)
        c = (o[0] + math.sin(a1) * 7.3 * u, o[1] + math.cos(a1) * 7.3 * u)      # cotovelo
        a2 = math.radians(ang + 7.0)
        m = (c[0] + math.sin(a2) * 6.9 * u, c[1] + math.cos(a2) * 6.9 * u)      # mão
        _peca(tela, o, (o[0] + math.sin(a1) * 3.4 * u, o[1] + math.cos(a1) * 3.4 * u), 3.3 * fator * u, c_camisa)  # manga curta
        _peca(tela, (o[0] + math.sin(a1) * 3.0 * u, o[1] + math.cos(a1) * 3.0 * u), c, 2.6 * fator * u, c_pele)     # braço
        _peca(tela, c, m, 2.4 * fator * u, c_pele)                             # antebraço
        _bolinha(tela, m[0], m[1], 1.75 * fator * u, c_pele)                   # mão
        return m

    perna(-1, False)
    braco(-1, False)

    # ---- tronco: peito mais largo, cintura mais fina (dois segmentos) ----
    ySY = y + SY + bob
    yQY = y + QY + bob
    yPEITO = y + SY + 4.6 * u + bob
    yCINTURA = y + QY + 1.4 * u + bob
    _peca(tela, (x, ySY + 1.2 * u), (x, yPEITO), 11.0 * u, kit.camisa)
    _peca(tela, (x, yPEITO), (x, yCINTURA), 8.4 * u, kit.camisa)
    # ombros arredondados
    _bolinha(tela, ombro_e[0] + 0.3 * u, ombro_e[1] + 1.6 * u, 1.7 * u, kit.camisa)
    _bolinha(tela, ombro_d[0] - 0.3 * u, ombro_d[1] + 1.6 * u, 1.7 * u, kit.camisa)
    # listras verticais do uniforme (opcional) — desenhadas dentro do tronco
    if kit.listras is not None:
        for k in (-1, 0, 1):
            lx = x + k * 3.4 * u
            tela.linha(lx, ySY + 2.6 * u, lx, yCINTURA - 0.4 * u, 1.5 * u, kit.listras)
    # gola
    tela.elipse(x, ySY + 1.4 * u, 3.6 * u, 1.7 * u, kit.camisa_escura)
    # número no peito
    esc = max(1, int(round(u * 0.62)))
    tela.texto_numero(str(kit.numero if numero is None else numero), x, ySY + 5.6 * u, esc,
                      (255, 255, 255, 235), contorno=(0, 0, 0, 110))

    perna(1, True)
    braco(1, True)

    # ---- pescoço, cabeça e cabelo ----
    yHY = y + HY + bob
    _peca(tela, (x, ySY + 1.6 * u), (x, yHY + RAIO_CABECA * 0.78), 2.4 * u, kit.pele, 0.24, 0.35)
    cy = yHY
    if costas:
        _bolinha(tela, x, cy, RAIO_CABECA, kit.cabelo)
        tela.circulo(x, cy + RAIO_CABECA * 0.55, RAIO_CABECA * 0.72, escurecer(kit.cabelo, 0.35))
    elif perfil:
        _bolinha(tela, x, cy, RAIO_CABECA, kit.cabelo)
        tela.circulo(x + 2.1 * u, cy + 1.3 * u, RAIO_CABECA * 0.78, kit.pele)      # rosto de perfil
        tela.circulo(x + 3.6 * u, cy + 0.9 * u, 0.62 * u, cor("20242c"))           # olho
        tela.circulo(x - 0.6 * u, cy - 1.2 * u, RAIO_CABECA * 0.95, kit.cabelo)    # cabelo no topo
        tela.circulo(x + 1.0 * u, cy - RAIO_CABECA * 0.55, 1.7 * u, clarear(kit.cabelo, 0.35)[:3] + (110,))
        tela.circulo(x - 1.6 * u, cy + 0.6 * u, 1.0 * u, escurecer(kit.pele, 0.18))  # orelha
    else:
        _bolinha(tela, x, cy, RAIO_CABECA, kit.pele)
        tipo = kit.cabelo_tipo
        if tipo == "calvo":
            tela.circulo(x - 1.6 * u, cy - RAIO_CABECA * 0.55, 1.5 * u, clarear(kit.pele, 0.35))
        elif tipo == "raspado":
            tela.circulo(x, cy - RAIO_CABECA * 0.58, RAIO_CABECA * 0.90, escurecer(kit.cabelo, 0.10))
        elif tipo == "black":
            tela.circulo(x, cy - RAIO_CABECA * 0.30, RAIO_CABECA * 1.16, kit.cabelo)
            tela.circulo(x - RAIO_CABECA * 0.85, cy - RAIO_CABECA * 0.15, RAIO_CABECA * 0.62, kit.cabelo)
            tela.circulo(x + RAIO_CABECA * 0.85, cy - RAIO_CABECA * 0.15, RAIO_CABECA * 0.62, kit.cabelo)
            tela.circulo(x, cy - RAIO_CABECA * 0.72, RAIO_CABECA * 0.96, kit.cabelo)
        elif tipo == "cacheado":
            for k in range(7):
                import math as _m
                a = _m.pi * (0.15 + 0.70 * k / 6.0)
                tela.circulo(x - _m.cos(a) * RAIO_CABECA * 0.92, cy - _m.sin(a) * RAIO_CABECA * 0.86,
                             RAIO_CABECA * 0.42, kit.cabelo)
            tela.circulo(x, cy - RAIO_CABECA * 0.52, RAIO_CABECA * 0.94, kit.cabelo)
        else:  # curto
            tela.ret_arredondado(x - RAIO_CABECA * 1.02, cy - RAIO_CABECA * 1.06, RAIO_CABECA * 2.04,
                                 RAIO_CABECA * 0.98, RAIO_CABECA * 0.50, kit.cabelo)
            tela.circulo(x, cy - RAIO_CABECA * 0.62, RAIO_CABECA * 0.92, kit.cabelo)
        tela.circulo(x - 1.65 * u, cy + 0.5 * u, 0.60 * u, cor("20242c"))          # olhos
        tela.circulo(x + 1.65 * u, cy + 0.5 * u, 0.60 * u, cor("20242c"))
        tela.circulo(x - 2.6 * u, cy + 1.5 * u, 0.75 * u, escurecer(kit.pele, 0.16))   # orelhas
        tela.circulo(x + 2.6 * u, cy + 1.5 * u, 0.75 * u, escurecer(kit.pele, 0.16))
        tela.circulo(x - 1.5 * u, cy - RAIO_CABECA * 0.86, 1.7 * u, clarear(kit.cabelo, 0.35)[:3] + (115,))


def desenhar_com_sombra_longa(tela, x, y, u, kit, direcao="frente", pose="parado"):
    tela.elipse(x - 4.0 * u, y + 1.2 * u, 12.0 * u, 3.4 * u, (0, 0, 0, 52))
    desenhar(tela, x, y, u, kit, direcao, pose)
