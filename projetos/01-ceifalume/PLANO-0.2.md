# Ceifalume 0.2 — plano de atualização (criado 2026-09-23, ordem do dono: "faça tudo que você recomenda")

## 0. Regra de ritmo (decidida com o dono em 23/09)

- **Ciclo:** 3–4 semanas entre versões nos primeiros meses; cada versão = **1 coisa nova que dê para mostrar num GIF** + correções.
- **Bug que impede jogar** (crash, save perdido, "Run game" não abre) não espera ciclo → **0.1.1 no mesmo dia**.
- **Calendário desta rodada:**

| Data | Marco |
|---|---|
| 23/09 → 05/10 | **Coletar, não construir**: rodadas diárias, posts sáb/ter, Reddit manual, post de coleta (§3). Meta: 5–10 opiniões reais |
| ~05/10 | **Decidir o escopo da 0.2** com o que apareceu (dono escolhe da lista §2) |
| ~19/10 | **Lançar 0.2** (4–5 semanas após o 0.1) — se não houver feedback, vai o pacote "sem feedback" (§2, linha A) |
| depois | 0.3, 0.4… a cada 3 semanas |

## 1. Análise do APK (feita em 23/09 sobre o `ceifalume.apk` publicado — 83,6 MB)

**Descoberta principal: o jogo em si tem 3,4 MB. Os outros 80 MB não são conteúdo.**

| Componente | Tamanho no APK | O que é |
|---|---|---|
| `lib/arm64-v8a/libgodot_android.so` | **70,0 MB** | o motor Godot 4.5.2 (template oficial release, sem símbolos de debug, só arm64 — está correto) |
| `classes*.dex` | 7,6 MB | código Java/Kotlin: Google Mobile Ads (AdMob) + UMP + OkHttp + Kotlin |
| `assets/` (o jogo) | 3,4 MB | 2 fundos 1280×720 (0,9 MB cada), fontes Baloo2 (0,4 MB), música (0,2 MB), cenas/scripts |
| `res/`, `resources.arsc` | 1,1 MB | ícones e recursos Android |
| `libc++_shared.so` | 1,3 MB | runtime C++ |

**O achado que muda tudo:** o `.so` de 70 MB está **guardado sem compressão** dentro do APK (método "stored"). Comprimido com zip nível 9 ele cai para **23,2 MB**. Ou seja:

> **APK hoje 83,6 MB → ≈ 36,5 MB só mudando a forma de empacotar. Zero mudança no jogo.**

**Como fazer (0.2 ou até 0.1.1):** no `export_presets.cfg` do preset Android, ativar **`gradle_build/compress_native_libraries=true`** (opção do Godot 4.3+; no editor: Export → Android → Gradle Build → *Compress Native Libraries*). Efeito: o Android extrai a lib na instalação (instalação ~1 s mais lenta na primeira vez; espaço em disco igual ao de hoje). Para download direto/itch é exatamente o que queremos; para a Play Store (futuro) o Google prefere sem compressão, mas lá o AAB resolve sozinho. **Custo: 1 linha + rebuild + re-upload em itch e GitHub Release.**

**Segundo passo (opcional, maior):** template de exportação **customizado** do Godot com `disable_3d=yes`, módulos não usados desligados e `optimize=size` — em jogos 2D isso costuma levar o `.so` para 25–35 MB **antes** da compressão → APK final na casa de **15–20 MB**. Exige compilar o Godot (SCons + NDK, ~1–2 h de máquina). Fica para 0.3+ se o download continuar sendo gargalo depois do passo 1.

**Terceiro (miúdo):** os dois fundos PNG de 0,9 MB podem virar WebP/ctex com perda leve (−1,2 MB). Não muda nada relevante enquanto o motor pesa 70 MB.

**Web:** o `index.wasm` chega em ~8,1 MB gzip pelo Pages (12 s em 4G) — está dentro do normal para Godot 4; o template customizado do passo 2 também reduziria isso.

## 2. Candidatos à 0.2 (o dono escolhe ~05/10; regra: 1 vitrine + correções)

### Linha A — "sem feedback" (se ninguém disser nada até 05/10)
1. **APK ≈ 36 MB** (compressão da lib) — ataca diretamente o gargalo "veem e não instalam" (66 views, 2 downloads itch / 21 GitHub).
2. **Polimento dos 3 primeiros dias** (o "tutorial macio"): uma frase de objetivo na tela ("plante 3 sementes e durma"), destaque no que tocar primeiro, recompensa visível ao acordar (o quanto a fazenda rendeu offline, em número grande).
3. **Correções acumuladas** que aparecerem nas rodadas / #bugs.

### Linha B — vitrine de GIF (escolher 1)
| # | Ideia | Por que | Esforço |
|---|---|---|---|
| B1 | **Resumo da noite** ao voltar: "enquanto você dormia: +12 abóboras, +R$ 40, choveu" com animação | é *a* mecânica do jogo (idle) e hoje é invisível; vira GIF perfeito e post "a fazenda trabalhou por você" | médio |
| B2 | **Uma cultura nova** (ex.: girassol noturno) com visual próprio | conteúdo clássico de update, GIF fácil | baixo |
| B3 | **Evento de clima** (tempestade/lua cheia com bônus) | dá variação e assunto ("dia 9, chuva boa" já rendeu) | médio |
| B4 | **Melhoria comprável** (espantalho, cerca, lanterna melhor) com efeito visível na fazenda | dá meta de médio prazo ao jogador | médio |
| B5 | **Marco/conquista simples** ("100 colheitas") com aviso | retenção + post de números | baixo |

**Sugestão do assistente se o dono quiser um chute:** A1 + A2 + **B1** (o resumo da noite). É o que mais explica o jogo em 5 segundos de GIF, resolve a sensação de "não aconteceu nada" e casa com o nome do devlog: *a fazenda não dorme*.

### Fora da 0.2 (anotado, não perdido)
- Idioma inglês na interface (a comunidade que está reagindo é internacional; forte candidato à 0.3).
- Template customizado do Godot (§1, passo 2).
- Play Store (decisão fechada: só com receita de AdMob).

## 3. Post de coleta de opinião ("o que você mudaria?") — **publicado em 24/09 12h** (janela opcional; corrigido — 25/09 é sexta), 6 canais

**Bluesky (≤300):**
> 🌙 Ceifalume 0.1 tem 1 semana. Antes de fazer a 0.2, quero ouvir quem jogou:
> — os 3 primeiros dias foram lentos, rápidos ou confusos?
> — o que você quer ver primeiro: resumo do que a fazenda rendeu à noite, cultura nova, ou evento de clima?
> Responde aqui que eu leio tudo. ▶ https://reboclbrank-max.itch.io/ceifalume
> #indiedev #godot

**Mastodon / Threads / Telegram / Discord #anúncios (pt+en):**
> 🌙 Ceifalume 0.1 completou 1 semana: 66 visitas, jogadores no navegador e no Android, e o trailer rodando. Obrigado!
>
> Antes de começar a 0.2, quero ouvir quem jogou:
> 1. Os 3 primeiros dias foram lentos, rápidos ou confusos?
> 2. O que você quer primeiro: (a) resumo do que a fazenda rendeu enquanto você dormia, (b) uma cultura nova, (c) eventos de clima?
> 3. Algo travou ou ficou pequeno demais no celular?
>
> Já decidido para a 0.2: APK bem menor (de 79 MB para ~36 MB).
>
> ▶ https://reboclbrank-max.itch.io/ceifalume
>
> *Ceifalume 0.1 is one week old. Before 0.2: were the first 3 days slow, fast or confusing? What first — overnight summary, a new crop, or weather events? Smaller APK is already on the list.*
>
> #indiedev #godot #idlegame #jogosbr

**Tumblr:** mesmo texto pt+en, com o GIF.
**itch devlog nº 2 (dono cola, ou fica para o assistente descrever tela a tela):** título *"1 semana de Ceifalume: o que vem na 0.2 (e eu quero sua opinião)"*, corpo = texto acima + tabela da §1 resumida (jogo 3,4 MB, motor 70 MB, APK vai cair pela metade).

## 4. O que o assistente já pode fazer sozinho antes de 05/10
- [x] Análise do APK (§1) — feita.
- [x] Lista de candidatos (§2) — feita.
- [x] Publicar o post de coleta (§3) na quinta 24/09 12h — **feito**: 5 canais publicados (Threads bloqueado pela Meta), links em `FEEDBACK-0.1.md` §2.
- [x] Criar `FEEDBACK-0.1.md` — feito em 24/09 12h (o caderno existe; as rodadas seguintes só registraram).
- [ ] 05/10: relatório "o que ouvimos" + recomendação final de escopo → dono decide.
- [ ] Quando o dono liberar o repositório `ceifalume` neste ambiente: aplicar `compress_native_libraries=true`, rebuild, medir o APK real, testar instalação.
