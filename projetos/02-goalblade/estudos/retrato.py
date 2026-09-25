#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retrato do GoalBlade — desenha UM QUADRO do jogo para conferir o visual antes de portar
para o Godot. A geometria é a mesma que o jogo vai usar (campo 620x380, câmera de cima
mostrando o campo inteiro), então este arquivo funciona como "spec" do visual.

Uso: python3 retrato.py  ->  gera retrato.png
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720
FW, FH = 620.0, 380.0          # campo (unidades de jogo)
ZOOM = 1.72                    # câmera de cima: campo inteiro (gol na esquerda/direita)
S = ZOOM

def fs(x, y):
    return ((x - FW / 2.0) * ZOOM + W / 2.0, (y - FH / 2.0) * ZOOM + H / 2.0)

def rect(x, y, w, h):
    a = fs(x, y); b = fs(x + w, y + h)
    return [a[0], a[1], b[0], b[1]]

# ---------------------------------------------------------------- cores
GRAMA1 = (58, 124, 63)
GRAMA2 = (49, 111, 55)
GRAMA_BORDA = (34, 78, 39)
APRON = (26, 58, 31)
LINHA = (255, 255, 255, 220)
LINHA_SOMBRA = (18, 40, 22, 90)
CAMISA = [(226, 62, 55), (48, 92, 214)]
CAMISA_ESC = [(176, 42, 38), (34, 66, 168)]
CALCAO = [(238, 240, 244), (20, 30, 66)]
MEIA = [(238, 240, 244), (28, 42, 84)]
PELE = (232, 185, 142)
CABELO = (44, 30, 22)
BOTA = (26, 26, 30)

fonte_num = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(9 * ZOOM * 1.85 * 0.62))
fonte_hud = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
fonte_hud2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
fonte_botao = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)

def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

# ---------------------------------------------------------------- campo
def desenhar_campo(img):
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, H], fill=(18, 34, 22))
    # entorno de grama (fora das linhas)
    d.rectangle(rect(-70, -60, FW + 140, FH + 120), fill=(38, 84, 44))
    # arquibancadas (topo e base): degraus escuros com torcida
    rnd = random.Random(11)
    for topo in (True, False):
        y0 = max(0.0, fs(0, -44)[1]) if topo else min(float(H), fs(0, FH + 4)[1])
        y1 = fs(0, -6)[1] if topo else min(float(H), fs(0, FH + 46)[1])
        d.rectangle([0, y0, W, y1], fill=(26, 30, 38))
        for linha in range(3):
            yy = y0 + (y1 - y0) * (linha + 0.5) / 4.0
            for _ in range(190):
                xx = rnd.uniform(0, W)
                cor = rnd.choice([(214, 96, 84), (86, 122, 198), (228, 216, 192), (86, 138, 100), (196, 172, 128), (60, 66, 82)])
                r = 3.6
                d.ellipse([xx - r, yy - r * 0.8, xx + r, yy + r * 0.8], fill=cor + (200,))
        d.rectangle([0, y0, W, y0 + 5], fill=(16, 20, 26))
        d.rectangle([0, y1 - 5, W, y1], fill=(16, 20, 26))
    # cerca em volta do campo
    for (a, b) in [((-8, -8), (FW + 8, -8)), ((-8, FH + 8), (FW + 8, FH + 8)),
                   ((-8, -8), (-8, FH + 8)), ((FW + 8, -8), (FW + 8, FH + 8))]:
        d.line([*fs(*a), *fs(*b)], fill=(30, 44, 34, 220), width=3)
    for k in range(0, 27):
        t = k / 26.0
        # postes da cerca (laterais e fundos), como marcas curtas
        for (px_, py_) in [(-8, -8 + t * (FH + 16)), (FW + 8, -8 + t * (FH + 16)),
                           (-8 + t * (FW + 16), -8), (-8 + t * (FW + 16), FH + 8)]:
            p2 = fs(px_, py_)
            d.line([p2[0], p2[1] - 6, p2[0], p2[1] + 1], fill=(58, 80, 62, 230), width=2)
    # grama com listras de corte
    faixa = FW / 10.0
    for i in range(10):
        cor = GRAMA2 if i % 2 else GRAMA1
        d.rectangle(rect(i * faixa, 0, faixa, FH), fill=cor)
    # textura (fios de grama) determinística
    rnd = random.Random(7)
    for _ in range(2600):
        x = rnd.uniform(0, FW); y = rnd.uniform(0, FH)
        px, py = fs(x, y)
        tom = (0, 0, 0, 16) if rnd.random() < 0.5 else (255, 255, 255, 12)
        d.line([px, py, px + rnd.choice([-1.4, 1.4]), py - 2.0], fill=tom, width=1)
    # sombra suave nas bordas do campo (profundidade)
    d.rectangle(rect(0, 0, FW, FH), outline=(0, 0, 0, 40), width=3)

    def linha(p1, p2, largura=2.0*S):
        d.line([fs(*p1)[0] + 1.2, fs(*p1)[1] + 1.2, fs(*p2)[0] + 1.2, fs(*p2)[1] + 1.2], fill=LINHA_SOMBRA, width=int(largura))
        d.line([*fs(*p1), *fs(*p2)], fill=LINHA, width=int(largura))

    def circulo(c, r, largura=2.0*S):
        b = rect(c[0]-r, c[1]-r, r*2, r*2)
        d.ellipse([b[0]+1.2, b[1]+1.2, b[2]+1.2, b[3]+1.2], outline=LINHA_SOMBRA, width=int(largura))
        d.ellipse([b[0], b[1], b[2], b[3]], outline=LINHA, width=int(largura))

    # contorno, meio, círculo e marca central
    linha((0, 0), (FW, 0)); linha((0, FH), (FW, FH))
    linha((0, 0), (0, FH)); linha((FW, 0), (FW, FH))
    linha((FW/2, 0), (FW/2, FH))
    circulo((FW/2, FH/2), FW*0.085)
    d.ellipse(rect(FW/2 - 1.4, FH/2 - 1.4, 2.8, 2.8), fill=LINHA)
    # áreas
    AW, AH = FW*0.20, FH*0.62
    SW, SH = AW*0.42, FH*0.30
    for lado in (0, 1):
        x0 = 0 if lado == 0 else FW - AW
        d.rectangle(rect(x0, FH/2 - AH/2, AW, AH), outline=LINHA_SOMBRA, width=int(2.6*S))
        d.rectangle(rect(x0 - 1.2, FH/2 - AH/2 - 1.2, AW, AH), outline=LINHA, width=int(2.6*S))
        x0s = 0 if lado == 0 else FW - SW
        d.rectangle(rect(x0s, FH/2 - SH/2, SW, SH), outline=LINHA_SOMBRA, width=int(2.6*S))
        d.rectangle(rect(x0s - 1.2, FH/2 - SH/2 - 1.2, SW, SH), outline=LINHA, width=int(2.6*S))
        marca = AW*0.72 if lado == 0 else FW - AW*0.72
        d.ellipse(rect(marca-1.6, FH/2-1.6, 3.2, 3.2), fill=LINHA)
    # arcos de canto
    rc = FW*0.018
    for (cx, cy), a0, a1 in [((0,0),0,90), ((FW,0),90,180), ((0,FH),270,360), ((FW,FH),180,270)]:
        px, py = fs(cx, cy)
        d.arc([px - rc*S, py - rc*S, px + rc*S, py + rc*S], a0, a1, fill=LINHA, width=int(2.4*S))
    return d

def desenhar_gols(d, sombras):
    gh = FH*0.22; depth = FW*0.028
    for lado in (0, 1):
        x = 0.0 if lado == 0 else FW
        sinal = -1 if lado == 0 else 1
        topo = FH/2 - gh/2
        # área do gol mais escura
        d.rectangle(rect(min(x, x+sinal*depth), topo, depth, gh), fill=(12, 30, 16, 110))
        # rede
        for i in range(1, 9):
            yy = topo + i*gh/9
            d.line([*fs(x, yy), *fs(x + sinal*depth, yy)], fill=(255,255,255,70), width=1)
        for j in range(1, 4):
            xx = x + sinal*depth*j/4
            d.line([*fs(xx, topo), *fs(xx, topo+gh)], fill=(255,255,255,70), width=1)
        # traves: moldura branca e grossa, com sombra projetada
        forma = rect(min(x, x+sinal*depth), topo, depth, gh)
        d.rectangle([forma[0]+3, forma[1]+4, forma[2]+3, forma[3]+4], outline=(0, 0, 0, 90), width=max(3, int(2.4*S)))
        d.rectangle(forma, outline=(250, 252, 250), width=max(3, int(2.4*S)))
        for i in range(1, 6):
            yy = topo + i*gh/6
            p1 = fs(x + sinal*depth, yy + 1.4); p2 = fs(x, yy + 1.4)
            d.line([p1[0]+2, p1[1]+3, p2[0]+2, p2[1]+3], fill=(0, 0, 0, 70), width=1)
            d.line([*fs(x + sinal*depth, yy), *fs(x, yy)], fill=(255, 255, 255, 120), width=2)

def desenhar_bandeirinhas(d, sombras):
    for (cx, cy) in [(0,0),(FW,0),(0,FH),(FW,FH)]:
        px, py = fs(cx, cy)
        alt = FH*0.05*S
        d.line([px, py, px, py-alt], fill=(240,240,240), width=2)
        lado = 1 if cx == 0 else -1
        d.polygon([(px, py-alt), (px + lado*9, py-alt*0.75), (px, py-alt*0.45)], fill=(255, 214, 92))
        sombras.append(("bandeira", (px, py)))

# ---------------------------------------------------------------- sombras
def desenhar_sombras(sombras):
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(camada, "RGBA")
    for tipo, dados in sombras:
        if tipo == "jogador":
            px, py = dados
            ds.ellipse([px - 8, py - 2, px + 16, py + 12], fill=(0, 0, 0, 150))
        elif tipo == "bola":
            px, py = dados
            ds.ellipse([px - 4.5, py - 1.5, px + 6.5, py + 4.5], fill=(0, 0, 0, 110))
        elif tipo == "bandeira":
            px, py = dados
            ds.line([px, py, px + 8, py + 4], fill=(0, 0, 0, 90), width=3)
        elif tipo == "trave":
            x0, x1, topo, gh = dados
            a = fs(min(x0, x1), topo); b = fs(max(x0, x1), topo + gh)
            ds.rectangle([min(a[0], b[0]) + 3, a[1] + 4, max(a[0], b[0]) + 3, b[1] + 4],
                         outline=(0, 0, 0, 80), width=int(2*S))
    camada = camada.filter(ImageFilter.GaussianBlur(3.2))
    return camada

# ---------------------------------------------------------------- bonecos
PESSOA = 1.85                 # bonecos desenhados maiores que o real (leitura na tela)

def desenhar_jogador(d, time, numero, x, y, dirx, passo):
    """Boneco de pé, visto de cima: sombra, pernas, calção, camisa com número, braços, cabeça."""
    cam = CAMISA[time]; cam_esc = CAMISA_ESC[time]; cal = CALCAO[time]; meia = MEIA[time]
    px, py = fs(x, y)
    if dirx < 0:
        espelho = True
    else:
        espelho = False
    s = S * PESSOA

    def P(lx, ly):
        return (px + lx * s, py + ly * s)

    def corpo(box, raio, cor, contorno=True):
        bx = [P(box[0], box[1])[0], P(box[0], box[1])[1], P(box[2], box[3])[0], P(box[2], box[3])[1]]
        if contorno:
            rr(d, [bx[0]-1.3, bx[1]-1.3, bx[2]+1.3, bx[3]+1.3], int(max(1, raio*s)), fill=(20, 34, 22, 150))
        rr(d, bx, int(max(1, raio*s)), fill=cor + (255,))

    bal = passo * 1.6
    # pernas/socorros e chuteiras
    corpo((-4.4, -8.6 + bal, -0.7, -0.6), 1.4, meia)
    corpo((0.7, -8.6 - bal, 4.4, -0.6), 1.4, meia)
    corpo((-5.0, -1.6 + bal, -0.2, 0.9), 1.0, BOTA)
    corpo((0.2, -1.6 - bal, 5.0, 0.9), 1.0, BOTA)
    # calção
    corpo((-5.6, -15.2, 5.6, -7.6), 2.0, cal)
    # tronco (camisa) + gola
    corpo((-6.6, -24.4, 6.6, -14.4), 2.6, cam)
    d.rectangle([*P(-6.6, -24.4), *P(6.6, -22.4)], fill=cam_esc + (255,))
    # braços
    corpo((-9.6, -23.2, -6.4, -17.4), 1.4, cam)
    corpo((6.4, -23.2, 9.6, -17.4), 1.4, cam)
    corpo((-9.9, -18.2, -6.7, -13.6), 1.3, PELE)
    corpo((6.7, -18.2, 9.9, -13.6), 1.3, PELE)
    # número
    nx, ny = P(0, -19.2)
    d.text((nx, ny), str(numero), font=fonte_num, fill=(255, 255, 255, 235), anchor="mm")
    # cabeça e cabelo
    cxa, cya = P(0.2, -28.0)
    d.ellipse([cxa - 4.6*s, cya - 4.6*s, cxa + 4.6*s, cya + 4.6*s], fill=(20, 34, 22, 150))
    d.ellipse([cxa - 4.4*s, cya - 4.4*s, cxa + 4.4*s, cya + 4.4*s], fill=PELE + (255,))
    d.ellipse([cxa - 4.6*s, cya - 5.6*s, cxa + 4.6*s, cya + 1.2*s], fill=CABELO + (255,))
    # braço/corpo indicando a direção (leve inclinação para o lado que corre)
    return

# ---------------------------------------------------------------- bola
def desenhar_bola(d, x, y):
    px, py = fs(x, y)
    r = 3.4 * S * PESSOA
    d.ellipse([px-r, py-r, px+r, py+r], fill=(255, 255, 255, 255), outline=(30, 40, 30, 180), width=1)
    d.ellipse([px-r*0.35, py-r*0.35, px+r*0.35, py+r*0.35], fill=(28, 34, 28, 255))
    for i in range(5):
        a = i * 2*math.pi/5
        cx, cy = px + math.cos(a)*r*0.62, py + math.sin(a)*r*0.62
        d.ellipse([cx-r*0.20, cy-r*0.20, cx+r*0.20, cy+r*0.20], fill=(28, 34, 28, 230))

# ---------------------------------------------------------------- HUD
def desenhar_hud(img, pts=(2, 1), relogio=137):
    d = ImageDraw.Draw(img, "RGBA")
    largura, altura = 760, 62
    x0, y0 = (W - largura)//2, 10
    rr(d, [x0+3, y0+4, x0+largura+3, y0+altura+4], 16, fill=(0, 0, 0, 70))
    rr(d, [x0, y0, x0+largura, y0+altura], 16, fill=(16, 22, 28, 225), outline=(255, 255, 255, 40), width=2)
    # times (chips) + números + relógio
    rr(d, [x0+18, y0+16, x0+68, y0+46], 8, fill=CAMISA[0] + (255,), outline=(255,255,255,120), width=2)
    rr(d, [x0+largura-68, y0+16, x0+largura-18, y0+46], 8, fill=CAMISA[1] + (255,), outline=(255,255,255,120), width=2)
    d.text((x0+150, y0+altura//2), str(pts[0]), font=fonte_hud, fill=(255, 255, 255), anchor="mm")
    # relógio: anel que esvazia + tempo em números
    d.text((x0+largura-150, y0+altura//2), str(pts[1]), font=fonte_hud, fill=(255, 255, 255), anchor="mm")
    cx, cy = x0+largura//2, y0+altura//2
    d.ellipse([cx-24, cy-24, cx+24, cy+24], fill=(30, 38, 44), outline=(255, 255, 255, 60), width=2)
    d.arc([cx-24, cy-24, cx+24, cy+24], -90, -90 + 360 * (relogio / 180.0), fill=(120, 220, 140), width=5)
    m, sg = divmod(relogio, 60)
    d.text((cx, cy+1), "%d:%02d" % (m, sg), font=fonte_hud2, fill=(240, 246, 240), anchor="mm")
    # pausa (alto à direita)
    rr(d, [W-96, 14, W-40, 62], 12, fill=(16, 22, 28, 210), outline=(255,255,255,50), width=2)
    d.rectangle([W-80, 26, W-70, 50], fill=(240, 244, 240)); d.rectangle([W-62, 26, W-52, 50], fill=(240, 244, 240))
    return d

def desenhar_controles(img):
    d = ImageDraw.Draw(img, "RGBA")
    # direcional (esquerda)
    cx, cy, r = 150, 580, 92
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 255, 255, 22), outline=(255, 255, 255, 55), width=3)
    d.ellipse([cx-34, cy-34, cx+34, cy+34], fill=(255, 255, 255, 55), outline=(255, 255, 255, 90), width=2)
    for dx, dy in [(-58, 0), (58, 0), (0, -58), (0, 58)]:
        d.polygon([(cx+dx-7, cy+dy), (cx+dx+7, cy+dy), (cx+dx, cy+dy-9 if dy == 0 else cy+dy+9)] if dy == 0 else
                  [(cx+dx, cy+dy-7), (cx+dx, cy+dy+7), (cx+dx+9, cy+dy)] if dx == 0 else [], fill=(255, 255, 255, 120))
    # CHUTE (vermelho grande) e PASSE (azul)
    for (bx, by, raio, cor, texto) in [(1150, 600, 78, (214, 62, 52), "CHUTE"), (975, 640, 62, (56, 104, 220), "PASSE")]:
        d.ellipse([bx-raio+4, by-raio+5, bx+raio+4, by+raio+5], fill=(0, 0, 0, 90))
        d.ellipse([bx-raio, by-raio, bx+raio, by+raio], fill=cor + (235,), outline=(255, 255, 255, 130), width=3)
        d.text((bx, by), texto, font=fonte_botao, fill=(255, 255, 255), anchor="mm")
    return d

# ---------------------------------------------------------------- montagem
def retrato():
    img = Image.new("RGB", (W, H), APRON)
    d = desenhar_campo(img)
    sombras = []
    desenhar_gols(d, sombras)
    desenhar_bandeirinhas(d, sombras)

    # formação 2-1-1 dos dois times (mesma do jogo)
    form = [(0.06, 0.50, 1), (0.26, 0.32, 2), (0.26, 0.68, 3), (0.48, 0.50, 4), (0.68, 0.50, 9)]
    jogadores = []
    for i, (fx, fy, num) in enumerate(form):
        jogadores.append((0, num, fx*FW, fy*FH, 1, 0.0))
    for i, (fx, fy, num) in enumerate(form):
        jogadores.append((1, num, FW - fx*FW, fy*FH, -1, 0.4))
    for (t, num, x, y, dirx, passo) in jogadores:
        sombras.append(("jogador", fs(x, y + 1.0)))
    bx, by = 300.0, 240.0     # bola perto do nosso meia
    sombras.append(("bola", fs(bx + 1.5, by + 2.0)))
    sombras.append(("jogador", fs(bx - 6, by + 9)))

    img = Image.alpha_composite(img.convert("RGBA"), desenhar_sombras(sombras)).convert("RGB")
    # luz vinda de cima + vinheta nas bordas (dá volume e tira o "chapado")
    luz = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(luz, "RGBA")
    for i in range(H):
        a = int(14 * (1 - i / H))
        dl.line([0, i, W, i], fill=(255, 250, 220, a))
    vin = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(vin, "RGBA")
    dv.rectangle([0, 0, W, H], outline=(0, 0, 0, 0), width=0)
    for k in range(40):
        dv.rectangle([k, k, W - k, H - k], outline=(0, 0, 0, int(70 * (k / 40.0) ** 2)), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), luz)
    img = Image.alpha_composite(img, vin).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    for (t, num, x, y, dirx, passo) in jogadores:
        desenhar_jogador(d, t, num, x, y, dirx, passo)
    desenhar_bola(d, bx, by)
    desenhar_hud(img)
    desenhar_controles(img)
    img.save("retrato.png")
    print("retrato.png salvo", img.size)

if __name__ == "__main__":
    retrato()
