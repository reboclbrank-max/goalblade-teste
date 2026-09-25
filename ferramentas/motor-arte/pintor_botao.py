#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — pintor de BOTÕES do GOALBLADE (v1, 25/09/2026) — FUTEBOL DE BOTÃO REALISTA.

O usuário rejeitou os bonecos ("feios e tortos") e pediu botões tão realistas quanto
os bonecos deveriam ser, mas mantendo partida com habilidades.

Este pintor desenha BOTÕES de futebol de mesa vistos de cima, com material real:
acrílico/plástico injetado com brilho especular, borda cromada/chanfrada, espessura
lateral, base de feltro, sombra de contato em 3 camadas e micro-riscos. Tudo por
código (sem imagem externa), em super-amostragem luz=6.

Uso: desenhar_botao(tela, x, y, u, kit, ang=0, habilidade=None, escurecido=0.0)
Compatível com KitTopo/Identidade do motor atual — mantém camisa/calcao/meia como
cores do botão para não quebrar o pipeline do jogo (depois o jogador escolhe habilidade
e o botão ganha detalhe visual extra).
"""
import math
from motor_rb import Tela, cor, escurecer, clarear, misturar

TAU = math.tau

def _sombra_chao(tela, x, y, u, intensidade=1.0):
    tela.elipse(x + 4.2 * u, y + 5.0 * u, 11.0 * u, 5.2 * u, (4, 9, 12, int(36 * intensidade)))
    tela.elipse(x + 2.4 * u, y + 3.2 * u, 8.0 * u, 3.8 * u, (4, 8, 11, int(72 * intensidade)))
    tela.elipse(x + 0.8 * u, y + 1.4 * u, 4.6 * u, 1.9 * u, (2, 6, 9, int(120 * intensidade)))

def _volume(tela, x, y, rx, ry, base, brilho=0.22, sombra=0.18):
    c = cor(base)
    tela.elipse(x - rx * 0.20, y - ry * 0.28, rx * 0.48, ry * 0.34, clarear(c, brilho)[:3] + (82,))
    tela.elipse(x + rx * 0.16, y + ry * 0.18, rx * 0.62, ry * 0.58, escurecer(c, sombra)[:3] + (66,))

def _bandeira(tela, x, y, r, nome):
    """Preenche o disco (x,y,r) com a bandeira do país, clipado ao círculo via scanline."""
    n = nome.upper()
    for k in range(29):
        dy = -r + 2*r*k/28.0
        # half width do círculo nesta altura
        try:
            hw = math.sqrt(max(0.0, r*r - dy*dy))
        except:
            hw = 0
        if hw < 0.5:
            continue
        xl = x - hw
        xr = x + hw
        # decide cor(s) para esta linha conforme bandeira
        if n == "BRASIL":
            # fundo verde, losango amarelo, globo azul
            # verde base
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, (0, 155, 58, 255))
            # losango amarelo: |dx| + |dy|*1.6 < r*0.82
            # desenha losango como segmento central amarelo
            # calcula interseção do losango com esta scanline
            # losango: |dx|/0.82r + |dy|/0.52r <1  =>  |dx| < 0.82r*(1 - |dy|/0.52r)
            lim = 0.82*r*(1 - abs(dy)/(0.52*r)) if abs(dy) < 0.52*r else -1
            if lim > 0:
                x1 = max(xl, x - lim)
                x2 = min(xr, x + lim)
                tela.linha(x1, y+dy, x2, y+dy, r*0.085, (255, 223, 0, 255))
                # globo azul central (|dx|<0.28r e |dy|<0.28r)
                if abs(dy) < r*0.28:
                    hw2 = math.sqrt(max(0.0, (r*0.28)**2 - dy*dy))
                    x1b = max(x1, x - hw2)
                    x2b = min(x2, x + hw2)
                    tela.linha(x1b, y+dy, x2b, y+dy, r*0.085, (0, 38, 118, 255))
        elif n == "ARGENTINA":
            # 3 faixas horizontais celeste-branco-celeste
            # y -r -> -r/3 , -r/3 -> r/3 , r/3 -> r
            if dy < -r/3:
                col = (116, 172, 223, 255)
            elif dy < r/3:
                col = (255, 255, 255, 255)
            else:
                col = (116, 172, 223, 255)
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, col)
            # sol central amarelo discreto
            if abs(dy) < r*0.18 and abs(dy) > -r*0.18:
                # pequeno círculo amarelo
                if abs(dy) < r*0.14:
                    hw2 = math.sqrt(max(0.0, (r*0.14)**2 - dy*dy))
                    tela.linha(x - hw2, y+dy, x + hw2, y+dy, r*0.085, (252, 212, 77, 255))
        elif n == "FRANCA":
            # 3 faixas verticais azul-branco-vermelho
            # divide largura em 3
            w = xr - xl
            x1 = xl + w/3
            x2 = xl + 2*w/3
            tela.linha(xl, y+dy, x1, y+dy, r*0.085, (0, 38, 124, 255))
            tela.linha(x1, y+dy, x2, y+dy, r*0.085, (255, 255, 255, 255))
            tela.linha(x2, y+dy, xr, y+dy, r*0.085, (206, 17, 38, 255))
        elif n == "ALEMANHA":
            # 3 faixas horizontais preto-vermelho-amarelo
            if dy < -r/3:
                col = (0, 0, 0, 255)
            elif dy < r/3:
                col = (221, 0, 0, 255)
            else:
                col = (255, 206, 0, 255)
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, col)
        elif n == "ESPANHA":
            # vermelho-amarelo-vermelho 1-2-1
            if dy < -r*0.25 or dy > r*0.25:
                col = (170, 21, 27, 255)
            else:
                col = (241, 191, 0, 255)
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, col)
        elif n == "INGLATERRA":
            # branco com cruz vermelha
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, (255, 255, 255, 255))
            # barra horizontal vermelha (|dy| < r*0.18)
            # barra vertical vermelha será desenhada como segmento central em cada linha
            if abs(dy) < r*0.18:
                tela.linha(xl, y+dy, xr, y+dy, r*0.085, (200, 16, 46, 255))
            else:
                # para linhas fora da barra horizontal, desenha barra vertical central
                hwv = r*0.18
                x1 = max(xl, x - hwv)
                x2 = min(xr, x + hwv)
                tela.linha(x1, y+dy, x2, y+dy, r*0.085, (200, 16, 46, 255))
        elif n == "PORTUGAL":
            # verde-vermelho vertical 40-60 + escudo simplificado amarelo
            w = xr - xl
            xmid = xl + w*0.40
            if hw == 0:
                continue
            # para cada linha, decide se está na parte verde ou vermelha conforme x
            # desenha duas faixas
            tela.linha(xl, y+dy, xmid, y+dy, r*0.085, (0, 102, 0, 255))
            tela.linha(xmid, y+dy, xr, y+dy, r*0.085, (255, 0, 0, 255))
            # escudo amarelo central pequeno
            if abs(dy) < r*0.20:
                hw2 = math.sqrt(max(0.0, (r*0.18)**2 - dy*dy))
                tela.linha(x - hw2*0.3, y+dy, x + hw2*0.3, y+dy, r*0.085, (255, 215, 0, 220))
        elif n == "ITALIA":
            # verde-branco-vermelho vertical
            w = xr - xl
            x1 = xl + w/3
            x2 = xl + 2*w/3
            tela.linha(xl, y+dy, x1, y+dy, r*0.085, (0, 146, 70, 255))
            tela.linha(x1, y+dy, x2, y+dy, r*0.085, (255, 255, 255, 255))
            tela.linha(x2, y+dy, xr, y+dy, r*0.085, (206, 43, 55, 255))
        elif n == "URUGUAI":
            # branco com 4 listras celestes horizontais finas + sol
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, (255, 255, 255, 255))
            # 4 listras celestes em dy = -0.6r, -0.2r, 0.2r, 0.6r com espessura r*0.10
            for centro in (-r*0.60, -r*0.20, r*0.20, r*0.60):
                if abs(dy - centro) < r*0.07:
                    tela.linha(xl, y+dy, xr, y+dy, r*0.085, (0, 56, 168, 255))
            # sol central
            if abs(dy) < r*0.16:
                hw2 = math.sqrt(max(0.0, (r*0.14)**2 - dy*dy))
                tela.linha(x - hw2, y+dy, x + hw2, y+dy, r*0.085, (255, 215, 0, 230))
        elif n == "HOLANDA":
            # vermelho-branco-azul horizontal
            if dy < -r/3:
                col = (174, 28, 40, 255)
            elif dy < r/3:
                col = (255, 255, 255, 255)
            else:
                col = (33, 70, 139, 255)
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, col)
        elif n == "BELGICA":
            # preto-amarelo-vermelho vertical
            w = xr - xl
            x1 = xl + w/3
            x2 = xl + 2*w/3
            tela.linha(xl, y+dy, x1, y+dy, r*0.085, (0, 0, 0, 255))
            tela.linha(x1, y+dy, x2, y+dy, r*0.085, (253, 218, 36, 255))
            tela.linha(x2, y+dy, xr, y+dy, r*0.085, (239, 51, 64, 255))
        elif n == "CROACIA":
            # xadrez vermelho-branco + listra azul fina embaixo
            # xadrez 4x2
            w = xr - xl
            # determina coluna (0..3) pelo x médio, e linha pelo dy
            # simplifica: alterna a cada faixa horizontal e vertical
            # usa 4 colunas e 2 linhas (topo e base)
            # para scanline, decide padrão de 4 blocos
            col_w = w/4.0
            # linha superior (dy<0) ou inferior
            is_top = dy < 0
            for c in range(4):
                seg_x1 = xl + c*col_w
                seg_x2 = xl + (c+1)*col_w
                # xadrez: (c + (0 if is_top else 1)) %2
                is_red = (c % 2 == 0) if is_top else (c % 2 == 1)
                col = (255, 0, 0, 255) if is_red else (255, 255, 255, 255)
                tela.linha(seg_x1, y+dy, seg_x2, y+dy, r*0.085, col)
            # faixa azul fina na base (simula borda)
            if dy > r*0.65:
                tela.linha(xl, y+dy, xr, y+dy, r*0.085, (23, 65, 143, 180))
        elif n == "MEXICO":
            # verde-branco-vermelho vertical + águia marrom central
            w = xr - xl
            x1 = xl + w/3
            x2 = xl + 2*w/3
            tela.linha(xl, y+dy, x1, y+dy, r*0.085, (0, 104, 71, 255))
            tela.linha(x1, y+dy, x2, y+dy, r*0.085, (255, 255, 255, 255))
            tela.linha(x2, y+dy, xr, y+dy, r*0.085, (206, 17, 38, 255))
            if abs(dy) < r*0.18:
                hw2 = math.sqrt(max(0.0, (r*0.12)**2 - dy*dy))
                tela.linha(x - hw2, y+dy, x + hw2, y+dy, r*0.085, (120, 70, 20, 230))
        elif n == "USA":
            # 7 listras vermelho/branco + cantão azul com estrelas
            # listras horizontais
            stripe = (2*r)/13.0
            idx = int((dy + r)/stripe)
            col = (179, 25, 66, 255) if idx % 2 == 0 else (255, 255, 255, 255)
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, col)
            # cantão azul no topo esquerdo (x < -r*0.35 e y < -r*0.35) — aprox retangular
            if dy < -r*0.45 and xl < x - r*0.35:
                # dentro do cantão, sobrescreve com azul
                cantao_x1 = xl
                cantao_x2 = x - r*0.10
                if cantao_x1 < cantao_x2:
                    tela.linha(cantao_x1, y+dy, cantao_x2, y+dy, r*0.085, (60, 59, 106, 255))
                    # estrelinhas brancas simplificadas como pontinhos
                    if int(abs(dy*10)) % 3 == 0:
                        tela.linha(cantao_x1 + (cantao_x2-cantao_x1)*0.5, y+dy, cantao_x1 + (cantao_x2-cantao_x1)*0.5 + 1, y+dy, r*0.085, (255,255,255,180))
        elif n == "JAPAO":
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, (255, 255, 255, 255))
            if abs(dy) < r*0.33:
                hw2 = math.sqrt(max(0.0, (r*0.30)**2 - dy*dy))
                tela.linha(x - hw2, y+dy, x + hw2, y+dy, r*0.085, (188, 0, 45, 255))
        elif n == "SENEGAL":
            # verde-amarelo-vermelho vertical + estrela verde
            w = xr - xl
            x1 = xl + w/3
            x2 = xl + 2*w/3
            tela.linha(xl, y+dy, x1, y+dy, r*0.085, (0, 133, 63, 255))
            tela.linha(x1, y+dy, x2, y+dy, r*0.085, (253, 239, 66, 255))
            tela.linha(x2, y+dy, xr, y+dy, r*0.085, (227, 27, 35, 255))
            if abs(dy) < r*0.16:
                hw2 = math.sqrt(max(0.0, (r*0.12)**2 - dy*dy))
                tela.linha(x - hw2, y+dy, x + hw2, y+dy, r*0.085, (0, 133, 63, 240))
        else:
            tela.linha(xl, y+dy, xr, y+dy, r*0.085, (200, 200, 200, 255))

def desenhar_botao(tela, x, y, u, kit, ang=0.0, habilidade=None, escurecido=0.0, bandeira=None):
    """Desenha um botão de futebol de mesa ultra-realista visto de cima.
    Se bandeira for passado (ex: 'BRASIL'), o topo vira a bandeira da seleção.
    Caso contrário usa kit.camisa como cor sólida.
    """
    # raio do botão em unidades U — grande o suficiente para ler número e textura
    r = 4.95 * u
    esp = 0.92 * u

    # sombra no gramado
    _sombra_chao(tela, x, y, u, 1.0)

    # base de feltro — um disco escuro levemente deslocado (peso)
    feltro = escurecer((28, 32, 36), 0.10 + escurecido * 0.5)
    tela.elipse(x + 0.35 * u, y + 0.85 * u, r * 1.02, r * 0.62, (14, 18, 22, 210))
    tela.elipse(x + 0.20 * u, y + 0.55 * u, r * 0.98, r * 0.58, feltro[:3] + (185,))

    # lateral/espessura — anel escuro que simula a altura do acrílico
    cor_base = cor(kit.camisa)
    if bandeira is not None:
        lateral = (28, 32, 36, 225)
    else:
        lateral = escurecer(cor_base, 0.38 + escurecido * 0.6)
    tela.elipse(x, y + 0.62 * u, r * 1.03, r * 0.58, lateral[:3] + (225,))
    # filete cromado da lateral
    tela.anel(x, y + 0.38 * u, r * 0.99, 0.38 * u, (220, 230, 238, 135))
    # sombra interna da lateral (oclusão)
    tela.elipse(x + 0.55 * u, y + 0.95 * u, r * 0.52, r * 0.32, (8, 12, 16, 85))

    # topo — disco principal de acrílico
    tela.circulo(x, y, r + 0.55, (12, 16, 22, 175))  # contorno sutil
    if bandeira is not None:
        # base branca e bandeira clipada ao círculo
        tela.circulo(x, y, r, (255, 255, 255, 255))
        _bandeira(tela, x, y, r, bandeira)
        topo = cor((245, 245, 245))
    else:
        topo = cor_base if escurecido == 0 else escurecer(cor_base, escurecido)
        tela.circulo(x, y, r, topo)
    # volume plástico: luz larga superior-esquerda + sombra inferior-direita
    _volume(tela, x, y, r * 0.98, r * 0.92, topo, brilho=0.20, sombra=0.18)
    # brilho especular curvo (reflexo de estúdio)
    tela.elipse(x - r * 0.28, y - r * 0.32, r * 0.52, r * 0.30, (255, 255, 255, 92))
    tela.elipse(x - r * 0.18, y - r * 0.22, r * 0.22, r * 0.14, (255, 255, 255, 145))
    # micro-riscos radiais muito suaves (só aparecem no zoom)
    for k in range(6):
        a = k * TAU / 6.0 + 0.35
        x1 = x + math.cos(a) * r * 0.42
        y1 = y + math.sin(a) * r * 0.42 * 0.62
        x2 = x + math.cos(a) * r * 0.82
        y2 = y + math.sin(a) * r * 0.82 * 0.62
        tela.linha(x1, y1, x2, y2, 0.10 * u, (255, 255, 255, 18))

    # borda chanfrada cromada
    tela.anel(x, y, r * 0.98, 0.52 * u, (242, 245, 250, 215))
    tela.anel(x, y, r * 0.92, 0.18 * u, (180, 188, 198, 110))
    # anel interno decorativo (onde o número assenta)
    tela.anel(x, y, r * 0.68, 0.24 * u, (255, 255, 255, 55))
    tela.anel(x, y, r * 0.66, 0.14 * u, escurecer(topo, 0.18)[:3] + (90,))

    # listras / faixas (se o Kit tiver) — como faixas de acrílico (ignora se bandeira)
    if bandeira is None and getattr(kit, 'listras', None) is not None:
        lc = cor(kit.listras) if escurecido == 0 else escurecer(cor(kit.listras), escurecido * 0.5)
        # 2 faixas verticais finas
        for sx in (-r * 0.38, r * 0.38):
            tela.elipse(x + sx, y, r * 0.18, r * 0.92, lc[:3] + (235,))
            tela.elipse(x + sx, y - r * 0.12, r * 0.10, r * 0.55, (255,255,255,70))

    # miolo central (onde vai número e distintivo) — leve rebaixo
    tela.circulo(x, y, r * 0.50, (248, 249, 252, 228))
    tela.circulo(x, y, r * 0.48, (255, 255, 255, 255))
    # sombra interna do miolo
    tela.anel(x, y, r * 0.48, 0.22 * u, (12, 16, 22, 45))

    # distintivo pequeno (time)
    if hasattr(kit, 'gola'):
        # usa cor da gola como distintivo se existir
        try:
            dg = cor(kit.gola)
            tela.circulo(x - r * 0.24, y - r * 0.18, r * 0.13, dg)
            tela.circulo(x - r * 0.24, y - r * 0.18, r * 0.08, (255,255,255, 85))
        except:
            pass
    else:
        # distintivo padrão dourado
        tela.circulo(x - r * 0.24, y - r * 0.18, r * 0.11, (242, 211, 88, 230))
        tela.circulo(x - r * 0.24, y - r * 0.18, r * 0.06, (255,255,255,90))

    # número central — grande, com contorno para leitura em campo reduzido
    num = str(getattr(kit, 'numero', 10))
    # fundo sutil atrás do número para contraste
    # escala do número: proporcional a U e ao raio
    escala = max(3, int(round(u * 0.95)))
    # desloca ligeiro para baixo (perspectiva top-down)
    nx, ny = x + 0.02 * u, y + 0.18 * u
    # o miolo é branco, então número sempre escuro com contorno claro colorido da camisa
    cor_num = (14, 16, 22, 255)
    cor_cont = (255, 255, 255, 255)
    # um pequeno contorno externo com a cor da camisa para leitura rápida
    tela.texto_numero_orientado(num, nx, ny, escala, cor_num, 0, contorno=cor_cont)
    # contorno fino na cor do time ao redor do miolo (segunda borda ajuda no campo pequeno)
    # já desenhado como anel, então só o número basta

    # seta sutil de direção (frente do botão) — só um triângulo cromado na borda
    if ang is not None:
        a = math.radians(ang)
        fx = math.sin(a); fy = math.cos(a)
        # fy invertido porque y cresce para baixo? No motor y - altura; para botão usamos fy como em tela normal
        # Usa o mesmo sistema do pintor_realista: frente y = +cos
        # Para marcar direção, desenha um pequeno trapézio na borda na direção ang
        px = x + fx * r * 0.92
        py = y + fy * r * 0.92 * 0.62
        # triângulo/seta
        tela.circulo(px, py, 0.52 * u, (242, 245, 250, 230))
        tela.circulo(px, py, 0.28 * u, escurecer(topo, 0.22)[:3] + (200,))

    # habilidade — anel externo pulsante + ícone pequeno
    if habilidade:
        # modo "tudo": anel arco-íris + 4 ícones ao redor
        if habilidade == "tudo" or habilidade == "completo":
            cols = [(255, 78, 58), (58, 168, 255), (58, 225, 138), (255, 211, 88)]
            nomes_h = ["C", "D", "V", "F"] # Cola, Drible, Velocidade, Força
            for k, hc in enumerate(cols):
                ang_h = k * TAU / 4.0 - TAU/8.0
                hx = x + math.cos(ang_h) * r * 1.18
                hy = y + math.sin(ang_h) * r * 1.18 * 0.62
                tela.circulo(hx, hy, 0.62 * u, hc + (230,))
                tela.circulo(hx, hy, 0.42 * u, (255,255,255, 235))
                tela.texto(nomes_h[k], hx, hy - 0.6, 1, (18,18,22), None, "centro")
            tela.anel(x, y, r * 1.09, 0.42 * u, (255,255,255, 110))
            tela.anel(x, y, r * 1.14, 0.18 * u, (255,255,255, 55))
        else:
            hab_cores = {
                "chute_forte": (255, 78, 58),
                "velocidade": (58, 168, 255),
                "escudo": (58, 225, 138),
                "curva": (255, 211, 88),
                "gelo": (140, 220, 255),
                "cola": (255, 158, 58),
                "drible": (180, 92, 255),
            }
            hc = hab_cores.get(habilidade, (200, 200, 255))
            # anel externo de habilidade
            tela.anel(x, y, r * 1.08, 0.38 * u, hc + (170,))
            tela.anel(x, y, r * 1.12, 0.18 * u, (255,255,255, 90))
            # pequeno brilho no anel
            hx = x - r * 0.55; hy = y - r * 0.55
            tela.circulo(hx, hy, 0.22 * u, (255,255,255, 140))
            # ícone textual mínimo (letra) dentro do anel superior
            tela.circulo(x, y - r * 1.02, 0.72 * u, hc + (230,))
            tela.circulo(x, y - r * 1.02, 0.48 * u, (255,255,255, 235))
            # letra da habilidade
            letra = habilidade[0].upper()
            tela.texto(letra, x, y - r * 1.02 - 1, 1, (18,18,22), None, "centro")

    # brilho final de topo (ponto quente)
    tela.circulo(x - r * 0.32, y - r * 0.38, r * 0.10, (255,255,255, 165))

if __name__ == "__main__":
    import os
    from motor_rb import Tela, cor
    from pintor import KitTopo, Identidade
    os.makedirs("saida", exist_ok=True)
    t = Tela(1280, 520, luz=6)
    t.fundo_gradiente(cor("3b7f43"), cor("2d6736"))
    kits = [
        KitTopo(camisa="c92f36", calcao="f3f2e8", meia="b9222f", numero=9, listras="f7eee0", identidade=Identidade(0)),
        KitTopo(camisa="285ac4", calcao="111b35", meia="244b9f", numero=10, listras="e9edf8", identidade=Identidade(1)),
        KitTopo(camisa="ffd34d", calcao="222936", meia="d3a52e", numero=1, luvas="e8f1eb", identidade=Identidade(2)),
        KitTopo(camisa="2f5fd8", calcao="111b35", meia="244b9f", numero=5, identidade=Identidade(3)),
    ]
    habs = [None, "chute_forte", "escudo", "velocidade"]
    for i, kit in enumerate(kits):
        desenhar_botao(t, 160 + i*280, 240, 4.6, kit, ang=i*35, habilidade=habs[i])
        t.texto(str(kit.numero), 160+i*280, 390, 3, (245,247,242), (11,16,22), "centro")
    t.salvar("saida/teste-botao-v1.png")
    print("ok: saida/teste-botao-v1.png")
