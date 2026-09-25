# Ceifalume 100% profissional — auditoria + pesquisa (2026-09-16)

> Resposta ao pedido do dono: "pesquisas que façam o jogo ficar 100%
> profissional e não restar nada genérico". Este documento é o mapa; a
> execução acontece nas próximas rodadas, uma frente por vez.

## Resumo executivo (leitura de 2 minutos)

O jogo está **terminado e testado**, mas "terminado" ≠ "profissional". A
auditoria achou **18 itens genéricos/provisórios**, em 3 grupos:

1. **Bloqueadores da loja Play (8)** — sem eles, o Google nem aceita o jogo.
   O mais urgente: estamos com `target_sdk 34` e o prazo do Google (31/ago/
   2026) **já passou** — hoje a loja exige API 36. E o motor Godot 4.3 não
   atende a exigência de 16KB (vale desde nov/2025) — precisa subir para
   4.5.2+.
2. **Dentro do jogo (7)** — sons provisórios, sem tutorial, sem objetivos
   curtos (padrão do gênero: quadro de pedidos), sem vibração/configurações,
   site com carimbo "rascunho".
3. **Papelada da loja (3)** — política de privacidade, consentimento de
   anúncios (UMP), conta de desenvolvedor (US$25 + decisão pessoal/empresa).

Nada aqui custa mensalidade nem servidor: tudo cabe na regra de ouro (só
investe o que ganhar). O único dinheiro é a taxa única de US$25 da conta
Play — e só na hora de publicar.

## Parte 1 — Inventário do genérico (o que a auditoria achou)

| # | Item genérico/provisório | Onde está | Vira o quê |
|---|---|---|---|
| P1 | `target_sdk 34` (loja exige 36 desde 31/ago/2026) | `export_presets.cfg` | `target_sdk 36` |
| P2 | Godot 4.3 sem suporte a páginas de 16KB (exigido p/ apps novos) | motor | Godot 4.5.2+ (ou 4.x estável mais novo) |
| P3 | Plugin AdMob v3.1.3 (mínimo dele hoje é Godot 4.5) | `addons/admob/` | Plugin v5.x + rewarded revalidado |
| P4 | Entregável é APK (a Play só aceita AAB) + sem Play App Signing | build | Export AAB; nossa chave vira chave de upload |
| P5 | Sem política de privacidade, sem Data safety, sem classificação IARC | lugar nenhum | URL pública + 2 formulários no Console |
| P6 | Sem conta de desenvolvedor Play | com o dono | US$25 + CPF ou CNPJ (decisão do dono) |
| P7 | Sem tela de consentimento de anúncios (UMP) | `anuncios.gd` (0 usos) | UMP ligado antes de carregar anúncio |
| P8 | Sem `app-ads.txt` (AdMob marca como não verificado) | site | arquivo no nosso domínio (grátis) |
| J1 | 6 efeitos sonoros "provisórios" + música procedural | `arte/som/` | SFX reais CC0 + música real + tela de créditos |
| J2 | Sem tutorial, sem "como jogar" | jogo | onboarding de 3–4 passos + ajuda |
| J3 | Sandbox puro (sem objetivos curtos) | jogo | quadro de pedidos ("entregue 5 nabos") |
| J4 | Só tem botão liga/desliga som; sem vibração | jogo | config música/som/vibração + vibrar nos toques |
| J5 | Sem suco de jogo (moeda voando, pulo da planta...) | jogo | juice barato: 3–5 microanimações |
| J6 | Site carimbado "rascunho" + meta description de teste | `site/` | página oficial (jogo + privacidade + contato) |
| J7 | Versão pública indefinida ("C.14" é codinome interno) | pendência #7 | 0.x ou 1.0 (decisão do dono) |
| J8 | Material de loja velho (itch C.9) / inexistente (Play) | `divulgacao/` | screenshots + capa + feature graphic novos |

Confirmado como JÁ profissional (não mexer): arte cartoon final (6 plantas ×
3 estágios, ícone, splash), anúncios só-recompensa, save offline 8h, 64-bit,
regras de preço/eventos, régua de testes 91/28/5/3.

## Parte 2 — O que a pesquisa descobriu (com fontes)

### 2.1 Regras da Play em set/2026 (fresquinho, conferido hoje)

- **API 36 obrigatória** para apps novos/atualizações desde 31/ago/2026
  (antes: API 35). Console bloqueia upload abaixo disso. ([ptkd](https://ptkd.com/journal/google-play-target-api-level-2026),
  [pixelappy](https://pixelappy.com/blogs/google-play-api-deadline-for-android-apps/))
- **16KB obrigatório** desde 1/nov/2025 para apps com código nativo (todo jogo
  Godot). Suporte entrou no Godot **4.5** (PR #106358, NDK r28b); 4.3 e 4.4
  **não** atendem. ([issue Godot](https://github.com/godotengine/godot/issues/110262),
  [fórum](https://forum.godotengine.org/t/godot-and-google-play-policy-warning-about-16-kb-memory-page-size/120934))
- **Conta pessoal nova** (criada após 13/nov/2023): teste fechado com **12
  testadores por 14 dias seguidos** + prova de uso real + pedido de acesso à
  produção. Conta **empresa**: sem essa exigência.
  ([medium](https://medium.com/@kefayatkhadem/google-play-closed-testing-in-2026-the-full-path-from-12-testers-to-production-access-1f48b7833671),
  [primetestlab](https://primetestlab.com/blog/google-play-changed-20-to-12-testers),
  [testerscommunity](https://www.testerscommunity.com/blog/google-play-closed-testing-requirements-2026))
- **Conta: US$25 uma vez**, sem anualidade. Pessoal = documento com foto
  (2–5 dias); empresa = D-U-N-S + documentos (5–10 dias úteis), publica com
  nome da empresa (passa mais credibilidade) e **não dá para virar empresa
  depois** (só transferindo o app). Verificação de desenvolvedor chega ao
  Brasil em 30/set/2026.
  ([testerscommunity](https://www.testerscommunity.com/blog/google-play-developer-account-guide),
  [afkarsoftware](https://afkarsoftware.com/en/blog-detail/google-play-console-account-2026-one-time-25-fee/),
  [colorleaves](https://colorleaves.in/blog/google-play-console-developer-account-setup-india/))
- **Formato AAB** (APK não entra) + **Play App Signing** (Google guarda a
  chave final; a nossa vira chave de upload — o `~/cofre/` continua valendo).
  ([testerscommunity](https://www.testerscommunity.com/blog/google-play-closed-testing-requirements-2026))

### 2.2 Privacidade, consentimento e dados (AdMob + Play + LGPD)

- **Data safety**: com AdMob, declarar: IDs de dispositivo (GAID —
  coletado+compartilhado), localização aproximada (via IP), atividade no app;
  finalidade = exibir/medir anúncios. A política de privacidade **precisa
  dizer o mesmo** que o formulário (o Google cruza os dois).
  ([doc oficial](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en),
  [tabela por SDK](https://ultrafastutilities.com/android-app-privacy-policy-template),
  [guia 2026](https://respectlytics.com/blog/google-play-data-safety-guide/))
- **Política de privacidade grátis**: geradores prontos para Play+AdMob —
  [nextnative](https://nextnative.dev/free-tools/play-store-privacy-policy)
  (marca AdMob, exporta Markdown),
  [8gwifi](https://8gwifi.org/app-privacy-policy-generator.jsp) (sem cadastro,
  HTML/Markdown),
  [firebaseapp](https://app-privacy-policy-generator.firebaseapp.com/)
  (clássico). Hospedagem grátis: nosso próprio GitHub Pages.
- **Consentimento (UMP)**: o plugin AdMob já traz o módulo UMP; nosso
  `anuncios.gd` não chama nada dele (grep = 0). Regra: mostrar o formulário
  onde a lei exige (Europa) **antes** de carregar anúncio; sem consentimento
  o Google serve anúncio limitado/não-personalizado ou nada — configurar
  "limited ads" no console do AdMob. Brasil (LGPD): política + consentimento
  para personalização.
  ([discussão dev](https://www.reddit.com/r/androiddev/comments/18my9ht/about_admob_ump_what_are_the_ruleslaws_of_whats/),
  [fórum AdMob](https://groups.google.com/g/google-admob-ads-sdk/c/pG2eFsfJRlY))
- **app-ads.txt**: arquivo de 1 linha no domínio do desenvolvedor; sem ele o
  AdMob trata o app como não verificado. Nosso domínio (GitHub Pages) serve
  de graça.

### 2.3 Upgrade do motor (Godot 4.3 → 4.5.2+)

- Migração 4.4→4.5 é "relativamente segura" segundo o doc oficial; quebras
  listadas são de C# e plugins de editor — nosso jogo é GDScript puro, sem
  GDExtension. ([doc migração](https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.5.html))
- Linha estável atual: 4.5.x (4.5.2 em mar/2026; já se fala em 4.6.x —
  decidir a versão exata na hora do upgrade).
  ([anúncio 4.5.2](https://godotengine.org/article/maintenance-release-godot-4-5-2/))
- **Atenções do nosso projeto**: regenerar o template de build Android,
  re-salvar `export_presets.cfg`, reimportar `.godot`, trocar o plugin AdMob
  (abaixo) e **rodar a régua inteira + rebuildar APK e web do zero**.
- Plugin AdMob: mínimo atual **Godot 4.5+** com compileSdk 35
  ([PR #520](https://github.com/poingstudios/godot-admob-plugin/pull/520)).
  Nosso v3.1.3 → v5.x: reservar folga para mudança de API (testar rewarded
  com ID de teste antes de plugar o real).

### 2.4 O gênero pede o quê? (benchmark fazendas cozy 2026)

Hay Day/Township/Family Farm (líderes) têm em comum: **pedidos com prazo**
(quadro/caminhão/barco), eventos por temporada, decoração, área social e
configurações completas; sessões curtas e progresso offline. A tendência cozy
2026 é conforto + criatividade + conexão, com atualizações regulares.
([Hay Day](https://apps.apple.com/us/app/hay-day/id506627515),
[top 10 2026](https://www.playnforge.com/best-farming-games-mobile/),
[trend cozy](https://webapprater.com/web-app-development/cozy-social-farming-games-trend-2026.html))
Nosso diferencial (ninguém tem): **fazenda noturna + especulação de preço**
(vender na hora certa). O plano: copiar só o que cabe sem servidor (pedidos,
tutorial, configs, eventos) e dobrar a aposta no diferencial.

### 2.5 Áudio profissional de graça (licenças conferidas)

- **SFX**: Kenney (CC0 total, sem crédito, uso comercial liberado) para
  cliques/moedas/UI; Freesound para ambiências específicas (conferir faixa a
  faixa: só CC0 ou CC-BY). ([cinevva](https://app.cinevva.com/guides/free-sound-effects-music),
  [gamineai](https://gamineai.com/blog/12-best-free-sound-effect-libraries-game-developers))
- **Música**: Pixabay Music (uso comercial, sem crédito; só não pode revender
  o arquivo puro) — buscar "cozy/farm/acoustic loop"; alternativa CC-BY:
  Incompetech (1 linha de crédito). Nossa caixinha procedural vira plano B.
- **Proibido**: CC-BY-NC, Jamendo grátis (só uso pessoal) e qualquer faixa
  sem licença escrita. Tudo com fonte anotada + tela de créditos no jogo.

## Parte 3 — Plano em fases (ordem de execução proposta)

| Fase | Conteúdo | Turnos estim. | Trava |
|---|---|---|---|
| **A. Base da loja** | Godot 4.5.2+ + plugin v5 + target 36 + AAB + régua+rebuild total | 2–4 (o upgrade do motor é o risco) | nenhuma |
| **B. Papelada** | política + Data safety + IARC + UMP + app-ads.txt + conta (dono) + 12 testadores (dono) | 1–2 + 14 dias de teste | decisão pessoal/empresa |
| **C. Áudio real** | SFX CC0 + música + créditos + re-testar som | 1–2 | nenhuma |
| **D. Conteúdo** | tutorial + pedidos + configs/vibração + juice + site oficial + screenshots | 3–5 | veredito de gosto do dono |
| **E. Produção** | listagem da loja + lançamento | com o dono | fases A–D |

## Parte 4 — Decisões que são do dono (quando chegar a hora)

1. **Conta Play: pessoal (CPF) ou empresa (CNPJ)?** Pessoal = publica no seu
   nome + teste de 12 pessoas × 14 dias. Empresa = precisa D-U-N-S, publica
   como Rebocl Brank, pula o teste fechado. US$25 de todo jeito.
2. **Número da versão pública:** 0.x (acesso antecipado) ou 1.0 (lançamento)?
3. **Nome público do estúdio** (se conta empresa): "Rebocl Brank" ok?
4. **Música**: manter nossa caixinha ou trocar por faixa real? (voto com ouvido)
5. **Lança/não-lança** (a decisão-mãe, pendência #1).

## Parte 5 — Fora de escopo de propósito (e por quê)

Multiplayer/social, ranking online e save na nuvem: exigem servidor (custo
mensal — fere a regra de ouro). Segundo idioma: dobra todo texto/revisão;
v1 PT-BR. Crashlytics: grátis, mas exige conta Firebase + plugin — opcional
fase 2. Nada disso impede o "100% profissional" na loja.

## Fontes (links vivos em 2026-09-16)

Ver links inline nas seções 2.1–2.5. Regra: antes de executar cada fase,
re-abrir os 2–3 links dela (regra de loja muda todo ano).

## Andamento (dias seguintes)

- 2026-09-16: P7 feito (UMP ligado em `anuncios.gd`); P5 parcial (política
  publicada em `site/privacidade.html` + fonte em `divulgacao/`; faltam Data
  safety + IARC, que são formulários no Console na hora da loja); P8 parcial
  (`app-ads.txt` criado; validação total exige domínio próprio ou repo de
  usuário — adiado, $0); J6 feito (site sem "rascunho" + link Privacidade).
  Régua após as mudanças: 91/28/5/3 + trio zero erros. UMP/política entram na
  C.15 (o APK e o pck C.14 publicados não os contêm).
- Ordem de execução (dono sem dinheiro p/ investir): frentes grátis e
  visíveis primeiro (papelada técnica, áudio, conteúdo); upgrade do motor
  (fase A) fica para quando a Play estiver próxima (a taxa US$25 é o
  gargalo real, não a técnica).

- 2026-09-16 (arte): análise tela a tela feita; J-fonte e J-suco-parcial
  feitos (Baloo 2 + balanço + pop + gramática). Áudio (fase C) é o próximo.

- 2026-09-16 (fechando): S2 + T5 feitos; capa pronta; bugs caçados. 93/100.
  Restam L1/L6 (upgrade do motor, próxima empreitada) + L5 (dono).
