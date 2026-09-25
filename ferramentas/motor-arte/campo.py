#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — campo de futebol (v0.1).

Desenha o campo inteiro como IMAGEM, com qualidade de arte:
  · grama com listras de corte, **gradiente de luz** e textura (fios) desenhada uma única vez;
  · **desgaste** nas áreas e no meio (onde mais se pisa) e poça de luz no centro;
  · **linhas** com sombra (as linhas ficam "deitadas" no gramado, não flutuando);
  · **gols** com trave, fundo escuro, rede fina e sombra no gramado;
  · área externa: pista, mureta com painéis, **arquibancada com torcida** em fileiras;
  · **vinheta** e escurecimento nas bordas (profundidade de câmera de TV).

Por que assim: o jogo passa a carregar UMA imagem em vez de desenhar o campo por código a cada
quadro. Melhor desenho E menos trabalho para o celular.

Geometria (bate exatamente com o GoalBlade):
  A imagem tem `img_w` × `img_h` pixels e cobre `mundo` unidades de mundo.
  O campo (620×380 unidades) ocupa a parte central, calculada por essa proporção.
"""
import math

from motor_rb import Tela, cor, escurecer, clarear, misturar

# medidas do GoalBlade (unidades de mundo)
CAMPO_W, CAMPO_H = 620.0, 380.0
MUNDO = 900.0
IMG_W, IMG_H = 1280, 720


def _px(v):
    """Unidade de mundo -> pixel da imagem."""
    return v * (IMG_W / MUNDO)


def desenhar(tela, x, y, w, h, torcida=True):
    """Campos com as bordas do campo em pixels (x, y, w, h)."""
    # ------------------------------------------------------------------ fora do campo
    tela.ret(0, 0, tela.W, tela.H, cor("26492c"))
    # MURETA FECHADA 100% (exigência: bola só sai no gol, ou bate e volta)
    # Desenho quadrado, sem arredondamento, com vão apenas na boca do gol
    marg = 22
    parede = 14
    cor_parede = cor("9aa8a2")
    cor_sombra = (0, 0, 0, 90)
    # fundo da pista externa
    tela.ret(0, 0, tela.W, tela.H, cor("1e2b1f"))
    # parede superior e inferior (fechadas)
    tela.ret(x - marg - parede, y - marg - parede, w + 2*(marg+parede), parede, cor_parede)
    tela.ret(x - marg - parede, y - marg - parede, w + 2*(marg+parede), 2, (255,255,255, 45)) # brilho
    tela.ret(x - marg - parede, y + h + marg, w + 2*(marg+parede), parede, cor_parede)
    tela.ret(x - marg - parede, y + h + marg + parede -2, w + 2*(marg+parede), 2, (0,0,0, 55)) # sombra
    # paredes laterais com VÃO apenas na boca do gol (quadrado)
    gh = h * 0.22
    cy = y + h/2
    # lateral esquerda: dois segmentos (acima e abaixo do gol)
    tela.ret(x - marg - parede, y - marg - parede, parede, (cy - gh/2) - (y - marg - parede), cor_parede)
    tela.ret(x - marg - parede, cy + gh/2, parede, (y + h + marg + parede) - (cy + gh/2), cor_parede)
    # lateral direita: idem
    tela.ret(x + w + marg, y - marg - parede, parede, (cy - gh/2) - (y - marg - parede), cor_parede)
    tela.ret(x + w + marg, cy + gh/2, parede, (y + h + marg + parede) - (cy + gh/2), cor_parede)
    # sombra da mureta no gramado (profundidade)
    tela.ret(x, y, w, 3, (0,0,0, 55))
    tela.ret(x, y + h -3, w, 3, (0,0,0, 55))
    tela.ret(x, y, 3, h, (0,0,0, 45))
    tela.ret(x + w -3, y, 3, h, (0,0,0, 45))
    # cantos quadrados reforçados
    for cx, cy2 in ((x - marg - parede, y - marg - parede), (x + w + marg, y - marg - parede), (x - marg - parede, y + h + marg), (x + w + marg, y + h + marg)):
        tela.ret(cx, cy2, parede, parede, cor_parede)

    # ------------------------------------------------------------------ grama
    gx, gy = x, y
    faixas = 12
    largura_faixa = w / faixas
    for i in range(faixas):
        base = cor("3c8142") if i % 2 == 0 else cor("347238")
        tela.ret(gx + i * largura_faixa, gy, largura_faixa + 0.6, h, base)

    # luz vinda de cima: gradiente suave sobre toda a grama
    for j in range(0, int(h), 2):
        t = j / max(1.0, h)
        tela.ret(gx, gy + j, w, 2, (255, 255, 255, int(16 * (1.0 - t))))

    # textura de fios (desenhada UMA vez) — dá "grama", não "plástico"
    for n in range(5200):
        fx = gx + ((n * 137.508) % w)
        fy = gy + ((n * 71.17) % h)
        claro = (n % 3 == 0)
        c = (255, 255, 255, 16) if claro else (0, 0, 0, 14)
        tela.linha(fx, fy, fx + (1.4 if claro else -1.2), fy - 2.1, 0.9, c)

    # desgaste: onde mais se pisa (meio e áreas)
    tela.elipse(gx + w * 0.5, gy + h * 0.5, w * 0.055, h * 0.13, cor("39743c", 150))
    tela.elipse(gx + w * 0.06, gy + h * 0.5, w * 0.030, h * 0.10, cor("417a41", 140))
    tela.elipse(gx + w * 0.94, gy + h * 0.5, w * 0.030, h * 0.10, cor("417a41", 140))
    tela.elipse(gx + w * 0.30, gy + h * 0.5, w * 0.020, h * 0.06, cor("417a41", 90))
    tela.elipse(gx + w * 0.70, gy + h * 0.5, w * 0.020, h * 0.06, cor("417a41", 90))

    # ------------------------------------------------------------------ linhas
    def linha(x1, y1, x2, y2, larg=2.6):
        tela.linha(gx + x1, gy + y1 + 1.6, gx + x2, gy + y2 + 1.6, larg, (0, 0, 0, 90))
        tela.linha(gx + x1, gy + y1, gx + x2, gy + y2, larg, (244, 248, 244, 238))

    def ret4(x1, y1, x2, y2, larg=2.6):
        linha(x1, y1, x2, y1, larg)
        linha(x1, y2, x2, y2, larg)
        linha(x1, y1, x1, y2, larg)
        linha(x2, y1, x2, y2, larg)

    ret4(0, 0, w, h)
    linha(w / 2, 0, w / 2, h)
    tela.anel(gx + w / 2, gy + h / 2, h * 0.134, 2.6, (0, 0, 0, 90))
    tela.anel(gx + w / 2, gy + h / 2, h * 0.134 - 1.6, 2.6, (244, 248, 244, 238))
    tela.circulo(gx + w / 2, gy + h / 2, 3.4, (244, 248, 244, 240))
    # áreas FIFA reais (precisas: 105x68) — antes 0.203/0.085 estavam grandes, gol parecia antecipado
    are_w, are_h = w * 0.157, h * 0.593  # 16.5m / 40.32m
    peq_w, peq_h = w * 0.052, h * 0.269  # 5.5m / 18.32m
    ret4(0, (h - are_h) / 2, are_w, (h + are_h) / 2)
    ret4(0, (h - peq_h) / 2, peq_w, (h + peq_h) / 2)
    ret4(w - are_w, (h - are_h) / 2, w, (h + are_h) / 2)
    ret4(w - peq_w, (h - peq_h) / 2, w, (h + peq_h) / 2)
    # marca do pênalti a 11m da linha (0.105*w) — antes 0.146*w estava adiantada
    tela.circulo(gx + w * 0.105, gy + h / 2, 3.0, (244, 248, 244, 235))
    tela.circulo(gx + w - w * 0.105, gy + h / 2, 3.0, (244, 248, 244, 235))
    # arcos de canto
    rc = h * 0.035
    for cx, cy, a0, a1 in ((0, 0, 0.0, math.pi / 2), (w, 0, math.pi / 2, math.pi),
                           (0, h, -math.pi / 2, 0.0), (w, h, math.pi, math.pi * 1.5)):
        tela.anel(gx + cx, gy + cy, rc, 2.4, (244, 248, 244, 225))

    # ------------------------------------------------------------------ gols - POSIÇÃO CORRIGIDA 25/09: gol na LINHA, para FORA (não antecipado)
    def gol(lado_esquerdo):
        gh, prof = h * 0.22, 26
        cy = gy + h / 2
        # gol fica FORA do campo, com a boca na linha (gx / gx+w) e a rede na pista (marg)
        x0 = (gx - prof) if lado_esquerdo else (gx + w)
        # fundo do gol (escuro) + rede quadrada (sem arredondamento)
        tela.ret(x0, cy - gh / 2, prof, gh, (6, 20, 12, 195))
        # rede quadrada bem marcada
        passo = 3.0
        j = cy - gh / 2
        while j <= cy + gh / 2:
            tela.linha(x0, j, x0 + prof, j, 0.8, (255, 255, 255, 75))
            j += passo
        k = x0
        while k <= x0 + prof:
            tela.linha(k, cy - gh / 2, k, cy + gh / 2, 0.8, (255, 255, 255, 60))
            k += passo
        # trave QUADRADA (exigência do dono) — sem arredondamento, cantos 90°
        # sombra quadrada no gramado
        tela.ret(x0 - 1, cy - gh / 2 - 4, prof + 2, 5, (0, 0, 0, 95))
        tela.ret(x0 - 1, cy + gh / 2 - 1, prof + 2, 5, (0, 0, 0, 85))
        # travessão e postes quadrados, brancos bem grossos
        tela.ret(x0 - 2, cy - gh / 2 - 5, prof + 4, 6, (245, 248, 245, 255))
        tela.ret(x0 - 2, cy + gh / 2 - 1, prof + 4, 6, (245, 248, 245, 255))
        tela.ret(x0 - 2, cy - gh / 2 - 5, 6, gh + 10, (245, 248, 245, 255))
        if not lado_esquerdo:
            tela.ret(x0 + prof - 4, cy - gh / 2 - 5, 6, gh + 10, (245, 248, 245, 255))
        else:
            tela.ret(x0 + prof - 4, cy - gh / 2 - 5, 6, gh + 10, (245, 248, 245, 255))
        # sombra dura do gol no gramado (profundidade) — a partir da boca (linha)
        if lado_esquerdo:
            boca = gx  # boca na linha do campo
            for d in range(4, 32, 3):
                tela.ret(boca + d, cy - gh / 2, 3, gh, (0, 0, 0, max(7, 38 - d)))
        else:
            boca = gx + w
            for d in range(4, 32, 3):
                tela.ret(boca - d - 3, cy - gh / 2, 3, gh, (0, 0, 0, max(7, 38 - d)))

    gol(True)
    gol(False)

    # ------------------------------------------------------------------ bandeirinhas
    def bandeirinha(cx, cy, mais_para_baixo):
        tela.elipse(cx + 2.5, cy + 2.2, 6.5, 2.4, (0, 0, 0, 90))
        tela.linha(cx, cy, cx, cy - 17, 1.7, "238242238")
        ponto = cor("f2c14a")
        tela.poligono([(cx, cy - 17), (cx + 11, cy - 13 if mais_para_baixo else cy - 14), (cx, cy - 9)], ponto)

    bandeirinha(gx + 2, gy + 3, True)
    bandeirinha(gx + w - 2, gy + 3, True)
    bandeirinha(gx + 2, gy + h - 3, False)
    bandeirinha(gx + w - 2, gy + h - 3, False)

    # ------------------------------------------------------------------ arquibancadas
    if torcida:
        faixa_top = max(12.0, y - marg - 6)
        faixa_bot = max(12.0, tela.H - (y + h + marg + 6))
        laterais = max(8.0, x - marg - 6)
        _arquibancada(tela, 0, 0, tela.W, faixa_top, baixo=False)
        _arquibancada(tela, 0, y + h + marg + 6, tela.W, faixa_bot, baixo=True)
        _arquibancada(tela, 0, faixa_top, laterais, tela.H - faixa_top - faixa_bot, baixo=False, vertical=True)
        _arquibancada(tela, tela.W - laterais, faixa_top, laterais, tela.H - faixa_top - faixa_bot,
                      baixo=False, vertical=True)

    # ---- sombra das arquibancadas caindo no campo (profundidade) ----
    if torcida:
        for d in range(0, 14):
            a = int(70 * (1.0 - d / 14.0))
            tela.ret(x, y + d, w, 1, (0, 0, 0, a))
            tela.ret(x, y + h - 1 - d, w, 1, (0, 0, 0, a))
            tela.ret(x + d, y, 1, h, (0, 0, 0, a))
            tela.ret(x + w - 1 - d, y, 1, h, (0, 0, 0, a))

    # ------------------------------------------------------------------ vinheta (profundidade)
    for i in range(90):
        t = i / 90.0
        a = int(52 * (t ** 3))
        tela.ret(i, 0, 1, tela.H, (0, 0, 0, a))
        tela.ret(tela.W - 1 - i, 0, 1, tela.H, (0, 0, 0, a))
        tela.ret(0, i, tela.W, 1, (0, 0, 0, a))
        tela.ret(0, tela.H - 1 - i, tela.W, 1, (0, 0, 0, a))


def _arquibancada(tela, x, y, w, h, baixo=False, vertical=False):
    """Arquibancada: degraus escuros, fileiras de torcida e mureta com painéis."""
    if w < 6 or h < 6:
        return
    tela.ret(x, y, w, h, cor("1a1f27"))
    fileiras = max(2, int(h / 17)) if not vertical else max(2, int(w / 17))
    cores = [cor("d66054"), cor("567ac6"), cor("e4d8c0"), cor("568c64"), cor("c4ac80"),
             cor("3c4254"), cor("b1543f"), cor("6f8fbf")]
    if not vertical:
        for r in range(fileiras):
            yy = y + (h * (r + 0.5) / fileiras)
            # degrau
            tela.ret(x, yy + 5, w, 2.0, cor("10141a", 200))
            tela.ret(x, yy + 4.0, w, 1.4, (0, 0, 0, 120))          # sombra do degrau
            tela.ret(x, yy + 5.4, w, 2.4, (26, 32, 42, 210))
            passo = 11
            n = int(w / passo)
            for i in range(n):
                xx = x + i * passo + ((r % 2) * 5.5)
                c = cores[(i * 3 + r * 5) % len(cores)]
                if (i * 7 + r * 3) % 5 == 0:
                    continue                      # cadeira vazia: quebra a repetição
                tam = 3.1 if (i + r) % 3 else 2.6
                tela.circulo(xx, yy, tam + 0.5, (0, 0, 0, 70))
                tela.circulo(xx - 0.4, yy - 0.6, tam, c)
                tela.circulo(xx - 1.1, yy - 1.5, tam * 0.42, clarear(c, 0.40)[:3] + (170,))
    else:
        for c in range(fileiras):
            xx = x + (w * (c + 0.5) / fileiras)
            tela.ret(xx + 5, y, 2.0, h, cor("10141a", 200))
            tela.ret(xx + 4.0, y, 1.4, h, (0, 0, 0, 120))
            tela.ret(xx + 5.4, y, 2.4, h, (26, 32, 42, 210))
            passo = 11
            n = int(h / passo)
            for i in range(n):
                yy = y + i * passo + ((c % 2) * 5.5)
                corx = cores[(i * 5 + c * 3) % len(cores)]
                if (i * 7 + c * 3) % 5 == 0:
                    continue
                tam = 3.1 if (i + c) % 3 else 2.6
                tela.circulo(xx, yy, tam + 0.5, (0, 0, 0, 70))
                tela.circulo(xx - 0.4, yy - 0.6, tam, corx)
                tela.circulo(xx - 1.1, yy - 1.5, tam * 0.42, clarear(corx, 0.40)[:3] + (170,))
    # mureta com painéis (na beira de baixo, virada para o campo)
    if baixo and h > 26:
        tela.ret(x, y, w, 12, cor("2b3440"))
        for i in range(int(w // 120) + 1):
            c = [cor("2f6fd0"), cor("d0a22f"), cor("c14b3f"), cor("2f9e63")][i % 4]
            tela.ret(x + i * 120 + 2, y + 2, 116, 8, (c[0], c[1], c[2], 90))
    if (not baixo) and h > 26:
        tela.ret(x, y + h - 12, w, 12, cor("2b3440"))
        for i in range(int(w // 120) + 1):
            c = [cor("2f6fd0"), cor("d0a22f"), cor("c14b3f"), cor("2f9e63")][i % 4]
            tela.ret(x + i * 120 + 2, y + h - 10, 116, 8, (c[0], c[1], c[2], 80))


def gerar(caminho_saida=None, com_torcida=True, luz=2):
    """Gera a imagem do campo no formato exato que o GoalBlade usa."""
    tela = Tela(IMG_W, IMG_H, luz=luz)
    # A imagem cobre 900 unidades de mundo na largura (1.4222 px por unidade); em altura,
    # 720 px = 506 unidades. O campo fica CENTRADO (é o que a câmera do jogo mostra).
    # AJUSTE 25/09 19:48 – campo estava encurtado/pequeno; escala 1.08 para ficar perfeito
    esc = IMG_W / MUNDO
    escala = 1.15
    w = CAMPO_W * esc * escala                  # ~1014 px (era 952)
    h = CAMPO_H * esc * escala                  # ~622 px (era 584)
    x = (IMG_W - w) / 2.0                        # ~133 px
    y = (IMG_H - h) / 2.0                        # ~49 px
    desenhar(tela, x, y, w, h, torcida=com_torcida)
    if caminho_saida:
        tela.salvar(caminho_saida)
        print("ok: %s (%dx%d) campo %.0fx%.0f em %.0f,%.0f escala %.2f" % (caminho_saida, tela.W, tela.H, w, h, x, y, escala))
    return tela


if __name__ == "__main__":
    import os
    os.makedirs("saida", exist_ok=True)
    gerar("saida/campo-goalblade.png")
