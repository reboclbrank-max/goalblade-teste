#!/bin/sh
# ============================================================
# CEIFALUME — APK de LANÇAMENTO assinado (0.1, site)
# Produção de verdade: pacote com.reboclbrank.ceifalume, versão
# 0.1/code 15, IDs REAIS do AdMob (unidade no fonte + App ID de
# ~/.segredos-apk), chave de lançamento, ícone, launcher.
# As 2 trocas (preset: AAB->APK; project.godot: App ID) voltam
# sozinhas ao final (trap) — o repo nunca guarda estado de build.
# Uso: sh tools/apk-lancamento.sh
# Saída: ceifalume/export/android/ceifalume.apk (verificado:
# apksigner, badging prod/15/0.1/36, App ID REAL, LAUNCHER,
# INTERNET, ícone, GMA+UMP no dex, 16KB, zero ID de teste)
# ============================================================
set -e
cd /home/user
log() { echo "[$(date +%H:%M:%S)] $*"; }
erro() { echo "FALHOU: $2"; exit "$1"; }
TESTE_APP="ca-app-pub-3940256099942544~3347511713"
TESTE_UNIT="ca-app-pub-3940256099942544/5224354917"
REAL_UNIT="ca-app-pub-3680795320914851/9323689735"

# 0a. guarda das chaves (igual ao teste) + App ID real obrigatório
for par in "lancamento copia-lancamento" "depuracao copia-depuracao"; do
  set -- $par; vivo="/home/user/cofre/$1"; copia="/home/user/cofre/$2"
  if [ ! -f "$vivo" ]; then
    if [ -f "$copia" ]; then cp "$copia" "$vivo"; echo "AVISO: $1 restaurado da copia!"
    else erro 3 "FALTA A CHAVE $1 (nem copia existe)"; fi
  fi
done
[ -f /home/user/.segredos-apk ] || erro 3 "sem ~/.segredos-apk"
APP_ID=$(grep -E "^APP_ID=" /home/user/.segredos-apk 2>/dev/null | cut -d= -f2)
[ -n "$APP_ID" ] || erro 3 "sem APP_ID real em ~/.segredos-apk (AdMob console -> Config. do app -> ID do app)"
echo "$APP_ID" | grep -q "^ca-app-pub-3680795320914851~" || erro 3 "APP_ID fora da conta do dono"
log "chaves ok (guarda passou)"

# 0b. estado de LANÇAMENTO exigido (nada de teste, nada de dev)
grep -q 'general/android/enabled=true' ceifalume/project.godot || erro 4 "plugin AdMob desligado em project.godot"
grep -q 'res://addons/admob/plugin.cfg' ceifalume/project.godot || erro 4 "plugin AdMob fora de [editor_plugins]"
[ -d ceifalume/addons/admob/android ] || erro 4 "sem addons/admob"
grep -q 'gradle_build/export_format=1' ceifalume/export_presets.cfg || erro 4 "preset Android não está em AAB=1"
grep -q 'package/unique_name="com.reboclbrank.ceifalume"' ceifalume/export_presets.cfg || erro 4 "pacote release inesperado"
grep -q 'version/code=15' ceifalume/export_presets.cfg || erro 4 "version/code não é 15"
grep -q 'version/name="0.1"' ceifalume/export_presets.cfg || erro 4 'version/name não é 0.1'
grep -q 'package/show_as_launcher_app=true' ceifalume/export_presets.cfg || erro 4 "app sem ícone no launcher!"
grep -q 'launcher_icons/main_192x192="res://' ceifalume/export_presets.cfg || erro 4 "ícone do launcher não configurado"
grep -q "$REAL_UNIT" ceifalume/anuncios.gd || erro 4 "unidade real sumiu de anuncios.gd"
grep -q "^teste_livre=false" ceifalume/project.godot || erro 4 "painel de teste LIGADO — desligue antes de publicar"
git -C ceifalume status --short | grep -v "^??" | grep -q . && erro 4 "repo ceifalume sujo — commite antes"
log "estado lançamento confirmado (repo limpo)"

# 0c. trocas de build (python com assert; trap restaura os 2 arquivos)
restaurar_build() { git -C ceifalume checkout -- export_presets.cfg project.godot 2>/dev/null || true; }
trap restaurar_build EXIT
python3 - "$APP_ID" <<'EOF'
import re, sys
p = "ceifalume/export_presets.cfg"; s = open(p).read()
trocas = [
    ("gradle_build/export_format=1", "gradle_build/export_format=0"),  # AAB -> APK
    ('export_path="export/android/ceifalume.aab"', 'export_path="export/android/ceifalume.apk"'),
]
for velho, novo in trocas:
    assert s.count(velho) == 1, "preset sem: " + velho
    s = s.replace(velho, novo)
open(p, "w").write(s)
p = "ceifalume/project.godot"; s = open(p).read()
s2, n = re.subn(r'general/android/app_id="[^"]*"', 'general/android/app_id="%s"' % sys.argv[1], s)
assert n == 1, "app_id não achado em project.godot"
open(p, "w").write(s2)
print("trocas de lançamento aplicadas (APK + App ID real)")
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

# 8. importa + BATERIA COMPLETA + exporta APK
G=$FERR/godot
$G --headless --path ceifalume --import 2>&1 | grep -iE '^(ERROR|SCRIPT ERROR)|Failed to' | head -n 4
for t in teste_economia teste_tortura teste_save_novo teste_anuncios teste_som; do
  OUT=$($G --headless --path ceifalume --script res://$t.gd 2>&1 | grep -E "testes, |TESTE_|TORTURA" | head -n 2)
  echo "  $t: $OUT"
  echo "$OUT" | grep -q "0 falhas" || erro 4 "bateria reprovou em $t"
done
mkdir -p ceifalume/export/android
$G --headless --path ceifalume --export-release "Android" export/android/ceifalume.apk

# 9. verifica o APK
A=ceifalume/export/android/ceifalume.apk
[ -f "$A" ] || erro 4 "APK não gerado"
BT=$ANDROID_HOME/build-tools/36.0.0
log "--- apksigner ---"
$BT/apksigner verify "$A" || erro 4 "apksigner reprovou a assinatura"
$BT/apksigner verify --print-certs "$A" 2>&1 | grep -E "certificate (DN|SHA-256)" | head -n 2
log "--- badging (pacote/versão/sdk/icone/launcher) ---"
$BT/aapt dump badging "$A" 2>/dev/null | grep -E "^package:|^sdkVersion:|^targetSdkVersion:" | head -n 3
$BT/aapt dump badging "$A" 2>/dev/null | grep -q "name='com.reboclbrank.ceifalume' versionCode='15' versionName='0.1'" || erro 4 "badging fora do esperado (prod/15/0.1)"
$BT/aapt dump badging "$A" 2>/dev/null | grep -q "targetSdkVersion:'36'" || erro 4 "targetSdk não é 36!"
$BT/aapt dump badging "$A" 2>/dev/null | grep -q "application-icon" || erro 4 "APK sem ícone!"
$BT/aapt dump badging "$A" 2>/dev/null | grep -q "launchable-activity" || erro 4 "APK sem activity lançável (não abre)!"
echo "  ícone + launchable: OK"
log "--- manifesto (App ID real + LAUNCHER + INTERNET) ---"
$BT/aapt dump xmltree "$A" AndroidManifest.xml > /tmp/apk-manifest.txt 2>/dev/null
grep -q "APPLICATION_ID" /tmp/apk-manifest.txt || erro 4 "APPLICATION_ID fora do manifesto"
grep -q "$APP_ID" /tmp/apk-manifest.txt || erro 4 "App ID REAL fora do manifesto!"
grep -q "LAUNCHER" /tmp/apk-manifest.txt || erro 4 "categoria LAUNCHER fora do manifesto (sem ícone na gaveta)!"
grep -q "android.permission.INTERNET" /tmp/apk-manifest.txt || erro 4 "permissão INTERNET fora do manifesto (anúncio não carrega)!"
echo "  App ID real + LAUNCHER + INTERNET: OK"
log "--- zero ID de teste no APK ---"
grep -q "$TESTE_APP" /tmp/apk-manifest.txt && erro 4 "App ID de TESTE no manifesto!"
T1=$(strings "$A" | grep -c "3940256099942544" || true)
[ "${T1:-0}" = "0" ] || erro 4 "ID de teste no binário ($T1 ocorrências)!"
echo "  nenhum ID de teste: OK"
log "--- GMA+UMP no dex ---"
N=$(unzip -p "$A" 'classes*.dex' 2>/dev/null | strings | grep -c "com/google/android/gms/ads" || true)
[ "${N:-0}" -ge 100 ] || erro 4 "GMA fraco no dex ($N < 100)"
echo "  refs GMA no dex: $N"
unzip -p "$A" 'classes*.dex' 2>/dev/null | strings | grep -qi "ump\|consent" || erro 4 "UMP sumiu do dex!"
echo "  UMP no dex: sim"
log "--- 16KB (offsets + LOAD) ---"
python3 - "$A" <<'EOF'
import struct, sys, zipfile
z = zipfile.ZipFile(sys.argv[1]); f = open(sys.argv[1], "rb")
n = n16 = 0
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
restaurar_build
trap - EXIT
git -C ceifalume status --short | grep -v "^??" | grep -q . && erro 4 "repo não voltou ao limpo!"
log "repo limpo (release) — APK DE LANÇAMENTO pronto: $A"
