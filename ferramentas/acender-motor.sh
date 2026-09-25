#!/usr/bin/env bash
# acender-motor.sh — religa o ambiente de verificação do zero.
# Por que existe: o sandbox só preserva /home/user entre turnos. Medido em
# 2026-09-15: chromium, node, ffmpeg, ripgrep, sqlite3, time, xvfb-run, o binário do
# Godot (~/.cache) e os export templates (~/.local) aparecem como PERDIDOS no turno
# seguinte; sobreviveram apenas ImageMagick (`compare`) e o Pillow do python.
# Rodar 1x por chat novo (ou 1x por turno, se precisar de navegador/vídeo).
# Motor padrão: 4.5.2 desde C.16 (4.3 aposentado: sem 16KB, sem target 36).
set -u
# Depois da virada de turno o XDG_RUNTIME_DIR apontado pelo ambiente pode não existir,
# e aí o xvfb-run morre com "X11 Display is not available" (visto em 2026-09-15).
export XDG_RUNTIME_DIR=/home/user/.cache/xdg
mkdir -p "$XDG_RUNTIME_DIR" && chmod 700 "$XDG_RUNTIME_DIR"
# /tmp é tmpfs de ~1 GB e costuma chegar cheio: nada de download grande ali.
rm -f /tmp/templates.tpz 2>/dev/null || true
echo "[$(date +%T)] apt (xvfb, chromium, ffmpeg, rg, tesseract, sqlite3, time…)"
sudo apt-get update -q >/dev/null 2>&1
sudo apt-get install -y -q xvfb mesa-utils libgl1 libglu1-mesa fonts-dejavu-core \
  chromium fonts-liberation ripgrep fd-find ffmpeg time jq sqlite3 imagemagick \
  tesseract-ocr tesseract-ocr-por moreutils rsync >/dev/null 2>&1
echo "[$(date +%T)] binário do Godot 4.5.2 (137 MB) — já deixa rodar bancada e simulação"
FERR=/home/user/.cache/ferramentas; mkdir -p "$FERR"; cd "$FERR"
if [ ! -x ./godot ]; then
  curl -sSL --retry 3 -o godot.zip https://github.com/godotengine/godot/releases/download/4.5.2-stable/Godot_v4.5.2-stable_linux.x86_64.zip
  unzip -oq godot.zip && mv -f Godot_v4.5.2-stable_linux.x86_64 godot && chmod +x godot && rm -f godot.zip
fi
echo "[$(date +%T)] godot: $(./godot --version 2>/dev/null | tail -1)"
echo "[$(date +%T)] puppeteer-core (medição no navegador)"
cd /home/user/tools && (npm i puppeteer-core@23 >/dev/null 2>&1 || true)
echo "[$(date +%T)] índice da base (busca instantânea na memória oficial)"
python3 /home/user/tools/indexar-base.py 2>/dev/null || true
echo "[$(date +%T)] templates de export Web 4.5 (~1 GB no .tpz; só necessário para publicar)"
if [ ! -f /home/user/.local/share/godot/export_templates/4.5.2.stable/web_nothreads_release.zip ]; then
  mkdir -p ~/.local/share/godot/export_templates/4.5.2.stable; cd "$FERR"   # /tmp é tmpfs de ~1 GB: download grande ali estoura (visto)
  curl -sSL --retry 3 -o templates.tpz https://github.com/godotengine/godot/releases/download/4.5.2-stable/Godot_v4.5.2-stable_export_templates.tpz
  unzip -oq -j templates.tpz "templates/web_*" "templates/version.txt" -d ~/.local/share/godot/export_templates/4.5.2.stable/ && rm -f templates.tpz || echo "  AVISO: .tpz inválido/incompleto — apague $FERR/templates.tpz e rode de novo"
fi
ls -la ~/.local/share/godot/export_templates/4.5.2.stable/ 2>/dev/null | tail -4
# .git/config NÃO entra no snapshot preservado: os repositórios acordam sem remoto e
# um "git push" vira "unable to access 'https:///'" (visto em 2026-09-15). Religando:
for r in base ceifalume site; do
  if [ -d "/home/user/$r/.git" ] && ! git -C "/home/user/$r" remote get-url origin >/dev/null 2>&1; then
    git -C "/home/user/$r" remote add origin "https://github.com/reboclbrank-max/$r.git"
    echo "[$(date +%T)] remoto religado em $r"
  fi
done
# A chave mora em ~/.chave-github (fora dos repos, chmod 600, nunca em commit):
# restaura a autenticação sem pedir nada ao dono (pedido dele, 2026-09-15).
if [ -f /home/user/.chave-github ]; then
  git config --global credential.helper "store --file /home/user/.credenciais-git"
  printf 'https://x-access-token:%s@github.com\n' "$(cat /home/user/.chave-github)" > /home/user/.credenciais-git
  chmod 600 /home/user/.credenciais-git
  echo "[$(date +%T)] git autenticado pela chave guardada"
fi
echo "PRONTO $(date +%T)"
