#!/usr/bin/env python3
"""CEIFALUME — auditor 100%: o quão profissional (nada genérico) está o jogo.

Mede 100 pontos em sinais OBJETIVOS de profissionalismo: identidade, arte,
som, textos, movimento e loja. Gosto (arte bonita?) continua sendo olho
humano — isto aqui garante que nada TÉCNICO escape.

Uso: python3 tools/auditor-100.py   (sai 0 se 100/100, 1 se falta algo)
"""
import os
import re
import sys

RAIZ = "/home/user"
JOGO = f"{RAIZ}/ceifalume"
SITE = f"{RAIZ}/site"
BASE = f"{RAIZ}/base"

pontos = 0
falhas = []


def ler(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def existe(caminho):
    return os.path.isfile(caminho)


def checar(nome, peso, ok, dica=""):
    global pontos
    if ok:
        pontos += peso
        print(f"  ✅ {nome} (+{peso})")
    else:
        falhas.append(nome)
        print(f"  ❌ {nome} (0/{peso}){(' — ' + dica) if dica else ''}")


def grep(padrao, arquivos):
    rx = re.compile(padrao)
    achados = []
    for arq in arquivos:
        for i, linha in enumerate(ler(arq).splitlines(), 1):
            if rx.search(linha):
                achados.append(f"{os.path.basename(arq)}:{i}")
    return achados


def arquivos_gd():
    return [f"{JOGO}/{f}" for f in os.listdir(JOGO)
            if f.endswith(".gd") and os.path.isfile(f"{JOGO}/{f}")]


def main():
    print("== IDENTIDADE (20) ==")
    proj = ler(f"{JOGO}/project.godot")
    checar("I1 ícone próprio (não icon.svg)",
           4, 'config/icon="res://arte/' in proj and ".png" in proj.split("config/icon=")[1].split("\n")[0],
           "project.godot config/icon")
    checar("I2 splash escuro com logo", 3,
           "boot_splash/bg_color=Color(0.04" in proj and "logo-rb" in proj)
    checar("I3 fonte padrão própria", 5, "theme/default_font=" in proj,
           "gui/theme/default_font no project.godot")
    checar("I4 nome do jogo com fonte de título", 2,
           "ExtraBold" in ler(f"{JOGO}/titulo.gd"))
    checar("I5 abertura da empresa com logo", 3,
           existe(f"{JOGO}/abertura.tscn") and existe(f"{JOGO}/arte/logo-rb-512.png"))
    checar("I6 nome + descrição do app", 3,
           'config/name="Ceifalume"' in proj and "config/description=" in proj)

    print("== ARTE (20) ==")
    roteiro = ler(f"{JOGO}/roteiro_principal.gd")
    ids = sorted(set(re.findall(r'"id"\s*:\s*"([^"]+)"', roteiro)))
    faltando = [f"plantacao-{i}-{e}-128.png" for i in ids
                for e in ("semente", "broto", "pronto")
                if not existe(f"{JOGO}/arte/plantacao-{i}-{e}-128.png")]
    checar(f"A1 toda planta tem 3 desenhos ({len(ids)} plantas)", 8,
           not faltando, f"faltam: {faltando[:3]}" if faltando else "")
    checar("A2 terra desenhada", 2, existe(f"{JOGO}/arte/solo-noite-240x210.png"))
    checar("A3 fundo + cartaz da fazenda", 3,
           existe(f"{JOGO}/arte/fundo-noite-ceifalume-1280x720.png")
           and existe(f"{JOGO}/arte/splash-fazenda-1280x720.png"))
    pngs = [f for f in os.listdir(f"{JOGO}/arte") if f.endswith(".png")]
    sem_import = [f for f in pngs if not existe(f"{JOGO}/arte/{f}.import")]
    checar("A4 todo desenho importado", 2, not sem_import,
           f"sem .import: {sem_import[:3]}" if sem_import else "")
    leia = ler(f"{JOGO}/arte/LEIA-ME.md")
    checar("A5 LEIA-ME sem ❌", 3, "❌" not in leia)
    todo_codigo = " ".join(ler(a) for a in arquivos_gd()) + " " + leia
    # plantacao-*.png carrega por contrato dinâmico (caminho_sprite) — o A1
    # já confere; aqui só contam arquivos com nome literal no código.
    import fnmatch
    cobertos = ("icone-ceifalume-512.png", "icone-ceifalume-192.png", "logo-rb-512.png",
                "splash-fazenda-1280x720.png",
                "fundo-noite-ceifalume-1280x720.png",
                "solo-noite-240x210.png")
    mortos = [f for f in pngs if f not in todo_codigo and f not in cobertos
              and not fnmatch.fnmatch(f, "plantacao-*-128.png")]
    checar("A6 sem desenho morto (não usado)", 2, not mortos,
           f"mortos: {mortos[:3]}" if mortos else "")

    print("== SOM (15) ==")
    ganchos = ["plantar", "colher", "vender", "dia-novo", "comprar",
               "evento", "logo-rb", "musica-tema"]
    def arq_som(g):
        if g == "musica-tema":
            return f"{JOGO}/arte/som/musica-tema-01.ogg"
        return f"{JOGO}/arte/som/som-{g}-01.ogg"
    sem_som = [g for g in ganchos if not existe(arq_som(g))]
    checar(f"S1 todo gancho tem som ({len(ganchos) - len(sem_som)}/{len(ganchos)})",
           8, not sem_som, f"mudos: {sem_som}" if sem_som else "")
    checar("S2 nenhum som provisório", 5, "provisório" not in leia,
           "trocar na fase C (áudio real)")
    try:
        tam = os.path.getsize(f"{JOGO}/arte/som/musica-tema-01.ogg")
    except OSError:
        tam = 0
    checar("S3 música-tema substancial (>100KB)", 2, tam > 100_000)

    print("== TEXTOS (15) ==")
    alvos = arquivos_gd() + [f"{JOGO}/cena_principal.tscn",
                             f"{JOGO}/titulo.tscn", f"{SITE}/ceifalume/index.html"]
    sujeira = grep(r"rascunho|lorem|TODO|FIXME|placeholder", alvos)
    sujeira = [s for s in sujeira if "prova_visual" not in s and "auditor" not in s.lower()]
    checar("T1 sem rascunho/lorem/TODO", 5, not sujeira,
           f"achados: {sujeira[:3]}" if sujeira else "")
    checar("T2 sem 'Semana N' visível", 3,
           not grep(r"Semana [0-9]", [f"{SITE}/ceifalume/index.html", f"{JOGO}/titulo.tscn"]))
    def sem_comentario(arq):
        linhas = []
        for i, linha in enumerate(ler(arq).splitlines(), 1):
            s = linha.strip()
            if s.startswith("#") or s == "":
                continue
            linhas.append((i, linha))
        return linhas
    rx_mau = re.compile(r"1 colhem|vc | eh ")
    maus = []
    for arq in arquivos_gd():
        for i, linha in sem_comentario(arq):
            if rx_mau.search(linha):
                maus.append(f"{os.path.basename(arq)}:{i}")
    checar("T3 sem erros caçados", 3, not maus,
           f"ver: {maus[:2]}" if maus else "")
    checar("T4 título mostra versão", 2,
           "RotuloVersao" in ler(f"{JOGO}/titulo.tscn"))
    checar("T5 tutorial/como-jogar existe", 2,
           bool(grep(r"como jogar|tutorial", arquivos_gd())), "fase D")

    print("== MOVIMENTO (15) ==")
    todo = " ".join(ler(a) for a in arquivos_gd())
    nj = len(re.findall(r"create_tween|AnimationPlayer", todo))
    checar(f"M1 animações no jogo ({nj})", 5, nj >= 2, "fase D (suco)")
    checar("M2 partículas", 4, "Particles" in todo, "vaga-lumes vivos, fase D")
    checar("M3 botão faz som", 3, "tocar_efeito" in todo or "tocar(" in todo)
    checar("M4 transição entre telas", 3,
           "change_scene" in todo and "fade" in todo.lower(),
           "fade abertura→título→jogo, fase D")

    print("== LOJA (15) ==")
    preset = ler(f"{JOGO}/export_presets.cfg")
    mt = re.search(r"target_sdk=(\d+)", preset)
    checar(f"L1 target_sdk atual ({mt.group(1) if mt else '?'})", 4,
           bool(mt and int(mt.group(1)) >= 36), "fase A (upgrade)")
    checar("L2 política de privacidade no ar", 3,
           existe(f"{SITE}/privacidade.html"))
    checar("L3 app-ads.txt", 2, existe(f"{SITE}/app-ads.txt"))
    checar("L4 AdMob pronto (UMP + plugin + App ID de teste)", 3,
           "load_consent_form" in ler(f"{JOGO}/anuncios.gd")
           and "res://addons/admob/plugin.cfg" in proj
           and ("general/android/app_id=" not in proj
                or 'general/android/app_id="ca-app-pub-3940256099942544~3347511713"' in proj),
           "anuncios.gd + [editor_plugins] + [admob] sem ID estranho")
    mv = re.search(r'version/name="([^"]+)"', preset)
    checar("L5 versão pública (não codinome)", 1,
           bool(mv and not mv.group(1).startswith("C.")),
           "decisão do dono (0.x ou 1.0)")
    checar("L6 exporta AAB", 2, "export_format=1" in preset, "fase A")

    print(f"\nAUDITOR-100: {pontos}/100 — {len(falhas)} itens a corrigir")
    for f in falhas:
        print(f"  · {f}")
    return 0 if pontos == 100 else 1


if __name__ == "__main__":
    sys.exit(main())
