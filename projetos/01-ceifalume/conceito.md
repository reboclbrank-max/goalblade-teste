# CEIFALUME — Documento de Conceito

> "A fazenda não dorme." — você planta, colhe e negocia à luz da lanterna,
> num mercado onde os preços mudam a cada dia.

**Um jogo Rebocl Brank** | Estilo: idle / administração | Motor: Godot
Plataformas: navegador (principal) e computador | Publicação: itch.io
Jogadores: 1 pessoa, sem internet/online na primeira versão

---

## 1. A ideia em uma frase

Você cuida de uma fazenda noturna: as plantações crescem sozinhas (mesmo com
o jogo fechado), e a graça é decidir **quando vender** — porque os preços do
mercado sobem e descem a cada dia.

## 2. Como se joga (o ciclo do jogo)

1. **Plantar** — você escolhe uma semente e clica num campo.
2. **Crescer** — a plantação cresce com o tempo, sozinha, à luz das lanternas.
3. **Colher** — clicando (ou com ajudantes, mais tarde) a colheita vai para o celeiro.
4. **Negociar** — o mercado mostra o preço de cada plantação HOJE:
   caro, normal ou barato. Você vende agora ou espera subir?
5. **Investir** — com as moedas: mais campos, sementes melhores, ferramentas
   e ajudantes que trabalham por você.
6. **Repetir** — a fazenda cresce e os números sobem.

Uma sessão curta (2–5 minutos) já dá progresso — ideal para celular e navegador.

## 3. Conteúdo da primeira versão

### Plantações (6, com números iniciais para ajustar depois)

| Plantação | Custo da semente | Tempo para crescer | Preço base de venda |
|---|---|---|---|
| Nabo | 5 | 30 segundos | 8 |
| Milho | 20 | 2 minutos | 35 |
| Trigo | 60 | 5 minutos | 110 |
| Tomate | 200 | 15 minutos | 380 |
| Abóbora | 700 | 45 minutos | 1.400 |
| Flor de Lume | 2.500 | 2 horas | 5.500 |

- A **Flor de Lume** é a plantação especial do jogo: nasce só em Ceifalume,
  brilha na noite e dá o nome ao jogo.
- Cada preço varia entre **50% e 200%** do valor base a cada dia do jogo.

### Campos
- Começa com 4 campos; pode expandir até 24 (cada expansão custa mais caro).

### Construções e melhorias (6)

| Melhoria | O que faz |
|---|---|
| Celeiro | Aumenta quantas colheitas dá para guardar |
| Poço | Plantações crescem mais rápido |
| Grande Lanterna | Todas as plantações rendem mais |
| Composteira | Cada colheita dá +1 unidade |
| Ajudante | Colhe sozinho um campo (pode contratar vários) |
| Carroça | Vende sozinha quando o celeiro enche |

### O mercado (coração do jogo)
- A cada "dia" do jogo (alguns minutos reais), os preços mudam.
- Setas mostram se cada preço subiu ou desceu.
- 3 eventos raros para dar emoção: **Chuva boa** (cresce mais rápido),
  **Feira da Madrugada** (preços dobram por 1 dia) e **Seca** (colheita rende menos).

### Progresso fora do jogo
- Com o jogo fechado, as plantações continuam crescendo, até o limite de 8 horas.
- Ao voltar, o jogo mostra: "Enquanto você estava fora..."

## 4. Visual e som

- **Cenário:** noite no campo — céu escuro, vaga-lumes, janelas acesas,
  plantações iluminadas por lanternas. Aconchegante, sem susto, sem pressa.
- **Arte:** 2D simples (feita no Krita/Inkscape ou com desenhos gratuitos).
- **Som:** grilos, vento, música calma feita no LMMS, efeitos de colher e vender.
- **Idioma:** português do Brasil (único idioma na primeira versão).

## 5. Técnica (resumo)

- Godot 4 com GDScript.
- Exportação para **web** (jogável no navegador e no celular pelo navegador)
  e para Windows/Linux (arquivos para baixar no itch.io).
- Salvamento automático no próprio navegador/computador.

## 6. O que fica DE FORA da primeira versão (proteção do prazo)

Estas ideias são boas — mas ficam para atualizações depois do lançamento:

- ❌ Internet, ranking ou troca entre jogadores
- ❌ Prestígio/recomeço (vira a primeira atualização após lançar)
- ❌ Animais e estações do ano
- ❌ Pessoas na fazenda com diálogos/histórias
- ❌ Aplicativo próprio para celular (a versão web já funciona no navegador do celular)
- ❌ Tradução para outros idiomas

## 7. O que significa "pronto"

O jogo está pronto quando **qualquer pessoa** puder abrir o link, jogar do
começo ao fim, fechar, voltar depois e continuar de onde parou — sem travar e
sem precisar de explicação.
