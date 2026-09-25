# Funções do assistente e modelo de operação por portfólio (decidido com o dono em 2026-09-23)

## Pedido do dono
Administrar **5 a 10 jogos** através do assistente, que exerce várias funções. **Regra do dono:** "jogos pequenos,
evoluindo aos poucos, igual o Ceifalume" — lançar pequeno (0.1) e crescer por versões.

## 1. Funções que o assistente exerce de ponta a ponta

| Área | O que faz | Prova no Ceifalume |
|---|---|---|
| Produtor / gerente de projeto | conceito, cronograma semanal, pendências, registro de decisões, relatórios, priorização | base inteira; PLANO-0.2; ESTRATEGIA-CATALOGO |
| Game designer | mecânicas, economia (curvas, preços), balanceamento, tutorial | Ceifalume 0.1 |
| Programador (Godot 4 / GDScript) | código completo, cenas, save, AdMob, correção de bugs, auditoria, testes automatizados | Ceifalume (91/91 testes), plugin AdMob, rev C |
| Build / release | export web + APK assinado, GitHub Release, GitHub Pages, verificação (apksigner, badging) | `apk-lancamento.sh`, APK 0.1 |
| Arte (limitada) | imagens geradas por IA (fundos, ícones, capas, banners), edição com Pillow, GIFs de divulgação | fundos, ícone, capa itch, GIF 640×360 |
| Áudio (limitada) | narração por voz sintética (trailer/devlog); **não** compõe música nem efeitos — usa bibliotecas CC0 | disponível, não usado ainda |
| Marketing / community | posts em 10 canais via API, rodadas de interação, newsletter, devlogs (dev.to), métricas diárias, SEO/IndexNow | tudo desde 18/09 |
| Analista de dados | medir, comparar séries, diagnosticar (ex.: jogo 3,4 MB vs motor 70 MB) | METRICAS.md, análise do APK |
| Suporte / QA | ler bugs (Discord/Telegram/itch), reproduzir, testar, responder jogadores | rodadas |
| Pesquisa | concorrentes, APIs, lojas, regras de plataforma, nicho | levantamentos de lojas; X descartado |
| Guia passo a passo | quando só o dono pode clicar (contas, termos, lojas), escrever a tela exata | Threads, Tumblr, Pinterest |

## 2. O que o assistente NÃO faz (limites que dimensionam o portfólio)

1. **Não age sozinho no tempo** — só trabalha quando o dono manda mensagem. Sem "rodada", não há rodada.
   Com muitos jogos, cada comando vira um lote grande (bom: dono fala pouco, assistente faz muito), mas nada
   acontece entre mensagens.
2. **Não cria contas, não passa captcha, não aceita termos, não paga.** Cada jogo novo em cada loja tem 5–10
   cliques do dono.
3. **Não faz arte de personagem com consistência** (mesmo personagem em várias poses) nem animação quadro a quadro.
   Jogos que dependem disso precisam de artista ou de estilo que contorne (formas simples, silhuetas, geométrico).
4. **Não compõe música/sons.**
5. **Não testa no celular do dono** — toque, sensação, jogabilidade real são do dono/jogadores.
6. **Não tem memória fora do repositório** — a base é a empresa. "Salve tudo" é a regra mais importante.

## 3. Modelo de operação por portfólio (aprovado)

### 3a. Sequência, não paralelo
- **1 jogo em produção** por vez + os demais **em manutenção** (versão nova a cada 4–6 semanas, revezando).
- Jogo novo só nasce quando o anterior está estável com ciclo de updates rodando (`ESTRATEGIA-CATALOGO.md`).
- **Ritmo realista:** jogo 2 em nov/2026 → 3–4 jogos até mar/2027 → 5+ no 2º semestre de 2027 → 10 só se a
  maioria for pequena e a manutenção couber nas rodadas.

### 3b. "Igual o Ceifalume": lançar pequeno, crescer por versões
- **0.1 em 2–3 semanas** (Ceifalume levou 8; o pipeline agora existe): 1 mecânica central, navegador + Android,
  página itch, trailer curto, 6 canais.
- **Versões a cada 3–4 semanas** enquanto for o jogo em produção; depois 4–6 semanas em manutenção.
- Cada versão = 1 vitrine em GIF + correções. Bug bloqueante = x.y.1 no dia.
- Jogo que não responde em 2–3 versões (views/downloads estagnados, zero feedback) entra em **modo mínimo**
  (só correções) e o esforço vai para o próximo — sem culpa, é o modelo de catálogo.

### 3c. Fábrica padronizada (cada jogo custa menos que o anterior)
- Mesmo motor (**Godot 4.7.2** — versão aprovada pelo dono em 24/09/2026), mesma pipeline (web via Pages + APK assinado via GitHub Release), mesmo plugin AdMob.
- **Pasta-modelo na base:** `projetos/NN-nome/` com `conceito.md`, `cronograma.md`, `progresso.md`,
  `auditoria.md`, `marketing/PLANO-MARKETING.md`, `marketing/METRICAS.md`, `divulgacao/`.
  (Criar o modelo `projetos/_modelo/` na abertura do jogo 2.)
- **Repositório por jogo** no GitHub (como `ceifalume`), site único (`site`) com uma landing por jogo em
  `site/jogos/<nome>/`.
- **Canais do estúdio, não por jogo:** Bluesky, Mastodon, Threads, Tumblr, dev.to, Discord (1 servidor, 1 canal
  de anúncios por jogo), Buttondown (1 newsletter). **Por jogo:** página itch, Release no GitHub, e canal Telegram
  só se o jogo criar público próprio (senão anuncia no `@ceifalume`, renomeável para o estúdio depois).
- Calendário de posts **único** para o portfólio: máx 3 posts/semana no total, revezando jogos — nunca spam.

### 3d. Dono como diretor, não operador — comandos por portfólio
| Comando | Efeito com vários jogos |
|---|---|
| `rodada` | interação + métricas de **todos** os jogos, um bloco por jogo |
| `como estamos?` | painel: 1 linha por jogo (views, downloads, versão, próxima data) |
| `relatório da semana` | consolidado do estúdio + destaque por jogo |
| `posta` / `posta X` | segue o calendário único; `posta <jogo>` força um jogo |
| `próximo jogo` | assistente traz 3 conceitos de 2–3 semanas; dono escolhe |
| `versão <jogo>` | abre ciclo de update do jogo escolhido (escopo → build → release → posts) |
| `pausa <jogo>` | jogo entra em modo mínimo |

### 3e. Ferramentas a adaptar (fazer na abertura do jogo 2, não antes)
- `ferramentas/medir-marketing.py` → ler lista de jogos (id itch, repo GitHub, vídeo YT) e gravar um
  `METRICAS.md` por jogo + um consolidado `empresa/METRICAS-ESTUDIO.md`.
- `pendencias.md` → tabela-resumo por jogo no topo.
- Relatório semanal → seção por jogo.

## 4. Próximos passos ligados a este documento
- 05/10: 3 conceitos de jogo 2 (2–3 semanas cada) — `ESTRATEGIA-CATALOGO.md`.
- Abertura do jogo 2 (após 0.2, ~fim de out): criar `projetos/_modelo/`, adaptar medidor e pendências (§3e).
