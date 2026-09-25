# Checklist de lançamento (Semana 8) — só o dono executa

O jogo está pronto para lançar (rev C.9, testado). Publicar é uma decisão
do dono, na conta dele. Passo a passo:

## 1. Criar a página no itch.io (~20 min)

- [ ] Criar conta / entrar em https://itch.io
- [ ] New project → título `Ceifalume`, tipo `Game`
- [ ] Colar os textos de `descricao-itch.md` (curta + longa + como jogar)
- [ ] Subir as imagens desta pasta como screenshots:
  - `shot-titulo-1280x720.png` (capa)
  - `shot-jogo-1280x720.png` (a fazenda)
- [ ] Classificação: `Farming`, tags sugeridas: `cozy`, `idle`, `farming-sim`,
      `portuguese`, `singleplayer`

## 2. Subir os arquivos (~15 min)

- [ ] Build web: zipar o conteúdo de `site/ceifalume/` → marcar
      **"This file will be played in the browser"**, viewport 1280×720
- [ ] Windows: zipar `ceifalume.exe` + `ceifalume.pck` (pasta
      `ceifalume/export/windows/`)
- [ ] Linux: zipar `ceifalume.x86_64` + `ceifalume.pck` (pasta
      `ceifalume/export/linux/`) — avisar que precisa dar permissão de
      execução (`chmod +x`)
- [ ] Preço: grátis (decisão atual; pode mudar depois)

## 3. Depois de publicar

- [ ] Jogar a versão do itch do começo ao fim uma vez (prova final)
- [ ] Trocar o card "Projeto 01" do site por Ceifalume (com link do itch)
- [ ] Anunciar onde os primeiros jogadores estão (decisão do dono)

## 4. Pós-lançamento (fora dos 60 dias, já planejado)

Prestígio ("Recomeço da Lua Nova"), mais plantações, ranking simples,
aplicativo de celular (Google Play).
