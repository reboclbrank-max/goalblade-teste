#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# GOALBLADE — recria as ferramentas do motor em qualquer computador/sessão.
#
# Por que isto existe: o ambiente de trabalho do assistente é reiniciado entre
# as sessões e as pastas temporárias (~/.cache, ~/.local, /tmp) NÃO são guardadas.
# Em vez de baixar o pacote oficial inteiro (1,2 GB), este script baixa SÓ o que
# precisa, direto de dentro do pacote, usando pedaços do arquivo (requisições
# HTTP por faixa). Assim a recriação leva ~1 minuto em vez de ~10.
#
# Uso:   bash recriar-motor.sh            (só navegador: ~90 MB)
#        bash recriar-motor.sh pc         (navegador + PC: +182 MB)
# ---------------------------------------------------------------------------
set -e

VERSAO="4.7.2-stable"
DEST_MOTOR="/tmp/godot"
DEST_TEMPLATES="$HOME/.local/share/godot/export_templates/4.7.2.stable"
BASE_URL="https://github.com/godotengine/godot/releases/download/${VERSAO}"

mkdir -p "$DEST_TEMPLATES"

# 1) o motor (editor) -------------------------------------------------------
if [ ! -x "$DEST_MOTOR" ]; then
  echo "== baixando o Godot ${VERSAO} =="
  curl -sL -o /tmp/godot.zip "${BASE_URL}/Godot_v${VERSAO}_linux.x86_64.zip"
  unzip -o -q /tmp/godot.zip -d /tmp/godot_extraido
  mv /tmp/godot_extraido/* "$DEST_MOTOR"
  chmod +x "$DEST_MOTOR"
  rm -rf /tmp/godot_extraido /tmp/godot.zip
fi
echo "motor: $("$DEST_MOTOR" --version)"

# 2) modelos de exportação (só os pedaços necessários do pacote de 1,2 GB) ---
PRECISA="templates/version.txt templates/web_release.zip templates/web_debug.zip templates/web_nothreads_release.zip templates/web_nothreads_debug.zip"
if [ "$1" = "pc" ]; then
  PRECISA="$PRECISA templates/windows_release_x86_64.exe templates/linux_release.x86_64"
fi
FALTANDO=""
for m in $PRECISA; do
  nome=$(basename "$m")
  [ -f "$DEST_TEMPLATES/$nome" ] || FALTANDO="$FALTANDO $m"
done
if [ -n "$FALTANDO" ]; then
  echo "== extraindo do pacote oficial só o necessário:$FALTANDO =="
  python3 - "$BASE_URL/Godot_v${VERSAO}_export_templates.tpz" $FALTANDO <<'PY'
import sys, os, zlib, struct, urllib.request

url, membros = sys.argv[1], sys.argv[2:]
destino = os.path.expanduser("~/.local/share/godot/export_templates/4.7.2.stable")

def faixa(inicio, fim):
    pedido = urllib.request.Request(url, headers={"Range": f"bytes={inicio}-{fim}"})
    with urllib.request.urlopen(pedido) as r:
        return r.read()

info = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"))
tamanho = int(info.headers["Content-Length"])
print(f"pacote: {tamanho/1e6:.0f} MB (vou baixar só os pedaços pedidos)")

# acha o fim do diretório central (EOCD), inclusive o formato zip64
fim = faixa(tamanho - 70000, tamanho - 1)
pos = fim.rfind(b"PK\x05\x06")
if pos < 0:
    raise SystemExit("não achei o índice do pacote (EOCD)")
eocd = fim[pos:pos + 22]
total_entradas = struct.unpack("<H", eocd[10:12])[0]
tam_cd = struct.unpack("<I", eocd[12:16])[0]
pos_cd = struct.unpack("<I", eocd[16:20])[0]
if pos_cd == 0xFFFFFFFF or tam_cd == 0xFFFFFFFF or total_entradas == 0xFFFF:
    p64 = fim.rfind(b"PK\x06\x07")
    if p64 >= 0:
        pos_cd64 = struct.unpack("<Q", fim[p64 + 8:p64 + 16])[0]
        eocd64 = faixa(pos_cd64, pos_cd64 + 56)
        total_entradas = struct.unpack("<Q", eocd64[32:40])[0]
        tam_cd = struct.unpack("<Q", eocd64[40:48])[0]
        pos_cd = struct.unpack("<Q", eocd64[48:56])[0]

cd = faixa(pos_cd, pos_cd + tam_cd - 1)
i, achados = 0, 0
while i < len(cd) - 4 and cd[i:i + 4] == b"PK\x01\x02":
    metodo = struct.unpack("<H", cd[i + 10:i + 12])[0]
    tam_comp = struct.unpack("<I", cd[i + 20:i + 24])[0]
    n_nome = struct.unpack("<H", cd[i + 28:i + 30])[0]
    n_extra = struct.unpack("<H", cd[i + 30:i + 32])[0]
    n_coment = struct.unpack("<H", cd[i + 32:i + 34])[0]
    desloc = struct.unpack("<I", cd[i + 42:i + 46])[0]
    nome = cd[i + 46:i + 46 + n_nome].decode("utf-8", "replace")
    if nome in membros:
        # cabeçalho local (para saber onde começam os dados comprimidos)
        cab = faixa(desloc, desloc + 30 + 512)
        n_nome_l = struct.unpack("<H", cab[26:28])[0]
        n_extra_l = struct.unpack("<H", cab[28:30])[0]
        inicio_dados = desloc + 30 + n_nome_l + n_extra_l
        dados = faixa(inicio_dados, inicio_dados + tam_comp - 1)
        conteudo = zlib.decompress(dados, -15) if metodo == 8 else dados
        saida = os.path.join(destino, os.path.basename(nome))
        open(saida, "wb").write(conteudo)
        os.chmod(saida, 0o755)
        print(f"  ok: {os.path.basename(nome)} ({len(conteudo)/1e6:.1f} MB)")
        achados += 1
        if achados == len(membros):
            break
    i += 46 + n_nome + n_extra + n_coment
if achados < len(membros):
    raise SystemExit(f"faltou extrair: {len(membros) - achados} arquivo(s)")
PY
fi
ls -la "$DEST_TEMPLATES" | tail -5
echo "== ferramentas prontas =="
