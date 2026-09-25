# `ferramentas/` — o motor de verificação, versionado

Estas são as ferramentas que o assistente usa para **medir** em vez de deduzir.
Moram na base de propósito: o sandbox do assistente só preserva `/home/user`, e
`~/tools` pode sumir entre sessões — aqui elas ficam no git e sobrevivem.

| Ferramenta | O que faz | Como usar |
|---|---|---|
| `acender-motor.sh` | religa o ambiente inteiro (apt, Godot 4.5.2, puppeteer, índice da base, templates de export) e conserta os remotos do git que somem por turno | `bash ferramentas/acender-motor.sh` (ou copia para `~/tools/`) |
| `indexar-base.py` / `buscar-na-base.py` | índice FTS5 da base + código, com ranking | `python3 buscar-na-base.py "versionCode"` |
| `medir-som.py` | pico, RMS, LUFS e duração de áudio; alvo por arquivo ou por mixagem | `python3 medir-som.py arte/som/*.wav` · `MEDIR_MODO=mix medir-som.py captura.wav` |
| `montar-trilha.py` | monta a trilha do trailer a partir do diário de sons da gravação (música + efeitos do jogo no tempo certo) | `python3 montar-trilha.py /home/user/trailer` |
| `compare-frames.sh` | diff de pixels com tolerância (mesmo cenário, mesmo quadro) | `compare-frames.sh antes.png depois.png 12` |
| `medidor-encaixe.js` | o quadro do jogo cabe inteiro? em 3 perfis de celular/desktop | servidor local + `node medidor-encaixe.js` |
| `medidor-pagina.js` | a página publicada: motor iniciado, erros de JS, pedidos quebrados | idem |
| `teste-toque2.js` | toque no canvas escalado chega no lugar certo (com controle sem-toque) | idem |
| `teste-audio-web.js` | o `AudioContext` do jogo fica suspenso no navegador? | idem |
| `teste-4g.js` | rede limitada via CDP: quanto tempo até o primeiro quadro | idem |
| `compara-motores.js` | dois builds do Godot, mesma máquina, mesma régua | idem |
| `sonda-aparelho.js` | o que um painel de diagnosticaria no celular do dono | idem |
| `preparar-godot.sh` / `baixar-godot-novo.sh` | baixam o motor do jogo (4.5.2) e um segundo motor ao lado (4.7.2) | `bash ...` |

Regra de sincronia: ao fim de cada sessão, `cp -r ~/tools/* base/ferramentas/ && git commit`,
porque a ferramenta que só existe no sandbox não existe para o próximo chat.
