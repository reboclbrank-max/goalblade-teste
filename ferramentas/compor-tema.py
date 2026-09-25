#!/usr/bin/env python3
"""Ceifalume — tema noturno v2 (caixinha de música da fazenda).

8 compassos 4/4 a 75bpm (pulso 0,8 s): C G Am F C G F C.
Melodia composta (não aleatória) + arpejo + baixo + cama de vento.
(C.18: cama de grilos removida — ruído branco soava como chiado de bug.)
Final com crossfade p/ o loop não ter clique. Saída: musica-tema-01.ogg
Uso: python3 tools/compor-tema.py  (precisa de ffmpeg no PATH)
"""
import math
import subprocess

import numpy as np

SR = 44100
PULSO = 0.8  # 75 bpm
COMPASSOS = [
    # (baixo, terca, quinta) por compasso
    (130.81, 164.81, 196.00),  # C
    (98.00, 246.94, 293.66),   # G
    (110.00, 261.63, 329.63),  # Am
    (87.31, 220.00, 261.63),   # F
    (130.81, 164.81, 196.00),  # C
    (98.00, 246.94, 293.66),   # G
    (87.31, 220.00, 261.63),   # F
    (130.81, 164.81, 196.00),  # C (fecha o loop)
]
# melodia: (freq, pulso_inicial, duracao_pulsos)
MELODIA = [
    (329.63, 0.0, 1), (392.00, 1.0, 1), (523.25, 2.0, 2),
    (493.88, 4.0, 1), (587.33, 5.0, 1), (392.00, 6.0, 2),
    (440.00, 8.0, 1), (523.25, 9.0, 1), (659.25, 10.0, 1.5), (587.33, 11.5, 0.5),
    (523.25, 12.0, 2), (440.00, 14.0, 1), (392.00, 15.0, 1),
    (329.63, 16.0, 1), (392.00, 17.0, 1), (440.00, 18.0, 1), (523.25, 19.0, 1),
    (587.33, 20.0, 1.5), (493.88, 21.5, 0.5), (392.00, 22.0, 2),
    (440.00, 24.0, 1), (392.00, 25.0, 1), (349.23, 26.0, 1), (329.63, 27.0, 1),
    (293.66, 28.0, 1), (329.63, 29.0, 1), (261.63, 30.0, 2),
]
TOTAL_PULSOS = 32
EXTRA = 1.2  # cauda p/ o crossfade


def nota_caixinha(f, t0, dur, n_total, nivel=0.5, brilho=0.28):
    """Seno + harmônicos com decaimento de caixinha de música."""
    n0 = int(t0 * SR)
    n1 = min(n_total, n0 + int((dur + 2.2) * SR))
    if n1 <= n0:
        return np.zeros(n_total)
    t = np.arange(n1 - n0) / SR
    env = np.exp(-t / 0.55) * np.minimum(1.0, t / 0.008)
    s = (np.sin(2 * math.pi * f * t)
         + brilho * np.sin(2 * math.pi * f * 3.01 * t) * np.exp(-t / 0.25)
         + 0.15 * np.sin(2 * math.pi * f * 2.0 * t) * np.exp(-t / 0.4))
    out = np.zeros(n_total)
    out[n0:n1] = nivel * env * s / 1.4
    return out


def nota_fofa(f, t0, dur, n_total, nivel=0.14):
    """Dedilhado macio (arpejo/baixo): triangular filtrado."""
    n0 = int(t0 * SR)
    n1 = min(n_total, n0 + int(dur * SR))
    if n1 <= n0:
        return np.zeros(n_total)
    t = np.arange(n1 - n0) / SR
    env = np.exp(-t / 0.35) * np.minimum(1.0, t / 0.01)
    s = (np.sin(2 * math.pi * f * t)
         + 0.25 * np.sin(2 * math.pi * f * 2 * t)
         + 0.08 * np.sin(2 * math.pi * f * 3 * t))
    out = np.zeros(n_total)
    out[n0:n1] = nivel * env * s / 1.3
    return out


def main():
    dur_total = TOTAL_PULSOS * PULSO + EXTRA
    n = int(dur_total * SR)
    mix = np.zeros(n)

    for f, p0, pd in MELODIA:
        mix += nota_caixinha(f, p0 * PULSO, pd * PULSO, n)
    for comp, (baixo, terca, quinta) in enumerate(COMPASSOS):
        t_bar = comp * 4 * PULSO
        mix += nota_fofa(baixo, t_bar, 4 * PULSO, n, nivel=0.16)
        for i, f in enumerate([baixo * 2, terca, quinta, terca * 2,
                               quinta, terca, baixo * 2, terca]):
            mix += nota_fofa(f, t_bar + i * PULSO / 2, PULSO / 2, n, nivel=0.09)

    # cama noturna bem baixa: vento (grilos FORA na C.18 — o ruído branco em
    # rajadas soava como chiado de bug no celular do dono; ganho 0 p/ reverter)
    rng = np.random.default_rng(7)
    GANHO_GRILOS = 0.0  # era 0.012
    grilos = rng.standard_normal(n)
    # chilreio: amplitude modulada em rajadas
    mod = (np.sin(2 * math.pi * 4.2 * np.arange(n) / SR) > 0.55).astype(float)
    grilos = grilos * mod * GANHO_GRILOS
    vento = np.convolve(rng.standard_normal(n), np.ones(4000) / 4000, mode="same")
    vento = vento / (np.abs(vento).max() + 1e-9) * 0.02
    mix += grilos + vento

    # espaço: eco simples 0,45 s
    eco = np.zeros(n)
    atraso = int(0.45 * SR)
    eco[atraso:] = mix[:-atraso] * 0.22
    mix += eco * 0.5

    # crossfade do fim com o começo (loop sem clique)
    base = TOTAL_PULSOS * PULSO
    n_base = int(base * SR)
    n_x = int(0.8 * SR)
    saida = mix[:n_base].copy()
    rampa = np.linspace(0, 1, n_x) ** 2
    saida[:n_x] = saida[:n_x] * rampa + mix[n_base:n_base + n_x] * (1 - rampa)

    pico = np.abs(saida).max()
    saida = saida / pico * 0.89
    print("pico master: %.1f dBFS | dur: %.1f s" % (20 * math.log10(0.89), base))

    pcm = (np.clip(saida, -1, 1) * 32767).astype(np.int16)
    raw = "/tmp/tema.raw"
    pcm.tofile(raw)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR),
                    "-ac", "1", "-i", raw, "-c:a", "libvorbis", "-q:a", "4",
                    "/home/user/ceifalume/arte/som/musica-tema-01.ogg"], check=True)
    print("ogg ok")


if __name__ == "__main__":
    main()
