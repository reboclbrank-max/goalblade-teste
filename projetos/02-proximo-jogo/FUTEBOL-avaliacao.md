> ⚠️ **Título de trabalho histórico.** O nome oficial do jogo 2, decidido pelo dono em 24/09/2026, é **GOALBLADE** (ver `../02-goalblade/nomes.md`).

# Jogo 2 — ideia do dono: FUTEBOL (23/09/2026) — avaliação do assistente

> **Atualização (mais tarde em 23/09):** o dono trouxe a ideia "Rumo ao Estrelato" (carreira). O assistente prefere
> essa aos recortes abaixo — ver `RUMO-AO-ESTRELATO-esboco.md`. O recorte nº 1 (pênaltis/chute por deslize) é
> reaproveitado como os "momentos jogáveis" da carreira.

## Ideia do dono
"Gostaria de criar um jogo de futebol, o que você acha?"

## Parecer: MUITO BOM tema — desde que seja UM PEDAÇO do futebol, não o futebol inteiro
**A favor:** Brasil + celular + grátis = público certo; pouquíssimo jogo de futebol leve e bom na itch/lojas grátis;
assunto infinito para marketing (rodadas, times, Copa); cresce por versões (campeonato, times, ranking, 2 jogadores).
**Pegadinhas:** (1) jogo 11×11 tipo FIFA é impossível em 2–3 semanas e fraco mesmo em meses; (2) limite de arte do
assistente: bonecos correndo em várias poses NÃO; bolas, discos, silhuetas, camisas e campo SIM; (3) sem times/jogadores
reais (licença) — times inventados com cores.

## Quatro recortes viáveis em 2–3 semanas
| # | Jogo | Como joga | Arte | Sem. | Diferencial |
|---|---|---|---|---|---|
| 1 | Disputa de pênaltis | deslizar = direção/força; goleiro reage; alterna bater/defender | bola, goleiro silhueta, gol | 2 | GIF perfeito; regra em 1 frase |
| **2** | **Futebol de botão ⭐** | turnos: puxa e solta o botão (disco) para chutar; física de mesa; 10 botões + goleiro por time | **discos com camisa** — zero boneco | 2–3 | clássico brasileiro; raro no celular; 1×1 no mesmo aparelho |
| 3 | Embaixadinha | toque no ritmo; truques pontuam | bola + perna silhueta | 1–2 | mais simples; retenção baixa |
| 4 | Técnico de bolso | escala, tática, assiste simulação em texto/pontos | quase nenhuma | 3 | lado coleção/evolução; menos GIF |

## Recomendação: futebol de botão
- Resolve a arte por definição (discos com escudo/cor); física é o forte do Godot (RigidBody2D, tabelas).
- Identidade brasileira própria; GIF de 5 s: botão dispara, bola bate na trave e entra.
- **Trilha de versões:** 0.1 partida vs computador, 2 times · 0.2 campeonato com 8 times inventados (+ modo pênaltis
  como desempate) · 0.3 personalizar time (cores, escudo, nome) · 0.4 dois jogadores no mesmo celular · depois
  coleção de botões/times raros → liga com a ideia guardada do dono (coleção + troca entre jogadores).

## Perguntas feitas ao dono (aguardando)
1. Futebol de botão ou outro dos quatro? (ou outro recorte que ele tenha em mente)
2. Visão de cima (clássico) ou levemente inclinada?
3. Partida rápida (3 min, 1 tempo) ou 2 tempos?
→ Com as respostas: `conceito.md` + escopo 0.1 + cronograma de 3 semanas (abertura após a 0.2 do Ceifalume, ~20/10).
