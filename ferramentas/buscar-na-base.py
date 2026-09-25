#!/usr/bin/env python3
"""Busca no índice da base (FTS5 do SQLite) — o "motor de conhecimento" da bancada.
Monta a consulta a partir de termos soltos (radicalização porter: retratação encontra
retratar), rankeia por bm25 (coluna `rank` do FTS5) e devolve trechos.

  python3 ~/tools/buscar-na-base.py "release train retratacao"
  CEI_N=10 python3 ~/tools/buscar-na-base.py "versionCode"

Reconstruir o índice (fim de sessão, ou quando a base mudar):
  python3 ~/tools/indexar-base.py
"""
import sqlite3, sys, os, re, pathlib

termos = [w for w in re.findall(r"[\wÀ-ÿ\-]{2,}", " ".join(sys.argv[1:]))]
if not termos:
    print('uso: buscar-na-base.py "termos da pergunta"'); sys.exit(1)
# FTS5: cada termo vira prefixo buscado dentro do campo `texto`, todos obrigatórios
fts = " AND ".join('"texto" MATCH "' + t.replace('"', "") + '*"' for t in termos)
fts = " AND ".join(t.replace('"', "") + "*" for t in termos)
db = pathlib.Path.home() / ".cache/ferramentas/base.db"
if not db.exists():
    print("SEM ÍNDICE — rode: python3 ~/tools/indexar-base.py"); sys.exit(1)
c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
try:
    linhas = c.execute(
        "SELECT caminho, snippet(base_doc, 1, '[', ']', ' … ', 16), rank "
        "FROM base_doc WHERE base_doc MATCH ? ORDER BY rank LIMIT ?",
        (fts, int(os.environ.get("CEI_N", "5")))).fetchall()
except sqlite3.OperationalError as e:
    print("consulta inválida:", e); sys.exit(1)
if not linhas:
    print(f"nada para: {fts}"); sys.exit(0)
for caminho, snp, pontos in linhas:
    snp = re.sub(r"\s+", " ", snp)
    print(f"{caminho.replace('/home/user/', '')}  (rank {pontos:.2f})\n   {snp[:250]}")
