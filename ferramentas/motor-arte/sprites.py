#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — folha de sprites do GoalBlade (v5.0, 25/09/2026).

Gera UMA imagem com todos os jogadores, em 8 direções e 8 poses, cada um com identidade própria
(tom de pele, cabelo, chuteira, meia alta, listras, capitão) — e o MAPA das posições.

Como o jogo usa: carrega esta imagem e recorta o quadro certo conforme a direção e o passo.
Um só carregamento, zero desenho por código por quadro — é o máximo de desempenho no celular.

Layout: linhas = pessoas (12: 5 do time 1, 5 do time 2, 2 goleiros) · colunas = 8 direções × 8 poses.
Passe v11: o pintor acrescenta volume suave de pele/tecido, costura dupla e sola da chuteira;
o Godot aplica escala base 0,56 e profundidade visual sem mudar a física.
"""
import json
import os
import sys

from motor_rb import Tela, cor
from pintor_realista import KitTopo, Identidade, desenhar_jogador

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saida")
U = 2.02                    # mobile 64x72 (4096x864) cabe em 4096 max texture - antes 144x160 estourava
QUADRO_W, QUADRO_H = 64, 72
ANGLES = list(range(0, 360, 45))          # 0,45,...,315
POSES = ["parado", "c0", "c1", "c2", "c3", "chute", "dividida", "comemora"]

# quem são as pessoas do jogo: 5 de cada time + os goleiros
PESSOAS = []
for i in range(5):
    PESSOAS.append({"kit": KitTopo(camisa="e23e37", calcao="fefefe", meia="d93a33", numero=i + 1,
                                   listras="fefefe" if i % 2 == 0 else None,
                                   identidade=Identidade(i, capitao=(i == 0)))})
for i in range(5):
    PESSOAS.append({"kit": KitTopo(camisa="2f5fd8", calcao="111a38", meia="22336b", numero=i + 1,
                                   listras="f8f8fa" if i % 2 == 1 else None,
                                   identidade=Identidade(i + 3))})
PESSOAS.append({"kit": KitTopo(camisa="ffd34d", calcao="1d2430", meia="ffd34d", numero=1,
                               luvas="25c0c9", cabelo_tipo="raspado", identidade=Identidade(1))})
PESSOAS.append({"kit": KitTopo(camisa="7ef2a8", calcao="16202c", meia="7ef2a8", numero=1,
                               luvas="f2f4f6", cabelo_tipo="curto", identidade=Identidade(4))})


def gerar():
    os.makedirs(SAIDA, exist_ok=True)
    colunas = len(ANGLES) * len(POSES)
    t = Tela(colunas * QUADRO_W, len(PESSOAS) * QUADRO_H, luz=2)
    t.limpar((0, 0, 0, 0))                     # fundo transparente: o jogo desenha sobre o campo
    mapa = {"u": U, "quadro": [QUADRO_W, QUADRO_H], "angles": ANGLES, "poses": POSES,
            "pessoas": [], "colunas": colunas}
    for linha, pessoa in enumerate(PESSOAS):
        info = {"linha": linha, "poses": {}}
        col = 0
        for ang in ANGLES:
            for pose in POSES:
                cx = col * QUADRO_W + QUADRO_W * 0.5
                cy = linha * QUADRO_H + QUADRO_H * 0.5
                if len(pose) == 2 and pose[1].isdigit():
                    p, fase = "corrida", int(pose[1]) / 4.0
                elif pose == "chute":
                    p, fase = "chute", 0.5
                elif pose == "dividida":
                    p, fase = "dividida", 0.5
                elif pose == "comemora":
                    p, fase = "comemora", 0.5
                else:
                    p, fase = "parado", 0.0
                desenhar_jogador(t, cx, cy, U, pessoa["kit"], ang, p, fase)
                info["poses"]["%d_%s" % (ang, pose)] = [col * QUADRO_W, linha * QUADRO_H, QUADRO_W, QUADRO_H]
                col += 1
        mapa["pessoas"].append(info)
    caminho = os.path.join(SAIDA, "jogadores.png")
    t.salvar(caminho)
    json.dump(mapa, open(os.path.join(SAIDA, "jogadores.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("folha: %dx%d · %d quadros" % (t.W, t.H, colunas * len(PESSOAS)))
    print("ok: %s + jogadores.json" % caminho)
    return caminho


if __name__ == "__main__":
    gerar()
