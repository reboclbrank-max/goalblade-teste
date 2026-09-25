#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR DE AUDITORIA — quem roda, guarda o histórico e escreve o que fazer (v0.1).

Uso:
    python3 auditar.py                 # auditoria completa (varre e grava)
    python3 auditar.py --rapido        # sem conferir links (mais rápido)
    python3 auditar.py --so-relatorio  # não grava histórico, só mostra

Ele:
  1. roda todas as verificações (`verificacoes.py`);
  2. calcula a **nota de saúde** (100 − soma dos pesos dos problemas);
  3. compara com a última auditoria e mostra o que **melhorou**, o que **piorou** e o que **se repete**;
  4. escreve `RELATORIO-AUDITORIA.md` (leitura humana, com o "faça isto" de cada achado);
  5. escreve `AUDITORIA.json` (máquina: histórico e baselines usados pelas verificações);
  6. acrescenta em `MELHORIAS.md` o que ainda não está escrito lá — o motor vai **moldando** as
     regras do projeto a cada rodada, em vez de só reclamar.
"""
import json
import os
import sys
from collections import Counter
from datetime import datetime

import verificacoes as V

PASTA = os.path.dirname(os.path.abspath(__file__))
RELATORIO = os.path.join(PASTA, "RELATORIO-AUDITORIA.md")
DADOS = os.path.join(PASTA, "AUDITORIA.json")
MELHORIAS = os.path.join(PASTA, "MELHORIAS.md")
PESOS = {"erro": 1.0, "aviso": 0.45, "nota": 0.0}


def carregar():
    if os.path.isfile(DADOS):
        try:
            return json.load(open(DADOS, encoding="utf-8"))
        except Exception:
            pass
    return {"historico": [], "recorrentes": {}, "baselines": {}}


def salvar(d):
    json.dump(d, open(DADOS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def agrupar(achados):
    """Junta achados do mesmo tipo e lugar: um auditor escreve uma linha, não trinta."""
    vistos, saida = {}, []
    for a in achados:
        chave = (a["id"], a["onde"], a["titulo"])
        if chave in vistos:
            vistos[chave]["vezes"] += 1
            continue
        a = dict(a)
        a["vezes"] = 1
        vistos[chave] = a
        saida.append(a)
    return saida


def nota(achados):
    perda = 0.0
    for a in achados:
        perda += a["peso"] * PESOS.get(a["nivel"], 0.4)
    return max(0, round(100 - perda))


def escrever_relatorio(achados, dados, anterior):
    n = nota(achados)
    erros = [a for a in achados if a["nivel"] == "erro"]
    avisos = [a for a in achados if a["nivel"] == "aviso"]
    notas = [a for a in achados if a["nivel"] == "nota"]
    ago = datetime.now().strftime("%d/%m/%Y %H:%M")

    ids_agora = {a["id"] for a in erros + avisos}
    ids_antes = set(anterior.get("ids", []))
    novos = ids_agora - ids_antes
    resolvidos = ids_antes - ids_agora
    repetidos = {i: dados["recorrentes"].get(i, 0) for i in ids_agora if dados["recorrentes"].get(i, 0) >= 3}

    linhas = []
    linhas.append("# Relatório do MOTOR DE AUDITORIA")
    linhas.append("")
    linhas.append("> Automático. Roda em toda rodada de trabalho. Gerado em **%s**." % ago)
    linhas.append("")
    linhas.append("## Nota de saúde: **%d/100**" % n)
    linhas.append("")
    linhas.append("| | quantidade |")
    linhas.append("|---|---|")
    linhas.append("| 🔴 erros | %d |" % len(erros))
    linhas.append("| 🟡 avisos | %d |" % len(avisos))
    linhas.append("| ⚪ conferências em ordem | %d |" % len(notas))
    linhas.append("")

    if anterior.get("nota") is not None:
        d = n - anterior["nota"]
        seta = "▬ sem mudança" if d == 0 else ("▲ +%d desde a última" % d if d > 0 else "▼ %d desde a última" % d)
        linhas.append("Comparação com a auditoria anterior (%s): **%s**." % (anterior.get("quando", "?"), seta))
        linhas.append("")
    if resolvidos:
        linhas.append("✅ **Corrigidos desde a última:** %s" % ", ".join(sorted(resolvidos)))
        linhas.append("")
    if novos:
        linhas.append("🆕 **Apareceram agora:** %s" % ", ".join(sorted(novos)))
        linhas.append("")
    if repetidos:
        linhas.append("♻️ **Insistem (3 ou mais auditorias):** %s" % ", ".join(
            "%s (%dx)" % (k, v) for k, v in sorted(repetidos.items())))
        linhas.append("")

    def bloco(titulo, itens):
        if not itens:
            return
        linhas.append("## %s" % titulo)
        linhas.append("")
        for a in itens:
            linhas.append("### %s — %s" % (("🔴" if a["nivel"] == "erro" else "🟡") if titulo.startswith("🔴") or titulo.startswith("🟡") else "•", a["titulo"]))
            linhas.append("")
            linhas.append("- **Onde:** `%s`" % a["onde"])
            if a["detalhe"]:
                extra = (" · **%d ocorrências**" % a["vezes"]) if a.get("vezes", 1) > 1 else ""
                linhas.append("- **O que o motor viu:** %s%s" % (a["detalhe"], extra))
            linhas.append("- **O que fazer:** %s" % a["correcao"])
            linhas.append("")

    bloco("🔴 Erros (quebrado — corrigir antes de seguir)", erros)
    bloco("🟡 Avisos (pode dar problema — corrigir quando der)", avisos)
    bloco("⚪ Conferências que passaram", notas)

    linhas.append("## Como este relatório é feito")
    linhas.append("")
    linhas.append("`verificacoes.py` tem %d tipos de conferência: python, GDScript, segredos, links, imagens, "
                  "desempenho do Godot, marketing, consistência dos documentos, repositório e rotina. "
                  "Cada problema tem peso; a nota é 100 menos a soma. O histórico fica em `AUDITORIA.json` e as "
                  "regras que o motor vai acumulando, em `MELHORIAS.md`." % 10)
    linhas.append("")
    open(RELATORIO, "w", encoding="utf-8").write("\n".join(linhas))


def moldar_regras(achados):
    """O motor 'molda': grava em MELHORIAS.md o que ainda não está escrito lá."""
    if not os.path.isfile(MELHORIAS):
        open(MELHORIAS, "w", encoding="utf-8").write(
            "# MELHORIAS — as regras que o MOTOR DE AUDITORIA foi acumulando\n\n"
            "Cada linha aqui nasceu de um problema real encontrado pelo motor. É a memória dele:\n"
            "antes de repetir um erro, ele lê este arquivo.\n\n")
    texto = open(MELHORIAS, encoding="utf-8").read()
    novos = []
    for a in achados:
        if a["nivel"] == "nota":
            continue
        marca = "(%s)" % a["id"]
        if marca not in texto:
            novos.append("- **Regra %s** — %s → *o que fazer:* %s  \n  onde apareceu: `%s` — %s"
                         % (marca, a["titulo"], a["correcao"], a["onde"], a["detalhe"]))
    if novos:
        with open(MELHORIAS, "a", encoding="utf-8") as f:
            f.write("\n## %s\n\n" % datetime.now().strftime("%d/%m/%Y"))
            f.write("\n".join(novos) + "\n")
    return len(novos)


def main():
    rapido = "--rapido" in sys.argv
    so_rel = "--so-relatorio" in sys.argv
    achados = agrupar(V.todas(incluir_links=not rapido))
    dados = carregar()
    anterior = {}
    if dados["historico"]:
        h = dados["historico"][-1]
        anterior = {"nota": h.get("nota"), "quando": h.get("quando"), "ids": h.get("ids", [])}

    n = nota(achados)
    ids = [a["id"] for a in achados if a["nivel"] in ("erro", "aviso")]
    for i in ids:
        dados["recorrentes"][i] = dados["recorrentes"].get(i, 0) + 1

    escrever_relatorio(achados, dados, anterior)
    if not so_rel:
        dados["historico"].append({"quando": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                   "nota": n, "ids": sorted(set(ids)),
                                   "erros": len([a for a in achados if a["nivel"] == "erro"]),
                                   "avisos": len([a for a in achados if a["nivel"] == "aviso"])})
        dados["historico"] = dados["historico"][-60:]
        salvar(dados)
        q = moldar_regras(achados)

    print("nota de saúde: %d/100  (erros %d · avisos %d)"
          % (n, len([a for a in achados if a["nivel"] == "erro"]), len([a for a in achados if a["nivel"] == "aviso"])))
    for a in achados:
        if a["nivel"] != "nota":
            print("  [%s] %s — %s" % (a["nivel"].upper(), a["titulo"], a["onde"]))
    if not so_rel:
        print("relatório: %s" % os.path.relpath(RELATORIO, V.RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
