#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOTOR DE AUDITORIA — as verificações (v0.1, 24/09/2026).

Cada função olha uma parte do projeto e devolve uma lista de achados. Achado é sempre:
    {id, nivel, titulo, detalhe, onde, correcao, peso}
  · id      = nome curto e estável (serve para saber se o mesmo problema volta)
  · nivel   = "erro" (quebrado) · "aviso" (pode dar problema) · "nota" (só informa)
  · peso    = quanto isso tira da nota de saúde (0 para nota)

Regra do motor: **achado sem correção escrita não entra** — o valor está em dizer o que fazer.
"""
import ast
import glob
import hashlib
import json
import os
import re
import struct
import subprocess
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# --------------------------------------------------------------------------- utilidades
def achado(i, nivel, titulo, detalhe, onde, correcao, peso):
    return {"id": i, "nivel": nivel, "titulo": titulo, "detalhe": detalhe,
            "onde": onde, "correcao": correcao, "peso": peso}


def rel(caminho):
    return os.path.relpath(caminho, RAIZ)


def ler(caminho, limite=400000):
    try:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            return f.read(limite)
    except Exception:
        return ""


def lista(exts, pastas=None):
    pastas = pastas or [RAIZ]
    saida = []
    for base in pastas:
        for raiz, dirs, arqs in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", ".godot", "__pycache__", "node_modules")]
            for a in arqs:
                if a.endswith(tuple(exts)):
                    saida.append(os.path.join(raiz, a))
    return sorted(saida)


# --------------------------------------------------------------------------- 1 python
def python_sintaxe():
    out = []
    for f in lista([".py"]):
        try:
            ast.parse(ler(f))
        except SyntaxError as e:
            out.append(achado("python.sintaxe", "erro", "Script Python com erro de sintaxe",
                              "linha %s: %s" % (e.lineno, e.msg), rel(f),
                              "abrir o arquivo na linha indicada e corrigir", 15))
    if not out:
        out.append(achado("python.sintaxe", "nota", "Scripts Python: sintaxe ok",
                          "%d arquivos conferidos" % len(lista([".py"])), "ferramentas/ · projetos/", "—", 0))
    return out


# --------------------------------------------------------------------------- 2 gdscript
def _sem_textos(codigo):
    """Tira comentários e textos entre aspas — senão um parêntese escrito numa frase vira 'erro'."""
    codigo = re.sub(r'#.*', '', codigo)
    codigo = re.sub(r'"""(?:.|\n)*?"""', '""', codigo)
    codigo = re.sub(r'"(?:\\.|[^"\\])*"', '""', codigo)
    codigo = re.sub(r"'(?:\\.|[^'\\])*'", "''", codigo)
    return codigo


def gdscript_estrutura():
    out = []
    for f in lista([".gd"]):
        s = _sem_textos(ler(f))
        nome = rel(f)
        for ab, fe, rot in (("(", ")", "parênteses"), ("{", "}", "chaves"), ("[", "]", "colchetes")):
            if s.count(ab) != s.count(fe):
                out.append(achado("gdscript.balanco", "erro", "Falta fechar %s" % rot,
                                  "%d abre e %d fecha" % (s.count(ab), s.count(fe)), nome,
                                  "conferir a função citada no fim do arquivo", 15))
        if re.search(r"^\t* {1,}\S", s, re.M):
            out.append(achado("gdscript.identacao", "aviso", "Linhas com espaço no meio de tabs",
                              "o Godot aceita, mas misturar tabulação e espaço esconde erro", nome,
                              "usar a formatação automática do editor do Godot", 2))
    if not out:
        out.append(achado("gdscript.estrutura", "nota", "GDScript: estrutura ok",
                          "%d scripts conferidos" % len(lista([".gd"])), "projetos/02-goalblade/jogo", "—", 0))
    return out


# --------------------------------------------------------------------------- 3 segredos
def segredos():
    out = []
    padroes = {
        "ghp_": "token do GitHub",
        "api_key": "chave de API em texto",
        "THA": None,                     # marcador do Threads (tratado abaixo)
    }
    perigosos = [("ghp_[A-Za-z0-9]{20,}", "token do GitHub"),
                 ("sk-[A-Za-z0-9]{20,}", "chave secreta"),
                 ("AAAAAAAAAA[A-Za-z0-9_-]{20,}", "chave longa suspeita")]
    for f in lista([".py", ".gd", ".js", ".html", ".json"]):
        s = ler(f)
        for pad, nome in perigosos:
            if re.search(pad, s):
                out.append(achado("segredos.codigo", "erro", "%s dentro de código" % nome,
                                  "credencial em arquivo de código (não deveria ter nenhuma)", rel(f),
                                  "mover para ferramentas/chaves.md e apagar do código", 20))
    # .gitignore cobre o quê?
    gi = ler(os.path.join(RAIZ, ".gitignore"))
    for item in ("tools",):
        if item not in gi:
            out.append(achado("segredos.gitignore", "aviso", "Cópia viva de credencial fora do .gitignore",
                              "o arquivo/pasta '%s' pode entrar num commit por engano" % item, ".gitignore",
                              "acrescentar a linha ao .gitignore", 4))
    if not out:
        out.append(achado("segredos.ok", "nota", "Segredos: nada em código",
                          "credenciais ficam só em ferramentas/chaves.md (cofre do dono)", "—", "—", 0))
    return out


# --------------------------------------------------------------------------- 4 links
def links(limite=14, tempo=6):
    out = []
    vistos = {}
    for f in lista([".md"], [os.path.join(RAIZ, "projetos"), os.path.join(RAIZ, "empresa"),
                             os.path.join(RAIZ, "ferramentas")]):
        for u in re.findall(r"https?://[^\s\)\]\"'<>]+", ler(f)):
            u = u.rstrip(".,;:")
            vistos.setdefault(u, rel(f))
    quebrados, testados = [], 0
    for u, onde in vistos.items():
        if "trycloudflare.com" in u:
            quebrados.append((u, onde, "link de túnel (morre quando o ambiente reinicia)"))
            continue
        if testados >= limite:
            continue
        testados += 1
        try:
            pedido = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(pedido, timeout=tempo) as r:
                if r.status >= 400:
                    quebrados.append((u, onde, "HTTP %d" % r.status))
        except Exception as e:
            cod = getattr(e, "code", None)
            if cod is None:
                quebrados.append((u, onde, "sem resposta: %s" % str(e)[:60]))
            elif cod >= 400:
                quebrados.append((u, onde, "HTTP %d" % cod))
    for u, onde, por in quebrados:
        nivel = "erro" if "túnel" in por else "aviso"
        out.append(achado("links.quebrado", nivel, "Link que não responde",
                          "%s (%s)" % (u, por), onde,
                          "trocar por link fixo (GitHub Pages) ou atualizar o endereço", 8 if nivel == "erro" else 3))
    if not out:
        out.append(achado("links.ok", "nota", "Links: %d conferidos, todos respondem" % testados, "—", "—", "—", 0))
    return out


# --------------------------------------------------------------------------- 5 imagens
def imagens():
    out = []
    for f in lista([".png"]):
        try:
            with open(f, "rb") as fh:
                cab = fh.read(24)
            if cab[:8] != b"\x89PNG\r\n\x1a\n":
                raise ValueError("não é PNG")
            w, h = struct.unpack(">II", cab[16:24])
            if w == 0 or h == 0:
                raise ValueError("tamanho zero")
            tam = os.path.getsize(f)
            if tam < 300:
                out.append(achado("imagem.suspeita", "aviso", "Imagem boa demais para ser verdade",
                                  "%d bytes (parece vazia)" % tam, rel(f), "gerar de novo", 2))
        except Exception as e:
            out.append(achado("imagem.ilegivel", "erro", "Imagem que não abre",
                              str(e)[:80], rel(f), "gerar de novo com o motor de arte", 10))
    if not out:
        out.append(achado("imagem.ok", "nota", "Imagens: %d arquivos legíveis" % len(lista([".png"])),
                          "todas com cabeçalho PNG válido", "—", "—", 0))
    return out


# --------------------------------------------------------------------------- 6 desempenho (GoalBlade)
def desempenho_godot():
    out = []
    jogo = os.path.join(RAIZ, "projetos", "02-goalblade", "jogo")
    proj = ler(os.path.join(jogo, "project.godot"))
    if not proj:
        return [achado("godot.ausente", "erro", "Projeto Godot não encontrado", jogo, jogo, "conferir a pasta", 10)]
    if "allow_hidpi=false" not in proj:
        out.append(achado("godot.hidpi", "erro", "Desenho na resolução física da tela ligado",
                          "num celular isso é ~3x mais pixels por quadro (foi a causa do travamento)", "jogo/project.godot",
                          "acrescentar window/dpi/allow_hidpi=false", 12))
    js = ler(os.path.join(jogo, "scripts", "jogo.gd"))
    if "Engine.max_fps" not in js:
        out.append(achado("godot.teto_fps", "aviso", "Sem teto de quadros por segundo",
                          "tela de 90/120 Hz desenha o dobro à toa", "scripts/jogo.gd",
                          "Engine.max_fps = 60 no _ready()", 6))
    if "_vigiar_desempenho" not in js:
        out.append(achado("godot.sem_leve", "aviso", "Sem ajuste automático de qualidade",
                          "se o aparelho não aguentar, o jogo fica travado sem plano B", "scripts/jogo.gd",
                          "ligar o MODO LEVE (vigiar fps e reduzir a resolução de desenho)", 6))
    if "content_scale_factor" in js and "reposicionar()" not in js:
        out.append(achado("godot.reposicionar", "aviso", "Mudar a escala sem reposicionar os controles",
                          "foi exatamente isso que deixou START/CHUTE fora de lugar", "scripts/jogo.gd",
                          "chamar hud._layout() e controles.reposicionar() depois de mudar a escala", 6))
    tex = ler(os.path.join(jogo, "scripts", "consts.gd"))
    m = re.search(r"TEX_W\s*:=\s*([0-9.]+)", tex)
    if m and float(m.group(1)) > 1400:
        out.append(achado("godot.campo_grande", "aviso", "Imagem do campo maior que o necessário",
                          "TEX_W = %s (o teste mostrou que 1280 basta)" % m.group(1), "scripts/consts.gd",
                          "baixar TEX_W para 1280", 4))
    web = os.path.join(jogo, "export", "web")
    pck = os.path.join(web, "index.pck")
    if os.path.isfile(pck):
        kb = os.path.getsize(pck) / 1024.0
        # o teto é o peso real do jogo no ar: o GoalBlade carrega a folha de sprites da arte
        # (818 KB em paleta de 256 cores), então 1,4 MB de pacote é o esperado. Acima de 3 MB
        # é sinal de arquivo que entrou no export sem precisar.
        if kb > 3000:
            out.append(achado("godot.pck_grande", "aviso", "Build com arquivo grande",
                              "index.pck = %.0f KB" % kb, rel(pck), "varrer arquivos que não são usados no export", 3))
    if not out:
        out.append(achado("godot.ok", "nota", "GoalBlade: desempenho em ordem",
                          "resolução lógica, teto de 60 fps, modo leve e reposicionamento presentes",
                          "projetos/02-goalblade/jogo", "—", 0))
    return out


# --------------------------------------------------------------------------- 7 marketing
def marketing(canais_exigidos=("Bluesky", "Mastodon", "Telegram", "Discord", "Tumblr", "Threads")):
    out = []
    chaves = ler(os.path.join(RAIZ, "ferramentas", "chaves.md"))
    faltando = [c for c in canais_exigidos if c.lower() not in chaves.lower()]
    if faltando:
        out.append(achado("marketing.canal_sem_chave", "aviso", "Canal sem credencial guardada",
                          "faltam: %s" % ", ".join(faltando), "ferramentas/chaves.md",
                          "conseguir a chave com o dono e guardar no cofre", 4))
    met = ler(os.path.join(RAIZ, "projetos", "01-ceifalume", "marketing", "METRICAS.md"))
    linhas = [l for l in met.splitlines() if l.strip().startswith("|")]
    if len(linhas) < 3:
        out.append(achado("marketing.metricas_vazias", "erro", "Histórico de métricas vazio",
                          "sem isso não dá para dizer se está crescendo", "marketing/METRICAS.md",
                          "rodar ferramentas/medir-marketing.py", 8))
    else:
        ult, pen = linhas[-1], linhas[-2]
        try:
            v_ult = [int(x) for x in re.findall(r"\b(\d+)\b", ult) if len(x) < 7]
            v_pen = [int(x) for x in re.findall(r"\b(\d+)\b", pen) if len(x) < 7]
            if len(v_ult) >= 4 and len(v_pen) >= 4:
                if v_ult[0] == v_pen[0] and v_ult[1] == v_pen[1]:
                    out.append(achado("marketing.parado", "aviso", "Views/downloads sem mudança",
                                      "itch views %d → %d, downloads %d → %d (semana sem movimento?)"
                                      % (v_pen[0], v_ult[0], v_pen[1], v_ult[1]), "marketing/METRICAS.md",
                                      "subir conteúdo novo (vídeo/GIF) e revisar o Reddit", 3))
        except Exception:
            pass
    fb = os.path.join(RAIZ, "projetos", "01-ceifalume", "FEEDBACK-0.1.md")
    if not os.path.isfile(fb):
        out.append(achado("marketing.sem_feedback", "erro", "Caderno de feedback inexistente",
                          "as opiniões dos jogadores não têm onde ser registradas", "projetos/01-ceifalume",
                          "criar FEEDBACK-0.1.md", 8))
    if not out:
        out.append(achado("marketing.ok", "nota", "Marketing: canais e medição em ordem",
                          "6 canais com credencial, métricas e caderno de feedback presentes", "—", "—", 0))
    return out


# --------------------------------------------------------------------------- 8 consistência
def _existe_em_algum_lugar(relativo):
    alvo = os.path.basename(relativo)
    for raiz, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in (".git", ".godot", "__pycache__")]
        if alvo in arqs:
            return True
    return False


def consistencia():
    out = []
    # (a) arquivos que os documentos citam e não existem — agrupado por arquivo citado
    faltando = {}
    for f in lista([".md"], [os.path.join(RAIZ, "empresa"), os.path.join(RAIZ, "projetos"),
                             os.path.join(RAIZ, "ferramentas")]):
        if os.path.basename(f) in ("RELATORIO-AUDITORIA.md", "MELHORIAS.md"):
            continue                      # o auditor não audita o próprio relatório
        s = ler(f)
        for cam in re.findall(r"`([\w\-/\.]+\.(?:md|py|gd|sh|json|png))`", s):
            if cam.startswith("http") or "/" not in cam:
                continue
            if cam.startswith("/tmp") or cam.startswith("tmp/"):
                continue                  # caminhos antigos de /tmp: registro histórico, não arquivo do projeto
            possiveis = [os.path.join(RAIZ, cam), os.path.join(os.path.dirname(f), cam),
                         os.path.join(RAIZ, "projetos", "02-goalblade", cam),
                         os.path.join(RAIZ, "projetos", "01-ceifalume", cam)]
            if not any(os.path.exists(pp) for pp in possiveis) and not _existe_em_algum_lugar(cam):
                d = faltando.setdefault(cam, set())
                d.add(rel(f))
    for cam, onde in sorted(faltando.items()):
        out.append(achado("consistencia.arquivo_citado", "aviso", "Documento cita arquivo que não existe",
                          "`%s` é citado em %d documento(s): %s" % (cam, len(onde), ", ".join(sorted(onde)[:3])),
                          sorted(onde)[0], "criar o arquivo citado ou corrigir o texto", 2))
    # (b) mesmo nome de arquivo em lugares diferentes com conteúdo diferente
    vistos = {}
    for f in lista([".py", ".gd", ".md", ".sh"]):
        chave = os.path.basename(f)
        h = hashlib.md5(open(f, "rb").read()).hexdigest()
        vistos.setdefault(chave, []).append((rel(f), h))
    for nome, itens in sorted(vistos.items()):
        if len({h for _, h in itens}) > 1 and len(itens) > 1:
            caminhos = [p for p, _ in itens]
            projetos = {p.split("projetos/")[1].split("/")[0] for p in caminhos if "projetos/" in p}
            if len(projetos) > 1 or all(any(seg in p for seg in ("site/", "export/")) for p in caminhos):
                continue                      # mesmo nome em projetos diferentes: é esperado
            out.append(achado("consistencia.duplicado", "aviso", "Mesmo nome de arquivo, conteúdo diferente",
                              "%s aparece em %d lugares com textos diferentes" % (nome, len(caminhos)),
                              ", ".join(caminhos[:3]), "escolher um dono para o arquivo (um fato, um lugar)", 3))
    if not out:
        out.append(achado("consistencia.ok", "nota", "Consistência: nenhuma citação quebrada",
                          "documentos apontam para arquivos que existem", "—", "—", 0))
    return out


# --------------------------------------------------------------------------- 9 repositório
def repositorio():
    out = []

    def git(*args):
        try:
            return subprocess.run(["git"] + list(args), cwd=RAIZ, capture_output=True, text=True,
                                  timeout=60).stdout.strip()
        except Exception:
            return ""

    if not git("rev-parse", "--is-inside-work-tree"):
        return [achado("repo.ausente", "erro", "Não é um repositório git", RAIZ, RAIZ, "conferir a pasta", 10)]
    sujo = git("status", "--porcelain")
    if sujo:
        out.append(achado("repo.nao_salvo", "erro", "Alterações não salvas no repositório",
                          "%d arquivo(s) sem commit: %s" % (len(sujo.splitlines()),
                                                            ", ".join(l[3:] for l in sujo.splitlines()[:4])), "—",
                          "commit + push (e informar o hash ao dono)", 12))
    head = git("rev-parse", "HEAD")
    remoto = git("ls-remote", "origin", "main").split()
    if remoto and head and remoto[0] != head:
        out.append(achado("repo.fora_de_sincronia", "erro", "Repositório local diferente do remoto",
                          "local %s · remoto %s" % (head[:8], remoto[0][:8]), "—", "fazer o push", 12))
    if not os.path.isfile(os.path.join(RAIZ, ".gitignore")):
        out.append(achado("repo.sem_gitignore", "aviso", "Sem .gitignore", "risco de subir lixo", "—",
                          "criar .gitignore", 3))
    if not out:
        out.append(achado("repo.ok", "nota", "Repositório: tudo salvo e sincronizado",
                          "HEAD %s" % head[:8], "—", "—", 0))
    return out


# --------------------------------------------------------------------------- 10 rotina
def rotina():
    out = []
    guia = ler(os.path.join(RAIZ, "guia-do-proximo-chat.md"))
    if "threads-token.py" not in guia:
        out.append(achado("rotina.threads_token", "aviso", "Rotina sem o zelador do acesso do Threads",
                          "o acesso pode vencer sem ninguém perceber", "guia-do-proximo-chat.md",
                          "registrar: rodar ferramentas/threads-token.py em toda rodada", 4))
    cal = ler(os.path.join(RAIZ, "empresa", "CALENDARIO-TRABALHE.md"))
    if cal and "threads-token" not in cal:
        out.append(achado("rotina.calendario", "nota", "Calendário não cita o zelador do Threads",
                          "a renovação automática depende de o dia ter rodada", "empresa/CALENDARIO-TRABALHE.md",
                          "acrescentar a renovação na rotina", 1))
    pend = ler(os.path.join(RAIZ, "pendencias.md"))
    if len(pend) < 400:
        out.append(achado("rotina.pendencias", "aviso", "Painel de pendências curto demais",
                          "%d caracteres" % len(pend), "pendencias.md",
                          "atualizar o painel com o estado do dia", 3))
    if not out:
        out.append(achado("rotina.ok", "nota", "Rotina: registrada e atualizada",
                          "zelador do Threads e painel de pendências em ordem", "—", "—", 0))
    return out


# --------------------------------------------------------------------------- todas
def todas(incluir_links=True):
    achados = []
    for fn in (python_sintaxe, gdscript_estrutura, segredos, imagens, desempenho_godot, marketing,
               consistencia, repositorio, rotina):
        try:
            achados += fn()
        except Exception as e:
            achados.append(achado("auditoria.falha_verificacao", "nota", "Verificação não rodou",
                                  "%s: %s" % (fn.__name__, str(e)[:90]), "—", "conferir essa verificação", 0))
    if incluir_links:
        try:
            achados += links()
        except Exception as e:
            achados.append(achado("auditoria.falha_links", "nota", "Verificação de links não rodou",
                                  str(e)[:90], "—", "—", 0))
    return achados
