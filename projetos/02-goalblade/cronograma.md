# GOALBLADE — cronograma da 0.1 (5 semanas: 20/10 → 24/11/2026)

Regra: uma entrega **verificável** por semana; o que não couber vai para a trilha de versões, nunca estica a 0.1.
Trabalho acontece dentro do "trabalhe" diário (rotina de marketing + bloco de produção). Antes de começar: dono
libera a criação do novo repositório `goalblade` (privado) (assistente cria via API do GitHub com o token existente).

| Semana | Datas | Entrega verificável | Dono faz |
|---|---|---|---|
| **1 — Fundações** | 20–26/10 | repositório + projeto Godot; campo desenhado; câmera seguindo; **seu jogador corre, passa e chuta uma bola com física**; controles touch + teclado; roda no navegador (Pages de teste) | testar 2 min no celular pelo navegador: "o controle responde?" |
| **2 — O time joga** | 27/10–02/11 | IA dos 9 (formação, estados, passe, marcação, goleiro); regras básicas; **partida 5×5 completa com placar e tempo**; simulação em passo fixo com semente (base do online futuro) | testar 1 partida: "parece futebol?" |
| **3 — Carreira** | 03–09/11 | criar jogador; Copa do Bairro (6 times, 8 jogos); nota, XP, 3 atributos; proposta final; save; interface do celular; **APK de teste** | jogar 1 temporada no APK e responder 5 perguntas |
| **4 — Polir** | 10–16/11 | correções do teste; balanceamento da IA; sprites/campo/sons finais; testes automatizados (regras, IA, save); desempenho no Android modesto | 2º teste rápido no APK |
| **5 — Lançar** | 17–23/11 | página itch (dono sobe zip + APK, assistente guia), capa, GIF, trailer 30 s, textos, GitHub Release, landing no site, newsletter — tudo já com o nome **GOALBLADE** | subir arquivos na itch; aprovar textos |
| **Lançamento** | **ter 24/11 20h** | **0.1 no ar** — 6 canais + newsletter + devlog | "trabalhe" às 20h |

## Depois do lançamento
- 25/11–08/12: coleta de feedback (rodadas), correções 0.1.x; Ceifalume recebe atenção de manutenção.
- ~09/12: escopo da 0.2 (7×7) fechado com o feedback → lançamento ~fim de dez/início de jan.

## Dependências
- Ceifalume 0.2 sai em 19/10 (antes da semana 1). Se atrasar, o futebol atrasa junto — não se sobrepõem.
- Nada de custo: fontes/sons CC0, arte gerada, hospedagem GitHub/itch.
