# GOALBLADE — conceito do jogo 2 (nome escolhido pelo dono em 24/09/2026; título de trabalho anterior: "Rumo ao Estrelato"; aprovado como "plano B" em 23/09/2026)

> **Decisão do dono (palavras dele):** "Pode ser o plano B, jogo com poucos jogadores em campo, facilitaria muito;
> dá pra começar com algo simples, jogo com promessa de se tornar melhor; single player e futuramente com
> possibilidade de se tornar online."

## 1. Em uma frase
Futebol **jogado em campo**, em 2D visto de cima, onde você cria um jogador e **controla só ele** — o resto do time
(e o adversário) joga com inteligência própria — começando no **society 5×5** do bairro e subindo, versão a versão,
até o 11×11 profissional. Single player na 0.1; arquitetura já preparada para online 1×1 no futuro.

## 2. Decisões fixas (não reabrir sem motivo forte)
| Tema | Decisão | Motivo |
|---|---|---|
| Visual | **2D visto de cima, com profundidade** (sombras no chão, grama listrada com textura, arquibancada, gols com rede) — mas com **bonecos desenhados de verdade** (corpo, camisa com número, calção, meias, chuteiras, cabelo, sombra, pernas animadas) e **campo com cara de campo** (grama listrada, marcações, bandeirinhas, traves com redes) | ordem do dono (24/09/2026): "**bonecos reais criados e um campo real**" — nada de bolinhas/desenho abstrato |
| Câmera | **de cima, mostrando o campo inteiro** (gol na esquerda/direita) — **padrão** —, com **opção de seguir o jogador** (troca na pausa ou tecla C) | decisão do dono (24/09/2026, depois de ver o jogo rodando): "o realismo da primeira com a **câmera da terceira**". A antiga "seguir a bola" foi **substituída** como padrão — o dono viu, jogou e escolheu |
| Controle | direcional virtual (esq.) + 3 botões (dir.): **Passe / Chute (segurar = força) / Dividir**; sem bola, Passe = pedir bola. Navegador: WASD + J/K/L | padrão de celular; cabe no polegar |
| Escala | 0.1 = **5×5** (4 linha + goleiro), campo society · 0.2 = 7×7 · 0.3 = **11×11**. **O campo cresce junto com o número de jogadores** (o 5×5 é pequeno; não se usa campo grande no society) | "poucos jogadores facilita"; ordem do dono (24/09/2026): "campo só aumenta conforme o número de jogadores aumenta". **A construção começa só com o 5×5** — ordem do dono (24/09/2026): "não há necessidade de aplicar vários modos, inicialmente começaremos com algo básico de só 5x5"; o 7×7 e o 11×11 entram na 0.2 e na 0.3 |
| Posição inicial | 0.1: **atacante ou meia** (goleiro e zagueiro entram na 0.2/0.3) | é onde controlar 1 jogador é divertido logo de cara — *decisão do assistente; dono pode mudar* |
| Times/ligas | **inventados** (nomes e cores próprios); sem escudos/jogadores reais | licença |
| Online | **não na 0.1**; mas a partida roda em **passo fixo, com entradas como comandos e aleatoriedade com semente** desde o dia 1 | é o que permite online (lockstep/rollback) depois sem reescrever |
| Motor | **Godot 4.7.2** — **aprovado pelo dono em 24/09/2026**: "iremos usar o Godot, caso perceba que esse motor não tá dando bom, migramos para outro". Estudo com as fontes em `motor-e-movimento.md` | grátis (MIT), 2D de primeira linha, roda por linha de comando (o assistente constrói sem editor), é a esteira do Ceifalume e nasce pronto para a Play Store |
| Pipeline | navegador (Pages) + APK assinado (Release), mesmo `apk-lancamento` do Ceifalume, AdMob só a partir da 0.2 | fábrica padronizada (`FUNCOES-E-OPERACAO.md` §3c) |
| Nome | **GOALBLADE** — gol + *blade* = "o gol cortante/o gol de lâmina". **Escolhido pelo dono em 24/09/2026** depois de 7 rodadas de verificação (API da itch + web) e de um nome reprovado na hora final (GoalStrike). Título de trabalho anterior: "Rumo ao Estrelato" (nome BR do modo do PES — descartado). | ✅ decidido |

## 3. A 0.1 — o que entra (e só isso)
**Partida**
- Campo society reduzido, dimensionado **pelo formato** (5×5 pequeno; cresce no 7×7 e no 11×11), 2 tempos de **3 min** (opção 2/3/4).
- **Câmera:** segue a bola, com opção de seguir o jogador (padrão: bola).
- **Jogo básico já rodando no motor (24/09):** saída de bola de verdade depois do gol (quem levou o gol recomeça),
  cronômetro de 3 min com tela de fim de jogo, placar, dois botões — **PASSE** (toque) e **CHUTE** (segurar = força).
  Implementado e testado no Godot 4.7.2 em `jogo/` (arquivo único `prototipos/5x5-basico.html` fica como referência).
- Bola com física (rolagem, quique leve, força do chute, desvio no goleiro/trave).
- **Seu jogador:** corre, passa, chuta (força por tempo de toque), divide/pressiona; cansaço simples.
- **IA dos outros 9:** posição-base por formação (2-1-1 + goleiro), estados *ir à bola / apoiar / marcar / voltar*,
  passe para o companheiro mais livre (com preferência por VOCÊ quando pede a bola e está em condição), chute na área,
  goleiro com posicionamento e defesa.
- Regras 0.1: gol, lateral e tiro de meta com **reposição automática** (rápida), escanteio simples; **sem impedimento**
  (society), **sem faltas** (entram na 0.2). Placar, cronômetro, replay curto do gol (opcional se sobrar tempo).
- Nota da partida (0–10) por gols, assistências, passes certos, desarmes, chutes no alvo.

**Carreira mínima ("promessa de se tornar melhor")**
- Criar jogador: nome, número, posição (atacante/meia), pele, cabelo, cor da chuteira.
- **Copa do Bairro:** 6 times inventados, 8 partidas (turno + 3 mata-mata) — uma temporada em ~40 min de jogo.
- Cada partida rende **XP** por nota → distribuir em 3 atributos: **Velocidade, Chute, Passe** (Drible e Físico na 0.2).
- Fim da temporada: **proposta de um time de 7×7** ("chegando na 0.2") + recorde e ficha do jogador.
- Save automático (perfil, temporada, atributos).

**Fora da 0.1 (anotado):** faltas/cartões, impedimento, treinos, lesões, dinheiro/contratos, transferências reais,
seleção, personalização de time, online, ranking, cards colecionáveis.

## 4. Trilha de versões ("promessa")
| Versão | Quando (previsto) | O que entra |
|---|---|---|
| **0.1** | **24/11/2026** | 5×5, Copa do Bairro, 3 atributos, carreira mínima |
| 0.2 | ~dez/2026 | **7×7**, faltas e cartões, treinos semanais, Drible/Físico, goleiro e zagueiro jogáveis, anúncio recompensado |
| 0.3 | ~jan/2027 | **11×11**, impedimento, campeonato de 10 times com tabela, transferência real entre clubes |
| 0.4 | ~fev/2027 | contratos, salário, imprensa, lesões, forma física |
| 0.5 | ~mar/2027 | seleção e Copa; cards de temporada colecionáveis; troféus |
| 0.6+ | 2027 | **online 1×1** (cada um controla seu jogador em times opostos), ranking, depois amigos |

## 5. Arte e som (dentro do limite do assistente)
- Jogadores: **bonecos desenhados de verdade pelo MOTOR RB** e carregados como folha raster no Godot — corpo, camisa com **número nas costas**, calção,
  meias, chuteiras, cabeça com cabelo, luz, sombra de contato e **pernas que alternam conforme a corrida** (o boneco vira para o lado que corre).
  A folha v11 tem 12 pessoas, 8 direções e 8 poses (incluindo chute, dividida e comemoração); torso, roupa, costuras, sombra, volume e número são orientados com o corpo; cores de camisa/pele/cabelo por paleta → zero problema de consistência.
- Campo, traves, redes, marcações, bandeirinhas: gerados pelo MOTOR RB como imagem estática (nítidos e leves no jogo); grama com listras de corte
  e a bola com gomos que **giram conforme ela rola**.
- **Jogo de verdade no motor (atual):** `jogo/` — projeto **Godot 4.7.2** (`project.godot`, cena `cenas/partida.tscn`, scripts em `scripts/`),
  com campo, bonecos, controles, goleiro, IA dos outros 9, placar e fim de jogo. Como abrir, testar e exportar: `jogo/LEIA-ME.md`.
- **Referência visual/histórica:** `prototipos/5x5-basico.html` (protótipo 3, HTML — serviu de base aprovada do port);
  históricos: `prototipos/visual-e-camera.html` (3 formatos de campo) e `prototipos/movimento-teste.html` (só o movimento, reprovado no visual).
- Ícones/capas/fundos de menu: imagem gerada por IA + recorte.
- Som: apito, chute, trave, torcida, gol — bibliotecas CC0 (creditadas em `creditos.md`).

## 6. Riscos e como medimos
| Risco | Sinal | Resposta |
|---|---|---|
| IA "burra" (companheiro não passa, goleiro engole) | teste do dono na semana 3 | semana 4 é toda de balanceamento; se ainda ruim, adia 1 semana em vez de lançar ruim |
| Controles ruins no toque | teste do dono | tamanho/posição dos botões configuráveis já na 0.1 |
| Escopo crescendo | qualquer item fora do §3 | vai para a trilha §4, não para a 0.1 |
| ~~Nome confundir com PES~~ | resolvido | ✅ **decidido em 24/09: GOALBLADE** (verificado; ver `nomes.md`) |

## 7. Meta da 0.1 (30 dias após o lançamento)
itch 300 views / 40 downloads (futebol + BR + 10 canais já quentes + Ceifalume como vitrine) · 10 opiniões de jogadores
· 1 vídeo de 60 s de partida no YouTube.
