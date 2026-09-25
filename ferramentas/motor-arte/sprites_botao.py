#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — folha de BOTÕES do GoalBlade (v6-botoes, 25/09/2026).

Gera a mesma folha 144×160 que o jogo espera, mas com BOTÕES em vez de bonecos.
Cada botão tem TODAS as funções no máximo: cola, drible, velocidade e chute forte.
O anel de habilidade é o modo 'tudo' (4 ícones C/D/V/F ao redor).

Uso: python3 sprites_botao.py  -> saida/jogadores.png + jogadores.json
Depois copiar para projetos/02-goalblade/jogo/arte/
"""
import json, os, sys
from motor_rb import Tela, cor
from pintor_botao import desenhar_botao
from pintor import KitTopo, Identidade

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida")
U = 2.02
QUADRO_W, QUADRO_H = 64, 72
ANGLES = list(range(0, 360, 45))
POSES = ["parado", "c0", "c1", "c2", "c3", "chute", "dividida", "comemora"]

PESSOAS = []
for i in range(5):
    PESSOAS.append({"kit": KitTopo(camisa="e23e37", calcao="fefefe", meia="d93a33", numero=i+1,
                                   listras="fefefe" if i%2==0 else None,
                                   identidade=Identidade(i, capitao=(i==0)))})
for i in range(5):
    PESSOAS.append({"kit": KitTopo(camisa="2f5fd8", calcao="111a38", meia="22336b", numero=i+1,
                                   listras="f8f8fa" if i%2==1 else None,
                                   identidade=Identidade(i+3))})
PESSOAS.append({"kit": KitTopo(camisa="ffd34d", calcao="1d2430", meia="ffd34d", numero=1,
                               luvas="25c0c9", cabelo_tipo="raspado", identidade=Identidade(1))})
PESSOAS.append({"kit": KitTopo(camisa="7ef2a8", calcao="16202c", meia="7ef2a8", numero=1,
                               luvas="f2f4f6", cabelo_tipo="curto", identidade=Identidade(4))})

def gerar():
    os.makedirs(SAIDA, exist_ok=True)
    colunas = len(ANGLES) * len(POSES)
    t = Tela(colunas * QUADRO_W, len(PESSOAS) * QUADRO_H, luz=2)
    t.limpar((0,0,0,0))
    mapa = {"u": U, "quadro": [QUADRO_W, QUADRO_H], "angles": ANGLES, "poses": POSES, "pessoas": [], "colunas": colunas,
            "modo": "botao", "habilidades": "tudo (cola+drible+velocidade+chute)"}
    for linha, pessoa in enumerate(PESSOAS):
        info = {"linha": linha, "poses": {}}
        col = 0
        for ang in ANGLES:
            for pose in POSES:
                cx = col * QUADRO_W + QUADRO_W * 0.5
                cy = linha * QUADRO_H + QUADRO_H * 0.5
                # todos com habilidade completa; goleiro com escudo extra mas também tudo
                hab = "tudo"
                # pose muda ligeiro o brilho/se a habilidade pulsa — mas botão é redondo, então ignora pose
                desenhar_botao(t, cx, cy, U, pessoa["kit"], ang, hab)
                info["poses"]["%d_%s" % (ang, pose)] = [col * QUADRO_W, linha * QUADRO_H, QUADRO_W, QUADRO_H]
                col += 1
        mapa["pessoas"].append(info)
    caminho = os.path.join(SAIDA, "jogadores.png")
    t.salvar(caminho)
    json.dump(mapa, open(os.path.join(SAIDA, "jogadores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("folha BOTOES: %dx%d · %d quadros" % (t.W, t.H, colunas * len(PESSOAS)))
    print("ok: %s + jogadores.json (luz=6, modo botao tudo)" % caminho)
    return caminho

if __name__ == "__main__":
    gerar()
