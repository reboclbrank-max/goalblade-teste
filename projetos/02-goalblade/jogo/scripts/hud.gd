extends Control
# GOALBLADE — HUD v8 (25/09/2026) — MENU 16 SELEÇÕES COM FORÇA REAL
var jogo = null
var anuncio = ""
var anuncio_tempo = 0.0
var pontos = [0, 0]
var relogio = 180.0
var tela = "inicio"
var cam_modo = "campo"
var botao_pausa: Button
var botao_continuar: Button
var botao_camera: Button
var botao_reiniciar: Button
var botao_jogar: Button
var botao_voltar: Button
var _ultimo_s = -1.0
var _ultimo_p = [-1, -1]
var _V = Vector2(1280.0, 720.0)
var _t_fps = 0.0
var SELECOES = [
	{"id":"ARG","nome":"Argentina","forca":92,"emoji":"🇦🇷","cor":Color("7dd3fc")},
	{"id":"FRA","nome":"França","forca":90,"emoji":"🇫🇷","cor":Color("1e3a8a")},
	{"id":"BRA","nome":"Brasil","forca":89,"emoji":"🇧🇷","cor":Color("facc15")},
	{"id":"ING","nome":"Inglaterra","forca":88,"emoji":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","cor":Color("ffffff")},
	{"id":"ESP","nome":"Espanha","forca":87,"emoji":"🇪🇸","cor":Color("dc2626")},
	{"id":"POR","nome":"Portugal","forca":86,"emoji":"🇵🇹","cor":Color("064e3b")},
	{"id":"NED","nome":"Holanda","forca":85,"emoji":"🇳🇱","cor":Color("f97316")},
	{"id":"GER","nome":"Alemanha","forca":84,"emoji":"🇩🇪","cor":Color("d1d5db")},
	{"id":"BEL","nome":"Bélgica","forca":83,"emoji":"🇧🇪","cor":Color("7f1d1d")},
	{"id":"CRO","nome":"Croácia","forca":82,"emoji":"🇭🇷","cor":Color("991b1b")},
	{"id":"URU","nome":"Uruguai","forca":81,"emoji":"🇺🇾","cor":Color("e0f2fe")},
	{"id":"ITA","nome":"Itália","forca":80,"emoji":"🇮🇹","cor":Color("60a5fa")},
	{"id":"MEX","nome":"México","forca":78,"emoji":"🇲🇽","cor":Color("16a34a")},
	{"id":"USA","nome":"USA","forca":77,"emoji":"🇺🇸","cor":Color("bfdbfe")},
	{"id":"JPN","nome":"Japão","forca":76,"emoji":"🇯🇵","cor":Color("fff7ed")},
	{"id":"SEN","nome":"Senegal","forca":75,"emoji":"🇸🇳","cor":Color("84cc16")},
]
var selecao_casa: String = "BRA"
var selecao_fora: String = "ARG"
var escolhendo: int = 0
var selecao_rects: Array = []
func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	botao_pausa = _cria_botao("||", Vector2.ZERO, Vector2(56, 48), 24)
	botao_pausa.pressed.connect(func(): if jogo: jogo.toque_na_tela())
	botao_continuar = _cria_botao("continuar", Vector2.ZERO, Vector2(420, 62), 26)
	botao_continuar.pressed.connect(func(): if jogo: jogo.toque_na_tela())
	botao_camera = _cria_botao("câmera: campo inteiro", Vector2.ZERO, Vector2(420, 62), 24)
	botao_camera.pressed.connect(func(): if jogo: jogo.trocar_camera())
	botao_reiniciar = _cria_botao("recomeçar partida", Vector2.ZERO, Vector2(420, 62), 24)
	botao_reiniciar.pressed.connect(func(): if jogo: jogo.novo_jogo(true))
	botao_jogar = _cria_botao("JOGAR ▶", Vector2.ZERO, Vector2(420, 62), 28)
	botao_jogar.pressed.connect(func(): _confirmar_selecao())
	botao_voltar = _cria_botao("voltar", Vector2.ZERO, Vector2(220, 48), 20)
	botao_voltar.pressed.connect(func(): mostrar_tela("inicio"))
	resized.connect(_layout)
	_layout.call_deferred()
func _cria_botao(texto: String, pos: Vector2, tam: Vector2, fonte: int) -> Button:
	var b = Button.new()
	b.text = texto
	b.position = pos
	b.size = tam
	b.focus_mode = Control.FOCUS_NONE
	b.add_theme_font_size_override("font_size", fonte)
	b.visible = false
	var normal = StyleBoxFlat.new()
	normal.bg_color = Color(0.10, 0.14, 0.18, 0.92)
	normal.border_color = Color(1, 1, 1, 0.22)
	normal.set_border_width_all(2)
	normal.set_corner_radius_all(14)
	var hover = normal.duplicate() as StyleBoxFlat
	hover.bg_color = Color(0.16, 0.22, 0.27, 0.96)
	b.add_theme_stylebox_override("normal", normal)
	b.add_theme_stylebox_override("hover", hover)
	b.add_theme_stylebox_override("pressed", hover)
	b.add_theme_color_override("font_color", Color("eef6ef"))
	add_child(b)
	return b
func _layout() -> void:
	var v = get_viewport_rect().size
	if v.x < 10.0 or v.y < 10.0:
		v = size
	_V = v
	var h = v.y
	botao_pausa.position = Vector2(v.x - h * 0.16 - 16.0, h * 0.014 + 8.0)
	var larg = minf(h * 0.58, maxf(260.0, v.x * 0.34))
	var y0 = h * 0.60
	for i in 3:
		var b: Button = [botao_continuar, botao_camera, botao_reiniciar][i]
		b.size = Vector2(larg, h * 0.086)
		b.position = Vector2((v.x - larg) * 0.5, y0 + float(i) * (h * 0.086 + 12.0))
	botao_jogar.size = Vector2(larg, h * 0.10)
	botao_jogar.position = Vector2((v.x - larg)*0.5, h * 0.86)
	botao_voltar.position = Vector2(16, 16)
	_calcular_grid_selecao()
	queue_redraw()
func _calcular_grid_selecao():
	selecao_rects.clear()
	var v = _V
	var h = v.y
	var cols = 4
	var rows = 4
	var grid_w = minf(820.0 * h/720.0, v.x * 0.82)
	var cell_w = grid_w / float(cols)
	var cell_h = 78.0 * h/720.0
	var gx = (v.x - grid_w)*0.5
	var gy = h * 0.20
	for i in 16:
		var c = i % cols
		var r = i / cols
		var rect = Rect2(gx + c*cell_w + 4, gy + r*cell_h + 4, cell_w - 8, cell_h - 8)
		selecao_rects.append(rect)
func _process(dt: float) -> void:
	if get_viewport_rect().size != _V:
		_layout()
	_t_fps += dt
	if anuncio_tempo > 0.0:
		anuncio_tempo -= dt
		queue_redraw()
	elif tela != "nenhuma" or _t_fps > 1.0:
		_t_fps = 0.0
		queue_redraw()
func _draw() -> void:
	var fonte = ThemeDB.fallback_font
	var v = _V
	var h = v.y
	var k = h / 720.0
	var bw = minf(720.0 * k, v.x * 0.62)
	var bh = 62.0 * k
	var bx = (v.x - bw) * 0.5
	var by = 10.0 * k
	_rr(Rect2(bx + 3, by + 4, bw, bh), 16.0 * k, Color(0, 0, 0, 0.45))
	_rr(Rect2(bx, by, bw, bh), 16.0 * k, Color(0.06, 0.09, 0.11, 0.92))
	_rr_borda(Rect2(bx, by, bw, bh), 16.0 * k, Color(1, 1, 1, 0.16), 2.0)
	var selA = _por_id(selecao_casa)
	var selB = _por_id(selecao_fora)
	_rr(Rect2(bx + 22 * k, by + 17 * k, 44 * k, 28 * k), 7.0 * k, selA["cor"])
	_rr(Rect2(bx + bw - 66 * k, by + 17 * k, 44 * k, 28 * k), 7.0 * k, selB["cor"])
	draw_string(fonte, Vector2(bx + 76 * k, by + 43 * k), selA["id"], HORIZONTAL_ALIGNMENT_CENTER, 66.0 * k, int(13 * k), Color(0.80, 0.88, 0.83))
	draw_string(fonte, Vector2(bx + bw - 142 * k, by + 43 * k), selB["id"], HORIZONTAL_ALIGNMENT_CENTER, 66.0 * k, int(13 * k), Color(0.80, 0.88, 0.83))
	draw_string(fonte, Vector2(bx + 152 * k, by + 46 * k), str(pontos[0]), HORIZONTAL_ALIGNMENT_CENTER, 60.0 * k, int(36 * k), Color.WHITE)
	draw_string(fonte, Vector2(bx + bw - 212 * k, by + 46 * k), str(pontos[1]), HORIZONTAL_ALIGNMENT_CENTER, 60.0 * k, int(36 * k), Color.WHITE)
	var cx = bx + bw * 0.5
	var cy = by + bh * 0.5
	draw_circle(Vector2(cx, cy), 24.0 * k, Color(0.11, 0.14, 0.16))
	draw_arc(Vector2(cx, cy), 24.0 * k, 0.0, TAU, 32, Color(1, 1, 1, 0.16), 3.0)
	draw_arc(Vector2(cx, cy), 24.0 * k, -PI / 2.0, -PI / 2.0 + TAU * clampf(relogio / GB.MEIO_TEMPO, 0.0, 1.0), 40, Color(0.55, 0.90, 0.60), 6.0)
	var seg = int(ceil(relogio))
	draw_string(fonte, Vector2(cx - 34 * k, cy + 8 * k), "%d:%02d" % [seg / 60, seg % 60], HORIZONTAL_ALIGNMENT_CENTER, 68.0 * k, int(20 * k), Color(0.94, 0.97, 0.94))
	if jogo != null:
		draw_string(fonte, Vector2(8.0, 17.0 * k), jogo.resumo_desempenho(), HORIZONTAL_ALIGNMENT_LEFT, v.x * 0.40, int(maxf(10.0, 13.0 * k)), Color(1, 1, 1, 0.50))
	if anuncio_tempo > 0.0:
		_rr(Rect2(v.x * 0.5 - 300 * k, 150 * k, 600 * k, 96 * k), 20.0 * k, Color(0, 0, 0, 0.42))
		draw_string(fonte, Vector2(v.x * 0.5 - 300 * k, 222 * k), anuncio, HORIZONTAL_ALIGNMENT_CENTER, 600.0 * k, int(56 * k), Color("ffe27a"))
	if tela != "nenhuma":
		draw_rect(Rect2(Vector2.ZERO, v), Color(0.02, 0.05, 0.03, 0.92))
		var cw = minf(980.0 * k, v.x * 0.94)
		var cx2 = (v.x - cw) * 0.5
		if tela == "inicio":
			draw_string(fonte, Vector2(cx2, 110 * k), "GOALBLADE", HORIZONTAL_ALIGNMENT_CENTER, cw, int(64 * k), Color("ffe27a"))
			_texto_linhas(fonte, [
				"COPA GOALBLADE  ·  5 × 5   ·   16 seleções",
				"ESCOLHA DUAS SELEÇÕES E DISPUTE COM FORÇA REAL",
				"",
				"BOTÃO COM BANDEIRA  ·  COLA + DRIBLE + VELOCIDADE + CHUTE",
				"CAMPO FECHADO COM TABELA  ·  3 MINUTOS",
			], Vector2(cx2, 155 * k), cw, int(20 * k))
			var preview_y = 250 * k
			_desenhar_preview(fonte, selA, selB, v, preview_y, k)
			draw_string(fonte, Vector2(cx2, 620 * k), "toque em ESCOLHER SELEÇÕES para trocar times", HORIZONTAL_ALIGNMENT_CENTER, cw, int(22 * k), Color(0.92, 0.98, 0.94))
			draw_string(fonte, Vector2(cx2, 650 * k), "força: %s %d  ×  %s %d  — IA difícil sem aleatório" % [selA["id"], selA["forca"], selB["id"], selB["forca"]], HORIZONTAL_ALIGNMENT_CENTER, cw, int(16 * k), Color(0.72, 0.86, 0.78))
		elif tela == "selecao":
			draw_string(fonte, Vector2(cx2, 60 * k), "ESCOLHA AS SELEÇÕES", HORIZONTAL_ALIGNMENT_CENTER, cw, int(42 * k), Color("ffe27a"))
			var sub = "CASA: %s  ×  FORA: %s   — toque para trocar" % [_por_id(selecao_casa)["nome"], _por_id(selecao_fora)["nome"]]
			draw_string(fonte, Vector2(cx2, 95 * k), sub, HORIZONTAL_ALIGNMENT_CENTER, cw, int(18 * k), Color(0.90, 0.96, 0.92))
			var hint = "1º toque escolhe CASA (vermelho), 2º escolhe FORA (azul)" if escolhendo==0 else "agora escolha o ADVERSÁRIO"
			draw_string(fonte, Vector2(cx2, 118 * k), hint, HORIZONTAL_ALIGNMENT_CENTER, cw, int(15 * k), Color(0.75, 0.85, 0.80))
			_desenhar_grid_selecao(fonte, k)
			var fa = _por_id(selecao_casa)["forca"]
			var fb = _por_id(selecao_fora)["forca"]
			var diff = fa - fb
			var msg = "equilíbrio" if abs(diff) <=2 else ("favorito: %s +%d" % [selecao_casa if diff>0 else selecao_fora, abs(diff)])
			draw_string(fonte, Vector2(cx2, 590 * k), "%s %d  ×  %d %s   ·  %s" % [selecao_casa, fa, fb, selecao_fora, msg], HORIZONTAL_ALIGNMENT_CENTER, cw, int(18 * k), Color(0.82, 0.92, 0.86))
		elif tela == "pausa":
			draw_string(fonte, Vector2(cx2, 110 * k), "PAUSA", HORIZONTAL_ALIGNMENT_CENTER, cw, int(60 * k), Color("ffe27a"))
			draw_string(fonte, Vector2(cx2, 176 * k), "%s %d × %d %s   ·   %d:%02d" % [selecao_casa, pontos[0], pontos[1], selecao_fora, int(relogio) / 60, int(relogio) % 60], HORIZONTAL_ALIGNMENT_CENTER, cw, int(26 * k), Color(0.90, 0.96, 0.92))
			draw_string(fonte, Vector2(cx2, 236 * k), "START volta ao jogo   ·   toque fora dos botões também volta", HORIZONTAL_ALIGNMENT_CENTER, cw, int(16 * k), Color(0.72, 0.80, 0.75))
			if jogo != null:
				draw_string(fonte, Vector2(cx2, 690 * k), jogo.diagnostico(), HORIZONTAL_ALIGNMENT_CENTER, cw, int(14 * k), Color(1, 1, 1, 0.60))
		elif tela == "fim":
			var resultado = "EMPATE"
			if pontos[0] > pontos[1]: resultado = "VITÓRIA %s!" % selecao_casa
			elif pontos[0] < pontos[1]: resultado = "VITÓRIA %s!" % selecao_fora
			draw_string(fonte, Vector2(cx2, 120 * k), resultado, HORIZONTAL_ALIGNMENT_CENTER, cw, int(52 * k), Color("ffe27a"))
			draw_string(fonte, Vector2(cx2, 210 * k), "%s %d × %d %s" % [selecao_casa, pontos[0], pontos[1], selecao_fora], HORIZONTAL_ALIGNMENT_CENTER, cw, int(42 * k), Color(0.94, 0.97, 0.94))
			draw_string(fonte, Vector2(cx2, 290 * k), "toque na tela para escolher novas seleções", HORIZONTAL_ALIGNMENT_CENTER, cw, int(22 * k), Color(0.85, 0.92, 0.87))
	if v.y > v.x * 1.05:
		draw_rect(Rect2(Vector2.ZERO, v), Color(0.02, 0.05, 0.03, 0.94))
		draw_string(fonte, Vector2(0, v.y * 0.45), "GIRE O CELULAR", HORIZONTAL_ALIGNMENT_CENTER, v.x, int(maxf(28.0, v.x * 0.075)), Color("ffe27a"))
		draw_string(fonte, Vector2(0, v.y * 0.52), "o jogo é deitado (paisagem)", HORIZONTAL_ALIGNMENT_CENTER, v.x, int(maxf(16.0, v.x * 0.040)), Color(0.88, 0.94, 0.90))
func _desenhar_preview(fonte, selA, selB, v, y, k):
	var cw = 320.0 * k
	var gap = 40.0 * k
	var x0 = v.x*0.5 - cw - gap*0.5
	var x1 = v.x*0.5 + gap*0.5
	for idx in 2:
		var sel = selA if idx==0 else selB
		var x = x0 if idx==0 else x1
		_rr(Rect2(x, y, cw, 130*k), 18*k, Color(0.08,0.11,0.14,0.96))
		_rr_borda(Rect2(x, y, cw, 130*k), 18*k, Color(1,1,1,0.14), 2)
		draw_string(fonte, Vector2(x, y+38*k), sel["emoji"], HORIZONTAL_ALIGNMENT_CENTER, cw, int(42*k), Color.WHITE)
		draw_string(fonte, Vector2(x, y+78*k), sel["nome"].to_upper(), HORIZONTAL_ALIGNMENT_CENTER, cw, int(18*k), Color(0.92,0.98,0.94))
		draw_string(fonte, Vector2(x, y+102*k), "FORÇA %d" % sel["forca"], HORIZONTAL_ALIGNMENT_CENTER, cw, int(16*k), Color("ffe27a"))
		var bw = cw*0.72
		var bh = 10*k
		var bx = x + (cw-bw)*0.5
		var by2 = y + 114*k
		_rr(Rect2(bx, by2, bw, bh), bh*0.5, Color(0,0,0,0.55))
		_rr(Rect2(bx, by2, bw * (float(sel["forca"]-70)/25.0), bh), bh*0.5, sel["cor"] if sel["forca"]>80 else Color(0.9,0.7,0.3))
func _desenhar_grid_selecao(fonte, k):
	for i in SELECOES.size():
		if i >= selecao_rects.size(): break
		var sel = SELECOES[i]
		var r: Rect2 = selecao_rects[i]
		var sel_id = sel["id"]
		var is_casa = sel_id == selecao_casa
		var is_fora = sel_id == selecao_fora
		var bg = Color(0.10,0.14,0.18,0.88)
		var borda = Color(1,1,1,0.14)
		if is_casa:
			bg = Color(0.24,0.14,0.14,0.96); borda = Color("e23e37")
		elif is_fora:
			bg = Color(0.12,0.16,0.24,0.96); borda = Color("2f5fd8")
		_rr(r, 14*k, bg)
		_rr_borda(r, 14*k, borda, 3 if is_casa or is_fora else 2)
		draw_string(fonte, Vector2(r.position.x, r.position.y + 30*k), sel["emoji"], HORIZONTAL_ALIGNMENT_CENTER, r.size.x, int(28*k), Color.WHITE)
		draw_string(fonte, Vector2(r.position.x, r.position.y + 52*k), sel["nome"], HORIZONTAL_ALIGNMENT_CENTER, r.size.x, int(13*k), Color(0.90,0.96,0.92))
		var bw = r.size.x * 0.74
		var bh = 7*k
		var bx = r.position.x + (r.size.x - bw)*0.5
		var by2 = r.position.y + r.size.y - 20*k
		_rr(Rect2(bx, by2, bw, bh), bh*0.5, Color(0,0,0,0.50))
		var pct = clampf(float(sel["forca"]-70)/25.0, 0,1)
		_rr(Rect2(bx, by2, bw*pct, bh), bh*0.5, sel["cor"])
		draw_string(fonte, Vector2(r.position.x, by2 - 4*k), str(sel["forca"]), HORIZONTAL_ALIGNMENT_CENTER, r.size.x, int(11*k), Color("ffe27a"))
		if is_casa or is_fora:
			var tag = "CASA" if is_casa else "FORA"
			_rr(Rect2(r.position.x + r.size.x - 46*k, r.position.y + 4*k, 42*k, 14*k), 6*k, borda)
			draw_string(fonte, Vector2(r.position.x + r.size.x - 46*k, r.position.y + 15*k), tag, HORIZONTAL_ALIGNMENT_CENTER, 42*k, int(8*k), Color.WHITE)
func _por_id(id: String) -> Dictionary:
	for s in SELECOES:
		if s["id"]==id: return s
	return SELECOES[0]
func _texto_linhas(fonte: Font, linhas: Array, pos: Vector2, largura: float, tam: int) -> void:
	for i in linhas.size():
		draw_string(fonte, Vector2(pos.x, pos.y + float(i) * float(tam + 8)), str(linhas[i]), HORIZONTAL_ALIGNMENT_CENTER, largura, tam, Color(0.92, 0.96, 0.93))
func _rr(r: Rect2, raio: float, cor: Color) -> void:
	draw_rect(Rect2(r.position.x + raio, r.position.y, r.size.x - raio * 2.0, r.size.y), cor)
	draw_rect(Rect2(r.position.x, r.position.y + raio, r.size.x, r.size.y - raio * 2.0), cor)
	draw_circle(Vector2(r.position.x + raio, r.position.y + raio), raio, cor)
	draw_circle(Vector2(r.position.x + r.size.x - raio, r.position.y + raio), raio, cor)
	draw_circle(Vector2(r.position.x + raio, r.position.y + r.size.y - raio), raio, cor)
	draw_circle(Vector2(r.position.x + r.size.x - raio, r.position.y + r.size.y - raio), raio, cor)
func _rr_borda(r: Rect2, raio: float, cor: Color, largura: float) -> void:
	var pts = PackedVector2Array()
	for canto in [Vector2(r.position.x + raio, r.position.y + raio), Vector2(r.position.x + r.size.x - raio, r.position.y + raio), Vector2(r.position.x + r.size.x - raio, r.position.y + r.size.y - raio), Vector2(r.position.x + raio, r.position.y + r.size.y - raio)]:
		pts.append(canto)
	pts.append(pts[0])
	draw_polyline(pts, cor, largura)
func atualizar(p: Array, r: float) -> void:
	pontos = [p[0], p[1]]
	relogio = r
	var s = floorf(r)
	if s != _ultimo_s or _ultimo_p[0] != p[0] or _ultimo_p[1] != p[1]:
		_ultimo_s = s
		_ultimo_p = [p[0], p[1]]
		queue_redraw()
func mostrar_anuncio(texto: String) -> void:
	anuncio = texto
	anuncio_tempo = 1.5
	queue_redraw()
func definir_camera(modo: String) -> void:
	cam_modo = modo
	botao_camera.text = "câmera: " + ("campo inteiro" if modo == "campo" else "seguir o jogador")
	queue_redraw()
func mostrar_tela(qual: String) -> void:
	tela = qual
	botao_pausa.visible = qual == "nenhuma"
	botao_continuar.visible = qual == "pausa" or qual == "fim"
	botao_camera.visible = qual == "pausa"
	botao_reiniciar.visible = qual == "pausa" or qual == "fim"
	var is_inicio = qual == "inicio"
	var is_selecao = qual == "selecao"
	botao_jogar.visible = is_inicio
	botao_voltar.visible = is_selecao
	if is_inicio:
		botao_continuar.visible = true
		botao_continuar.text = "ESCOLHER SELEÇÕES"
		var v = _V
		var h = v.y
		var larg = minf(h * 0.58, maxf(260.0, v.x * 0.34))
		botao_continuar.size = Vector2(larg, h * 0.086)
		botao_continuar.position = Vector2((v.x - larg)*0.5, h * 0.60)
		botao_camera.visible = false
		botao_reiniciar.visible = false
	elif is_selecao:
		botao_continuar.visible = false
		botao_camera.visible = false
		botao_reiniciar.visible = false
	queue_redraw()
func esconder_tela() -> void:
	mostrar_tela("nenhuma")
	anuncio_tempo = 0.0
	_ultimo_s = -1.0
func _confirmar_selecao():
	if jogo:
		jogo.aplicar_selecoes(selecao_casa, selecao_fora)
		jogo.comecar_partida()
func _input(evento: InputEvent) -> void:
	if tela == "selecao":
		var pos = Vector2.ZERO
		var tocou = false
		if evento is InputEventScreenTouch and evento.pressed:
			pos = evento.position; tocou = true
		elif evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
			pos = evento.position; tocou = true
		if tocou:
			for b in [botao_jogar, botao_voltar]:
				if b.visible and Rect2(b.position,b.size).has_point(pos):
					return
			for i in selecao_rects.size():
				if selecao_rects[i].has_point(pos):
					var id = SELECOES[i]["id"]
					if escolhendo==0:
						selecao_casa = id
						if selecao_casa == selecao_fora:
							for s in SELECOES:
								if s["id"] != selecao_casa:
									selecao_fora = s["id"]; break
						escolhendo = 1
					else:
						if id != selecao_casa:
							selecao_fora = id
						escolhendo = 0
					_calcular_grid_selecao()
					queue_redraw()
					return
			return
	if tela == "inicio":
		var pos2 = Vector2.ZERO
		var tocou2 = false
		if evento is InputEventScreenTouch and evento.pressed:
			pos2 = evento.position; tocou2=true
		elif evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
			pos2 = evento.position; tocou2=true
		if evento is InputEventKey and evento.pressed and not evento.echo:
			if evento.keycode == KEY_ENTER or evento.keycode == KEY_SPACE:
				mostrar_tela("selecao"); return
		if tocou2:
			for b in [botao_jogar, botao_continuar]:
				if b.visible and Rect2(b.position,b.size).has_point(pos2):
					if b==botao_continuar:
						mostrar_tela("selecao")
					return
			return
	if tela != "nenhuma" and tela != "selecao" and tela != "inicio":
		if evento is InputEventKey and evento.pressed and not evento.echo:
			if jogo: jogo.toque_na_tela(); return
		var pos = Vector2.ZERO
		var tocou = false
		if evento is InputEventScreenTouch and evento.pressed:
			pos = evento.position; tocou=true
		elif evento is InputEventMouseButton and evento.pressed:
			pos = evento.position; tocou=true
		if not tocou: return
		for b in [botao_pausa, botao_continuar, botao_camera, botao_reiniciar, botao_jogar]:
			if b.visible and Rect2(b.position,b.size).has_point(pos):
				return
		if jogo: jogo.toque_na_tela()
	elif tela == "nenhuma":
		return
