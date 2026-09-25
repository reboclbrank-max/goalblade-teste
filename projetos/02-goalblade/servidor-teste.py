#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Servidor de teste do GOALBLADE (24/09/2026, versão 5).
Sobe o jogo web + a pasta de divulgação do Ceifalume + a pasta do .exe de PC.
Guardado DENTRO do repositório de propósito: o /tmp é apagado entre as sessões do
assistente e antes isto vivia lá (e sumia toda vez).

Uso:  python3 servidor-teste.py [porta]        (padrão 8412)
   /            -> jogo web (projetos/02-goalblade/jogo/export/web)
   /div/<arq>   -> arquivos de divulgação do Ceifalume (projetos/01-ceifalume/divulgacao)
   /pc/<arq>    -> executável do PC (/tmp/pc, se existir)
"""
import http.server, socketserver, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))          # .../projetos/02-goalblade
WEB = os.path.join(BASE, "jogo", "export", "web")
DIV = os.path.abspath(os.path.join(BASE, "..", "01-ceifalume", "divulgacao"))
PC = "/tmp/pc"
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8412


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        rota = self.path.split("?")[0]
        if rota.startswith("/div/"):
            return self._servir(DIV, rota[5:])
        if rota.startswith("/pc/"):
            return self._servir(PC, rota[4:])
        return self._servir(WEB, rota.lstrip("/") or "index.html")

    def _servir(self, raiz, rel):
        rel = rel.replace("..", "")
        cam = os.path.join(raiz, rel)
        if not os.path.isfile(cam):
            self.send_error(404, "nao encontrado: " + rel)
            return
        tipo = self.guess_type(cam)
        with open(cam, "rb") as f:
            dados = f.read()
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        # sem cache: o dono sempre pega a versão nova quando recarrega
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.end_headers()
        self.wfile.write(dados)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args), flush=True)


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print("jogo web :", WEB, "(existe)" if os.path.isdir(WEB) else "(FALTA!)")
    print("divulgação:", DIV, "(existe)" if os.path.isdir(DIV) else "(FALTA!)")
    print("PC       :", PC, "(existe)" if os.path.isdir(PC) else "(vazio — .exe não exportado)")
    print(f"ouvindo em 0.0.0.0:{PORTA}")
    Servidor(("0.0.0.0", PORTA), Handler).serve_forever()
