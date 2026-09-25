# Imagens e desenhos — como a arte entra e onde ela mora

> Regra-mãe deste arquivo: **imagem que existe só no chat não existe.** Arte
> que não foi commitada em repositório some junto com a conversa. Toda logo,
> desenho, ícone ou som que servirmos usar tem de estar num repositório, com
> nome previsível, antes de ser usada.

## Onde cada coisa mora

| Tipo de arquivo | Repositório | Pasta | Formato |
|---|---|---|---|
| Marca (logo RB, monograma, ícones da marca) | `base` (privado) | `empresa/logo/` | SVG mestre + PNG renders |
| Arte do jogo (plantações, fundo, telas, ícones do jogo) | `ceifalume` (privado) | `arte/` | PNG com alpha; SVG para o que escala |
| Som do jogo | `ceifalume` | `arte/som/` | WAV em produção → OGG no export |
| Arquivos de build publicados (web) | `site` (público) | `ceifalume/` | gerados pelo pipeline — **nunca editar à mão** |
| APK de teste | `ceifalume` | Releases (não no versionamento) | `ceifalume.apk` |
| Prints e imagens para o itch.io | `base` | `projetos/01-ceifalume/divulgacao/` | PNG |

Regra de ouro: **o arquivo-fonte fica junto do que usa.** Marca → na base,
porque é da empresa. Arte do jogo → no repositório do jogo, porque o Godot
precisa enxergar o arquivo para importar.

## Padrão de nome (vale para os dois repositórios)

```
<tipo>-<sujeito>[-<estado ou variante>]-<dimensao>.<ext>
```

- tudo minúsculo, sem acento, sem espaço, sem cedilha;
- **dimensão** = `128` para quadrado, `1280x720` para retangular;
- proibido: `final`, `final2`, `novo`, `versao`, `ok`, `copy`, datas no nome;
- o `.svg` mestre e o `.png` render têm **o mesmo nome**, só muda a extensão;
- a versão editável (Krita `.kra`, Inkscape) fica ao lado quando existir — o
  render derivado se regenera, não se desenha por cima.

Exemplos já usados e previstos:

| Nome | O que é |
|---|---|
| `logo-rb-dourada.svg` / `logo-rb-dourada-512.png` | marca da empresa (existe) |
| `rb-monograma-transparente-192.png` | só o "RB", para sobrepor (existe) |
| `plantacao-nabo-pronto-128.png` | nabo no estágio final (Semana 7) |
| `plantacao-nabo-semente-128.png` | o mesmo nabo no estágio 1 |
| `plantacao-flor-de-lume-pronto-128.png` | a plantação especial |
| `fundo-noite-vagalumes-1280x720.png` | cenário da fazenda |
| `ui-botao-vender-256x64.png` | fatia visual de botão (se sair do tema nativo) |
| `icone-jogo-ceifalume-512.png` | ícone do jogo nas lojas (substitui o `icon.svg` provisório) |
| `som-colher-01.ogg` | efeito de colher |

## Como o dono entrega um desenho

1. **Pelo chat:** anexar a imagem (ou o `.kra`/`.svg`) e dizer em uma linha o
   que é e onde deve aparecer. O assistente renomeia conforme o padrão, salva
   na pasta certa, roda o import do Godot e registra no `progresso.md`.
2. **Pelo GitHub:** arrastar o arquivo na pasta dentro do repositório
   (`ceifalume` → `arte/…`) e fazer commit. O assistente puxa com `git pull` no
   próximo turno.
3. O que o dono **não** precisa fazer: pensar nome de arquivo, tamanho, formato
   de exportação, nem mexer em cena — isso é trabalho do assistente.

Dimensões amigas do Godot: potências de dois (64, 128, 256, 512). Para o fundo,
usar o tamanho da janela do projeto (1280×720) ou o dobro.

## Tamanhos que a marca já tem prontos (em `empresa/logo/`)

| Tamanho | Para quê |
|---|---|
| 512×512 | ícone de loja (Google Play) e ícone do itch.io |
| 192×192 | ícone Android/PWA |
| 180×180 | `apple-touch-icon` |
| 64×64 | README, listas |
| 32×32 | favicon |

Especificações de itch.io e Google Play **conferir na doc oficial na hora de
publicar** (Semana 8) — não decorar tamanho de banner, eles mudam.

## Ferramenta de render (SVG → PNG)

```bash
pip install cairosvg pillow
python3 -c "import cairosvg; cairosvg.svg2png(url='entrada.svg', write_to='saida-512.png', output_width=512, output_height=512)"
```

⚠️ **Não usar ImageMagick para SVG neste ambiente:** o renderizador interno
(`MSVG`) ignora gradiente e texto e devolve um quadrado preto silenciosamente
(aconteceu em 2026-09-15). Sempre **abrir e olhar** o PNG gerado antes de
commitar — render quebrado passa por "fundo escuro bonito" se ninguém verificar.

## Ao plugar arte no jogo (ordem correta)

1. Salvar o arquivo em `ceifalume/arte/<subpasta>/`.
2. Rodar `godot --headless --path . --import` e **ler o log** (é onde aparece
   nome errado de arquivo).
3. Usar `res://arte/...` na cena (não caminho absoluto, não "uid" manual).
4. Exportar web e/ou APK e testar.
5. Registrar em `projetos/01-ceifalume/progresso.md` (o que entrou, o que saiu
   de lugar) e, se mudou o visual aprovado, avisar o dono antes de seguir.

Observação de versionamento: este projeto **não commita `*.import`** — o
pipeline regenera o import a cada build (`.godot/` está no `.gitignore`). Se o
dono abrir o projeto no editor e o Godot quiser commitar esses arquivos, tanto
faz: só não tirar o `.godot/` do `.gitignore`.
