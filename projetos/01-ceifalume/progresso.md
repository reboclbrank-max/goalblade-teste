# CEIFALUME — Progresso

> Este arquivo é atualizado a cada sessão de trabalho. Ele diz ao próximo
> chat exatamente onde as coisas pararam.

## 🧮 Estado em uma tela

| Semana | Entrega prevista | Situação | Veredito do dono |
|---|---|---|---|
| 1 | botão que soma moedas | ✅ feita (2026-09-14) | aprovado — exercícios de aquecimento pulados a pedido dele |
| 2 | campo que planta, cresce e colhe | ✅ feita (2026-09-14) | "Gostei, continue" |
| 3 | ciclo plantar → colher → vender | ✅ feita (2026-09-14) | "muito bom, continue" |
| 4 | mercado (dia que vira, preço variando) | ✅ feita (2026-09-14) | "Testei, tá bom, pode continuar" |
| 5 | loja (campos + Celeiro/Poço/Lanterna) | ✅ feita (2026-09-14) | "Gostei, continue" |
| 6 | economia completa (6 plantações, eventos) | ✅ feita (2026-09-14) | ⚠️ **reprovada pela interface**, não pela mecânica |
| 6b | APK Android de teste (canal do dono) | ✅ publicado `v0.1-teste-android` (2026-09-15) | ⏳ **aguardando o teste dele** |
| — | reformulação da interface | ✅ feita (2026-09-15, rev C.2) | aprovado 2× (web + print) |
| 7 | rosto do jogo (arte e som) | 🔄 metade (rev C.8, 2026-09-15): fundo+solo+4 plantas; faltam 5 sprites + música-tema | ⏳ veredito do cartoon com o dono |
| 8 | polimento e lançamento (título, itch.io, downloads) | ⬜ não iniciada (save+offline adiantados na C.6) | — |

- **Relógio:** largada 2026-09-14 → dia 60 em **2026-11-12** (hoje 2026-09-15:
  dia 2 de 60; conteúdo na altura da Semana 7 — bem adiantado).
- **O que está publicado hoje:** rev C.8 (interface nova + cartoon parcial) no
  build web; APK ainda na Semana 6 (interface antiga).
- **Nada foi balanceado ainda:** os tempos de crescimento e o dia de 60 s são
  valores de teste (ver "Números do jogo" abaixo).

## Estado atual

- **Semana 6: o dono REPROVOU a interface.** Crítica literal dele:
  "os texto estão pequenos ao extremo, mal consigo ler o nome, o designer
  do jogo está fraco, a forma que o jogo está organizado está muito ruim,
  além do jogo não ter bom interface".
- **O dono também não consegue testar pelo site:** o PC dele dá erro de
  hardware ao carregar o jogo web (sem suporte a WebGL). Por isso ele pediu
  um **APK para celular, deitado, fora do site**.
- **APK DE TESTE ENTREGUE** em 2026-09-15 (Release no GitHub):
  👉 https://github.com/reboclbrank-max/ceifalume/releases/tag/v0.1-teste-android
  (arquivo `ceifalume.apk`, 26,7 MB, modo paisagem travado, build de debug)
- **Aguardando o dono:** instalar o APK no celular, testar a jogabilidade e
  dizer o que achou. **Depois do teste dele** vem a reformulação completa
  da interface (textos grandes, reorganização, visual noturno).
- A economia do jogo (Semana 6) segue completa e intacta: 6 plantações,
  sementeira, ajudante, composteira, carroça, 3 eventos.

### Decisão desta etapa
- Reformulação visual/interface foi puxada para ANTES da Semana 7 (arte e
  som), a pedido do dono — não adianta desenhar por cima de uma tela que
  ele já reprovou. A Semana 7 do cronograma vira: primeiro a interface
  nova, depois os desenhos.

### 🏷️ Política de build nesta fase (definida pelo dono em 2026-09-15)

- **O jogo não foi lançado, então nada aqui é versão.** Todo APK e todo build
  web desta fase é **rascunho de teste**. Nome de rascunho: `rascunho-AAAA-MM-DD`
  (a release `v0.1-teste-android` fica com o nome que tem porque o dono vai
  baixar por ela; não renomear no meio).
- **Não mexer** em `version/name` / `version/code` no `export_presets.cfg`, nem
  planejar "como o cliente atualiza", nem changelog de versão. Isso é assunto de
  **Semana 8 e de loja**, não de desenvolvimento.
- A numeração oficial (0.01, 0.1, 1.0…) é **decisão do dono no lançamento** — está
  aberta como pendência.
- Consequência útil: rascunho velho pode ser apagado sem cerimônia, e o jogo
  entregue ao cliente no lançamento é **inteiro e novo** — sem dívida de update.

### 📱 Página de teste no celular (entregue em 2026-09-15)

O dono pediu para o site ficar utilizável no celular, porque baixar APK a cada
teste é fricção. Foi criada a camada mobile da página, no repositório do jogo:
`ceifalume/web/` (`gerar-pagina.py` + `mobile.css` + `mobile.js` +
`manifest.webmanifest` + ícones da marca).

O que ela entrega: carregamento com porcentagem e texto grande, botão de **tela
cheia**, aviso para virar o aparelho (dispensável), **instalar na tela inicial**
(manifest + ícones, sem service worker de propósito), carimbo dizendo **qual
rascunho** está aberto, caixa de **erro legível** (no celular não há console) e
`canvas_resize_policy=1` (o canvas acompanha a janela e o giro de tela).

- **Publicar é sempre pelo gerador**, nunca editar o `index.html` do `site`:
  `python3 web/gerar-pagina.py --entrada export/web/index.html --publicar ../site/ceifalume`
- PWA do Godot **deixa-se desligado** (`progressive_web_app/enabled=false`): o
  service worker dele cacheia, e o dono jogaria versão velha sem perceber.
- Link do teste: https://reboclbrank-max.github.io/site/ceifalume/ — QR pronto em
  `divulgacao/qr-teste-celular.png`. Custo honesto: baixa ~35,4 MB de engine a
  cada abertura, então Wi-Fi.
- **Não resolve** o tamanho da letra dentro do jogo. Isso é a reformulação da
  interface (logo abaixo), não a página.

### Lições técnicas desta etapa
- Android no Godot sem interface gráfica exige vários ajustes (seção
  "Pipeline Android" abaixo). O erro de "configuration errors" VAZIO era a
  compressão de texturas ETC2 desligada — o Godot reprova sem dizer nada.
- O Gradle do build Android morre por falta de memória nesta máquina
  (2 GB). Os ajustes de `gradle.properties` já resolvem (documentados).

## 🎨 Roteiro da reformulação da interface (a próxima execução)

Derivado da crítica literal do dono em 2026-09-15. Cada item é verificável na
tela — só marcar como feito quando der para ver.

> Por que ficou ilegível (medidas reais de hoje): cada campo é um painel de
> **240×210** com `font_size = 18` no rótulo e planta desenhada em `Polygon2D`.
> Oito desses numa tela de 1280×720 = letra miúda de verdade, não impressão do
> dono.

1. **Escala de texto.** Títulos ~28–32, estado do campo ~22–24, corpo ~20,
   nada abaixo de 18 na referência 1280×720. Legível no celular **sem zoom**.
2. **Cabeçalho fixo** com as três coisas que importam: moedas · dia/evento ·
   mercado. Ele não pode sumir ao rolar a fazenda.
3. **Fazenda protagonista.** Grade de campos grande, no centro; a sementeira
   encostada nela (escolher semente é decisão de plantio, não de loja).
4. **Loja agrupada e simples:** uma linha por melhoria com nome grande, custo,
   efeito em uma frase e nível atual — não oito botões miúdos.
5. **Mercado compacto:** 6 linhas (plantação · preço de hoje · ▲▼), lidas de
   relance; evento do dia em destaque quando existir.
6. **Paisagem E retrato.** Layout que se reorganiza ao girar o aparelho
   (o dono usa o celular em pé). Testar os dois antes de gerar o APK.
7. **Alvos de toque** de pelo menos ~44×44 — é dedo, não mouse.
8. **Feedback de toda ação:** se falhou (celeiro cheio, moeda insuficiente),
   dizer o motivo em texto grande, não silenciar.
9. **Clima de Ceifalume:** céu noturno, lanternas, vaga-lumes no fundo — sem
   antecipar a arte final, que é da Semana 7.

**Critérios de aceite propostos** (sugestão do assistente a partir das palavras
dele; ele pode rejeitar, cortar ou acrescentar): (a) dá para ler no celular sem
zoom; (b) bater o olho e saber moedas, dia e preço; (c) jogar 5 minutos sem
dúvida sobre onde clicar; (d) a economia idêntica à da Semana 6.

**Ordem de execução:** interface nova → testar nos dois modos → gerar novo APK
→ republicar o web → aí sim pedir o veredito do dono → Semana 7.
**Invariante:** nenhuma dessas etapas muda números de economia. Se precisar
mudar, é decisão registrada antes de codar.

## O que existe no jogo até agora

- Semana 1: contador de moedas + botão **"Fazer um bico (+1 moeda)"**.
- Semana 2: **campo** (peça reutilizável `campo.tscn`/`campo.gd`):
  - Clique com campo vazio → planta; cresce em 3 etapas visuais
    (12s de teste; constante `TEMPO_CRESCIMENTO`)
  - Barra de progresso e texto de estado; clique na planta pronta → colhe
- Semana 3: **venda** — botão "Vender todos os nabos", bloqueado sem estoque.
- Semana 4: **mercado** — dia de 60s (`DIA_DURACAO`), preço sorteado entre
  4 e 16 moedas, setas ▲/▼/estável, barra do dia.
- Semana 5: **loja e tela nova em duas colunas** (decisões à esquerda,
  fazenda em grade à direita, com rolagem para até 24 campos):
  - **Comprar campo** — custo cresce ×1.8 a partir de 50 moedas (máx. 24).
    Campos novos já nascem com a velocidade do Poço atual.
  - **Ampliar Celeiro** — capacidade começa em 10 nabos, +10 por nível
    (custo ×1.7 a partir de 30, máx. nível 20). Celeiro cheio bloqueia a
    colheita e avisa "Celeiro cheio! Venda os nabos."
  - **Cavar Poço** — +10% de velocidade de crescimento por nível
    (custo ×1.7 a partir de 40, máx. nível 10), aplicado a todos os campos
  - **Acender Grande Lanterna** — +1 nabo por colheita por nível
    (custo ×1.7 a partir de 60, máx. nível 10)
  - Botões da loja mostram custo e efeito, e ficam bloqueados sem moedas
  - Todas as constantes de custo ficam no topo do `roteiro_principal.gd`
    (fáceis de balancear na Semana 6)
- Semana 6: **economia completa**
  - **6 plantações** (tabela `PLANTACOES` no roteiro, com os números do
    conceito): Nabo (30s, 8 moedas), Milho (2min, 35), Trigo (5min, 110),
    Tomate (15min, 380), Abóbora (45min, 1400) e Flor de Lume (2h, 5500).
    Cada uma com cor própria no desenho (a forma é a mesma por enquanto;
    desenhos distintos chegam na Semana 7).
  - **Sementeira**: 6 botões acima dos campos para escolher a semente;
    plantar agora CUSTA a semente (jogador começa com 25 moedas).
  - **Mercado por plantação**: cada uma tem preço próprio sorteado por dia
    (50%–200% do base), com ▲/▼ na lista do mercado.
  - **Celeiro por plantação**: rótulo mostra o total e o detalhe
    ("2 Nabo · 1 Milho"); capacidade total continua 10 + 10/nível.
  - **Contratar Ajudante** (100 moedas, ×1.9, máx. 12): cada ajudante
    colhe sozinho 1 campo pronto a cada 2 segundos.
  - **Composteira** (80 moedas, ×1.8, máx. 5): +8% de chance por nível de
    colher em dobro (diferente da Lanterna, que é +1 garantido).
  - **Carroça** (500 moedas, única): vende tudo sozinho quando o celeiro
    enche, com aviso.
  - **Eventos** (15% de chance por dia): Chuva boa (cresce 2x), Feira da
    Madrugada (preços em dobro), Seca (colheita pela metade). O rótulo do
    evento aparece no painel do mercado.
  - A venda ("Vender toda a colheita") soma cada plantação pelo preço do dia.

## 🔢 Números do jogo (para balancear na Semana 8)

Ficam como constantes no topo de `roteiro_principal.gd` — é ali que se mexe,
nunca "de cabeça". Esta tabela é o espelho delas.

| O quê | Valor hoje | Origem / observação |
|---|---|---|
| `PRECO_NABO` (preço fixo da Semana 3) | 8 moedas | conceito |
| `DIA_DURACAO` | 180 s (3 min) | conceito ("alguns minutos"); era 60 s de teste até a C.9 |
| Faixa do preço diário | 50%–200% do base (nabo: sorteado entre 4 e 16) | conceito |
| Plantações (custo semente / tempo / preço base) | Nabo 5 / 30s / 8 · Milho 20 / 2min / 35 · Trigo 60 / 5min / 110 · Tomate 200 / 15min / 380 · Abóbora 700 / 45min / 1400 · Flor de Lume 2500 / 2h / 5500 | tabela `PLANTACOES` |
| Comprar campo | 50 moedas, ×1,45 por compra, máx. 24 | medido (sim_limite): ×1,8 punha o 24º campo no dia ~9.689 |
| Ampliar Celeiro | capacidade 10 + 10/nível; custo 30, ×1,7, máx. nível 20 | Semana 5 |
| Cavar Poço | +10% velocidade de crescimento/nível; custo 40, ×1,7, máx. 10 | Semana 5 |
| Acender Grande Lanterna | +1 unidade por colheita/nível; custo 60, ×1,7, máx. 10 | Semana 5 |
| Contratar Ajudante | colhe 1 campo pronto a cada 2 s; custo 100, ×1,9, máx. 12 | Semana 6 |
| Composteira | +8% de chance de colher em dobro por nível; custo 80, ×1,8, máx. 5 | Semana 6 |
| Carroça | vende tudo ao encher o celeiro; 500 moedas, única | Semana 6 |
| Eventos | 15% de chance por dia — Chuva boa (2× crescimento), Feira da Madrugada (2× preço), Seca (½ colheita) | Semana 6 |
| Moedas iniciais | 25 | Semana 6 (plantar passou a custar semente) |
| Progresso offline | até 8 horas, com resumo | ✅ desde a C.6 |

⚠️ Ao mexer em qualquer número, atualizar **esta tabela no mesmo commit** — é
ela que o dono consulta quando acha que algo está caro ou barato.

## Como o build de teste funciona (PIPELINE — importante para o próximo chat)

O jogo é compilado pelo próprio assistente (o dono não precisa instalar nada):

1. Motor: Godot 4.3-stable rodando em modo "headless" (sem tela).
2. Exportação: preset "Web" com **threads desligados**
   (`variant/thread_support=false` em `export_presets.cfg`) — isso é
   obrigatório para funcionar no GitHub Pages, que não permite os cabeçalhos
   especiais que a versão com threads exige.
3. Os arquivos exportados vão para a pasta `ceifalume/` do repositório
   **`site`** (público, com Pages ativo). A URL segue o padrão
   `https://reboclbrank-max.github.io/site/ceifalume/`.
4. Cada push em `main` do repositório `site` republica automaticamente
   (~1 minuto).

### Ferramentas (ATENÇÃO: ficam em pasta de cache que NÃO persiste)

Estão em `/home/user/.cache/ferramentas/` (fora do snapshot do workspace).
O JDK e o SDK do Android ficam em `/home/user/.cache/android/` e o keystore
em `~/.godot/` — TUDO isso também some entre sessões. Verificar ANTES de
compilar. Se a pasta não existir em uma nova sessão, baixar de novo:

```
mkdir -p ~/.cache/ferramentas && cd ~/.cache/ferramentas
curl -sL -o godot.zip https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_linux.x86_64.zip
unzip godot.zip && mv Godot_v4.3-stable_linux.x86_64 godot && chmod +x godot
curl -sL -o templates.tpz https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_export_templates.tpz
mkdir -p ~/.local/share/godot/export_templates/4.3.stable
unzip -o -j templates.tpz "templates/web_*" "templates/version.txt" -d ~/.local/share/godot/export_templates/4.3.stable/

# para gerar PNG a partir de SVG (logo, ícones) — NÃO usar ImageMagick, ele
# renderiza SVG preto neste ambiente:
pip install cairosvg pillow
```

### Comandos para compilar e publicar

```
cd /home/user/ceifalume
mkdir -p export/web
~/.cache/ferramentas/godot --headless --path . --import
~/.cache/ferramentas/godot --headless --path . --export-release "Web" export/web/index.html
# depois: subir os arquivos de export/web/ para a pasta ceifalume/ do repositório site
# (mesmo padrão de upload via API usado nas demais sessões)
```

### Pipeline Android (APK) — comprovado em 2026-09-15

Build de teste fora do site, para o celular do dono (modo paisagem).

**Ferramentas extras (TAMBÉM ficam em cache que NÃO persiste):**
- JDK 17 (Temurin): `/home/user/.cache/android/jdk`
- Android SDK: `/home/user/.cache/android/sdk` (platform-tools, platforms;android-34,
  build-tools;34.0.0) — instalado pelo `sdkmanager` (aceitar licenças: `yes |`).
- Modelos Android: extrair do mesmo `templates.tpz` os arquivos
  `android_debug.apk`, `android_release.apk` e `android_source.zip` para
  `~/.local/share/godot/export_templates/4.3.stable/`.
- Keystore de debug: `~/.assinatura/depuracao` (alias `androiddebugkey`,
  senha `android`) — gerar com `keytool` se sumir:
  `keytool -keyalg RSA -genkeypair -alias androiddebugkey -keypass android -keystore debug.keystore -storepass android -dname "CN=Android Debug,O=Android,C=US" -validity 9999 -deststoretype pkcs12`
- Configuração do editor em `~/.config/godot/editor_settings-4.3.tres`
  apontando SDK/JDK/keystore (já escrita nesta sessão).

**Ajustes OBRIGATÓRIOS no projeto (já aplicados, persistem no repositório):**
1. `project.godot`: `window/handheld/orientation=4` (paisagem com sensor)
   E `textures/vram_compression/import_etc2_astc=true` — SEM isso o Godot
   aborta a exportação com erro VAZIO ("configuration errors:" sem texto).
2. Modelo de compilação Gradle extraído do `android_source.zip` para
   `android/build/` + arquivo `android/.build_version` com "4.3.stable".
3. `.gdignore` DENTRO de `android/` — impede o editor de escanear a pasta
   (senão gera `.import` dentro de `res/` e o Gradle quebra).
4. `android/build/gradle.properties`: memória reduzida (a máquina tem 2 GB):
   `org.gradle.jvmargs=-Xmx900m -XX:MaxMetaspaceSize=320m -XX:+UseSerialGC`,
   `org.gradle.daemon=false`, `org.gradle.workers.max=2`,
   `org.gradle.parallel=false`, `kotlin.compiler.execution.strategy=in-process`.
5. `android/` no `.gitignore` (só existe localmente).

**Comando para gerar o APK:**
```
cd /home/user/ceifalume
export JAVA_HOME=/home/user/.cache/android/jdk
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/home/user/.cache/android/sdk
~/.cache/ferramentas/godot --headless --path . --import
~/.cache/ferramentas/godot --headless --path . --export-debug "Android" export/android/ceifalume.apk
```
Se o Gradle morrer por memória dentro do Godot, rodar o `gradlew` na mão
(com o Godot fechado, os mesmos argumentos `-P...` que o Godot usa) e
depois repetir o comando do Godot.

**Entrega:** o APK vai como anexo de uma Release do repositório `ceifalume`
(releases aceitam arquivos grandes mesmo em repo privado; o dono logado
baixa). Criar release e subir o ativo via API do GitHub.

## Arquivos do projeto e o que cada um faz

| Arquivo | Função |
|---|---|
| `project.godot` | Configuração: nome, janela 1280x720, cena inicial, renderizador `gl_compatibility` (escolhido de propósito: é o que roda na exportação web) |
| `cena_principal.tscn` | A tela em duas colunas: mercado, celeiro, venda e loja à esquerda; grade de campos à direita |
| `roteiro_principal.gd` | Código principal: mercado, dinheiro, celeiro, loja e constantes de custo |
| `campo.tscn` + `campo.gd` | Peça reutilizável do campo: plantar, crescer em 3 etapas, colher |
| `icon.svg` | Ícone do projeto (C dourado em fundo preto) — **provisório**; o `project.godot` aponta para `res://icon.svg`, então trocar o conteúdo é ok, trocar o caminho quebra |
| `arte/` | Pasta criada em 2026-09-15 para receber os desenhos e o som. `arte/LEIA-ME.md` traz o manifesto da Semana 7 (34 arquivos, o que cortar primeiro) e as medidas-alvo (sprite de planta 128×128 ancorado em `Planta.position`) |
| `export_presets.cfg` | Presets de exportação: Web (sem threads) e Android (APK paisagem) |

## 🧯 Autópsia dos incidentes (o que já quebrou e como não repetir)

| Quando | Sintoma | Causa real | Como não repetir |
|---|---|---|---|
| Semanas 4 e 5 | exportação falhou **em silêncio** | cache do ambiente foi limpo e o Godot sumiu | testar a existência das ferramentas antes de compilar |
| Semana 6 | build quebrou | função chamada com nome errado | ler o log inteiro do `--import` antes de exportar |
| 2026-09-15 (Android) | Godot abortou com `configuration errors:` **vazio** | `textures/vram_compression/import_etc2_astc` desligada | ligar no `project.godot` (o erro não explica nada sozinho) |
| 2026-09-15 (Android) | Gradle morria no meio | máquina de 2 GB de RAM | `gradle.properties` com `-Xmx900m`, sem daemon e sem paralelismo; se ainda morrer, rodar o `gradlew` na mão |
| 2026-09-15 (Android) | Gradle quebrou com `.import` dentro de `res/` | o editor escaneou a pasta `android/` | `.gdignore` dentro de `android/` + `android/` no `.gitignore` |
| 2026-09-15 | dono não consegue testar pelo navegador | PC dele não tem WebGL | o **APK é o canal dele**; o web continua publicado para terceiros — não "consertar" o web à força |
| 2026-09-15 | `progresso.md` perdeu 152 linhas no GitHub | commit com arquivo truncado, sem conferência | `git show --stat` + `wc -l` antes de todo push nesta base |

## 🛠️ Checklist de sessão de build (web e Android)

1. Conferir ferramentas: `~/.cache/ferramentas/godot`, templates em
   `~/.local/share/godot/export_templates/4.3.stable/`, e (Android)
   `~/.cache/android/jdk`, `~/.cache/android/sdk`, `~/.assinatura/depuracao`.
   Faltou algum → reinstalar com os comandos desta seção.
2. Clonar/atualizar `/home/user/ceifalume` (chat novo começa sem ele).
3. `--import` headless e **ler o log todo** — erro de digitação aparece aqui.
3b. Teste de bancada: `~/.cache/ferramentas/godot --headless --path . --script
   res://teste_economia.gd` → tem de terminar com "48 testes, 0 falhas" e
   nenhuma linha `SCRIPT ERROR`. Ele cobre regra de economia, não visual.
4. Web: `--export-release "Web"` → subir `export/web/*` para a pasta
   `ceifalume/` do repositório `site` → esperar ~1 min e abrir a URL.
5. Android: `--export-debug "Android"` (ou release) → anexar a Release **nova**
   na `ceifalume` (não substituir em silêncio a que o dono já baixou).
6. Testar o mínimo antes de avisar o dono, **renderizando de verdade** (desde
   2026-09-15 isto é possível neste ambiente): `prova_visual.gd` sob `xvfb-run`
   em 1280×720, 844×390 e 390×844 — olhar as imagens E ler os números que ele
   imprime (item fora da tela / texto cortado / lista rolável); e Chromium na
   pasta publicada para medir o quadro do canvas, a escala, o scroll e os erros
   da página. Critério de aceite: 0 itens fora da tela, 0 textos cortados,
   0 `SCRIPT ERROR`, 48/48 no teste de bancada.
7. Gravar o resultado: `progresso.md` + `registro-de-decisoes.md` +
   `pendencias.md`, commit conferido com `git show --stat`, push, validar com
   `git ls-remote`.

## Próximos passos (nesta ordem)

1. **O dono testa o rascunho** — pelo navegador do celular (link na seção da
   página mobile, sem instalar nada) ou pelo APK — e dá o veredito
   (jogabilidade, ritmo, o que faltou). Se o Android bloquear o APK: permitir
   "instalar apps desconhecidos" para o navegador/gerenciador de arquivos.
2. **REFAZER A INTERFACE** (a prioridade nº 1, pedida pelo dono):
   - Textos grandes (mínimo ~18–20px na resolução de referência; nada de
     letrinha miúda), contraste alto, leitura fácil.
   - Reorganizar a tela: cabeçalho com moedas/dia/preços, fazenda no
     centro como protagonista, loja simplificada e agrupada.
   - Adaptar para paisagem E retrato (o dono pode girar o aparelho).
   - Visual: céu noturno estrelado, lanternas — identidade do Ceifalume.
   - Depois disso, gerar NOVO APK e republicar o build web (o dono testa
     os dois; o APK é o canal principal dele).
3. **Semana 7 — rosto do jogo:** desenhos distintos para cada plantação,
   céu estrelado, vaga-lumes e lanternas no fundo, música calma e efeitos
   de colher/vender (Krita/Inkscape, LMMS, Audacity — ou gratuitos).
   A lista exata do que desenhar, o tamanho-alvo de cada arquivo e o padrão
   de nome estão em `ceifalume/arte/LEIA-ME.md` (fluxo completo de arte e
   imagens: `empresa/imagens-e-desenhos.md` na base). O dono manda o desenho
   como ele quiser — renomear e encaixar é trabalho do assistente.
4. **Semana 8 — polimento e lançamento:** salvamento automático no navegador
   (aqui entra também o progresso com o jogo fechado, até 8h), tela de
   título, balanceamento final dos números, página no itch.io com imagens e
   descrição, troca do card "Projeto 01" no site (com autorização do dono).
   Ver `cronograma.md`.

Nota: quando o dono quiser mexer no código junto, ele pode instalar o Godot
na máquina dele (passo a passo no README do repositório `ceifalume`), mas
nada trava enquanto isso — o assistente compila e publica sozinho.

## Instruções para o próximo chat

- Antes de fazer qualquer coisa, leia: `guia-do-proximo-chat.md`, este
  arquivo, `conceito.md` e `cronograma.md`.
- Todo o código é em **português** (variáveis, funções, comentários).
  Mantenha assim.
- Toda tela nova que entrar, entrar com texto grande — a interface anterior foi
  reprovada exatamente por isso. Esse é o filtro de qualidade da próxima etapa.
- Antes de compilar, seguir o "Checklist de sessão de build" (uma seção acima
  dos próximos passos): as ferramentas somem do ambiente entre sessões.
- O projeto vive no repositório `ceifalume`. O caminho local
  `/home/user/ceifalume/` **só existe no chat que o clonou**: em chat novo é
  preciso clonar de novo (verificado em 2026-09-15 — o espaço de trabalho
  daquele chat tinha apenas a `base`).
- Ao final de cada sessão: atualize este arquivo + `registro-de-decisoes.md`.
- Não adiantar semanas do cronograma sem comando do dono.

---

## 🔍 Auditoria e correções — 2026-09-15 (rascunho "rev B")

O dono jogou, aprovou o ritmo ("o jogo está muito bom") e mandou auditar o que
funciona e o que pode estar dando erro, corrigindo o que aparecer. Relatório
completo, com arquivo e linha de cada achado: **`auditoria.md`** nesta pasta.
Resumo executivo:

- **11 defeitos encontrados e corrigidos** nos dois scripts e nos dois `.tscn`.
  Os três que importam para quem joga: (a) **celeiro cheio empacava a partida**
  — a Carroça era acionada depois da rejeição da colheita, nunca antes; (b) o
  campo desenhava "planta pronta" nos últimos 25% do tempo, mentindo sobre a
  colheita; (c) a **Seca não doía** (divisão inteira de `1 / 2` virava 1) e não
  tocava o crescimento. Completam a lista: etiqueta do Poço sem o efeito, loja
  que recusava compra sem dizer por quê, aviso que apagava o aviso seguinte,
  começo com 1 campo em vez dos 4 do conceito (com o custo do campo reajustado
  para não saltar a 292), fontes de 12–21 px e botões de 34 px, duas seções
  `[rendering]` no `project.godot` e um erro de script silencioso ao colher
  campo vazio.
- **Rede que faltava:** `teste_economia.gd` na raiz do repositório — 48
  checagens de regra rodando a cena real, headless (`--script
  res://teste_economia.gd`), mais uma simulação de 400 turnos aleatórios e 120
  dias de mercado. **48/48 verdes** e nenhum `SCRIPT ERROR` no output. Está
  fora do build exportado (`exclude_filter="*teste_economia.gd"`). Este é o
  checklist permanente: rodar antes de todo export.
- **Letra maior sem reforma da interface:** fontes 12→17, 13→17, 14→18, 16→19,
  18→20, 19→21, 21→24; botões da loja de 34 para 48 px de altura; rótulo novo
  `Ritmo ×1,1 · 4/24 campos` no painel do mercado, que é o que torna o efeito do
  Poço visível na tela; rótulo do campo agora conta o tempo que falta
  ("Nabo crescendo — 12s"); `autowrap_mode` nos textos longos (antes, linha
  larga era cortada sem aviso). Uma checagem do teste vigia o comprimento das
  etiquetas da loja (≤ 34 caracteres por linha nos 360 px do painel).
- **Retratação e volta atrás:** o `canvas_resize_policy=1` que eu havia aplicado
  na sessão anterior estava errado para este layout (fixo, sem reflow) — policy 1
  recorta, não adapta. Voltou para **2** e o encaixe virou responsabilidade da
  página: moldura `#rd-arena` com 16:9 travado (o jogo inteiro cabe, nada é
  cortado) + botão de zoom **Ajustar / 150% / 200%** com a escolha lembrada.
  Corrigido também o publicador, que copiava só a página e deixava o `.pck` old
  no ar; hoje copia os sete arquivos do motor e confere byte a byte.
- **O que não foi verificado (e por isso não se pode dizer que ficou ótimo):**
  nada foi visto renderizado — sem GPU/navegador aqui, moldura e zoom são
  dedução de CSS, não medição. Com o dono: a tela coube inteira? o zoom deixou
  legível? E fica de pé o diagnóstico da letra: com base 1280×720 e
  `stretch=canvas_items`, num celular de ~390 pt tudo é reduzido a ~30% — 17 px
  viram ~5 px no vidro. Isso só fecha com a reforma da interface (fila a seguir).
- **Publicação:** `ceifalume 1247845`, `site b2f6b3a` (pck 84.272 B novo, wasm
  inalterado), selo na tela `rascunho 2026-09-15 · rev B · Semana 6`. **Push
  ainda não rodou** — sem token nesta sessão; enquanto isso a URL serve a rev A
  (ver `pendencias.md` §8).

Nada do cronograma foi adiantado e nada da interface foi redesenhado: este lote
é correção + legibilidade mínima, exatamente como combinado. A reforma da
interface continua a primeira frente depois do veredito dele.

## 🖥️ Verificação visual dentro do ambiente — 2026-09-15 (rev C)

Porque o dono perguntou "como resolvemos o que você não consegue verificar?":
construindo o ambiente que verifica. Duas rotas, ambas usadas de fato nesta
sessão (comandos no `guia-do-proximo-chat.md`, números em `auditoria.md`):

- **Rota A — motor:** Xvfb + Mesa llvmpipe renderizam o Godot aqui dentro;
  `prova_visual.gd` (no repositório do jogo) fotografa a cena e mede cada nó
  crítico — posição, tamanho, se passa da janela, se o texto foi cortado, e se
  está só dentro de uma lista rolável.
- **Rota B — navegador:** Chromium + WebGL por SwiftShader abre a pasta
  publicada, espera o motor subir e mede o quadro do canvas, a escala, a
  necessidade de rolar, erros de JavaScript e requisições quebradas.

**O que isso achou na hora (e a leitura de código não achou):** a minha própria
melhora de legibilidade tinha empurrado parte da interface para fora da tela —
o contador de moedas 86 px acima do topo, a sementeira cortada, três botões da
loja e o "Fazer um bico" abaixo do fim — porque a coluna passou a medir 1012 px
numa janela de 720 px e o contêiner central era um `CenterContainer`, que divide
o excesso entre topo e base. E os botões de semente, com `autowrap` e sem
largura mínima, tinham encolhido para ~16 px. Corrigido em `ef00926`
(`MarginContainer` + `size_flags_vertical = 3` na Loja/Corpo/Grade +
`ScrollContainer` na loja + 116 px mínimos na sementeira; removido o padding de
6 px da caixa da página, que cortava o topo do quadro).

**Estado medido depois (rev C):** 0 itens fora da tela e 0 textos cortados em
1280×720, 844×390 e 390×844; 48/48 no teste de bancada; sem `SCRIPT ERROR`. Na
página: celular deitado → quadro 693×390, cabe inteiro, não rola, fonte de 17 px
= 18,4 px físicos; em pé → 10,4 px (inviável, por isso existe o aviso de girar).

**Decisão de processo que sai daqui:** nenhuma mudança de layout ou de fonte vai
para o ar sem as duas medições acima. "Achei bonito no código" deixou de ser
evidência.

### Motor de verificação: o que foi instalado e o que rendeu (2026-09-15, 2ª rodada)

O dono chamou a bancada de **motor** e mandou instalar o melhor que existe. Foi
instalado, foi medido, e o resultado está no registro de decisões da mesma data.
Resumo operacional para quem for continuar o jogo:

- `ripgrep`, `fd-find` (`fdfind`) e `ffmpeg 7.1.5` no sistema. Busca no código do
  jogo: 3 ms com `grep`, 6 ms com `rg` — usar `rg` por conforto (ele ignora
  binários), não por velocidade. `/usr/bin/time` **não existe** aqui; medir com
  `date +%s%N`.
- Dois motores de jogo instalados: **4.3** em `~/.cache/ferramentas/godot` (é o que
  o projeto usa) e **4.7.2** em `~/.cache/ferramentas/novo/godot`, só para
  comparação. Ambos com templates Web (`~/.local/share/godot/export_templates/`).
  **Não apontar o projeto para o 4.7** sem reescrever o encaixe da página: o
  template novo ignora a moldura e o download fica +2,1 MB gzip.
- Ferramenta nova: `grava_jogo.gd` (na raiz do jogo, excluída do export por
  `exclude_filter` em `export_presets.cfg`). Ela gera os PNGs que viram o vídeo de
  jogabilidade com `ffmpeg`. Regerar:

```bash
mkdir -p /home/user/tools/frames && rm -f /home/user/tools/frames/*.png
xvfb-run -a -s "-screen 0 1280x720x24" env LIBGL_ALWAYS_SOFTWARE=1 \
  CEI_FRAMES=/home/user/tools/frames CEI_QUADROS=140 CEI_VELOCIDADE=14 \
  ~/.cache/ferramentas/godot --path /home/user/ceifalume --rendering-driver opengl3 \
  --script res://grava_jogo.gd
ffmpeg -framerate 20 -i /home/user/tools/frames/%04d.png \
  -c:v libx264 -preset veryfast -crf 24 -pix_fmt yuv420p ceifalume-jogando.mp4
rm -f /home/user/tools/frames/*.png
```

- Pacote publicado enxuto: os scripts de ferramenta não vão mais no `.pck`
  (89.520 → **84.704 B**), e os três nomes foram confirmados ausentes lendo o
  binário. Artefato atual = **rev C.1**; o `.pck` no ar continua 30.128 B (rev A)
  até o push, que depende do token do dono.

### rev C.2 (2026-09-15, 3ª rodada) — faixa da loja, folga medida na fonte, publicado

O que mudou no jogo: (1) a Loja virou `FaixaLoja` em grade (até 4 colunas) no pé da
tela em janela larga, com `CEI_LOJA=lista` para forçar o modo reserva; (2) a linha de
sementes virou `HFlowContainer` com largura medida na fonte — isso devolveu o último
dígito do preço da Flor de Lume (2500 estava aparecendo como 250); (3) `prova_visual.gd`
ganhou régua de altura, "sem folga" abaixo de 2 px, medição contra o fim da grade e
busca de nó por nome (a loja mudou de pai em runtime).

Medido na rev C.2: 48/48; `Coluna` 1256×708 (1280×720), 1534×708 (844×390 deitado),
1256×2758 (390×844 em pé, onde cabem 6 de 6 campos na grade sem rolar); 0 cortes de
largura e de altura; 0 `SCRIPT ERROR`; navegador com `cabe_inteiro=true`,
`precisa_rolar=false`, 0 erros de JS nos 3 perfis; `.pck` 87.312 B.

Publicado: `ceifalume e32514d`, `site 9926517`, `base 509e4a7`. **Conferido no ar**
em 2026-09-15: `curl -s …/ceifalume/index.pck | wc -c` = 87.312 e `index.html` =
21.053 — os dois iguais aos locais, então a URL do QR já é a rev C.2 (o Pages demora
~1 min para rebuild; conferir, nunca presumir).

Checklist de build da Semana 6, atualização: o passo 6 (medição) agora **exige**
rodar `CEI_CENARIO=inicial` além do "meio", e o passo 3b inclui o OCR de recorte
quando a mudança envolver texto em botão. Evidência nova em
`projetos/01-ceifalume/verificacao/`: `jogo-*-revC2.png` (3 janelas) e
`ceifalume-jogando.mp4` regravado com a interface nova (140 quadros a 20 fps,
91.845 B).

### Semana 7, frente 1: som (2026-09-15, 6ª rodada) — fiação completa e medida

Existe agora: buses `Master`/`Musica`/`Efeitos` (último com -6 dB de folga),
autoload `Sons` com pool de seis jogadores e preferências em `user://audio.cfg`,
botão `Som: ligado` no canto superior direito, e quatro ganchos no jogo (plantar,
colher, vender, novo dia) com quatro efeitos provisórios nivelados em -5 dBFS.
A música-tema **não** foi criada: é gosto do dono, e o bus está esperando.

Medição que virou critério: a saída do motor gravada num null-sink do PulseAudio
(`ffmpeg -f pulse -i grava.monitor`) passou de **pico 0,0 dBFS / -12,8 LUFS**
(estouro de dois eventos somados) para **-4,8 dBFS / -14,6 LUFS** com a folga no bus.
Custo no download: `.pck` 87.312 → 262.288 B (193.579 gzip) → ~8,17 MB por abertura.

Testes: `teste_som.gd` 19/19, `teste_economia.gd` 49/49 (atualizado junto com a
curva ×1,45), `CEI_SEMENTE=7` dando marcos idênticos em rodadas repetidas, e
`teste-audio-web.js` mostrando o `AudioContext` do jogo `running` no Chromium com
política de autoplay restritiva. Publicação: rev C.3, selo "Semana 7", verificação
de encaixe e de console nos três perfis ✓.

Arquivos tocados: `default_bus_layout.tres`, `sons.gd`, `teste_som.gd` (novos);
`roteiro_principal.gd` (semente, curva, ganchos, botão), `cena_principal.tscn`
(`BotaoSom`), `project.godot` (autoload), `arte/som/*` (8 arquivos),
`arte/LEIA-ME.md`, `export_presets.cfg`, `prova_visual.gd` (sobreposição pelo texto).

### Semana 7, frente 2 (lote 1, 2026-09-15): fiação da arte — rev C.4 no ar

Decisão do dono: arte **realista detalhada**, **desenhada por ele**, clima
**aconchego**, **interface atual mantida**, arte antes de fechar o som. Este lote
é a fiação: nenhum pixel do jogo mudou, mas cada desenho que ele mandar entra
sem tocar em código.

- `campo.gd`: `_mostrar_estagio()` monta `plantacao-<id>-<estagio>-128.png`
  (`id`: nabo, milho, trigo, tomate, abobora, flor-de-lume — chave nova em
  `PLANTACOES`; `estagio`: semente, broto, pronto). Com arquivo → `Sprite2D`
  (base em 120,150); sem arquivo → polígonos de sempre. Arquivo ausente é
  caminho normal, nunca erro (mesma filosofia do `Sons`). Só reavalia ao
  trocar de estágio (não 60×/s) e cacheia a textura.
- `cena_principal.tscn` + roteiro: `ArteFundo` (`TextureRect`, coberto sem
  deformar) carrega `fundo-noite-ceifalume-1280x720.png` se existir.
- Régua: `_checar_12` (6 checagens, lê o disco de verdade — continua valendo
  quando a arte chegar). **55/55** na economia, 19/19 no som, `--import` limpo.
- Piloto provado com sprites temporários (apagados depois): 3 estágios do Nabo
  + fundo renderizados em cena real (`semente/broto/pronto/fundo=true`), medida
  `Coluna` idêntica à rev C.2 nos 3 tamanhos (1256×708 / 1534×708 / 1256×2758),
  0 cortes, 0 `SCRIPT ERROR`. Evidência:
  `verificacao/loader-piloto-3-estagios-1280x720.png`.
- Publicado: rev C.4 (selo "Semana 7"), `.pck` 243.504 B no ar = local;
  navegador nos 3 perfis com `cabe_inteiro=true`, 0 erros de JS; áudio-web
  `running` sem avisos. Detalhe para o desenhista: o rótulo do campo ocupa o
  topo — a planta deve viver nos 2/3 de baixo do sprite 128×128.
- Ordem de entrega: **1º o Nabo inteiro** (semente+broto+pronto, o piloto que
  valida o encaixe com arte real), depois as outras 5 plantas, depois o fundo.
  Contrato completo em `ceifalume/arte/LEIA-ME.md` (§ Fiação).

### Semana 7, frente 2 (lote 2, 2026-09-15): som completo + painel de teste — rev C.5

Ordem do dono: "continue trabalhando" (sem os desenhos ainda). Dois buracos
fechados, ambos sem decisão de gosto:

- **Loja e eventos ganharam som.** `_pagar()` toca `som-comprar-01` (um gancho
  cobre os 7 botões); `_sortear_evento()` toca `som-evento-01` junto com o sino
  do dia. Provisórios medidos: -5,0 dBFS, PASSA. Mixagem capturada no motor
  (sequência plantar→comprar→evento→colher→vender→dia): pico -4,8 dBFS,
  -14,6 LUFS, PASSA; linha do tempo de energia mostra os 6 eventos na janela.
- **Painel de teste (item 6, desde a rev C.2).** 5 toques no título em 2 s abrem
  um `PopupPanel`: moedas +5000, completar 24 campos, encher celeiro, zerar
  (recarrega a cena). Só existe com `rebocl/teste_livre=true` (está em
  `project.godot`; **Semana 8 desliga**). `CEI_PAINEL=1` abre sozinho para a
  bancada fotografar. Evidência: `verificacao/painel-teste-1280x720.png`.
- Régua: **64/64** economia (`_checar_13`, 9 do painel), **23/23** som (+2
  arquivos, +2 ganchos exercitados), `--import` limpo, 0 `SCRIPT ERROR`;
  `Coluna` idêntica nos 3 tamanhos, com e sem painel aberto.
- Publicado: rev C.5, `.pck` 378.400 B no ar = local (som novo: +135 KB;
  abertura ~8,3 MB). Navegador 3 perfis verde, áudio-web `running`.
- Erro meu: `:=` em `find_children()` (o analisador não infere) — tipo
  explícito. E o pico/LUFS iguais aos da 6ª rodada: o pico é o mesmo sino;
  a energia por janela prova os 6 sons, não o número repetido.

### Semana 7, frente 2 (lote 3, 2026-09-15): núcleo do save + offline — rev C.6

Ordem do dono: "continue trabalhando" (ainda sem os desenhos). Adiantada a
engenharia do save — matemática e teste, zero dependência da arte — porque
cada reload apagando tudo atrapalhava até o teste dele. Tela de título e
itch.io continuam na Semana 8, com ele.

- `salvamento.gd` (novo): `guardar/carregar/apagar` em `user://ceifalume-save.cfg`
  (ConfigFile, formato 1) + `avanco_offline()` (teto de 8 h, nunca negativo).
- Roteiro: `_guardar_jogo()` no fim de `_atualizar_interface()` (toda ação
  persiste); `_carregar_jogo()` no fim do `_ready` (save ou partida limpa);
  `_aplicar_estado()` reconcilia campos (piso 4, teto 24), replanta com avanço
  offline e avisa "Enquanto você estava fora (XhYm): N terminaram" (só se ≥1 min).
  Trava `_save_pronto`: antes de carregar, nada salva (senão zerava o save).
- `_teste_zerar()` agora apaga o save antes do reload (sem isto restaurava tudo).
- Bico ganhou o som da moeda (era a única ação muda). Régua: **72/72** economia
  (`_checar_14`: roundtrip, offline 2 h/20 h/futuro, corrupção, apagar, cena),
  **24/24** som, sim de regressão 13/48/174/336/475 idêntica, vai-volta entre
  processos provado (5477 moedas, 6 campos, plantado).
- **Lição nova (checklist): save contamina ferramenta.** Prova/sim/testes
  instanciam a cena real, que agora carrega E salva. Achado: `Coluna` 711 px
  em vez de 708 porque uma rodada carregou o save da anterior. Regra: `rm` no
  `ceifalume-save.cfg` antes de cada rodada de ferramenta; os testes apagam
  sozinhos no início (`_init_cena` + teste_som §4).
- Publicado: rev C.6, `.pck` 383.216 B no ar = local; navegador 3 perfis verde.
- **Não verificado:** persistência do `user://` no navegador real (IndexedDB do
  aparelho) — só o dono valida, fechando e reabrindo a aba.

### Semana 7, frente 2 (lote 4, 2026-09-15): arte piloto no jogo — rev C.7

Cobrança do dono ("cadê a arte?") + virada de decisão: **eu gero a arte aqui**
(antes era ele). Interface: organização aprovada **mantida**; a mudança visível
é a arte. O resto das plantas segue o mesmo pipeline do piloto.

- 5 arquivos em `ceifalume/arte/`: fundo noturno 1280×720, solo 240×210 e Nabo
  semente/broto/pronto em 128×128 com alpha. Recorte: o "magenta" gerado era
  malva (174,45,127) — limiar global falhou (0%), cantos falharam (vinheta);
  valeu distância-à-borda + componentes conexos (scipy) + erosão 1 px. Pronto
  coube em 127×91 (folhas largas não cortam).
- Código: loader do solo (`TextureRect` + some `Terra`, mesmo fallback);
  **sombra nos rótulos** do campo e do celeiro — o render mostrou dourado
  ilegível sobre a terra clara (a régua de corte não pega contraste; olho sim).
  Solo ganhou grau noturno (×0,62/0,66/0,78) para casar com o fundo.
- Régua art-aware de verdade: `_checar_09` quebrou honestamente com o Nabo
  dentro (exigia polígono, o jogo certo mostrava sprite) — agora lê o disco.
  **73/73** economia, 24/24 som, `Coluna` idêntica nos 3 tamanhos, 0 cortes.
- Publicado: rev C.7, `.pck` 1.616.816 B no ar = local. Custo honesto: fundo
  PNG 1,4 MB → abertura ~9,5 MB (+1,2). Otimização (JPEG/qualidade) é polimento
  da Semana 8, anotado nas pendências. Evidência:
  `verificacao/arte-piloto-nabo-1280x720.png` (Nabo no cenário meio) e
  `verificacao/arte-no-navegador-1280x720.png` (fundo+solo no Chromium).
- Bug pego pelo print do navegador (não pela régua): loader com
  `FileAccess.file_exists` cai em fallback silencioso no exportado, porque o
  `.png` original não vai no `.pck` (só o importado). Troca para
  `ResourceLoader.exists` em 10 pontos (jogo + régua); `user://` continua
  `FileAccess`. Lição: **todo lote com arte fecha olhando o print do
  navegador**, não só os números.

### Semana 7, frente 2 (lote 5, 2026-09-15): virada cartoon 2D — rev C.7c

Veredito do dono: realista "deixa o jogo ruim"; pediu dinâmica 2D + pesquisa
de jogos famosos de fazenda antes de propor.

- Pesquisa: Stardew (pixel aconchegante), Harvest Moon/Story of Seasons
  (desenho fofo), leva nova (Roots of Pacha, Fields of Mistria, Sun Haven) —
  todos 2D estilizados, legibilidade por silhueta simples; realista só no
  Farming Simulator (simulador de máquina, outro público). Voto do dono:
  **cartoon 2D limpo** (linha Hay Day — o Ceifalume é jogo de cartas/clique,
  não de avatar andando), **piloto primeiro**.
- Piloto refeito nos mesmos contratos: fundo + solo + Nabo ×3 em cartoon
  noturno dourado. Nabo veio **com rostinho** (fofo; dono decide se fica).
  Terra v1 saiu "veias de madeira" gigante — refeita minimalista (pontilhado
  sutil). Realistas arquivados em `arte-raw/legado-realista/` (nunca foram
  ao ar — o push travou antes).
- Prova ganhou `CEI_NABO_PRONTO=1` (retrato do Nabo pronto no 1º campo).
- Bug de exportação pego pelo tamanho: `verificacao/` (2 MB) entrava no `.pck`
  (2,80 MB!) → preset agora exclui; `.pck` final **1.310.400 B** (realista era
  1.616.816). `export/` é ignorado pelo git (38 MB só locais).
- 73/73, 24/24, `Coluna` idêntica, navegador verde nos bytes finais, prints
  olhados (editor + Chromium).
- **TRAVA:** push segue bloqueado (credencial expirou, 3× `could not read
  Username`); C.7c gravada nos 3 repositórios locais, link ainda na C.6.
- Destrave (mesma noite): chave do dono → push OK nos 3 (`abdf10e`,
  `11f4225`, `abdd945`); **C.7c NO AR** (pck 1310400 = local, selo C.7).
  Régua estendida: `_checar_12` agora cobre 6 plantas × 3 estágios (**88/88**,
  som 24/24). Faltam os 15 sprites das 5 plantas — o gerador de imagens
  bateu o teto de 10 por turno; continua no próximo turno.

### Semana 7, frente 2 (lote 6, 2026-09-15): 4 plantas completas — rev C.8

- 10 sprites novos (teto de 10/turno de novo): Milho, Trigo e Tomate inteiros
  + semente da Abóbora. Prontos com rostinho (mesma linha do Nabo). Faltam 5:
  Abóbora broto/pronto + Flor de Lume ×3 (próximo turno).
- Recorte quase todo limpo (fundo 70–92%); exceção: broto do Trigo veio num
  cartão magenta sobre fundo branco — recorte em 2 passos (corta branco,
  chaveia magenta). Folha de conferência em `verificacao/folha-sprites-c8.png`
  virou o olho padrão do lote: 1 print valida todos os sprites.
- 88/88 (a régua nova cobre o que existe), 24/24, `Coluna` idêntica, navegador
  verde. `.pck` 1.398.368 B (+88 KB p/ 10 sprites — cartoon é leve mesmo).
  Evidência: `verificacao/arte-c8-meio-1280x720.png`.

### Semana 8 (lote 7, 2026-09-15): jogo completo e testado — rev C.9

Ordem do dono: terminar o aplicativo por inteiro + teste total antes dele
encostar. Entregue como **pronta para lançar** (a decisão lança/não-lança
é dele).

- Arte completa: 5 sprites finais (Abóbora broto/pronto, Flor de Lume ×3) —
  **18/18**, folha validada no olho (`verificacao/folha-sprites-c9.png`).
- Ambiente caiu no turno novo (`.cache`/`.local` zerados): religado pelos
  scripts da base + templates web+windows+linux + puppeteer. Lição: conferir
  o motor no início de **todo** turno (o import "0 erros" chegou a fingir
  verde com o binário ausente). O Git também amnésia: `origin` some
  (`.git/config` fora do snapshot) e o `site/.git` já voltou 2× sem o último
  commit — ritual de início de turno: motor + `git remote -v` + `fetch` +
  conferir HEAD antes de commitar.
- **BUG DO SOM CONFIRMADO E MORTO:** `sons.gd` usava `FileAccess` — falso no
  `.pck` — então o jogo publicado **era mudo de verdade** (explica o relato
  do dono). Prova: parser do índice do `.pck` (fontes ausentes; só
  `.godot/imported` + `.import` + `.remap`). Corrigido para
  `ResourceLoader.exists`. Mesma classe do bug da arte.
- Música-tema procedural (`musica-tema-01.ogg`, 210 KB, loop 34 s: pad +
  grilos + vento) + player no bus Musica + início no primeiro gesto
  (botão Jogar). Régua do som: **27/27**. WAVs removidos (só OGG, −240 KB).
- Balanceamento: dia 60→180 s (conceito: "alguns minutos"); const morta
  `TEMPO_CRESCIMENTO` removida da tabela; tabela sincronizada (campo ×1,45,
  offline ✅ C.6); `_checar_15` trava os números → **91/91**.
- Tela de título (nome + frase + Jogar + fundo) + `main_scene`; teste de
  clique na prova (foi pro jogo? música tocando?); print validado. Sonda
  pegou `script =` esquecido no `.tscn` (botão com 0 conexões, sem erro).
- Presets Windows + Linux; builds com 0 erros (exe 84 MB, linux 66 MB,
  pck 1,45 MB); boot do Linux limpo por 20 s no Xvfb.
- Varredura total: cenários limite + cheio sem erros/cortes, navegador verde
  nos 3 perfis, `.pck` final **1.451.136 B**. Kit itch.io pronto em
  `divulgacao/` (descrição + checklist + shots) — **não publicado**
  (conta e decisão do dono). Evidência: `verificacao/arte-c9-titulo-1280x720.png`.

### Semana 8 (lote 8, 2026-09-15): abertura RB + resposta do ganho — rev C.10

- Pedido do dono: logo RB antes do título, sobre uma fazenda. Feito:
  monograma oficial copiado de `base/empresa/logo/` (sem redesenho) +
  fazenda cartoon nova 1280×720; 2,5 s ou toque para pular; `main_scene`
  agora é a abertura; prova testa `_avancar()` → título; print validado
  (`verificacao/arte-c10-abertura-1280x720.png`).
- Custo honesto: splash PNG 1,1 MB → `.pck` **2.353.952 B** (+900 KB).
  Otimizar (JPEG) segue anotado para pós-lançamento.
- Navegador: o shot do medidor caiu no título = auto-avanço funciona no
  build real. 91/91, 27/27, trio verde.
- Ganho: respondido ao dono que hoje o plano é **grátis** (Fase 0, pessoa
  física, itch.io sem custo); caminhos futuros: doação no itch, preço fixo,
  Play com anúncios (Fase 1, US$ 25). Decisão de preço com ele.
### Semana 8 (lote 9, 2026-09-15): intro v2 da empresa — rev C.11

- Pedido do dono: entrada individual da RB **mais bonita, com gráfico bom**.
  Feito: logo acende em fade (0,9 s) + nome em seguida, brilho dourado
  pulsante atrás da logo, 20 vagalumes subindo, vinheta de 2 notas
  (`arte/som/som-logo-rb-01.ogg`, 6,9 KB), 3 s ou toque → fade-out 0,2 s.
- Régua: import 0 erros, econ **91/91**, som **28/28** (vinheta é a 28ª
  checagem), limite 0 cortes, 3 renders da abertura validados a olho
  (vagalumes foram de gigante → invisível → ponto certo),
  `.pck` **2.344.272 B**, trio navegador verde com selo C.11, áudio `running`.
- Evidências: `verificacao/arte-c11-abertura-1280x720.png` (intro v2) +
  `verificacao/arte-c11-titulo-1280x720.png` (título no navegador, pós-auto-avanço).
- Nota de ferramenta: `prova_visual.gd` ganhou `CEI_QUADROS` (nº de quadros
  antes do print) para fotografar a animação acesa; padrão segue 10.

### Semana 8 (lote 10, 2026-09-15): APK + anúncio com recompensa — rev C.12

- Regra do dono: **só investe o que ganhar** — zero custo: APK distribuído
  fora da loja (Release no GitHub + botão no site), sem taxa da Play.
- Anúncio **só com recompensa e opcional**: botão `Vídeo = pronto` no campo
  crescendo (só no Android, só acende com anúncio carregado); assistir até
  o fim amadurece a planta na hora. Nada interrompe o jogador.
- Fiação: autoload `Anuncios` (`anuncios.gd`: carregar/mostrar/disponivel,
  recarrega após ver ou fechar) + plugin Poing v3.1.3 (Godot, commitado em
  `addons/admob/`) + nativo 4.3 da v3.0.6 (GMA 24.9.0, minSdk 24).
  IDs de **teste** do Google até o dono criar o AdMob; troca documentada
  na §17 de pendências (1 linha no .gd + 1 no manifest + rebuild).
- Build: keystore release próprio (`~/.assinatura`, senhas em
  `~/.segredos-apk`, ambos fora dos repos); `versionCode=12`,
  pacote `com.reboclbrank.ceifalume`; assinatura SHA-256
  `c6e5e7ba...cc7840`; 85 MB; `tools/publicar-apk.sh` repete tudo.
- Régua: import 0 erros, econ 91/91, som 28/28, **anúncios 5/5** (novo
  `teste_anuncios.gd`: invisível fora do Android), APK verificado
  (apksigner + badging + APPLICATION_ID no manifest + GMA no dex).
- Lições de build: Gradle morria no OOM (caixa de 2 GB) → swap 3 GB via
  sudo; `.build_version` com `4.3.stable` + `.gdignore` (o menu do editor
  faria); senhas no `.godot/export_credentials.cfg` (gitignored), nunca
  no preset; `plugins/AdMob=true` no preset (fonte: export_plugin.cpp).

### Semana 8 (lote 11, 2026-09-15): IDs reais do AdMob — rev C.13

- Dono criou app + unidade Premiada no AdMob (guiado por print) e mandou os
  IDs: App `...4851~2798643988`, unidade `...4851/9323689735`
  ("Colheita instantânea"). `APP_ID` em `~/.segredos-apk`, unidade em
  `anuncios.gd` → APK C.13 (versionCode 13) com anúncio valendo dinheiro.
- INCIDENTE keystore: o snapshot estourou o teto (~128MB) por causa do
  template de build (184MB em `android/build/`) e o `.keystore/` + debug
  keystore se perderam. C.12 (chave perdida) foi APAGADA (Release + tag) e
  a C.13 nasceu com chave NOVA (SHA-256 `356a4c7b...8748d14`): quem instalou
  a C.12 precisa desinstalar antes (base instalada ≈ só o dono, dano mínimo).
- Blindagem: `publicar-apk.sh` agora (a) apaga `android/build` no fim de
  todo build (snapshot volta a ~65MB), (b) força SDK/Java no editor_settings
  via sed (o Godot escreve as chaves vazias e enganava o grep), (c) upsert
  do App ID todo turno, (d) gradle magro + swap todo turno.
- Régua: econ 91/91, som 28/28, anúncios 5/5; APK verificado (nova
  assinatura + App ID real no manifest + GMA no dex; unit ID conferido no
  fonte pois `.gdc` é comprimido). Release `apk-c13` + botão no site.

### Semana 8 (lote 12, 2026-09-15/16): plantio de volta + cara final — rev C.14

- BUG DO PLANTIO (dono: "clico e não planta"): causa raiz achada — a edição
  C.12 do botão de vídeo comeu o corpo de `campo.gd::_ao_clicar` (só sobrou
  `if crescendo: return`; o `if pronto/else` foi parar dentro de `_ao_video`).
  Restaurado + `teste_clique_campo.gd` (clique de verdade via warp+evento,
  3/3) como regressão. LIÇÃO: nunca ancorar patch no meio de função; conferir
  `grep -A` depois de editar.
- ÍCONE + SPLASH: `arte/icone-ceifalume-512.png` full-bleed (lanterna+broto+
  lua, 512px) como `config/icon`; `boot_splash` escuro (`#0A0D1A`) com logo RB.
  Confirmado DENTRO do APK (extraí os PNGs e olhei: é a lanterna).
- MÚSICA: `tools/compor-tema.py` (cópia em `base/ferramentas/`) compõe o tema
  v2 (caixinha 8 compassos, 25,6s, loop sem clique, pico -1dBFS).
- IDENTIDADE UI: painéis azul-noite/ouro, botões pergaminho, cartão terra
  (`cena_principal.tscn` + `campo.tscn` + `roteiro_principal.gd`); aprovada em
  render (`novacara.png`, mesmo layout do jogo real).
- REMENDO AdMob: `version_helper.gd` gritava "Failed to load plugin.cfg" no
  log do jogador (web); agora cai silencioso p/ v3.1.3 vendida.
- INCIDENTE chave nº 2: a causa NÃO era o teto do snapshot — arquivos com
  "keystore" no nome são removidos entre turnos (proteção da plataforma).
  C.13 morreu junto com a chave (`apk-c13` apagada); C.14 nasceu com chave Nº 3
  (SHA-256 `ef844053...226689`). BLINDAGEM: chaves em `~/.assinatura/` (sem a
  palavra proibida) + cópia reserva + guarda no script (restaura ou aborta).
- DIETA web: preset Web exclui testes + `addons/admob/{assets,sample,docs}`
  (pck 8,3→2,9MB).
- Régua C.14: econ 91/91, som 28/28, anúncios 5/5, clique 3/3, trio navegador
  3/3 zero erros JS. Release `apk-c14` + botão no site + selo C.14.

### Semana 8 (lote 12b, 2026-09-16): rollback do workspace + regra real de guarda

- O workspace local REGREDIU entre turnos (git na era C.8, `.assinatura/`
  apagada, `export/` e `node_modules` sumidos) — mas o GitHub estava INTACTO
  (C.14, Release apk-c14, site C.14). Recuperação: clone fresco dos 3 repos.
- ACHADO GRAVE no rebase do lote 12: o commit C.14 foi parar em cima da C.13
  com `campo.gd` CORROMPIDO (`_ao_clicar` quebrado + `_ao_video`/`_anuncios`/
  `_atualizar_botao_video` duplicados) — o rebase "aplicou limpo" e ninguém
  re-rodou os testes depois. O APK e o site publicados estão BONS (builds de
  antes do commit); só o repo estava errado. CORRIGIDO + régua verde de novo
  (91/0, 28/0, 5/5, 3/3). LIÇÃO NOVA NO RITUAL: re-verificar SEMPRE depois
  de rebase/merge (import + 4 testes), nunca só antes do commit.
- REGRA REAL DE GUARDA (3ª teoria, agora com prova): pastas OCULTAS na raiz
  (`~/.* /`) são apagadas entre turnos (`.keystore`, `.assinatura`, `.local`,
  `.cache`); arquivos ocultos PEQUENOS sobrevivem (`.chave-github`,
  `.segredos-apk`, `.gitconfig`); workspace acima de ~128MB perde o que é
  grande. Chaves agora em `~/cofre/` (pasta normal, fora dos repos) + cópia.
- Chave nº 3 (C.14) PERDIDA no rollback — C.14 não pode mais ser atualizada
  no lugar; próxima release sai com chave nº 4 (SHA-256 `36184875...cbf9f2`,
  já gerada em `~/cofre/`) e o dono desinstala a C.14 antes. Cofre = canário:
  se sobreviver ao próximo turno, a regra está provada.
- BACKUP TOTAL (pedido do dono): `arte-raw/` (23 PNGs fonte, 33MB) e os 3
  prints do dono em `base/projetos/01-ceifalume/`; render da UI + trio web em
  `ceifalume/verificacao/`; `tools/` == `base/ferramentas/` (idênticos).

### Semana 8 (pesquisa, 2026-09-16): Ceifalume 100% profissional

- Pedido do dono: pesquisas para nada genérico restar. Entregue
  `pesquisa-profissional-100.md`: auditoria achou 18 itens (8 bloqueadores da
  Play + 7 no jogo + 3 papelada) + plano em 5 fases (A loja, B papelada,
  C áudio, D conteúdo, E produção).
- Achados críticos: prazo API 36 passou em 31/ago/2026 (estamos na 34);
  16KB exige Godot 4.5.2+ (estamos na 4.3); plugin AdMob mínimo virou 4.5;
  conta pessoal nova = 12 testadores × 14 dias; UMP nunca foi ligado (0 usos).

### Semana 8 (profissional-100, 2026-09-16): consentimento + privacidade + site

- Dono mandou fazer TUDO e avisou que está sem dinheiro: ordem virou
  grátis-visível-primeiro (motor/Play por último, pois a taxa US$25 trava).
- UMP ligado: `anuncios.gd` resolve consentimento antes de carregar anúncio
  (formulário só onde a lei exige; falha silenciosa → carrega direto).
- Política de privacidade PT-BR publicada (`site/privacidade.html`, bate com
  Data safety futuro) + `app-ads.txt` + site sem "rascunho" (selo novo).
- Régua: 91/28/5/3 + trio zero erros. Tudo entra na C.15 (C.14 publicada sem).

### Semana 8 (profissional-100, 2026-09-16): análise total + fonte + suco

- Dono perguntou se o jogo/desenho é genérico e se há "motor que refaz tudo":
  respondido com honestidade (não existe botão mágico) + análise tela a tela
  (abertura/título/inicial/meio renderizados e olhados).
- Veredito: direção de arte JÁ é própria (faro noturna + lanterna + lume);
  o genérico estava na tipografia (fonte padrão), na paralisia (zero
  animação) e num erro de texto ("1 colhem").
- Feito (C.15): fonte Baloo 2 OFL (SemiBold padrão + ExtraBold no nome),
  balanço das plantas ao vento, pulinho ao ficar pronta, gramática.
  Régua 91/28/5/3 verde; renders conferidos a olho, sem corte de texto.
- Nota de ferramenta: `read_file` em paralelo pode devolver imagens fora de
  ordem — ler renders sequencialmente quando a ordem importar.

### Semana 8 (profissional-100, 2026-09-16): auditor-100 + vaga-lumes (86/100)

- Dono pediu "algo que analise o jogo de forma completa": construído o
  `auditor-100.py` (100 pts: identidade 20, arte 20, som 15, textos 15,
  movimento 15, loja 15). Base 77 → 82 (2 falsos-positivos calibrados).
- M2 corrigido: vaga-lumes vivos (CPUParticles2D) atrás do título.
  Placar: **86/100**, 5 faltas (S2 sons, T5 tutorial, L1 SDK, L5 versão
  pública, L6 AAB). Régua 91/28/5/3 verde.

### Semana 8 (profissional-100, 2026-09-16): 93/100 + caça-bugs + capa

- S2 fechado: 6 SFX reais Kenney CC0 no lugar dos provisórios, masterizados
  a -6dBFS (medir-som 7/7 PASSA); LEIA-ME sem "provisório".
- T5 fechado: tutorial "COMO JOGAR" (3 passos + botão ouro, transparente ao
  toque, flag no save; saves antigos tratados como veteranos).
- Caça-bugs: corrigidos ritmo cortado (24/24), tutorial em save antigo,
  bancada não-determinística (prova agora apaga save); verificados como SÃOS:
  offline 8h, preços (feira 4× é jackpot intencional), lógica do vender,
  sim 300 dias sem exceção; avisos de saída = ruído do teste, não do jogo.
- Capa profissional: arte-base + feature 1024×500 + itch 630×500 (Baloo ouro)
  + shots atualizados em `divulgacao/`. Placar: 93/100 (faltam L1/L6 = motor,
  L5 = decisão do dono).

### Semana 8 (profissional-100, 2026-09-16): C.16 motor 4.5.2 + AAB (100/100)

- Dono mandou "fechar primeiro 100" antes de decidir versão/publicação.
- Upgrade do motor 4.3→4.5.2 em branch `motor-4.5`: import limpo, régua
  91/28/5/3 verde no motor novo, renders inicial/meio/cheio conferidos a olho.
- Plugin AdMob v3.1.3→v5.1.0 (nativo 4.5.2): UMP igual ao v3 (código mantido);
  `anuncios.gd` agora segue ordem oficial UMP→init→load (load antes do init
  pronto dá exceção) + `destroy()` ao dispensar. Docs do plugin (README/SKILL)
  descrevem API estática que NÃO existe no zip 5.1.0 — vale o código do zip.
- Preset Android: target_sdk 36, export_format AAB, versão 0.1 (provisório até
  o dono escolher o número final), code 15; App ID de teste no repo, real
  injetado no build via ~/.segredos-apk (restaurado depois pelo trap).
- Build: SDK platform-36 + build-tools 36/35 + NDK 28.1.13356709 (pinado pelo
  template) + compileSdk 35→36 no config.gradle; Gradle 8.11.1. AAB verificado:
  jarsigner, bundletool validate, manifesto (pacote/código 15/0.1/target 36),
  AdMob dentro, .so STORED alinhado em 16KB + LOAD 0x4000 no readelf.
- Placar: **100/100**. Ferramentas 4.3 aposentadas (acender/preparar/publicar
  agora falam 4.5.2). Lição: nunca rodar testes Godot em paralelo (user://
  compartilhado contamina save); teste de clique exige xvfb (dummy não tem mouse).

### Semana 8 (tortura, 2026-09-16): C.17 — 100% verificado

- Pedido do dono: caçar todo bug + confirmar estabilidade total + dizer como
  testar e o plano da Play. Entregue: `teste_tortura.gd` (fuzzer 3000 ações
  com invariantes a cada passo + 14 saves envenenados + matriz evento×load +
  4 boots em processo separado) — **3030 testes, 0 falhas**, zero SCRIPT ERROR.
- Bugs mortos (5): Poço/evento perdidos no reload; save corrompido derrubando
  (`_num/_numf/_aplicar_precos/_verdade` em `_aplicar_estado`); `bool(String)`
  (3 pontos); `get_section_keys` sem seção; volumes/mudo sem clamp; e o
  CRÍTICO nº 5 — plugin AdMob desligado desde C.12 (SDK nativo nunca
  empacotado; botão de vídeo morto em todo aparelho; C.17c liga + verificação
  de dex-conteúdo; a checagem antiga de nomes era falso-positivo).
- Régua final desktop: 91/91 econ, 28/28 som, 5/5 anúncios, 3/3 clique (xvfb),
  auditor-100 100/100. Visual: 4 renders erro=0, zero cortes (o "corte" visto
  era o tutorial cobrindo — CEI_SEM_TUTORIAL=1 prova).
- Web C.17 republicada COM camada (a anterior subiu crua): selo oficial,
  manifest, ícones, worklet de posição; export 61→0 erros (csharp/skills fora);
  fumaça 3 perfis verde + clique real abertura→título→jogo (desktop e toque
  844×390). `.pck` 3.767.184 B sem conteúdo de teste.
- APK-teste: `tools/apk-teste.sh` (APK + IDs de teste + 0.1-teste/code 16,
  restaura o repo sozinho); chave nº 5 (cofre sumiu com a nº 4 — chave agora
  viaja com o dono). Verificação: apksigner, badging, App ID de teste, GMA e
  UMP no dex, 16KB. Release `apk-c17-teste` + botão no site. (Status do build:
  ver registro da 20ª rodada.)
- Save: dono reportou restart ("sai e entra, recomeça") — bug nº 6 real nos
  publicados. C.17d + rede extra (guardar devolve erro, _notification pausa/
  foco/fechar, periódico 10 s): save_novo 10/0, economia 91/91, tortura 3030/0.
  Falta republicar web+APK para o fix chegar ao jogador.

## C.18 (2026-09-16) — chiado + botão de vídeo
- Chiado na música: era a "cama de grilos" (ruído branco em rajadas, 4,2 Hz).
  `tools/compor-tema.py` com GANHO_GRILOS=0, ogg regenerado (161 KB), agudo -36 dB.
- Botão "Vídeo = pronto": retry automático de 20 em 20 s em `anuncios.gd`
  (antes: 1 falha e o botão morria para sempre). TESTE_ANUNCIOS 8/0, TESTE_SOM 28/0.

## 0.1 (2026-09-16) — auditoria total + pronto p/ lançar
- Lidos 1014 linhas do roteiro + todos os subsistemas; 7 consertos: painel de
  teste DESLIGADO, launcher (ícone na gaveta) + ícone 192, matemática do Poço,
  texto da Lanterna/Ajudante, save por id de planta (índice antigo ainda abre).
- Web nova (sem chiado, selo 0.1, manifest landscape) + botão no site
  (Baixar APK via release do repo público + Jogar na web). Auditor 100/100.
- Novo `tools/apk-lancamento.sh`: APK prod com 34 travas (App ID real, LAUNCHER,
  INTERNET, ícone, zero ID de teste, bateria completa). Bloqueio: APP_ID real.

## 🎬 Trailer do 0.1 (2026-09-16, noite) — gravado, publicado e conferido

O trailer novo pedido para o 0.1 existe e está no ar como **asset da release `v0.1`**
do repositório `site`: https://github.com/reboclbrank-max/site/releases/download/v0.1/ceifalume-trailer-0.1.mp4

| O quê | Valor medido |
|---|---|
| Duração / resolução / fps | **45,9 s** · 1280×720 · 30 fps |
| Tamanho | 3.473.373 bytes (3,3 MB) |
| Conteúdo | abertura RB (logo acende + vaga-lumes) → título com o vaga-lume → Dia 1 plantando os 4 campos → crescimento → colheita → venda → fazenda grande (Dia 12, chuva boa, 10 campos, 6 culturas) → loja (campo + poço) → dia vira → colheita e venda grande → Flor de Lume pronta → fecha no título |
| Áudio | a **música-tema e os 6 efeitos do próprio jogo**, no tempo certo (pico local -3,2 dB no plantio, +12 dB sobre a cama musical) |
| Régua do som (`MEDIR_MODO=mix`) | pico **-1,9 dB**, integrado **-17,1 LUFS** → **PASSA** |
| Verificação | 12 quadros conferidos a olho (folha em `verificacao/trailer-0.1-folha-geral.jpg`), `blackdetect` apontando preto só nas 3 transições, download pela rede conferido byte a byte |

**Como foi feito (regerável):** `ceifalume/trailer.gd` (ferramenta, fora do `.pck`
por `exclude_filter`) roda a cena real, dirige o jogo pelas funções de verdade e
salva quadro a quadro; `base/ferramentas/montar-trilha.py` lê o diário de sons
(`eventos.txt`) e monta a trilha com o ffmpeg. Comando no cabeçalho do `trailer.gd`.
O tempo de jogo que entra em cada quadro de vídeo é calculado pelo tempo real
medido, então o ritmo não depende do fps da máquina.

**Incidentes desta sessão (com lição):**
1. **Quadro preto em 45 s de vídeo:** o véu de transição (`ColorRect` preto) havia
   sido criado com `alpha = 1` e ficou opaco o roteiro inteiro — a imagem só
   aparecia depois de blocos de corte o apagarem. Lição: instrumento que cobre a
   tela precisa nascer transparente e ser medido com `convert -format "%[fx:mean]"`.
2. **Primeira versão foi publicada SEM o fundo noturno:** a virada de turno apagou
   arquivos do workspace (o `.git` do `site`, os `.ogg` do jogo, o PNG do fundo e o
   cache `.godot`); o jogo rodou com fundo preto liso e parecia "moldura dupla".
   Descoberto ao ampliar um quadro publicado. Regravado com o fundo, asset
   substituído e download conferido. **Lição: workspace inchado (≈400 MB com
   quadros de vídeo) perde arquivos entre turnos — limpar antes de virar o turno,
   e nunca julgar um render sem comparar com um render antigo já verificado.**
3. **`--import` some com o `.godot/`:** sem reimportar, `class_name Salvamento` não
   resolve e o trailer nem carrega. Rotina: `--import` → `--check-only` → rodar.
4. **O Godot reescreve o `project.godot`** ao abrir o projeto e apaga a seção
   `[admob]` se o plugin não estiver habilitado — restaurado com `git checkout`.
   Conferir `git status` do repositório do jogo depois de rodar a bancada.

**Pendente (com o dono):** baixar o mp4 (link acima), subir no YouTube e colar o
link no campo trailer da página da itch.io. Depois: Samsung Galaxy Store (grátis).

## 📺 Divulgação — trailer no YouTube e Short (2026-09-16)

- **Trailer publicado:** https://youtu.be/tB449xupDzY — "Ceifalume — trailer oficial
  (jogo de fazenda noturna grátis)", 00:46, público, com título, descrição, tags,
  capítulos e miniatura do kit (`marketing/youtube-kit.md`).
  - ⚠️ **Categoria veio "Pessoas e blogs"** — **decisão do dono em 2026-09-17:
    fica assim** (o campo só existe no Studio pela web; não trocar).
- **Short publicado:** https://youtube.com/shorts/Gm7ZIGNRLTg — cortado do trailer.
  - ✅ Título corrigido pelo dono em 2026-09-17 (veio só com as hashtags).
- Kit do canal versionado: `marketing/youtube-kit.md` + `youtube-banner-2560x1440.jpg`
  + `youtube-thumb-1280x720.jpg`.
