#!/bin/bash
set -e
FERR=~/.cache/ferramentas
mkdir -p "$FERR"
cd "$FERR"
echo "[$(date +%T)] baixando godot 4.5.2 (137 MB)"
curl -sSL --retry 3 -o godot.zip https://github.com/godotengine/godot/releases/download/4.5.2-stable/Godot_v4.5.2-stable_linux.x86_64.zip
unzip -oq godot.zip && mv -f Godot_v4.5.2-stable_linux.x86_64 godot && chmod +x godot
echo "[$(date +%T)] godot pronto: $(./godot --version 2>/dev/null | tail -1)"
echo "[$(date +%T)] baixando export templates (1350 MB) - isso demora"
curl -sSL --retry 3 -o templates.tpz https://github.com/godotengine/godot/releases/download/4.5.2-stable/Godot_v4.5.2-stable_export_templates.tpz
echo "[$(date +%T)] download concluído: $(stat -c%s templates.tpz) bytes"
mkdir -p ~/.local/share/godot/export_templates/4.5.2.stable
unzip -oq -j templates.tpz "templates/web_*" "templates/version.txt" -d ~/.local/share/godot/export_templates/4.5.2.stable/
rm -f templates.tpz
echo "[$(date +%T)] templates web:"
ls -la ~/.local/share/godot/export_templates/4.5.2.stable/ | tail -6
echo "PRONTO"
