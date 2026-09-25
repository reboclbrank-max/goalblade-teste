#!/usr/bin/env python3
"""Medidor de som da bancada: pico, RMS, loudness integrado (EBU R128) e duração.

  medir-som.py arquivo.wav [outro.ogg ...]
  MEDIR_ALVO=-6 medir-som.py arte/som/*.wav      # alvo de pico em dBFS

Por que existe: "o som ficou bom" não é verificável; pico, LUFS e silêncio são.
Alvos usados em 2026-09-15 para efeito de jogo em navegador:
  pico (true peak) entre -6 e -3 dBFS · integrado em torno de -24 a -16 LUFS
  para a mixagem inteira · nenhum estouro em 0 dBFS · sem silêncio absoluto no
  loop de música (a falha clássica do export web é o arquivo existir e não tocar).
Saída: uma linha por arquivo, com PASSA/FALHA contra os alvos.
"""
import re
import subprocess
import sys
import os
import json


def ffmpeg(args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args],
                          capture_output=True, text=True).stderr


def medir(caminho):
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", caminho], capture_output=True, text=True).stdout.strip()
    astats = ffmpeg(["-i", caminho, "-af", "astats=measure_overall=Peak_level+RMS_level", "-f", "null", "-"])
    pico = rms = None
    # o astats do ffmpeg imprime "Channel: 1 Peak level dB: -6.0 RMS level dB: -20.1"
    # na MESMA linha — por isso a expressão não pode exigir começo de linha
    m = re.search(r"Peak level dB:\s*(-?[0-9.]+)", astats)
    if m:
        pico = float(m.group(1))
    m = re.search(r"RMS level dB:\s*(-?[0-9.]+)", astats)
    if m:
        rms = float(m.group(1))
    m = re.search(r"Peak level dB:\s*(-?[0-9.]+).*?Peak level dB:\s*(-?[0-9.]+)", astats, re.S)
    ebu = ffmpeg(["-i", caminho, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    lu = tp = None
    bloco = ebu.split("Summary:")[-1] if "Summary:" in ebu else ""
    m = re.search(r"I:\s*(-?[0-9.]+)\s*LUFS", bloco)
    if m:
        lu = float(m.group(1))
    m = re.search(r"Peak:\s*\d+:\s*(-?[0-9.]+)\s*dBFS", bloco)
    if m:
        tp = float(m.group(1))
    return dict(duracao=float(dur) if dur else None, pico_db=pico, rms_db=rms,
                lufs=lu, true_peak_db=tp)


def main():
    arquivos = sys.argv[1:]
    if not arquivos:
        print(__doc__)
        return 1
    # MEDIR_MODO=clip  → alvo de pico por efeito (o que o desenhista de som entrega)
    # MEDIR_MODO=mix   → a mixagem inteira: pico ≤ -1 dBFS e integrado entre -20 e -10
    modo = os.environ.get("MEDIR_MODO", "clip")
    alvo_pico = float(os.environ.get("MEDIR_ALVO", "-6"))
    tolerancia = float(os.environ.get("MEDIR_TOL", "3"))
    linhas = []
    for a in arquivos:
        m = medir(a)
        pico = m["true_peak_db"] if m["true_peak_db"] is not None else m["pico_db"]
        # R128 não mede loudness integrado de clip curto (a janela de gate é de 3 s
        # e o ebur128 devolve -70): para efeito pontual o que vale é o pico.
        curto = (m["duracao"] or 0.0) < 3.0
        if modo == "mix":
            ok = (pico is not None and pico <= -1.0
                  and m["lufs"] is not None and -21.0 <= m["lufs"] <= -9.0)
        else:
            ok = pico is not None and abs(pico - alvo_pico) <= tolerancia
        linhas.append(dict(arquivo=os.path.basename(a), **m, passa=ok))
        print("%-24s dur=%5.2fs pico=%7s dB  LUFS=%7s  RMS=%7s dB  %s" % (
            os.path.basename(a), m["duracao"] or 0,
            "-" if pico is None else f"{pico:.1f}",
            "n/a" if (m["lufs"] is None or (curto and m["lufs"] <= -69.5)) else f"{m['lufs']:.1f}",
            "-" if m["rms_db"] is None else f"{m['rms_db']:.1f}",
            "PASSA" if ok else f"FALHA (alvo {alvo_pico:+.0f} ±{tolerancia:.0f} dB)"))
    if os.environ.get("MEDIR_JSON"):
        print(json.dumps(linhas, ensure_ascii=False))
    return 0 if all(l["passa"] for l in linhas) else 2


if __name__ == "__main__":
    sys.exit(main())
