# GOALBLADE — qual motor usar e como o jogo se move

**Estudo pedido pelo dono em 24/09/2026:** *"Como iremos fazer um jogo de futebol se movimentar? Qual o motor que irá fazer isso? Quais os motores que usam para construir um jogo de futebol? Procure saber e traga o melhor motor para ser usado."*

## 0. Resposta curta

1. **Motor recomendado: Godot** — gratuito (licença MIT, sem royalties, sem taxa), o melhor motor 2D livre de 2026, e **o mesmo motor da nossa esteira** (Ceifalume). Versão sugerida para o jogo nascer: **4.7.2** (a estável atual; já está baixada no ambiente de trabalho).
2. **O movimento é feito por código, não por "animação".** A cada 1/60 de segundo o jogo recalcula a posição do jogador e da bola com física simples (aceleração → atrito → colisão). É isso que faz um jogo de futebol "se movimentar".
3. **Protótipo jogável para sentir:** `prototipos/movimento-teste.html` (um arquivo; abre no celular ou no computador).

**Status: APROVADO pelo dono em 24/09/2026** — palavras dele: *"como você analisou e percebi que o Godot é o melhor, iremos usar o Godot, caso perceba que esse motor não tá dando bom, migramos para outro"*, e autorizou atualizar o repositório (feito: `conceito.md` §2 = **Godot 4.7.2**). A troca de motor, se necessária, é decisão registrada e não "fracasso": o jogo é a prioridade, a ferramenta é meio.

---

## 1. Como um jogo de futebol se movimenta (a parte técnica, em palavras simples)

Nada "anda sozinho" na tela. A cada **passo fixo de 1/60 de segundo** (60 vezes por segundo) o jogo repete o mesmo ciclo:

1. **Ler o comando** — direcional do dedo (celular) ou WASD/setas (teclado) vira uma direção desejada.
2. **Aceleração** — o jogador ganha velocidade na direção do comando (não teleporta; ganha embalo). Sem comando, ele **freia**.
3. **Atrito** — a velocidade cai sozinha; é o que dá "peso" ao movimento.
4. **Bola é um objeto separado** — ela rola, desacelera sozinha (atrito com a grama) e quica nas linhas e nas traves.
5. **Condução (drible)** — quando o jogador encosta na bola, ela ganha um empurrão na direção do movimento. É por isso que a bola "fica indo na frente" de quem corre.
6. **Chute é um impulso único** — a bola recebe uma velocidade de uma vez só; a força vem do tempo que você segura o botão.
7. **Colisão** — jogadores são círculos que não podem se sobrepor; quem está no caminho é empurrado.
8. **Câmera segue** o seu jogador com um atraso suave (e um pouco adiantada na direção da corrida).
9. **A IA decide a cada ~8 quadros**, não a cada quadro — decisão menos "nervosa" e mais barata de processar.

**Por que "passo fixo" e não "o quanto o computador conseguir":** o passo fixo faz a partida andar sempre no mesmo ritmo, em qualquer celular (rápido ou lento), e **é o que permite transformar o jogo em online depois sem reescrever nada** — os dois celulares dão os mesmos passos e chegam ao mesmo resultado (por isso a aleatoriedade usa semente fixa). Está no `conceito.md` §2 como decisão fixa.

---

## 2. Quais motores são usados para fazer jogos de futebol (jogos reais)

| Jogo / série | Motor usado |
|---|---|
| **EA Sports FC / FIFA** (EA) | **Frostbite** — motor próprio da EA, substituiu o Ignite a partir do FIFA 17/18 |
| **eFootball / PES** (Konami) | **Fox Engine** (motor próprio, de PES 2014 até 2020) e, desde eFootball 2022, **Unreal Engine** |
| **Football Manager** (Sports Interactive) | tinha motor próprio; migrou para **Unity** (FM25/FM26) |
| **Maioria dos jogos de celular** | **Unity** — a própria Unity diz que mais de 70% dos 1.000 maiores jogos mobile usam o motor dela |
| **Jogos 2D de futebol no itch.io** | **Godot é o mais comum**: a etiqueta "soccer" com "made with Godot" tem mais de 100 jogos (ex.: *2D Pixel Art Realistic Soccer Game*, *Super Soccer*, *Sendit Soccer*) |
| **Jogos de navegador (HTML5)** | **Phaser / Construct / Godot** — motores leves, feitos para rodar no navegador |
| **Jogos antigos de futebol** (Sensible Soccer e afins) | motores próprios, escritos à mão pelos estúdios |

**Leitura útil:** os motores dos jogos AAA (Frostbite, Fox, Unreal) são feitos para times de 100+ pessoas em 3D. O nosso caso é 2D, uma pessoa (o assistente) escrevendo código, custo zero, rodando em celular modesto e navegador. **Nesse recorte, Unity é o padrão do mercado mobile e Godot é o padrão dos indies 2D.**

---

## 3. Comparação para o NOSSO caso

Cinco critérios, na ordem do que pesa aqui:

1. **Custo zero** (orçamento R$ 0,00 — nada de taxa, assinatura ou royalty).
2. **Exporta os dois alvos**: navegador (teste rápido no celular, página no site) e **APK Android**.
3. **Funcionar por linha de comando, sem editor gráfico, sem conta e sem licença** — porque quem constrói o jogo é o assistente escrevendo código; não há ninguém clicando num editor. ⚠️ Este é o critério decisivo.
4. **Leve no celular** (app pequeno, roda em aparelho modesto) e compatível com a Play Store atual.
5. **Já estar na nossa esteira** (o Ceifalume está em Godot) — evita retrabalho e reaproveita as receitas que já funcionaram.

| Motor | Custo | 2D | Navegador | Android | Linha de comando (sem editor) | Veredito para nós |
|---|---|---|---|---|---|---|
| **Godot 4.7.x** | **Grátis (MIT, sem royalties)** | **Excelente** | **Sim (WebGL2)** | **Sim (APK/AAB)** | **Sim, nativo (`--headless`)** | ✅ **escolhido** |
| Unity | Grátis até US$ 200 mil/ano; Pro US$ 2.310/ano | Bom | Sim, porém builds pesadas | Sim | Limitado: depende do editor gráfico e de conta/licença | ❌ (não dá para construir do nosso jeito) |
| Unreal Engine | Grátis com royalty acima da isenção | Fraco em 2D | Builds enormes | Pesado | Não prático | ❌ (é 3D AAA) |
| GameMaker | US$ 99,99 para uso comercial | Excelente | Sim | Sim | Não (editor gráfico) | ❌ (pago + editor) |
| Construct 3 / GDevelop | Assinatura / grátis | Bom (sem código) | Sim | Sim | Não | ❌ (sem controle fino do código) |
| Defold | Grátis | Bom | Sim (builds menores) | Sim | Sim | 🟡 alternativa, mas fora da nossa esteira |
| Phaser (biblioteca JS) | Grátis | Bom | Só navegador | Não (não gera APK) | Sim | ❌ (só navegador) |

---

## 4. Recomendação

**Usar Godot — versão 4.7.2.**

1. **Zero custo e sem royalties** — a licença MIT permite até vender o jogo sem pagar nada a ninguém.
2. **Roda 100% por linha de comando** (`--headless`): importar, exportar navegador e exportar APK — é exatamente o que já fazemos no Ceifalume, e é o que permite o assistente construir o jogo sem editor gráfico, sem conta e sem licença.
3. **É a nossa esteira** — receitas de build, assinatura do APK, página no site e publicação na itch já estão documentadas e testadas (`projetos/01-ceifalume/progresso.md`, `empresa/FUNCOES-E-OPERACAO.md` §3c).
4. **2D de primeira linha** — motor com renderizador 2D dedicado, considerado o melhor motor 2D livre de 2026; e é o mais usado entre os jogos de futebol 2D do itch.io.
5. **Alvos certos** — exporta navegador (WebGL2) e Android, com app leve; a versão 4.7.2 já atende o que a Play Store exige hoje (páginas de 16 KB, API recente), então **o jogo nasce "pronto para loja"** — diferente do Ceifalume, que nasceu na 4.3 e vai precisar de portagem.

**Sobre a versão:** o `conceito.md` §2 hoje diz "Godot 4.5" (escrito antes deste estudo). A recomendação é nascer na **4.7.2** — é a estável atual (4.7 saiu em junho/2026; 4.7.2 desde agosto/2026, com a 4.8 em desenvolvimento) e é a versão para onde o Ceifalume vai migrar de qualquer forma. Se aparecer qualquer incompatibilidade nas nossas receitas de build, a queda segura é a 4.5.2 (a que o ambiente já instala por padrão).

**Por que não Unity, sendo ele o motor da maioria dos jogos de futebol de celular:** porque ele exige editor gráfico com conta e licença para gerar os builds — não existe caminho "só por linha de comando" confiável para o nosso jeito de trabalhar — e as builds de navegador são pesadas. Ou seja: não é um problema de qualidade, é um problema de **encaixe no nosso processo e no orçamento zero**.

---

## 5. Como o movimento vai ser no GOALBLADE (números já definidos)

Estes são os números que estão rodando no protótipo e que serão levados para o Godot **sem mudança de comportamento**:

| O que | Número | Efeito percebido |
|---|---|---|
| Passo da simulação | 60 por segundo | mesmo ritmo em qualquer aparelho; base do online futuro |
| Raio do jogador / da bola | 10 / 5,5 unidades | proporção parecida com jogador e bola de verdade |
| Velocidade máxima do jogador | 205 unidades/s | atravessa o campo (1.000) em ~5 s |
| Aceleração | 1.150 unidades/s² | **chega à velocidade máxima em 0,18 s** (resposta imediata, mas com peso) |
| Freio (sem comando) | 1.250 unidades/s² | **para em 0,17 s**, andando 15 unidades |
| Atrito da bola | 1,05 por segundo (proporcional) | a bola desacelera como bola rolando na grama |
| Quique nas linhas | 0,72 da velocidade | ela volta sem "grudar" na linha |
| Chute: força | 430 (toque leve) → 1.070 (barra cheia, segurando 0,65 s) | do passe curto ao chute de campo inteiro |
| Condução | bola empurrada a 1,2× a velocidade do jogador | ela fica indo à frente de quem corre |
| Câmera | segue com atraso suave + 26 unidades adiantada | dá para ver o que vem na frente |

**Medições feitas na simulação (conferidas por script):**

⚠️ **Importante:** estes números valem para um campo de **1.000 unidades de largura**. Nos outros formatos, tudo (velocidades, força do chute,
raio dos bonecos) é multiplicado por `FS = largura/1000` — assim o mesmo chute percorre a mesma **fração** do campo e o jogo se comporta igual
no 5×5, no 7×7 e no 11×11.

| Ação | Resultado |
|---|---|
| Acelerar do zero até a máxima | 0,183 s, andando 21 unidades |
| Frear da máxima até parar | 0,167 s, andando 15 unidades |
| Chute forte (barra cheia) | sai a 1.070 u/s, para depois de 4,7 s, percorrendo **995 unidades** (o campo tem 1.000) |
| Chute médio | 750 u/s → 695 unidades |
| Passe curto | 430 u/s → 396 unidades |

**Botões de ajuste (se o dono não gostar do toque):** `velocidade máxima` e `aceleração` mudam a sensação de "peso"; `atrito da bola` muda o quanto ela corre sozinha; `força do chute` muda o alcance. São 4 números num arquivo só.

---

## 6. Os protótipos (para sentir com os dedos)

**Atual — `prototipos/5x5-basico.html` (protótipo 3, 24/09/2026):** o jogo básico **só no 5×5**, como o dono pediu ("não há necessidade de
aplicar vários modos, inicialmente começaremos com algo básico de só 5x5"): campo society 620×380, 5 de cada lado, saída de bola depois do gol,
cronômetro de 3 min, placar, **PASSE** e **CHUTE**, câmera com os dois modos. Testado no ambiente: 3 min de partida com um jogador-robô e mais
5 min sem controle → **0 erros, 0 valores inválidos, 0 travamentos, 0 jogadores fora do campo**; o fim de jogo aparece direito.

**Histórico — `prototipos/visual-e-camera.html` (protótipo 2, 24/09/2026):** bonecos desenhados, campo com cara de campo,
**três formatos de campo** (5×5 = 620×380 · 7×7 = 1.000×600 · 11×11 = 1.400×880, o campo cresce com o número de jogadores) e
**câmera com dois modos** (bola ⇄ jogador; botão na tela ou tecla **C**). Os NPCs têm comportamento simples de propósito
(correr na bola e chutar para o gol) — a IA de verdade é a peça seguinte.

**Histórico — `prototipos/movimento-teste.html` (protótipo 1, 24/09/2026):** só o movimento, com bolinhas. **Superado:** o dono
reprovou o visual ("não vamos criar desse jeito") e pediu bonecos e campo de verdade. Fica guardado como registro.

- Abre no **celular**: correr com o polegar esquerdo (arrastar em qualquer lugar do lado esquerdo da tela) e o botão **CHUTE** no canto direito (segurar = barra enche = chute mais forte).
- Abre no **computador**: WASD ou setas para correr, **espaço** para chutar.
- O que testar: (1) a resposta do controle; (2) frear e voltar; (3) encostar na bola e conduzir; (4) bater no gol — aparece "GOL!" e a bola volta ao centro.
- O que ele **não** é: não é o jogo. É um desenho de teste do movimento, escrito em HTML para você poder abrir hoje. O jogo de verdade é feito no Godot, reaproveitando exatamente estes números.

---

## 7. Próximos comandos (o dono escolhe a ordem)

1. **"pode usar o Godot"** → eu fixo o motor na base (`conceito.md` §2 + registro) e a versão.
2. **"faz o campo e o jogador"** → primeira peça de verdade no Godot: campo desenhado, câmera seguindo, jogador correndo (mesma matemática do protótipo).
3. **"coloca a bola"** → bola com física, condução e chute.
4. **"faz os outros jogadores"** → IA (os 9 companheiros e adversários).

---

## 7b. Correções do dono depois do 1º protótipo (24/09/2026)

Depois de ver o protótipo 1, o dono deu quatro ordens — todas aplicadas no protótipo 2 e no `conceito.md`:

1. **"Não vamos criar desse jeito: bonecos reais criados e um campo real."** → bonecos desenhados (não bolinhas) e campo com cara de campo.
2. **"Como é 5×5, não precisa ser campo grande: o campo só aumenta conforme o número de jogadores aumenta."** → três formatos de campo, o tamanho acompanha o número de jogadores.
3. **"Tem que ser um jogo que segue a bola, mas também que tem a opção de seguir o jogador."** → câmera com dois modos (bola ⇄ jogador).
4. **Godot aprovado** + autorização para atualizar o repositório (feito) + cláusula "se não der bom, migramos para outro".

**Testes automáticos do protótipo 2 (feitos no ambiente, antes de entregar):** 12 minutos de jogo simulado nos três formatos, com trocas de câmera —
**0 erros, 0 valores inválidos, 0 travamentos, 0 jogadores fora do campo**. Numa simulação com um "jogador-robô" que sempre chuta bem saem muitos gols
(números de fliperama); o ritmo real depende de quem joga, e o **equilíbrio fino (dificuldade da IA e do goleiro) é a peça dos "outros jogadores"**.

## 8. Fontes consultadas (24/09/2026)

- FIFA/EA FC = Frostbite; PES = Fox Engine e depois Unreal — https://www.videogameschronicle.com/news/the-former-boss-of-metal-gear-solid-and-efootballs-fox-engine-is-overseeing-tech-on-netflixs-new-fifa-game/ · https://grokipedia.com/page/Fox_Engine
- Football Manager migrou para Unity — https://www.pcgamesinsider.biz/news/73889/si-moves-to-unity-for-football-manager-25/ · https://www.gosugamers.net/entertainment/news/77565-review-football-manager-26-looks-good-but-its-buggy-interface-leaves-much-to-be-desired
- Unity no celular (70%+ dos 1.000 maiores) — https://unity.com/solutions/mobile
- Motores 2D em 2026 (Godot 4.7/4.7.2, preços de GameMaker e Unity) — https://app.cinevva.com/guides/best-2d-game-engines-2026 · https://www.soonlab.ai/blog/2d-ai-game-maker-tools/ · https://egmatic.com/blog/5-powerful-godot-alternatives-worth-considering-2026
- Jogos de futebol 2D feitos em Godot no itch.io — https://itch.io/games/made-with-godot/tag-soccer

---

## 9. O jogo dentro do motor (Godot 4.7.2) — port feito em 24/09/2026

Ordem do dono: **"Faça os 3, leve o jogo pro Godot já para iniciar o trabalho real"** (24/09/2026). O que era HTML virou
projeto de verdade no motor, na pasta **`jogo/`**:

| Arquivo | O que é |
|---|---|
| `jogo/project.godot` | configuração do projeto (passo fixo 60/s, tela 1280×720, renderizador compatível com celular) |
| `jogo/cenas/partida.tscn` | a cena da partida |
| `jogo/scripts/consts.gd` | **todos os números** do movimento/chute/campo (os mesmos do protótipo aprovado) |
| `jogo/scripts/campo.gd` | grama listrada, marcações, áreas, bandeirinhas, gols com rede |
| `jogo/scripts/jogador.gd` | o boneco (camisa com número, calção, meias, chuteiras, cabelo, pernas correndo) **e a IA** |
| `jogo/scripts/bola.gd` | a bola (atrito, gomos que giram, rastro no chute forte) |
| `jogo/scripts/jogo.gd` | o cérebro: passo fixo, regras (gol, saída de bola, laterais), relógio, placar, câmera, robô de teste |
| `jogo/scripts/hud.gd` | placar, relógio, aviso de "GOL!", botão da câmera, tela de fim |
| `jogo/scripts/controles.gd` | direcional que segue o dedo + botões CHUTE (segurar = força) e PASSE |
| `jogo/LEIA-ME.md` | como abrir, como testar e como exportar para o navegador |

### A IA nova (tarefa 1 da ordem)

- O time decide a cada **0,15 s** (não a cada quadro, para não ficar "nervoso").
- **Cassador:** um por time vai na bola chegando **por trás** dela (na direção da meta adversária) e já prevê para onde ela vai.
- **Apoio:** quando o time tem a bola, os outros abrem na frente, nas laterais, sem se amontoar.
- **Marcação:** quando o adversário tem a bola, cada um pega **um adversário diferente** e fica **entre ele e a nossa meta**.
- **Goleiro:** lê a bola, **prevê onde ela cruza a linha** e corre para o ponto (defesa de verdade); sai para abafar quando o perigo é perto;
  recua quando o time tem a bola; **mergulha** (com o raio de abafa maior) quando o chute vem.
- **Quem tem a bola:** chuta se está na faixa de chute e não tem ninguém na frente; senão **toca** para o companheiro melhor colocado;
  senão **conduz** para a frente.
- **Passe e chute erram mais de longe** (mira com erro proporcional à distância) — é o que evita o "fliperama".

### Números medidos (testes automáticos, antes de mostrar)

Todos os testes rodam **sem tela** (`--headless`), com o jogo de verdade:

```
~/.cache/ferramentas/godot --headless --path jogo -- --teste --tempo=180        # robô no lugar do dedo
~/.cache/ferramentas/godot --headless --path jogo -- --teste --auto --tempo=180 # só IA dos dois lados
```

| Teste (partidas de 3 min) | Com o goleiro da 1ª versão | Com o goleiro ajustado |
|---|---|---|---|
| **Só IA**, os dois lados (3 min) | **13 × 15** — ritmo de fliperama, sem graça | **4 × 2** (posse nossa 49%) — equilibrado |
| **Robô** que corre na bola e chuta sempre com força total (3 min) | **10 × 9** | **1 × 1** (posse 56%) |

O robô **não passa** e chuta sempre no mesmo lugar: o número dele é um **piso** do que dá para fazer, não o que o dono vai viver
(ele tem o PASSE e a mira na mão). O que importa para o equilíbrio é a partida **só IA**: 4 × 2 com posse dividida ao meio.

Em **todos** os testes: **0 valores inválidos, 0 jogadores fora do campo, 0 travamentos de bola, 0 erros de script**.
Duas correções vieram desses números: o goleiro estava fraco (13×15) e, depois de reforçado, ficou forte demais (1×1) —
o ponto final é **velocidade 0,78× (0,98× no mergulho) + raio de abafa 1,75× mergulhando + chute da IA só a partir de 0,36 do campo**.
A bola também ficava presa encostada na lateral: agora **bate e volta ao campo** e, se ficar parada na linha por 1,2 s, é recolocada em jogo
(era o único "travamento" que sobrava).

### A partida como ela é hoje (ordem do dono: "primeiro vamos criar a partida para eu testar")

O dono mandou **fechar primeiro a partida** (e deixar o "por fora" — menus, carreira — para depois). A partida ganhou:

- **Tela de início com o apito:** "GOALBLADE — 5 × 5, NÓS × ELES", o **como jogar** em quatro linhas e "toque na tela para começar".
  O relógio e o jogo **não andam** antes do apito.
- **Botão de pausa** no alto (o mesmo botão vira "continuar") e o relógio **congela** na pausa.
- **Autor do gol:** o aviso agora é "**GOL do 9!**" — o jogo guarda quem tocou na bola por último e credita o gol a ele
  (é a base da nota de partida e das assistências depois).
- **Um toque resolve tudo:** começa, continua (na pausa) ou **recomeça** (na tela de fim).
- **Fim de jogo** com VITÓRIA NOSSA / EMPATE / DERROTA e o placar.

Testes dessa peça (3 min de partida, sem tela): **pausa aos 20 s → relógio ficou em 25 s por 30 quadros (congelado, como tem de ser) → retomada ok**;
**recomeço no meio da partida** (relógio e placar zerados, os 10 jogadores em campo) → **0 anomalias, 0 travamentos, 0 erros**.
Partidas de conferência (3 min, só IA, duas medidas): **4 × 2** e **1 × 3** — de 4 a 6 gols por partida, com a posse dividida ao meio
(a partida entre IAs varia de um jogo para o outro, como no futebol de verdade).

### Versão de navegador (a que o dono testa no celular)

```
~/.cache/ferramentas/godot --headless --path jogo --export-release "Web" jogo/export/web/index.html
```

Gera `index.html` + `index.wasm` (≈39 MB, sem exigir cabeçalhos especiais no servidor — escolha de propósito para hospedar em qualquer lugar).

### Dois canais de teste (pedido do dono em 24/09: "tem teste para PC também?")

1. **Celular (navegador):** `--export-release "Web"` → servido pela prévia do ambiente. É o canal principal, porque o PC do dono
   não tem WebGL (o jogo no navegador não abre lá).
2. **PC (programa):** presets **"PC (Windows)"** e **"PC (Linux)"** em `export_presets.cfg`, com o jogo embutido no próprio arquivo
   (`binary_format/embed_pck=true`) → **um arquivo só**: `GoalBlade.exe` (~109 MB) no Windows, `GoalBlade.x86_64` (~73 MB) no Linux.
   Baixar e dar dois cliques. Teclado: **WASD/setas** corre, **espaço** chuta (segurando, mais forte), **J** passa, **C** troca a câmera.
   **Teste feito antes de entregar:** o programa de Linux (mesma esteira do .exe) rodou uma partida de 20 s sem tela → **0 anomalias**,
   e o .exe conferido como executável PE32+ de Windows válido.
3. Os modelos de exportação de PC foram extraídos do pacote oficial (`windows_release_x86_64.exe`, `linux_release.x86_64`)
   para `~/.local/share/godot/export_templates/4.7.2.stable/`.

### O que ainda não entrou

Dois tempos de 3 minutos (hoje é um tempo só), faltas/impedimento, laterais e escanteios como regras (hoje a bola bate e volta),
menu/carreira/Copa do Bairro/XP, e o ajuste fino do equilíbrio com o dedo do dono.

---

## 10. Depois do "não gostei" — versão 4 do jogo (24/09/2026)

**O que o dono disse, e o que foi feito:**

| Reclamação | O que foi feito |
|---|---|
| "não é um jogo 2D, tá mais pra 1D" + "o realismo da primeira com a câmera da terceira" | **Câmera de cima mostrando o campo inteiro** (gol na esquerda/direita), com **profundidade de verdade**: sombra no chão de cada boneco e da bola, grama com listras e textura, arquibancada com torcida, cerca, gols com moldura branca e rede. A opção "seguir o jogador" continua existindo (botão na pausa / tecla **C**) |
| "sem bonecos reais" | Bonecos redesenhados: **maiores na tela** (1,85× o tamanho real — convenção dos jogos, para leitura), com **número na camisa**, meias na cor do time, chuteiras, braços, cabeça com cabelo e sombra deslocada (é o que dá a sensação de estar **de pé**) |
| "jogo muito rápido" | **Ritmo 30% mais lento**: velocidade máxima 127 → **88**, aceleração 713 → **470**, chute máximo 663 → **455**, bola com atrito maior. A carga do chute passou de 0,65 s para **0,95 s** (chute deliberado, não metralhadora) |
| "sem estratégia" | Goleiro com 1,02× de velocidade no mergulho (defende de verdade), IA que **prefere o PASSE**, apoio com largura e distância, separação maior entre companheiros (fim do bolo no meio) e chutão só quando pressionado |
| "jogo trava muito" | Tirei o que pesava: **o campo virou estático** (era redesenhado 60×/s com listras e 160 pontos), o boneco deixou de montar polígonos por quadro, o HUD não redesenha sem mudança, listas reaproveitadas. Medido: **0,10 ms de CPU por quadro** no teste (era o caminho para travamento no celular) |
| "desorganizado" | HUD nova: barra de placar com chips dos times, números e **relógio redondo com anel que esvazia**; só o **botão de pausa** no canto; telas de início/pausa/fim com botões grandes alinhados; joystick e botões de CHUTE/PASSE em cantos fixos |

**Números medidos (partidas de 3 min, sem tela):** só IA = **1 × 0** (posse 53%) · com robô = **2 × 0** (posse 66%) ·
**0 anomalias**, 0 erros de script, **0,10 ms/quadro**. Partidas de 1 a 2 gols — o placar deixou de ser de fliperama,
que era o pedido de "estratégia".

**Como o assistente confere o visual sem ninguém olhar:** instalou um "monitor virtual" (Xvfb) e o próprio jogo **tira fotos**
com `--foto=arquivo.png` (e `--foto-quadro=N`). As fotos desta revisão estão em `estudos/jogo-v4-campo.png` e `estudos/jogo-v4-jogador.png`.
Os três rumos visuais que o dono escolheu estão em `estudos/visoes-comparadas.jpg` (visão 1 = cima inclinada, visão 2 = isométrica,
visão 3 = de cima com bonecos de pé) e o retrato desenhado antes do port em `estudos/retrato.jpg` (com `estudos/retrato.py`).

**Ferramentas:** `jogo/recriar-motor.sh` recria o motor e os modelos de exportação **baixando só os pedaços necessários**
do pacote oficial (20 MB em vez de 1,28 GB, ~20 s) — necessário porque o ambiente do assistente limpa essas pastas entre sessões.

### Versão 5 — o "trava muito" tratado de verdade (24/09/2026)

O dono perguntou "travou?" e a resposta honesta era sim: o link estava servindo uma versão antiga (erro do assistente) **e** o
desempenho ainda dependia de ~2.500 traços desenhados por quadro (grama, torcida, cerca, linhas). Correções:

1. **O campo virou UMA imagem:** ele é desenhado uma vez numa imagem de 2.560×1.440 e, a partir do 3º quadro, **para de ser redesenhado** —
   na tela aparece como **uma única imagem por quadro** em vez de milhares de traços. É a maior economia de celular possível sem trocar o motor.
2. **Menos traços no desenho do campo:** 2.200 → 900 fios de grama e 210 → 110 pontos de torcida por faixa (agora isso só pesa no 1º quadro).
3. **Publicação conferida de verdade:** o assistente compara o arquivo do jogo servido no link com o seu (o resultado tem de ser idêntico) —
   foi assim que o erro da versão antiga apareceu. Esse passo passa a ser obrigatório antes de mandar link ao dono.

## Versão 6 — "ainda tá travando ao extremo … o controle tá horrível, sem start e select" (24/09/2026, à noite)

Queixa do dono, palavra por palavra: *"ainda ta travando ao extremo, nao ta rodasndao liso nunca, e o controle ta horrivel,
sem start e select sem funcionalidade"*.

### O que foi feito no jogo

| # | Problema | Causa medida | Correção |
|---|---|---|---|
| 1 | travamento | o jogo desenhava na **resolução física da tela** (celular comum ≈ 2,5 a 3× mais pixels que o necessário) | `window/dpi/allow_hidpi=false`: desenha sempre em 1280×720 lógicos |
| 2 | travamento | tela de 90/120 Hz dobrava o trabalho à toa | `Engine.max_fps = 60` |
| 3 | travamento | a imagem do campo era 2.560×1.440 (7,4 Mpx por quadro só nela) | `TEX_W` caiu para **1280** (1,8 Mpx) e a câmera que desenha o campo passou a acompanhar a escala |
| 4 | travamento | nenhuma rede de segurança se o aparelho ainda não aguentar | **MODO LEVE automático**: se os fps caírem (< 46 por 2 s) o jogo desenha em 75% e, se precisar, 62% — e volta sozinho quando o aparelho aguentar |
| 5 | travamento | era impossível saber o que o dono via | linha de desempenho no canto (`fps · MODO LEVE · motor de vídeo`) + **tela de pausa mostra tudo** (tamanho da janela, escala, versão do Godot) |
| 6 | controle | CHUTE/PASSE/joystick tinham posição FIXA em 1280×720 → no celular (mais largo) saíam do lugar certo | todos os controles agora se posicionam **pelo tamanho real da tela**, recalculado a cada mudança |
| 7 | controle | START e SELECT não existiam | **START** = começar / pausar / voltar ao jogo / jogar de novo · **SELECT** = trocar a câmera. Ficam nos cantos de CIMA (embaixo cobriam o gol) |
| 8 | controle | direcional sem zona morta (dedo parado empurrava o boneco) | zona morta de 16% e raio maior |
| 9 | tela em pé | nada avisava | aviso "GIRE O CELULAR" ocupando a tela |

### Erros que o assistente cometeu e consertou no caminho (para não repetir)

- **A foto automática travava o teste:** ela usava o contador de quadros *de jogo* (`t_frames`), que não anda nas telas de início/pausa
  → a foto nunca saía e o processo ficava 100% de CPU para sempre. Agora existe `t_pfisicos`, que conta desde a abertura.
- **O "modo leve" quebrava o jogo:** ao ligar sozinho, a moldura de desenho encolhia e os controles ficavam fora de lugar (visto nas
  fotos: START/CHUTE deslocados, campo pequeno). Agora a moldura é **sempre** 1280×720 e o que cai é só a quantidade de pixels;
  depois de mudar a escala, HUD e controles são reposicionados e a câmera refaz o zoom.
- **HUD e controles com layout "preso":** passaram a conferir o tamanho da tela **a cada quadro** (barato) em vez de só no evento de
  redimensionar — era isso que deixava tudo desalinhado quando a tela mudava por baixo.

### Ferramentas (mudança de método)

- O servidor de teste agora vive **no repositório**: `projetos/02-goalblade/servidor-teste.py`
  (`/` = jogo web · `/div/` = divulgação do Ceifalume · `/pc/` = .exe quando existir). Antes vivia em `/tmp` e era apagado a cada
  sessão.
- Os **modelos de exportação** ficam em `~/.local/share/godot/...`, pasta que o ambiente apaga: rodar `bash recriar-motor.sh` é
  sempre o **primeiro passo** antes de exportar.
- Conferência de publicação (obrigatória): `md5sum` do `index.pck` local × o baixado pelo link. v6 = `797c4806d05df6c5fa219f3e2e983a72` (79.972 B).

**Link fixo (24/09):** a build v6 foi publicada no repositório `site` (pasta `goalblade/`) → https://reboclbrank-max.github.io/site/goalblade/ — não depende de túnel nem do ambiente ligado. O túnel do cloudflared continua existindo só para arquivos de divulgação (/div/).

## Versão 7 — "quero gráficos bons e perfeitos" (24/09/2026, noite)

Ordem do dono: *"permaneça trabalhando, principalmente agora nesse novo jogo, aonde quero gráficos bons e perfeitos,
conforme o que eu prezo"*.

**O caminho escolhido: o MOTOR RB passou a desenhar a arte do jogo.** Em vez de o jogo desenhar cada peça por código a cada
quadro (e de eu desenhar tudo à mão), o **motor de arte gera as imagens** e o jogo carrega uma imagem.

| # | O que mudou | Arquivo |
|---|---|---|
| 1 | **Campo vira imagem de arte** com grama texturizada (fios), listras, desgaste nas áreas, sombra das arquibancadas caindo no gramado, gols com trave/rede/sombra, torcida em fileiras com degraus, vinheta e sombra nas laterais | `ferramentas/motor-arte/campo.py` → `jogo/arte/campo.png` (1280×720) |
| 2 | **O jogo não desenha mais o campo por código** (o desenho antigo continua como reserva se a imagem faltar) e **deixou de precisar do desenho intermediário (SubViewport)** — menos memória e menos trabalho por quadro | `jogo/scripts/campo.gd`, `jogo/scripts/jogo.gd` |
| 3 | **Goleiro de verdade:** camisa de manga longa, luvas, boné e sombra no chão (antes era um quadrado com círculo) | `jogo/scripts/goleiro.gd` (novo) |
| 4 | **Sombra em duas camadas** nos jogadores (núcleo escuro + borda suave) | `jogo/scripts/jogador.gd` |
| 5 | Conferido por foto e publicado: build v7 no **link fixo** (md5 conferido: `31e4391…`, pck 290.616 B) | `site/goalblade/` |

**Erros cometidos e corrigidos no caminho (para não repetir):**
- conta errada da posição do campo na imagem (o campo saiu fora do quadro na primeira tentativa — a imagem cobre 900 unidades de
  **largura**, então 720 px de altura valem 506 unidades, não 900);
- `campo.gd` ficou com **dois `_ready()`** ao trocar o desenho pela imagem (o Godot recusa) — lição: ao substituir um bloco, apagar o antigo;
- `var px := s * 3.2` dentro de `for s in [...]` não tem tipo inferível no GDScript 4.7.2 → anotar `: float` (mesma lição da v4);
- os quadros da folha de sprites cortavam a cabeça: o quadro precisa de 84×152 na escala 3.

**Falta (próximo passo natural):** ampliar a arte — poses de dividida, comemoração com o time inteiro, torcida animada — e revisar
o tamanho do boneco em telas pequenas.

---

## Versão 8 — os bonecos viraram ARTE de verdade (24/09/2026, madrugada)

**O que o dono reprovou na v7:** *"tá uma porcaria, os bonecos estão 100% genéricos, os bonecos não foram feitos e nem trabalhados,
não tem realismo"*. Resposta: parar de desenhar o boneco com retângulos dentro do jogo e **criar de verdade** o desenho dele — no motor
de arte, na **perspectiva certa** (vista de cima, que é a câmera padrão do dono), com luz, sombra e **uma pessoa diferente por jogador**.

| # | O que mudou | Arquivo |
|---|---|---|
| 1 | **`pintor.py` — pintor de jogador em visão de cima** (v2): o corpo é montado num referencial próprio (`lado` × `frente`) e girado para a tela, então o mesmo desenho vale para as 8 direções e nunca sai torto. Ombro em peça única e larga (é o que dá a leitura de pessoa de cima), tronco comprido, braços recolhidos como quem corre, coxa/canela com dobra, meia descendo até a chuteira, sombra elíptica | `ferramentas/motor-arte/pintor.py` |
| 2 | **Identidade por jogador:** tons de pele (6), cabelos (7 cores), tipos (curto, raspado, black, cacheado, calvo), chuteiras, meia alta, listras no uniforme, faixa de capitão. **Nada de clones** — cada um dos 5 jogadores de cada time é uma pessoa | `pintor.py` (`Identidade`, `KitTopo`) |
| 3 | **Passada de corrida de verdade:** a perna avança e recua no sentido da corrida (swing), o braço balança cruzado, a cabeça/e o corpo sobem no impulso. Antes a "corrida" só abria as pernas para os lados | `pintor.py` |
| 4 | **Folha de sprites do jogo:** 12 pessoas × 8 direções × 7 poses (corrida em 4 quadros, parado, chute, comemoração) = 672 quadros de 124×136 → `6944×1632`, otimizada para **818 KB** (paleta de 256 cores) | `ferramentas/motor-arte/sprites.py` → `jogo/arte/jogadores.png` |
| 5 | **O jogo passou a carregar a arte:** `jogador.gd` recorta o quadro da folha por `AtlasTexture` + `Sprite2D` (a direção vem do vetor de movimento, a pose da velocidade num relógio de passada); `goleiro.gd` usa as linhas 10 e 11 (o de amarelo e o de verde), mergulhando na pose de impulso. **Zero desenho por código por quadro** | `jogo/scripts/jogador.gd`, `jogo/scripts/goleiro.gd` |
| 6 | Conferido por foto (`estudos/jogo-v8-campo.png`, `jogo-v8-perto.png`) e publicado no **link fixo**: pck 1.435.976 B, md5 `33934883…` | `site/goalblade/` |

**Erros cometidos e corrigidos no caminho (para não repetir):**
- **`_ready()` duplicado** ao trocar o desenho no `jogador.gd` — a mesma lição do `campo.gd`: ao substituir um bloco, apagar o antigo;
- no `sprites.py`, `pose.startswith("c")` pegava `"chute"` e quebrava o teste → testar `pose[1].isdigit()`;
- a passada abria as pernas para os lados (não era corrida) → `swing` no eixo da corrida;
- membros longos demais faziam o boneco parecer "estrela-do-mar" → encurtar braços e coxas;
- a folha sem otimização pesava 2,0 MB → `quantize(256 cores)` baixou para **818 KB** sem perda visível.

---

## Versão 9 — realismo 2D trabalhado (25/09/2026)

**Ordem do dono nesta sessão:** continuar no GOALBLADE e buscar o melhor 2D realista. A v8 já tinha identidade por jogador, mas na foto de campo os bonecos ainda ficavam pequenos e com aparência genérica. A v9 é uma peça visual, sem mudar a física ou a IA.

1. **Novo pintor:** `ferramentas/motor-arte/pintor_realista.py`. O corpo agora é montado em camadas: sombra macia + sombra de contato, tronco trapezoidal, manga, antebraço, mão, calção, coxa, joelho, meia, faixa da meia e chuteira com sola/cadarço. A camisa tem luz lateral, sombra de tecido, gola, listras, distintivo e número; cabelo e pele têm variações por pessoa.
2. **Folha nova:** `sprites.py` passou a gerar **12 pessoas × 8 direções × 8 poses = 768 quadros**, 144×160 por quadro. Entrou a pose de **dividida** e o jogo trocou de 7 para 8 colunas de pose.
3. **Leitura no celular:** a escala do `Sprite2D` passou de 0,33 para **0,50** e o filtro de `NEAREST` para `LINEAR`. A imagem continua sendo uma folha única, então o jogo não voltou a redesenhar bonecos por quadro.
4. **Evidência:** `estudos/jogo-v9-campo.png` e `estudos/jogo-v9-jogador.png`, fotografias reais do projeto sob Xvfb. O campo inteiro continua organizado; a câmera próxima permite conferir número, roupa, cabelo e sombra.
5. **Regressão medida:** `--import` limpo; partida IA por 30 s = 0×0, 0 anomalias; partida com robô por 30 s = 1×0, 0 anomalias; foto de 5 s = 0 erros; CPU da simulação ficou em **0,18–0,19 ms/quadro** (o desenho continua fora do passo de física).

**Pendente:** com o dono — jogar a build v9 no link do GoalBlade e dizer se agora o visual dos bonecos está no caminho. Se aprovar: próxima peça é o "por fora"; se ainda achar genérico, o próximo corte será a direção artística dos bonecos, não a IA.


## Versão 10 — passe final de arte 2D realista (25/09/2026)

**Comando do dono:** continuar trabalhando no visual do GoalBlade e buscar o melhor 2D realista possível.
Esta peça mexe só na leitura visual; física, IA, regras e números da partida permanecem os mesmos.

1. **Material e anatomia:** `pintor_realista.py` ganhou contorno próprio no torso, painel de sombra, costuras de ombro e barra, dobras de tecido, manga/punho separados, joelho destacado, faixa da meia, lingueta/cadarço/cravos da chuteira e volume adicional no cabelo.
2. **Número coerente com a direção:** `motor_rb.py` agora tem `texto_numero_orientado()`. O número da camisa gira junto com o eixo do jogador; não fica mais preso à horizontal da tela quando o atleta vira.
3. **Peso no campo:** a sombra passou a ter três camadas (volume, direção e contato). No Godot, a escala varia levemente conforme a profundidade do jogador no campo e o `z_index` segue a coordenada Y, criando sobreposição natural sem alterar colisões ou velocidade.
4. **Folha e jogo:** os 768 quadros continuam em 144×160; a unidade de desenho passou a 4,35, a escala base no Godot a 0,54 e o filtro segue linear. O `jogadores.json` acompanha os retângulos da folha.
5. **Verificação real:** `--import` limpo; partida só-IA e partida com robô por 30 s terminaram com **0 anomalias e 0 travamentos**. CPU medida: **0,15 ms/quadro** na simulação. Fotos sob Xvfb: `estudos/jogo-v10-campo.png` e `estudos/jogo-v10-jogador.png`; contato ampliado em `estudos/jogador-v10-close.png`.
6. **Publicação:** a exportação Web foi refeita com Godot 4.7.2, o `index.pck` local tem **3.781.464 bytes** e a pasta `goalblade/` do site foi substituída byte a byte antes do push.

**Pendente:** com o dono — jogar a v10 no link fixo `https://reboclbrank-max.github.io/site/goalblade/` e dizer se o realismo 2D chegou ao nível desejado. Só depois entra o "por fora" (menu, criação e Copa do Bairro).

---

## Versão 11 — volume e presença em escala de partida (25/09/2026)

**Comando do dono:** continuar trabalhando no GoalBlade e buscar o melhor 2D realista. Esta peça refina a arte sem mudar física, IA, regras ou controles.

1. **Pele e tecido:** `pintor_realista.py` acrescentou luz e sombra suaves em camadas, sombra curta de gola e barra, costura dupla dos ombros e microdobras de movimento. O objetivo é a leitura de material, não um brilho plástico.
2. **Anatomia em primeiro plano:** pescoço, rosto e cabelo ganharam volumes separados; a chuteira agora tem sola própria, lingueta, cadarço e cravos. As oito direções continuam coerentes porque tudo é calculado no referencial do jogador.
3. **Presença no campo:** `sprites.py` passou a usar unidade 4,55 (antes 4,35) e o Godot passou de escala 0,54 para **0,56**. O quadro permanece 144×160 e sem cortes; a folha continua com 768 quadros.
4. **Verificação real:** `--import` limpo; só IA por 30 s = **0 × 0**, posse nossa **49%**, CPU **0,17 ms/quadro**; robô por 30 s = **1 × 0**, posse nossa **72%**, CPU **0,19 ms/quadro**; em ambos, **0 anomalias e 0 travamentos**. Fotos sob Xvfb: `estudos/jogo-v11-campo.png` e `estudos/jogo-v11-jogador.png`; contatos ampliados: `jogador-v11-close.png` e `jogador-v11-direcoes.png`.
5. **Publicação:** export Web reconstruído com Godot 4.7.2; `index.pck` local = **4.089.576 bytes**, md5 `c67d5b8c4d71b4935e576f259d20801d`; a pasta `goalblade/` foi substituída e conferida byte a byte no repositório público `site`, commit **`9bfee01be5b705d7ffdf6029091a9560f2f9f6cc`**.

**Pendente:** com o dono — jogar a v11 em `https://reboclbrank-max.github.io/site/goalblade/` e dizer se o realismo 2D chegou ao nível desejado. Se aprovado, a próxima peça é o "por fora"; se ainda houver algo que incomode, continuamos primeiro na direção visual.
