#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zelador do acesso do Threads (24/09/2026).

A Meta NÃO dá acesso infinito: o Threads dá no máximo 60 dias. Mas dá para nunca deixar vencer:
este script testa o acesso e, quando ele já tem mais de 24 h de vida, RENOVA por mais 60 dias —
guardando o novo em `ferramentas/chaves.md` e em `~/tools/.threads.json`.

Regra de trabalho: rodar isto em TODA rodada de marketing (o calendário já é cheio de rodadas).
Se ficar mais de 60 dias sem nenhuma rodada, aí sim vence e é preciso reautorizar (1 clique do dono).

Uso:
    python3 ferramentas/threads-token.py            # testa e renova se valer a pena
    python3 ferramentas/threads-token.py --so-testar
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAVES = os.path.join(RAIZ, "ferramentas", "chaves.md")
COPIA = os.path.expanduser("~/tools/.threads.json")
SECRET = "23c98b40fd9b8f5657dc197915e69e51"


def url(rota):
    return "https://graph.threads.net/" + rota


def abrir(u):
    try:
        r = urllib.request.urlopen(u, timeout=45)
        return r.status, json.loads(r.read())
    except Exception as e:
        d = ""
        try:
            d = e.read().decode()[:220]
        except Exception:
            pass
        return getattr(e, "code", "?"), d


def token_guardado():
    if os.path.exists(COPIA):
        try:
            return json.load(open(COPIA))["token"]
        except Exception:
            pass
    s = open(CHAVES, encoding="utf-8").read()
    m = re.search(r"Token longo \(60 dias[^)]*\)[^`]*`([^`]+)`", s)
    return m.group(1) if m else None


def guardar(tok):
    os.makedirs(os.path.dirname(COPIA), exist_ok=True)
    json.dump({"token": tok, "user_id": "28974190178853073"}, open(COPIA, "w"))
    s = open(CHAVES, encoding="utf-8").read()
    s = re.sub(r"Token longo \(60 dias[^)]*\)[^`]*`[^`]+`",
               "Token longo (60 dias, renovado sozinho por `ferramentas/threads-token.py`; último em %s):** `%s`"
               % (datetime.now(timezone.utc).strftime("%d/%m/%Y"), tok), s, count=1)
    open(CHAVES, "w", encoding="utf-8").write(s)


def main():
    tok = token_guardado()
    if not tok:
        print("SEM TOKEN guardado — precisa do link de autorização (1 clique do dono).")
        return 1

    # 1) o acesso está vivo?
    st, r = abrir(url("v1.0/me?fields=id,username&access_token=" + tok))
    if st != 200:
        print("ACESSO INVÁLIDO —", r)
        print(">>> Precisa reautorizar: link em projetos/01-ceifalume/destravar-threads.md (Parte B).")
        return 1
    print("acesso vivo:", r)

    # 2) quantos dias faltam? (debug_token do Threads não expõe a data; usamos um teste de refresh)
    if "--so-testar" in sys.argv:
        print("(--so-testar: sem renovar)")
        return 0
    st2, r2 = abrir(url("access_token?grant_type=th_refresh_token&client_secret=%s&access_token=%s" % (SECRET, tok)))
    if st2 == 200 and "access_token" in r2:
        guardar(r2["access_token"])
        print("RENOVADO por mais 60 dias (válido até ~%s)" %
              datetime.fromtimestamp(datetime.now().timestamp() + r2.get("expires_in", 5183944), tz=timezone.utc).strftime("%d/%m/%Y"))
        return 0
    # A Meta só renova depois de 24 h de vida do acesso — antes disso ela responde "not supported".
    texto = str(r2)
    if "24" in texto or "not supported" in texto or "unsupported" in texto.lower():
        print("acesso recém-criado (<24 h): renova na próxima rodada. Nada a fazer. 👍")
        return 0
    print("não deu para renovar:", r2, "— o acesso atual continua valendo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
