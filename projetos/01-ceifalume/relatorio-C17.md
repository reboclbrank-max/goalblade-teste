# Relatório C.17 — Auditoria total + APK de teste + AAB code 16 (2026-09-16)

## 1. Veredito (honesto)

- **Jogo (lógica, som, tela, save): 100% verificado, zero defeito aberto.** A tortura e a
  régua passaram limpas; o que elas acharam foi corrigido e travado com teste.
- **Anúncio (o dinheiro): ESTAVA QUEBRADO e foi CONSERTADO.** O plugin AdMob nunca tinha
  sido ligado no editor: todos os builds Android até aqui (inclusive o AAB code 15)
  saíam **sem o SDK do Google dentro** — nenhum anúncio jamais apareceria e nenhum
  centavo entraria. Achado, corrigido e provado nesta auditoria (seção 4).
- **Entregas de hoje:** APK de teste `0.1-teste` (84 MB, instala direto) + link web
  atualizado + AAB code 16 pronto para o Play (36 MB, ID real, SDK dentro).

## 2. Matriz de verificação (tudo que rodei)

| # | Frente | Ferramenta | Resultado |
|---|--------|------------|-----------|
| 1 | Economia-1000 (regras, preços, lojas, poço, evento, save) | teste_economia.gd | **90/90** |
| 2 | Tortura A (3000 ações aleatórias, seed 777) | teste_tortura.gd | **3000/3000, 0 invariantes quebradas** |
| 3 | Tortura B (saves corrompidos/estranhos) | teste_tortura.gd | **9/9** |
| 4 | Tortura C (estresse: 24 campos, celeiro, Flor) | teste_tortura.gd | **6/6** |
| 5 | Tortura D (persistência: salva→fecha→abre→confere) | teste_tortura.gd | **4/4** |
| 6 | Erros de script em TUDO acima | grep SCRIPT ERROR | **zero** |
| 7 | Som (8 ganchos, liga/desliga, música) | teste_som.gd | **28/28** |
| 8 | Anúncios (lógica: UMP, premiado, fallback) | teste_anuncios.gd | **5/5** |
| 9 | Clique real no campo (mouse de verdade) | teste_clique_campo.gd | **3/3** |
| 10 | Simulação 5000 dias (economia não quebra no longo prazo) | sim_limite.gd | **24/24, Flor 137.5/campo-dia** |
| 11 | Auditor profissionalismo (identidade, arte, som, textos, loja) | auditor-100.py | **100/100** |
| 12 | Telas no motor 4.5.2 (abertura RB + título, olho humano) | Xvfb + captura | **aprovadas** |
| 13 | Web: Jogar→tutorial→plantar→moedas 25→20, áudio running, 0 erros de página | fumaca-web.js | **verde** |
| 14 | APK teste: assinatura, 0.1-teste/code 16/sdk 24→36, App ID de TESTE, SDK no dex (23), zipalign 16K | apk-teste.sh | **verde, exit 0** |
| 15 | AAB code 16: validate, manifesto, App ID REAL, ELF 16K, splits 16K, SDK no split entregue (23) | publicar-apk.sh | **verde, exit 0** |
| 16 | Segredos (ID real de anúncio e senhas fora dos repos) | git grep 3 repos | **0 ocorrências** |

## 3. Defeitos achados E corrigidos (com a trava que impede voltar)

1. **Tortura B (saves estranhos):** `bool(texto)` explodia; seção de save inexistente
   gritava; evento inválido + celeiro negativo aceitos. → Higiene de tipos + evento
   canônico + `maxi(0)` + guarda `has_section`. Trava: tortura B 9/9 no próximo ciclo.
2. **Textos cortados:** "Flor de Lume: 55…" e "(chuva b…" estouravam o painel. →
   Preços 15px + ritmo sem sufixo (o evento já tem linha própria). Trava: olho no render.
3. **Export web puxava lixo do plugin (17 erros):** amostras C# entrando no pacote. →
   Preset web exclui `skills/*` e `csharp/*`. Trava: export com grep de erro = 0.
4. **Templates no caminho errado:** motor 4.5.2 procura `4.5.2.stable`, scripts usavam
   `4.5.stable` (resto da época do 4.3). → Scripts corrigidos. Trava: export web no ciclo.
5. **O CRÍTICO — anúncio morto (detalhe na seção 4).** Trava em 4 camadas (§4).

## 4. O caso do anúncio (para constar, sem enfeite)

- **Sintoma:** o APK de teste saía sem a entrada `APPLICATION_ID` no manifesto.
- **Causa 1:** o plugin AdMob nunca foi habilitado no editor (`[editor_plugins]`
  ausente no `project.godot`) — o instalador original foi só copiar arquivos.
  Sem isso, o exportador do plugin nunca rodava: sem dependência Maven, sem AARs,
  sem manifesto. Prova: dex do AAB-15 tinha **0** marcadores do SDK.
- **Causa 2 (pegadinha do editor):** com o plugin ligado, o editor APAGA a seção
  `[admob]` do `project.godot` quando ela vale o padrão (= ID de teste). Descoberto
  quando a trava de segurança do script abortou o build v3. O exportador usa o padrão
  como fallback (provado: manifesto v2 com ID de teste), então estado correto do
  repo = seção ausente.
- **Causa 3 (pegadinha da medida):** o R8 ofusca os pacotes — `gms/ads` some do dex
  mesmo com o SDK dentro. Medida certa: URLs que sobrevivem (`doubleclick`,
  `googlesyndication`, `ads-mobile-sdk`). Positivo: **23** no APK e no split; **0** no AAB-15.
- **Causa 4 (pegadinha do split):** o split `arm64` só tem `.so` — o dex mora no split
  `master`. O script agora descobre o master sozinho.
- **Causa 5 (infra):** `/tmp` (1 GB) estourou assinando os splits. Script usa `/home` agora.
- **4 travas permanentes:** (a) auditor L4 exige plugin + UMP + App ID de teste;
  (b) `apk-teste.sh` aborta se faltar ID de teste no manifesto ou SDK no dex;
  (c) `publicar-apk.sh` aborta se faltar ID real no manifesto ou SDK no split;
  (d) injeção do ID real virou UPSERT (recria a seção se o editor apagou).

## 5. Como o dono testa (ordem recomendada)

1. **APK de teste** (`ceifalume-teste.apk`, 84 MB): copia para o celular, toca para
   instalar (autoriza "fonte desconhecida" uma vez), joga. O anúncio é de mentira
   (demo do Google, escrito "Test Ad") de propósito — clicar nele não dá dinheiro
   nem causa problema. Versão marcada `0.1-teste`, impossível confundir.
2. **Link web** (mesmo link de sempre, já atualizado): abre no navegador do celular
   ou do PC. Vale para mostrar para os outros.
3. **O que conferir no aparelho:** som sai? música continua? 5 toques no título abrem
   o painel de teste? anúncio demo aparece e dá a recompensa? tela gira sem quebrar?
   volta ao jogo depois de atender ligação? (checklist completo na conversa).
4. **Play Interno só DEPOIS** do dono aprovar o APK + conta de desenvolvedor ($25
   uma vez, na conta/moeda dele) + eu subir o AAB-16 na faixa de teste interno.

## 6. Roadmap até o Play (resumo; detalhe na conversa)

Teste privado (APK + web, AGORA) → aprovação do dono → conta Play $25 dele →
faixa interna (só quem ele convidar) → 12–14 dias de teste fechado (regra do Google
para contas novas) → produção. Eu preparo textos, imagens e formulários; ele só
paga os $25 e clica onde eu mandar.

## 7. Dinheiro (recap de 3 linhas)

Anúncio PREMIADO e opcional (só aparece se o jogador quiser dobrar a venda).
Google fica com ~30%, ele com ~70%; recebe por transferência quando juntar
US$ 100. Sem anúncio no meio da cara, sem pagar nada antecipado.

## 8. Commits de hoje (tudo guardado e empurrado)

- `ceifalume`: `f1bfbf0` (tortura+correções) → `1ccbc2b` (textos+preset web) → `8647d03`
  (plugin ligado + canônico). Remoto confere.
- `site`: `5dc6601` (web 4.5.2 no ar). Remoto confere.
- `base`: ferramentas (`apk-teste.sh`, `fumaca-web.js`, `publicar`/`auditor` novos) +
  este relatório. Remoto confere.
- Segredos: App ID real e senhas = 0 ocorrências nos 3 repos (só teste + unidade
  premiada real no código, que é o desenho desde o C.15).
