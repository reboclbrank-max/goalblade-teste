#!/usr/bin/env python3
"""Monta a trilha do trailer a partir do diário do trailer.gd.

O trailer é gravado quadro a quadro (silencioso). Este script lê
/trailer/eventos.txt (quadro + som), converte para segundos (30 fps)
e monta a trilha com os sons DO PRÓPRIO JOGO, no tempo certo:
  - música-tema do jogo (com laço) a partir do clique em Jogar;
  - efeitos de plantar/colher/vender/comprar em cada ação;
  - vinheta da marca na abertura e sino no dia novo.

Uso: python3 montar-trilha.py [pasta-do-trailer]
"""
import json
import subprocess
import sys
from pathlib import Path

FPS = 30
RAIZ = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/trailer")
JOGO = Path("/home/user/ceifalume")
SONS = JOGO / "arte" / "som"
SAIDA = RAIZ / "trilha.wav"

# volumes por elemento (0 a 1) — calibrados medindo a mixagem com medir-som.py
VOL_MUSICA = 0.52
VOL_EFEITO = 1.55
VOL_VINHETA = 1.20


def duracao(caminho: Path) -> float:
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(caminho)],
        capture_output=True, text=True, check=True)
    return float(saida.stdout.strip())


def main() -> int:
    eventos = []
    for linha in (RAIZ / "eventos.txt").read_text().splitlines():
        if not linha.strip():
            continue
        quadro, som = linha.split()
        eventos.append((int(quadro), som))
    quadros = int(sorted(RAIZ.glob("frames/*.png"))[-1].stem) + 1
    total = quadros / FPS
    print(f"trilha: {quadros} quadros = {total:.2f} s")

    entradas = []
    filtros = []
    rotulos = []
    indice = 0

    musica_em = None
    for quadro, som in eventos:
        if som == "MUSICA":
            musica_em = quadro / FPS
            break

    # música (com laço para cobrir o trailer todo) ---------------------------
    if musica_em is not None:
        arquivo = SONS / "musica-tema-01.ogg"
        dur = duracao(arquivo)
        repeticoes = int(total / dur) + 2
        entradas += ["-stream_loop", str(repeticoes), "-i", str(arquivo)]
        corte = total - musica_em
        filtros.append(
            f"[{indice}:a]atrim=0:{corte:.3f},asetpts=N/SR/TB,"
            f"afade=t=in:st=0:d=0.6,"
            f"afade=t=out:st={max(0.0, corte - 2.4):.3f}:d=2.4,"
            f"volume={VOL_MUSICA},adelay={int(musica_em * 1000)}:all=1[m{indice}]")
        rotulos.append(f"[m{indice}]")
        indice += 1

    # efeitos e vinheta ------------------------------------------------------
    for quadro, som in eventos:
        if som == "MUSICA":
            continue
        arquivo = SONS / f"{som}.ogg"
        if not arquivo.exists():
            print(f"  AVISO: sem arquivo para {som}")
            continue
        atraso = int(round(quadro / FPS * 1000))
        vol = VOL_VINHETA if som == "som-logo-rb-01" else VOL_EFEITO
        entradas += ["-i", str(arquivo)]
        filtros.append(f"[{indice}:a]volume={vol},adelay={atraso}:all=1[e{indice}]")
        rotulos.append(f"[e{indice}]")
        indice += 1

    if not rotulos:
        print("  ERRO: nenhum som no diário")
        return 1
    filtros.append("".join(rotulos) + f"amix=inputs={len(rotulos)}:duration=longest:"
                   f"normalize=0,volume=1.30,alimiter=limit=-1dB,apad,atrim=0:{total:.3f}[trilha]")

    cmd = ["ffmpeg", "-y", *entradas, "-filter_complex", ";".join(filtros),
           "-map", "[trilha]", "-ar", "48000", "-ac", "2", str(SAIDA)]
    print("  ffmpeg ...")
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  trilha: {SAIDA} ({SAIDA.stat().st_size / 1024:.0f} KB, {duracao(SAIDA):.2f} s)")

    # medição: a mesma régua que o projeto usa para mixagem
    medidor = Path("/home/user/base/ferramentas/medir-som.py")
    if medidor.exists():
        import os
        env = dict(os.environ, MEDIR_MODO="mix")
        r = subprocess.run([sys.executable, str(medidor), str(SAIDA)],
                           capture_output=True, text=True, env=env)
        print(r.stdout.strip() or r.stderr.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
