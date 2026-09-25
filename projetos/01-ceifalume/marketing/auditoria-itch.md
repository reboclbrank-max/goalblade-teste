# Auditoria da itch.io — perfil + página do Ceifalume

**Rodada 1 (2026-09-17):** leitura externa do HTML público + conferência byte
a byte das imagens.
**Rodada 2 (2026-09-17):** auditoria 100% via API oficial com a chave do
dono + reconfirmação após a edição de tags manual.
**Rodada 3 (2026-09-18):** aplicação das correções **via API** (endpoint de
escrita descoberto por sondagem) + verificação item a item na página pública
+ um incidente (tags, depois `p_android`) com lição registrada.

- Jogo: https://reboclbrank-max.itch.io/ceifalume (id **5017404**)
- Perfil: https://reboclbrank-max.itch.io/ (id 15163150)
- Chave da API, o que ela dá/não dá e as regras do endpoint de escrita:
  `base/ferramentas/chaves.md`
- Textos prontos para o que fica web-only:
  `base/projetos/01-ceifalume/marketing/itch-kit-manual.md`

---

## 1. Dados oficiais pela API (medição de referência — repetir para medir
antes/depois a cada sessão de marketing)

| Campo | Valor em 2026-09-18 (medição da rodada 3) |
|---|---|
| Views | **14** |
| Downloads | **1** (o APK) |
| Compras | 0 (jogo grátis) |
| Publicado | 2026-09-16 21:06 UTC |
| Capa | 630×500 (tamanho oficial recomendado — ok) |
| Build no ar | HTML5 (zip subido pelo dono; carimbo a conferir no celular) |

Ler 14 views no dia 2 sem audiência ainda é normal — o que move esse número é
o item M (comunidades/Shorts/lojas); a página só precisa não desperdiçar quem
chega.

## 2. Os 10 achados da rodada 1 — status FINAL (2026-09-18)

| # | Achado | Prioridade | Status |
|---|---|---|---|
| 1 | Faltavam tags do nicho (idle/incremental/farming/offline) | P0 | ✅ **RESOLVIDO via API (2026-09-18):** as 10 tags finais no ar e verificadas no HTML da página — `idle, incremental, farming, cozy, casual, relaxing, management, economy, mobile, offline` (o dono tinha adicionado idle/incremental/farming manualmente; o resto foi feito pelo assistente via `POST /games/5017404`) |
| 2 | Zero GIF na galeria | P0 | ✅ **GIF NO AR via API (2026-09-18):** `gif-jogo-ceifalume-640x360.gif` (14 s, 640×360, 3,0 MB; janela 13,5–27,5 s do trailer) hospedado em `site/media/ceifalume/` (GitHub Pages) e **embutido no topo da descrição** (`<img>` sobreviveu ao changeset; URL 200 image/gif). A galeria em si (badges) continua web-only — item opcional do dono |
| 3 | Screenshot nº 1 = capa duplicada (mesmo SHA-256, 630×500) | P1 | 🟡 **Meio resolvido:** substituta pronta (`shot-jogo-1280x720.png`, hospedada em `site/media/ceifalume/`); **excluir a duplicada (id 30040026) é web-only** (API de imagens morta) — 1 clique do dono |
| 4 | "Capa 630×500 deveria virar 1024×500" | P1 | ❌ **Achado ERRADO (corrigido):** doc oficial da itch recomenda **630×500** (315:250); 1024×500 só para featured editorial. Capa atual **já está no tamanho certo — nada a fazer** |
| 5 | Descrição sem palavras de busca, link do canal e CTA | P1 | ✅ **RESOLVIDO via API (2026-09-18):** descrição nova no ar e verificada no HTML — 1ª linha com "jogo de fazenda grátis", "Como jogar" (4 linhas), "O que tem" (7 bullets), "Onde jogar" (trailer, canal, site, privacidade, e-mail), linha de marca no pé + GIF embutido no topo |
| 6 | Perfil vestindo o jogo, sem marca nem bio | P1 | 🟡 **Pronto para 1 upload:** `perfil-rb-itch-630x500.png` (monograma RB central — o recorte da itch mostra o RB inteiro no avatar E no banner) + bio pronta no kit; API de perfil é só leitura (POST/PUT negados) — 2 min do dono |
| 7 | Zero interação pública e nada preparado | P2 | ✅ **Kit de 6 respostas pronto** (Seção 8 do kit) — o dono cola quando os comentários chegarem |
| 8 | Sem devlog | P2 | 🟡 **Texto pronto** (Passo 7 do kit: "0.1 no ar: a fazenda não dorme"); endpoint de devlog morto nos dois hosts — 2 min do dono |
| 9 | Qual build está no "Run game"? | P2 | ⏳ **Só o dono verifica** (2 min no celular; deve ser o 0.1 com carimbo) |
| 10 | Toque Rápido no perfil (rascunho 404) | P3 | ✅ **Decisão do dono: não será usado** (API confirmou `published: false`) |

## 3. Incidente da rodada 3 (registrado por extensão no `chaves.md`)

No primeiro uso do endpoint de escrita, encoding de tags errado (`tags[]`)
deixou a página com **1 tag em vez de 10** e o changeset **zerou
`p_android`** (true→false — flag não é campo escrevível). Tags corrigidas na
hora (10 no ar, verificado). **`p_android` continua false** → pendência do
dono: remarcar "Android" em Platforms (1 clique). Plataforma Android do
download (APK 79 MB) continua listada normalmente — o que mudou foi a flag de
metadado.

## 4. O que está bom (manter)

- Released + grátis explícito + indexado na seção Free games
- Trailer embutido (youtu.be/tB449xupDzY) + APK 79 MB no botão Download
- Godot + Simulation preenchidos · og:image/og:title corretos
- Capa 630×500 no tamanho oficial

## 5. O que ficou para o dono (web-only, na ordem) — total ~10 min

1. **Platforms → marcar "Android"** (consequência do incidente) — 1 clique
2. **Excluir a screenshot duplicada** (a 1ª da galeria, idêntica à capa) — 1 clique
3. *(opcional)* Subir o GIF na galeria para o badge de GIF — 30 s
4. **Perfil:** imagem `perfil-rb-itch-630x500.png` + bio (texto no kit) — 2 min
5. **Tema:** Two column (HTML5 nasce single column, esconde a coluna de shots) — 2 cliques
6. **Devlog nº 1** (título + texto no kit) — 2 min
7. **Conferir o "Run game" no celular** (carimbo do 0.1) — 2 min

## 6. Critério de "auditoria resolvida"

Itens 1–6 acima feitos pelo dono + rodadas de medição registradas aqui
(views/downloads antes × depois) + build do "Run game" conferido no celular.
Depois disso: comunidades/Shorts (item M) e lojas grátis (1d).
