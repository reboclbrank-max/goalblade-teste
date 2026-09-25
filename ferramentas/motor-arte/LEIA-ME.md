# MOTOR RB — o nosso motor de desenho (v0.6, 25/09/2026)

**O que é:** o nosso próprio motor de **arte**. Ele não usa nenhum programa externo nem biblioteca instalada — só o Python que
já existe na máquina. Ele desenha (formas, luz, sombra, contorno, anti-serrilhado) e **arquiteta** a imagem: boneco = esqueleto +
poses + uniforme + cores; campo = parâmetros (tamanho, listras, desgaste, gols).

**Por que é "motor" e não "um desenho":** trocar a cor do time, o número ou a pose **não muda o desenho** — muda os números.
É a mesma ideia dos motores de jogo: o desenho é consequência de parâmetros.

---

## Como rodar

```bash
cd ferramentas/motor-arte
python3 gerar.py teste     # 1 boneco grande (conferência de qualidade)
python3 gerar.py folha      # folha de poses e direções (frente/lado/costas)
python3 gerar.py elenco     # imagem de destaque: 5×5 no campo inteiro
python3 gerar.py tudo       # as três
python3 pintor.py           # conferência do jogador de visão de cima
python3 sprites.py          # A FOLHA DE SPRITES DO JOGO (é esta que o GoalBlade usa)
```

**Do motor de arte para o jogo:** `sprites.py` gera `saida/jogadores.png`; a cópia que o jogo usa fica em
`projetos/02-goalblade/jogo/arte/jogadores.png`. A folha v11 tem **12 pessoas × 8 direções × 8 poses = 768 quadros**, em quadros de 144×160. Ela usa luz/sombra rasterizadas, volume suave de pele e tecido, e filtro linear no motor; o arquivo final é conferido depois do `--import` do Godot.
Depois de trocar a imagem: rodar `--import` no projeto do Godot (senão o jogo não vê a arte nova).

Saída em `ferramentas/motor-arte/saida/`.

## Arquivos

| Arquivo | O que é |
|---|---|
| `motor_rb.py` | o **núcleo**: Tela, cores, formas (círculo, elipse, cápsula, retângulo arredondado, polígono), dígitos, gravação PNG |
| `boneco.py` | o **gerador de bonecos**: esqueleto, poses, uniforme (`Kit`) e o desenho de cada peça |
| `gerar.py` | **quem manda desenhar**: as três cenas prontas (teste, folha, elenco) |
| `pintor.py` | pintor v8 preservado como referência histórica |
| `pintor_realista.py` | pintor v11 usado pelo jogo: pessoa em vista de cima, tronco/roupa/pele/cabelo/chuteira com volume, costuras, luz, sombra de contato e poses de corrida, chute, dividida e comemoração |
| `sprites.py` | a **folha de sprites do GoalBlade v11**: 12 pessoas × 8 direções × 8 poses = 768 quadros → `saida/jogadores.png` + `jogadores.json` |
| `saida/` | as imagens geradas |

---

## A arquitetura (como o desenho funciona por dentro)

1. **Camada de desenho (Tela):** as formas são pedidas em coordenadas de desenho, não em pixels.
2. **Super-amostragem (`luz=N`):** tudo é desenhado numa grade N×N maior e depois reduzido — é daí que vem o
   **anti-serrilhado** (borda lisa). `luz=4` = qualidade de perto; `luz=2` = rápido para imagens grandes.
3. **Formas por distância (SDF):** círculo, elipse, cápsula e retângulo arredondado sabem a **distância** de cada ponto até a
   borda. Por isso contorno, sombra e brilho saem exatos, sem "escadinha".
4. **Composição por camadas (alfa):** a ordem é sempre
   `sombra no chão → membros de trás → tronco → número → membros da frente → cabeça/cabelo`.
   O que está atrás é desenhado com tom mais escuro: isso cria **profundidade**.
5. **Luz:** cada peça recebe brilho em cima/esquerda e sombra embaixo/direita — é o que dá volume sem textura.
6. **Gravação PNG à mão:** zlib + CRC32, PNG RGBA 8 bits. Sem dependências.

## Regras de proporção do boneco (é isso que dá a "qualidade")

- ~5,5 cabeças de altura; ombro mais largo que a cintura; perna mais comprida que o tronco.
- Toda peça tem **contorno escuro** (o boneco lê em fundo claro ou escuro).
- Membros: manga (uniforme) → pele → mão; calção → pele da coxa → **meia** → chuteira.
- Número no peito com contorno por deslocamento (estilo placa).
- Pés em `(x, y)`: o boneco "pisa" no ponto que você mandar — é o que permite colocá-lo no campo.

## Uniforme (Kit) — trocar o time é trocar 4 cores

```python
from boneco import Kit, desenhar
VERMELHO = Kit(camisa="e23e37", calcao="fefefe", meia="d93a33", numero=9)
AZUL     = Kit(camisa="2f5fd8", calcao="111a38", meia="22336b", numero=4, pele="c98a5e", cabelo="14100c")
desenhar(tela, x, y, escala=3.0, kit=VERMELHO, direcao="frente", pose="corrida0")
```

Poses prontas: `parado · corrida0..3 · chute · comemora` · Direções: `frente · lado · costas`.

---

## Erros que já foram cometidos (para não repetir)

- **v0.1 "boneco de massinha":** braço grosso, tronco redondo, perna curta. Corrigido com o esqueleto novo e membros longos/finos.
- **Tronco gigante:** peças do tronco usaram coordenada **absoluta** em vez de relativa (só a perna/braço usavam relativo).
  Regra do motor: **toda** peça é desenhada a partir de `(x, y)` dos pés.
- **Número com "quadro preto":** o contorno era um retângulo atrás de cada ponto. Agora o contorno é o próprio número desenhado
  1 pixel deslocado (esquerda/direita/cima/baixo).

## Novidades da v0.6 (25/09, v11 do GoalBlade)

- `pintor_realista.py` continua sendo a fonte da folha que entra no jogo; a v8 fica no `pintor.py` apenas para comparação.
- Passe v11: volume suave em pele, cabelo e tecido; sombra curta de gola e barra; costura dupla nos ombros; microdobras de movimento; sola separada, cadarço e cravos da chuteira.
- A sombra mantém três camadas (volume, direção e contato); o jogo acrescenta escala de perspectiva por profundidade e `z_index` pela coordenada Y.
- A unidade do desenho passou a 4,55 para dar 5% mais presença sem cortar o quadro; a escala base no Godot passou a 0,56. A folha mantém **8 poses**: `parado`, `c0..c3`, `chute`, `dividida`, `comemora`; quadros **144×160**, filtro linear.
- Evidências: `projetos/02-goalblade/estudos/jogo-v11-campo.png`, `jogo-v11-jogador.png`, `jogador-v11-close.png` e `jogador-v11-direcoes.png`.

## Novidades da v0.2.1 (24/09, à noite)

- **Fonte própria 5×7** no núcleo: `tela.texto("GOALBLADE 0.1", x, y, escala, cor, contorno)` e `texto_medido()` para caber num
  espaço exato (títulos de capa). Sem arquivo de fonte externo.
- **Uniformes com listras verticais** (`Kit(..., listras="fefefe")`).
- **5 tipos de cabelo:** `curto · raspado · black · cacheado · calvo` (`cabelo_tipo=`).
- **Exportador de folha de sprites** (`sprites.py`): gera `saida/sprites-goalblade.png` (63 quadros: 3 uniformes × 3 direções ×
  7 poses) + `saida/sprites.json` com o retângulo de cada quadro. É o caminho para o jogo carregar **uma imagem** em vez de
  desenhar o boneco por código a cada quadro.
- **Ajuste de quadro:** o quadro de sprite precisa de 84×152 na escala 3 (com 112 de altura as cabeças cortavam — visto na imagem).

## Próximos passos naturais (não são pedidos ainda)

1. **Levar a folha de sprites para dentro do Godot:** o `sprites.json` já tem os retângulos; falta o `jogador.gd` passar a usar
   `AtlasTexture` no lugar do desenho por código (ganho de desempenho definitivo no celular).
2. **Campos por parâmetro:** `campo(t = "society" | "grama sintética", cor1, cor2, chuva=True)`.
3. **Retratos** (cabeça grande para menu/elenco) e **capas** (itch, YouTube) no mesmo motor.
4. **Estúdio com telinha:** escolher cores, número e formação sem mexer em código.
