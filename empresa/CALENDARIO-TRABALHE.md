# Comando único "trabalhe" — calendário do que o assistente faz em cada dia (a partir de 24/09/2026)

## Regra (decisão do dono, 23/09/2026)
O dono não especifica mais nada: manda só **"trabalhe"** e o assistente faz **tudo que está designado e acertado
para aquele dia** (este calendário + PLANO-MARKETING + PLANO-0.2 + ESTRATEGIA-CATALOGO + FUNCOES-E-OPERACAO), e
responde com um resumo curto + hash do commit. Os comandos antigos ("rodada", "posta", "como estamos?") continuam
valendo, mas não são mais necessários.

**Primeira coisa que o assistente faz ao receber "trabalhe": conferir a data e o dia da semana no fuso de
Fortaleza (`TZ=America/Fortaleza date`) e ler este arquivo.** Nunca presumir o dia.

## Horário para o dono mandar "trabalhe" (1 mensagem por dia, fuso de Fortaleza)

| Dia da semana | Hora ideal | Por quê |
|---|---|---|
| **Sábado** | **17h** | post principal da semana (#ScreenshotSaturday, pico do Bluesky) |
| **Terça** | **20h** | post 2 da semana (melhor dia útil, noite BR / fim de tarde EUA) |
| **Quinta** | **12h** | post curto opcional (almoço BR / manhã EUA) |
| Dom, seg, qua, sex | **20h** (qualquer hora entre 19h e 21h serve) | só interação + métricas; hora pouco importa |

Se o dono perder o horário: manda "trabalhe" assim mesmo — o assistente faz o que era do dia (post inclusive, se
ainda for o mesmo dia; se o dia virou, o post é adiado para a próxima janela e ele avisa). Se mandar duas vezes no
mesmo dia, o segundo "trabalhe" só faz o que ficou faltando.

## O que "trabalhe" sempre inclui (todo dia)
1. Data + leitura de `pendencias.md` e deste calendário.
2. **Rodada** (PLANO-MARKETING §2b): notificações e respostas no Bluesky/Mastodon/Threads; 3–5 follows e
   3–5 likes em contas do nicho; olhar Discord #bugs/#feedback e Telegram; anotar toda opinião de jogador em
   `projetos/01-ceifalume/FEEDBACK-0.1.md`.
3. **Medição** (`ferramentas/medir-marketing.py` → METRICAS.md).
4. Bug bloqueante relatado → abre 0.1.1 no dia (avisa o dono antes de publicar).
5. Commit + push verificado; resposta em poucas linhas com o que foi feito, números do dia e o que vem amanhã.

## Calendário até o lançamento da 0.2

| Data | Dia | Hora | Além da rotina (inclui `python3 ferramentas/threads-token.py` para o acesso do Threads nunca vencer) diária |
|---|---|---|---|
| 24/09 | qui | 12h | **Post de coleta de opinião** (PLANO-0.2 §3) em 6 canais; cria `FEEDBACK-0.1.md` |
| 25/09 | sex | 20h | rotina |
| 26/09 | sáb | **17h** | **Post 4 — Android sem loja** (APK direto) em 6 canais |
| 27/09 | dom | 20h | rotina + **relatório da semana** (números 21–27/09 vs meta 30 dias) |
| 28/09 | seg | 20h | rotina |
| 29/09 | ter | **20h** | **Post 5 — bastidor idle** ("a fazenda trabalha enquanto você dorme") |
| 30/09 | qua | 20h | rotina |
| 01/10 | qui | 12h | post curto opcional (resposta/bastidor) só se houver assunto; senão rotina |
| 02/10 | sex | 20h | rotina |
| 03/10 | sáb | **17h** | **Post 6 — #ScreenshotSaturday 2** |
| 04/10 | dom | 20h | rotina + relatório da semana |
| **05/10** | **seg** | 20h | **Relatório "o que ouvimos" + escopo recomendado da 0.2** (+ confirmar o jogo 2 escolhido em `projetos/02-proximo-jogo/CONCEITOS.md`, se ainda não escolhido) → dono decide (responde na mesma conversa ou no dia seguinte) |
| 06/10 | ter | **20h** | **Post 7 — devlog "o que vem na 0.2"** (+ artigo dev.to) — com o escopo decidido |
| 07–09/10 | qua–sex | 20h | rotina + **construção da 0.2** (assistente pede ao dono o clone do repositório `ceifalume` na primeira vez) |
| 10/10 | sáb | **17h** | **Post 8** — GIF da vitrine da 0.2 em andamento |
| 11–12/10 | dom–seg | 20h | rotina + construção; relatório da semana no domingo |
| 13/10 | ter | **20h** | **Post 9** — pedido de Reddit manual ao dono (texto pronto) + espelho nos canais |
| 14–16/10 | qua–sex | 20h | rotina + testes da 0.2 (dono testa no celular quando o assistente mandar o APK de teste) |
| 17/10 | sáb | **17h** | Post 10 — "0.2 chega terça" |
| 18/10 | dom | 20h | rotina + relatório |
| **19/10** | **seg** | 20h | **Lançamento 0.2**: itch (dono sobe o zip/APK, assistente guia) + GitHub Release + newsletter + 6 canais |
| 20/10 | ter | **20h** | Post pós-lançamento + **abertura do **GoalBlade**** (semana 1 do `projetos/02-goalblade/cronograma.md`) |
| 20/10 → 23/11 | todos | idem | rotina de marketing (2 jogos) + bloco de produção do futebol; posts revezam Ceifalume/bastidores do futebol (máx 3/sem) |
| **24/11** | **ter** | **20h** | **Lançamento GoalBlade 0.1** (itch + Pages + APK + 6 canais + newsletter) |

## Onde o dono entra além de "trabalhe"
- Responder às decisões de 05/10 (escopo da 0.2 e escolha do jogo 2).
- Testar o APK de teste da 0.2 no celular (~14–16/10) e dizer o que achou.
- Subir os arquivos na itch em 19/10 (a API de escrita da itch é proibida — regra ⛔ em `chaves.md`).
- Reddit manual (13/10) — texto pronto, ele cola.
- Pendências antigas quando puder: e-mail do Pinterest, token do Hashnode, aprovação do Lemmy, bloco "Comunidade"
  na itch, bio do Threads.
