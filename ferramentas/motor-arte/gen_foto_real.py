#!/usr/bin/env python3
import os
from motor_rb import Tela, cor
import campo as campo_mod
from pintor_botao import desenhar_botao
from pintor import KitTopo, Identidade

W, H = 1280, 720
# NOVO TAMANHO: escala 1.08
IMG_W, IMG_H = 1280, 720
MUNDO = 900
CAMPO_W, CAMPO_H = 620, 380
esc = IMG_W / MUNDO
escala = 1.08
w = CAMPO_W * esc * escala
h = CAMPO_H * esc * escala
x = (IMG_W - w)/2
y = (IMG_H - h)/2
print(f"campo {w:.0f}x{h:.0f} em {x:.0f},{y:.0f} escala {escala}")

t = Tela(W, H, luz=3)
campo_mod.desenhar(t, x, y, w, h, torcida=True)

# Kits com bandeira – numeros variados
# Brasil kits
def kit_bra(numero, idx):
    return KitTopo(camisa="009739", calcao="002776", meia="009739", numero=numero, identidade=Identidade(idx))

def kit_arg(numero, idx):
    return KitTopo(camisa="74acdf", calcao="111a38", meia="74acdf", numero=numero, identidade=Identidade(idx+10))

u = 2.9
# posições relativas fx,fy dentro do campo
br_pos = [
    (0.07, 0.50, 1),
    (0.20, 0.32, 4),
    (0.20, 0.70, 4),
    (0.36, 0.50, 8),
    (0.485, 0.50, 10),
]
ar_pos = [
    (0.93, 0.50, 1),
    (0.80, 0.32, 4),
    (0.80, 0.70, 4),
    (0.63, 0.50, 8),
    (0.56, 0.50, 10),
]

for i,(fx,fy,num) in enumerate(br_pos):
    px = x + w*fx
    py = y + h*fy
    desenhar_botao(t, px, py, u, kit_bra(num, i), ang=0, bandeira="BRASIL")

for i,(fx,fy,num) in enumerate(ar_pos):
    px = x + w*fx
    py = y + h*fy
    desenhar_botao(t, px, py, u, kit_arg(num, i), ang=180, bandeira="ARGENTINA")

# bola no centro levemente para centro
bx = x + w*0.505
by = y + h*0.50 + 6
t.elipse(bx+3, by+6, 9, 5, (0,0,0,90))
t.circulo(bx, by, 7.5, cor("f6f8f4"))
t.circulo(bx, by, 2.8, cor("1a1c22"))
import math
for k in range(5):
    a = k*1.2566
    t.circulo(bx+math.cos(a)*4.8, by+math.sin(a)*4.8, 1.4, cor("1a1c22"))

# HUD topo – limpo, dentro da faixa da torcida (topo ficou menor com campo maior)
# deixa 28px de topo para HUD, por isso y baixo
t.texto("BRASIL 0 X 0 ARGENTINA  01:42", W/2, 14, 2, (255,255,255), (0,0,0), "centro")
t.texto("CAMPO REAL DETALHADO - GOL QUADRADO - MURETA FECHADA", W/2, 28, 1, (180,255,180), (0,0,0), "centro")

# controles pequenos canto inferior direito (igual foto anterior)
# posições bottom
def botao_controle(cx, cy, r, label, corfundo):
    t.elipse(cx+2, cy+3, r*0.9, r*0.5, (0,0,0, 80))
    t.circulo(cx, cy, r, cor(corfundo))
    t.circulo(cx - r*0.22, cy - r*0.28, r*0.32, (255,255,255, 90))
    t.texto(label, cx, cy+1, 1, (255,255,255), None, "centro")

# PASSE azul, DRIBLE roxo, VELOC amarelo, CHUTE vermelho
botao_controle(W- 108, H-38, 32, "PASSE", "2f5fd8")
botao_controle(W- 108, H-92, 28, "DRIBLE", "7b3fe8")
botao_controle(W- 42, H-78, 26, "VELOC", "d9b42f")
botao_controle(W- 42, H-28, 34, "CHUTE", "d93a3a")

out = os.path.join(os.path.dirname(__file__), "saida", "foto-jogo-campo-real.png")
t.salvar(out)
print(f"ok: {out} ({t.W}x{t.H})")

out2 = "/home/user/base/projetos/02-goalblade/estudos/foto-jogo-campo-real.png"
t.salvar(out2)
print(f"ok copia: {out2}")
