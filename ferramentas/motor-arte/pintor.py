#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — pintor de jogador em VISÃO DE CIMA (v1.0, 24/09/2026).

Por que existe: a câmera do GoalBlade olha o campo de cima. Boneco desenhado "de pé, de frente"
(como estava) fica com cara de bonequinha e não tem nada de realista. Aqui o jogador é desenhado
como **visto de drone**: cabeça do alto, ombros, número nas costas, braços e pernas com balanço
real na direção em que corre, e sombra no chão.

O que dá o realismo:
  · **perspectiva certa** — o corpo é desenhado em volta do eixo de corrida (gira com o jogador);
  · **luz fixa no céu** (vem de cima/esquerda da tela): brilho de um lado, sombra do outro;
  · **contorno escuro** em toda peça (o jogador lê sobre o gramado em qualquer posição);
  · **anatomia de corredor**: coxa mais grossa, canela mais fina, meia até o meio da canela, chuteira;
  · **balanço cruzado**: perna direita avança junto com o braço esquerdo (é assim que se corre de verdade);
  · **sombra** elíptica deslocada + sombra das pernas;
  · **número nas costas** com contorno (lido de cima).

Uso:
    from pintor import desenhar_jogador
    desenhar_jogador(tela, x, y, u=2.6, kit=KIT_VERMELHO, ang=0, pose="corrida", fase=0.25)

`ang` em graus: 0 = correndo para BAIXO (frente da tela) · 90 = para a DIREITA ·
180 = para CIMA (fundo) · 270 = para a ESQUERDA.
"""
import math

from motor_rb import Tela, cor, escurecer, clarear

CONC = 1.0


def _rot(v, a):
    """Gira o vetor v (x, y) pelo ângulo a (graus)."""
    r = math.radians(a)
    return (v[0] * math.cos(r) - v[1] * math.sin(r), v[0] * math.sin(r) + v[1] * math.cos(r))


def _frente(ang):
    """Vetor unitário da direção em que o jogador corre (tela: y cresce para baixo)."""
    a = math.radians(ang)
    return (math.sin(a), math.cos(a))


def _lado(ang):
    f = _frente(ang)
    return (f[1], -f[0])          # perpendicular (direita do jogador)


def _peca(tela, a, b, largura, c, contorno=True, brilho=0.42):
    """Peça do corpo: contorno, corpo, brilho de um lado e sombra do outro (luz fixa no céu)."""
    if contorno:
        tela.linha(a[0], a[1], b[0], b[1], largura + 2.0, (16, 20, 28, 235))
    tela.linha(a[0], a[1], b[0], b[1], largura, c)
    d = largura * 0.26
    # luz vem de cima/esquerda da TELA (não do jogador): fica realista em qualquer direção
    tela.linha(a[0] - d, a[1] - d, b[0] - d, b[1] - d, largura * 0.34, clarear(c, brilho)[:3] + (120,))
    tela.linha(a[0] + d * 0.9, a[1] + d * 0.9, b[0] + d * 0.9, b[1] + d * 0.9, largura * 0.40,
               escurecer(c, 0.32)[:3] + (130,))


def _bola_tela(tela, cx, cy, r, c):
    tela.circulo(cx, cy, r + 0.9, (16, 20, 28, 220))
    tela.circulo(cx, cy, r, c)
    tela.circulo(cx - r * 0.30, cy - r * 0.32, r * 0.40, clarear(c, 0.45)[:3] + (110,))


# Paletas de pessoas: tom de pele, cabelo e tipo. Usadas para dar identidade a cada jogador.
PELES = ["f2c6a0", "e8b98e", "d8a273", "c98a5e", "a96b41", "8a5330", "6b3f24"]
CABELOS = ["1d1712", "2c1e16", "4a2f1c", "6b4a2a", "14100c", "3a2a1a", "b8873f", "d9c08a"]
TIPOS_CABELO = ["curto", "curto", "raspado", "black", "cacheado", "curto", "raspado", "black"]
BOTAS = ["f2f4f6", "141821", "e8d24a", "d63a2f", "2f7fd6", "1f2a1c"]
MEIAS_ALTAS = [True, False, True, False, True]


class Identidade:
    """A pessoa por trás do número: pele, cabelo, chuteira e detalhes próprios."""

    def __init__(self, indice=0, capitao=False):
        self.pele = PELES[indice % len(PELES)]
        self.cabelo = CABELOS[(indice * 3) % len(CABELOS)]
        self.cabelo_tipo = TIPOS_CABELO[(indice * 5) % len(TIPOS_CABELO)]
        self.bota = BOTAS[(indice * 2) % len(BOTAS)]
        self.meia_alta = MEIAS_ALTAS[indice % len(MEIAS_ALTAS)]
        self.capitao = capitao


class KitTopo:
    """Uniforme visto de cima. Só as cores mudam de time para time."""

    def __init__(self, camisa, calcao, meia, numero=9, pele="e8b98e", cabelo="2c1e16",
                 bota="141821", luvas=None, cabelo_tipo="curto", gola=None,
                 listras=None, identidade=None):
        self.camisa = cor(camisa)
        self.calcao = cor(calcao)
        self.meia = cor(meia)
        self.pele = cor(pele)
        self.cabelo = cor(cabelo)
        self.bota = cor(bota)
        self.luvas = cor(luvas) if luvas else None
        self.numero = numero
        self.cabelo_tipo = cabelo_tipo
        self.gola = cor(gola) if gola else escurecer(camisa, 0.35)
        self.listras = cor(listras) if listras else None
        self.id = identidade                      # Identidade (pele/cabelo/chuteira próprios)
        if identidade is not None:
            self.pele = cor(identidade.pele)
            self.cabelo = cor(identidade.cabelo)
            self.cabelo_tipo = identidade.cabelo_tipo
            self.bota = cor(identidade.bota)


def desenhar_jogador(tela, x, y, u, kit, ang=0.0, pose="corrida", fase=0.0, numero=None,
                     escurecido=0.0):
    """Desenha o jogador visto de cima (vista de drone), na direção `ang`.

    Como o corpo é montado: primeiro calculo TODOS os pontos no referencial do jogador
    (x = lado, y = para onde ele corre) e só no fim giro cada ponto para a tela. Assim o
    mesmo desenho serve para as oito direções — e o jogador nunca fica "torto".
    """
    f = _frente(ang)
    d = _lado(ang)

    def R(lado, frente, altura=0.0):
        """Ponto no referencial do jogador -> ponto na tela (altura = quanto sobe do chão)."""
        px = x + d[0] * lado * u + f[0] * frente * u
        py = y + d[1] * lado * u + f[1] * frente * u
        return (px, py - altura * u)

    # ------------------------------------------------------------------ ritmo do passo
    if pose == "corrida":
        passo = math.sin(fase * math.tau)
        sobe = abs(math.cos(fase * math.tau)) * 0.55
    elif pose == "chute":
        passo, sobe = 0.85, 0.20
    elif pose == "comemora":
        passo, sobe = 0.0, 1.9
    else:
        passo, sobe = 0.0, 0.0

    # ------------------------------------------------------------------ sombra (luz de cima)
    tela.elipse(x + 1.4 * u, y + 2.0 * u, 7.2 * u, 4.4 * u, (14, 22, 16, 84))
    tela.elipse(x + 1.0 * u, y + 1.4 * u, 4.6 * u, 2.8 * u, (14, 22, 16, 62))

    # ------------------------------------------------------------------ pernas
    def perna(sinal, perto):
        esc = 0.0 if perto else 0.26
        c_pele = escurecer(kit.pele, esc + escurecido)
        c_meia = escurecer(kit.meia, esc + escurecido)
        c_calcao = escurecer(kit.calcao, esc * 0.8 + escurecido)
        # "passo" de verdade: a perna avança e recua NO SENTIDO DA CORRIDA
        # (swing = +1 perna à frente, -1 perna atrás; o desvio pequeno mantém as pernas
        #  separadas, senão uma tapa a outra vista de cima).
        if pose == "chute" and sinal > 0:
            swing, dobra = 1.25, 6.0
        elif pose == "corrida":
            swing, dobra = passo * sinal, 14.0 + 12.0 * (1.0 - passo * sinal) * 0.5
        elif pose == "comemora":
            swing, dobra = 0.35 * sinal, 20.0
        else:
            swing, dobra = -0.12, 16.0
        # quadril -> joelho (a coxa sai do quadril e vai para trás/frente, no eixo de corrida)
        q = R(1.9 * sinal, -0.6, 0.0)
        fa = _frente(ang + 90.0 - 90.0 * swing + 9.0 * sinal)   # coxa
        fj = _frente(ang + 90.0 - 90.0 * swing + 9.0 * sinal - dobra)  # canela (atrás da coxa)
        joelho = (q[0] + fa[0] * 5.2 * u, q[1] + fa[1] * 5.2 * u)
        # joelho -> pé (canela), com meia
        pe = (joelho[0] + fj[0] * 5.4 * u, joelho[1] + fj[1] * 5.4 * u)
        meio = (pe[0] - fj[0] * 1.6 * u, pe[1] - fj[1] * 1.6 * u)   # meia desce até a chuteira
        _peca(tela, q, (joelho[0] - fj[0] * 3.0 * u, joelho[1] - fj[1] * 3.0 * u), 3.6 * u, c_calcao)
        _peca(tela, (joelho[0] - fj[0] * 2.8 * u, joelho[1] - fj[1] * 2.8 * u), joelho, 3.0 * u, c_pele)
        _peca(tela, joelho, meio, 2.6 * u, c_meia)
        # chuteira: ponta arredondada no sentido do movimento do pé
        tela.linha(pe[0], pe[1], pe[0] + fj[0] * 2.4 * u, pe[1] + fj[1] * 2.4 * u, 3.0 * u, (16, 20, 28, 230))
        tela.linha(pe[0], pe[1], pe[0] + fj[0] * 2.2 * u, pe[1] + fj[1] * 2.2 * u, 2.4 * u,
                   escurecer(kit.bota, escurecido))
        return pe

    def braco(sinal, perto):
        esc = 0.0 if perto else 0.28
        c_camisa = escurecer(kit.camisa, esc + escurecido)
        c_pele = escurecer(kit.pele, esc + escurecido)
        if pose == "comemora":
            abre = 24.0 * sinal
            ang_b = ang + abre
            o = R(3.6 * sinal, 1.4, sobe * 0.5)
        elif pose == "chute":
            ang_b = ang + 22.0 * sinal
            o = R(3.6 * sinal, 1.6, 0.0)
        elif pose == "corrida":
            ang_b = ang + 168.0 + 7.0 * sinal + 16.0 * passo * sinal   # braço para trás, balançando
            o = R(3.4 * sinal, 1.6, 0.0)
        else:
            ang_b = ang + 165.0 + 5.0 * sinal
            o = R(3.4 * sinal, 1.4, 0.0)
        fb = _frente(ang_b)
        c = (o[0] + fb[0] * 3.1 * u, o[1] + fb[1] * 3.1 * u)
        m = (c[0] + fb[0] * 2.7 * u, c[1] + fb[1] * 2.7 * u)
        _peca(tela, o, (o[0] + fb[0] * 2.4 * u, o[1] + fb[1] * 2.4 * u), 3.2 * u, c_camisa)   # manga
        _peca(tela, (o[0] + fb[0] * 2.1 * u, o[1] + fb[1] * 2.1 * u), c, 2.3 * u, c_pele)     # braço
        luva = kit.luvas if kit.luvas else c_pele
        _peca(tela, c, m, 2.2 * u, luva)
        _bola_tela(tela, m[0], m[1], 1.55 * u, luva)
        return m

    # ------------------------------------------------------------------ camadas (de trás para frente)
    perna(-1.0, False)
    braco(-1.0, False)

    # tronco: OMBROS como peça única e larga (é o que dá a leitura de pessoa vista de cima)
    quadril = R(0.0, -1.6, sobe * 0.35)
    peito = R(0.0, 6.2, sobe * 0.7)
    ombros_e = R(-4.0, 6.4, sobe)
    ombros_d = R(4.0, 6.4, sobe)
    _peca(tela, quadril, peito, 5.8 * u, escurecer(kit.camisa, escurecido))          # cintura/quadril
    _peca(tela, ombros_e, ombros_d, 5.2 * u, escurecer(kit.camisa, escurecido))      # ombros (barra)
    _peca(tela, R(0.0, 2.2, sobe * 0.55), R(0.0, 7.6, sobe), 6.6 * u,
          escurecer(kit.camisa, escurecido))                                          # peito
    # listras do uniforme (frente -> trás)
    if kit.listras is not None:
        for k in (-1, 1):
            a1 = R(k * 1.9, 0.6, sobe * 0.4)
            a2 = R(k * 2.3, 6.6, sobe * 0.9)
            tela.linha(a1[0], a1[1], a2[0], a2[1], 1.15 * u, kit.listras)
    # gola
    g = R(0.0, 7.6, sobe)
    tela.circulo(g[0], g[1], 2.5 * u, escurecer(kit.camisa, 0.34 + escurecido))
    tela.circulo(g[0], g[1], 1.6 * u, escurecer(kit.gola, escurecido))

    perna(1.0, True)
    braco(1.0, True)

    # ------------------------------------------------------------------ cabeça
    cab = R(0.0, 10.4, sobe * 1.15)
    r = 2.55 * u
    tipo = kit.cabelo_tipo
    _bola_tela(tela, cab[0], cab[1], r * 1.06, escurecer(kit.cabelo, escurecido))
    if tipo == "black":
        tela.circulo(cab[0], cab[1], r * 1.22, escurecer(kit.cabelo, escurecido))
    elif tipo == "cacheado":
        for i in range(6):
            a2 = i * math.tau / 6.0
            tela.circulo(cab[0] + math.cos(a2) * r * 0.66, cab[1] + math.sin(a2) * r * 0.66, r * 0.52,
                         clarear(kit.cabelo, 0.12))
        tela.circulo(cab[0], cab[1], r * 0.72, escurecer(kit.cabelo, escurecido))
    elif tipo == "calvo":
        _bola_tela(tela, cab[0], cab[1], r, escurecer(kit.pele, 0.08 + escurecido))
        tela.anel(cab[0], cab[1], r * 0.80, 1.3 * u, escurecer(kit.cabelo, 0.12))
    elif tipo == "raspado":
        tela.circulo(cab[0] - 0.5 * u, cab[1] - 0.6 * u, r * 0.52, clarear(kit.cabelo, 0.24)[:3] + (150,))
    else:
        tela.circulo(cab[0] - 0.7 * u, cab[1] - 0.9 * u, r * 0.60, clarear(kit.cabelo, 0.30)[:3] + (140,))
    # rosto só quando ele corre para perto da câmera (é o que a luz mostra)
    if f[1] > 0.45:
        rosto = R(0.0, 11.6, sobe * 1.15)
        tela.circulo(rosto[0], rosto[1], r * 0.66, escurecer(kit.pele, 0.05 + escurecido))
        for s2 in (-1.0, 1.0):
            ol = R(1.1 * s2, 12.1, sobe * 1.15)
            tela.circulo(ol[0], ol[1], 0.46 * u, (26, 28, 36, 230))

    # ------------------------------------------------------------------ número nas costas
    if f[1] >= -0.35:
        num = kit.numero if numero is None else numero
        costas = R(0.0, 2.2, sobe * 0.5)
        tela.texto_numero(str(num), costas[0], costas[1] - 3.2 * u, max(3, min(4, int(round(u * 0.95)))),
                          (251, 252, 248, 255), contorno=(8, 12, 18, 255))

    # braçadeira de capitão
    if kit.id is not None and kit.id.capitao:
        b1 = R(-4.0, 5.6, sobe)
        b2 = R(-4.6, 3.6, sobe * 0.9)
        tela.linha(b1[0], b1[1], b2[0], b2[1], 2.0 * u, cor("f2c14a"))


# --------------------------------------------------------------------------- testes
if __name__ == "__main__":
    from motor_rb import Tela
    import os
    os.makedirs("saida", exist_ok=True)
    VERMELHO = KitTopo(camisa="e23e37", calcao="fefefe", meia="d93a33", numero=9)
    AZUL = KitTopo(camisa="2f5fd8", calcao="111a38", meia="22336b", numero=4, pele="c98a5e",
                   cabelo="14100c", cabelo_tipo="black")
    GOL = KitTopo(camisa="ffd34d", calcao="1d2430", meia="ffd34d", numero=1, luvas="25c0c9",
                  cabelo_tipo="raspado")
    t = Tela(1180, 300, luz=3)
    t.fundo_gradiente(cor("3c8142"), cor("347238"))
    for n in range(900):
        fx = (n * 137.508) % 1180
        fy = (n * 71.17) % 300
        t.linha(fx, fy, fx + 1.3, fy - 2.0, 0.9, (255, 255, 255, 14) if n % 3 else (0, 0, 0, 12))
    x = 90
    for ang, nome in ((0, "BAIXO"), (90, "DIREITA"), (180, "CIMA"), (270, "ESQUERDA")):
        for fase in (0.0, 0.25, 0.5):
            desenhar_jogador(t, x, 150, 2.9, VERMELHO, ang, "corrida", fase)
            x += 96
        x += 14
    x = 90
    for kit, pose in ((VERMELHO, "parado"), (AZUL, "chute"), (GOL, "comemora"), (AZUL, "parado")):
        desenhar_jogador(t, x, 262, 2.9, kit, 0, pose, 0.5)
        t.texto(pose.upper(), x, 272, 2, (244, 248, 244), (16, 20, 28), "centro")
        x += 170
    t.salvar("saida/teste-visao-de-cima.png")
    print("ok: saida/teste-visao-de-cima.png")
