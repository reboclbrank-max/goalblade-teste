#!/usr/bin/env bash
# Instala o Godot 4.7.2 AO LADO do 4.3 (nada é substituído): motor novo para comparar.
# Só baixa o que este projeto usa: templates Web (libera espaço apagando o .tpz).
set -u
V=4.7.2
D=/home/user/.cache/ferramentas/novo
mkdir -p "$D"
echo "baixando engine $V…"
curl -sSL --retry 3 -o "$D/godot.zip" "https://github.com/godotengine/godot/releases/download/${V}-stable/Godot_v${V}-stable_linux.x86_64.zip" || { echo FALHOU_ENGINE; exit 1; }
unzip -o -q "$D/godot.zip" -d "$D" && rm -f "$D/godot.zip"
mv -f "$D/Godot_v${V}-stable_linux.x86_64" "$D/godot" 2>/dev/null || true
chmod +x "$D/godot"
echo "engine: $("$D/godot" --version 2>/dev/null | tail -1)"
echo "baixando templates $V (arquivo grande)…"
curl -sSL --retry 3 -o "$D/templates.tpz" "https://github.com/godotengine/godot/releases/download/${V}-stable/Godot_v${V}-stable_export_templates.tpz" || { echo FALHOU_TEMPLATES; exit 1; }
mkdir -p "$HOME/.local/share/godot/export_templates/$V.stable"
cd "$D" && unzip -o -q templates.tpz "templates/web_release.zip" "templates/web_nothreads_release.zip" -d "$D/x" \
  && cp "$D/x/templates/web_release.zip" "$D/x/templates/web_nothreads_release.zip" "$HOME/.local/share/godot/export_templates/$V.stable/" \
  && echo "$V" > "$HOME/.local/share/godot/export_templates/$V.stable/version.txt"
rm -f "$D/templates.tpz"; rm -rf "$D/x"
echo "templates:"; ls -l "$HOME/.local/share/godot/export_templates/$V.stable/" | awk '{print $5,$9}'
echo PRONTO
