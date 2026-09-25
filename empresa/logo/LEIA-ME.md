# Arquivos da marca — o que há aqui

**Status:** `logo-rb-dourada.svg` é o arquivo-mestre da logo aprovada (monograma
RB dourado sobre preto). Os PNGs são renders dele nos tamanhos que as lojas,
o itch.io e o favicon usam.

## Proveniência (importante)

- Até 2026-09-15 a logo **só existia embutida dentro do `index.html`** do
  repositório `site` — não havia arquivo nenhum. Foi resgatada de lá,
  byte a byte, sem redesenho.
- O `<svg>` do site usa a fonte `Georgia, serif`. **Nada aqui é texto do site
  modificado**: os dois `.svg` deste diretório carregam o mesmo `font-family`,
  então a letra pode variar um pouco de aparelho para aparelho (Windows tem
  Georgia; Android/este ambiente caem em outra serifada).
- Consequência: se um dia a logo for para loja/imprensa, o ideal é ter o **RB em
  contornos** (letras convertidas em caminhos, sem depender de fonte). Isso está
  anotado como ressalva na pendência §3 de `../../pendencias.md`.

## Inventário

| Arquivo | O que é | Para que serve |
|---|---|---|
| `logo-rb-dourada.svg` | mestre, com moldura e fundo | site, apresentações, qualquer tamanho |
| `logo-rb-dourada-512.png` | render 512×512 | ícone de loja (Google Play) e itch.io |
| `logo-rb-dourada-192.png` | 192×192 | ícone Android/PWA |
| `logo-rb-dourada-180.png` | 180×180 | `apple-touch-icon` |
| `logo-rb-dourada-64.png` | 64×64 | ícone pequeno, README |
| `logo-rb-dourada-32.png` | 32×32 | favicon |
| `rb-monograma-transparente.svg` | só o "RB", sem moldura e sem fundo | marca d'água, sobrepor em telas escuras |
| `rb-monograma-transparente-512.png` / `-192.png` | renders do acima | idem |

Regras de uso: fundo preto/escuro sempre que possível; sobre dourado ou claro,
usar a versão com moldura (o fundo escuro é o que garante o contraste).

## Como regerar os PNGs (chat novo precisa instalar a dependência)

```bash
pip install cairosvg pillow          # some entre sessões, reinstalar
python3 - <<'PY'
import cairosvg
svg = open('logo-rb-dourada.svg','rb').read()
for lado in (512, 192, 180, 64, 32):
    cairosvg.svg2png(bytestring=svg, write_to=f'logo-rb-dourada-{lado}.png',
                     output_width=lado, output_height=lado)
PY
```

> ⚠️ **Não usar ImageMagick (`convert`/`magick`) para renderizar SVG neste
> ambiente:** o renderizador interno dele ignora gradiente e texto e devolve um
> quadrado preto — silenciosamente, parecendo que funcionou. Já aconteceu em
> 2026-09-15. Usar `cairosvg` e **olhar o PNG resultante** antes de gravar.

## Padrão de nome usado aqui

```
<sujeito>-<descritor>-<lado ou LARGURAxALTURA>.png
ex.: logo-rb-dourada-512.png
     rb-monograma-transparente-192.png
```

- minúsculas, sem acento, sem espaço, sem "final"/"novo"/"versao2";
- o `.svg` mestre tem o **mesmo nome** do PNG, só muda a extensão;
- padrão completo de nomes (inclusive arte de jogo) em
  `../imagens-e-desenhos.md`.
