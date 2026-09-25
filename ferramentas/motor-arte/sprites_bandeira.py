#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — folha de BOTÕES-BANDEIRA do GoalBlade (25/09/2026) — JOGO RODANDO.

Gera a folha que o Godot realmente usa: 144x160, 8 direções x 8 poses, 12 linhas.
Time 0 (linhas 0-4) = BRASIL bandeira, Time 1 (linhas 5-9) = ARGENTINA bandeira,
Goleiros linhas 10-11 = BRASIL/ARGENTINA também (com luvas).
Todas com habilidade 'tudo' e cola máxima.

Para trocar adversário, basta trocar a lista SELECOES abaixo.
"""
import json, os
from motor_rb import Tela, cor
from pintor_botao import desenhar_botao
from pintor import KitTopo, Identidade

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida")
U = 4.55
QUADRO_W, QUADRO_H = 144, 160
ANGLES = list(range(0, 360, 45))
POSES = ["parado", "c0", "c1", "c2", "c3", "chute", "dividida", "comemora"]

# JOGO RODANDO: 5 jogadores + goleiro por time, com bandeira no botão
# Time 0 = BRASIL, Time 1 = ARGENTINA (clássico para foto)
SELECAO_A = "BRASIL"
SELECAO_B = "ARGENTINA"

PESSOAS = []
for i in range(5):
    PESSOAS.append({"kit": KitTopo(camisa="ffffff", calcao="ffffff", meia="ffffff", numero=i+1, identidade=Identidade(i, capitao=(i==0))), "bandeira": SELECAO_A})
for i in range(5):
    PESSOAS.append({"kit": KitTopo(camisa="ffffff", calcao="ffffff", meia="ffffff", numero=i+1, identidade=Identidade(i+3)), "bandeira": SELECAO_B})
# goleiros
PESSOAS.append({"kit": KitTopo(camisa="ffffff", calcao="ffffff", meia="ffffff", numero=1, luvas="f0f0f0", cabelo_tipo="raspado", identidade=Identidade(1)), "bandeira": SELECAO_A})
PESSOAS.append({"kit": KitTopo(camisa="ffffff", calcao="ffffff", meia="ffffff", numero=1, luvas="f0f0f0", cabelo_tipo="curto", identidade=Identidade(4)), "bandeira": SELECAO_B})

def gerar():
    os.makedirs(SAIDA, exist_ok=True)
    colunas = len(ANGLES) * len(POSES)
    t = Tela(colunas * QUADRO_W, len(PESSOAS) * QUADRO_H, luz=2)
    t.limpar((0,0,0,0))
    mapa = {"u": U, "quadro": [QUADRO_W, QUADRO_H], "angles": ANGLES, "poses": POSES, "pessoas": [], "colunas": colunas, "modo": "botao-bandeira", "selecoes": [SELECAO_A, SELECAO_B]}
    for linha, pessoa in enumerate(PESSOAS):
        info = {"linha": linha, "poses": {}}
        col = 0
        for ang in ANGLES:
            for pose in POSES:
                cx = col * QUADRO_W + QUADRO_W*0.5
                cy = linha * QUADRO_H + QUADRO_H*0.5
                desenhar_botao(t, cx, cy, U, pessoa["kit"], ang, "tudo", bandeira=pessoa["bandeira"])
                info["poses"]["%d_%s"%(ang,pose)] = [col*QUADRO_W, linha*QUADRO_H, QUADRO_W, QUADRO_H]
                col+=1
        mapa["pessoas"].append(info)
    caminho = os.path.join(SAIDA, "jogadores.png")
    t.salvar(caminho)
    json.dump(mapa, open(os.path.join(SAIDA, "jogadores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("folha BANDEIRA: %dx%d · %d quadros (%s vs %s)"%(t.W,t.H,colunas*len(PESSOAS),SELECAO_A,SELECAO_B))
    print("ok: %s + jogadores.json (luz=2, bandeira)"%caminho)
    return caminho

if __name__ == "__main__":
    gerar()
