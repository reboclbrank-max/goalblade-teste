# GoalBlade — 16 Seleções (licença segura)

**Decisão do dono (25/09/2026):** não usar nomes de jogadores, apenas seleções. Campo fechado com tabela na mureta. 4 botões: PASSE, DRIBLE, VELOCIDADE, CHUTE + COLA automática. Nomes dos botões reduzidos.

## Regra de ouro (jurídico)
- **Pode:** nome do país ("Brasil", "Argentina") + bandeira do país + cores inspiradas no uniforme, desde que **não copie o escudo oficial da federação nem o kit exato** e não use marcas da FIFA. Itens com termos genéricos de futebol e/ou nomes de países ou bandeiras nacionais não constituem violação da FIFA [2](https://www.fifadigitalarchive.com/welcome_old/markrequest/Common/documents/FIFA_World_Cup_26tm_IP_Guidelines_Portuguese_version_2_0_June_2024.pdf).
- **Não pode:** escudo da CBF, nome "Seleção Brasileira", camisa oficial idêntica, troféu, logo "Copa do Mundo FIFA 2026", slogan oficial — são propriedade da CBF/FIFA [3](https://portal.saladanoticia.com.br/noticia/33767/copa-do-mundo-empresas-devem-ter-cuidados-com-uso-de-marcas-da-fifa). Nomes e logos de times são marcas registradas [5](https://gamedev.stackexchange.com/questions/75485/can-i-use-the-names-or-logos-of-real-football-teams-in-my-game). No Brasil, direitos de imagem de atletas exigem autorização expressa e individual [2](https://lexsportiva.blog/2020/07/22/easportsvimagerightsinbrazil/) — por isso NÃO usaremos atletas reais.
- **Nome do modo:** não chamar de "Copa do Mundo" — use "Copa GoalBlade" ou "Torneio das Nações" para não infringir marca da FIFA [2](https://www.fifadigitalarchive.com/welcome_old/markrequest/Common/documents/FIFA_World_Cup_26tm_IP_Guidelines_Portuguese_version_2_0_June_2024.pdf).

**Prática segura para o GoalBlade:** uniforme fictício inspirado (ex: amarelo/verde para Brasil, mas sem o mesmo tom exato e sem estrelas/escudo CBF), distintivo genérico redondo com a bandeira, número grande no botão. Chamar de "Brasil" no menu, com bandeira. Nomes dos botões reduzidos para leitura (CHUTE/PASSE/DRIBLE/VELOC.).

## 16 seleções mais conhecidas do mundo — ALTAMENTE ÚNICO v3 (auditoria total)
| # | País | Camisa / Calção | Listras | Por que é único (Delta máx) |
|---|------|----------------|---------|------------------------------|
| 1 | **Brasil** | **#facc15** ouro / #0f2b4d | não | único amarelo puro |
| 2 | **Argentina** | **#7dd3fc** celeste claro / #0e2a4a | branca | celeste + 2 listras brancas |
| 3 | **França** | **#1e3a8a** navy royal / #7f1d1d | não | azul-marinho fechado |
| 4 | **Alemanha** | **#d1d5db** cinza gelo / #111111 | amarela | único cinza claro + amarelo |
| 5 | **Espanha** | **#dc2626** vermelho vivo / #1e1b4b | não | vermelho puro sem listra |
| 6 | **Inglaterra** | **#ffffff** branco puro / #0f172a | vermelha | único branco puro + vermelho |
| 7 | **Portugal** | **#064e3b** verde floresta escuro / #7f1d1d | não | verde mais escuro do jogo |
| 8 | **Itália** | **#60a5fa** azzurro céu / #f8fafc | não | azul claro saturado |
| 9 | **Uruguai** | **#e0f2fe** ciano pálido / #0e0e0e | não | quase branco azulado |
|10 | **Países Baixos** | **#f97316** laranja / #0e0e0e | não | único laranja |
|11 | **Bélgica** | **#7f1d1d** bordô / #facc15 | amarela | bordô + listra amarela |
|12 | **Croácia** | **#991b1b** vermelho escuro / #1e3a8a | branca xadrez | xadrez único |
|13 | **México** | **#16a34a** verde médio / #7f1d1d | não | verde vivo médio |
|14 | **Estados Unidos** | **#bfdbfe** azul-gelo pálido / #1e3a8a | vermelha | azul-gelo + listra vermelha |
|15 | **Japão** | **#fff7ed** branco quente / #0a2a8a | não | branco amarelado sem listra |
|16 | **Senegal** | **#84cc16** lima limão / #facc15 | amarela | lima neon único |

Todos os botões têm as 4 funções no máximo: **cola** (bola colada até roubar), **drible** (curto), **velocidade** (turbo), **chute** (forte) — anel C/D/V/F ao redor do botão na foto.

## Como jogar com as seleções
- Menu `Copa GoalBlade`: escolhe 2 seleções entre as 16.
- Em campo: 5 botões por lado com as cores da seleção escolhida (ex: Brasil amarelo vs Argentina celeste) + goleiro com kit diferenciado.
- Cada botão tem cola automática — tabela na mureta quica e volta, sem lateral.
- 4 botões na tela (tam. reduzido): **PASSE, DRIBLE, VELOC., CHUTE** + analógico.

## Implementação técnica
- `ferramentas/motor-arte/pintor_botao.py` modo `tudo` já gera os 4 ícones ao redor.
- `ferramentas/motor-arte/sprites_botao.py` gera `jogo/arte/jogadores.png` com 12 seleções.
- `jogo/scripts/consts.gd` e `jogo/scripts/jogo.gd` com cola magnética (CTRL 19.5) e velocidade/drible.
- `jogo/scripts/controles.gd` com 4 botões + analógico.
- `jogo/scripts/jogo.gd` `_fora_de_campo()` com mureta (bola quica, permite tabela).

> Aviso: isto não é parecer jurídico. Para lançamento comercial, validar com advogado de PI no Brasil.
