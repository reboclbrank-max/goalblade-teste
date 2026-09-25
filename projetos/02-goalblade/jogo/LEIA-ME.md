# GOALBLADE — projeto no motor (Godot 4.7.2)

Este é o **jogo de verdade**, dentro do motor, começando do que já foi aprovado no
protótipo 3 (`../prototipos/5x5-basico.html`). Nada de tela separada por formato:
aqui é só o **5×5 básico**, como o dono pediu em 24/09/2026.

## Como abrir no computador

1. Abra o Godot 4.7.2.
2. Clique em **Import** (Importar) e escolha o arquivo `project.godot` desta pasta.
3. Aperte **F5** para jogar.

No celular: os testes são feitos com a versão de navegador (exportação web) — o
mesmo caminho usado no jogo 1.

## O que já está dentro

- **Campo 5×5** desenhado por código: grama listrada, linhas completas, áreas,
  marca do pênalti, arcos de canto, bandeirinhas e **gols com rede**.
- **Bonecos de verdade (arte v11 do MOTOR RB)**: 12 pessoas diferentes, com camisa numerada,
  calção, meias, chuteiras, braços, cabelo, volume de pele/tecido, luz e sombra de contato. A folha tem 8 direções e 8 poses;
  o Godot recorta um `AtlasTexture` por jogador, com filtro linear e escala base 0,56 para leitura no celular.
- **Time 2-1-1 + goleiro**, com o dono no comando do **atacante**.
- **Chute segurando o botão** (a barra enche em 0,65 s = força máxima) e **passe**.
  Teclado: setas/WASD, ESPAÇO = chute, J = passe, C = troca a câmera.
- **Câmera segue a bola** (padrão) e **pode seguir o jogador** (botão na tela ou tecla C).
- **IA nova dos companheiros e adversários** (a tarefa 1 da ordem de 24/09):
  - o time decide a cada 0,15 s quem **vai na bola** (chegando por trás dela);
  - os outros **apoiam** (abrem na frente) e **marcam** (ficam entre o adversário e a nossa meta),
    com cada um pegando um adversário diferente e se afastando dos companheiros (nada de bolo);
  - **goleiro** fica na linha do ângulo, sai para abafar quando o perigo é perto,
    mergulha quando a bola vem no gol e recua quando o time tem a bola;
  - quem tem a bola **chuta** se está na faixa de chute sem ninguém na frente,
    senão **toca** para o companheiro melhor colocado, senão **conduz** para a frente.
- **Regras**: gol, saída de bola de quem levou o gol, bola que bate na lateral volta ao campo,
  relógio de 3 minutos, placar e tela de fim (VITÓRIA NOSSA / EMPATE / DERROTA).
- **A partida tem começo, pausa e recomeço**: tela de início com o apito e o "como jogar"
  (o jogo não anda antes de você tocar), **botão de pausa** no alto, **"GOL do N!"** com o autor,
  e um toque na tela de fim já recomeça a partida.
- **Passo fixo de 60/s**: a partida roda sempre no mesmo ritmo. Isso é a base para o
  online futuro (o mesmo cálculo roda no servidor e no aparelho).

## Arte v11 — passe final de realismo 2D, refinado

A arte dos jogadores não é mais montada por retângulos durante a partida. O MOTOR RB gera uma folha
com 768 quadros: 12 identidades × 8 direções × 8 poses (`parado`, quatro passos, `chute`, `dividida`,
`comemora`). Cada quadro tem 144×160 e é recortado por `AtlasTexture`; isso deixa o desenho mais humano,
com sombra, roupa em camadas e detalhes de chuteira, sem pagar o custo de redesenhar formas a cada quadro.

Evidências renderizadas pelo próprio jogo:
- `../estudos/jogo-v11-campo.png` — campo inteiro, teste de 5×5.
- `../estudos/jogo-v11-jogador.png` — câmera seguindo o jogador, para conferir escala e leitura.
- `../estudos/jogador-v11-close.png` e `jogador-v11-direcoes.png` — contato ampliado do pintor e coerência nas oito direções.
- Passe v11: torso contornado e sombreado, volume suave de pele e tecido, costura dupla, sombra de gola/barra, manga/punho, joelho/meia, sola/cadarço/cravos da chuteira, número orientado com o corpo e sombra de contato em três camadas.
- Profundidade v11: a escala varia levemente pela posição no campo e o desenho usa `z_index` pela coordenada Y; isso dá perspectiva sem alterar a física.

Depois de trocar a folha, sempre rodar `--import` antes do teste. Os testes que fecham esta peça são:
`--teste --auto` (IA), `--teste` (robô) e duas fotos sob Xvfb; nenhum é substituto do veredito do dono.

## Como testar sem ver (o jeito que este projeto usa)

O assistente roda os testes aqui, no modo sem tela. O jogo entra em **modo de teste**
(robô no lugar do dedo do dono + medição) e termina sozinho:

```
~/.cache/ferramentas/godot --headless --path . -- --teste --tempo=180
~/.cache/ferramentas/godot --headless --path . -- --teste --auto --tempo=180
```

- `--teste` liga a medição (gols, posse, bola travada, valores inválidos) e o robô.
- `--auto` joga com **só IA** (nem o jogador do dono é humano) — serve para medir o
  equilíbrio da inteligência artificial.
- `--tempo=N` encurta a partida para o teste (em segundos).

Os números medidos em cada rodada (placar, posse, travamentos) ficam em
`../motor-e-movimento.md` §9 — este arquivo é só o "como fazer".

## Versão para PC (programa que abre com dois cliques)

```
~/.cache/ferramentas/godot --headless --path . --export-release "PC (Windows)" /tmp/pc/GoalBlade.exe
~/.cache/ferramentas/godot --headless --path . --export-release "PC (Linux)"   /tmp/pc/GoalBlade.x86_64
```

Sai **um arquivo só** (o jogo vem embutido, `binary_format/embed_pck=true`) — no Windows são ~109 MB: salvar e dar dois cliques.
Teclado: **WASD/setas** correm, **espaço** chuta (segurando, mais forte), **J** passa, **C** troca a câmera.
A versão de Linux foi usada como teste: o programa exportado rodou uma partida de 20 s sem tela → **0 anomalias** (mesma esteira do .exe).

## Como exportar a versão de navegador (a que o dono testa no celular)

```
~/.cache/ferramentas/godot --headless --path . --export-release "Web" export/web/index.html
```

O resultado em `export/web/` é o que sobe para o ar (mesma pipeline do jogo 1).

## Ainda não está aqui (próximos passos, um comando por vez)

- Dois tempos de 3 minutos (aqui ainda é um tempo só de 3 minutos).
- Faltas, impedimento, laterais e escanteios como regras de verdade.
- Menu, escolha de time, Copa do Bairro, XP e atributos — só depois do básico aprovado.
- Ajuste fino do equilíbrio (quantos gols por partida) — medido pelos testes acima.
