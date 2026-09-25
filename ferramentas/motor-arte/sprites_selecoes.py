#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR RB — folha de BOTÕES com BANDEIRA para 16 seleções (v8, 25/09/2026).

Gera 16 linhas (1 por seleção) × 64 direções×poses = 4096×1152
Cada linha é um botão com a bandeira estampada (pintor_botao) e numero legível.
Modo BOTÃO com bandeira: uniforme = bandeira, não só cor.

Uso:
  python sprites_selecoes.py                # 16 seleções completas 4096×1152
  python sprites_selecoes.py BRA ARG        # só 2 seleções (4096×864 com 12 linhas: 5 jogadores+goleiro cada) — geração dinâmica
Depois copiar para projetos/02-goalblade/jogo/arte/jogadores.png
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

# 16 seleções — dados sincronizados com projetos/02-goalblade/jogo/scripts/selecoes.gd
SELECOES = [
    ("ARG","Argentina",92,"7dd3fc","ARGENTINA"),
    ("FRA","França",90,"1e3a8a","FRANCA"),
    ("BRA","Brasil",89,"facc15","BRASIL"),
    ("ING","Inglaterra",88,"ffffff","INGLATERRA"),
    ("ESP","Espanha",87,"dc2626","ESPANHA"),
    ("POR","Portugal",86,"064e3b","PORTUGAL"),
    ("NED","Holanda",85,"f97316","HOLANDA"),
    ("GER","Alemanha",84,"d1d5db","ALEMANHA"),
    ("BEL","Bélgica",83,"7f1d1d","BELGICA"),
    ("CRO","Croácia",82,"991b1b","CROACIA"),
    ("URU","Uruguai",81,"e0f2fe","URUGUAI"),
    ("ITA","Itália",80,"60a5fa","ITALIA"),
    ("MEX","México",78,"16a34a","MEXICO"),
    ("USA","USA",77,"bfdbfe","USA"),
    ("JPN","Japão",76,"fff7ed","JAPAO"),
    ("SEN","Senegal",75,"84cc16","SENEGAL"),
]

def kit_para_selecao(sel, numero=10):
    # sel = tupla (id,nome,forca,camisa,bandeira)
    camisa = sel[3]
    # calcao e meia acompanham tons escuros da seleção para leitura
    calcao_map = {"facc15":"0f2b4d","7dd3fc":"0e2a4a","1e3a8a":"7f1d1d","d1d5db":"111111","dc2626":"1e1b4b","ffffff":"0f172a","064e3b":"7f1d1d","60a5fa":"f8fafc","e0f2fe":"0e0e0e","f97316":"0e0e0e","7f1d1d":"facc15","991b1b":"1e3a8a","16a34a":"7f1d1d","bfdbfe":"1e3a8a","fff7ed":"0a2a8a","84cc16":"facc15"}
    calcao = calcao_map.get(camisa, "111111")
    return KitTopo(camisa=camisa, calcao=calcao, meia=camisa, numero=numero, identidade=Identidade(numero))

def gerar(dinamico=None):
    """
    dinamico: None -> 16 seleções (4096×1152)
              [id1, id2] -> 2 seleções com 6 jogadores cada (5+goleiro) = 12 linhas 4096×864
    """
    os.makedirs(SAIDA, exist_ok=True)
    colunas = len(ANGLES) * len(POSES)
    if dinamico and len(dinamico)==2:
        # modo dinâmico só 2 times (12 linhas) — recomendado para partida
        ids = dinamico
        sel_map = {s[0]: s for s in SELECOES}
        escolhidas = [sel_map[i] for i in ids if i in sel_map]
        if len(escolhidas)!=2:
            print("ids invalidos, use ex: BRA ARG. Disponiveis:", list(sel_map.keys()))
            return
        # layout compativel com jogo.gd/jogador.gd: 0-4 time0, 5-9 time1, 10 goleiro0, 11 goleiro1
        pessoas = []
        bandeiras = []
        # 5 de cada time
        for n in range(5):
            pessoas.append(kit_para_selecao(escolhidas[0], numero=n+1))
            bandeiras.append(escolhidas[0][4])
        for n in range(5):
            pessoas.append(kit_para_selecao(escolhidas[1], numero=n+1))
            bandeiras.append(escolhidas[1][4])
        # goleiros
        pessoas.append(kit_para_selecao(escolhidas[0], numero=1))
        bandeiras.append(escolhidas[0][4])
        pessoas.append(kit_para_selecao(escolhidas[1], numero=1))
        bandeiras.append(escolhidas[1][4])
        linhas = len(pessoas) # 12
    else:
        # 16 seleções — 1 botão por seleção (para menu/preview) — mas para jogo precisamos 12 linhas, então aqui 16 linhas
        pessoas = []
        bandeiras = []
        for sel in SELECOES:
            pessoas.append(kit_para_selecao(sel, numero=10))
            bandeiras.append(sel[4])
        linhas = len(pessoas) # 16

    t = Tela(colunas * QUADRO_W, linhas * QUADRO_H, luz=2)
    t.limpar((0,0,0,0))
    mapa = {"u": U, "quadro": [QUADRO_W, QUADRO_H], "angles": ANGLES, "poses": POSES, "pessoas": [], "colunas": colunas, "modo": "botao-bandeira", "selecoes": [s[0] for s in SELECOES] if dinamico is None else dinamico}
    for linha, (kit, bandeira) in enumerate(zip(pessoas, bandeiras)):
        info = {"linha": linha, "bandeira": bandeira, "numero": kit.numero, "poses": {}}
        col=0
        for ang in ANGLES:
            for pose in POSES:
                cx = col * QUADRO_W + QUADRO_W*0.5
                cy = linha * QUADRO_H + QUADRO_H*0.5
                hab = "tudo"  # 4 habilidades no máximo: cola+drible+velocidade+chute
                desenhar_botao(t, cx, cy, U, kit, ang, hab, bandeira=bandeira)
                info["poses"]["%d_%s"%(ang,pose)] = [col*QUADRO_W, linha*QUADRO_H, QUADRO_W, QUADRO_H]
                col+=1
        mapa["pessoas"].append(info)
    caminho = os.path.join(SAIDA, "jogadores.png")
    t.salvar(caminho)
    json.dump(mapa, open(os.path.join(SAIDA, "jogadores.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("folha BOTA0-BANDEIRA: %dx%d · %d quadros · modo %s" % (t.W, t.H, colunas*linhas, "dinamico 2 times" if dinamico else "16 selecoes"))
    print("ok: %s + jogadores.json" % caminho)
    return caminho

if __name__ == "__main__":
    if len(sys.argv)==3:
        gerar([sys.argv[1].upper(), sys.argv[2].upper()])
    else:
        gerar()
