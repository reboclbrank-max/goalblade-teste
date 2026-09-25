# Plano de marketing do Ceifalume — o assistente executa, o dono só dá o "posta"

**Criado:** 2026-09-18 · **Decisão do dono:** "a partir de agora você fará o marketing por mim"
(ver `empresa/registro-de-decisoes.md`). Orçamento: **R$ 0,00** (sem anúncios pagos até haver receita).

## 1. O que está pronto (fechado em 2026-09-18, tudo verificado pela API)

| Canal | Estado | Link |
|---|---|---|
| itch.io — página | 10 tags, descrição nova + GIF, **HTML5 + Android**, devlog nº 1 "0.1 no ar: a fazenda não dorme" publicado | https://reboclbrank-max.itch.io/ceifalume |
| itch.io — perfil | foto + bio | https://reboclbrank-max.itch.io |
| YouTube — trailer | no ar (categoria: decisão fechada, não mexer) | https://youtu.be/tB449xupDzY |
| Mastodon | perfil completo + post 1 (GIF) | https://mastodon.social/@ReboclBrank |
| Bluesky | perfil completo + post 1 (screenshot) | https://bsky.app/profile/reboclbrank.bsky.social |
| Site (Pages) | mídias servidas | https://reboclbrank-max.github.io/site/ |

Único item web-only que ficou de fora (opcional, sem impacto em tráfego): tema **Two column** na itch — a página ainda é single column (`right_col` escondida). Faz quando quiser.

## 2. Horários — análise e decisão

Fontes (2026): Buffer/State of Social 2026 via spicycreatortips (3 milhões de posts): **melhor dia no Bluesky = sábado; melhor horário isolado = sábado 17h; janela 16–19h nos fins de semana; dias de semana 18–21h**. Schedulala e Picmim (dados menores) apontam **terça** como melhor dia útil, manhã 9–11h e noite 19–21h (horário do leste dos EUA). Mastodon não tem estudo grande; a comunidade #gamedev/#godot é majoritariamente europeia + EUA, e o `#ScreenshotSaturday` é a tradição semanal do indie dev (sábado).

Nosso público é misto: **BR** (jogo em pt-BR, idle, celular) + **indie/Godot internacional** (hashtags em inglês). Fuso do dono: **Fortaleza = UTC-3** (= EUA leste +1h no horário de verão deles, +2h no inverno; Europa central −5h/−6h).

**Grade adotada (horário de Fortaleza):**

| Quando | Janela | Por quê |
|---|---|---|
| **Sábado 17h–19h** ⭐ | post principal da semana (#ScreenshotSaturday) | pico do Bluesky (17h) + tradição indie + BR de fim de tarde |
| **Terça 20h–21h** | post 2 da semana | melhor dia útil; 19h–20h EUA leste, noite BR |
| **Quinta 12h–13h** (opcional) | post curto / resposta / bastidor | almoço BR + manhã EUA (9–11h leste) |
| Domingo 10h–12h | reserva (boost do post de sábado no Mastodon) | segundo pico de fim de semana |

Evitar: madrugada, sexta à noite, depois das 22h. **Ritmo: 2 posts/semana fixos + 1 opcional.** Mais que isso em conta nova parece spam e não rende.

## 2b. Frequência — resposta à pergunta "pode ser todo dia?" (dono, 2026-09-19)

**Publicar post novo todo dia: não** (conta nova + mesmo jogo todo dia = ruído; as contas do nicho que curtiram param de curtir, e o Mastodon marca como spam). **Mas o marketing acontece todo dia** — só que a maior parte é interação, não post:

| Todo dia (o dono manda "rodada" — 1 vez/dia, qualquer hora) | O assistente faz via API |
|---|---|
| Ler respostas/menções nas duas redes | responde em nome do dono (tom: gentil, curto, pt/en conforme quem falou) |
| Curtir/repostar 3–5 posts de #godot / #ScreenshotSaturday / #indiedev de outros devs | reciprocidade real; é o que faz os outros olharem de volta |
| Seguir 3–5 contas novas do nicho (nunca mais que isso por dia) | crescimento sem parecer bot |
| Medir (itch + redes) | painel só se houver variação |

**Posts novos:** sáb 17h + ter 20h (fixos) + quinta 12h (bastidor curto, opcional). Ou seja: **3 posts/semana no máximo, interação todo dia.** Se o dono mandar "rodada" todo dia, o assistente faz o bloco acima e responde em 3 linhas.

**Feito em 2026-09-19 (autorização "faça isso, faça tudo pela chave"):**
- Bluesky: **14 follows** — quem interagiu (GameBrief 2,4k · Kevin Pedatte 4,2k · freepixel.art · indiegameloveit · Latest Gaming Buzz · Chiitan 188k) + curadores/oficiais (Godot Engine 44k · itch.io 147k · GDQuest 4,4k · INDIEGAMES.WTF 10k · Godot Barn · Indie Games Plus · Rak/Godot · bitbra.in). Seguindo: 15.
- Mastodon: **5 follows** (Godot Engine 22,9k · itch.io 17,3k · indiegames · gamedev · pixelart) + **4 hashtags seguidas** (#godot #indiedev #screenshotsaturday #gamedev) para a home mostrar gente do nicho. GDQuest lá bloqueia follow (403).

## 3. Como o dono pede (é só mandar uma destas frases)

- **"posta"** → publico o próximo item do calendário (seção 4) nas duas redes, na hora, e devolvo os links.
- **"posta X"** (ex.: "posta o trailer") → publico esse item específico.
- **"como estamos?"** → rodo `ferramentas/medir-marketing.py`, atualizo `METRICAS.md` e devolvo o painel com a variação desde a última medição.
- **"rodada"** → bloco diário da seção 2b (responder, curtir, seguir 3–5, medir se mudou).
- **"relatório da semana"** → painel + o que funcionou/não + o próximo passo sugerido.

Aviso do lado do assistente: ele **não consegue postar sozinho num horário** — não há agendador entre as conversas. Por isso o dono manda "posta" **dentro da janela** (sábado 17h, terça 20h) e a publicação sai em menos de 1 minuto.

## 4. Calendário (próximos 30 dias)

| # | Data sugerida | Conteúdo | Mídia | Estado |
|---|---|---|---|---|
| 1 | 18/09 (qui) | "0.1 no ar" | GIF (Masto) / shot (Bsky) | ✅ publicado |
| 2 | sáb 19/09 20:35 (janela perdida, ainda sábado) | #ScreenshotSaturday — dia 9, chuva boa | shot-jogo 1280×720 | ✅ publicado — Masto https://mastodon.social/@ReboclBrank/117300325175773099 · Bsky https://bsky.app/profile/reboclbrank.bsky.social/post/3mvvtw7tpk22z |
| 3 | ter 22/09 20:25 | Trailer 0.1 (46 s) | Masto: MP4 nativo · Bsky: card do YouTube + republicado em vídeo nativo 3mw5fhok2tw2q | ✅ Masto https://mastodon.social/@ReboclBrank/117317268552155642 · Bsky https://bsky.app/profile/reboclbrank.bsky.social/post/3mw5eygdmn72m |
| 4 | **sáb 26/09 17h** | "Jogue no Android sem loja" — APK direto, sem conta | shot-titulo | pronto |
| 5 | ter 29/09 20h | Bastidor: "por que a fazenda continua 8 h com o jogo fechado" (idle) | GIF | rascunho |
| 6 | sáb 03/10 17h | #ScreenshotSaturday 2 — pedir feedback ("o que plantariam primeiro?") | shot nova (dono manda print) | depende de print |
| 7 | ter 06/10 20h | Devlog: "o que vem na 0.2" | capa devlog | depende do dono decidir a 0.2 |
| 8 | sáb 10/10 17h | Número redondo ("X pessoas já colheram") se houver | GIF | depende das métricas |
| 9 | ter 13/10 20h | Reddit **manual pelo dono** (r/godot "Made with Godot", r/IndieGaming) — texto pronto na seção 6 | shot + GIF | texto pronto |

Regras: só conteúdo próprio; nada de comentário automático em posts de terceiros; nenhum follow em massa. Responder comentários reais é bem-vindo (o assistente redige, o dono aprova se quiser).

## 5. Textos prontos (colar/publicar)

### Post 2 — #ScreenshotSaturday (sáb 20/09)
**Mastodon (pt+en, ≤500):**
> 🌧️ Dia 9 no Ceifalume: chuva boa. Quando chove, a fazenda se rega sozinha e a lanterna vira só companhia.
>
> Jogo de fazenda noturna, idle, grátis — navegador ou Android, sem conta.
> ▶ https://reboclbrank-max.itch.io/ceifalume
>
> Day 9, good rain: the farm waters itself and the lantern is just company. Free idle night-farm, browser or Android. Made with Godot.
>
> #ScreenshotSaturday #indiedev #godot #idlegame #pixelart #jogosbr #gamedev

**Bluesky (≤300):**
> 🌧️ Dia 9 no Ceifalume: chuva boa. A fazenda se rega sozinha e a lanterna vira só companhia.
> Fazenda noturna, idle, grátis — navegador ou Android, sem conta.
> ▶ https://reboclbrank-max.itch.io/ceifalume
> #ScreenshotSaturday #indiedev #godot #idlegame

### Post 3 — Trailer (ter 23/09)
**Mastodon:**
> 🎬 15 segundos de Ceifalume 0.1: plantar, colher e negociar à luz da lanterna — e a fazenda continua trabalhando até 8 h depois que você fecha o jogo.
>
> Grátis, sem cadastro. ▶ https://reboclbrank-max.itch.io/ceifalume
> YouTube: https://youtu.be/tB449xupDzY
>
> 15 seconds of Ceifalume 0.1 — a night farm that keeps working up to 8 h after you close the game. Free, no sign-up.
>
> #indiedev #godot #trailer #idlegame #jogosbr #gamedev

**Bluesky:**
> 🎬 15 segundos de Ceifalume 0.1: plantar, colher e negociar à luz da lanterna — a fazenda continua até 8 h com o jogo fechado.
> Grátis, sem cadastro ▶ https://reboclbrank-max.itch.io/ceifalume
> #indiedev #godot #idlegame #trailer

### Post 4 — Android sem loja (sáb 27/09)
**Mastodon:**
> 📱 Ceifalume no Android sem passar por loja: baixa o APK (79 MB) direto da itch, instala, joga. Sem conta, sem cadastro, sem compra — só um vídeo opcional com recompensa, se você quiser.
>
> ▶ https://reboclbrank-max.itch.io/ceifalume (botão Download)
>
> Ceifalume on Android, no store needed: grab the APK on itch. No account, no purchase.
>
> #android #indiedev #godot #idlegame #jogosbr #freegame

**Bluesky:**
> 📱 Ceifalume no Android sem loja: APK direto da itch (79 MB), instala e joga. Sem conta, sem compra — só um vídeo opcional com recompensa.
> ▶ https://reboclbrank-max.itch.io/ceifalume
> #android #indiedev #godot #idlegame

## 6. Reddit — manual, pelo dono (maior tráfego, único canal que não dá para automatizar)

Quando quiser (sugestão: ter 14/10 ou antes se as métricas estiverem paradas), poste **em r/godot** com flair "project" e **r/IndieGaming**. Regras: 1 post por sub, não repostar, responder aos comentários. Título e texto (inglês, é o idioma dos subs):

**Título:** `I released a free idle night-farming game made with Godot — the farm keeps working up to 8h after you close it (browser + Android)`

**Texto:**
> Ceifalume is a small cozy idle game: plant, harvest and trade by lantern light. Offline progress up to 8 h, auto-save, original music. Free, no account, plays in the browser or as an Android APK. Made solo with Godot 4. Would love feedback on the pacing of the first days.
> Play: https://reboclbrank-max.itch.io/ceifalume

Anexar o **GIF** (Reddit aceita até 100 MB). Depois me diga "postei no reddit" que eu meço o efeito.

## 7. O que medir e quando

`python3 ferramentas/medir-marketing.py` (usa as chaves de `ferramentas/chaves.md`) coleta: itch views/downloads/compras, YouTube views do trailer, seguidores + engajamento de cada post no Bluesky e Mastodon, e grava uma linha em `METRICAS.md`. Rodar: **a cada "como estamos?"** e sempre **24 h depois de cada post**. Meta realista de 30 dias: **itch 16 → 150 views, 2 → 15 downloads**; sinal de alerta: 2 semanas sem variação → mudar de conteúdo (mais vídeo, menos texto) e acelerar o Reddit.


## 8. Relatórios semanais

### Semana 1 — 2026-09-19 (sáb), 20:35
**Números (Δ vs base de 18/09 02:11):** itch **44 views (+28, quase 3×)** · 2 downloads (=) · 0 compras · trailer 3 views (+1) · Bluesky post 1: **6 likes, 2 reposts, 2 respostas**, 0 seguidores · Mastodon: 0 em tudo.

**O que funcionou:** o Bluesky. O post 1 foi curtido por contas do nicho com alcance real — **GameBrief (2,4 mil seguidores)**, **Kevin Pedatte (4,2 mil, dev indie)**, freepixel.art (466), indiegameloveit (70, repostou) e Latest Gaming Buzz (repostou). Os +28 views da itch em 42 h coincidem com esses reposts — é a primeira evidência de que rede → itch funciona. As hashtags `#indiedev #godot #pixelart` são o que trouxe essas contas.

**O que não funcionou:** Mastodon zero (normal em conta com 0 seguidores e sem interação; lá o alcance vem de hashtags + tempo). Downloads não mexeram: as pessoas entram, olham, mas ainda não instalam → o post 4 (Android sem loja) e o trailer devem atacar isso.

**Ajustes:** (1) calendário corrigido para as datas reais (22/09 trailer, 26/09 Android); (2) próximo post do Bluesky mantém `#indiedev #godot #pixelart` sempre (foram as que renderam); (3) seguir ~10 contas do nicho no Bluesky (as que interagiram + curadores de Godot) — manual, moderado, feito pelo assistente na próxima rodada se o dono autorizar; (4) Mastodon: adicionar `#Godot #IndieGame` capitalizadas e responder quem aparecer.

**Próximo:** **terça 22/09 20h → "posta"** (trailer). Meta 30 dias segue: 150 views / 15 downloads — no ritmo atual (~14 views/dia) a de views é alcançável; downloads é a que precisa do conteúdo certo.

## 9. Diário de rodadas (interação diária)

| Data | Feito | Números depois |
|---|---|---|
| dom 20/09 12:30 | Bsky: respondi as 3 replies (indiegameloveit) em EN, 1 por post · +4 follows (pixel-forge — 1º seguidor, seguido de volta; Nat/ex-Godot; Loekni; Ash/Cartomantic) · 5 likes em posts #ScreenshotSaturday/#godot de devs pequenos · 1 repost (rathaelos, Godot) · Masto: 4 favoritos na tag, +3 follows (Taffer 610, upmultimedia 533, uberduck 332) | itch 47 views (+3) · Bsky 1 seguidor, 11 likes, 4 reposts, 3 respostas · Masto 0 |

| seg 21/09 19:11 | Bsky: 1 repost novo (sem replies) · +3 follows (GodotFest 480, possmonaut 547, untrustedlife 440) · 5 likes #indiedev/#godot · Masto: 4 favs, +3 follows (rwitherspoon, goodbinary, dos@librem 1,1k) | itch **54 views (+7)** · Bsky 1 seg, 12 likes, 5 reposts · Masto 0 |

| ter 22/09 20:30 | **Post 3 (trailer)** nas duas · Bsky: 1 reply nova (já respondida na thread) · **+3 seguidores** (looleveryday, astrariumdigital, crisplease — todos seguidos de volta) · +3 follows (hopscor.ch 3,6k, toptags 1,1k, 42zero) · 5 likes · Masto: 4 favs, +3 follows (ArmouredWizard, GodotSteam 427, partnano) | itch 57 (+3) · Bsky **4 seguidores**, 13 likes, 6 reposts · YT 4 · Masto 0 |

**✅ RESOLVIDO 22/09 ~21h — e-mail do Bluesky confirmado pelo dono** (reenvio via `POST com.atproto.server.requestEmailConfirmation`, sem body; `emailConfirmed: true`). Trailer republicado em **vídeo nativo**: https://bsky.app/profile/reboclbrank.bsky.social/post/3mw5fhok2tw2q (processamento 15 s). O post com card do YouTube foi **mantido** — já tinha 2 likes, 1 repost e 1 resposta. Histórico do problema: a API de vídeo recusou o upload (`unconfirmed_email`; `createSession` devolve `emailConfirmed: false`). O post 3 saiu com card do YouTube em vez de vídeo nativo (vídeo nativo rende bem mais no feed). Correção: abrir o e-mail usado no cadastro do Bluesky → clicar em "Confirm email" (ou Configurações → Conta → Email → reenviar). Depois disso o assistente repõe o trailer em vídeo nativo. Rota técnica que funciona: `getServiceAuth(aud=did do PDS do usuário, lxm=com.atproto.repo.uploadBlob)` → `video.bsky.app/xrpc/app.bsky.video.uploadVideo` → poll `getJobStatus` → `app.bsky.embed.video`.
| qua 23/09 19:15 | Bsky: 8 likes/2 reposts novos no trailer nativo; reply nova (indiegameloveit, 4ª) respondida · +3 follows (dotplus 2,6k, qaqelol 2,5k, ameerashour 1,4k) · 5 likes #indiedev/#godot/#pixelart · Masto: **seguidor novo ashi_246f** (seguido de volta), 4 favs, +3 follows (thoughtpunks 1,3k, silverspookgames 6,5k, qaqelol) · Discord 2 membros · Telegram 2 inscritos | itch **66 (+5)** · YT 6 · Bsky 4 seg, 21 likes, 8 reposts · Masto 1 seg |

Nota técnica: `public.api.bsky.app/…/searchPosts` devolve 403 para o sandbox; usar o mesmo endpoint em `bsky.social` com o JWT da sessão (funciona).

## 10. Canais sem API — feitos pelo assistente em 2026-09-22 (ordem do dono: "as que não precisam de chave, faça tudo")

| Item | O que foi feito | Verificação |
|---|---|---|
| **Landing page SEO** | `site/jogos/ceifalume/index.html` — título/description com as buscas-alvo ("jogo de fazenda grátis", "idle", "android", "navegador"), Open Graph + Twitter card (imagem 1280×720), JSON-LD `VideoGame` (+ trailer `VideoObject`, oferta grátis, plataformas, sameAs), trailer embutido, botões Jogar/APK/itch, `rel=me` para Bluesky/Mastodon | 200 no Pages; card do Bluesky extrai título+imagem ✓ |
| **index.html do site** | description nova, OG/Twitter, canonical, JSON-LD `Organization` (sameAs: itch, YouTube, Bluesky, Mastodon, GitHub), botão "Saiba mais" → landing | publicado `site@847e03e` |
| **sitemap.xml + robots.txt** | 4 URLs (raiz, landing, jogo web, privacidade) | 200 |
| **IndexNow** | chave `38c1335d28fcb40c020f0a1b7ae73e1a` em `site/38c1335d28fcb40c020f0a1b7ae73e1a.txt`; ping em `api.indexnow.org` (→ Bing, Yandex, Naver, Seznam, Yep) = **202** e `bing.com/indexnow` = **200** | reenviar a cada URL nova/alterada: `POST https://api.indexnow.org/indexnow` com host/key/keyLocation/urlList |
| **GitHub — repo `site`** | descrição nova, homepage = landing, **13 tópicos** (godot, godot4, idle-game, incremental-game, farming-game, android, html5-game, indie-game, free-game, cozy-game, pixel-art, brazil) | API ✓ |
| **GitHub Release v0.1** | renomeada "Ceifalume 0.1 — a fazenda não dorme", texto rico pt+en com tabela de links; assets já existentes (APK **20 downloads** pelo GitHub!, web.zip 3, trailer 2) | https://github.com/reboclbrank-max/site/releases/tag/v0.1 |
| awesome-godot (PR) | **NÃO feito, e não fazer:** a lista exige código aberto com licença livre; o Ceifalume é fechado → seria recusado | — |

**Descoberta:** o APK no GitHub Releases já tinha **20 downloads** (vs 2 na itch) — o link do site/README manda para lá. O medidor passa a contar isso também (coluna `gh_apk`).

**Google:** não tem IndexNow; indexa pelo sitemap sozinho (dias/semanas). Acelerar exigiria Search Console (login Google do dono) — opcional, sem pressa.

## 11. Canais que precisam de chave — links diretos para o dono (enviados 22/09)

| Rede | Criar conta | Gerar a chave | O que me mandar |
|---|---|---|---|
| **Lemmy** (Reddit do fediverso; comunidades !godot, !indiegaming, !gamedev) | https://lemmy.world/signup (usuário sugerido `reboclbrank`) | não tem chave — a API usa **usuário + senha** | usuário + senha da conta Lemmy |
| **dev.to** (artigos/devlogs com tags #godot #gamedev) | https://dev.to/enter (pode entrar com GitHub) | https://dev.to/settings/extensions → rolar até **"DEV Community API Keys"** → descrição `arena` → **Generate API Key** | a chave gerada |
| **Tumblr** (pixel art / indie) | https://www.tumblr.com/register | https://www.tumblr.com/oauth/apps → **Register application** (nome `arena`, website = landing, callback = `https://reboclbrank-max.github.io/site/`) → depois abrir https://api.tumblr.com/console/calls/user/info → **Show keys** | consumer key, consumer secret, token, token secret (4 códigos) |
| Threads (Meta) | conta Threads via Instagram | developers.facebook.com → app → Threads API (complexo no celular) | **não recomendado agora** |

## 12. dev.to + Tumblr ativos (2026-09-22 ~23h)

| Canal | Perfil | Post 1 | Papel no calendário |
|---|---|---|---|
| **dev.to** | reboclbrankmax | artigo em EN "I shipped a free idle night-farming game with Godot 4" (design + notas técnicas + pedido de feedback; GIF, canonical → landing) | **1 artigo por devlog** (0.2, pós-mortem, técnicas) — público de programadores; quinta 12h |
| **Tumblr** | reboclbrank | GIF + texto pt/en, 11 tags (indie games, pixel art, godot, cozy games…) | **espelho dos posts de sábado/terça** (GIF/vídeo funcionam bem lá; tags são tudo) |
| Lemmy | — | — | quando a conta for aprovada: 1 post em !godot e 1 em !indiegaming (texto do Reddit, §6) |

Regra de espelhamento a partir do post 4: cada "posta" publica em **Bluesky + Mastodon + Tumblr**; dev.to só quando há devlog/artigo.

## 13. Expansão de canais — links enviados ao dono em 2026-09-22 ("vamos fazer tudo que você consiga controlar")

Ordem fácil → chato. Para cada um: o que o dono cria, o que entrega, o que o assistente faz depois.

| # | Canal | Papel | Dono cria | Dono entrega | Assistente depois |
|---|---|---|---|---|---|
| 1 | **Telegram** | canal de avisos (retenção BR) | bot no @BotFather (`ceifalume_bot`) + canal público `t.me/ceifalume` com o bot como admin | token do bot + link do canal | posta novidades/updates via `sendPhoto`/`sendVideo`; link do canal na landing e na itch |
| 2 | **Discord** | comunidade (feedback, updates) | servidor `Ceifalume` + app em discord.com/developers → Bot token + Application ID | token + App ID | gera link de convite do bot, cria canais (#anúncios #feedback #bugs #geral), regras, webhook de novidades |
| 3 | **Hashnode** | espelho técnico do dev.to | conta + blog `reboclbrank.hashnode.dev`; token em hashnode.com/settings/developer | PAT | republica artigos com canonical → landing |
| 4 | **Buttondown** | newsletter "avise-me da 0.2" | conta `ceifalume`; API key em buttondown.com/settings/programming | API key | formulário de inscrição na landing; e-mail a cada versão |
| 5 | **Pinterest** | buscador visual, tráfego longo | conta business + app `arena` em developers.pinterest.com/apps (redirect URI = site) | App ID + secret | link OAuth (mesmo esquema do Tumblr: `?code=` cai no site) → boards "Ceifalume", "Cozy games", "Pixel art"; 1 pin por screenshot/GIF |
| 6 | **Threads** | rede indie em crescimento | app Meta com caso de uso Threads API; redirect URI = site; adicionar-se como Threads Tester e aceitar no app | Threads App ID + secret | link OAuth → posta espelho de Bluesky (500 chars, imagem/vídeo) |
| — | Lemmy | Reddit do fediverso | aguardando aprovação da conta | "aprovado" + senha | 1 post em !godot e !indiegaming |

Descartados com justificativa (2026-09-22): **X** — plano grátis extinto para novos devs; pay-per-use US$ 0,015/post e US$ 0,20 com link (fora do orçamento zero). **Medium** — tokens de integração não são mais emitidos para contas novas. **Instagram/Facebook/TikTok/YouTube upload** — exigem app review/conta business; ficam manuais (dono) com material pronto. **Reddit** — manual pelo dono (§6). **Steam** — taxa US$ 100 (adiado como a Play Store).

Vitrines sem API (fase seguinte, guiadas tela a tela): GameJolt, Newgrounds, CrazyGames (submissão), Uptodown/Aptoide, IndieDB, Product Hunt.

## 14. Telegram + Discord + Buttondown ativos (2026-09-22 ~23:50)

| Canal | Link público | Post/estado | Papel |
|---|---|---|---|
| **Telegram** | https://t.me/ceifalume | post 1 fixado (GIF + links) | cada "posta" também sai aqui (`sendAnimation`/`sendVideo`); avisos de versão |
| **Discord** | https://discord.gg/AnJr5nqx4K | regras + anúncio embed; 6 canais | #anúncios espelha os posts; #feedback/#bugs são a fonte de melhorias da 0.2 |
| **Buttondown** | https://buttondown.com/reboclbrank | 0 inscritos | e-mail só quando sair versão (0.2) |

Links dos três já na landing (`site@358c110`, seção "Acompanhe"). **Na itch**: não é possível via API sem zerar o Android (regra em chaves.md) — texto pronto para o dono colar no fim da descrição (Edit game → Description):

> **Comunidade:** Telegram (avisos de versão): https://t.me/ceifalume · Discord (feedback e bugs): https://discord.gg/AnJr5nqx4K · Newsletter: https://buttondown.com/reboclbrank

Espelhamento a partir do post 4: **Bluesky + Mastodon + Tumblr + Telegram + Discord #anúncios** (5 saídas por "posta"); dev.to/Hashnode para artigos; Buttondown por versão.

## 15. Threads — ATIVO em 23/09 ~19:40 (post 1: https://www.threads.com/@reboclbrank/post/DdpwAPmDdtY, trailer em vídeo). Causa do último erro: redirect cadastrado sem barra final. Espelhamento a partir do post 4: **6 saídas** (Bluesky, Mastodon, Tumblr, Telegram, Discord, Threads).

### Histórico do bloqueio
App `arena` OK (ID `1063985229878724`), redirect URIs cadastrados, convite de testador enviado (A) e aceito pelo dono (B). **Falta só o passo C** (o dono clicar "Permitir" no link de autorização) — travou por internet ruim; do lado público o link já responde com a tela de login (sem erro 1349168/1349245). Quando o dono tiver conexão: abrir `threads.com/login` no Chrome, depois o link de autorização; se a página final ficar em branco, copiar a URL da barra (`…/site/?code=…`) e mandar. O código expira em minutos → trocar imediatamente.
