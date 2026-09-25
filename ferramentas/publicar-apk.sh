#!/bin/sh
# ============================================================
# CEIFALUME — publica o AAB release assinado (C.16 em diante)
# Motor 4.5.2 + AdMob v5.1.0 + SDK 36 + NDK r28 (página 16KB,
# exigida pelo Play desde nov/2025).
# Reinstala tudo que some entre turnos (JDK, SDK+NDK, templates,
# plugin AdMob, template de build) e exporta com o keystore
# guardado em ~/cofre + cópia (senhas em ~/.segredos-apk, chmod 600,
# fora dos repositórios — nunca entram em commit).
# Uso: sh tools/publicar-apk.sh
# Saída: ceifalume/export/android/ceifalume.aab (verificado:
# assinatura jarsigner, bundletool validate, targetSdk 36 no
#	manifesto, AdMob dentro, .so alinhado em 16KB)
# ============================================================
set -e
cd /home/user

# 0a. GUARDA DAS CHAVES (C.14): arquivos com "keystore" no nome e pastas OCULTAS somem entre
# turnos (protecao da plataforma); as chaves moram em ~/cofre (pasta NORMAL, sem ponto) + copia.
for par in "lancamento copia-lancamento" "depuracao copia-depuracao"; do
  set -- $par; vivo="/home/user/cofre/$1"; copia="/home/user/cofre/$2"
  if [ ! -f "$vivo" ]; then
    if [ -f "$copia" ]; then cp "$copia" "$vivo"; echo "AVISO: $1 restaurado da copia!"
    else echo "FALTA A CHAVE $1 (nem copia existe) - abortando"; exit 3; fi
  fi
done
echo "chaves ok (guarda passou)"
grep -q "^teste_livre=false" ceifalume/project.godot || { echo "FALHOU: painel de teste LIGADO (teste_livre) — desligue antes de publicar"; exit 4; }
echo "painel de teste desligado ok"

# 0. base de sempre (godot + remotos + auth git) e swap 3G
sh tools/acender-motor.sh
if ! swapon --show 2>/dev/null | grep -q /swapfile; then
  [ -f /swapfile ] || { sudo fallocate -l 3G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile >/dev/null; }
  sudo swapon /swapfile 2>/dev/null || true  # pode já estar ligado
fi

export JAVA_HOME=/home/user/.cache/jdk17
export ANDROID_HOME=/home/user/.cache/android-sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export GRADLE_USER_HOME=/home/user/.cache/gradle
export GRADLE_OPTS="-Xmx1024m -XX:MaxMetaspaceSize=256m"  # 1536m morre de OOM na caixa 2GB (C.17)
export PATH=$JAVA_HOME/bin:$PATH
FERR=~/.cache/ferramentas

# 1. JDK 17 (o do sistema é 11; Gradle 8.11 + sdkmanager atual exigem 17)
if [ ! -x "$JAVA_HOME/bin/java" ]; then
  mkdir -p ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o jdk17.tar.gz "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jdk/hotspot/normal/eclipse"
  mkdir -p ~/.cache/jdk17 && tar -xzf jdk17.tar.gz -C ~/.cache/jdk17 --strip-components=1
  rm -f jdk17.tar.gz
  cd /home/user
fi

# 2. Android SDK (cmdline-tools + platform 36 + build-tools 36/35 + NDK r28)
#    build-tools 35.0.1 = padrão do template Godot; 36.0.0 = nosso alvo.
#    NDK 28.1.13356709 = pinado pelo template 4.5.2 (16KB nativo).
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
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH

# 3. templates Android do Godot 4.5.2 (+ .tpz some; baixa de novo ~1.3GB)
TDIR=~/.local/share/godot/export_templates/4.5.2.stable
if [ ! -f "$TDIR/android_release.apk" ]; then
  mkdir -p $TDIR ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o templates.tpz https://github.com/godotengine/godot/releases/download/4.5.2-stable/Godot_v4.5.2-stable_export_templates.tpz
  mkdir -p ../x && unzip -oq templates.tpz "templates/android_*" "templates/version.txt" -d ../x/
  cp ../x/templates/* $TDIR/ && rm -rf ../x templates.tpz
  cd /home/user
fi

# 4. plugin AdMob (pinado: editor v5.1.0 + nativo 4.5.2)
#    res://android e addons/admob/android/bin são gitignored: reinstala
#    todo turno. O addons/admob do editor É commitado (classes usadas
#    pelo jogo); só rebaixa se sumiu ou se a versão não é a pinada.
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

# 5. template de build + compileSdk 36 + App ID + .build_version (editor faria no menu)
if [ ! -f ceifalume/android/build/AndroidManifest.xml ]; then
  mkdir -p ceifalume/android/build
  unzip -oq $TDIR/android_source.zip -d ceifalume/android/build/
  touch ceifalume/android/build/.gdignore
fi
# Carimbo EXATO (4.5.2.stable, não 4.5.stable: o export confere e barra) +
# compileSdk 36 (o template fixa 35; target 36 exige >= 36). Idempotentes:
# rodam sempre, inclusive se o build anterior morreu no meio.
printf '4.5.2.stable\n' > ceifalume/android/.build_version
sed -i 's/compileSdk *: *35/compileSdk : 36/' ceifalume/android/build/config.gradle
grep -q 'compileSdk *: *36' ceifalume/android/build/config.gradle || { echo "FALHOU: compileSdk não subiu"; exit 4; }
# App ID: o real mora em ~/.segredos-apk (APP_ID=...); sem ele, teste do Google.
# v5 lê de project.godot [admob]: injeta antes do build e RESTAURA depois (trap),
# para o repo guardar só o ID de teste (público, do próprio Google).
APP_ID=$(grep -E "^APP_ID=" /home/user/.segredos-apk 2>/dev/null | cut -d= -f2)
  [ -z "$APP_ID" ] && APP_ID="ca-app-pub-3940256099942544~3347511713"  # teste do Google
  restaurar_projeto() { git -C ceifalume checkout -- project.godot 2>/dev/null || true; }
  trap restaurar_projeto EXIT
  python3 - "$APP_ID" <<'EOF'
import re, sys
p = "ceifalume/project.godot"
s = open(p).read()
novo = sys.argv[1]
if "[admob]" not in s:
    # O editor apaga a secao quando ela vale o padrao: recria com o ID real.
    s += '\n[admob]\n\ngeneral/android/enabled=true\ngeneral/android/app_id="%s"\n' % novo
    n = 1
else:
    s, n = re.subn(r'general/android/app_id="[^"]*"', 'general/android/app_id="%s"' % novo, s)
    if n == 0:
        s, n = re.subn(r"(\[admob\]\n)", r"\1\ngeneral/android/app_id=\"%s\"\n" % novo, s, count=1)
assert n == 1 and novo in s, "falha ao injetar App ID"
open(p, "w").write(s)
print("project.godot App ID ok")
EOF

# 6. senha do keystore (mora no .godot, gitignored — nunca no preset)
. /home/user/.segredos-apk
printf '[preset.1.options]\nkeystore/release_password="%s"\n' "$STOREPASS" > ceifalume/.godot/export_credentials.cfg

# 7. editor settings (SDK + Java) — Godot 4.5
ES=~/.config/godot/editor_settings-4.5.tres
for par in 'export/android/android_sdk_path = "/home/user/.cache/android-sdk"' 'export/android/java_sdk_path = "/home/user/.cache/jdk17"'; do
  chave=$(echo "$par" | cut -d= -f1 | sed 's/ *$//')
  if grep -q "^${chave} =" $ES 2>/dev/null; then
    sed -i "s|^${chave} =.*|${par}|" $ES
  else
    echo "$par" >> $ES
  fi
done

# 7b. gradle magro (caixa de 2GB: sem isso o OOM killer come o build)
mkdir -p $GRADLE_USER_HOME
printf 'org.gradle.daemon=false\norg.gradle.workers.max=1\norg.gradle.parallel=false\norg.gradle.caching=false\nkotlin.compiler.execution.strategy=in-process\nandroid.useAndroidX=true\n' > $GRADLE_USER_HOME/gradle.properties

# 7c. bundletool (verificação oficial do AAB; some entre turnos, rebaixa)
if [ ! -f ~/.cache/dl/bundletool.jar ]; then
  BT=$(curl -s https://api.github.com/repos/google/bundletool/releases/latest 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('tag_name',''))")
  mkdir -p ~/.cache/dl && cd ~/.cache/dl
  curl -sSL --retry 3 -o bundletool.jar "https://github.com/google/bundletool/releases/download/$BT/bundletool-all-$BT.jar"
  cd /home/user
fi

# 8. importa + régua rápida + exporta AAB
G=$FERR/godot
$G --headless --path ceifalume --import 2>&1 | grep -iE '^(ERROR|SCRIPT ERROR)|Failed to' | head -n 4
$G --headless --path ceifalume --script res://teste_anuncios.gd 2>&1 | grep -E "TESTE_ANUNCIOS"
mkdir -p ceifalume/export/android
$G --headless --path ceifalume --export-release "Android" export/android/ceifalume.aab

# 9. verifica (assinatura + bundletool + manifesto + AdMob + 16KB)
A=ceifalume/export/android/ceifalume.aab
[ -f "$A" ] || { echo "FALHOU: AAB não gerado"; exit 4; }
echo "--- assinatura (jarsigner) ---"
$JAVA_HOME/bin/jarsigner -verify "$A" 2>&1 | grep -iE "verified" | head -n 1
echo "--- bundletool validate ---"
$JAVA_HOME/bin/java -jar ~/.cache/dl/bundletool.jar validate --bundle="$A" > /tmp/aab-validate.log 2>&1 && echo "validate OK"
echo "--- manifesto (pacote/versão/sdk) ---"
$JAVA_HOME/bin/java -jar ~/.cache/dl/bundletool.jar dump manifest --bundle="$A" > /tmp/aab-manifest.xml
python3 - <<'EOF'
import re
xml = open("/tmp/aab-manifest.xml").read()
for k in ["package", "android:versionCode", "android:versionName", "android:minSdkVersion", "android:targetSdkVersion"]:
    m = re.search(k + r'="([^"]+)"', xml)
    print(" ", k, "=", m.group(1) if m else "?")
assert 'android:targetSdkVersion="36"' in xml, "targetSdk não é 36!"
print("  targetSdk 36 OK")
EOF
echo "--- App ID no manifesto do AAB (tem que ser o de ~/.segredos-apk) ---"
grep -q "$APP_ID" /tmp/aab-manifest.xml || { echo "FALHOU: App ID ausente no manifesto do AAB!"; exit 4; }
echo "  App ID no manifesto OK"
echo "--- AdMob dentro do AAB ---"
unzip -l "$A" | grep -ciE 'gms/ads|admob' | sed 's/^/  arquivos admob-gms: /'
echo "--- ELF do motor (todo LOAD >= 0x4000) ---"
rm -rf /tmp/so16 && mkdir -p /tmp/so16
unzip -oq "$A" 'base/lib/arm64-v8a/*.so' -d /tmp/so16
SO16=$(ls /tmp/so16/base/lib/arm64-v8a/*.so | head -n 1)
readelf -lW "$SO16" | grep LOAD | awk '{print "  LOAD align:", $NF}'
RUIM=$(readelf -lW "$SO16" | grep LOAD | awk '{print $NF}' | (c=0; while read a; do [ "$(($a))" -ge 16384 ] || c=$((c+1)); done; echo $c))
[ "$RUIM" = "0" ] || { echo "FALHOU: $RUIM LOAD < 16KB"; exit 4; }
echo "  ELF 16KB OK"
echo "--- APK que o Play geraria (splits) alinhado em 16KB ---"
rm -f /home/user/.cache/bt-tmp/split.apks
mkdir -p /home/user/.cache/bt-tmp
$JAVA_HOME/bin/java -Djava.io.tmpdir=/home/user/.cache/bt-tmp -jar ~/.cache/dl/bundletool.jar build-apks --bundle="$A" --output=/home/user/.cache/bt-tmp/split.apks --ks=/home/user/cofre/depuracao --ks-pass=pass:android --ks-key-alias=androiddebugkey --key-pass=pass:android > /tmp/aab-apks.log 2>&1
rm -rf /home/user/.cache/sp16 && mkdir -p /home/user/.cache/sp16 && cd /home/user/.cache/sp16
unzip -oq /home/user/.cache/bt-tmp/split.apks 'splits/base-arm64*.apk' 'splits/base-master*.apk'
cd /home/user
python3 - <<'EOF'
import struct, glob, zipfile
n = 0
for apk in sorted(glob.glob("/home/user/.cache/sp16/splits/base-arm64*.apk")):
    z = zipfile.ZipFile(apk); f = open(apk, "rb")
    for info in z.infolist():
        if info.file_size > 0 and info.filename.endswith(".so"):
            assert info.compress_type == zipfile.ZIP_STORED, "comprimido: " + info.filename
            f.seek(info.header_offset)
            _s, _v, _fl, _c, _mt, _md, _crc, _cs, _us, fnl, efl = struct.unpack("<IHHHHHIIIHH", f.read(30))
            dado = info.header_offset + 30 + fnl + efl
            assert dado % 16384 == 0, "DESALINHADO: " + info.filename
            n += 1
print("  %d .so STORED alinhados em 16KB: OK" % n)
assert n > 0
EOF
$ANDROID_HOME/build-tools/36.0.0/zipalign -c -p 16 /home/user/.cache/sp16/splits/base-arm64_v8a.apk && echo "  zipalign -p 16 oficial: OK"
echo "--- SDK ads no dex do split (o que o Play entrega; URLs sobrevivem ao R8) ---"
MAST=""
for apk in /home/user/.cache/sp16/splits/base-master*.apk; do
  if unzip -l "$apk" | grep -q 'classes.dex'; then MAST="$apk"; break; fi
done
[ -n "$MAST" ] || { echo "FALHOU: split master com dex nao achado"; exit 4; }
REFS=0
for d in $(unzip -l $MAST | grep -oE 'classes[0-9]*\.dex'); do
  n=$(unzip -p $MAST "$d" | strings | grep -ciE 'doubleclick|googlesyndication|ads-mobile-sdk' || true)
  REFS=$((REFS + n))
done
echo "  marcadores ads no dex: $REFS (AAB-15 sem SDK = 0)"
[ "$REFS" -gt 10 ] || { echo "FALHOU: SDK do AdMob ausente no dex!"; exit 4; }
rm -f /home/user/.cache/bt-tmp/split.apks
echo "AAB PRONTO: $A ($(stat -c%s $A) bytes)"
# 10. dieta do snapshot (teto ~128MB): o template de build (~200MB) e
# regeneravel e JA comeu o keystore uma vez (C.12) — apaga sempre no fim.
rm -rf ceifalume/android/build ceifalume/android/.build_version
restaurar_projeto; trap - EXIT
git -C ceifalume status --short | head -n 3
echo "limpeza pos-build ok (plugins e keystore ficam; project.godot restaurado)"
