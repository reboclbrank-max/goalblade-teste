#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — quem manda desenhar (v0.1).

    python3 gerar.py teste        # 1 boneco grande (para conferir a qualidade)
    python3 gerar.py folha        # folha de poses e direções
    python3 gerar.py elenco       # imagem de destaque: 5×5 no campo inteiro
    python3 gerar.py tudo
"""
import os
import sys
import time

from motor_rb import Tela, cor, escurecer, clarear, misturar
from boneco import Kit, desenhar, desenhar_com_sombra_longa

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida")

VERMELHO = Kit(camisa="e23e37", calcao="fefefe", meia="d93a33", numero=9)
AZUL = Kit(camisa="2f5fd8", calcao="111a38", meia="22336b", numero=4,
           pele="c98a5e", cabelo="14100c")
GOLEIRO_R = Kit(camisa="ffd34d", calcao="1d2430", meia="ffd34d", numero=1, pele="e8b98e")


def _preparar():
    os.makedirs(SAIDA, exist_ok=True)


# --------------------------------------------------------------------------- 1 boneco
def teste():
    _preparar()
    t = Tela(360, 400, luz=4)
    t.fundo_gradiente(cor("1c2733"), cor("0d1218"))
    t.ret(0, 330, 360, 70, cor("16321f"))
    t.elipse(180, 332, 150, 26, cor("1d4026"))
    desenhar_com_sombra_longa(t, 180, 330, 6.2, VERMELHO, "frente", "parado")
    t.salvar(os.path.join(SAIDA, "teste-boneco.png"))
    print("ok: saida/teste-boneco.png")


# --------------------------------------------------------------------------- folha
def folha():
    _preparar()
    direcoes = ["frente", "lado", "costas"]
    poses = ["parado", "corrida0", "corrida1", "chute", "comemora"]
    cw, ch = 84, 132
    t = Tela(cw * len(poses), ch * len(direcoes) + 24, luz=3)
    t.fundo_gradiente(cor("141c24"), cor("0a0f14"))
    for linha, d in enumerate(direcoes):
        faixa = cor("101820") if linha % 2 == 0 else cor("141d26")
        t.ret(0, 24 + linha * ch, cw * len(poses), ch, faixa)
        for col, p in enumerate(poses):
            x = col * cw + cw / 2.0
            y = 24 + linha * ch + ch - 14
            kit = VERMELHO if p != "chute" else AZUL
            t.elipse(x, y + 1, 26, 7, (0, 0, 0, 60))
            desenhar(t, x, y, 2.35, kit, d, p)
    # tarja de referência no topo (identifica as colunas sem precisar de letras)
    t.ret(0, 0, cw * len(poses), 24, cor("0b1016"))
    for col in range(len(poses)):
        t.ret(col * cw + 6, 8, cw - 12, 8, cor("d4af37", 90 if col % 2 else 160))
    t.salvar(os.path.join(SAIDA, "folha-poses.png"))
    print("ok: saida/folha-poses.png")


# --------------------------------------------------------------------------- elenco
def elenco():
    """Imagem de destaque: campo inteiro visto de cima, 5×5, com as sombras e o volume."""
    _preparar()
    W, H = 1280, 720
    t = Tela(W, H, luz=2)
    t.fundo_gradiente(cor("0d1512"), cor("05080a"))

    # --- gramado ---
    gx, gy, gw, gh = 60, 70, W - 120, H - 190
    t.ret(gx - 26, gy - 22, gw + 52, gh + 44, cor("24502c"))
    t.ret_arredondado(gx - 26, gy - 22, gw + 52, gh + 44, 8, cor("24502c"))
    faixa = gw / 12.0
    for i in range(12):
        c = cor("3a7c3f") if i % 2 == 0 else cor("337036")
        t.ret(gx + i * faixa, gy, faixa + 0.5, gh, c)
    # desgaste no meio e nas áreas (dá "campo de verdade")
    t.elipse(gx + gw * 0.5, gy + gh * 0.5, gw * 0.10, gh * 0.24, cor("2e6a34", 120))
    t.elipse(gx + gw * 0.06, gy + gh * 0.5, gw * 0.045, gh * 0.18, cor("2e6a34", 110))
    t.elipse(gx + gw * 0.94, gy + gh * 0.5, gw * 0.045, gh * 0.18, cor("2e6a34", 110))

    # --- linhas ---
    branco = cor("eef4ee", 235)
    def linha(x1, y1, x2, y2, larg=3.0):
        t.linha(gx + x1, gy + y1, gx + x2, gy + y2, larg, (0, 0, 0, 70))
        t.linha(gx + x1, gy + y1 - 2, gx + x2, gy + y2 - 2, larg, branco)

    linha(0, 0, gw, 0)
    linha(0, gh, gw, gh)
    linha(0, 0, 0, gh)
    linha(gw, 0, gw, gh)
    linha(gw / 2, 0, gw / 2, gh)
    linha(0, gh * 0.5 - 52, 78, gh * 0.5 - 52)
    linha(0, gh * 0.5 + 52, 78, gh * 0.5 + 52)
    linha(78, gh * 0.5 - 52, 78, gh * 0.5 + 52)
    linha(gw, gh * 0.5 - 52, gw - 78, gh * 0.5 - 52)
    linha(gw, gh * 0.5 + 52, gw - 78, gh * 0.5 + 52)
    linha(gw - 78, gh * 0.5 - 52, gw - 78, gh * 0.5 + 52)
    linha(0, gh * 0.5 - 22, 32, gh * 0.5 - 22)
    linha(0, gh * 0.5 + 22, 32, gh * 0.5 + 22)
    linha(32, gh * 0.5 - 22, 32, gh * 0.5 + 22)
    linha(gw, gh * 0.5 - 22, gw - 32, gh * 0.5 - 22)
    linha(gw, gh * 0.5 + 22, gw - 32, gh * 0.5 + 22)
    linha(gw - 32, gh * 0.5 - 22, gw - 32, gh * 0.5 + 22)
    t.anel(gx + gw / 2, gy + gh / 2, 78, 3.0, branco)
    t.circulo(gx + gw / 2, gy + gh / 2, 3.4, branco)
    t.circulo(gx + 78 * 0.72, gy + gh / 2, 3.0, branco)
    t.circulo(gx + gw - 78 * 0.72, gy + gh / 2, 3.0, branco)

    # --- gols (trave branca + rede) ---
    def gol(x0, para_dentro):
        gh2, prof = 84, 14
        y0 = gy + gh / 2 - gh2 / 2
        t.ret(x0, y0, prof * (1 if para_dentro else -1), gh2, cor("0a1a10", 150))
        for k in range(1, 6):
            yy = y0 + k * gh2 / 6.0
            t.linha(x0, yy, x0 + prof * (1 if para_dentro else -1), yy, 1.2, (255, 255, 255, 90))
        t.ret_arredondado(min(x0, x0 + prof * (1 if para_dentro else -1)), y0, prof, gh2, 3, cor("f2f6f2", 255))
        t.ret(x0 + (2 if para_dentro else -2) - 2, y0 + 4, prof - 4, gh2 - 8, cor("0a1a10", 120))
    gol(gx, True)
    gol(gx + gw, False)

    # --- banco de reservas / beira do campo ---
    t.ret(0, H - 108, W, 108, cor("0b1218"))
    for i in range(26):
        t.circulo(28 + i * 48, H - 78, 9, cor(["d66054", "567ac6", "e4d8c0", "568c64", "c4ac80"][i % 5], 150))

    # --- times (5×5: goleiro + 2 zagueiros + meia + atacante) ---
    def time(kit, gk, lado):
        escala = 3.0
        base_x = gx + (gw * 0.22 if lado == 0 else gw * 0.78)
        # goleiro
        desenhar(t, gx + (24 if lado == 0 else gw - 24), gy + gh / 2, escala, gk,
                 "lado" if lado == 1 else "lado", "parado")
        posicoes = [
            (0.10, 0.30, "frente"), (0.10, 0.70, "frente"),
            (0.28, 0.50, "lado"), (0.44, 0.50, "corrida1"),
        ]
        for i, (fx, fy, po) in enumerate(posicoes):
            px = gx + (gw * (0.30 + fx * 0.9) if lado == 0 else gw * (0.70 - fx * 0.9))
            py = gy + gh * fy
            desenhar(t, px, py, escala, kit, po, "corrida0" if i % 2 == 0 else "parado")
    time(VERMELHO, GOLEIRO_R, 0)
    time(AZUL, GOLEIRO_R, 1)

    # --- bola no círculo central ---
    bx, by = gx + gw / 2 + 26, gy + gh / 2 + 10
    t.elipse(bx + 3, by + 6, 11, 5, (0, 0, 0, 90))
    t.circulo(bx, by, 9, cor("f6f8f4"))
    t.circulo(bx, by, 3.2, cor("1a1c22"))
    for i in range(5):
        a = i * 1.2566
        import math
        t.circulo(bx + math.cos(a) * 5.6, by + math.sin(a) * 5.6, 1.9, cor("1a1c22"))

    t.salvar(os.path.join(SAIDA, "elenco-5x5.png"))
    print("ok: saida/elenco-5x5.png")


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    t0 = time.time()
    if alvo in ("teste", "tudo"):
        teste()
    if alvo in ("folha", "tudo"):
        folha()
    if alvo in ("elenco", "tudo"):
        elenco()
    print("tempo: %.1f s" % (time.time() - t0))
