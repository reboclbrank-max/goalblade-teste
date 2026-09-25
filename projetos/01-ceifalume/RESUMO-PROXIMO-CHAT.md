# Passagem de turno — Ceifalume (2026-09-16, noite — atualizado após o trailer)

## ✅ FEITO (tudo no ar e verificado como visitante)
- **0.1 LANÇADO**: APK 83.579.693 bytes (BUILD-01B EXIT 0, App ID real, 0 ID teste).
- Release `v0.1` no repo público `site`: `ceifalume.apk` + `ceifalume-0.1-web.zip` (13 MB).
- Site com botão launch: https://reboclbrank-max.github.io/site/
- Web jogável: https://reboclbrank-max.github.io/site/ceifalume/
- **itch.io PÚBLICA**: https://reboclbrank-max.itch.io/ceifalume (Run game + APK 79 MB + 4 prints + capa + 10 tags).
- Kit itch guardado em `base/projetos/01-ceifalume/itch/` (textos, capa, prints, links).
- YouTube do dono existe: https://youtube.com/@reboclbrank (6 gameplays + 2 Shorts, parado ~10 meses).
- **TRAILER 0.1 GRAVADO E PUBLICADO (2026-09-16, noite)** — 45,9 s, 1280×720, 30 fps,
  3.473.373 bytes, abertura RB + gameplay real (Dia 1 → Dia 13) com a música e os
  efeitos do próprio jogo. Baixar:
  https://github.com/reboclbrank-max/site/releases/download/v0.1/ceifalume-trailer-0.1.mp4
  Cópia no repositório: `base/projetos/01-ceifalume/divulgacao/ceifalume-trailer-0.1.mp4`.
  Ferramenta: `ceifalume/trailer.gd` (fora do export) + `base/ferramentas/montar-trilha.py`.

## ⏳ A FAZER (ordem)
1. **Dono**: baixar o mp4, subir no YouTube (@reboclbrank) e colar o link no campo
   trailer da página da itch.io. (É o único passo que depende dele.)
2. Samsung Galaxy Store (grátis) → Aptoide → Amazon → Uptodown → Huawei.
3. Play Store: FORA (sem dinheiro) — só pós-receita.

## 📌 Regras de pé
- pt-BR; orçamento-zero; token guardado em `/home/user/tools/.token-github` (reutilizar, só pedir se 401);
  token NUNCA em repo/commit/mensagem; conta `reboclbrank-max`, tudo em `main`
  (`base` privado, `ceifalume` privado, `site` público); **SEMPRE salvar tudo nos repos**.
- `.git` some entre turnos: re-clonar + mover `.git` (pattern `GIT_ASKPASS=/tmp/.ap`); nunca `echo` no token.
- **Espaço de trabalho grande demais perde arquivos entre turnos** (medido: ~400 MB →
  sumiram `.git` do `site`, os `.ogg` do jogo, o PNG do fundo e o cache `.godot`).
  Depois de gerar vídeo/frames: apagar os quadros e manter o workspace magro.

## 🗺️ Arquivos-chave
- `itch/kit-itch.md` (+ `capa-630x500.png`, `shots/*.png`) — kit da página.
- Trailer: `divulgacao/ceifalume-trailer-0.1.mp4` + `trailer-0.1-poster-1280x720.jpg`
  (thumbnail) + `verificacao/trailer-0.1-folha-geral.jpg` (conferência) +
  `verificacao/trailer-0.1-trilha.txt` (mapa dos sons).
- Prints do dono salvos em `/home/user/uploads/` (chegam TRUNCADOS: abrir com PIL
  `LOAD_TRUNCATED_IMAGES=True` e salvar PNG).
