class_name GB
## Constantes do GOALBLADE — versão 4 (depois do "não gostei" do dono, 24/09/2026).
##
## Mudanças desta versão: RITMO MAIS LENTO (o dono achou "muito rápido"),
## VISUAL com profundidade (sombras e luz) e CÂMERA de cima mostrando o campo inteiro
## (gol na esquerda/direita) — a escolha do dono: "o realismo da primeira com a câmera da terceira".

# --- campo society 5×5 ---
const F_W := 620.0
const F_H := 380.0
const FS := 0.62
const GOAL_H := 83.6
const AREA_W := 124.0
const AREA_H := 235.6
const SIX_W := 52.08
const SIX_H := 114.0
const GOLO_D := 17.36

# --- corpos (colisão) — MODO BOTÃO (25/09/2026): cola, drible e velocidade no máximo ---
const RP := 6.8                  # botão um pouco maior que o boneco (leitura)
const RB := 3.41
const CONTATO := RP + RB         # 10.21
const CTRL := 19.5               # cola: antes 15.19 — agora a bola não escapa (fica colada no pé)

# --- movimento — BOTÃO COM TUDO: mais rápido e com resposta instantânea ---
const MAXV := 108.0              # antes 88 — velocidade no máximo (botão corre)
const ACC := 620.0               # antes 470 — arranca no drible
const DEC := 580.0               # freia mas não escorrega
const BFRI := 0.88               # bola gruda mais (menos atrito solto) — drible curto
const BSTOP := 2.2               # só para bem devagar

# --- chute e passe — BOTÃO CHUTE FORTE + COLA ---
const SHOT_MIN := 195.0          # antes 182
const SHOT_MAX := 520.0          # antes 455 — chute forte no máximo
const CHARGE_TIME := 0.82        # carrega mais rápido (chute responsivo)
const PASS_POW := 0.48
const SHOT_RANGE := 24.0         # antes 22.32 — alcance do toque de botão
const KICK_NEAR_X := 345.0
const KICK_NEAR_Y := 445.0
const KICK_FAR_X := 255.0
const KICK_FAR_Y := 350.0

# --- câmera: campo inteiro (padrão) ou seguindo o jogador (opção) ---
const ZOOM_CAMPO := 1.72         # mostra o campo inteiro, gol na esquerda/direita
const ZOOM_JOGADOR := 3.05       # aproxima no seu jogador (opção)
const VIEW_H := 418.0            # usado no cálculo do zoom (720 / 1.72)

# --- campo como imagem (desenhado uma vez; menos trabalho para o celular) ---
const TEX_W := 1280.0            # tamanho da imagem do campo (era 2560; caiu na v6 pelo celular)
const TEX_MUNDO := 900.0         # quanto do mundo essa imagem cobre (unidades)
const TEX_ZOOM := TEX_W / TEX_MUNDO          # zoom da câmera interna
const TEX_ESCALA := TEX_MUNDO / TEX_W        # escala do desenho na tela

# --- partida ---
const MEIO_TEMPO := 180.0

# --- formação 2-1-1 + goleiro (o dono controla o atacante) ---
const FORM_X := [0.06, 0.26, 0.26, 0.48, 0.68]
const FORM_Y := [0.50, 0.32, 0.68, 0.50, 0.50]
const FUNCOES := ["gol", "def", "def", "mei", "ata"]
const INDICE_USUARIO := 4
const POR_TIME := 5

# --- visual: o boneco é desenhado maior que o real (leitura na tela, como nos jogos) ---
const PESSOA := 1.85

# --- cores ---
const COR_CAMISA := [Color("e23e37"), Color("305cd6")]
const COR_CAMISA_ESCURA := [Color("b02a26"), Color("2242a8")]
const COR_CALCAO := [Color("eef0f4"), Color("141e42")]
const COR_MEIA := [Color("d93a33"), Color("22336b")]   # meias na cor do time (leitura)
const COR_PELE := Color("e8b98e")
const COR_CABELO := Color("2c1e16")
const COR_BOTA := Color("1a1a1e")
const GRAMA_A := Color("3a7c3f")
const GRAMA_B := Color("317037")
