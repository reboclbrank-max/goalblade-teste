# Evidência visual (renderizada, não desenhada à mão)

Fotos do jogo renderizado neste ambiente (Xvfb + GPU por software llvmpipe, Godot
4.3, cenário "meio": moedas 55, Dia 9, chuva boa, Celeiro 12/30, dois campos
comprados). Servem de linha de base para a reforma da interface: qualquer mudança
de layout tem de ser re-renderizada e comparada com estas.

| Arquivo | O que é |
|---|---|
| `jogo-1280x720-revA-antes.png` | antes das mudanças de legibilidade (6 px cortados — quase nada) |
| `jogo-1280x720-revB-cortado.png` | depois de aumentar as fontes: **292 px fora da tela** — "Moedas" acima do topo, "Fazer um bico" e os últimos botões da loja abaixo do fim |
| `jogo-1280x720-depois.png` | com o encaixe corrigido (rev C): tudo na tela; a loja vira lista rolável quando falta altura |
| `jogo-844x390-depois.png` | o mesmo, na janela do celular deitado (lógico 1558×720) |
| `pagina-celular-deitado-revC.png` | a **página publicada** aberta no Chromium a 844×390 com WebGL por software — é o que ele vê no aparelho |

Regerar (as ferramentas precisam ser reinstalladas em chat novo; os comandos
estão no `guia-do-proximo-chat.md`):

```bash
xvfb-run -a -s "-screen 0 1280x720x24" \
  env LIBGL_ALWAYS_SOFTWARE=1 CEI_MEDIR=1 CEI_CENARIO=meio \
  CEI_SAIDA=/home/user/tools/renders/tela.png \
  ~/.cache/ferramentas/godot --path /home/user/ceifalume --rendering-driver opengl3 \
  --resolution 1280x720 --script res://prova_visual.gd
```

Nada aqui é arte do jogo: é instrumento de trabalho, e por isso mora na base.

| `jogo-1280x720-revC1.png` | o mesmo cenário na rev C.1 (pacote sem ferramentas de teste): layout inalterado, 0 cortes — é a linha de base vigente |
| `ceifalume-jogando.mp4` | **vídeo de 7 s do jogo jogando sozinho** (bot + `grava_jogo.gd`, tempo acelerado ×14, 140 quadros a 20 fps, 1280×720, 69 KB): serve para julgar ritmo e economia sem aparelho; **não** serve para julgar toque, temperatura ou gosto |

| `jogo-1280x720-revC2.png` | rev C.2: Loja em faixa no pé (7 itens, sem rolo), sementeira com folga medida na fonte |
| `jogo-844x390-revC2.png` | a mesma em janela de celular deitado (lógico 1534×720) |
| `jogo-390x844-revC2.png` | em pé: 6 de 6 campos cabem inteiros dentro da grade |
| `ceifalume-jogando.mp4` | **atualizado na 3ª rodada**: 140 quadros a 20 fps com a interface nova (91.845 B) — antes da correção do aquecimento o gravador devolvia tela escura |

Duas checagens novas que valem mais que olhar print: `~/tools/compare-frames.sh
antes.png depois.png [fuzz%]` (diff de pixels com tolerância; use o MESMO cenário e o
MESMO quadro) e OCR de recorte: `convert render.png -crop LxA+X+Y +repage -resize 400%
-colorspace gray /tmp/o.png && tesseract /tmp/o.png stdout --psm 7` — foi o OCR que
provou que o preço 2500 estava sendo desenhado como 250.

Como regerar o vídeo (o comando do render acima não cobre isto): `grava_jogo.gd`
grava os quadros em PNG e o `ffmpeg` do sistema monta o MP4 — os dois comandos
estão em `projetos/01-ceifalume/progresso.md`, seção "Motor de verificação".

| `estado-limite-1280x720.png` | o jogo com **24/24 campos** plantados (cenário `limite`): a grade mostra 3 linhas e rola; nada estoura |
| `estado-limite-844x390.png` | o mesmo, na janela do celular deitado |
| `estado-limite-390x844.png` | em pé: cabem os 24 campos inteiros (a grade aproveita a altura) |

O cenário limite se regera assim (ninguém chega a 24 campos jogando — medido: dia
9.689 ≈ 161 h de tela — então este é o jeito de olhar o estado):

```bash
xvfb-run -a -s "-screen 0 1280x720x24" env LIBGL_ALWAYS_SOFTWARE=1 \
  CEI_MEDIR=1 CEI_CENARIO=limite CEI_SAIDA=/tmp/limite.png \
  ~/.cache/ferramentas/godot --path /home/user/ceifalume --rendering-driver opengl3 \
  --resolution 1280x720 --script res://prova_visual.gd
```