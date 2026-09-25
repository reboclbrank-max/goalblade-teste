# Kit itch.io — passo a passo do dono (texto pronto para colar)

**Data:** 2026-09-17 · **Atualizado 2026-09-18** (passos 1, 2 e 3 foram
**aplicados via API pelo assistente** — tags finais, descrição nova e GIF no
topo já estão no ar e verificados). **O que resta para o dono: 6 cliques,
~8 min.**
**Regra de ouro:** em cada passo, onde está um **texto entre aspas/duplo
travessão**, é só selecionar, copiar e colar. Não precisa entender nada —
se um botão não aparecer, para e me avise que eu resolvo com você.

## 0. Antes de começar: baixar os arquivos (links diretos)

Abra o link no navegador: a imagem abre na tela. Para salvar: **no celular,
segure o dedo em cima da imagem → "Salvar imagem"** · **no computador, botão
direito → "Salvar imagem como"**.

| Arquivo | Para quê | Link de download |
|---|---|---|
| Imagem do perfil (RB) | avatar + banner do perfil | https://reboclbrank-max.github.io/site/media/ceifalume/perfil-rb-itch-630x500.png |
| Screenshot nova (Dia 9, chuva boa) | galeria do jogo | https://reboclbrank-max.github.io/site/media/ceifalume/shot-jogo-1280x720.png |
| GIF (14 s, 3 MB) | **não precisa baixar** — já está embutido no topo da descrição | https://reboclbrank-max.github.io/site/media/ceifalume/gif-jogo-ceifalume-640x360.gif |

Origem dos arquivos na base: `projetos/01-ceifalume/divulgacao/` (e cópia
servida em `site/media/ceifalume/`, repo público).

**A capa NÃO precisa de troca** (o item antigo da auditoria estava errado): a
capa atual já é 630×500, que é exatamente o tamanho recomendado pela doc
oficial da itch (razão 315:250). O 1024×500 só vale para destaque editorial.

---

## O que resta para o dono (2026-09-18) — na ordem, ~8 min

1. **Remarcar "Android"** nas plataformas (novo — ver bloco abaixo)
2. **Excluir a screenshot duplicada** (Passo 4 antigo)
3. **Subir a screenshot nova** (resto do Passo 2 antigo)
4. **Perfil: imagem + bio** (Passo 5 antigo)
5. **Two column** (Passo 6 antigo)
6. **Devlog nº 1** (Passo 7 antigo)
7. **Conferir o "Run game" no celular** (seção 10 antiga)

### ✋ Remarcar "Android" (1 clique) — consequência do incidente da API

Na primeira escrita via API (2026-09-18), o sistema zerou a flag de plataforma
Android por ela não ser campo gravável. A página voltou a mostrar só "HTML5".
Correção:

1. Abra https://itch.io/game/5017404/edit
2. Role até a seção **Platforms** (Plataformas).
3. Marque a caixinha **Android**.
4. **Save.** O botão "Download" com o APK (79 MB) já está lá — isso só
   reinstala a flag de metadado.

Os passos antigos abaixo ficam para referência (textos exatos e onde clicar).

Você já colocou `idle`, `incremental` e `farming` (obrigado ✅). A itch limita
a **10 tags**, então trocamos 4:

1. Entre em: https://itch.io/game/5017404/edit (ou: Dashboard → Ceifalume → lápis)
2. No campo **Tags**, **apague estas 4:** `2d` · `android` · `farming-simulator` · `singleplayer`
3. **Adicione estas 4:** `cozy` · `relaxing` · `economy` · `offline`
4. **Guarde (Save).**

Lista final (10):
**idle · incremental · farming · cozy · casual · relaxing · management · economy · mobile · offline**

Por que estas: `idle`/`incremental`/`farming` são as palavras que o público do
jogo digita na busca; `cozy`/`relaxing` puxam quem navega por clima; `economy`
pega quem busca gestão de fazenda; `mobile` + `offline` (o diferencial de 8 h
com o jogo fechado) fecham a lista. O que saiu: `2d` (meta, quase todo indie é
2D), `android` (repete `mobile`), `farming-simulator` (puxa o público do
simulador pesado de trator, que não é o nosso) e `singleplayer` (óbvio para o
gênero, não filtra nada).

## 2. PASSO 2 — Subir o GIF e a screenshot nova (2 min) — ✅ GIF via API · ⏳ **só a screenshot falta** (botão de imagem do editor)

Ainda na página de edição (o mesmo passo 1):

1. Rode até a **descrição** do jogo. Na barra do editor tem um botão de
   **imagem** (ícone de foto/paisagem). Clique nele.
2. Escolha o arquivo `gif-jogo-ceifalume-640x360.gif`.
   O GIF entra na galeria do jogo e fica embutido onde você clicou.
3. Repita o mesmo botão e envie o `shot-jogo-1280x720.png`.

## 3. PASSO 3 — Descrição nova (1 min) — ✅ **FEITA VIA API (2026-09-18), não precisa mais** (texto que foi ao ar idêntico ao abaixo, com GIF embutido no topo)

1. Ainda no editor de descrição: selecione **tudo** o que está lá e apague.
2. Cole o texto abaixo, **inteiro e igual**:

```
🌙 Ceifalume é um jogo de fazenda grátis — idle noturno e aconchegante: plante, colha e negocie à luz da lanterna, num mercado onde o preço muda a cada dia. As plantações crescem sozinhas, até com o jogo fechado (até 8 horas). A graça: vender na hora certa.

[deixe aqui o GIF que você subiu no Passo 2, se ele não veio embutido sozinho]

Como jogar:
1. Escolha uma semente e toque num campo para plantar.
2. Espere crescer (ou feche o jogo e volte depois).
3. Colete, veja o preço do dia e venda na alta.
4. Invista em campos e melhorias. Repita e cresça.

O que tem:
• 6 plantações com arte própria — do Nabo de 30 segundos à Flor de Lume de 2 horas
• Loja com 7 melhorias: campos (até 24), celeiro, poço, lanterna, ajudante, composteira e carroça
• Mercado do dia: preços variam de 50% a 200%
• Eventos raros: Chuva boa, Feira da Madrugada e Seca
• Progresso offline: a fazenda continua até 8 h com o jogo fechado
• Save automático, música e efeitos sonoros originais
• Grátis, sem conta, sem cadastro — anúncios só em vídeo opcional com recompensa

Onde jogar:
• No navegador: botão "Run game" (computador ou celular)
• Android: botão "Download" (APK)
• Trailer: https://youtu.be/tB449xupDzY
• Canal do YouTube: https://www.youtube.com/channel/UCQdxKtfRnqNLd1ZOs9B6eaQ
• Site oficial: https://reboclbrank-max.github.io/site/
• Privacidade: https://reboclbrank-max.github.io/site/privacidade.html
• Contato: reboclbrank@gmail.com

Um jogo Rebocl Brank · feito em Godot · pt-BR · 1 jogador · offline
```

3. **Guarde.** (Se o GIF não ficar embutido na descrição, tudo bem — ele já
   está na galeria pelo Passo 2.)

## 4. PASSO 4 — Apagar a screenshot duplicada (1 min)

A 1ª imagem da galeria é a **capa repetida** (conferida byte a byte — é o
mesmo arquivo). Para tirar:

1. Abra a página pública do jogo (logado): https://reboclbrank-max.itch.io/ceifalume
2. Passe o mouse (ou o dedo) sobre a **primeira imagem da galeria** — a que
   idêntica à capa. Deve aparecer um **X / excluir**. Clique e confirme.
3. Se o X não aparecer aí, procure a galeria na página de edição
   (https://itch.io/game/5017404/edit) e exclua por lá.
4. **Não encontrou?** Me avise com uma foto da tela que eu resolvo com você.

## 5. PASSO 5 — Perfil com a marca da RB (2 min) — guia "preencha tudo" campo a campo (2026-09-18)

1. Entre em: https://itch.io/manage/profile
2. **Bio:** (o dono já colou o texto certo na tela, 2026-09-18 — confirmar e
   seguir) — texto de referência:
```
Jogos e aplicativos feitos à luz da lanterna. Ceifalume: fazenda noturna grátis, idle, no navegador ou no Android. Site: https://reboclbrank-max.github.io/site/ · YouTube: https://www.youtube.com/channel/UCQdxKtfRnqNLd1ZOs9B6eaQ
```
3. **Imagem do perfil** ("Add profile picture"): baixar de
   https://reboclbrank-max.github.io/site/media/ceifalume/perfil-rb-itch-630x500.png
   e enviar. (Monograma RB dourado centralizado sobre preto — a itch recorta o
   meio para o avatar e o banner; no recorte do meio o RB fica inteiro nos dois.)
4. **Trailer do perfil (opcional):** em "Upload game trailer" enviar o vídeo
   (download:
   https://reboclbrank-max.github.io/site/media/ceifalume/ceifalume-trailer-0.1.mp4,
   3,5 MB — o dono também deve ter o original no celular, do upload do YouTube).
   Pode pular sem prejuízo: a página do JOGO já tem o trailer embutido.
5. **Links:** no campo genérico "Add another link", cole
   https://reboclbrank-max.github.io/site/ — YouTube aparece sozinho (a itch
   reconhece a conta); **Mastodon e GitHub: deixar em branco** (decisão 2026-09-18:
   perfil focado em site + YouTube).
6. **Tema (presets):** escolher o que gostar — só muda a cor da página, dá
   para trocar depois.
7. **Guarde** (botão azul Save).

## 6. PASSO 6 — Layout em 2 colunas (1 min)

Jogos HTML5 na itch nascem em **coluna única, que esconde a coluna de
screenshots** (comportamento padrão da plataforma, confirmado na doc oficial).
Para a galeria aparecer ao lado do texto:

1. Na página pública do jogo, procure o botão **"Edit Theme"** (no topo da
   página, aparece porque você é o dono).
2. Em **Layout**, marque **Two column** (duas colunas).
3. **Guarde.**

## 7. PASSO 7 — Devlog nº 1 (2 min) — guia campo a campo da tela "Criar postagem" (2026-09-18)

1. No Dashboard, procure **Posts** (ou **Devlog**) → **Create a new post**.
2. **Título:** `0.1 no ar: a fazenda não dorme`
3. **Tipo de postagem:** escolher **Anúncio** ("Compartilhe um novo projeto ou
   uma atualização de um projeto existente") — **não** deixar no padrão
   "Blogar".
4. **Texto** (editor grande; se não aparecer, role a página):

```
O Ceifalume lançou a versão 0.1 — grátis, no navegador e no Android (APK).

O que tem na primeira versão:
• 6 plantações, 7 melhorias e um mercado que muda de preço todo dia
• Progresso offline (até 8 h com o jogo fechado)
• Música e efeitos sonoros originais, tudo em pt-BR

E o trailer foi feito de um jeito diferente: o jogo dirigiu a si mesmo.
Gravamos o motor do jogo jogando de verdade (plantando, colhendo, vendendo)
quadro a quadro e montamos a trilha com os sons do próprio jogo. O resultado
saiu a 30 fps lisos — dá para assistir na página do jogo.

Obrigado a quem testou e comentou! Próxima parada: as lojas do Android.
```

5. **Etiquetas** (Enter depois de cada uma): `ceifalume` · `release` ·
   `godot` · `pt-br`
6. **Idiomas:** marcar **Português** · **Data de publicação original:** em
   branco (é só para migração).
7. **Imagem de capa:** proporcão 16:9, largura mínima 500 px → enviar a
   `shot-jogo-1280x720.png` (1280×720, a screenshot nova baixada no Passo 2).
8. **Comentários:** deixar ativo · **Visibilidade:** "Publicado".
9. **Vincular ao jogo:** se aparecer campo "Projeto"/"Vincular a um projeto",
   escolher **Ceifalume**; se não aparecer, ao salvar pode surgir **"Convert to
   Devlog"** — é ele que vincula o post ao jogo: clicar.
10. **Salvar** (e o "Convert to Devlog", se aparecer).

## 8. KIT DE RESPOSTAS — quando alguém comentar (copiar e colar)

- **"Como baixo?"** →
  "No computador ou celular: botão 'Run game' (joga direto no navegador, sem
  instalar). No Android: botão 'Download' (APK, ~79 MB) — ao instalar, permita
  'instalar apps de fontes desconhecidas'. Qualquer dúvida, me chama por aqui. 🙂"
- **"É pago?"** →
  "Grátis, sem conta e sem cadastro. No Android tem um anúncio opcional: você
  assiste a um vídeo se quiser a planta amadurecer na hora — nunca é
  obrigatório para jogar."
- **"Tem pra iPhone?"** →
  "Por enquanto o download é Android; mas no iPhone dá para jogar pelo
  navegador também — é só abrir o link do jogo. 🙂"
- **"Qual o motor?"** →
  "Godot, todo em GDScript. Arte e música originais, feitas pelo próprio
  desenvolvedor."
- **"Achei um bug"** →
  "Obrigado por avisar! Me conta: o que aconteceu, em que tela e se você
  joga no navegador ou no Android? Vou olhar. 🙏"
- **"Dá para aprender sozinho / como começo?"** →
  "Dá sim: escolha uma semente (Nabo é a mais barata), toque num campo, espere,
  colha e venda no mercado quando o preço estiver subindo. Pode fechar o jogo
  quando quiser — a fazenda continua trabalhando até 8 h. 🙂"

## 9. O que eu já fiz sozinho (sem precisar de você)

- **Auditoria 100% via API da itch** (chave que você criou): estatísticas
  oficiais do jogo e do perfil — 14 visualizações, 1 download (o APK), 0
  compras (é grátis), publicado 2026-09-16 21:06 UTC. Detalhe em
  `projetos/01-ceifalume/marketing/auditoria-itch.md`.
- **Confirmei que sua edição de tags foi publicada** (a página mostra
  "atualizada" e as tags idle/incremental/farming já estão no ar).
- **Veredito sobre o que a API dá e o que não dá** (gravado em
  `ferramentas/chaves.md`): estatísticas sim; editar a página não — por isso
  os 7 passos acima existem.
- **Gerei os 3 arquivos do Passo 0** e guardei tudo na base.

## 10. Depois que terminar

1. Me mande um "feito" (ou foto de onde travou).
2. Eu vou conferir tudo pela API e pela página pública e registrar os números
   antes/depois na base.
3. Depois disso a fila é: **comunidades + Shorts** (a divulgação de verdade
   começa a encher a página) e as **lojas grátis** (Galaxy Store → Aptoide →
   Amazon → Uptodown → Huawei).
4. Continue conferindo o **"Run game" no seu celular** (tem de ser o 0.1 com
   carimbo) — esse é o único item que só você pode fazer.
