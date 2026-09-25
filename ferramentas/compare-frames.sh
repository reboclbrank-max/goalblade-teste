#!/usr/bin/env bash
# Diff de pixels com tolerância, para "antes × depois" de tela parada.
#   compare-frames.sh antes.png depois.png [fuzz%]
#
# Controle honesto (visto em 2026-09-15): renderizar o MESMO build duas vezes com o
# MESMO cenário NÃO é idêntico — deu 20 px de diferença porque o preço do dia é
# sorteado em tempo de execução. Portanto: (a) número pequeno isolado (dezenas de px)
# é ruído de dado, não regressão; (b) o controle de bit-exatidão só vale comparando o
# mesmo arquivo, ou depois que existir CEI_SEMENTE no jogo (pendência registrada).
set -u
a=${1:-}; b=${2:-}; f=${3:-12}
[ -f "$a" ] && [ -f "$b" ] || { echo "uso: compare-frames.sh antes.png depois.png [fuzz%]"; exit 1; }
n=$(compare -metric AE -fuzz "${f}%" "$a" "$b" null: 2>&1)
case $n in
  ''|*[!0-9]*) echo "compare falhou: $n"; exit 1 ;;
esac
quadro=$(identify -format "%w %h" "$a" 2>/dev/null)
set -- $quadro
total=$(( ${1:-0} * ${2:-0} ))
if [ "$total" -gt 0 ]; then
	pct=$(awk -v n="$n" -v t="$total" 'BEGIN{printf "%.2f", 100*n/t}')
	printf "%s  vs  %s\n  %s px diferentes de %s (%s%%) — fuzz %s%%\n" \
		"$(basename "$a")" "$(basename "$b")" "$n" "$total" "$pct" "$f"
else
	printf "%s  vs  %s\n  %s px diferentes — fuzz %s%%\n" "$(basename "$a")" "$(basename "$b")" "$n" "$f"
fi
[ "$n" = "0" ] && echo "  → idênticos (0 px)"
exit 0
