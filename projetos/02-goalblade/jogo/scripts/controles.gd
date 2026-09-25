extends Control
## Controles de dedo — VERSÃO 7-BOTÃO (25/09/2026) — 4 botões de ação.
##
## Pedido do dono: PASSE, DRIBLE, VELOCIDADE e CHUTE — os 4 botões de ação,
## mais a COLA automática (a bola fica colada no pé até ser roubada).
## Campo fechado com tabela: a bola não sai, quica na mureta e permite tabela.
##
## Teclado (PC): setas/WASD mover, J = passe, K = drible, L/Shift = velocidade, Espaço = chute
## + C câmera, Esc pausa, Enter start.

var jogo = null
var vetor := Vector2.ZERO
var chute_pressionado := false
var pedir_passe := false
var drible_pressionado := false
var velocidade_pressionada := false

# --- geometria (recalculada quando a tela muda de tamanho) ---
var RAIO := 96.0
var BASE_JOY := Vector2(150.0, 520.0)
var R_CHUTE := 80.0
var R_PASSE := 62.0
var R_DRIBLE := 58.0
var R_VELOCIDADE := 58.0
var POS_CHUTE := Vector2(1150.0, 540.0)
var POS_PASSE := Vector2(985.0, 600.0)
var POS_DRIBLE := Vector2(1100.0, 420.0)
var POS_VELOCIDADE := Vector2(985.0, 420.0)
var R_START := Rect2(1180.0, 330.0, 144.0, 63.0)
var R_SELECT := Rect2(900.0, 390.0, 144.0, 63.0)

const ZONA_MORTA := 0.16

var _toque_dir := -1
var _centro := Vector2.ZERO
var _toque_chute := -1
var _toque_passe := -1
var _toque_drible := -1
var _toque_velocidade := -1
var _brilho_start := 0.0
var _brilho_select := 0.0
var _sujo := true
var _layout_v := Vector2.ZERO

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	resized.connect(reposicionar)
	reposicionar.call_deferred()

# ---------------------------------------------------------------- geometria
func reposicionar() -> void:
	## Chamado quando a tela muda de tamanho E a cada quadro (é barato): o layout nunca fica preso.
	var v := get_viewport_rect().size
	_layout_v = v
	if v.x < 10.0 or v.y < 10.0:
		return
	var h := v.y                                  # deitado, a altura útil é sempre 720 unidades
	RAIO = h * 0.135
	BASE_JOY = Vector2(h * 0.20, h * 0.72)
	R_CHUTE = h * 0.105
	R_PASSE = h * 0.090
	R_DRIBLE = h * 0.082
	R_VELOCIDADE = h * 0.082
	# 4 botões em 2 colunas × 2 linhas (direita) — nada cobre o gol
	POS_CHUTE = Vector2(v.x - h * 0.13, h - h * 0.17)          # inf-dir: CHUTE (vermelho)
	POS_PASSE = Vector2(v.x - h * 0.31, h - h * 0.17)          # inf-esq: PASSE (azul)
	POS_DRIBLE = Vector2(v.x - h * 0.31, h - h * 0.34)         # sup-esq: DRIBLE (roxo)
	POS_VELOCIDADE = Vector2(v.x - h * 0.13, h - h * 0.34)     # sup-dir: VELOCIDADE (amarelo)
	# START e SELECT no alto (cantos): embaixo eles cobriam o gol e atrapalhavam a jogada
	var tam := Vector2(h * 0.20, h * 0.088)
	R_START = Rect2(Vector2(v.x - h * 0.145, h * 0.155) - tam * 0.5, tam)
	R_SELECT = Rect2(Vector2(h * 0.145, h * 0.155) - tam * 0.5, tam)
	_centro = BASE_JOY
	_sujo = true

# ---------------------------------------------------------------- entrada
func _input(evento: InputEvent) -> void:
	if evento is InputEventScreenTouch:
		if evento.pressed:
			_pressionar(evento.position, evento.index)
		else:
			_soltar(evento.index)
		return
	if evento is InputEventScreenDrag:
		if evento.index == _toque_dir:
			_arrastar(evento.position)
		return
	if evento is InputEventMouseButton and evento.button_index == MOUSE_BUTTON_LEFT:
		if evento.pressed:
			_pressionar(evento.position, -2)
		else:
			_soltar(-2)
		return
	if evento is InputEventMouseMotion and _toque_dir == -2:
		_arrastar(evento.position)

func _pressionar(pos: Vector2, idx: int) -> void:
	# START e SELECT valem SEMPRE: na tela de início, durante o jogo, na pausa e no fim.
	if R_START.has_point(pos):
		_brilho_start = 1.0
		_sujo = true
		if jogo:
			jogo.toque_na_tela()
		return
	if R_SELECT.has_point(pos):
		_brilho_select = 1.0
		_sujo = true
		if jogo:
			jogo.trocar_camera()
		return
	if jogo == null or jogo.estado != "jogando":
		_sujo = true
		return                                    # parado: quem responde ao toque é a tela do jogo
	if pos.distance_to(POS_CHUTE) < R_CHUTE:
		_toque_chute = idx
		chute_pressionado = true
		_sujo = true
		return
	if pos.distance_to(POS_PASSE) < R_PASSE:
		_toque_passe = idx
		pedir_passe = true
		_sujo = true
		return
	if pos.distance_to(POS_DRIBLE) < R_DRIBLE:
		_toque_drible = idx
		drible_pressionado = true
		_sujo = true
		return
	if pos.distance_to(POS_VELOCIDADE) < R_VELOCIDADE:
		_toque_velocidade = idx
		velocidade_pressionada = true
		_sujo = true
		return
	if pos.x < _layout_v.x * 0.5 and _toque_dir < 0:
		_toque_dir = idx
		_centro = pos
		vetor = Vector2.ZERO
		_sujo = true

func _soltar(idx: int) -> void:
	if idx == _toque_chute and _toque_chute != -1:
		_toque_chute = -1
		chute_pressionado = false
		_sujo = true
	elif idx == _toque_passe and _toque_passe != -1:
		_toque_passe = -1
		_sujo = true
	elif idx == _toque_drible and _toque_drible != -1:
		_toque_drible = -1
		drible_pressionado = false
		_sujo = true
	elif idx == _toque_velocidade and _toque_velocidade != -1:
		_toque_velocidade = -1
		velocidade_pressionada = false
		_sujo = true
	elif idx == _toque_dir and _toque_dir != -1:
		_toque_dir = -1
		vetor = Vector2.ZERO
		_centro = BASE_JOY
		_sujo = true

func _arrastar(pos: Vector2) -> void:
	var v := pos - _centro
	var l := v.length()
	if l > RAIO:
		v = v / l * RAIO
	if v.length() / RAIO < ZONA_MORTA:
		vetor = Vector2.ZERO
	else:
		vetor = v / RAIO
	_sujo = true

func _process(dt: float) -> void:
	if get_viewport_rect().size != _layout_v:
		reposicionar()                      # a tela mudou (giro, modo leve): reposiciona tudo
	# teclado PC extra: K = drible, L/Shift = velocidade (com soltura)
	if jogo != null and jogo.estado == "jogando":
		var k_now := Input.is_key_pressed(KEY_K)
		if k_now != drible_pressionado and _toque_drible == -1:
			drible_pressionado = k_now
			_sujo = true
		var v_now := Input.is_key_pressed(KEY_L) or Input.is_key_pressed(KEY_SHIFT)
		if v_now != velocidade_pressionada and _toque_velocidade == -1:
			velocidade_pressionada = v_now
			_sujo = true
		# quando o dedo está segurando, o teclado não sobrescreve — o toque manda
	_brilho_start = maxf(0.0, _brilho_start - dt * 3.0)
	_brilho_select = maxf(0.0, _brilho_select - dt * 3.0)
	var carregando: bool = jogo != null and jogo.carregando
	if carregando or _sujo or _brilho_start > 0.0 or _brilho_select > 0.0:
		_sujo = false
		queue_redraw()

# ---------------------------------------------------------------- desenho
func _draw() -> void:
	var fonte := ThemeDB.fallback_font

	# ---- direcional (esquerda) ----
	var usando := _toque_dir != -1
	var centro := _centro if usando else BASE_JOY
	draw_circle(centro + Vector2(2, 3), RAIO, Color(0, 0, 0, 0.28))
	draw_circle(centro, RAIO, Color(1, 1, 1, 0.10 if usando else 0.06))
	draw_arc(centro, RAIO, 0.0, TAU, 32, Color(1, 1, 1, 0.30 if usando else 0.18), 3.0)
	var a := RAIO * 0.15
	for dir in [Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN]:
		var c: Vector2 = centro + (dir as Vector2) * (RAIO * 0.66)
		var perp: Vector2 = Vector2(-(dir as Vector2).y, (dir as Vector2).x)
		draw_colored_polygon(PackedVector2Array([
			c + (dir as Vector2) * a,
			c - (dir as Vector2) * a * 0.6 + perp * a * 0.8,
			c - (dir as Vector2) * a * 0.6 - perp * a * 0.8]), Color(1, 1, 1, 0.34 if usando else 0.22))
	draw_circle(centro, RAIO * 0.36, Color(1, 1, 1, 0.16 if usando else 0.10))
	draw_circle(centro + vetor * RAIO * 0.55, RAIO * 0.31, Color(1, 1, 1, 0.42 if usando else 0.26))

	# ---- 4 botões de ação (2×2) ----
	# CHUTE (segurar = força) — inf-dir vermelho
	draw_circle(POS_CHUTE + Vector2(3, 4), R_CHUTE, Color(0, 0, 0, 0.30))
	draw_circle(POS_CHUTE, R_CHUTE, Color(0.84, 0.25, 0.20, 0.88 if _toque_chute != -1 or chute_pressionado else 0.72))
	draw_arc(POS_CHUTE, R_CHUTE, 0.0, TAU, 32, Color(1, 1, 1, 0.45), 2.5)
	draw_string(fonte, POS_CHUTE + Vector2(-R_CHUTE, R_CHUTE * 0.28), "CHUTE", HORIZONTAL_ALIGNMENT_CENTER,
		R_CHUTE * 2.0, int(maxf(11.0, R_CHUTE * 0.20)), Color(1, 1, 1, 0.95))
	if jogo != null and jogo.carregando:
		draw_arc(POS_CHUTE, R_CHUTE + 7.0, -PI / 2.0, -PI / 2.0 + TAU * jogo.potencia, 40,
			Color("ffe27a"), 5.0)

	# PASSE — inf-esq azul
	draw_circle(POS_PASSE + Vector2(3, 4), R_PASSE, Color(0, 0, 0, 0.30))
	draw_circle(POS_PASSE, R_PASSE, Color(0.22, 0.41, 0.86, 0.80 if _toque_passe != -1 else 0.66))
	draw_arc(POS_PASSE, R_PASSE, 0.0, TAU, 28, Color(1, 1, 1, 0.42), 2.5)
	draw_string(fonte, POS_PASSE + Vector2(-R_PASSE, R_PASSE * 0.28), "PASSE", HORIZONTAL_ALIGNMENT_CENTER,
		R_PASSE * 2.0, int(maxf(11.0, R_PASSE * 0.21)), Color(1, 1, 1, 0.92))

	# DRIBLE — sup-esq roxo (segurar = cola + zig-zag curto)
	draw_circle(POS_DRIBLE + Vector2(3, 4), R_DRIBLE, Color(0, 0, 0, 0.30))
	draw_circle(POS_DRIBLE, R_DRIBLE, Color(0.55, 0.28, 0.82, 0.82 if _toque_drible != -1 or drible_pressionado else 0.64))
	draw_arc(POS_DRIBLE, R_DRIBLE, 0.0, TAU, 26, Color(1, 1, 1, 0.42), 2.5)
	draw_string(fonte, POS_DRIBLE + Vector2(-R_DRIBLE, R_DRIBLE * 0.28), "DRIBLE", HORIZONTAL_ALIGNMENT_CENTER,
		R_DRIBLE * 2.0, int(maxf(10.0, R_DRIBLE * 0.20)), Color(1, 1, 1, 0.92))

	# VELOCIDADE — sup-dir amarelo (segurar = turbo)
	draw_circle(POS_VELOCIDADE + Vector2(3, 4), R_VELOCIDADE, Color(0, 0, 0, 0.30))
	draw_circle(POS_VELOCIDADE, R_VELOCIDADE, Color(0.88, 0.76, 0.18, 0.82 if _toque_velocidade != -1 or velocidade_pressionada else 0.64))
	draw_arc(POS_VELOCIDADE, R_VELOCIDADE, 0.0, TAU, 26, Color(1, 1, 1, 0.42), 2.5)
	draw_string(fonte, POS_VELOCIDADE + Vector2(-R_VELOCIDADE, R_VELOCIDADE * 0.28), "VELOC.", HORIZONTAL_ALIGNMENT_CENTER,
		R_VELOCIDADE * 2.0, int(maxf(10.0, R_VELOCIDADE * 0.20)), Color(1, 1, 1, 0.92))

	# ---- START e SELECT (os botões que faltavam) ----
	_botao(R_START, "START", Color(0.20, 0.62, 0.38), _brilho_start)
	_botao(R_SELECT, "SELECT", Color(0.34, 0.44, 0.78), _brilho_select)
	if jogo != null:
		var diz_start := "começar"
		match jogo.estado:
			"jogando": diz_start = "pausar"
			"pausado": diz_start = "voltar ao jogo"
			"fim": diz_start = "jogar de novo"
		_dica(R_START, diz_start)
		var cam: String = "campo inteiro" if jogo.cam_mode == "campo" else "seguir o jogador"
		_dica(R_SELECT, "câmera: " + cam)

func _botao(r: Rect2, texto: String, cor: Color, brilho: float) -> void:
	var c := cor.lerp(Color.WHITE, brilho * 0.45)
	_rr(Rect2(r.position + Vector2(3, 4), r.size), r.size.y * 0.32, Color(0, 0, 0, 0.35))
	_rr(r, r.size.y * 0.32, Color(c.r, c.g, c.b, 0.86))
	_rr_borda(r, r.size.y * 0.32, Color(1, 1, 1, 0.34), 2.0)
	draw_string(ThemeDB.fallback_font, Vector2(r.position.x, r.position.y + r.size.y * 0.68),
		texto, HORIZONTAL_ALIGNMENT_CENTER, r.size.x, int(r.size.y * 0.44), Color(1, 1, 1, 0.96))

func _dica(r: Rect2, texto: String) -> void:
	var l := r.size.x * 2.0
	var x := r.position.x + r.size.x * 0.5 - l * 0.5
	x = clampf(x, 6.0, maxf(6.0, _layout_v.x - l - 6.0))     # nunca sai da tela
	draw_string(ThemeDB.fallback_font, Vector2(x, r.position.y + r.size.y + r.size.y * 0.72),
		texto, HORIZONTAL_ALIGNMENT_CENTER, l, int(r.size.y * 0.30), Color(1, 1, 1, 0.62))

func _rr(r: Rect2, raio: float, cor: Color) -> void:
	draw_rect(Rect2(r.position.x + raio, r.position.y, r.size.x - raio * 2.0, r.size.y), cor)
	draw_rect(Rect2(r.position.x, r.position.y + raio, r.size.x, r.size.y - raio * 2.0), cor)
	draw_circle(Vector2(r.position.x + raio, r.position.y + raio), raio, cor)
	draw_circle(Vector2(r.position.x + r.size.x - raio, r.position.y + raio), raio, cor)
	draw_circle(Vector2(r.position.x + raio, r.position.y + r.size.y - raio), raio, cor)
	draw_circle(Vector2(r.position.x + r.size.x - raio, r.position.y + r.size.y - raio), raio, cor)

func _rr_borda(r: Rect2, raio: float, cor: Color, largura: float) -> void:
	var pts := PackedVector2Array()
	for canto in [Vector2(r.position.x + raio, r.position.y + raio), Vector2(r.position.x + r.size.x - raio, r.position.y + raio),
			Vector2(r.position.x + r.size.x - raio, r.position.y + r.size.y - raio), Vector2(r.position.x + raio, r.position.y + r.size.y - raio)]:
		pts.append(canto)
	pts.append(pts[0])
	draw_polyline(pts, cor, largura)
