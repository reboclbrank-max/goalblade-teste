> # 🔒 REGRA FIXA Nº 1 (dono, 23/09/2026) — vale para este e para QUALQUER outro chat
> **Ao fim de CADA conversa (cada resposta que mudou algo — decisão, texto, número, credencial, plano), salvar tudo
> no repositório: commit + push verificado + hash informado ao dono.** Nada fica só na conversa. Se a resposta foi
> só conversa mas gerou decisão ou recomendação aceita, ela vira texto na base (registro-de-decisoes + arquivo do
> tema). Antes de encerrar qualquer resposta, perguntar-se: "isso já está no repositório?" Se não, salvar.
> Repositórios: `base` (privado, memória da empresa) e `site` (público). Credenciais: `ferramentas/chaves.md`.

# base — Base de conhecimento da Rebocl Brank

Este repositório privado é a **memória oficial da empresa Rebocl Brank**.
Ele existe para que qualquer pessoa (ou chat/IA) consiga continuar o trabalho
de onde ele parou, sem perder contexto.

## 🚨 Comece por aqui

Se você é um chat/IA assumindo o trabalho, **leia nesta ordem** (é a mesma
ordem que o dono passa quando abre um chat novo):

1. [`guia-do-proximo-chat.md`](guia-do-proximo-chat.md) — regras de trabalho e como agir
2. [`empresa/ficha-da-marca.md`](empresa/ficha-da-marca.md) — tudo sobre a marca e decisões fechadas
3. [`empresa/registro-de-decisoes.md`](empresa/registro-de-decisoes.md) — histórico datado do que já foi feito/decidido
4. [`pendencias.md`](pendencias.md) — o que está em aberto
5. [`projetos/01-ceifalume/conceito.md`](projetos/01-ceifalume/conceito.md) — o que é o primeiro jogo
6. [`projetos/01-ceifalume/cronograma.md`](projetos/01-ceifalume/cronograma.md) — as 8 semanas planejadas
7. [`projetos/01-ceifalume/progresso.md`](projetos/01-ceifalume/progresso.md) — **onde o trabalho parou de verdade** + pipelines de build (web e Android)
8. [`site/instrucoes-do-site.md`](site/instrucoes-do-site.md) — como o site funciona e como atualizá-lo

Sem os itens 5 a 7 você vai trabalhar achando que o projeto está atrasado:
as semanas 1 a 6 já foram entregues.

## 📁 Estrutura

| Caminho | Conteúdo |
|---|---|
| `guia-do-proximo-chat.md` | Manual de instruções para quem assume o trabalho |
| `empresa/` | Identidade, decisões e histórico da marca |
| `projetos/` | Um projeto por pasta (`01-ceifalume/`: conceito, cronograma, progresso) + a pesquisa que antecedeu o primeiro jogo |
| `site/` | Documentação técnica do site |
| `pendencias.md` | Decisões e tarefas em aberto |

### Cada arquivo responde a uma pergunta

| Arquivo | A pergunta que ele responde | Quando ele precisa ser atualizado |
|---|---|---|
| `guia-do-proximo-chat.md` | "Como devo trabalhar com este dono?" | mudou regra de convivência, endereço de algo, ou o estado geral do projeto |
| `empresa/ficha-da-marca.md` | "O que já está FECHADO sobre a marca?" | decisão fechada nova (identidade, CNPJ, fase, stack, meta) |
| `empresa/registro-de-decisoes.md` | "O que aconteceu, em que ordem?" | **toda sessão**, com data — inclusive sessão só de documentação |
| `pendencias.md` | "Com quem está a bola agora?" | abriu, fechou ou mudou qualquer frente de trabalho |
| `projetos/01-ceifalume/conceito.md` | "O que é o jogo?" | mudou mecânica, conteúdo da v1 ou a lista do que fica de fora |
| `projetos/01-ceifalume/cronograma.md` | "Qual era o plano das 8 semanas?" | mudou entrega de semana ou o próprio prazo |
| `projetos/01-ceifalume/progresso.md` | "Onde o trabalho parou de verdade?" | **toda sessão que tocar no jogo** (código, build, publicação, interface) |
| `projetos/00-pesquisa-de-direcao.md` | "Por que idle de fazenda, e não outra coisa?" | nunca — é histórico, só se consulta |
| `projetos/01-ceifalume/divulgacao/` | imagens prontas para itch.io/imprensa (prints, cartaz) | quando existir material da Semana 8 |
| `empresa/logo/` | os **arquivos** da marca (SVG mestre + PNG nos tamanhos das lojas) | quando a logo for mexida ou o dono mandar o original |
| `empresa/imagens-e-desenhos.md` | "Onde entra imagem/desenho/som e com que nome?" | mudou padrão de nome, pasta de arte ou o fluxo de entrega |
| `site/instrucoes-do-site.md` | "Como o site é feito e publicado?" | mudou estrutura do site, o Pages ou o que o site hospeda |

**Se dois arquivos discordarem:** `progresso.md` manda sobre o estado do jogo,
`registro-de-decisoes.md` manda sobre o que foi decidido e `ficha-da-marca.md`
manda sobre a marca. O defasado é corrigido no mesmo dia da descoberta.

## 🧱 Convenções desta base

- **Idioma:** português do Brasil, em documentação e em código. Tratamento: "você".
- **Datas:** sempre ISO `AAAA-MM-DD` (ex.: 2026-09-15). Nunca "ontem", "semana
  passada" ou "breve" — quem lê daqui a dois meses não tem o que traduzir.
- **Links:** caminho relativo dentro do repositório (`projetos/01-ceifalume/conceito.md`);
  URL completa só para o que é de fora.
- **Um fato, um lugar:** os outros arquivos apontam, não copiam. Cópia é o que
  apodrece primeiro.
- **Status padronizado:** ✅ feito · 🔜 planejado/agendado · ⬜ não iniciado ·
  ⏳ aguardando alguém · ⚠️ problema ou retrabalho · 📌 ideia guardada · ❌ decidido contra.
- **Nada de credencial AQUI:** token, senha ou chave não entram em arquivo,
  commit nem mensagem deste repositório. Se houver operação autorizada, a
  credencial é temporária da sessão, fica fora do worktree e é apagada depois.
- **Não renomear, mover nem apagar** arquivo daqui sem pedido do dono — os
  links são por nome e a ordem de leitura também.
- **Um commit, um assunto**, conferido com `git show --stat` antes do push.

## 📏 Regra de ouro

**Toda sessão de trabalho DEVE terminar atualizando este repositório:**

- O que foi feito → `empresa/registro-de-decisoes.md` (com data)
- O que ficou em aberto → `pendencias.md`
- Mudanças em componentes específicos → arquivo de instruções correspondente

Nunca registre tokens, senhas ou credenciais neste repositório. O índice `ferramentas/chaves.md` guarda apenas caminhos, endpoints e regras; valores ficam fora da base e não são reutilizados entre sessões.

## Marketing (desde 2026-09-18)
- Plano, horários, calendário e textos: `projetos/01-ceifalume/marketing/PLANO-MARKETING.md`
- Métricas (histórico): `projetos/01-ceifalume/marketing/METRICAS.md` — gerar com `python3 ferramentas/medir-marketing.py --nota "..."`
- Credenciais de postagem: `ferramentas/chaves.md`
