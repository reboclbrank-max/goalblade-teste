# MOTOR DE AUDITORIA (v0.1, 24/09/2026)

**O que é:** um auditor automático do projeto. Ele varre o repositório, **encontra falhas**, **compara com a auditoria
anterior** (o que melhorou, o que piorou, o que se repete), escreve um **relatório com o "faça isto" de cada achado** e ainda
**acumula as regras** que o projeto vai aprendendo — é assim que ele "molda" o trabalho, em vez de só reclamar.

**Regra de ouro:** achado sem correção escrita não entra. O valor está em dizer o que fazer.

## Como rodar

```bash
cd ferramentas/motor-auditoria
python3 auditar.py              # auditoria completa (varre, grava histórico e melhora as regras)
python3 auditar.py --rapido     # sem conferir links (mais rápido)
python3 auditar.py --so-relatorio
```

**Rotina:** rodar **no começo de cada sessão de trabalho** (o resultado entra no painel de pendências) e **no fecho**, antes do
commit. Assim nenhuma sessão começa sem saber o que está quebrado.

## O que ele confere (10 frentes)

| Frente | O que olha |
|---|---|
| Python | sintaxe de todos os `.py` |
| GDScript | parênteses/chaves/colchetes (fora de textos), linhas com espaço no meio de tabs |
| Segredos | token/chave dentro de código, `.gitignore` cobrindo as cópias vivas |
| Links | links dos documentos (marca os de túnel, que morrem sozinhos) |
| Imagens | PNG que não abre ou está vazio |
| Desempenho (Godot) | resolução física ligada, teto de fps, MODO LEVE, reposicionar controles, tamanho do campo/build |
| Marketing | canal sem credencial, histórico de métricas vazio ou parado, caderno de feedback |
| Consistência | documento citando arquivo que não existe; mesmo nome de arquivo com conteúdos diferentes |
| Repositório | alteração sem commit, local diferente do remoto, `.gitignore` |
| Rotina | zelador do acesso do Threads registrado, painel de pendências atualizado |

## Saídas

| Arquivo | Para quem |
|---|---|
| `RELATORIO-AUDITORIA.md` | **humano** — nota de saúde, o que corrigir, onde, e o que fazer |
| `AUDITORIA.json` | **máquina** — histórico (até 60 auditorias) e quantas vezes cada problema se repetiu |
| `MELHORIAS.md` | **memória do projeto** — cada regra nasceu de um problema real e fica escrita |

## Escala de leitura

- **Nota de saúde** = 100 − soma dos pesos (erro = 1,0 · aviso = 0,45 · nota = 0).
- **erro** = quebrado, corrigir antes de seguir · **aviso** = pode dar problema · **nota** = conferência que passou.
- **Insistem (3×+)** no relatório = problema crônico: precisa de conserto de raiz, não de remendo.

## O que ele já encontrou (primeira rodada, 24/09 — nota 75/100)

1. Ele mesmo estava errado (contava parênteses dentro de textos) → consertado na primeira execução.
2. Cópia viva de credenciais fora do `.gitignore` → corrigido.
3. `projetos/01-ceifalume/progresso.md` era citado em 24 lugares e não existia → criado como índice.
4. Documentos citavam `github.com/.../ceifalume/releases` — **404 para quem não está logado** (repositório privado): o caminho
   público do APK é o botão Download da página da itch.
5. Histórico de métricas com views/downloads repetidos → sinal de "semana sem movimento" (virou aviso, não erro).

## Próximos passos naturais (não pedidos ainda)

1. Conferir o **contraste das imagens** do motor de arte (legibilidade) e o **alinhamento dos quadros** da folha de sprites.
2. Medir **tempo de resposta dos 6 canais de marketing** numa rodada real (detectar canal caído).
3. Rodar a auditoria no **celular** (via web) para o dono ver o relatório sem depender do computador.
