#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — motor de desenho por código. Núcleo (v0.5, 25/09/2026).

O que é: o nosso próprio motor de arte. Ele desenha formas com **luz, sombra, contorno e
anti-serrilhado** e grava imagens PNG — sem depender de nenhum programa externo (nem
biblioteca instalada): só o Python que já existe na máquina.

Como ele funciona por dentro (a "arquitetura" dos gráficos):
  1. **Camada de desenho** (Tela): recebe as formas em coordenadas de desenho.
  2. **Super-amostragem** (`luz`): cada ponto é desenhado numa grade N×N maior e depois
     reduzido — é isso que dá o anti-serrilhado (borda lisa), como nos jogos profissionais.
  3. **Formas por distância** (SDF): círculo/elipse/linha arredondada sabem a que distância
     cada pixel está da borda, então a sombra e o contorno saem exatos (nada de "escadinha").
  4. **Composição alfa**: as formas são empilhadas por cima (over), o que permite camadas
     (fundo → sombra → corpo → roupa → número → brilho) na ordem certa.
  5. **Gravação**: PNG RGBA escrito à mão (zlib + struct), 8 bits por canal.

Cores: tuplas (r, g, b) ou (r, g, b, a) — 0 a 255.

Uso rápido:
    from motor_rb import Tela, cor
    t = Tela(320, 200, luz=3)
    t.fundo_gradiente(cor("1b2430"), cor("0d1218"))
    t.circulo(160, 100, 40, cor("d4af37"))
    t.salvar("saida/teste.png")
"""
import struct
import zlib
import math

__all__ = ["Tela", "cor", "misturar", "escurecer", "clarear"]


# --------------------------------------------------------------------------- cores
def cor(valor, alfa=255):
    """Aceita "#rrggbb", "rrggbb" ou (r,g,b[,a]) e devolve (r,g,b,a)."""
    if isinstance(valor, (tuple, list)):
        c = tuple(int(v) for v in valor)
        return (c[0], c[1], c[2], c[3] if len(c) > 3 else alfa)
    v = valor.lstrip("#")
    if len(v) == 3:
        v = "".join(ch * 2 for ch in v)
    return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), alfa)


def misturar(a, b, t):
    """Mistura duas cores: t=0 devolve a, t=1 devolve b."""
    a, b = cor(a), cor(b)
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t), int(a[3] + (b[3] - a[3]) * t))


def escurecer(c, quanto=0.28):
    return misturar(c, (0, 0, 0, cor(c)[3]), quanto)


def clarear(c, quanto=0.28):
    return misturar(c, (255, 255, 255, cor(c)[3]), quanto)



# --------------------------------------------------------------------------- fonte 5×7
# Letras e números desenhados por código (5 colunas × 7 linhas). É o que permite escrever
# TÍTULOS nas imagens (capas, cartazes) sem depender de arquivo de fonte externo.
FONTE = {
    "A": "01110100011000111111100011000110001",
    "B": "11110100011111010001100011000111110",
    "C": "01110100011000010000100001000101110",
    "D": "11110100011000110001100011000111110",
    "E": "11111100001000011110100001000011111",
    "F": "11111100001000011110100001000010000",
    "G": "01110100011000010111100011000101111",
    "H": "10001100011111110001100011000110001",
    "I": "11111001000010000100001000010011111",
    "J": "00111000100001000010000101001001100",
    "K": "10001100101110010010100011000110001",
    "L": "10000100001000010000100001000011111",
    "M": "10001110111010110101100011000110001",
    "N": "10001110011010110011100011000110001",
    "O": "01110100011000110001100011000101110",
    "P": "11110100011000111110100001000010000",
    "Q": "01110100011000110001101011001001101",
    "R": "11110100011000111110101001001010001",
    "S": "01111100001000001110000010000111110",
    "T": "11111001000010000100001000010000100",
    "U": "10001100011000110001100011000101110",
    "V": "10001100011000110001100010101000100",
    "W": "10001100011000110101101011010110001",
    "X": "10001100010101000100010101000110001",
    "Y": "10001100010101000100001000010000100",
    "Z": "11111000010001000100010001000011111",
    "0": "01110100011001110101110011000101110",
    "1": "00100011000010000100001000010001110",
    "2": "01110100010000100010001000100011111",
    "3": "11111000100010000010000110001101110",
    "4": "00010001100101010010111110001000010",
    "5": "11111100001111000001000011000101110",
    "6": "00110010001000011110100011000101110",
    "7": "11111000010001000100010000100001000",
    "8": "01110100011000101110100011000101110",
    "9": "01110100011000101111000010001001100",
    " ": "00000000000000000000000000000000000",
    ".": "00000000000000000000000000000000100",
    ":": "00000001000000000000000001000000000",
    "-": "00000000000000011111000000000000000",
    "!": "00100001000010000100001000000000010",
    "?": "01110100010000100110001000000000100",
    "X2": "00000000000010001010101010001000000",
}
ESPECIAIS = {"×": "X2"}


# --------------------------------------------------------------------------- tela
class Tela:
    def __init__(self, largura, altura, luz=3, fundo=None):
        self.W = int(largura)
        self.H = int(altura)
        self.luz = max(1, int(luz))
        self.LW = self.W * self.luz
        self.LH = self.H * self.luz
        self.buf = bytearray(self.LW * self.LH * 4)
        if fundo is not None:
            self.limpar(fundo)

    # ---------------------------------------------------------------- base
    def limpar(self, c):
        c = cor(c)
        if c[3] == 255:
            linha = bytes(c) * self.LW
            self.buf[:] = linha * self.LH
        else:
            for y in range(self.LH):
                self._linha_alfa(y, 0, self.LW, c)

    def _linha_alfa(self, y, x0, x1, c):
        """Preenche um trecho da linha aplicando alfa — usado por retângulos/gradientes."""
        buf = self.buf
        r, g, b, a = c
        if a == 255:
            base = (y * self.LW + x0) * 4
            buf[base:base + (x1 - x0) * 4] = bytes(c) * (x1 - x0)
            return
        if a == 0:
            return
        fa = a / 255.0
        ini = y * self.LW + x0
        for i in range(ini, y * self.LW + x1):
            p = i * 4
            buf[p] = int(buf[p] + (r - buf[p]) * fa)
            buf[p + 1] = int(buf[p + 1] + (g - buf[p + 1]) * fa)
            buf[p + 2] = int(buf[p + 2] + (b - buf[p + 2]) * fa)
            buf[p + 3] = max(buf[p + 3], a if buf[p + 3] < a else buf[p + 3])

    def ponto(self, x, y, c):
        """Pinta um ponto (coordenadas de desenho)."""
        c = cor(c)
        for dy in range(self.luz):
            for dx in range(self.luz):
                px, py = x * self.luz + dx, y * self.luz + dy
                if 0 <= px < self.LW and 0 <= py < self.LH:
                    p = (py * self.LW + px) * 4
                    a = c[3] / 255.0
                    b = self.buf
                    b[p] = int(b[p] + (c[0] - b[p]) * a)
                    b[p + 1] = int(b[p + 1] + (c[1] - b[p + 1]) * a)
                    b[p + 2] = int(b[p + 2] + (c[2] - b[p + 2]) * a)
                    if a > b[p + 3] / 255.0:
                        b[p + 3] = c[3]

    # ---------------------------------------------------------------- fundos
    def fundo_gradiente(self, c1, c2, horizontal=False):
        c1, c2 = cor(c1), cor(c2)
        n = self.LW if horizontal else self.LH
        for y in range(self.LH):
            if horizontal:
                self._linha_alfa(y, 0, self.LW, c1)          # base; depois as faixas verticais
                continue
            t = y / max(1, n - 1)
            self._linha_alfa(y, 0, self.LW, misturar(c1, c2, t))
        if horizontal:
            for x in range(self.LW):
                t = x / max(1, self.LW - 1)
                c = misturar(c1, c2, t)
                for y in range(self.LH):
                    p = (y * self.LW + x) * 4
                    self.buf[p:p + 4] = bytes(c)

    def ret(self, x, y, w, h, c):
        c = cor(c)
        x0, y0 = self._lim(x, y)
        x1, y1 = self._lim(x + w, y + h)
        for ly in range(y0, y1):
            self._linha_alfa(ly, x0, x1, c)

    # ---------------------------------------------------------------- formas
    def ret_arredondado(self, x, y, w, h, r, c):
        self._por_sdf(c, x - r, y - r, x + w + r, y + h + r,
                      lambda px, py: _sdf_ret(px, py, x, y, w, h, r))

    def circulo(self, cx, cy, r, c):
        self._por_sdf(c, cx - r, cy - r, cx + r, cy + r,
                      lambda px, py: math.hypot(px - cx, py - cy) - r)

    def elipse(self, cx, cy, rx, ry, c):
        self._por_sdf(c, cx - rx, cy - ry, cx + rx, cy + ry,
                      lambda px, py: _sdf_elipse(px, py, cx, cy, rx, ry))

    def anel(self, cx, cy, r, largura, c):
        meia = largura / 2.0
        self._por_sdf(c, cx - r - meia - 1, cy - r - meia - 1, cx + r + meia + 1, cy + r + meia + 1,
                      lambda px, py: abs(math.hypot(px - cx, py - cy) - r) - meia)

    def linha(self, x1, y1, x2, y2, largura, c):
        """Traço com pontas redondas (é o que dá o formato de 'cápsula' nos braços e pernas)."""
        r = largura / 2.0
        self._por_sdf(c, min(x1, x2) - r - 1, min(y1, y2) - r - 1, max(x1, x2) + r + 1, max(y1, y2) + r + 1,
                      lambda px, py: _sdf_segmento(px, py, x1, y1, x2, y2) - r)

    def poligono(self, pontos, c):
        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        c = cor(c)
        x0, y0 = self._lim(min(xs), min(ys))
        x1, y1 = self._lim(max(xs) + 1, max(ys) + 1)
        n = len(pontos)
        for ly in range(y0, y1):
            py = (ly + 0.5) / self.luz
            cortes = []
            for i in range(n):
                ax, ay = pontos[i]
                bx, by = pontos[(i + 1) % n]
                if (ay <= py < by) or (by <= py < ay):
                    cortes.append(ax + (py - ay) / (by - ay) * (bx - ax))
            if not cortes:
                continue
            cortes.sort()
            for i in range(0, len(cortes) - 1, 2):
                a, b = self._lim(cortes[i], 0)[0], self._lim(cortes[i + 1], 0)[0]
                self._linha_alfa(ly, a, b, c)

    # ---------------------------------------------------------------- números
    _DIG = {
        "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
        "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
        "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
        "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
        "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
        "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
        "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
        "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
        "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
        "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    }

    def texto_numero(self, texto, x, y, escala, c, contorno=None):
        """Escreve dígitos (número da camisa) no estilo placa: contorno por deslocamento."""
        texto = str(texto)
        largura_total = len(texto) * 6 * escala - escala
        px0 = x - largura_total / 2.0
        if contorno:
            for dx, dy in ((-escala, 0), (escala, 0), (0, -escala), (0, escala)):
                self._digitos(texto, px0 + dx, y + dy, escala, contorno)
        self._digitos(texto, px0, y, escala, c)

    def texto_numero_orientado(self, texto, cx, cy, escala, c, angulo=0.0, contorno=None):
        """Escreve o número girado junto com o jogador.

        A versão anterior deixava o número sempre paralelo à tela. Em uma vista de
        cima isso denuncia o truque: o atleta vira, mas a camisa não. Aqui cada
        quadradinho da fonte 5×7 é transformado no referencial local do corpo.
        `cx, cy` é o centro do número e `angulo` é o eixo horizontal da camisa.
        """
        texto = str(texto)
        largura = len(texto) * 6 * escala - escala
        altura = 7 * escala
        x0 = -largura / 2.0
        y0 = -altura / 2.0
        co, si = math.cos(angulo), math.sin(angulo)

        def transformar(px, py):
            return (cx + px * co - py * si, cy + px * si + py * co)

        def desenhar_cor(cor_local, dx=0.0, dy=0.0):
            px = x0
            for ch in texto:
                mapa = self._DIG.get(ch)
                if mapa is None:
                    px += 6 * escala
                    continue
                for ly, linha in enumerate(mapa):
                    for lx, v in enumerate(linha):
                        if v != "1":
                            continue
                        xa = px + lx * escala + dx
                        ya = y0 + ly * escala + dy
                        pontos = [transformar(xa, ya), transformar(xa + escala, ya),
                                  transformar(xa + escala, ya + escala), transformar(xa, ya + escala)]
                        self.poligono(pontos, cor_local)
                px += 6 * escala

        if contorno is not None:
            for dx, dy in ((-escala * 0.42, 0), (escala * 0.42, 0),
                           (0, -escala * 0.42), (0, escala * 0.42)):
                desenhar_cor(contorno, dx, dy)
        desenhar_cor(c)

    def _digitos(self, texto, px, y, escala, c):
        for ch in texto:
            mapa = self._DIG.get(ch)
            if mapa is None:
                px += 6 * escala
                continue
            for ly, linha in enumerate(mapa):
                for lx, v in enumerate(linha):
                    if v == "1":
                        self.ret(px + lx * escala, y + ly * escala, escala, escala, c)
            px += 6 * escala

    # ---------------------------------------------------------------- texto
    def texto(self, txt, x, y, escala, c, contorno=None, alinhamento="esquerda", largura_extra=0):
        """Escreve texto (A-Z, 0-9 e alguns sinais) com a fonte do motor.

        `escala` = tamanho de cada ponto. `contorno` desenha o texto 1 ponto deslocado
        nas quatro direções (é o contorno "de placa", legível em qualquer fundo).
        """
        txt = str(txt).upper()
        letras = []
        for ch in txt:
            ch = ESPECIAIS.get(ch, ch)
            letras.append(ch if ch in FONTE else (" " if ch == " " else "?"))
        larg = len(letras) * 6 * escala - escala + largura_extra
        px = x
        if alinhamento == "centro":
            px = x - larg / 2.0
        elif alinhamento == "direita":
            px = x - larg
        if contorno is not None:
            for dx, dy in ((-escala, 0), (escala, 0), (0, -escala), (0, escala)):
                self._letras(letras, px + dx, y + dy, escala, contorno)
        self._letras(letras, px, y, escala, c)
        return larg

    def _letras(self, letras, px, y, escala, c):
        for ch in letras:
            mapa = FONTE.get(ch)
            if mapa:
                for ly in range(7):
                    for lx in range(5):
                        if mapa[ly * 5 + lx] == "1":
                            self.ret(px + lx * escala, y + ly * escala, escala, escala, c)
            px += 6 * escala

    def largura_texto(self, txt, escala):
        return len(str(txt)) * 6 * escala - escala

    def texto_medido(self, txt, x, y, alvo_largura, c, contorno=None, alinhamento="centro"):
        """Escreve o texto no maior tamanho que caiba em `alvo_largura` (útil para capas)."""
        for escala in range(1, 64):
            if self.largura_texto(txt, escala) > alvo_largura:
                return self.texto(txt, x, y, max(1, escala - 1), c, contorno, alinhamento)
        return self.texto(txt, x, y, 32, c, contorno, alinhamento)

    # ---------------------------------------------------------------- gravação
    def salvar(self, caminho):
        img = self._reduzir()
        linhas = bytearray()
        passo = self.W * 4
        for y in range(self.H):
            linhas.append(0)                    # filtro 0 (sem predição)
            linhas += img[y * passo:(y + 1) * passo]
        png = b"\x89PNG\r\n\x1a\n"
        png += _bloco(b"IHDR", struct.pack(">IIBBBBB", self.W, self.H, 8, 6, 0, 0, 0))
        png += _bloco(b"IDAT", zlib.compress(bytes(linhas), 9))
        png += _bloco(b"IEND", b"")
        with open(caminho, "wb") as f:
            f.write(png)
        return caminho

    def _reduzir(self):
        """Super-amostragem: cada ponto de desenho vira a média de luz×luz amostras (anti-serrilhado)."""
        if self.luz == 1:
            return bytes(self.buf)
        saida = bytearray(self.W * self.H * 4)
        n = self.luz * self.luz
        for y in range(self.H):
            for x in range(self.W):
                r = g = b = a = 0
                for dy in range(self.luz):
                    base = ((y * self.luz + dy) * self.LW + x * self.luz) * 4
                    for dx in range(self.luz):
                        p = base + dx * 4
                        r += self.buf[p]
                        g += self.buf[p + 1]
                        b += self.buf[p + 2]
                        a += self.buf[p + 3]
                p = (y * self.W + x) * 4
                saida[p] = r // n
                saida[p + 1] = g // n
                saida[p + 2] = b // n
                saida[p + 3] = a // n
        return bytes(saida)

    # ---------------------------------------------------------------- interno
    def _lim(self, x, y):
        return (max(0, min(self.LW, int(round(x * self.luz)))),
                max(0, min(self.LH, int(round(y * self.luz)))))

    def _por_sdf(self, c, x0, y0, x1, y1, sdf):
        """Desenha uma forma descrita por 'distância até a borda' (SDF).

        Pixels com distância < 0 estão dentro. Como tudo é desenhado na grade ampliada
        (`luz`), a borda sai suave depois da redução — é o anti-serrilhado do motor.
        """
        c = cor(c)
        if c[3] == 0:
            return
        ax, ay = self._lim(x0, y0)
        bx, by = self._lim(x1, y1)
        inv = 1.0 / self.luz
        for ly in range(ay, by):
            py = (ly + 0.5) * inv
            for lx in range(ax, bx):
                if sdf((lx + 0.5) * inv, py) <= 0.0:
                    p = (ly * self.LW + lx) * 4
                    a = c[3] / 255.0
                    b = self.buf
                    b[p] = int(b[p] + (c[0] - b[p]) * a)
                    b[p + 1] = int(b[p + 1] + (c[1] - b[p + 1]) * a)
                    b[p + 2] = int(b[p + 2] + (c[2] - b[p + 2]) * a)
                    if c[3] > b[p + 3]:
                        b[p + 3] = c[3]


# --------------------------------------------------------------------------- SDFs
def _sdf_ret(px, py, x, y, w, h, r):
    qx = abs(px - (x + w / 2.0)) - (w / 2.0 - r)
    qy = abs(py - (y + h / 2.0)) - (h / 2.0 - r)
    fora = math.hypot(max(qx, 0.0), max(qy, 0.0))
    dentro = min(max(qx, qy), 0.0)
    return fora + dentro - r


def _sdf_elipse(px, py, cx, cy, rx, ry):
    # aproximação estável da distância (normalizada pelo vetor de raio)
    dx = (px - cx) / rx
    dy = (py - cy) / ry
    d = math.hypot(dx, dy)
    return (d - 1.0) * min(rx, ry)


def _sdf_segmento(px, py, x1, y1, x2, y2):
    vx, vy = x2 - x1, y2 - y1
    comp = vx * vx + vy * vy
    if comp <= 1e-9:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * vx + (py - y1) * vy) / comp))
    return math.hypot(px - (x1 + t * vx), py - (y1 + t * vy))


def _bloco(tipo, dados):
    return (struct.pack(">I", len(dados)) + tipo + dados
            + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF))
