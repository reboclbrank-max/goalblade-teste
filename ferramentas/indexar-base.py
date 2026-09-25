#!/usr/bin/env python3
"""Índice FTS5 da memória oficial (base) + código do jogo. Rápido de refazer,
barato de manter: é o que faz a próxima conversa começar sabendo."""
import sqlite3, time, pathlib
RAIZES = [pathlib.Path("/home/user/base"), pathlib.Path("/home/user/ceifalume")]
IGNORAR = ("/.git", "/.godot", "/export/", "/node_modules")
DEST = pathlib.Path.home() / ".cache/ferramentas/base.db"
DEST.parent.mkdir(parents=True, exist_ok=True)
c = sqlite3.connect(DEST)
c.execute("DROP TABLE IF EXISTS base_doc")
c.execute("CREATE VIRTUAL TABLE base_doc USING fts5(caminho, texto, tokenize='porter unicode61')")
t0 = time.perf_counter(); n = 0
for r in RAIZES:
    for p in sorted(r.rglob("*.md")) + sorted(r.rglob("*.gd")) + sorted(r.rglob("*.js")):
        s = str(p)
        if any(x in s for x in IGNORAR) or "grava_jogo" in s:
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        c.execute("INSERT INTO base_doc VALUES (?,?)", (s, txt)); n += 1
c.commit()
print(f"índice: {n} documentos, {DEST.stat().st_size/1e6:.1f} MB, {(time.perf_counter()-t0)*1000:.0f} ms")
