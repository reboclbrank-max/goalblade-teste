# Guia do próximo chat — leia antes de fazer qualquer coisa

> # 🔒 REGRA FIXA Nº 1 (dono, 23/09/2026) — vale para este e para QUALQUER outro chat
> **Ao fim de CADA conversa (cada resposta que mudou algo — decisão, texto, número, credencial, plano), salvar tudo
> no repositório: commit + push verificado + hash informado ao dono.** Nada fica só na conversa. Se a resposta foi
> só conversa mas gerou decisão ou recomendação aceita, ela vira texto na base (registro-de-decisoes + arquivo do
> tema). Antes de encerrar qualquer resposta, perguntar-se: "isso já está no repositório?" Se não, salvar.
> Repositórios: `base` (privado, memória da empresa) e `site` (público). Credenciais: `ferramentas/chaves.md`.

> ## ⚡ Estado em 2026-09-23 23h (Fortaleza) — leia primeiro, nesta ordem
> **0. Primeiros 5 minutos de qualquer chat novo:** (1) `TZ=America/Fortaleza date`; (2) ler esta caixa, `pendencias.md`
> (painel) e `empresa/CALENDARIO-TRABALHE.md`; (3) reparar o git se o sandbox resetou: `git config user.name "Rebocl Brank"`,
> `git config user.email reboclbrank@gmail.com`, `git remote add origin https://github.com/reboclbrank-max/base.git`, `git fetch origin`,
> **`git reset origin/main`** (nunca rebase; se `git status` mostrar dezenas de mudanças, é o `.git` antigo — o reset resolve);
> **segredos não ficam na base nem no cofre local**. Se o dono autorizar push, usar uma credencial temporária fornecida na sessão, por variável ou script GIT_ASKPASS em `/tmp`, e apagar depois. **Nunca token na URL do remote.**
>
> **1. Como o dono opera:** manda só **"trabalhe"** (1×/dia: sáb 17h, ter 20h, qui 12h, demais 20h). O assistente faz tudo do dia
> conforme `empresa/CALENDARIO-TRABALHE.md` (rodada + medição + post do dia + marcos), commit+push, resposta curta com hash.
> **Regra fixa nº 1** (caixa acima): salvar ao fim de cada conversa. Dono é leigo: instruções clicadas, sem jargão.
>
> **2. Ceifalume 0.1 (jogo 1) — no ar, em marketing.** 10 canais ativos via API (itch, YouTube, Bluesky, Mastodon, Tumblr,
> dev.to, Telegram, Discord, Buttondown, Threads) — credenciais TODAS em `ferramentas/chaves.md`. Métricas 23/09: itch 66 views/2 dl,
> APK GitHub 21 dl, Bsky 4 seg. Plano em `projetos/01-ceifalume/marketing/PLANO-MARKETING.md` (+ `METRICAS.md`, `medir-marketing.py`).
> **Próximo:** qui 24/09 12h = post de coleta de opinião (texto em `PLANO-0.2.md` §3) + rodada; sáb 26/09 17h = post 4 (Android sem loja).
> **0.2 do Ceifalume:** `projetos/01-ceifalume/PLANO-0.2.md` — coleta até 05/10, escopo em 05/10, lançamento **19/10**. Achado: jogo = 3,4 MB,
> motor Godot = 70 MB sem compressão → `gradle_build/compress_native_libraries=true` leva o APK de 83,6 para ≈36 MB. Repositório `ceifalume`
> NÃO está clonado neste ambiente — clonar quando a produção da 0.2 começar (07/10).
>
> **3. GOALBLADE (jogo 2; antes "Rumo ao Estrelato") — nome decidido em 24/09/2026; projeto APROVADO em 23/09 (plano B).** Futebol jogado em campo, 2D visto de cima, o jogador controla só o seu
> atleta, resto do time com IA; 0.1 = 5×5 society + Copa do Bairro + 3 atributos; depois 7×7 (0.2), 11×11 (0.3), online 1×1 (0.6+).
> `projetos/02-goalblade/conceito.md` + `cronograma.md`: abertura **20/10**, APK de teste semana 3, **lançamento ter 24/11 20h**.
> **Nome decidido em 24/09: GOALBLADE** (7 rodadas de verificação; o escolhido anterior, GoalStrike, caiu na checagem final). **Pendente do dono (sem pressa):** posição inicial (assistente definiu atacante/meia). Ideias descartadas/reserva:
> **Construção em pedaços (ordem do dono, 24/09):** cada comando dele constrói UMA peça, explicada em linguagem simples, com commit/push verificado e hash no fim. **Motor: Godot 4.7.2 aprovado pelo dono em 24/09** ("se não der bom, migramos para outro"); `conceito.md` §2 atualizado. **Peças entregues:** protótipo 2 `projetos/02-goalblade/prototipos/visual-e-camera.html` (bonecos desenhados, campo de verdade, campo que cresce com o número de jogadores, câmera bola/jogador) e protótipo 3 **`projetos/02-goalblade/prototipos/5x5-basico.html`** — o dono disse "dá pra melhorar, promissor" e mandou **começar só com o 5×5** ("não há necessidade de aplicar vários modos"): saída de bola, cronômetro de 3 min, placar, PASSE e CHUTE. Histórico: protótipo 1 (`movimento-teste.html`), reprovado no visual. Estudo do motor/movimento com as fontes em `projetos/02-goalblade/motor-e-movimento.md`. **Ordem seguinte do dono (24/09, 3ª resposta): "Faça os 3, leve o jogo pro Godot já para iniciar o trabalho real"** → entregue: **(1) IA nova** dos outros 9 (cassador/apoiador/marcador/goleiro que prevê a bola), **(2) o jogo portado para o Godot 4.7.2** em `projetos/02-goalblade/jogo/` (campo, bonecos, toque, regras, placar, fim de jogo, exportação de navegador) e **(3) polimento** (números nas camisas, pernas animadas, rastro no chute, rede nos gols, barra de força). Testes sem tela antes de entregar: **só IA 4 × 2** (posse 49%), robô 1 × 1, **0 anomalias / 0 travamentos**. Números e mapa de arquivos em `projetos/02-goalblade/motor-e-movimento.md` §9. **Ordem do dono (24/09, 4ª):** partida primeiro, "por fora" depois. **O dono testou e reprovou (5ª resposta):** "tá desorganizado, não é um jogo 2d, tá mais pra 1d, jogo muito rápido, sem estratégia, sem bonecos reais, jogo trava muito". **Escolha dele para o visual:** "o realismo da primeira com a câmera da terceira" → **versão 4**: câmera de cima com o campo inteiro (padrão) + profundidade (sombra nos bonecos, arquibancada, cerca, redes), bonecos maiores com número na camisa, ritmo 30% mais lento, goleiros que defendem (placar 1×0 e 2×0), desenho sem o que pesava (campo estático, **0,10 ms de CPU por quadro**). **Como o assistente confere o visual:** Xvfb (monitor virtual) + o próprio jogo tirando foto (`--foto=arquivo.png`) → `estudos/jogo-v4-campo.png`. **Ferramentas:** `jogo/recriar-motor.sh` (recria Godot + modelos baixando só pedaços do pacote oficial, ~20 MB / 20 s) — o ambiente limpa essas pastas entre sessões. **Versões visuais entregues:** v4 organizou câmera/ritmo; v7 levou o campo para imagem; v8 levou bonecos por folha; **v9 (25/09) trabalhou o 2D realista** com 12 pessoas, 8 direções, 8 poses, quadros 144×160, escala 0,50 e filtro linear. **v10 (25/09) fez o passe final de arte:** torso contornado e sombreado, costuras/dobras, manga e punho separados, joelho/meia/chuteira detalhados, número orientado com o corpo, sombra de contato em três camadas, perspectiva de escala no campo e ordem de profundidade. **v11 (25/09) refinou a leitura:** volume suave de pele/tecido, costura dupla, sombra de gola/barra, microdobras e sola/cadarço/cravos da chuteira; unidade 4,55 e escala base 0,56. A folha continua com 12 pessoas, 8 direções, 8 poses, quadros 144×160 e filtro linear. Evidências atuais: `projetos/02-goalblade/estudos/jogo-v11-campo.png`, `jogo-v11-jogador.png`, `jogador-v11-close.png`; build Web republicada no link fixo. **Próximo comando esperado:** o dono jogar a v11 no link fixo e dizer se o realismo chegou ao nível desejado; depois, o "por fora".
**⚠️ Ferramentas do sandbox:** o snapshot **não guarda `.git/config`** → em cada sessão nova o `origin` e o nome/e-mail do git somem; antes de commitar/pushar: `git config user.email "reboclbrank@gmail.com" && git config user.name "Rebocl Brank" && git remote add origin https://github.com/reboclbrank-max/base.git`. A pasta `~/tools/` (cópias vivas das chaves) também é apagada: recriar `~/tools/.threads.json` e `~/tools/.tumblr.json` para o medidor ler Threads/Tumblr. O **Discord recusa** chamadas de API com User-Agent padrão do Python (403) — usar `User-Agent: CeifalumeBot (...)`.
**🔁 Acesso do Threads (24/09):** rodar `python3 ferramentas/threads-token.py` em TODA rodada de marketing — ele testa e renova o acesso por mais 60 dias sozinho (a Meta não dá acesso infinito; assim ele nunca vence). Se algum dia o script disser ACESSO INVÁLIDO: reautorizar pelo link da Parte B de `projetos/01-ceifalume/destravar-threads.md`.
**🔎 MOTOR DE AUDITORIA (24/09):** rodar `python3 ferramentas/motor-auditoria/auditar.py` **no começo de cada sessão e antes do commit final** — ele acha falhas, compara com a auditoria anterior, escreve `RELATORIO-AUDITORIA.md` com o "faça isto" de cada achado e acumula regras em `MELHORIAS.md`. Achado sem correção escrita não entra. Nota de saúde de 24/09: 75/100.
**Rodada de marketing 24/09 12h (ordem: "12h faça mais uma rodada completa de marketing"):** post de coleta publicado em **5 de 6 canais** (Bluesky, Mastodon+GIF, Telegram+GIF, Discord #anúncios, Tumblr+GIF) — links e estado em `projetos/01-ceifalume/FEEDBACK-0.1.md`; **Threads bloqueado pela Meta** (`API access blocked` — erro do app, passos em §5); caderno **`FEEDBACK-0.1.md`** criado com as 3 perguntas, tabela de opiniões e o **texto pronto do devlog nº 2** para o dono colar na itch. Medição 12:58: itch 71/2, APK 22, YT 6, Bluesky 21 likes, Mastodon 2 respostas. Consertos: cópias vivas `~/tools/.{threads,tumblr}.json` recriadas (o sandbox apaga), refresh do Tumblr girou e `chaves.md` foi atualizado, e **Discord exige User-Agent próprio** (senão 403). **Devlog nº 2 no ar** (14h12 de 24/09): https://rebocl-brank.itch.io/ceifalume/devlog/1675714/01-no-ar-a-fazenda-no-dorme — rodada fechou **6 de 6** se contar o devlog (Threads segue bloqueado). **Medição de 24 h do devlog: 25/09 depois da rotina das 20h.** Próximo comando esperado: rodadas diárias (registrar opiniões) e/ou destravar o Threads; 05/10 = relatório "o que ouvimos".
> `projetos/02-proximo-jogo/`.
>
> **4. Empresa / portfólio:** dono quer 5–10 jogos, "pequenos, evoluindo aos poucos, igual o Ceifalume", em sequência (1 em produção, resto em
> manutenção). `empresa/ESTRATEGIA-CATALOGO.md`, `empresa/FUNCOES-E-OPERACAO.md` (funções, limites, comandos por portfólio, fábrica padronizada
> — adaptar medidor/pendências para multi-jogo na abertura do jogo 2). Decisões fechadas: orçamento R$ 0; MEI inviável; Play Store adiada;
> X/Medium/Instagram/TikTok/Steam descartados (PLANO §13). Pendências antigas do dono: e-mail Pinterest, token Hashnode, aprovação Lemmy,
> bloco "Comunidade" na itch, bio do Threads.
>
> **5. Ambiente:** sem ffmpeg; Pillow não salva GIF animado; ITCH `POST /games/...` PROIBIDO (só o dono edita na web); vídeo Bluesky via
> `video.bsky.app`; Threads redirect_uri SEM barra final. Detalhes em `ferramentas/chaves.md` e PLANO-MARKETING §13–15.

Você é um assistente assumindo o trabalho contínuo da marca **Rebocl Brank**.
Este documento define como trabalhar com o dono da empresa.

## 👤 Quem é o usuário

- Está criando a marca/empresa **Rebocl Brank** (jogos e aplicativos), trabalhando **sozinho**.
- Quer **começar pequeno e básico** e ser **guiado passo a passo**.
- **Orçamento: R$ 0,00.** Ele só investe dinheiro depois que entrar receita.
- Localização: Tobias Barreto, Sergipe, Brasil. Fale em português (pt-BR).

## ⚠️ Regras de convivência (importantes)

1. **Espere o comando dele.** Não faça nada além do que foi pedido. Ele já se irritou
   quando um assistente agiu por conta própria (recriou um repositório sem permissão).
2. **Antes de ações destrutivas ou estruturais** (apagar repositórios, mudar nomes,
   publicar coisas), explique o que vai acontecer e confirme.
3. **Não rediscuta decisões fechadas** — elas estão listadas em
   `empresa/ficha-da-marca.md`. Se ele pedir para mudar, aí sim atualize e registre.
4. **Documente tudo aqui** ao final de cada sessão (regra de ouro no README).
5. Seja direto e organizado. Ele prefere passos numerados e claros.

## 🔑 Acesso ao GitHub

- Conta: **`reboclbrank-max`** (nome de exibição "Rebocl Brank")
- GitHub: **não há token persistido** na base nem no cofre local. Se houver
  autorização para push, pedir/usar uma credencial temporária somente naquela
  sessão, com escopo mínimo `repo`, e apagá-la ao terminar.
- **Nunca salve a credencial DENTRO de repositório**, nem em commit, mensagem,
  URL ou arquivo permanente — principalmente no `site`, que é público.
- Um token antigo foi colado em chat em 2026-09-14 e deve ser considerado exposto;
  se ele reaparecer, avise o usuário para revogá-lo.
- **Clonar sem colar token na URL.** O jeito seguro aqui é `GIT_ASKPASS` com
  arquivo temporário (o `git -c http.extraHeader=` não funciona neste ambiente).
  Se algum clone for feito com token dentro da URL, **corrigir na mesma
  sessão** com `git remote set-url origin https://github.com/<dono>/<repo>.git`
  — senão a credencial fica gravada em `.git/config`. Conferir com `git remote -v`.

## 📦 Onde as coisas vivem

| O quê | Onde |
|---|---|
| Este repositório (privado) — a memória | `reboclbrank-max/base` |
| Código do jogo (privado até lançar) | `reboclbrank-max/ceifalume` |
| APKs de teste para o celular do dono | Releases de `ceifalume` → https://github.com/reboclbrank-max/ceifalume/releases |
| Repositório do site (público) | `reboclbrank-max/site` |
| Site no ar | https://reboclbrank-max.github.io/site |
| Build web de teste do jogo | https://reboclbrank-max.github.io/site/ceifalume/ |
| Página no itch.io | https://reboclbrank-max.itch.io/ceifalume (0.1 no ar desde 2026-09-16) + perfil `reboclbrank-max.itch.io` · **chave da API da itch em `base/ferramentas/chaves.md`** (ordem do dono de guardá-la) · kit de marketing itch em `base/projetos/01-ceifalume/marketing/itch-kit-manual.md` |
| E-mail oficial | reboclbrank@gmail.com |
| Arquivos da marca (logo SVG + PNG das lojas) | `base` → `empresa/logo/` |
| Arte e som do jogo | `ceifalume` → `arte/` (padrão de nome em `empresa/imagens-e-desenhos.md`) |
| Imagens de divulgação (prints, cartaz) | `base` → `projetos/01-ceifalume/divulgacao/` |

- O GitHub Pages do repositório `site` usa a branch `main`, pasta raiz (build "legacy").
  Qualquer push em `main` republica o site automaticamente (~1 minuto).
- **Cada repositório tem uma vida separada:** código no `ceifalume`, documentação
  aqui na `base`, público no `site`. No `site` não entra nada além do
  `index.html` e da pasta `ceifalume/` gerada pelo build.

### Caminhos dentro do ambiente de trabalho (leia antes de compilar)

| O quê | Caminho | Persiste entre chats? |
|---|---|---|
| Espaço de trabalho | `/home/user/` | só os arquivos do repositório clonado |
| Clones | `/home/user/base`, `/home/user/ceifalume`, `/home/user/site` | ❌ chat novo começa vazio — clonar de novo |
| Godot 4.3 + templates de exportação | `/home/user/.cache/ferramentas/`, `~/.local/share/godot/export_templates/4.3.stable/` | ❌ some (pasta de cache fica fora do snapshot) |
| JDK 17 + Android SDK 34 | `/home/user/.cache/android/` | ❌ some |
| Chaves de assinatura (release+debug) | `~/cofre/` (pasta NORMAL, chmod 700) + cópias reserva (guarda no script restaura ou aborta) | ⚠️ canário: se `~/cofre/lancamento` sumir, gerar de novo e anotar aqui — NUNCA pasta oculta (`.x/`) nem "keystore" no nome: a plataforma apaga entre turnos! |
| Ajustes do editor Godot (SDK/JDK/keystore) | `~/.config/godot/editor_settings-4.3.tres` | ❌ some (regravar antes do build Android) |
| Ambiente de **verificação visual** | pacotes do sistema (`xvfb`, `mesa-utils`, `libgl1`, `libglu1-mesa`, `chromium`, `fonts-liberation`, `fonts-dejavu-core`) e `puppeteer-core` em `/home/user/tools/node_modules` | ❌ some — reinstalar com `sudo apt-get install -y` (sudo funciona sem senha aqui) |

**Verificar sem depender do aparelho do dono (desde 2026-09-15):** dá para
renderizar o jogo aqui dentro e medir a tela, em vez de deduzir do código.
Rota A (motor): `prova_visual.gd` sob `xvfb-run` com GPU de software. Rota B
(navegador): Chromium + WebGL por SwiftShader abrindo a pasta publicada, medindo
o quadro do canvas e os erros da página. Comandos prontos e os números já
obtidos estão em `projetos/01-ceifalume/auditoria.md` (seção "O que foi
verificado depois disso"). **Nada disso substitui o veredito do dono** —
substitui adivinhar o que a tela mostra.

**Workspace inchado perde arquivos (medido em 2026-09-16):** com ~400 MB de quadros
de vídeo no espaço de trabalho, a virada de turno apagou o `.git` do `site`, os
`.ogg` do jogo e um PNG de arte — sem aviso. Regra: apagar frames/exportações antes
de encerrar a sessão; o que importa vive no GitHub.

**Consequência prática:** em chat novo nada está pronto para compilar. Os
comandos de instalação e os ajustes obrigatórios do Android estão em
`projetos/01-ceifalume/progresso.md` — seguir aqueles comandos, não improvisar.

## 🗺️ Estado atual do projeto (visão rápida)

> Atualizado em **2026-09-17**. O detalhe minuto a minuto está em
> `projetos/01-ceifalume/progresso.md` — leia ele antes de agir.

- ✅ Marca definida (nome, logo RB dourado/preto, e-mail)
- ✅ Site oficial no ar com a estrutura aprovada
- ✅ **Primeiro jogo definido: CEIFALUME** (fazenda idle com mercado de
  preços variando) — repositório `ceifalume` (privado)
- ✅ Documento de conceito + cronograma de 60 dias criados e **aprovados**;
  largada dada em **2026-09-14**
- ✅ **Semanas 1 a 6 implementadas** (bico, campo, venda, mercado, loja e a
  economia completa: 6 plantações, sementeira, ajudante, composteira,
  carroça, 3 eventos)
- ✅ Interface reformada (rev C.2, faixa da loja) e **aprovada como base**
  ("ficou bom, tem potencial")
- ✅ Som ligado (rev C.3): 4 efeitos + botão de mudo; tema musical aguardando
  o gosto do dono (sem música, abrir o jogo = silêncio, por projeto)
- ✅ Fiação da arte pronta (rev C.4): loader com fallback, à espera
  dos desenhos do dono (realista, clima aconchego, ele desenha)
- ✅ Som completo + painel de teste (rev C.5): 6 efeitos, 5 toques
  no título abrem o painel (`rebocl/teste_livre`, desliga na Semana 8)
- ✅ Save + offline adiantados (rev C.6): autosave por ação, volta
  de até 8 h com resumo; persistência web a validar no aparelho dele
- ✅ C.11 NO AR (pck 2,34 MB): intro v2 da RB (logo acende + vagalumes +
  vinheta) + tudo da C.10; 91/91 + 28/28; decisão lança/não-lança + preço
  com o dono
- ✅ APK C.12 (85 MB, Release apk-c12 + botão no site): rewarded opcional
  com IDs de teste; 91/91 + 28/28 + anúncios 5/5
- ✅ APK C.13 (Release apk-c13): IDs REAIS do AdMob do dono; C.12 apagada
  (keystore perdido no estouro do snapshot; desinstalar C.12 antes)
- ✅ C.14–C.16: plantio de volta, IDs reais valendo, motor 4.5.2 + AAB 16KB,
  UMP, privacidade, fonte própria, sons Kenney, tutorial, auditor 100/100
- ✅ **0.1 LANÇADO (2026-09-16): site + itch.io pública + APK 83.579.693 B na release `v0.1`**
- ✅ **TRAILER 0.1 no ar (2026-09-16): 45,9 s, 1280×720, 30 fps, 3,3 MB, asset da
  release `v0.1` — no YouTube (youtu.be/tB449xupDzY); link na itch + título do
  Short corrigidos (2026-09-17); categoria do vídeo **ficou como veio**
  (decisão do dono, 2026-09-17)**
- ✅ C.17 (2026-09-16): tortura 3030/0 + 4 bugs mortos + régua 91/28/5/3 +
  web republicada com camada + APK-teste (chave nº 5, cofre não persiste)
- 📱 Canal de teste: navegador do celular (preferido) + APK C.12
  (Release apk-c12 + botão `Baixar APK` no site); o PC dele **não roda o build web** (sem WebGL)
- ✅ **Página da itch feita via API (2026-09-18):** endpoint de escrita
  descoberto por sondagem (`POST api.itch.io/games/{id}`, form, objeto
  inteiro — regras e incidentes em `ferramentas/chaves.md`); **no ar e
  verificado no HTML da página:** 10 tags finais + descrição nova com GIF de
  14 s embutido no topo (GIF/screenshot hospedados em `site/media/ceifalume/`,
  GitHub Pages). Incidente: flag `p_android` zerada pelo changeset (campo não
  escrevível) → 1 clique do dono para remarcar
- 👉 Próxima ação: **dono faz os 7 itens web-only** (~10 min, listados em
  `auditoria-itch.md` §5: remarcar Android · excluir duplicada · perfil + bio
  · tema two column · devlog nº 1 · conferir o "Run game" no celular) e manda
  "feito" → assistente mede antes/depois pela API → comunidades + Shorts →
  lojas grátis: Samsung Galaxy Store (grátis) → Aptoide → Amazon → Uptodown →
  Huawei → AdMob acumula → SÓ ENTÃO conta Play (regra do dono: ZERO
  investimento até o jogo gerar dinheiro)
- 📅 **Relógio dos 60 dias:** 2026-09-14 → prazo final **2026-11-12**
  (dia 2/60 em 2026-09-15)
- 🟡 Jogo 2: pequeno (2–3 sem), começa após a 0.2; 05/10 levar 3 conceitos ao dono (`empresa/ESTRATEGIA-CATALOGO.md`). RPG de coleção = jogo 3–4.

## ✅ Checklist de abertura de sessão (nesta ordem)

1. Clonar a `base` e ler os 8 arquivos na ordem do `README.md`.
2. Ler a tabela "Painel" de `pendencias.md` — é ela que diz com quem está a
   bola agora.
3. Só se for compilar/publicar: verificar se as ferramentas ainda existem na
   tabela de caminhos acima e reinstalar o que faltar.
4. Confirmar com o dono o que ele pediu — e fazer **só** isso.
5. Se for escrever em repositório: usar somente credencial temporária autorizada
   nesta sessão, por variável ou `GIT_ASKPASS`; nunca salvar, imprimir ou colocar
   na URL do remote.

## 📝 Checklist de fim de sessão (a regra de ouro, executável)

- [ ] `projetos/01-ceifalume/progresso.md` → o que mudou no jogo e onde parou
- [ ] `empresa/registro-de-decisoes.md` → entrada datada de hoje (inclusive
      sessão que só organizou a documentação)
- [ ] `pendencias.md` → itens e tabela "Painel" batendo com a realidade
- [ ] `guia-do-proximo-chat.md` → "visão rápida" atualizada se o estado geral mudou
- [ ] Mexeu no site/build? → `site/instrucoes-do-site.md` ou a seção de
      pipeline do `progresso.md`
- [ ] Erro ou incidente? → a lição escrita junto, não só o fato
- [ ] `git show --stat` em cada commit antes de subir (já houve commit que
      cortou 152 linhas do `progresso.md`)
- [ ] `grep -rn "ghp_" .` devolvendo nada antes do push
- [ ] `git push origin main` e confirmar no servidor com `git ls-remote`

## 🚫 Faça / Não faça

| Faça | Não faça |
|---|---|
| Passos numerados, diretos, em pt-BR | Narrativa longa e genérica |
| Propor e esperar o "vai" | Agir por conta própria (ele já se irritou com isso) |
| Apontar para o arquivo dono do fato | Copiar o mesmo texto para dois arquivos |
| Confirmar antes de apagar, renomear ou publicar | Mexer em estrutura sem autorização |
| Registrar decisão no mesmo dia | Deixar fato só no chat (chat morre, a base não) |
| Cortar conteúdo quando atrasar | Cortar o polimento da Semana 8 |
| Falar de SLU/Fase 2 quando houver receita | Sugerir MEI para desenvolvedor (não serve) |
| Verificar ferramentas antes de compilar | Assumir que Godot/SDK/keystore estão lá |
| Tratar o celular como canal de teste dele | Obrigar o dono a depender do build web (o PC não tem WebGL) |

## O ambiente de verificação (estado em 2026-09-15, 2ª rodada)

Isto é o que o dono chama de **motor de verificação**. Está montado e medido; num
chat novo é preciso reinstalar (nada disso persiste no snapshot da base):

```bash
sudo apt-get update -q
sudo apt-get install -y -q xvfb mesa-utils libgl1 libglu1-mesa fonts-dejavu-core \
  chromium fonts-liberation ripgrep fd-find ffmpeg
pip install pillow puppeteer-core   # npm responde 200; node 20 já existe
```

- Motor do jogo em uso: **4.3** (`~/.cache/ferramentas/godot`), com templates Web em
  `~/.local/share/godot/export_templates/4.3.stable/`. **4.7.2** está instalado ao
  lado (`~/.cache/ferramentas/novo/godot`) para comparação — ver o veredito no
  registro de decisões de 2026-09-15 antes de pensar em portar.
- Rota A (dentro do motor): `prova_visual.gd` sob `xvfb-run` + `LIBGL_ALWAYS_SOFTWARE=1`,
  com `CEI_MEDIR=1 CEI_CENARIO=inicial|meio|cheio CEI_SAIDA=…`. Também `grava_jogo.gd`
  (vídeo) e `teste_economia.gd` (48 verificações; `_checar_08` roda uma por plantação,
  por isso 45 chamadas viram 48 checagens).
- Rota B (navegador real): `node ~/tools/medidor-encaixe.js`, `medidor-pagina.js`,
  `teste-toque2.js` (controle × toque), `teste-4g.js` (throttle via CDP),
  `compara-motores.js`, `sonda-aparelho.js`. Todos apontam para
  `python3 -m http.server 8099 --directory …`.
- Números que já foram medidos e não precisam ser redisputados: **~8,1 MB por
  abertura** (gzip do Pages; o `index.wasm` cru tem 35.376.909 B — o "~35 MB" que
  andou escrito aqui era erro), ~12 s em 4G, 3,3 s sem limite. fps daqui (7,8–9,8)
  **não** dizem nada sobre o celular dele: llvmpipe com 2 CPUs/1,8 GB só detecta
  patologia.
- Não tente: `/usr/bin/time` (não existe), `pkill -f "http.server 8099"` (mata o
  próprio shell), swap sem `/usr/sbin/swapon` (caminho absoluto; funciona, 512 MB
  bastaram para o teste, e é reversível com `swapoff`).

## Ensinei o próximo chat: o que este chat aprendeu (2026-09-15, 3ª rodada)

Isto é a continuação da "linha do ambiente de verificação". Quem chegar depois de mim
deve assumir três coisas: **(1)** a base está no GitHub (`reboclbrank-max/base`),
push exige token colado no chat; **(2)** o projeto roda no Godot **4.3** — 4.7.2 está
instalado ao lado só para comparação, e a tabela de por que não portar ainda está em
`empresa/registro-de-decisoes.md`; **(3)** nada entra no ar sem as medições abaixo.

### Regras de verificação que custaram dias e não podem ser perdidas

1. **Meça o estado inicial, não só o cenário bonito.** `CEI_CENARIO=meio|inicial|cheio`
   — rode os dois primeiros em toda mudança de layout. Um `Coluna` de 3381 px passou
   batido porque eu só media o "meio".
2. **Corte de texto é medido, não olhado.** A régua de `prova_visual.gd` compara
   `get_combined_minimum_size()` com o tamanho recebido, **sem tolerância**, e avisa
   "⚠ sem folga" abaixo de 2 px. Em 2026-09-15 isso achou um dígito engolido
   (2500 lido como 250) — o "parêntese faltando" que eu desconfiava era pior.
3. **Texto que existe na tela ≠ texto que o motor desenhou.** Confira com OCR:
   `convert render.png -crop LxA+X+Y +repage -resize 400% -colorspace gray /tmp/o.png
   && tesseract /tmp/o.png stdout --psm 7`. Faça o recorte pelo `rect` que o motor
   reporta, nunca por estimativa visual (errado uma vez: usei y=100..130 para um
   rótulo que estava em y=59..93 e quase chamei um corte de "não cortado").
4. **Mudança de tela precisa de controle.** `compare -metric AE -fuzz 12% antes.png
   depois.png null:` — e o "antes/depois" tem de vir do mesmo cenário e do mesmo
   número de quadro, senão a barra do dia animando vira falso positivo.
5. **Limites de container são o que o jogador vê.** Campos/itens medidos contra o fim
   da **grade** (ou do `ScrollContainer`), não contra a janela.
6. **Ao rodar o jogo em bancada (`--script`), o `SceneTree` só desenhou de verdade
   depois de ~35 `await process_frame`.** Sem aquecimento, o `get_texture().get_image()`
   devolvia só o fundo (e um vídeo de 9 KB de tela escura).

### Regras de escrita de código que peguei no ato

* `GridContainer` não estica coluna: calcule a largura da célula ou use `SIZE_EXPAND_FILL`
  **e** mínimo explícito. `custom_minimum_size` é piso, não teto.
* `@onready` com tipo errado aborta o `_ready` inteiro; o erro aparece noutro lugar
  (`... on a base object of type 'Nil'`). Ao trocar o tipo de um container no `.tscn`,
  anote a variável como `Container`.
* Reparentear (`remove_child` + `add_child`) durante `_ready`: `call_deferred()`.
* Chaves de export ficam em `export_presets.cfg` (o `exclude_filter` do preset), **não**
  em `project.godot`; uma substituição que não acha âncora não reclama — confira com
  `git status`/`grep -c`.
* Scripts de ferramenta ficam fora do `.pck` (`exclude_filter`: `*teste_economia.gd`,
  `res://grava_jogo.gd`, `res://prova_visual.gd`, `res://mede_botao.gd`).

### Ferramentas do ambiente (nada disso persiste entre chats; reinstale)

**Ambiente: o motor morre a cada turno.** Medido em 2026-09-15: sobrevive só o que está em `/home/user`; `chromium`, `node`, `ffmpeg`, `ripgrep`, `sqlite3`, `time`, `xvfb-run`, o binário do Godot (`~/.cache`) e os export templates (`~/.local`) aparecem como PERDIDOS no turno seguinte (escaparam ImageMagick e o Pillow do python). Um comando religa tudo:

```bash
bash ~/tools/acender-motor.sh   # ~3 min sem templates; ~10 min com os ~1 GB de export templates
```

Depois disso valem as rotas abaixo. **E um detalhe que queima tempo:** `.git/config`
não entra no snapshot, então os repositórios acordam **sem o remoto `origin`** (o
`git push` responde `unable to access 'https:///'`). O `acender-motor.sh` já religa os
três e faz `branch --set-upstream-to`; sem rodar o script, é `git remote add origin
https://github.com/reboclbrank-max/<repo>.git` e usar uma credencial temporária
fornecida na sessão por variável dentro do comando (nunca `echo`, saída por `sed`).

Duas outras armadilhas do mesmo tipo, ambas medidas em 2026-09-15: `XDG_RUNTIME_DIR`
inválido faz o `xvfb-run` morrer com "X11 Display is not available" (parece "o
render saiu em branco"), e `/tmp` é tmpfs de ~993 MB que chega cheio — nunca baixar
os ~1 GB de export templates para lá, e conferir `df -h /tmp` antes de culpar o motor. O índice de busca da base é refeito pelo próprio script (`python3 ~/tools/indexar-base.py`, 22 docs, ~30 ms).

* Medição de layout dentro do motor: Rota A do `prova_visual.gd` (comando no
  `projetos/01-ceifalume/verificacao/LEIA-ME.md`), com `CEI_MEDIR=1`,
  `CEI_CENARIO=inicial|meio|cheio`, `CEI_LOJA=lista|faixa`.
* Navegador real: `node ~/tools/medidor-encaixe.js`, `medidor-pagina.js`,
  `teste-toque2.js`, `teste-4g.js`, `compara-motores.js`, `sonda-aparelho.js` — todos
  contra `python3 -m http.server 8099 --directory <pasta>` (grave o PID e `kill`;
  **nunca** `pkill -f "http.server 8099"`, que mata o próprio shell).
* Vídeo de jogabilidade (o dono assistindo sem aparelho): `grava_jogo.gd` + `ffmpeg`
  (comando em `projetos/01-ceifalume/progresso.md`).
* Velocidade: meça com `/usr/bin/time -f "%e s"` (agora instalado) ou `date +%s%N`;
  não prometa ganho de ferramenta sem duas medidas. Em projeto deste tamanho, `grep`
  e `rg` ficam em 3–6 ms — o ganho do `rg` é ignorar binários, não ser mais rápido.

### Fila do dono (nesta ordem, sem adiantar semana)

1. **Teste no celular dele** (URL: `https://reboclbrank-max.github.io/site/ceifalume/`)
   e veredito de gosto/ritmo — isso eu não consigo verificar; é validação, não
   verificação. Perguntas que só ele responde: deu para ler sem zoom? a faixa da loja
   no pé ficou alcançável com o polegar? o ritmo do Dia 1 ao Dia 3 está chato ou certo?
2. Semana 7: arte e som. Para som, dá para medir LUFS/pico/silêncio com `ffmpeg`
   (instalar `pulseaudio`+`alsa-utils` se quiser gravar a saída do jogo).
3. Semana 8: save/offline, tela de título, itch.io, numeração. Lembrar: `patch PCK
   delta` é ganho do 4.6+ (só na portagem), e `VirtualJoystick` é do 4.7 (toque).
4. ⚠️ Não inflar número: se um documento da base divergir do que eu medir agora, o
   measured manda e o documento é corrigido no mesmo dia, com registro.

### Dois furos novos que eu paguei em hora de relógio (2026-09-15, 6ª rodada)

1. **Trocou asset de áudio/imagem → rode `--import` antes de medir.** O motor serve o
   cache de `.godot/imported/`; sem reimportar, sua medição escuta o arquivo **velho**
   e você conclui que "o nível não mudou" (foi exatamente o que quase me enganou com a
   mixagem). Ordem certa: editar → `--import` → medir → exportar.
2. **Sobreposição se mede no bounds do texto**, não no retângulo do `Label`: um rótulo
   centralizado ocupa a linha toda, e a régua acusaria colisão onde o olho não vê
   nada. O `prova_visual.gd` já trata isso (e por isso serve de exemplo).

Medição de som, quando o assunto é áudio: `python3 ferramentas/medir-som.py` com
`MEDIR_MODO=clip` (alvo -6 ±3 dBFS por arquivo) ou `MEDIR_MODO=mix` (pico ≤ -1 dBFS e
integrado entre -21 e -9 LUFS). Para capturar a saída real do motor: subir
`pulseaudio -F` com um `module-null-sink`, rodar o jogo sob `xvfb-run` e gravar
`grava.monitor`. Se o `Default Sink` aparecer como `auto_null`, seu `default.pa` não
foi carregado — o daemon quer `-F caminho`, não o arquivo em `$XDG_RUNTIME_DIR/pulse/`.
**⚠️ Velocidade (ordem do dono, 24/09):** o dono reclamou de demora — passar a responder CURTO (3 a 6 linhas), com poucos passos por mensagem, sem explicar o que não foi perguntado e sem rodar teste longo sem necessidade. Explicação longa só quando ele pedir.
