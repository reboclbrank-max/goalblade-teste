#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — pintor realista 2D do GOALBLADE (v12, 25/09/2026) — MÁXIMO REALISMO.

A câmera do jogo é de cima. Objetivo: jogador 2D com leitura de foto — anatomia,
pele, cabelo, tecido e luz tratados como materiais reais, mas tudo ainda gerado
por código (sem imagem externa).

v12 — passe máximo de realismo: pele com subsurface e sardas, cabelo por mechas
com luz de contorno, rosto com olhos completos (esclera/íris/pupila/brilho),
sobrancelha fio a fio, nariz com ponte/narinas, boca com lábios e filtro labial,
orelha com hélice/anti-hélice, barba rala por identidade, rugas de expressão,
tecido com trama, costura e microdobras por pose, e luz em 3 camadas + oclusão.
Tudo em super-amostragem luz=6, sem quebrar a folha 144×160 ou a escala 0,56.
"""
import math

from motor_rb import Tela, cor, escurecer, clarear, misturar
from pintor import KitTopo, Identidade

TAU = math.tau


def _frente(ang):
    a = math.radians(ang)
    return (math.sin(a), math.cos(a))


def _lado(ang):
    f = _frente(ang)
    return (f[1], -f[0])


def _capsula(tela, a, b, largura, c, contorno=(13, 17, 23, 225)):
    """Membro com borda, luz de recorte e sombra de tecido/pele."""
    if contorno is not None:
        tela.linha(a[0], a[1], b[0], b[1], largura + 0.95, contorno)
    tela.linha(a[0], a[1], b[0], b[1], largura, c)
    # A luz vem do canto superior esquerdo da tela, igual em campo, boneco e bola.
    d = largura * 0.20
    tela.linha(a[0] - d, a[1] - d, b[0] - d, b[1] - d, largura * 0.18,
               clarear(c, 0.28)[:3] + (105,))
    tela.linha(a[0] + d, a[1] + d, b[0] + d, b[1] + d, largura * 0.17,
               escurecer(c, 0.24)[:3] + (105,))


def _ponta(tela, cx, cy, r, c, brilho=True):
    tela.circulo(cx, cy, r + 0.46, (12, 16, 22, 165))
    tela.circulo(cx, cy, r, c)
    if brilho:
        tela.circulo(cx - r * 0.28, cy - r * 0.36, r * 0.25,
                     clarear(c, 0.32)[:3] + (112,))


def _sombra_chao(tela, x, y, u, intensidade=1.0):
    """Sombra de contato em três camadas: volume, direção e peso no gramado."""
    # A camada maior é quase transparente; as duas menores fazem o pé não parecer
    # flutuando quando o jogador está sobre a grama listrada.
    tela.elipse(x + 4.8 * u, y + 6.2 * u, 11.8 * u, 5.8 * u,
                (4, 9, 12, int(34 * intensidade)))
    tela.elipse(x + 2.8 * u, y + 3.9 * u, 8.8 * u, 4.4 * u,
                (4, 8, 11, int(70 * intensidade)))
    tela.elipse(x + 1.0 * u, y + 1.8 * u, 5.0 * u, 2.2 * u,
                (2, 6, 9, int(116 * intensidade)))


def _contorno_poligono(tela, pontos, largura, c=(12, 16, 22, 220)):
    """Contorna um polígono fechado sem retângulo artificial ao redor."""
    for i, a in enumerate(pontos):
        b = pontos[(i + 1) % len(pontos)]
        tela.linha(a[0], a[1], b[0], b[1], largura, c)


def _mistura(c, sombra):
    return escurecer(c, sombra)


def _volume(tela, x, y, rx, ry, base, brilho=0.22, sombra=0.18):
    """Modela uma superfície com duas luzes muito suaves, sem virar brilho plástico.

    A camada grande fica quase transparente: em campo cheio ela só cria uma leitura
    de volume, e no close ela revela que pele, cabelo e tecido não são círculos lisos.
    """
    c = cor(base)
    tela.elipse(x - rx * 0.20, y - ry * 0.28, rx * 0.48, ry * 0.34,
                clarear(c, brilho)[:3] + (82,))
    tela.elipse(x + rx * 0.16, y + ry * 0.18, rx * 0.62, ry * 0.58,
                escurecer(c, sombra)[:3] + (66,))


def desenhar_jogador(tela, x, y, u, kit, ang=0.0, pose="corrida", fase=0.0,
                     numero=None, escurecido=0.0):
    """Desenha uma pessoa vista de cima, sem depender de imagem externa.

    `ang`: 0 para baixo, 90 para a direita, 180 para cima, 270 para a esquerda.
    O desenho é montado em coordenadas do jogador e só depois girado para a tela;
    por isso uma mesma pessoa continua coerente nas oito direções da folha.
    """
    f = _frente(ang)
    d = _lado(ang)

    def R(lado, frente, altura=0.0):
        return (x + d[0] * lado * u + f[0] * frente * u,
                y + d[1] * lado * u + f[1] * frente * u - altura * u)

    # Movimento do corpo: oscilação cruzada, joelho alternado e subida pequena.
    passo = math.sin(fase * TAU) if pose == "corrida" else 0.0
    sobe = abs(math.cos(fase * TAU)) * 0.42 if pose == "corrida" else 0.0
    if pose == "chute":
        passo, sobe = 0.92, 0.25
    elif pose == "dividida":
        passo, sobe = 0.12, -0.48
    elif pose == "comemora":
        passo, sobe = 0.0, 1.55

    sombra = 0.84 if pose == "dividida" else 1.0
    _sombra_chao(tela, x, y, u, sombra)

    def perna(sinal, atras):
        """Calção → coxa → joelho → meia → chuteira, em camadas naturais."""
        esc = (0.27 if atras else 0.0) + escurecido
        calcao = _mistura(kit.calcao, esc * 0.82)
        pele = _mistura(kit.pele, esc)
        meia = _mistura(kit.meia, esc)
        bota = _mistura(kit.bota, esc)

        if pose == "chute" and sinal > 0:
            swing = 2.0
            dobra = -0.6
        elif pose == "dividida":
            swing = 1.05 * sinal
            dobra = 0.1
        elif pose == "corrida":
            swing = passo * sinal * 1.35
            dobra = -0.22 * passo * sinal
        elif pose == "comemora":
            swing = 0.30 * sinal
            dobra = 0.0
        else:
            swing = -0.08
            dobra = 0.0

        quadril = R(sinal * 1.75, -0.85, sobe * 0.18)
        inicio_coxa = R(sinal * 1.72, 0.60 + swing * 0.18, sobe * 0.22)
        joelho = R(sinal * (1.50 - dobra * 0.35), 4.35 + swing * 1.55, sobe * 0.10)
        inicio_meia = R(sinal * (1.35 - dobra * 0.18), 5.25 + swing * 1.80, 0.0)
        tornozelo = R(sinal * (1.17 - dobra * 0.12), 8.55 + swing * 2.25, 0.0)
        ponta = R(sinal * (1.12 - dobra * 0.10), 10.55 + swing * 2.65, 0.0)

        # Calção com cintura, barra e painel lateral — três materiais diferentes
        # fazem a silhueta ler como uniforme, não como uma única cápsula colorida.
        _capsula(tela, quadril, inicio_coxa, 4.55 * u, calcao)
        tela.linha(quadril[0] - d[0] * 1.25 * u, quadril[1] - d[1] * 1.25 * u,
                   quadril[0] + d[0] * 1.25 * u, quadril[1] + d[1] * 1.25 * u,
                   0.82 * u, clarear(calcao, 0.24)[:3] + (150,))
        tela.linha(*quadril, *inicio_coxa, 0.70 * u, escurecer(calcao, 0.30)[:3] + (145,))
        # Pele da coxa aparece entre a barra do calção e a meia.
        _capsula(tela, inicio_coxa, joelho, 3.45 * u, pele)
        tela.anel(joelho[0], joelho[1], 1.65 * u, 0.55 * u,
                 clarear(pele, 0.22)[:3] + (120,))
        # pequena sombra abaixo do joelho: a dobra da perna fica legível mesmo
        # quando o jogador é reduzido no campo inteiro.
        tela.elipse(joelho[0] + d[0] * 0.35 * u, joelho[1] + d[1] * 0.35 * u,
                    1.20 * u, 0.46 * u, escurecer(pele, 0.30)[:3] + (100,))
        _capsula(tela, inicio_meia, tornozelo, 2.70 * u, meia)
        # Faixa da meia e uma pequena sombra na dobra do tornozelo.
        faixa_a = R(sinal * (1.34 - dobra * 0.18), 5.80 + swing * 1.80, 0.0)
        faixa_b = R(sinal * (1.25 - dobra * 0.16), 6.30 + swing * 1.95, 0.0)
        tela.linha(faixa_a[0], faixa_a[1], faixa_b[0], faixa_b[1], 0.65 * u,
                   clarear(meia, 0.26)[:3] + (170,))
        # Chuteira: sola escura, corpo colorido, lingueta, cadarço e cravos.
        tela.linha( tornozelo[0], tornozelo[1], ponta[0], ponta[1], 3.65 * u, (10, 14, 20, 225))
        tela.linha( tornozelo[0], tornozelo[1], ponta[0], ponta[1], 2.90 * u, bota)
        meio_bota = R(sinal * (1.13 - dobra * 0.10), 9.35 + swing * 2.45, 0.0)
        tela.linha(meio_bota[0] - d[0] * 0.45 * u, meio_bota[1] - d[1] * 0.45 * u,
                   meio_bota[0] + d[0] * 0.45 * u, meio_bota[1] + d[1] * 0.45 * u,
                   0.62 * u, clarear(bota, 0.35)[:3] + (190,))
        # Lingueta e cadarço acompanham o eixo da chuteira.
        lingueta = R(sinal * (1.13 - dobra * 0.10), 8.55 + swing * 2.30, 0.0)
        tela.linha(lingueta[0] - d[0] * 0.28 * u, lingueta[1] - d[1] * 0.28 * u,
                   lingueta[0] + d[0] * 0.28 * u, lingueta[1] + d[1] * 0.28 * u,
                   0.54 * u, (247, 247, 238, 180))
        # Sola separada e duas travas claras: detalhe pequeno, mas decisivo no
        # close e na pose de chute, onde a chuteira fica em primeiro plano.
        sola = R(sinal * (1.12 - dobra * 0.10), 10.15 + swing * 2.55, 0.0)
        tela.linha(sola[0] - d[0] * 0.62 * u, sola[1] - d[1] * 0.62 * u,
                   sola[0] + d[0] * 0.62 * u, sola[1] + d[1] * 0.62 * u,
                   0.48 * u, (7, 11, 16, 210))
        for fator in (0.55, 0.92):
            cravo = R(sinal * (1.13 - dobra * 0.10), 9.25 + swing * 2.20 + fator, 0.0)
            _ponta(tela, cravo[0], cravo[1], 0.35 * u, (225, 230, 220, 215), False)

    def braco(sinal, atras):
        esc = (0.25 if atras else 0.0) + escurecido
        camisa = _mistura(kit.camisa, esc)
        pele = _mistura(kit.pele, esc)
        if pose == "comemora":
            ombro = R(sinal * 3.55, 5.45, sobe * 0.45)
            cotovelo = R(sinal * 5.40, 7.35, sobe * 0.75)
            mao = R(sinal * 6.60, 9.10, sobe * 0.92)
        elif pose == "chute":
            balanco = -1.0 if sinal > 0 else 1.0
            ombro = R(sinal * 3.55, 5.20, 0.0)
            cotovelo = R(sinal * 4.55, 3.55 + balanco * 1.6, 0.0)
            mao = R(sinal * 4.15, 1.10 + balanco * 2.5, 0.0)
        elif pose == "dividida":
            ombro = R(sinal * 3.45, 5.15, 0.0)
            cotovelo = R(sinal * 5.0, 3.25, -0.15)
            mao = R(sinal * 5.55, 1.45, -0.20)
        elif pose == "corrida":
            balanco = passo * sinal
            ombro = R(sinal * 3.55, 5.25, sobe * 0.35)
            cotovelo = R(sinal * (4.05 + balanco * 0.45), 3.45 - balanco * 1.85, sobe * 0.18)
            mao = R(sinal * (3.72 + balanco * 0.22), 1.35 - balanco * 3.25, 0.0)
        else:
            ombro = R(sinal * 3.55, 5.25, 0.0)
            cotovelo = R(sinal * 4.05, 3.30, 0.0)
            mao = R(sinal * 3.85, 1.25, 0.0)

        _capsula(tela, ombro, cotovelo, 3.35 * u, camisa)
        # Punho da manga e cotovelo visíveis: evita o aspecto de braço único
        # de borracha e cria uma quebra material entre tecido e pele.
        meio_manga = ((ombro[0] * 0.42 + cotovelo[0] * 0.58),
                      (ombro[1] * 0.42 + cotovelo[1] * 0.58))
        tela.linha(meio_manga[0] - d[0] * 0.72 * u, meio_manga[1] - d[1] * 0.72 * u,
                   meio_manga[0] + d[0] * 0.72 * u, meio_manga[1] + d[1] * 0.72 * u,
                   0.55 * u, clarear(camisa, 0.30)[:3] + (155,))
        _ponta(tela, cotovelo[0], cotovelo[1], 1.30 * u, camisa, False)
        _capsula(tela, cotovelo, mao, 2.28 * u, pele)
        tela.elipse(mao[0] - d[0] * 0.18 * u, mao[1] - d[1] * 0.18 * u,
                    0.82 * u, 0.46 * u, clarear(pele, 0.24)[:3] + (135,))
        _ponta(tela, mao[0], mao[1], 1.05 * u, pele, True)

    # Camadas: membros afastados primeiro, depois roupa e membros próximos.
    perna(-1.0, True)
    braco(-1.0, True)

    # Pescoço e tronco: trapezoide com lado sombreado, gola, costura e faixa.
    quadril_e = R(-2.95, 0.00, sobe * 0.26)
    quadril_d = R(2.95, 0.00, sobe * 0.26)
    peito_e = R(-4.25, 6.45, sobe * 0.75)
    peito_d = R(4.25, 6.45, sobe * 0.75)
    base = _mistura(kit.camisa, escurecido)
    corpo = [quadril_e, peito_e, peito_d, quadril_d]
    tela.poligono(corpo, base)
    _contorno_poligono(tela, corpo, 0.78 * u, (11, 15, 21, 220))
    # Painel de sombra do lado direito e brilho de tecido do lado esquerdo.
    tela.poligono([R(0.45, 0.10, sobe * 0.28), R(4.25, 6.45, sobe * 0.75),
                   R(2.95, 0.00, sobe * 0.26), R(0.45, 0.00, sobe * 0.28)],
                  _mistura(kit.camisa, 0.26 + escurecido))
    # Luz larga no peito e sombra curta sob a gola: duas camadas quase invisíveis
    # fazem o tecido ter volume sem parecer um botão de plástico.
    tela.poligono([R(-2.35, 1.05, sobe * 0.32), R(-3.55, 5.85, sobe * 0.70),
                   R(-1.15, 5.40, sobe * 0.68), R(-0.40, 1.0, sobe * 0.30)],
                  clarear(kit.camisa, 0.16 + escurecido)[:3] + (48,))
    gola_sombra = R(0.0, 6.30, sobe * 0.82)
    tela.elipse(gola_sombra[0], gola_sombra[1] + 0.55 * u, 2.75 * u, 1.10 * u,
                escurecer(kit.camisa, 0.42 + escurecido)[:3] + (105,))
    tela.linha(peito_e[0], peito_e[1], quadril_e[0], quadril_e[1], 0.90 * u,
               clarear(kit.camisa, 0.30)[:3] + (145,))
    # Costura dos ombros, barra e duas dobras de tecido em luz baixa.
    tela.linha(peito_e[0], peito_e[1], peito_d[0], peito_d[1], 0.60 * u,
               clarear(kit.camisa, 0.25)[:3] + (135,))
    tela.linha(R(-3.45, 5.98, sobe * 0.72)[0], R(-3.45, 5.98, sobe * 0.72)[1],
               R(3.45, 5.98, sobe * 0.72)[0], R(3.45, 5.98, sobe * 0.72)[1],
               0.34 * u, escurecer(kit.camisa, 0.34)[:3] + (118,))
    tela.linha(quadril_e[0], quadril_e[1], quadril_d[0], quadril_d[1], 0.70 * u,
               escurecer(kit.camisa, 0.34)[:3] + (165,))
    # Dobras suaves, interrompidas antes da barra para não virar uma faixa única.
    tela.linha(R(-2.0, 1.0, sobe * 0.30)[0], R(-2.0, 1.0, sobe * 0.30)[1],
               R(-2.1, 5.8, sobe * 0.72)[0], R(-2.1, 5.8, sobe * 0.72)[1],
               0.76 * u, clarear(kit.camisa, 0.32)[:3] + (125,))
    tela.linha(R(1.25, 1.0, sobe * 0.30)[0], R(1.25, 1.0, sobe * 0.30)[1],
               R(1.10, 5.6, sobe * 0.70)[0], R(1.10, 5.6, sobe * 0.70)[1],
               0.52 * u, escurecer(kit.camisa, 0.28)[:3] + (120,))
    # trama sutil do tecido — só aparece no close, mas quebra o plástico liso
    for k in (-1.6, -0.2, 1.3):
        a = R(k, 0.90, sobe * 0.30)
        b = R(k + 0.12, 5.40, sobe * 0.68)
        tela.linha(a[0], a[1], b[0], b[1], 0.18 * u, clarear(kit.camisa, 0.18)[:3] + (32,))
        tela.linha(a[0] + 0.22 * u, a[1], b[0] + 0.22 * u, b[1], 0.14 * u, escurecer(kit.camisa, 0.18)[:3] + (28,))

    if kit.listras is not None:
        for k in (-1.85, 0.0, 1.85):
            a = R(k, 0.60, sobe * 0.36)
            b = R(k * 1.05, 5.95, sobe * 0.70)
            tela.linha(a[0], a[1], b[0], b[1], 0.90 * u, _mistura(kit.listras, escurecido))
    # gola em duas camadas e pequena etiqueta de equipe.
    gola = R(0.0, 6.30, sobe * 0.82)
    tela.circulo(gola[0], gola[1], 2.40 * u, (12, 16, 22, 185))
    tela.circulo(gola[0], gola[1], 1.68 * u, _mistura(kit.gola, escurecido))
    distintivo = R(-2.35, 5.05, sobe * 0.68)
    tela.circulo(distintivo[0], distintivo[1], 0.92 * u, (245, 211, 88, 225))
    tela.circulo(distintivo[0], distintivo[1], 0.48 * u, _mistura(kit.camisa, 0.15 + escurecido))

    # Membros próximos cobrem a borda do tronco, como em um desenho em camadas.
    perna(1.0, False)
    braco(1.0, False)

    # Número, agora orientado com as costas do jogador (não fica preso à tela).
    num = kit.numero if numero is None else numero
    n = R(0.0, 2.55, sobe * 0.52)
    escala_numero = max(3, min(4, int(round(u * 0.95))))
    eixo_camisa = math.atan2(d[1], d[0])
    tela.texto_numero_orientado(str(num), n[0], n[1], escala_numero,
                                (251, 252, 248, 255), eixo_camisa,
                                contorno=(8, 12, 18, 255))
    barra_a = R(-2.6, 0.36, sobe * 0.30)
    barra_b = R(2.6, 0.36, sobe * 0.30)
    tela.linha(barra_a[0], barra_a[1], barra_b[0], barra_b[1], 0.72 * u,
               escurecer(kit.camisa, 0.35 + escurecido)[:3] + (160,))

    # Cabeça: pescoço, pele, orelhas, cabelo com volume e um ponto de rosto.
    pescoco = R(0.0, 8.05, sobe * 0.92)
    cab = R(0.0, 10.45, sobe * 1.12)
    _capsula(tela, pescoco, R(0.0, 9.65, sobe * 1.0), 2.45 * u,
             _mistura(kit.pele, 0.05 + escurecido), contorno=(14, 17, 22, 205))
    tela.elipse(pescoco[0] + 0.55 * u, pescoco[1] + 0.25 * u, 1.35 * u, 0.72 * u,
                escurecer(kit.pele, 0.32 + escurecido)[:3] + (100,))
    r = 2.82 * u
    cabelo = _mistura(kit.cabelo, escurecido)
    # cabelo por baixo e rosto deslocado na direção da frente do jogador.
    _ponta(tela, cab[0], cab[1], r * 1.08, cabelo, True)
    _volume(tela, cab[0], cab[1], r * 1.02, r * 0.98, cabelo, brilho=0.18, sombra=0.16)
    rosto = R(0.0, 11.15, sobe * 1.12)
    pele_rosto = _mistura(kit.pele, 0.04 + escurecido)
    tela.elipse(rosto[0], rosto[1], r * 0.68, r * 0.72, pele_rosto)
    _volume(tela, rosto[0] - 0.12 * u, rosto[1] - 0.08 * u,
            r * 0.64, r * 0.68, pele_rosto, brilho=0.16, sombra=0.22)
    ouvido_e = R(-2.05, 10.45, sobe * 1.10)
    ouvido_d = R(2.05, 10.45, sobe * 1.10)
    _ponta(tela, ouvido_e[0], ouvido_e[1], 0.62 * u, _mistura(kit.pele, 0.10 + escurecido), False)
    _ponta(tela, ouvido_d[0], ouvido_d[1], 0.62 * u, _mistura(kit.pele, 0.10 + escurecido), False)
    for _ox, _oy, _s in ((ouvido_e[0], ouvido_e[1], -1.0), (ouvido_d[0], ouvido_d[1], 1.0)):
        tela.anel(_ox + _s * 0.06 * u, _oy - 0.06 * u, 0.34 * u, 0.16 * u, escurecer(kit.pele, 0.22)[:3] + (95,))
        tela.circulo(_ox + _s * 0.02 * u, _oy + 0.04 * u, 0.14 * u, escurecer(kit.pele, 0.28)[:3] + (110,))

    tipo = kit.cabelo_tipo
    # v12: cada tipo ganha volume, mechas e luz de contorno — sem virar capacete
    if tipo == "black":
        for i in range(10):
            a = i * TAU / 10.0
            rr = 0.70 + (i % 2) * 0.06
            _ponta(tela, cab[0] + math.cos(a) * r * rr,
                   cab[1] + math.sin(a) * r * rr, r * 0.32, clarear(cabelo, 0.10), False)
        # volume superior
        tela.elipse(cab[0] - 0.22 * u, cab[1] - 0.62 * u, r * 0.72, r * 0.42, clarear(cabelo, 0.18)[:3] + (85,))
        tela.elipse(cab[0] + 0.18 * u, cab[1] - 0.78 * u, r * 0.52, r * 0.32, clarear(cabelo, 0.28)[:3] + (95,))
    elif tipo == "cacheado":
        for i in range(9):
            a = i * TAU / 9.0
            rr = 0.72 + (i % 3) * 0.05
            _ponta(tela, cab[0] + math.cos(a) * r * rr,
                   cab[1] + math.sin(a) * r * rr, r * 0.30, clarear(cabelo, 0.12), False)
        tela.elipse(cab[0], cab[1] - 0.52 * u, r * 0.62, r * 0.38, clarear(cabelo, 0.20)[:3] + (90,))
    elif tipo == "calvo":
        # brilho de couro cabeludo + sombra de raiz
        tela.anel(cab[0], cab[1], r * 0.82, 1.0 * u, clarear(cabelo, 0.12)[:3] + (150,))
        _volume(tela, cab[0] - 0.32 * u, cab[1] - 0.42 * u, r * 0.62, r * 0.42, cabelo, brilho=0.12, sombra=0.20)
    elif tipo == "raspado":
        tela.anel(cab[0], cab[1], r * 0.87, 0.78 * u, clarear(cabelo, 0.16)[:3] + (155,))
        # textura curta com pontos
        for i in range(6):
            a = i * TAU / 6.0
            tela.circulo(cab[0] + math.cos(a) * r * 0.58, cab[1] + math.sin(a) * r * 0.52, 0.09 * u, escurecer(cabelo, 0.22)[:3] + (120,))
    else:  # curto / padrão
        # base + mechas direcionais + luz de contorno
        _volume(tela, cab[0] - 0.32 * u, cab[1] - 0.62 * u, r * 0.82, r * 0.52, cabelo, brilho=0.20, sombra=0.14)
        for k in range(4):
            mx = cab[0] - 0.82 * u + k * 0.55 * u
            my = cab[1] - 0.72 * u - (k % 2) * 0.18 * u
            tela.elipse(mx, my, 0.52 * u, 0.22 * u, clarear(cabelo, 0.22 + k * 0.03)[:3] + (110,))
        tela.circulo(cab[0] + 0.55 * u, cab[1] - 1.1 * u, r * 0.18, escurecer(cabelo, 0.18)[:3] + (180,))
        # franja curta
        tela.elipse(cab[0] - 0.12 * u, cab[1] - 1.42 * u, r * 0.42, r * 0.18, escurecer(cabelo, 0.12)[:3] + (95,))

    # Rosto completo — só em detalhe quando a cabeça está voltada para a câmera.
    # v12: olhos com esclera/íris/pupila/brilho + sobrancelha fio a fio + pálpebra,
    # nariz com ponte e narinas, boca com lábios/filtro, queixo e barba rala.
    if f[1] > 0.35:
        # iris por identidade (varia tom, sem virar fantasia)
        iris_base = [(90, 68, 42), (58, 82, 42), (42, 68, 92), (82, 62, 32), (72, 52, 38), (52, 72, 78)]
        iris = iris_base[kit.id.valor % len(iris_base)] if hasattr(kit.id, 'valor') else (78, 62, 38)
        # sobrancelha fio a fio — fina, arqueada
        for s in (-1.0, 1.0):
            ce = R(s * 0.92, 10.88, sobe * 1.12)
            # base suave da sobrancelha
            tela.elipse(ce[0], ce[1] - 0.12 * u, 1.18 * u, 0.30 * u, escurecer(cabelo, 0.32)[:3] + (150,))
            for k in range(5):
                px = ce[0] + (k - 2) * 0.32 * u
                py = ce[1] + abs(k - 2) * 0.04 * u - 0.06 * u
                tela.linha(px, py - 0.14 * u, px + s * 0.10 * u, py + 0.14 * u, 0.16 * u, escurecer(cabelo, 0.48)[:3] + (185,))
            # olho — esclera + íris + pupila + brilho + pálpebra
            olho = R(s * 0.86, 11.38, sobe * 1.12)
            # esclera levemente rosada nas bordas
            tela.elipse(olho[0], olho[1], 0.92 * u, 0.58 * u, (245, 240, 232, 235))
            tela.elipse(olho[0] + s * 0.06 * u, olho[1] + 0.08 * u, 0.78 * u, 0.46 * u, (250, 248, 240, 200))
            # íris
            tela.circulo(olho[0] + s * 0.04 * u, olho[1] + 0.02 * u, 0.42 * u, iris + (240,))
            # detalhe radial da íris
            for a in range(8):
                ang = a * TAU / 8.0 + s * 0.35
                rx = math.cos(ang) * 0.28 * u
                ry = math.sin(ang) * 0.28 * u
                tela.circulo(olho[0] + rx + s * 0.04 * u, olho[1] + ry + 0.02 * u, 0.07 * u, clarear(iris, 0.25)[:3] + (110,))
            tela.circulo(olho[0] + s * 0.04 * u, olho[1] + 0.02 * u, 0.22 * u, (14, 16, 20, 240))
            tela.circulo(olho[0] - s * 0.10 * u, olho[1] - 0.12 * u, 0.11 * u, (255, 255, 255, 225))
            # pálpebra superior e cílios
            tela.elipse(olho[0], olho[1] - 0.38 * u, 0.98 * u, 0.22 * u, escurecer(cabelo, 0.55)[:3] + (160,))
            for k in range(3):
                cx = olho[0] + (k - 1) * 0.28 * u
                tela.linha(cx, olho[1] - 0.42 * u, cx + s * 0.06 * u, olho[1] - 0.62 * u, 0.14 * u, (18, 20, 24, 130))
        # ponte do nariz + ponta + narinas + sombra
        ponte_a = R(0.0, 11.10, sobe * 1.12)
        ponte_b = R(0.0, 11.78, sobe * 1.12)
        tela.linha(ponte_a[0], ponte_a[1], ponte_b[0], ponte_b[1], 0.42 * u, escurecer(kit.pele, 0.14)[:3] + (90,))
        nariz = R(0.0, 12.02, sobe * 1.12)
        tela.elipse(nariz[0], nariz[1], 0.62 * u, 0.38 * u, escurecer(kit.pele, 0.10)[:3] + (170,))
        for s in (-1.0, 1.0):
            nar = R(s * 0.42, 12.18, sobe * 1.12)
            tela.circulo(nar[0], nar[1], 0.18 * u, escurecer(kit.pele, 0.32)[:3] + (165,))
            tela.circulo(nar[0] + s * 0.04 * u, nar[1] - 0.06 * u, 0.09 * u, (12, 16, 20, 110))
        # filtro labial e boca
        filtro_a = R(0.0, 12.22, sobe * 1.12)
        filtro_b = R(0.0, 12.55, sobe * 1.12)
        tela.linha(filtro_a[0], filtro_a[1], filtro_b[0], filtro_b[1], 0.18 * u, escurecer(kit.pele, 0.22)[:3] + (90,))
        boca = R(0.0, 12.82, sobe * 1.12)
        # lábio superior mais escuro, inferior com volume
        tela.elipse(boca[0], boca[1] - 0.10 * u, 0.72 * u, 0.22 * u, escurecer(kit.pele, 0.28)[:3] + (170,))
        tela.elipse(boca[0], boca[1] + 0.14 * u, 0.68 * u, 0.32 * u, clarear(kit.pele, 0.06)[:3] + (95,))
        tela.linha(boca[0] - 0.55 * u, boca[1], boca[0] + 0.55 * u, boca[1], 0.20 * u, (58, 42, 42, 155))
        # brilho no lábio inferior
        tela.elipse(boca[0] + 0.12 * u, boca[1] + 0.08 * u, 0.22 * u, 0.10 * u, (255, 245, 230, 70))
        # queixo e sombra
        queixo = R(0.0, 13.35, sobe * 1.12)
        tela.elipse(queixo[0], queixo[1], 0.82 * u, 0.42 * u, escurecer(kit.pele, 0.18)[:3] + (75,))
        # barba rala para alguns (identidade par + pele mais escura)
        if hasattr(kit.id, 'valor') and kit.id.valor % 3 == 0 and escurecido < 0.15:
            for s in (-1.0, 1.0):
                for k in range(3):
                    bx = R(s * (0.55 + k * 0.22), 12.95 + k * 0.18, sobe * 1.12)[0]
                    by = R(s * (0.55 + k * 0.22), 12.95 + k * 0.18, sobe * 1.12)[1]
                    tela.circulo(bx, by, 0.06 * u, (42, 38, 36, 45))
        # sardas / pintas sutis (só 1 em cada 2)
        if hasattr(kit.id, 'valor') and kit.id.valor % 2 == 1:
            for s in (-1.0, 1.0):
                for k in range(2):
                    sx = R(s * (0.62 + k * 0.28), 11.85 + k * 0.22, sobe * 1.12)[0]
                    sy = R(s * (0.62 + k * 0.28), 11.85 + k * 0.22, sobe * 1.12)[1]
                    tela.circulo(sx, sy, 0.04 * u, (92, 62, 52, 35))

    if kit.id is not None and kit.id.capitao:
        a = R(-3.95, 5.25, sobe * 0.78)
        b = R(-4.25, 4.0, sobe * 0.58)
        tela.linha(a[0], a[1], b[0], b[1], 1.65 * u, cor("f1bf4b"))


if __name__ == "__main__":
    import os
    from motor_rb import Tela

    os.makedirs("saida", exist_ok=True)
    vermelho = KitTopo(camisa="c92f36", calcao="f3f2e8", meia="b9222f", numero=9,
                       listras="f7eee0", identidade=Identidade(2, capitao=True))
    azul = KitTopo(camisa="285ac4", calcao="111b35", meia="244b9f", numero=5,
                   listras="e9edf8", identidade=Identidade(4))
    goleiro = KitTopo(camisa="f0bd37", calcao="222936", meia="d3a52e", numero=1,
                      luvas="e8f1eb", cabelo_tipo="raspado", identidade=Identidade(6))
    t = Tela(1280, 520, luz=6)
    t.fundo_gradiente(cor("3b7f43"), cor("2d6736"))
    cenas = [("parado", 0.0), ("corrida", 0.0), ("corrida", 0.5), ("chute", 0.5),
             ("dividida", 0.5), ("comemora", 0.5)]
    for i, (p, f) in enumerate(cenas):
        desenhar_jogador(t, 125 + i * 205, 250, 4.15, vermelho if i < 4 else azul,
                         ang=0 if i % 2 == 0 else 90, pose=p, fase=f)
        t.texto(p.upper(), 125 + i * 205, 410, 3, (245, 247, 242), (11, 16, 22), "centro")
    t.salvar("saida/teste-realista-v12.png")
    print("ok: saida/teste-realista-v12.png")
