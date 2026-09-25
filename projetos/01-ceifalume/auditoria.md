# Auditoria do Ceifalume — 2026-09-15 (rascunho "rev B")

O que foi olhado, o que estava quebrado de verdade, o que foi consertado e —
importante — **o que esta auditoria não conseguiu verificar**. Feita a pedido do
dono ("faça uma auditoria do que tá funcionando e o que pode estar dando erro,
corrija e me traga"), logo depois do veredito de que o jogo "está muito bom".

Estado de referência: `ceifalume` em `9baf0d1` (antes) → `1247845` (depois).
Build publicado: `site` em `b2f6b3a`.

---

## Como a auditoria foi feita (reproduzível)

1. **Leitura integral dos quatro arquivos que compõem o jogo** —
   `roteiro_principal.gd` (475 linhas antes), `campo.gd` (110),
   `cena_principal.tscn` (229), `campo.tscn` (132) — mais
   `export_presets.cfg` e `project.godot`. Nada foi julgado de memória: cada
   afirmação abaixo tem arquivo e linha.
2. **Teste de bancada** criado nesta sessão: `teste_economia.gd` na raiz do
   repositório. Ele instancia a cena real do jogo e exercita as regras — sem
   tela, sem mouse. 48 checagens. Rodar:

   ```bash
   ~/.cache/ferramentas/godot --headless --path . --script res://teste_economia.gd
   ```

   Resultado hoje: **48 checagens, 0 falhas, 0 erros de script no output**.
   Saída completa desta rodada: `/tmp/saida-teste.txt` (efêmero — o que vale é
   o teste, que está no repositório).
3. **Export real** (`--export-release "Web"`) para provar que o que passou no
   teste é o que vai no arquivo que o navegador baixa, e conferência byte a byte
   entre o `index.pck` do build e o publicado.

O teste de bancada é a peça que faltava: as Semanas 1–6 foram todas conferidas
"no olho", abrindo o jogo. Ele fica no repositório e roda em qualquer sessão, o
que torna regressão visível sem depender de alguém jogar.

---

## O que estava funcionando bem (verificado, não mexido)

| Área | Evidência da checagem |
|---|---|
| Custos da loja (curvas ×1,7 Poço, ×1,8 campo, ×1,7 Celeiro…) | `5º campo custa 50`, `6º campo custa 90 (x1.8)`, `celeiro nível 1 custa 30`, `poço nível 1 custa 40` — ok |
| Plantar cobra o preço da semente e não cobra duas vezes | `plantar nabo custa 5`, `sem moedas não cobra` — ok |
| Ritmo do Poço chega aos campos, inclusive aos novos | `campo novo já herda o poço` (fator 1,1) — ok |
| Ciclo plantar → crescer → pronto → colher → livre | `tempo cheio deixa pronto`, `campo volta a ficar livre` — ok |
| Venda paga exatamente o preço do dia e esvazia o celeiro | `venda paga o preço do dia`, `celeiro esvazia na venda` — ok |
| Ajudante colhe um campo por batida, sem passar do número contratado | `dois ajudantes colhem dois campos` — ok |
| Faixa de preço do mercado (50%–200% do preço base; dobra na Feira) | 120 dias simulados para cada uma das 6 plantações, todos dentro da faixa |
| Economia não quebra em uso longo e aleatório | simulação de 400 turnos misturando plantio, colheita, venda, compras: moedas nunca negativas, celeiro nunca acima da capacidade, preço nunca zero |
| Sem erro de script oculto durante a partida | o output do headless não tem nenhuma linha `SCRIPT ERROR` (tinha — ver defeito 9) |

---

## Defeitos encontrados — todos corrigidos nesta sessão

Numeração = a ordem em que apareceram na leitura. O teste entre backticks é o
nome da checagem em `teste_economia.gd` que prova a correção.

**1. O Poço era o único botão da loja que não dizia o que faz.**
`roteiro_principal.gd:496-500` (antes): a etiqueta era
`"Cavar Poço — %d moedas (nível %d)"`, enquanto Celeiro dizia `guarda %d`,
Lanterna `+%d por colheita`, Ajudante `%d colhem sozinhos`, Composteira
`%d%% de colheita dupla`. Quem quisesse entender o Poço tinha que abrir o
código. → Agora a etiqueta mostra o efeito e o resultado: `Cavar Poço — 40
moedas / crescimento +10% (iria a ×1,1)`. *`etiqueta do poço diz preço e efeito`*

**2. O campo mentia "pronto" antes da hora.**
`campo.gd:66-69` (antes): `_atualizar_visual` mostrava o desenho de planta
pronta a partir de 75% do tempo e o rótulo ia a `"planta pronta"` só em 100%.
Numa Flor de Lume de 2 horas, era **meia hora** de desenho dizendo que tinha
colheita onde ainda não havia. → O desenho de pronta só aparece quando ela está
pronta (`semente < 40%`, `broto ≥ 40%`), e o rótulo passou a contar o tempo:
`"Nabo crescendo — 12s"`. *`planta pronta some do desenho antes da hora`,
`rótulo mostra quanto falta`, `ao terminar, o desenho vira 'pronto'`*

**3. Celeiro cheio travava o jogo — a Carroça não salvava.**
Este era o mais grave. `roteiro_principal.gd:214-216` (antes): a verificação de
capacidade devolvia `false` **antes** de qualquer venda, e a Carroça só era
acionada depois de a colheita entrar no celeiro. Com o celeiro cheio, a colheita
era rejeitada → a carroça nunca vendia → o campo ficava pronto para sempre →
com celeiro 10/10 e sem botão de venda manual aparente, a partida empacava.
→ A carroça agora esvazia o celeiro *antes* de rejeitar a colheita; se não há
carroça, a colheita continua bloqueada (isso é regra do jogo, não defeito) e o
aviso diz o que fazer. *`carroça destrava a colheita com celeiro cheio`,
`sem carroça, celeiro cheio bloqueia`*

**4. A Seca não doía.**
`roteiro_principal.gd:209` (antes): `quantidade = maxi(1, quantidade / 2)` com
`quantidade` inteira — com Lanterna no nível 0, rendimento 1 ÷ 2 = 0 → virava 1
de novo. A Seca também não tocava o crescimento: só reduzia rendimento, e só a
partir da Lanterna 1. → Seca agora reduz o **crescimento** para ×0,7 (o campo
anda mais devagar de fato, via `fator_extra`) e o rendimento usa arredondamento
(`4 → 2`, `3 → 2`). *`seca reduz rendimento par (4 → 2)`,
`fator do evento no campo é 0.7 na seca`*

**5. Aviso novo era apagado pelo aviso antigo.**
`_avisar` fazia `rotulo_aviso.text = texto` e, três segundos depois,
`rotulo_aviso.text = ""` — sem verificar se aquele texto ainda era o seu. Dois
avisos em sequência: o primeiro limpava a tela e sumia o segundo. E erro tinha a
mesma cor de informação. → Cada aviso ganha um token (`_aviso_token`), só o
último pode limpar, tempo subiu para 4 s, e "aviso" de problema sai em cor
própria. *coberto indiretamente por `aviso apareceu no rótulo`*

**6. O jogo começava com 1 campo, e o conceito manda 4.**
`roteiro_principal.gd:129` (antes): uma única chamada `_criar_campo()`. Com 1
campo, os primeiros minutos eram um campo só e um tédio. Mas só colocar 4
iniciais encarecia tudo: `custo_campo()` era
`50 × 1,8^(campos.size()-1)`, que com 4 campos livres cobraria **292** no
primeiro campo comprado. → Constante nova `CAMPOS_INICIAIS := 4`, os 4 campos
são criados no `_ready`, e o expoente passou a contar só o que o jogador
comprou (`maxi(0, size - 4)`). Primeiro campo comprado: 50 moedas de novo.
*`começa com 4 campos`, `5º campo custa 50`, `6º campo custa 90 (x1.8)`*

**7. Letra e alvos de toque pequenos demais (a queixa do dono).**
Fontes nos `.tscn` iam de 12 a 21 px e os botões da loja tinham altura mínima de
34 px — menos que os 44–48 px recomendados para dedo. → Fontes 12→17, 13→17,
14→18, 16→19, 18→20, 19→21, 21→24; botões da loja com altura 48 px; rótulo do
ritmo novo no painel do mercado; `autowrap_mode` nos textos longos (antes,
qualquer linha mais larga que os 360 px do painel era cortada sem aviso — vale
para as etiquetas novas da loja, que viraram duas linhas). Um teste vigia isso:
*`nenhuma etiqueta da loja passa de 34 caracteres por linha`*.

**8. O jogador não sabia por que uma compra foi recusada.**
Os seis botões da loja terminavam em `if moedas < custo: return` — toque, nada
acontece, nenhuma palavra. → Função `_pagar(custo, nome)`: quando falta
dinheiro, o aviso diz quanto falta e quanto há ("Faltam 12 moedas para cavar o
Poço (tem 26)"). Só o plantio avisava; a loja não avisava nada.

**9. Erro de script silencioso na colheita (apareceu no teste, não na mão).**
`_registrar_colheita` lia `campo.plantacao.nome` sem checar se havia plantação.
Pela interface isso não aparecia (o clique só emite `colhido` quando o campo está
pronto), mas qualquer caminho que chamasse a colheita em campo vazio derrubava o
script com `Invalid access to property or key 'nome'` — e a partida seguinte ao
salvamento da Semana 8 seria exatamente esse caminho. → Guarda no topo da
função: plantação vazia devolve `false` e nada estoura. O teste de bancada
registrava 25 desses erros antes da correção; agora: zero.

**10. `project.godot` tinha duas seções `[rendering]`.**
Pendência 6 da `pendencias.md` — o bloco `import_etc2_astc` foi anexado como
segunda seção em vez de entrar na primeira. Funcionava, mas o editor reescreve
o arquivo e uma das seções podia sumir na próxima sessão de alguém. → Unificadas
em `[rendering]` só com as três chaves; `--import` headless limpo depois.

**11. Sobras de development que enganavam.**
`campo.gd:51` (antes) usava `plantacao.get("tempo", 12.0)` — 12 s era o valor do
tempo de teste da Semana 2; se uma definição viesse sem `tempo`, o campo
crescia numa velocidade de teste em vez de falhar alto. → Fallback agora é o
tempo do Nabo (30 s), que é o campo de entrada do jogo, e o teste cobre o
caminho.

---

## O que eu havia feito errado na sessão passada e foi desfeito

**`html/canvas_resize_policy`**: eu tinha trocado de 2 para 1 no
`export_presets.cfg` e escrito na documentação que isso deixava o canvas
adaptativo ("política 1: o canvas acompanha o tamanho da janela"). Estava
errado, e no layout deste jogo a mudança **piorava** o celular: policy 1 faz o
tamanho interno do canvas seguir a janela, mas o layout do Ceifalume é de
tamanho fixo (painel esquerdo de 360 px dentro de um `CenterContainer`, grade
de campos com `custom_minimum_size` de 780 px) — sem reflow, nada "acompanha";
o que acontece é recorte nas bordas. → Voltou para **2** (canvas do tamanho do
projeto) e o encaixe passou a ser resolvido onde é responsabilidade de página:
a moldura `#rd-arena` com proporção travada em 16:9, que **encolhe o jogo
inteiro até caber** em vez de cortar, mais o botão de zoom (Ajustar / 150% /
200%) lembrando a escolha entre sessões. Nenhum pixel do jogo fica
inacessível.

**Publicar a página sem os arquivos do motor**: `web/gerar-pagina.py` copiou só
`index.html` + ícones + manifest. O `.pck` ficou o do build anterior — o site
teria servido interface nova com jogo velho, e eu não teria como perceber. → O
publicador agora copia os sete arquivos do motor e compara o tamanho de cada um
depois de copiar; divergiu, ele aborta.

---

## O que a auditoria NÃO conseguiu verificar (não afirmar que está ótimo)

- **Nada foi visto renderizado.** Este ambiente não tem GPU nem navegador,
  então o que a moldura e o zoom fazem *no celular do dono* é dedução do CSS,
  não medição. Precisa da palavra dele: a tela ficou inteira? Deu para alcançar
  o canto? O zoom 200% ajudou a ler?
- **Toque real.** O remapeamento de toque com canvas escalado é feito pelo
  próprio Godot (`getBoundingClientRect`), mas não testei com dedo.
- **Desempenho no aparelho (medido daqui, não no aparelho dele).** `index.wasm`
  tem 35.376.909 B crus, mas o Pages serve gzip: **8.145.118 B entregues**
  (`curl -sI --compressed`). O `index.pck` foi de 30.128 → 89.520 B na rev C e
  **84.704 B na rev C.1** (os scripts de ferramenta — `teste_economia.gd`,
  `prova_visual.gd`, `grava_jogo.gd` — ficaram fora do pacote pelo
  `exclude_filter` do preset). Com a rede limitada via CDP: 3,3 s sem throttle,
  ~49,6 s em 4G **sem** gzip → **~12 s em 4G com os 8,1 MB reais**, ~44 s em 3G.
  Os fps daqui (7,8–9,8) **não** valem para o aparelho dele: são llvmpipe com
  2 CPUs, e só servem para detectar patologia.
- **A letra ainda é pequena no celular, e a causa não é o `.tscn`.** O projeto
  é 1280×720 com `stretch/mode="canvas_items"`: num celular de ~390 pt de
  largura, o inteiro é reduzido a ~30%. Uma fonte de 17 px dentro do jogo vira
  ~5 px no vidro. O zoom 150/200% é alívio parcial (e exige arrastar). A
  verdadeira cura é a **reformulação da interface** (painéis mais largos, menos
  texto por linha, widget grande) — adiada por ordem do dono, que quer o teste
  antes disso. Esta auditoria melhorou o que dava para melhorar sem refazer a
  interface, e é honesto dizer que isso não resolve a queixa original dele.
- **Segundo plano.** O `_process` para quando a aba do navegador vai para trás,
  e não há progresso offline nem salvamento — planejado para a Semana 8. Num
  celular, "a tela apagou" = "nada cresceu". Isso é conhecido e não foi
  consertado aqui.

---

## Lista do que **não** mudou (decisão, não esquecimento)

| Assunto | Por quê |
|---|---|
| Layout / reformulação da interface | adiada pelo dono até o veredito do teste; o roteiro está em `progresso.md` ("Roteiro da reformulação da interface") |
| `version/code`, `version/name`, política de update, changelog | antes do lançamento não existe versão (decisão dele, registrada) |
| Salvamento, progresso offline, tela de título | Semana 8 |
| `progressive_web_app/enabled` | continua `false` de propósito: o service worker prenderia o cache e ele testaria rascunho velho |
| Números de balanceamento (custos, tempos, preços) | mexer neles junto com correção de código misturaria as causas; a fila própria está marcada ⚠️ em `progresso.md` |
| Arte e som | Semana 7 |

---

## Publicação — estado

`https://reboclbrank-max.github.io/site/ceifalume/` precisa do **push** do
repositório `site` (`b2f6b3a`). Enquanto o push não roda, a URL continua
servindo a rev A (o jogo anterior, sem estas correções). Ver `pendencias.md` §1
— o push está bloqueado por token novo do dono, não por trabalho inacabado.

Arquivos no destino local `site/ceifalume/`: `index.html` 20.925 B,
`index.pck` 84.272 B (novo, byte a byte igual ao build), `index.wasm`
35.376.909 B (igual), `index.js` 331.495 B (igual), `manifest.webmanifest`
793 B, três ícones da marca. Selo na tela: `rascunho 2026-09-15 · rev B ·
Semana 6`.

## O que foi verificado depois disso (ambiente de render construído na mesma data)

A lacuna declarada acima ("nada foi visto renderizado") foi fechada montando
ambiente para renderizar de verdade, neste mesmo espaço de trabalho:

- **Rota A — o jogo renderizado pelo motor:** `Xvfb` + Mesa llvmpipe (GPU por
  software, OpenGL 4.5) + o mesmo Godot 4.3, com a ferramenta `prova_visual.gd`
  (na raiz do repositório do jogo). Fotografa a cena real e **mede** cada nó
  crítico: posição, tamanho, se passa da janela, se o texto foi cortado
  (`get_combined_minimum_size()` vs largura recebida) e se está apenas dentro de
  uma lista rolável.
- **Rota B — a página no navegador:** Chromium 152 do Debian + `puppeteer-core`,
  com WebGL por SwiftShader. Abre a pasta publicada, espera o motor iniciar e
  mede `getBoundingClientRect` do canvas, se o quadro cabe na caixa, se precisa
  rolar, a escala do jogo, quantos píxeis físicos tem uma fonte de 17 px, erros
  de JavaScript e requisições quebradas.

**O que ele pegou de imediato — dois defeitos que a leitura de código não achava,
causados pela minha própria mudança de legibilidade:**

1. A coluna central passou a medir 1012 px dentro de uma janela de 720 px, e o
   contêiner era um `CenterContainer` (que centraliza, dividindo o excesso em cima
   e embaixo): o contador **"Moedas" ficava 86 px ACIMA da tela**, a sementeira
   42 px cortada, e "Composteira", "Carroça" e "Fazer um bico" abaixo do fim da
   tela. Na rev A eram 6 px cortados; na rev B, 292 px. Um botão de compra
   literalmente fora do mundo não aparece em revisão de `.gd` nenhum.
2. Os botões da sementeira, com `autowrap` e sem largura mínima, **colapsaram para
   ~16 px cada** e a linha inteira sumiu da tela.

Corrigido no commit `ef00926` do repositório `ceifalume` (Centro vira
`MarginContainer`; Corpo/Loja/Grade expandem na vertical; a Loja ganha
`ScrollContainer`; sementeira com 116 px mínimos e `SIZE_EXPAND_FILL`; sem o
padding de 6 px da caixa da página). Re-medido em 1280×720, 844×390 e 390×844:
**zero itens fora da tela, zero textos cortados, 48/48 no teste de bancada, zero
`SCRIPT ERROR`**.

**Números medidos no navegador com o build atual (rev C), DPR 2:**

| Janela | Quadro do jogo | Cabe inteiro? | Precisa rolar? | Escala | Fonte de 17 px vira |
|---|---|---|---|---|---|
| 844×390 (celular deitado) | 693×390 CSS | sim | não | ×0,542 | **18,4 px físicos** |
| 390×844 (celular em pé) | 390×219 CSS | sim | não | ×0,305 | 10,4 px físicos |
| 1280×720 (desktop) | 1280×720 CSS | sim | não | ×1,0 | 34 px físicos |

Leitura honesta: deitado a letra está no limite do confortável (18 px físicos é
visível, mas é letra de rodapé, não de jogo); em pé continua inviável — por isso
o aviso "gire o celular" existe, e a cura de verdade é a reforma da interface
(poucos elementos, grandes), não aumentar fonte.

**Como refazer o ambiente numa sessão nova** (nada disto persiste entre ambientes;
as ferramentas somem, os comandos não):

```bash
# 1. motor de render (rota A) — depois de rodar preparar-godot.sh
sudo apt-get update -q
sudo apt-get install -y -q xvfb mesa-utils libgl1 libglu1-mesa fonts-dejavu-core
cd /home/user/ceifalume
xvfb-run -a -s "-screen 0 1280x720x24" \
  env LIBGL_ALWAYS_SOFTWARE=1 CEI_MEDIR=1 CEI_CENARIO=meio \
  CEI_SAIDA=/home/user/tools/renders/tela.png \
  ~/.cache/ferramentas/godot --path . --rendering-driver opengl3 \
  --resolution 1280x720 --script res://prova_visual.gd

# 2. navegador (rota B)
sudo apt-get install -y -q chromium fonts-liberation
cd /home/user/tools && npm i puppeteer-core@23
python3 -m http.server 8099 --directory /home/user/site &
node /home/user/tools/medidor-encaixe.js
```

Os dois scripts (`prova_visual.gd` versionado no repositório do jogo;
`medidor-encaixe.js` em `tools/`) não fazem parte do build: o `.gd` fica de fora
do `.pck` pelo `exclude_filter` do preset, e o `.js` vive fora do repositório.

---

## O que fazer com esta auditoria

- **Próxima ação do dono:** mandar o token da sessão → push dos três repositórios
  → abrir a URL no celular e responder três coisas: a tela cabe inteira? o zoom
  150/200% deixou legível? o celeiro cheio ainda trava algo?
- **Próxima ação do assistente (depois do veredito):** reformulação da interface
  com o filtro "texto grande" como critério de aceite, depois Semana 7.
- **Sempre que mexer na economia:** rodar `teste_economia.gd` antes de exportar.
  Ele é a rede que faltava; as Semanas 1–6 passaram sem.

## Desdobramento da rev C.2 (2026-09-15, 3ª rodada): dois defeitos achados pela régua nova

| # | Defeito | Como apareceu | Estado |
|---|---|---|---|
| 13 | Preço da Flor de Lume ilegível: `2500` desenhado como `250` | a régua apertada (sem tolerância) marcou "⚠ sem folga 0,0 px"; OCR leu "(250"; o pixel não tinha texto nos 8 px antes da borda | ✅ corrigido em `e32514d` (largura medida na fonte + linha com `HFlowContainer`); OCR depois do conserto lê o número fechado |
| 14 | `Coluna` ia a 3381 px no **estado inicial** (Loja em faixa com rótulo curto) | `GridContainer` deixou cada coluna no mínimo do texto (autowrap → 8 px); só se revelou ao rodar a medição sem `CEI_CENARIO=meio` — o cenário mascarava | ✅ corrigido (largura-alvo da célula calculada da janela); depois: 1256×708 nos dois estados |

Aprendizado de auditoria, registrado para não repetir: (1) toda régua precisa do
estado *vazio* no banco de casos, senão o cenário de demonstração vira cúmplice;
(2) limite de visibilidade é o do container que rola, não o da janela — acrescentado
como "campos inteiros dentro da grade (sem rolar)". Medida nova, com a faixa da Loja
em 136 px: **3 de 6** campos inteiros dentro da grade em 1280×720 (a grade é rolável
por design: ela comporta os 24 campos), **6 de 6** em 390×844.

Camada de verificação que passou a existir, com número: diff de pixels com tolerância
(`~/tools/compare-frames.sh`) e OCR de recorte (`convert … -crop` + `tesseract --psm 7`).
Medido com `~/tools/compare-frames.sh` (2026-09-15): **rev C.1 × rev C.2 = 38.675 px
diferentes de 921.600 (4,19 %) com fuzz 12 %** — o tamanho esperado de uma mudança real
de interface. E o controle, que deu trabalho achar o valor certo: renderizar o MESMO build
duas vezes com o MESMO cenário dá **20 px** de diferença (medido), porque o preço do
dia é sorteado em tempo de execução — não existe bit-exatidão sem semente fixa. Bit-exato
só o par "mesmo arquivo × ele mesmo" (0 px). Conclusão metodológica que fica: dezenas de
px entre renders são ruído de dado; a régua útil começa em milhares, e **o número do
projeto precisa de `CEI_SEMENTE` no jogo** (anotado em `pendencias.md`) se um dia
quisermos golden-image de verdade.