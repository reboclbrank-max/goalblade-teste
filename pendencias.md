# Pendências — o que está em aberto

> # 🔒 REGRA FIXA Nº 1 (dono, 23/09/2026) — vale para este e para QUALQUER outro chat
> **Ao fim de CADA conversa (cada resposta que mudou algo — decisão, texto, número, credencial, plano), salvar tudo
> no repositório: commit + push verificado + hash informado ao dono.** Nada fica só na conversa. Se a resposta foi
> só conversa mas gerou decisão ou recomendação aceita, ela vira texto na base (registro-de-decisoes + arquivo do
> tema). Antes de encerrar qualquer resposta, perguntar-se: "isso já está no repositório?" Se não, salvar.
> Repositórios: `base` (privado, memória da empresa) e `site` (público). Credenciais: `ferramentas/chaves.md`.

## 📊 Painel (a primeira coisa que qualquer chat lê)

| # | Frente | Status | A bola está com | Próximo passo concreto |
|---|---|---|---|---|
| 1 | Ceifalume **0.1 LANÇADO** (site + itch.io + APK na release v0.1) | ✅ no ar | **assistente** | lojas grátis (1d) — após o dono aprovar o plano de marketing (M) |
| — | (item 1c fechado em 2026-09-17: trailer + Short no ar, link na itch e título do Short corrigidos; categoria do vídeo **ficou como veio**, decisão do dono — ver registro) | ✅ | — | — |
| 1d | Divulgação nas lojas grátis | ⬜ não iniciada | assistente | Samsung Galaxy Store → Aptoide → Amazon → Uptodown → Huawei |
| M | Marketing do 0.1 — **itch feita via API** (tags + descrição + GIF no ar) | ⏳ dono (7 cliques web-only, ~10 min) | dono | itens 1–7 de `projetos/01-ceifalume/marketing/auditoria-itch.md` §5 |
| 2 | **GOALBLADE** (jogo 2; antes "Rumo ao Estrelato") — futebol jogado em campo, controla só o seu jogador, 2D de cima; **plano B aprovado** (5×5 → 7×7 → 11×11; single → online futuro) | ✅ conceito + cronograma + **nome decidido 24/09** + **motor aprovado 24/09 (Godot 4.7.2)** + **arte v11 publicada** (`projetos/02-goalblade/`) | assistente | dono testar a v11; depois o "por fora"; abertura **20/10**; **0.1 em ter 24/11 20h** |
| 2 | Meta de 60 dias | ⏳ relógio rodando (dia 2/60 em 2026-09-15) | — | entregar Semanas 7 e 8 até 2026-11-12 |
| 3 | Arquivo-fonte da logo | ✅ resolvido em 2026-09-15 (`empresa/logo/`) | dono, só se tiver o original | opcional: RB em contornos (independe de fonte) |
| 4 | Segurança do token | ✅ regra corrigida em 2026-09-15 | o dono, se quiser revogar | cada chat pede token novo; nunca reusar valor antigo |
| 5 | Limpeza de `backup-site/` | ⚪ não existe neste ambiente | dono (autorizar) | ver item 5 — aqui não há o que apagar |
| 7 | Numeração oficial do jogo | 📌 decidir no lançamento | dono (Semana 8) | escolher 0.01 / 0.1 / 1.0 quando o jogo estiver terminado |
| — | (item 6 fechado em 2026-09-15: as duas seções `[rendering]` do `project.godot` foram unidas — está no registro de decisões) | ✅ | — | — |
| — | (item 8 fechado em 2026-09-15: rev C.2 publicada, `site 9926517` — ver §11) | ✅ | — | — |

### Como manter este arquivo

- Um item por frente aberta, com os campos fixos: **Status · Bola com ·
  Próxima ação · Bloqueia · Critério de "resolvido"**.
- Pendência **fechada** sai daqui e vira linha datada em
  `empresa/registro-de-decisoes.md`. Este arquivo só contém o que está vivo.
- A tabela "Painel" é obrigatória e precisa bater com o corpo do arquivo; se
  discordarem, o corpo manda e o painel é corrigido na mesma hora.
- Ideia boa que não é para agora não some: vira item 📌 (como o jogo 2).
- Este arquivo não guarda estado do jogo semana a semana — isso é do
  `projetos/01-ceifalume/progresso.md`.

## 🔴 1. CEIFALUME — rascunho no navegador do celular (rev C); interface será refeita

**Status:** ⚠️ retrabalho aprovado pelo dono (a interface) + 🔴 aguardando o teste do APK
**Natureza do que está publicado:** rascunho de teste, **não é versão** e não precisa
de mecanismo de atualização (decisão do dono em 2026-09-15 — ver registro).
**Bola com:** o dono
**Próxima ação do dono:** (a) mandar token para o push da rev C — sem isso a URL
ainda serve o build anterior às correções da auditoria; (b) depois, testar por um
destes dois canais e dizer o que achou (ritmo? o que trava? o que faltou?):
- **Navegador do celular** — agora é o caminho preferido, não instala nada:
  https://reboclbrank-max.github.io/site/ceifalume/ (QR em
  `projetos/01-ceifalume/divulgacao/qr-teste-celular.png`). **8,1 MB baixados por
  abertura** — o GitHub Pages entrega gzip: `index.wasm` chega em 8.145.118 B
  (medido com `curl -sI --compressed` em 2026-09-15), os outros arquivos somam
  ~100 KB. Carga medida com throttle: 3,3 s sem limite, **~12 s em 4G**, ~44 s em
  3G. Wi-Fi continua recomendado, mas não é mais obrigatório — e o número antigo
  ("~35 MB") era erro meu: era o tamanho cru do arquivo, não o que a rede entrega. Página adaptada em 2026-09-15: tela cheia, carimbo do
  rascunho, erro em texto grande. Na **rev C.1** (2026-09-15, auditoria + encaixe da interface + pacote limpo)
  entraram também: moldura que encaixa o jogo inteiro na tela sem cortar, botão
  de zoom (Ajustar / 150% / 200%), letra maior dentro do jogo e a interface
  refeita só no que era necessário para nada ficar fora da tela. Medido aqui dentro, antes de
  mandar para ele: em 844×390 o quadro fica 693×390, cabe inteiro e não precisa
  rolar (fonte de 17 px = 18,4 px físicos). Perguntar ao dono: a tela coube
  inteira? o zoom ajudou a ler? — ver `projetos/01-ceifalume/auditoria.md`.
- **APK** (`v0.1-teste-android`, link logo abaixo) — roda offline, mas cada
  mudança exige baixar de novo.
**Próxima ação do assistente:** depois do veredito → refazer a interface → novo
APK + republicar o web → Semana 7
**Bloqueia:** Semana 7 (arte/som) e, na sequência, Semana 8, itch.io e o card
do site
**Critério de "resolvido":** o dono aprovar a nova tela E a economia da Semana 6
continuar intacta (mesmos números, sem regressão de mecânica)

### Como se chegou aqui

- Desenvolvimento iniciado em **2026-09-14** (largada dos 60 dias).
- Semanas 1–6 feitas na largada: bico, campo, venda, mercado, loja e
  economia completa (6 plantações, ajudante, composteira, carroça, eventos).
- **2026-09-15:** o dono reprovou a interface da Semana 6 (textos pequenos
  demais, organização ruim) e avisou que o PC dele não roda o build web
  (erro de hardware/WebGL). Pediu APK para celular.
- **APK de teste publicado** (Release `v0.1-teste-android` no repositório
  `ceifalume`, modo paisagem):
  https://github.com/reboclbrank-max/ceifalume/releases/tag/v0.1-teste-android
- **O APK não se perdeu** (verificado em 2026-09-15 pela API do GitHub): o
  arquivo `ceifalume.apk` continua lá, íntegro, com 26.689.310 bytes
  (~26,7 MB). A Release vive no GitHub, não no chat — fechar o chat não apaga
  nada.
- ⚠️ **Contador de downloads da release: 0.** Ou seja, o arquivo nunca foi
  baixado por link. Como o repositório é privado, para baixar no celular é
  preciso **estar logado na sua conta do GitHub no navegador do aparelho** e
  abrir:
  https://github.com/reboclbrank-max/ceifalume/releases/download/v0.1-teste-android/ceifalume.apk
  (se o Android avisar "arquivo pode ser perigoso" por vir de repo privado /
  app de fonte desconhecida: permitir "instalar apps desconhecidos" para o
  navegador ou o gerenciador de arquivos).
- O que "refazer a interface" significa, item por item, está em
  `projetos/01-ceifalume/progresso.md` (seção "Roteiro da reformulação da
  interface"). Pipelines web **e** Android estão no mesmo arquivo.

## 🟡 V. Versão 0.2 — plano em `projetos/01-ceifalume/PLANO-0.2.md` (23/09)
Ciclo 3–4 semanas. **Achado:** jogo = 3,4 MB; motor Godot = 70 MB sem compressão no APK → `gradle_build/compress_native_libraries=true` leva o APK de 83,6 para ≈36,5 MB sem tocar no jogo. Coleta de feedback até 05/10 → escopo → lançamento ~19/10. Bug bloqueante = 0.1.1 imediato.

## ✅ M. Marketing do 0.1 — SETUP FECHADO em 2026-09-18 (operação contínua: ver seção M2)

> Estado final 2026-09-18: itch (tags, descrição+GIF, Android religado, devlog nº 1 publicado, perfil com foto+bio), YouTube (trailer), Bluesky e Mastodon (perfis + post 1). Só ficou de fora o tema Two column (opcional). Histórico abaixo mantido para referência.


**Status:** 🟡 em conversa — o dono perguntou se o assistente consegue "fazer o
marketing" e pediu para conversar **sem executar nada**
**Bola com:** dono (executar os 7 passos do kit itch) + assistente (medir
antes/depois pela API e registrar)
**Próxima ação:** dono escolher a frente de início (recomendação do assistente:
as lojas grátis, que já são o item 1d — distribuição primeiro, conteúdo depois)
**Bloqueia:** nada (o 0.1 já está no ar; marketing é crescimento)
**Critério de "resolvido":** plano aprovado frente a frente, com quem faz o quê
e o que o dono precisa providenciar

- **O que o assistente faz (R$ 0, sem custo nenhum):** escrever todas as
  listagens (nome, descrição, palavras-chave em pt-BR) das 5 lojas grátis;
  preparar assets (prints para as lojas, GIF do itch.io, cortes/Shorts do
  trailer); textos para redes sociais e respostas de comentário; pesquisar
  comunidades e canais de divulgação de jogos indie brasileiros; medir
  downloads por loja e ajustar o que não estiver rendendo.
- **O que precisa do dono:** criar as contas das lojas (todas grátis — o
  assistente guia passo a passo, como no AdMob); publicar/colar o que o
  assistente preparar; ~30 min por semana para postar e responder.
- **O que NÃO entra (regra do dono: orçamento-zero):** anúncio pago e qualquer
  coisa que custe dinheiro antes do jogo gerar receita.
- **Foco pedido pelo dono (2026-09-17):** mais pessoas vendo o jogo na
  itch.io + mais pessoas vendo o conteúdo no YouTube.
- **Levantamento (2026-09-17, só leitura, nada tocado):** perfil do dono =
  `reboclbrank-max.itch.io` — Ceifalume em `reboclbrank-max.itch.io/ceifalume`
  (publicado, Released, grátis, web jogável, trailer embutido, APK 79 MB).
  "Toque Rápido" confirmado como **rascunho (página 404, não pública)** e o
  dono decidiu que **não será usado**. **Auditoria completa da itch em
  `projetos/01-ceifalume/marketing/auditoria-itch.md`** — 10 achados: tags
  idle/incremental/farming/offline faltando, zero GIF, screenshot nº 1 = capa
  duplicada byte a byte, capa 630×500 (a 1024×500 já existe na base),
  descrição sem palavras de busca/link do canal, perfil sem marca nem bio, sem
  devlog, 0 comentários públicos, build do "Run game" a conferir no aparelho.
  Canal YouTube com 24 inscritos, 1 vídeo + 1 Short.
- **Plano acordado em conversa (aguardando o "vai" do dono):** (1) arrumar a
  página da itch — tags idle/incremental/farming, GIF do jogo na galeria, 1ª
  linha da descrição com as palavras de busca, links do canal + Short,
  confirmar preço explícito "grátis"; (2) YouTube — 1–2 Shorts novos por
  semana cortados do trailer (o assistente corta, o dono posta); (3) kit de
  divulgação para comunidades (Reddit r/idlegames, r/incremental_games,
  r/CozyGaming, r/IndieGaming, grupos BR de jogos indie) — o assistente escreve
  cada post, o dono cola; (4) devlog/updates na itch para avisar seguidores.
- Fila das lojas (item 1d): Samsung Galaxy Store → Aptoide → Amazon → Uptodown
  → Huawei. Play Store (US$ 25) só depois do AdMob acumular.
- **Execução do eixo itch (2026-09-17/18):**
  - 2026-09-17: dono colocou `idle`/`incremental`/`farming` manualmente; API
    key criada e guardada na base (`ferramentas/chaves.md`); kit pronto em
    `marketing/itch-kit-manual.md`.
  - **2026-09-18 (dono: "faça tudo por mim"):** assistente **descobriu o
    endpoint de escrita da itch** (`POST api.itch.io/games/{id}`, form,
    objeto inteiro — regras em `chaves.md`) e **aplicou via API, verificado
    no HTML da página pública:** as **10 tags finais** · **descrição nova**
    (SEO + links) · **GIF embutido no topo** (hospedado em
    `site/media/ceifalume/`, repo público, GitHub Pages).
  - **Incidente do assistente (mesmo dia):** encoding de tags errado
    (`tags[]`) zerou as tags (10→1, corrigido na hora) e **zerou a flag
    `p_android`** (campo não escrevível — testado 3 nomes, ignorados).
    **Consequência que ficou: dono remarca "Android" em Platforms (1 clique).**
  - **Resto é web-only (7 itens, ~10 min, em `auditoria-itch.md` §5):**
    remarcar Android · excluir duplicada (id 30040026) · (opcional) GIF na
    galeria · perfil (imagem + bio) · tema two column · devlog nº 1 · conferir
    "Run game" no celular. Todos os textos prontos no kit.
- **Push: RESOLVIDO (2026-09-17, histórico):** base e site publicados e verificados
  com `git ls-remote` (o site ganhou a pasta `media/ceifalume/`, documentada no
  README do `site`). As antigas referências a cofre de token foram invalidadas
  em 25/09; usar apenas credencial temporária de sessão.

## 🔴 0. COMANDO ÚNICO "trabalhe" (23/09) — `empresa/CALENDARIO-TRABALHE.md`
Dono manda só "trabalhe" 1×/dia (sáb 17h, ter 20h, qui 12h, demais 20h). Assistente confere a data (Fortaleza), lê o calendário e faz tudo do dia (rodada + medição + post do dia + o que estiver marcado), commit+push, resumo curto. **Próximo: qui 24/09 12h → post de coleta + rodada.**

## 📌 1c. Operação multi-jogo (23/09) — `empresa/FUNCOES-E-OPERACAO.md`
**Próxima ação:** na abertura do jogo 2 criar `projetos/_modelo/`, medidor multi-jogo, tabela por jogo no topo deste arquivo. **Bola com:** assistente (gatilho: dono escolher o jogo 2 em 05/10).

## ✅ 2. GOALBLADE — jogo 2 (nome decidido 24/09; aprovado 23/09, plano B)
`projetos/02-goalblade/conceito.md` + `cronograma.md`. 5 semanas a partir de 20/10; 0.1 (5×5, Copa do Bairro, 3 atributos) em 24/11. Pendente do dono (sem pressa): confirmar a posição inicial (atacante/meia). Nome já decidido em 24/09. **Motor APROVADO pelo dono em 24/09: Godot 4.7.2** (cláusula dele: "se não der bom, migramos para outro") — estudo em `projetos/02-goalblade/motor-e-movimento.md`; `conceito.md` §2 atualizado. **Correções do dono no visual (24/09):** bonecos de verdade e campo de verdade; **campo cresce com o número de jogadores**; **câmera segue a bola com opção de seguir o jogador**. **Decisão do dono (24/09): começar só com o 5×5** ("não há necessidade de aplicar vários modos"). **GoalBlade v11 (25/09):** o MOTOR RB refinou o passe final de arte: volume suave de pele e tecido, costura dupla, sombra de gola/barra, microdobras, sola/cadarço/cravos da chuteira, número orientado com o corpo e sombra de contato em três camadas. O jogo adiciona perspectiva de escala (mais perto = ligeiramente maior) e ordem de profundidade. A folha mantém 768 quadros — 12 identidades, 8 direções, 8 poses — em 144×160; filtro linear e escala base 0,56. Fotos `estudos/jogo-v11-campo.png` e `jogo-v11-jogador.png`; Web republicada no link fixo. Simulações: 0 anomalias, 0 travamentos, CPU 0,17–0,19 ms/quadro. **Falta:** veredito do dono no link fixo; depois o "por fora".

**GoalBlade v8/v7 (histórico):** v7 tornou o campo uma imagem de arte (grama com textura, desgaste, sombra das arquibancadas, torcida, gols com rede e vinheta); v8 levou a primeira folha de sprites para dentro do Godot. Link fixo: `https://reboclbrank-max.github.io/site/goalblade/`.

**GoalBlade v6 publicado (24/09, noite) — ordem: "ainda ta travando ao extremo … controle horrível, sem start e select":**
**link fixo de teste: https://reboclbrank-max.github.io/site/goalblade/** (publicado no repositório `site`, pasta `goalblade/` — não morre mais; o túnel antigo caiu de novo).
Feito: desenho em 1280×720 lógico (fim do gasto com a resolução física da tela), teto de 60 fps, imagem do campo 2560→1280,
**MODO LEVE automático** (75%/62% + volta sozinho), linha de fps no canto + diagnóstico na pausa, **START e SELECT com função**
(começar/pausar/jogar de novo e trocar a câmera), controles posicionados pelo tamanho real da tela, zona morta no direcional,
aviso de girar o celular. Conferido: pck `797c4806…` (79.972 B) igual no local e no link. **Falta do dono:** testar a build v10 e responder se o novo realismo 2D chegou ao nível desejado. O servidor virou arquivo do repositório (`servidor-teste.py`).

**Rodada de marketing 24/09 12h (ordem do dono):** post de coleta de opinião publicado em **5 canais** (Bluesky, Mastodon c/ GIF, Telegram, Discord #anúncios, Tumblr — links em `projetos/01-ceifalume/FEEDBACK-0.1.md`); **Threads bloqueado pela Meta** (passos para destravar em §5 do mesmo arquivo); criado o caderno **`FEEDBACK-0.1.md`** com o **texto pronto do devlog nº 2** para o dono colar na itch. Medição das 12:58 gravada em `marketing/METRICAS.md`. **Threads resolvido em 24/09 à noite** (https://www.threads.com/@reboclbrank/post/DdrnwECD5u-) — rodada de 24/09 fechou **6 de 6**. **Falta do dono:** nada no marketing — o devlog nº 2 **já está no ar** (https://rebocl-brank.itch.io/ceifalume/devlog/1675714/01-no-ar-a-fazenda-no-dorme), com o título a corrigir quando puder. **Ceifalume 0.1 — 71 views, 2 downloads (itch), 22 APK.**

**Rascunho atual para conferir:** `projetos/02-goalblade/prototipos/5x5-basico.html` (históricos: `visual-e-camera.html` com os 3 formatos e `movimento-teste.html`, reprovado no visual). **Ordem do dono em 24/09 ("Faça os 3, leve o jogo pro Godot já para iniciar o trabalho real"):** IA nova dos outros 9 + **port do jogo para o Godot 4.7.2** + visual caprichado — **feito e testado**: o jogo agora é projeto de verdade em **`projetos/02-goalblade/jogo/`** (campo, bonecos, controles de toque, goleiro, IA, placar, fim de jogo), com a versão de navegador exportada. **Ordem do dono (24/09, 4ª resposta):** "primeiro vamos criar a partida para eu testar e depois vamos criar o por fora do jogo" → **partida fechada**. **O dono testou e não gostou (24/09, 5ª resposta):** "tá desorganizado, não é um jogo 2d, tá mais pra 1d, jogo muito rápido, sem estratégia, sem bonecos reais, jogo trava muito, tá muito mal trabalhado" → **versão 4 feita**: campo inteiro na tela com profundidade (sombras, arquibancada, redes), bonecos maiores com número na camisa, **ritmo 30% mais lento**, goleiro que defende e IA que joga de passe (placar 1×0 e 2×0 em vez de 13×15), e o que pesava por quadro foi retirado (**0,10 ms de CPU por quadro**). **Falta:** o dono **ver de novo** — celular: https://bids-adware-thriller-subject.trycloudflare.com/index.html · PC (programa .exe): https://bids-adware-thriller-subject.trycloudflare.com/pc/ — e dizer se agora está no caminho. **Depois disso: o "por fora"** (menu, criar jogador, Copa do Bairro).

- **Nome DECIDIDO em 24/09: GOALBLADE** ✅ (gol + *blade* = "o gol cortante"). 7 rodadas de verificação: o dono escolheu GoalStrike, que **caiu na checagem final** (plataforma de fantasy football + "SuperGoalStrike" na itch.io); o **GoalBlade passou limpo** (0 na itch.io; na web só um desenho de fã no DeviantArt). Tudo em `projetos/02-goalblade/nomes.md`. **Próximo uso do nome:** repositório novo `goalblade` (privado, com autorização do dono na abertura de 20/10) e página `itch.io/goalblade`.

## 🟡 1b. (histórico) Jogo 2 — planejado (23/09): pequeno, em sequência após a 0.2

**Estratégia:** `empresa/ESTRATEGIA-CATALOGO.md`. **Conceitos entregues em 23/09 (antecipado):** `projetos/02-proximo-jogo/CONCEITOS.md` — A Vaga-Lume (arcade, 2 sem), **B Brotos da Lua (merge no mundo do Ceifalume, 2–3 sem) ⭐**, C Fogueira (defesa leve, 3 sem). **23/09 (mais tarde): dono quer um jogo NOVO, ideia dele — os 3 conceitos são reserva. Bola com o dono:** descrever a ideia. Abertura após a 0.2 (~20/10); 0.1 ~10/11. **RPG de coleção** abaixo permanece guardado como jogo 3–4.

### (histórico) Candidato original: RPG de coleção

**Status:** 📌 guardado — adiado de propósito, não esquecido
**Bola com:** ninguém (reabrir depois do lançamento do Ceifalume)
**Próxima ação:** nenhuma agora; registrar a decisão no `registro-de-decisoes.md`
quando o dono reabrir
**Bloqueia:** nada (é o que vem depois)
**Critério de "resolvido":** existir conceito + cronograma aprovados para o jogo 2

Ideia do dono guardada para o futuro: RPG de coleção + cartas/personagens +
batalhas automáticas + evolução de equipe. Avaliar depois do lançamento de
Ceifalume, com mais experiência e possível verba para desenhos. Personagens
colecionáveis encaixam na ideia de troca entre jogadores (fase online).

### Histórico — comparações anteriores (superadas)

Comparação JOGO vs APP apresentada ao dono em 2026-09-14:

| Critério | Jogo (Godot → itch.io/web) | App (Flutter → Google Play) |
|---|---|---|
| Custo até publicar | R$ 0 | US$ 25 (taxa única) |
| Tempo até publicar | mesmo dia em que terminar | +2 a 3 semanas: regra do Google para contas pessoais novas exige 12 testadores usando o app por 14 dias consecutivos, depois aprovação de produção |
| Monetização inicial | baixa (itch.io: você escolhe a taxa, padrão 10%, pode ser 0%; comum "pague o quanto quiser") | caminhos mais claros (venda, assinatura, AdMob), mas depende de usuários |
| Encaixe na meta de 60 dias | folga | apertado/arriscado |

**Resultado:** o dono escolheu JOGO.

## ⏳ 2. Meta de 60 dias

**Status:** ⏳ relógio rodando desde 2026-09-14
**Bola com:** — (o que trava o cronômetro hoje é a pendência 1)
**Próxima ação:** cumprir Semana 7 e Semana 8
**Bloqueia:** o lançamento — e lançar é a meta
**Critério de "resolvido":** Ceifalume no ar, jogável do começo ao fim por
qualquer pessoa, dentro dos 60 dias

A largada foi dada em **2026-09-14**, quando o dono aprovou conceito +
cronograma e mandou começar a Semana 1.

| | |
|---|---|
| Dia 1 | 2026-09-14 |
| Dia 60 (prazo final) | **2026-11-12** |
| Fotografia em 2026-09-15 | dia 2 de 60 (58 restantes) |

- **Objetivo:** 1 projeto pequeno e TERMINADO — no caso, CEIFALUME aberto por
  qualquer pessoa, jogável do começo ao fim, sem travar e sem explicação
  (critério literal em `projetos/01-ceifalume/conceito.md`, item 7).
- **Onde acompanhar:** plano semanal em `projetos/01-ceifalume/cronograma.md`;
  estado real e pipelines de build em `projetos/01-ceifalume/progresso.md`
  (atualizar a CADA sessão — o cronômetro não é cobrado em outro lugar).
- **Ritmo até agora:** 6 das 8 semanas entregues no primeiro dia de trabalho.
  Folga grande no papel — o que consome tempo é justamente o acabamento
  (Semana 7: arte/som; Semana 8: salvamento, offline, itch.io), que é onde o
  cronograma proíbe economizar.
- **Regra de atraso (já no cronograma):** semana estourou → corta conteúdo do
  fim, nunca corta o polimento final.
- **Não fazer:** rediscutir escopo, adicionar animais/prestígio/online na v1,
  ou adiantar semana sem comando do dono.

## ✅ 3. Arquivo-fonte da logo — RESOLVIDO em 2026-09-15 (com uma ressalva)

**Status:** ✅ os arquivos da marca existem no repositório (`base` → `empresa/logo/`)
**Bola com:** o dono, só se ele tiver o arquivo original do designer
**Próxima ação:** nenhuma obrigatória
**Bloqueia:** nada (itch.io e lojas já têm o ícone 512)
**Critério de "resolvido":** atendido — SVG mestre + PNGs em 512/192/180/64/32

- Como foi resolvido: a logo aprovada **só existia embutida no `index.html` do
  site**. Ela foi resgatada de lá (mesmos caminhos, mesmas cores, sem
  redesenho), virou `logo-rb-dourada.svg` e foram gerados os renders PNG nos
  tamanhos de loja. Inventário e forma de regerar: `empresa/logo/LEIA-ME.md`.
- ⚠️ **Ressalva técnica:** o SVG usa `<text>` com a fonte Georgia, então o
  desenho da letra depende da fonte instalada no aparelho de quem abre. Para
  loja/imprensa o ideal é uma versão com o **RB em contornos** (curvas, sem
  dependência de fonte). Barato de fazer quando o dono mandar o arquivo
  original do design — ou convertendo as letras em caminhos no Inkscape.
- Se o dono tiver o vetor original (o arquivo que ele aprovou), ele substitui o
  `logo-rb-dourada.svg` e os PNGs são regerados com o comando do LEIA-ME.

## 🟡 4. Segurança do token

**Status:** ✅ regra corrigida em 2026-09-15
**Bola com:** o dono, apenas se ele quiser revogar (não insistir)
**Próxima ação:** nenhuma — é política de uso, não tarefa
**Bloqueia:** nada
**Critério de "resolvido":** os próximos chats seguirem a regra abaixo sem precisar de lembrete

- Em **2026-09-14** um token de acesso total foi colado em chat
  (prefixo omitido). O usuário foi orientado a revogá-lo, mas
  **dispensou a troca** ("ninguém tem acesso a esse chat") — não insistir
  mais no assunto.
- Em **2026-09-15** o dono forneceu **outro token** para o trabalho da
  sessão (valor diferente do de 2026-09-14). Ou seja: o token muda de
  sessão para sessão.
- **Regra corrigida (a anterior estava errada):** não existe "o token ativo
  do dono" guardado nesta base. Cada chat usa **somente** o token que o
  próprio usuário colar naquele chat, e só naquele chat. Nunca assumir que
  um valor antigo ainda vale, nunca reaproveitar token de conversa anterior
  e nunca registrar o valor de um token em arquivo deste repositório.
- Para mexer na `base`, no `site` ou no `ceifalume`: pedir um token novo ao
  dono, com escopo mínimo (`repo` basta).
- No ambiente deste tipo de sessão, o token é gravado só em arquivo temporário
  de credencial (`/tmp/.tk` + `GIT_ASKPASS`) e apagado logo depois do push —
  conferir com `ls` que sumiu.
- Se um dia ele decidir revocar/girar: só conferir scripts locais que ainda
  referenciem o valor antigo — nada aqui na `base` guarda valor de token.

## ⚪ 5. Limpeza opcional

**Status:** ⚪ não se aplica a este ambiente
**Bola com:** o dono (autorizar) — e só no chat onde a pasta existe
**Próxima ação:** nenhuma aqui
**Bloqueia:** nada
**Critério de "resolvido":** a pasta não existir mais no espaço de trabalho onde vive

A pasta local `backup-site/` do espaço de trabalho contém cópia do repositório
antigo apagado (só lixo de teste, nada com valor). Pode ser apagada quando o
dono autorizar.

- **Verificado em 2026-09-15:** o espaço de trabalho deste chat tem apenas a
  `base` clonada — não existe `backup-site/` aqui. Ela vive no espaço de
  trabalho de outra sessão. Nada foi apagado nesta sessão e nada havia para
  apagar.

## 📌 7. Numeração oficial do jogo (só no lançamento)

**Status:** 📌 aberta de propósito — não decidir agora
**Bola com:** o dono
**Próxima ação:** nenhuma até a Semana 8
**Bloqueia:** nada (nenhum rascunho depende de número de versão)
**Critério de "resolvido":** existir versão oficial escolhida no dia em que o jogo
for publicado no itch.io

- O dono deixou claro em 2026-09-15: enquanto não há lançamento, não há versão.
  Os builds de agora são rascunhos datados; a escolha entre `0.01`, `0.1`, `1.0`
  ou outro esquema se faz **quando o jogo estiver terminado**, junto com a página
  do itch.io.
- Só nesse momento entram em cena as coisas que eu estava querendo adiantar:
  `versionCode` crescente, `retain_data_on_uninstall`, política de update e
  changelog. Antes disso é peso morto.
- O jogo chega ao cliente **inteiro e novo** — é essa a promessa da marca nesta
  fase: um jogo acabado, não um app que se conserta pelo caminho.


## ⚠️ 9. A letra no celular ainda é pequena — e a causa é o tamanho base

**Status:** ⚠️ aberta de propósito; só fecha com a reformulação da interface
**Bola com:** o dono (a reforma é a frente que ele mesmo apontou)
**Próxima ação:** reforma da interface com "texto grande" como critério de aceite
**Bloqueia:** nada (o zoom da página é o alívio parcial enquanto isso)
**Critério de "resolvido":** o dono dizer que consegue ler sem zoom

- O projeto é 1280×720 com `stretch/mode="canvas_items"`. **Medido no navegador
  (não é mais estimativa):** no celular deitado (844×390 CSS, DPR 2) o quadro fica
  em 693×390 e cabe inteiro, com escala ×0,542 → uma fonte de 17 px vira
  **18,4 px físicos**; em pé (390×844) a escala cai para ×0,305 → 10,4 px,
  inviável (daí o aviso para girar). Nenhum dos dois precisa rolar a página.
- O que falta não é aumento de fonte, é **menos coisa na tela e maior**: a reforma
  da interface. Números e método em `projetos/01-ceifalume/auditoria.md`
  (seção "O que foi verificado depois disso").

## 10. Motor: o que foi instalado, o que ficou de fora, e a fila que isso destrava

**Status:** ✅ instalado e medido (2026-09-15, 2ª rodada) · ⚠️ duas coisas abertas
**Bola com:** o dono (decidir a portagem para 4.7 depois do lançamento)
**Próxima ação dele:** mandar token para o push da **rev C.1** e dizer o que achou
**Bloqueia:** nada

- **Instalado e no caminho:** `ripgrep 14.1.1`, `fd-find` (`fdfind`), `ffmpeg 7.1.5`
  — e o **Godot 4.7.2 ao lado do 4.3** (`~/.cache/ferramentas/novo/godot`, templates
  Web em `~/.local/share/godot/export_templates/4.7.2.stable/`).
- **Medido, sem eufemismo:** busca no código do jogo leva 3 ms (grep) ou 6 ms (rg)
  — "motor melhor" **não** acelera minhas respostas neste projeto. Os gargalos reais
  são o download do toolchain em chat novo e os 7–30 s de render/carregamento sob
  GPU por software (2 CPUs, 1,8 GB).
- **Por que o jogo continua no 4.3:** o 4.7.2 produz layout e testes idênticos,
  `.wasm` +2,1 MB gzip na rede e o template novo ignora a moldura mobile. Tabela
  completa no registro de 2026-09-15 (2ª rodada), §2.
- **Aberta 1 — portagem para 4.7.x (Semana 9+):** reescrever o encaixe da página
  para o template novo e re-medir os 3 perfis; ganhos esperados: `pck` −18 KB,
  `VirtualJoystick`, erro claro de ETC2/ASTC, templates seletivos.
- **Aberta 2 — suspeita de corte fino no último botão da sementeira:** no frame do
  vídeo em 1280×720 o texto "Flor de Lume (250)" parece perder o parêntese final,
  e a medição da rev C diz que aquele botão tem **folga zero** (mínimo = 163,0 px =
  tamanho recebido). A checagem atual só acusa corte com 1 px de tolerância, então
  pode estar no limite sem acusar. Como fechar: apertar o limiar de
  `prova_visual.gd` para `min.x > size.x` (sem o `+1`) e medir de novo; se bater,
  a correção é dar largura à linha (`LadoDireito` com `size_flags_horizontal = 3`,
  sobram ~100 px de espaço morto à direita em 1280).
- **Novo canal de teste que não depende de aparelho:** o vídeo de jogabilidade
  (`projetos/01-ceifalume/verificacao/ceifalume-jogando.mp4`, regerável com
  `grava_jogo.gd` + `ffmpeg`). Serve para ritmo/economia; **não** serve para toque,
  temperatura, ou gosto — esses continuam sendo do dono.

## 11. Fechado e aberto depois da rev C.2 (2026-09-15, 3ª rodada)

**Fechado:**
- ~~empurrar a rev C~~ → **publicado** (base `c9e7027`, jogo `e32514d`, site
  `9926517`); o artefato no ar passou a ser o da rev C.2 (`.pck` 87.312 B).
- ~~Loja exige rolo em 1280×720~~ → virou `FaixaLoja` em grade (até 4 colunas) no pé
  da tela; 7 itens, nenhum rolo; medido nos 3 perfis de janela.
- ~~suspeita de folga zero no último botão da sementeira~~ → era defeito real e pior
  do que parecia: o preço 2500 perdia o último dígito. Corrigido e confirmado por
  OCR + régua de folga.
- ~~~35 MB por abertura~~ → substituído pelo medido: 8,1 MB entregues (gzip do Pages).

**Aberto (o que depende do dono):**
1. Teste no celular + veredito de gosto/ritmo (validação, não verificação). Perguntas
   a responder por ele: leu sem zoom? a faixa no pé ficou alcançável com o polegar?
   o ritmo Dia 1→3 está chato?
2. Semana 7 (arte e som). Para medir som: `ffmpeg` já serve para LUFS/pico/silêncio;
   gravar a saída do jogo pede `pulseaudio` + `alsa-utils` (~150 MB).
3. Semana 8: save, offline de 8 h, tela de título, itch.io, numeração.
4. Em pé (390×844) a escala do jogo é ×0,305 → fonte de 17 px vira 10,4 px físicos.
   O aviso "gire o celular" é a resposta atual. Alternativa, se ele quiser: layout
   vertical próprio (não "encolher o horizontal").
5. Portagem para Godot 4.7.x na Semana 9+: tabela de custo/benefício já medida em
   `empresa/registro-de-decisoes.md` (2026-09-15, 2ª rodada, §2) — e lembrete: o
   template novo ignora a moldura mobile, então é reescrever `web/gerar-pagina.py`
   + re-medir os 3 perfis.
6. ✅ **Gancho de teste FEITO na 8ª rodada** (rev C.5): 5 toques no título abrem o
   painel (moedas, 24 campos, celeiro, zerar), só com `rebocl/teste_livre=true` —
   a Semana 8 desliga. (Era: "aguardando o vai dele".) Opções B e C superadas.: (A) 5 toques no título abrem um painel de teste — encher moedas,
   comprar até 24/24, encher celeiro, zerar — ligado por
   `ProjectSettings: rebocl/teste_livre`, falso no build de lançamento; (B) zero
   código: eu renderizo o estado 24/24 aqui na bancada e mando imagem/vídeo;
   (C) rebalancear o `×1,8` (item 7 acima). Minha recomendação: B agora e A+C juntos.
7. **Semente fixa para teste de imagem (`CEI_SEMENTE` no jogo):** sem ela, o
   golden-image não pode exigir 0 px — medido, o mesmo build renderizado duas vezes dá
   20 px porque o preço do dia usa `randi_range`. Custa duas linhas no `_seed()` do
   roteiro e libera a camada 7 da auditoria (comparar com tolerância zero). Vale fazer
   junto com a Semana 7, que já mexe no `roteiro_principal.gd`.
7. **O limite dos campos é inatingível com a curva atual (número, não opinião).**
   Custo do campo = `50 × 1,8^k`; do 5º ao 24º soma **7.967.587 moedas** e o 24º
   sozinho custa 3.541.177. Renda por campo-dia (1 unidade por colheita × preço
   base): Nabo 24,0 · Milho 17,5 · Trigo 22,0 · Tomate 25,3 · Abóbora 31,1 ·
   Flor de Lume 45,8. Jogando com a melhor cultura: 8 campos no dia 2, 12 no dia
   16, 16 no dia ~117, 20 no dia ~944 e o **24º por volta do dia 8.052** ≈ **134 h
   reais** de tela ligada (dia = 60 s). Com Trigo, 280 h. Tabelas de alternativa,
   mesma renda: ×1,6 → 24º no dia ~1.044; ×1,45 → ~202; ×1,35 → ~65; ×1,25 → ~21.
   Decisão do dono: baixar o multiplicador (ou premiar escala) antes de prometer
   "24 campos" em material de divulgação. Ferramenta para re-medir:
   `ceifalume/sim_limite.gd` (bot guloso, `CEI_DIAS=5000`).
8. ⚠️ Balanceamento: os preços do dia variam de `base*0,5` a `base*2` e a Feira dobra;
   com `HFlowContainer` os rótulos ganharam folga, mas o *número* continua a decisão
   que ele precisa confirmar jogando.

## 12. O limite dos campos, medido (2026-09-15, 4ª rodada)

- **24/24 campos no dia 9.689 de jogo ≈ 161 h reais** (bot guloso, motor aberto,
  `ceifalume/sim_limite.gd`). Com Trigo no lugar da melhor cultura: ~280 h. Para o
  dono decidir com número em vez de intuição: ×1,45 → dia ~202; ×1,35 → ~65;
  ×1,25 → ~21. **Nada foi mudado no jogo** — decisão dele.
- **Chão de design descoberto de graça:** plantar tudo com o celeiro quase vazio e
  não vender pequeno quebra no Dia 1 (moedas 0). O jogo tem saída (vender quando
  quiser + "fazer um bico"), mas o primeiro bot que escrevi caiu exatamente aí. Se
  o dono quiser um piso, a alavanca natural é o preço do bico ou a semente inicial.
- **Para *ver* o limite hoje, sem tocar no jogo:** `CEI_CENARIO=limite` na prova
  visual (evidência em `projetos/01-ceifalume/verificacao/estado-limite-*.png`).
- **Para *jogar* o limite no celular**, falta o gancho de teste (item 6 acima):
  5 toques no título → painel com moedas/24 campos/celeiro/zerar, ligado por
  `rebocl/teste_livre` no `ProjectSettings`, falso no build de lançamento.
  Aguardando o "vai" do dono — é mudança em código do jogo.

## 13. Veredito do aparelho chegou (2026-09-15, 5ª rodada) e o que ele destrava

- ✅ **Teste no celular: feito e aprovado nos termos do dono** ("ficou bom, tem
  potencial"). A tela atual está aprovada como base de trabalho; a rev C.2 é o
  artefato publicado e verificado (`.pck` 87.312 B no ar = local, selo no HTML).
- **Em aberto, por decisão dele:** (a) painel de teste por 5 toques no título (item 6);
  (b) a curva de custo dos campos — tabela medida no registro da 5ª rodada (×1,80 →
  24º no dia ~9.689; ×1,45 → ~565; ×1,35 → ~292; ×1,25 → ~182). Recomendação
  registrada: ×1,45 + `CEI_SEMENTE` antes de mexer em mais número.
- **Próxima frente do cronograma (Semana 7, ordem ajustada):** 1) interface ✓ feita e
  aprovada; 2) web ✓ publicado — o APK segue bloqueado *aqui dentro* (sem JDK/SDK
  Android no sandbox; ~40 min e ~1,3 GB se um dia for necessário); 3) **arte e som** —
  é por onde se continua. Som primeiro: é código + medível (LUFS, pico, silêncio com o
  `ffmpeg` instalado) e não depende do traço dele; a arte final depende.

## 14. Som entrou (6ª rodada) — o que fica para o dono decidir agora

- **Tema musical:** o bus `Musica` existe e está pronto; não inventei melodia porque
  é decisão de gosto, não de verificação. Quando ele mandar/tiver o arquivo, entra como
  `arte/som/musica-tema-01.ogg` (loop, integrado em torno de -20 LUFS, sem pico).
- **Efeitos finais:** os quatro atuais são provisórios e estão rotulados assim no
  `arte/LEIA-ME.md`. Alvo para troca: pico -6 ±3 dBFS por arquivo (medir com
  `base/ferramentas/medir-som.py`), e **`--import` antes de medir**.
- **Teste no aparelho com som:** preciso e só ele responde — política de áudio do
  iOS/Android real não é reproduzível aqui. Perguntas: o som tocou sem ele tocar na
  tela? o botão `Som: ligado` ficou alcançável e visível? o efeito de colher é
  gostoso ou irritante em repetição (é o mais tocado do jogo)?
- **Custo aceito:** o som custou +0,13 MB na abertura (`.pck` 262.288 B). Se um dia
  isso pesar, a alavanca é baixar a taxa dos `.ogg`, não tirar o som.
- Seguem abertas da 5ª rodada: painel de teste por 5 toques (item 6) e layout
  vertical para o modo em pé (10,4 px). Semana 8 (save/offline/tela de título/itch.io)
  é a próxima depois da arte.

## 15. Abertura RB + pronto para lançar — rev C.10

**Status:** ✅ C.10 (pck 2353952, selo C.10) · 91/91 + 27/27 · ⏳ decisão lança + preço com o dono
**Bola com:** o dono (desenhar) → depois o assistente (plugar + publicar)
**Próxima ação do dono:** mandar o **Nabo piloto**: 3 arquivos (semente, broto,
pronto), 128×128 PNG com fundo transparente, planta nos 2/3 de baixo (o rótulo
do campo ocupa o topo), estilo realista, clima aconchego. Anexar no chat e dizer
o que é — renomear e encaixar é trabalho do assistente.
**Bloqueia:** Semana 8 (polimento/lançamento)
**Critério de "resolvido":** 18 sprites de planta + fundo no jogo, validados na
prova visual e aprovados pelo dono no celular

- Contrato de nome e tamanhos: `ceifalume/arte/LEIA-ME.md` (§ Fiação + Manifesto).
- Ordem: Nabo piloto → outras 5 plantas → fundo → resto (corte nunca nos sprites).
- Reteste do som (roteiro no §14, agora com 6 sons) continua pendente em paralelo.
- Estreia do painel: 5 toques no título em 2 s (só funciona com a flag de dev).
- Save: fechar e reabrir mantém tudo (só ele valida no navegador real).
- Semana 8: otimizar o fundo (PNG 1,0 MB → JPEG/qualidade; abertura hoje ~9,2 MB).

## 16. Intro v2 RB — rev C.11

**Status:** ✅ C.11 (pck 2344272, selo C.11) · 91/91 + 28/28 · ⏳ decisão lança + preço com o dono
**Bola com:** o dono (jogar a C.11 e dar o veredito)
**Próxima ação do dono:** abrir o jogo no celular, ver a entrada nova da RB
(logo acende + vagalumes + vinheta) e responder: gostou? lança ou não? preço
(grátis com doação / pago)?
**Bloqueia:** Semana 8 (polimento/lançamento)
**Critério de "resolvido":** veredito do gosto + decisão lança/não-lança + preço

- Intro v2: `abertura.tscn/gd` (fade + brilho + `Vagalumes` + `Vinheta`) +
  `arte/som/som-logo-rb-01.ogg`; evidência `verificacao/arte-c11-abertura-1280x720.png`.
- Seguem valendo da §15: reteste do som no aparelho real (agora com 7 sons),
  painel de 5 toques, layout vertical em pé, save no navegador real.
- Semana 8: otimizar o fundo (PNG 1,0 MB → JPEG/qualidade).

## 17. APK C.12 + rewarded (teste) — dinheiro real pendente

**Status:** ✅ APK C.12 (85 MB, versionCode 12, assinado) · 91/91 + 28/28 + 5/5 · ⏳ conta AdMob do dono
**Bola com:** o dono (instalar + testar + criar conta AdMob)
**Próxima ação do dono:** instalar o APK no celular (botão `Baixar APK` no
site; liberar "instalar de fonte desconhecida"), plantar algo, tocar em
`Vídeo = pronto` e ver o anúncio de teste amadurecer a planta.
**Bloqueia:** receita real (sem conta AdMob, anúncio de teste = R$ 0)
**Critério de "resolvido":** conta AdMob criada + IDs reais no jogo + rebuild

- Criar conta em apps.admob.com (grátis; pede CPF, endereço e dados
  bancários) → cadastrar o app `com.reboclbrank.ceifalume` → anotar o
  **App ID** (`ca-app-pub-XXXX~YYYY`) e criar 1 unidade **Rewarded**.
- Troca (assistente, 10 min): `APP_ID` real em `~/.segredos-apk` (o script
  injeta no manifest) + `ID_RECOMPENSA_REAL` em `anuncios.gd` + rebuild
  (`sh tools/publicar-apk.sh`) + nova Release. versionCode sobe a cada APK.
- Seguem valendo da §16: veredito do gosto + decisão lança/não-lança.
  Play Store (US$ 25) só com dinheiro que o jogo ganhar (regra do dono).

## 18. C.13 com IDs reais — validar dinheiro

**Status:** ✅ C.13 (APK, versionCode 13, IDs reais) · 91/91 + 28/28 + 5/5 · ⏳ dono valida no aparelho
**Bola com:** o dono (desinstalar C.12 → instalar C.13 → assistir 1 vídeo)
**Próxima ação do dono:** desinstalar a C.12 (assinatura antiga morreu),
instalar a C.13 pelo botão do site, plantar, ver 1 vídeo e conferir se a
planta amadureceu + se o vídeo era anúncio real (não o de teste).
**Bloqueia:** primeira receita (unidade nova serve após ~1h)
**Critério de "resolvido":** vídeo real assistido + recompensa entregue

- NÃO clicar nos próprios anúncios (conta em risco); assistir normal pode.
- Pagamento: Configurações → Pagamentos no AdMob (banco); saque após US$ 100.
- Seguem valendo: veredito do gosto + decisão lança/não-lança + Play no futuro.

## 19. C.17 — tortura + web nova + APK-teste

**Status:** ✅ auditado + APK-teste VERDE + save corrigido · ⏳ falta publicar (token recebido, aguardo confirmação)
**Bola com:** assistente (terminar build) → depois **o dono** (testar tudo)
**Próxima ação do dono:** (a) abrir a web nova no celular
(https://reboclbrank-max.github.io/site/ceifalume/) e jogar do título ao Dia 2+;
(b) desinstalar a C.14, instalar o APK-teste (botão no site), plantar e ver 1
vídeo de TESTE amadurecer a planta; (c) responder: lança/não-lança + preço +
número da versão + guardar a chave nº 5.
**Bloqueia:** lançamento (decisão-mãe) e APK com IDs reais (rebuild de 10 min).
**Critério de "resolvido":** veredito do dono + decisão lança/preço/versão.

- Bugs: 5 reais achados e mortos (detalhes no registro 20ª rodada), o nº 5
  CRÍTICO (AdMob nunca empacotado C.12→C.16; botão de vídeo morto em todo
  aparelho; C.17c corrige + dex verificado). Nenhum conhecido restante:
  91/28/5/3 + 3030 + 100/100 + web 3 perfis + APK verificado.
- Chave nº 5: arquivos entregues ao dono (cofre NÃO persiste — canário morreu).
  Sem eles, a próxima release troca de chave e exige desinstalar de novo.
- Play Store: ADIADA por regra do dono (ZERO investimento até gerar dinheiro).
  Caminho grátis: APK real no botão do site → divulgar → AdMob acumula até
  US$100 (saca no banco) → US$25 da conta → AAB pronto → Play.
- Save (dono: "sai e entra, recomeça"): bug nº 6 real nos publicados (partida
  nova nunca ligava o save). C.17d + rede extra (pausar/fechar/periódico 10 s +
  erro visível): save_novo 10/0, economia 91/91, tortura 3030/0. Sem conta/cloud
  (orçamento-zero): save é local — mesmo app/navegador; desinstalar/limpar perde.
- Publicar = web nova + Release apk-c17-teste + botão no site. Regra: sem push
  sem confirmação. **Histórico de 16/09:** naquela época a credencial foi mantida
  fora do repositório; regra atual (25/09) é não persistir segredo em nenhum arquivo.
- C.18 (2026-09-16, APK apk-c18-teste): retry de anúncio sozinho de 20 em 20 s
  (1ª falha sem rede não mata o botão) + música sem grilos (chiado era ruído
  branco em rajadas no compor-tema.py). Medido: TESTE_ANUNCIOS 8/0, TESTE_SOM 28/0.
- 0.1 PRONTO p/ lançar (2026-09-16, tudo local, sem push): auditor 100/100;
  bateria economia 92/0 + tortura 3030/0 + save_novo 13/0 + anuncios 8/0 + som 28/0.
  Faltam SÓ 2 coisas do dono: (1) APP_ID real do AdMob (-> ~/.segredos-apk);
  (2) dizer "lança" p/ subir APK na release do site + push do site.


## M2. Operação de marketing (a partir de 2026-09-18 — assistente executa, dono manda "posta")

Plano, horários e textos: `projetos/01-ceifalume/marketing/PLANO-MARKETING.md` · métricas: `.../METRICAS.md` (script `ferramentas/medir-marketing.py`).
**Post 2 publicado sáb 19/09. Post 3 (trailer) ter 22/09 ✓; rodadas dom/seg/ter ✓. itch 57 views, Bsky 4 seguidores. Próximo post: **sáb 26/09 17h (Android sem loja)** — dono manda "posta"; rodadas diárias sob "rodada".** Relatório semana 1 em PLANO-MARKETING.md §8 (itch 16→44 views).

### Canais sem API (22/09) ✓ landing SEO + IndexNow + GitHub topics/release — plano §10
### dev.to ✓ e Tumblr ✓ ativos (plano §12). Telegram ✓ Discord ✓ Buttondown ✓ (plano §14). Rodada qua 23/09 ✓ (itch 66). Aguardando do dono: Threads ✓ (post 1). Pinterest (e-mail de aprovação do trial), Hashnode (token), Lemmy (aprovação); opcional: colar bloco Comunidade na itch. **Próximo post: sáb 26/09 17h (Android sem loja) em 6 canais.**
### Setup (fechado)
- [x] Contas criadas pelo dono: Bluesky `reboclbrank.bsky.social` + Mastodon `@ReboclBrank@mastodon.social`; chaves em `ferramentas/chaves.md`
- [x] Perfis montados + post nº 1 nas duas (links em chaves.md)
- [x] Post 3 trailer publicado ter 22/09 (Masto vídeo nativo; Bsky card YouTube)
- [x] E-mail do Bluesky confirmado (22/09) → trailer em vídeo nativo publicado
- [ ] Post 3: "screenshot saturday" (sábado) com a shot dia 9 + hashtag #ScreenshotSaturday
- [ ] Post 4: Android/APK ("sem loja, sem conta") — liberado (Android salvo ✓)
- [ ] Post 5: devlog "o que vem na 0.2" — plano pronto em `projetos/01-ceifalume/PLANO-0.2.md` (decisão do dono ~05/10; lançamento ~19/10)
- [ ] Post de coleta de opinião (PLANO-0.2 §3) — qui 24/09 12h, no "trabalhe" do dia
- [x] 19/09: 14 follows Bluesky + 5 follows e 4 hashtags no Mastodon (lista em PLANO §2b). Daqui em diante: 3–5/dia na "rodada"
- [ ] Medir: views itch antes (14) × 7 dias depois; contar cliques nos posts (Mastodon dá favoritos/boosts; Bluesky dá likes/reposts)
- [ ] Bluesky + GIF: resolver recompressão (<1 MB) ou usar vídeo MP4

## GoalBlade v11 — passe refinado de arte 2D realista (25/09)
- [x] `pintor_realista.py` — volume suave de pele/tecido, costura dupla, sombra de gola/barra, microdobras, mangas e punhos, joelho/meia, sola/cadarço/cravos da chuteira, número orientado e sombra de contato em três camadas
- [x] `sprites.py` — folha de **768 quadros** (12 pessoas × 8 direções × 8 poses), incluindo `dividida`; `jogadores.json` acompanha os retângulos
- [x] Jogo atualizado para quadros 144×160, filtro linear, escala base 0,56, perspectiva de escala por profundidade e ordem de desenho por y; CPU da simulação ficou em 0,17–0,19 ms/quadro
- [x] Fotos do jogo geradas e olhadas: `estudos/jogo-v11-campo.png` e `jogo-v11-jogador.png`; contatos do pintor em `estudos/jogador-v11-close.png` e `jogador-v11-direcoes.png`
- [x] Web republicada no link fixo; `index.pck` 4.089.576 bytes, md5 `c67d5b8c4d71b4935e576f259d20801d`, commit do site `9bfee01`
- [ ] **Veredito do dono:** jogar a build v11 no link fixo e dizer se o 2D realista agora chegou ao nível desejado
- [ ] Próxima peça, depois da aprovação visual: "por fora" do jogo (menu, criar jogador, Copa do Bairro)
- [ ] **4 avisos antigos da auditoria** (do jogo 1): `progresso.md` e `registro-de-decisoes.md` citam arquivos que não existem
      (`arte/icone-ceifalume-512.png`, `ceifalume/grava_jogo.gd`); `FUNCOES-E-OPERACAO.md` cita `empresa/METRICAS-ESTUDIO.md`;
      link de release do repo privado dá 404 para quem não está logado (histórico — o caminho público do APK é a itch)

## Segurança (corrigida em 25/09/2026)
- [x] **Credenciais removidas dos arquivos rastreados:** apagada a cópia `.token-github`,
      redigidos os valores de `ferramentas/chaves.md` e atualizada a regra oficial.
- [x] Push desta sessão usou credencial temporária fora do worktree; ela não foi salva
      em arquivo, commit ou mensagem. Próximas sessões devem pedir/receber uma nova
      credencial temporária quando necessário; nunca recriar segredo a partir da base.
