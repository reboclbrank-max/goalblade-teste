#!/bin/sh
# ============================================================
# CEIFALUME — APK de TESTE assinado (C.17 em diante)
# Mesmo corpo do publicar-apk.sh (prova C.16), mas exporta APK
# (não AAB) com IDs de TESTE do Google: pacote .teste, versão
# 0.1-teste/code 16. As 3 trocas (preset, anuncios.gd,
# project.godot) voltam sozinhas ao final (trap) — o repo nunca
# guarda estado de teste.
# Uso: sh tools/apk-teste.sh
# Saída: ceifalume/export/android/ceifalume-teste.apk (verificado:
# apksigner, badging .teste/16/36, App ID de teste, unidade real
# AUSENTE do dex, GMA+UMP no dex, 16KB)
# ============================================================
set -e
cd /home/user
log() { echo "[$(date +%H:%M:%S)] $*"; }
erro() { echo "FALHOU: $2"; exit "$1"; }
TESTE_APP="ca-app-pub-3940256099942544~3347511713"
TESTE_UNIT="ca-app-pub-3940256099942544/5224354917"
REAL_UNIT="ca-app-pub-3680795320914851/9323689735"

# 0a. guarda das chaves (igual ao publicar)
for par in "lancamento copia-lancamento" "depuracao copia-depuracao"; do
  set -- $par; vivo="/home/user/cofre/$1"; copia="/home/user/cofre/$2"
  if [ ! -f "$vivo" ]; then
    if [ -f "$copia" ]; then cp "$copia" "$vivo"; echo "AVISO: $1 restaurado da copia!"
    else erro 3 "FALTA A CHAVE $1 (nem copia existe)"; fi
  fi
done
[ -f /home/user/.segredos-apk ] || erro 3 "sem ~/.segredos-apk"
log "chaves ok (guarda passou)"

# 0b. estado LIMPO de release exigido (as trocas de teste partem dele)
grep -q 'general/android/enabled=true' ceifalume/project.godot || erro 4 "plugin AdMob desligado em project.godot"
grep -q 'res://addons/admob/plugin.cfg' ceifalume/project.godot || erro 4 "plugin AdMob fora de [editor_plugins] (C.17c: nunca empacota sem isso)"
[ -d ceifalume/addons/admob/android ] || erro 4 "sem addons/admob"
grep -q 'gradle_build/export_format=1' ceifalume/export_presets.cfg || erro 4 "preset Android não está em AAB=1"
grep -q 'package/unique_name="com.reboclbrank.ceifalume"' ceifalume/export_presets.cfg || erro 4 "pacote release inesperado"
grep -q "$REAL_UNIT" ceifalume/anuncios.gd || erro 4 "unidade real sumiu de anuncios.gd"
git -C ceifalume status --short | grep -v "^??" | grep -q . && erro 4 "repo ceifalume sujo — commite antes"
log "estado release confirmado (repo limpo)"

# 0c. trocas de teste (python com assert; trap restaura os 3 arquivos)
restaurar_teste() { git -C ceifalume checkout -- export_presets.cfg project.godot anuncios.gd 2>/dev/null || true; }
trap restaurar_teste EXIT
python3 - "$TESTE_APP" <<'EOF'
import re, sys
p = "ceifalume/export_presets.cfg"; s = open(p).read()
trocas = [
    ("gradle_build/export_format=1", "gradle_build/export_format=0"),  # AAB -> APK
    ('export_path="export/android/ceifalume.aab"', 'export_path="export/android/ceifalume-teste.apk"'),
    ('package/unique_name="com.reboclbrank.ceifalume"', 'package/unique_name="com.reboclbrank.ceifalume.teste"'),
    ("version/code=15", "version/code=16"),
    ('version/name="0.1"', 'version/name="0.1-teste"'),
]
for velho, novo in trocas:
    assert s.count(velho) == 1, "preset sem: " + velho
    s = s.replace(velho, novo)
open(p, "w").write(s)
p = "ceifalume/anuncios.gd"; s = open(p).read()
velho = 'const ID_RECOMPENSA_REAL := "ca-app-pub-3680795320914851/9323689735"'
assert s.count(velho) == 1, "anuncios.gd sem unidade real"
open(p, "w").write(s.replace(velho, 'const ID_RECOMPENSA_REAL := ""'))
p = "ceifalume/project.godot"; s = open(p).read()
s2, n = re.subn(r'general/android/app_id="[^"]*"', 'general/android/app_id="%s"' % sys.argv[1], s)
assert n == 1, "app_id não achado em project.godot"
open(p, "w").write(s2)
print("trocas de teste aplicadas (preset+anuncios+app_id)")
EOF

# 0d. base de sempre (godot + remotos + auth git) e swap 3G
sh tools/acender-motor.sh
if ! swapon --show 2>/dev/null | grep -q /swapfile; then
  [ -f /swapfile ] || { sudo fallocate -l 3G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile >/dev/null; }
  sudo swapon /swapfile 2>/dev/null || true
fi

export JAVA_HOME=/home/user/.cache/jdk17
export ANDROID_HOME=/home/user/.cache/android-sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export GRADLE_USER_HOME=/home/user/.cache/gradle
export GRADLE_OPTS="-Xmx1024m -XX:MaxMetaspaceSize=256m"
export PATH=$JAVA_HOME/bin:$PATH
FERR=~/.cache/ferramentas

# 1. JDK 17
if [ ! -x "$JAVA_HOME/bin/java" ]; then
  mkdir -p ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o jdk17.tar.gz "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jdk/hotspot/normal/eclipse"
  mkdir -p ~/.cache/jdk17 && tar -xzf jdk17.tar.gz -C ~/.cache/jdk17 --strip-components=1
  rm -f jdk17.tar.gz
  cd /home/user
fi

# 2. Android SDK (cmdline-tools + platform 36 + build-tools 36/35 + NDK r28)
if [ ! -x "$ANDROID_HOME/build-tools/36.0.0/apksigner" ] || [ ! -d "$ANDROID_HOME/ndk/28.1.13356709" ]; then
  mkdir -p ~/.cache/dl && cd ~/.cache/dl
  if [ ! -x "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" ]; then
    curl -sSL --retry 3 -o cmdtools.zip "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
    mkdir -p $ANDROID_HOME/cmdline-tools
    unzip -oq cmdtools.zip -d $ANDROID_HOME/cmdline-tools/
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest
    rm -f cmdtools.zip
  fi
  export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
  yes 2>/dev/null | sdkmanager --licenses >/dev/null 2>&1
  sdkmanager "platform-tools" "platforms;android-36" "build-tools;36.0.0" "build-tools;35.0.1" "ndk;28.1.13356709" >/dev/null 2>&1
  cd /home/user
fi
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/build-tools/36.0.0:$PATH

# 3. templates Android do Godot 4.5.2
TDIR=~/.local/share/godot/export_templates/4.5.2.stable
if [ ! -f "$TDIR/android_release.apk" ]; then
  mkdir -p $TDIR ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o templates.tpz https://github.com/godotengine/godot/releases/download/4.5.2-stable/Godot_v4.5.2-stable_export_templates.tpz
  mkdir -p ../x && unzip -oq templates.tpz "templates/android_*" "templates/version.txt" -d ../x/
  cp ../x/templates/* $TDIR/ && rm -rf ../x templates.tpz
  cd /home/user
fi

# 4. plugin AdMob (pinado: editor v5.1.0 + nativo 4.5.2)
if ! grep -q 'version="5.1.0"' ceifalume/addons/admob/plugin.cfg 2>/dev/null; then
  mkdir -p ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o admob-p.zip https://github.com/poingstudios/godot-admob-plugin/releases/download/v5.1.0/poing-godot-admob-v5.1.0.zip
  rm -rf stage-p && unzip -oq admob-p.zip "poing-godot-admob/addons/*" -d stage-p
  rm -rf /home/user/ceifalume/addons/admob
  mkdir -p /home/user/ceifalume/addons
  cp -r stage-p/poing-godot-admob/addons/admob /home/user/ceifalume/addons/admob
  rm -rf stage-p admob-p.zip
  cd /home/user
fi
if [ ! -f ceifalume/addons/admob/android/bin/package.gd ]; then
  mkdir -p ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o admob-d.zip "https://github.com/poingstudios/godot-admob-plugin/releases/download/v5.1.0/android-template-v4.5.2.zip"
  mkdir -p /home/user/ceifalume/addons/admob/android/bin
  unzip -oq admob-d.zip -d /home/user/ceifalume/addons/admob/android/bin/
  rm -f admob-d.zip
  cd /home/user
fi

# 5. template de build + compileSdk 36 + .build_version
if [ ! -f ceifalume/android/build/AndroidManifest.xml ]; then
  mkdir -p ceifalume/android/build
  unzip -oq $TDIR/android_source.zip -d ceifalume/android/build/
  touch ceifalume/android/build/.gdignore
fi
printf '4.5.2.stable\n' > ceifalume/android/.build_version
sed -i 's/compileSdk *: *35/compileSdk : 36/' ceifalume/android/build/config.gradle
grep -q 'compileSdk *: *36' ceifalume/android/build/config.gradle || erro 4 "compileSdk não subiu"

# 6. senha do keystore (mora no .godot, gitignored — nunca no preset)
. /home/user/.segredos-apk
printf '[preset.1.options]\nkeystore/release_password="%s"\n' "$STOREPASS" > ceifalume/.godot/export_credentials.cfg

# 7. editor settings (SDK + Java) + gradle magro
ES=~/.config/godot/editor_settings-4.5.tres
for par in 'export/android/android_sdk_path = "/home/user/.cache/android-sdk"' 'export/android/java_sdk_path = "/home/user/.cache/jdk17"'; do
  chave=$(echo "$par" | cut -d= -f1 | sed 's/ *$//')
  if grep -q "^${chave} =" $ES 2>/dev/null; then
    sed -i "s|^${chave} =.*|${par}|" $ES
  else
    echo "$par" >> $ES
  fi
done
mkdir -p $GRADLE_USER_HOME
printf 'org.gradle.daemon=false\norg.gradle.workers.max=1\norg.gradle.parallel=false\norg.gradle.caching=false\nkotlin.compiler.execution.strategy=in-process\nandroid.useAndroidX=true\n' > $GRADLE_USER_HOME/gradle.properties

# 8. importa + régua rápida + exporta APK
G=$FERR/godot
$G --headless --path ceifalume --import 2>&1 | grep -iE '^(ERROR|SCRIPT ERROR)|Failed to' | head -n 4
$G --headless --path ceifalume --script res://teste_anuncios.gd 2>&1 | grep -E "TESTE_ANUNCIOS"
mkdir -p ceifalume/export/android
$G --headless --path ceifalume --export-release "Android" export/android/ceifalume-teste.apk

# 9. verifica o APK
A=ceifalume/export/android/ceifalume-teste.apk
[ -f "$A" ] || erro 4 "APK não gerado"
BT=$ANDROID_HOME/build-tools/36.0.0
log "--- apksigner ---"
$BT/apksigner verify "$A" || erro 4 "apksigner reprovou a assinatura"
$BT/apksigner verify --print-certs "$A" 2>&1 | grep -E "certificate (DN|SHA-256)" | head -n 2
log "--- badging (pacote/versão/sdk) ---"
$BT/aapt dump badging "$A" 2>/dev/null | grep -E "^package:|^sdkVersion:|^targetSdkVersion:" | head -n 3
$BT/aapt dump badging "$A" 2>/dev/null | grep -q "name='com.reboclbrank.ceifalume.teste' versionCode='16' versionName='0.1-teste'" || erro 4 "badging fora do esperado (.teste/16/0.1-teste)"
$BT/aapt dump badging "$A" 2>/dev/null | grep -q "targetSdkVersion:'36'" || erro 4 "targetSdk não é 36!"
log "--- App ID no manifesto (lido do binário, não do zip) ---"
$BT/aapt dump xmltree "$A" AndroidManifest.xml > /tmp/apk-manifest.txt 2>/dev/null
grep -q "APPLICATION_ID" /tmp/apk-manifest.txt || erro 4 "APPLICATION_ID fora do manifesto (plugin não empacotou?)"
grep -q "$TESTE_APP" /tmp/apk-manifest.txt || erro 4 "App ID de teste fora do manifesto"
echo "  APPLICATION_ID = teste Google: OK"
log "--- swap de unidades (no fonte: .gdc sai comprimido, sem texto) ---"
grep -q 'const ID_RECOMPENSA_REAL := ""' ceifalume/anuncios.gd || erro 4 "swap da unidade real não aplicado!"
grep -q "const ID_RECOMPENSA_TESTE := \"$TESTE_UNIT\"" ceifalume/anuncios.gd || erro 4 "unidade de TESTE sumiu do fonte!"
echo "  fonte: REAL vazia (-> usa TESTE) + TESTE intacta: OK"
log "--- nenhum ID real em texto claro no APK ---"
VAZOU=$(strings "$A" | grep -c "3680795320914851" || true)
[ "${VAZOU:-0}" = "0" ] || erro 4 "unidade REAL em texto no APK de teste!"
echo "  real ausente do binário: OK"
log "--- GMA+UMP no dex (CONTEÚDO, não nomes — C.17c) ---"
N=$(unzip -p "$A" 'classes*.dex' 2>/dev/null | strings | grep -c "com/google/android/gms/ads" || true)
[ "${N:-0}" -ge 100 ] || erro 4 "GMA fraco no dex ($N < 100)"
echo "  refs GMA no dex: $N"
unzip -p "$A" 'classes*.dex' 2>/dev/null | strings | grep -qi "ump\|consent" || erro 4 "UMP sumiu do dex!"
echo "  UMP no dex: sim"
log "--- 16KB (offsets + LOAD; zipalign -c mente em APK assinado v2) ---"
python3 - "$A" <<'EOF'
import struct, sys, zipfile
z = zipfile.ZipFile(sys.argv[1]); f = open(sys.argv[1], "rb")
n4 = n16 = n = 0
for info in z.infolist():
    if info.file_size > 0 and info.compress_type == zipfile.ZIP_STORED:
        n += 1
        f.seek(info.header_offset)
        d = struct.unpack("<IHHHHHIIIHH", f.read(30))
        dado = info.header_offset + 30 + d[9] + d[10]
        assert dado % 4 == 0, "4B desalinhado: " + info.filename
        if info.filename.endswith(".so"):
            assert dado % 16384 == 0, "16KB desalinhado: " + info.filename
            n16 += 1
print("  %d stored 4B-ok, %d .so 16KB-ok: OK" % (n, n16))
EOF
rm -rf /tmp/so16 && mkdir -p /tmp/so16
unzip -oq "$A" 'lib/arm64-v8a/*.so' -d /tmp/so16
SO16=$(ls /tmp/so16/lib/arm64-v8a/*.so | head -n 1)
readelf -lW "$SO16" | grep LOAD | awk '{print "  LOAD align:", $NF}'
RUIM=$(readelf -lW "$SO16" | grep LOAD | awk '{print $NF}' | (c=0; while read a; do [ "$(($a))" -ge 16384 ] || c=$((c+1)); done; echo $c))
[ "$RUIM" = "0" ] || erro 4 "$RUIM LOAD < 16KB"
log "--- tamanho + impressão da chave ---"
ls -la "$A"
keytool -list -v -keystore /home/user/cofre/lancamento -storepass:env STOREPASS 2>/dev/null | grep -E "SHA256|Alias" | head -n 2

# 10. limpa o monstro do gradle (snapshot) e devolve o repo ao release
rm -rf ceifalume/android/build
restaurar_teste
trap - EXIT
git -C ceifalume status --short | grep -v "^??" | grep -q . && erro 4 "repo não voltou ao limpo!"
log "repo limpo (release) — APK de teste pronto: $A"
