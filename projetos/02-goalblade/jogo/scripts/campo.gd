extends Node2D
## O campo — agora desenhado pelo MOTOR RB (nosso motor de arte) e usado como IMAGEM.
##
## v6.2 (24/09/2026): o campo deixa de ser desenhado por código dentro do jogo. O MOTOR RB
## (ferramentas/motor-arte/campo.py) desenha tudo com qualidade de arte — grama com textura,
## desgaste, sombra das arquibancadas, torcida em fileiras, gols com rede e vinheta — e o jogo
## apenas carrega `res://arte/campo.png`. Ganho duplo: desenho melhor E menos trabalho por quadro.
##
## Se a imagem não existir (ou em teste sem tela), o desenho por código continua valendo como reserva.

const CAMINHO_ARTE := "res://arte/campo.png"

func _ready() -> void:
	z_index = -10
	if ResourceLoader.exists(CAMINHO_ARTE):
		var img: Texture2D = load(CAMINHO_ARTE)
		if img != null:
			var s := Sprite2D.new()
			s.texture = img
			s.centered = true
			s.position = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
			var escala := GB.TEX_MUNDO / float(img.get_width())   # 900 unidades de mundo
			s.scale = Vector2(escala, escala)
			add_child(s)
			return                          # a arte cuidou de tudo: não desenha por código
	queue_redraw()

func _draw() -> void:
	var escuro := Color("122216")
	draw_rect(Rect2(-4000, -4000, 8000, 8000), escuro)

	# grama em volta do campo
	draw_rect(Rect2(-90, -80, GB.F_W + 180, GB.F_H + 160), Color("2a5a2f"))

	# arquibancadas em cima e embaixo (degraus escuros com torcida)
	arquibancada(-62.0, -14.0)
	arquibancada(GB.F_H + 14.0, GB.F_H + 62.0)

	# cerca em volta do campo
	var cerca := Color("3a5040")
	var lw := 1.4
	draw_line(Vector2(-6, -6), Vector2(GB.F_W + 6, -6), cerca, lw)
	draw_line(Vector2(-6, GB.F_H + 6), Vector2(GB.F_W + 6, GB.F_H + 6), cerca, lw)
	draw_line(Vector2(-6, -6), Vector2(-6, GB.F_H + 6), cerca, lw)
	draw_line(Vector2(GB.F_W + 6, -6), Vector2(GB.F_W + 6, GB.F_H + 6), cerca, lw)
	for k in 27:
		var t := float(k) / 26.0
		var px := -6.0 + t * (GB.F_W + 12.0)
		var py := -6.0 + t * (GB.F_H + 12.0)
		draw_line(Vector2(px, -6), Vector2(px, -11), cerca, 1.6)
		draw_line(Vector2(px, GB.F_H + 6), Vector2(px, GB.F_H + 11), cerca, 1.6)
		draw_line(Vector2(-6, py), Vector2(-11, py), cerca, 1.6)
		draw_line(Vector2(GB.F_W + 6, py), Vector2(GB.F_W + 11, py), cerca, 1.6)

	# grama com listras de corte
	var faixa := GB.F_W / 10.0
	for i in 10:
		var cor := GB.GRAMA_A if i % 2 == 0 else GB.GRAMA_B
		draw_rect(Rect2(float(i) * faixa, 0.0, faixa, GB.F_H), cor)
	# textura da grama (fios) — posições fixas (sem sorteio, para não mudar a cada quadro)
	var fio_claro := Color(1, 1, 1, 0.045)
	var fio_escuro := Color(0, 0, 0, 0.05)
	for n in 900:
		var rx := fmod(float(n) * 137.508, GB.F_W)
		var ry := fmod(float(n) * 71.17, GB.F_H)
		var cor2 := fio_claro if n % 2 == 0 else fio_escuro
		draw_line(Vector2(rx, ry), Vector2(rx + (1.1 if n % 3 else -1.1), ry - 1.8), cor2, 1.0)
	# sombra suave na borda interna do campo (dá profundidade)
	draw_rect(Rect2(0, 0, GB.F_W, GB.F_H), Color(0, 0, 0, 0.10), false, 3.0)

	# marcações
	var linha := Color(1, 1, 1, 0.88)
	var sombra_l := Color(0.06, 0.15, 0.08, 0.35)
	var lw2 := 1.9
	_linha(Vector2(0, 0), Vector2(GB.F_W, 0), linha, sombra_l, lw2)
	_linha(Vector2(0, GB.F_H), Vector2(GB.F_W, GB.F_H), linha, sombra_l, lw2)
	_linha(Vector2(0, 0), Vector2(0, GB.F_H), linha, sombra_l, lw2)
	_linha(Vector2(GB.F_W, 0), Vector2(GB.F_W, GB.F_H), linha, sombra_l, lw2)
	_linha(Vector2(GB.F_W / 2.0, 0), Vector2(GB.F_W / 2.0, GB.F_H), linha, sombra_l, lw2)
	_circulo(Vector2(GB.F_W / 2.0, GB.F_H / 2.0), GB.F_W * 0.085, linha, sombra_l, lw2)
	draw_circle(Vector2(GB.F_W / 2.0, GB.F_H / 2.0), 1.6, linha)
	# áreas, pequenas áreas e marcas de pênalti
	var meio := GB.F_H / 2.0
	for lado in 2:
		var x0: float = 0.0 if lado == 0 else GB.F_W - GB.AREA_W
		var x0s: float = 0.0 if lado == 0 else GB.F_W - GB.SIX_W
		_ret( Rect2(x0, meio - GB.AREA_H / 2.0, GB.AREA_W, GB.AREA_H), linha, sombra_l, lw2)
		_ret( Rect2(x0s, meio - GB.SIX_H / 2.0, GB.SIX_W, GB.SIX_H), linha, sombra_l, lw2)
		var mx: float = GB.AREA_W * 0.72 if lado == 0 else GB.F_W - GB.AREA_W * 0.72
		draw_circle(Vector2(mx, meio), 1.8, linha)
	# arcos de canto
	var rc := GB.F_W * 0.018
	draw_arc(Vector2(0, 0), rc, 0.0, PI / 2.0, 12, linha, lw2)
	draw_arc(Vector2(GB.F_W, 0), rc, PI / 2.0, PI, 12, linha, lw2)
	draw_arc(Vector2(0, GB.F_H), rc, -PI / 2.0, 0.0, 12, linha, lw2)
	draw_arc(Vector2(GB.F_W, GB.F_H), rc, PI, PI * 1.5, 12, linha, lw2)

	# bandeirinhas
	bandeirinha(Vector2(0, 0), 1.0)
	bandeirinha(Vector2(GB.F_W, 0), 1.0)
	bandeirinha(Vector2(0, GB.F_H), -1.0)
	bandeirinha(Vector2(GB.F_W, GB.F_H), -1.0)

	# gols
	gol(0.0, true)
	gol(GB.F_W, false)

func arquibancada(y0: float, y1: float) -> void:
	# torcida: pontinhos de cores em três faixas (posições fixas)
	draw_rect(Rect2(-600, y0, GB.F_W + 1200, y1 - y0), Color("1a1e26"))
	var cores := [Color("d66054"), Color("567ac6"), Color("e4d8c0"), Color("568c64"), Color("c4ac80"), Color("3c4254")]
	for linha in 3:
		var yy: float = y0 + (y1 - y0) * (float(linha) + 0.5) / 3.0
		for k in 110:
			var xx := -560.0 + fmod(float(k) * 83.7 + float(linha) * 41.0, GB.F_W + 1120.0)
			var cor: Color = cores[(k + linha * 3) % cores.size()]
			draw_circle(Vector2(xx, yy), 3.4, cor)
	draw_rect(Rect2(-600, y0, GB.F_W + 1200, 4.0), Color("10141a"))
	draw_rect(Rect2(-600, y1 - 4.0, GB.F_W + 1200, 4.0), Color("10141a"))

func _linha(a: Vector2, b: Vector2, cor: Color, sombra: Color, w: float) -> void:
	draw_line(a + Vector2(1.2, 1.2), b + Vector2(1.2, 1.2), sombra, w)
	draw_line(a, b, cor, w)

func _circulo(c: Vector2, r: float, cor: Color, sombra: Color, w: float) -> void:
	draw_arc(c + Vector2(1.2, 1.2), r, 0.0, TAU, 64, sombra, w)
	draw_arc(c, r, 0.0, TAU, 64, cor, w)

func _ret(r: Rect2, cor: Color, sombra: Color, w: float) -> void:
	draw_rect(Rect2(r.position + Vector2(1.2, 1.2), r.size), sombra, false, w)
	draw_rect(r, cor, false, w)

func bandeirinha(pos: Vector2, cima: float) -> void:
	var h := GB.F_H * 0.05
	var lado := 1.0 if pos.x == 0.0 else -1.0
	draw_line(pos + Vector2(6, 4), pos + Vector2(6, 4 - cima * h), Color(0, 0, 0, 0.28), 2.2)
	draw_line(pos, pos + Vector2(0, -cima * h), Color(0.95, 0.95, 0.95), 1.6)
	var pts := PackedVector2Array([
		pos + Vector2(0, -cima * h),
		pos + Vector2(lado * h * 0.9, -cima * h * 0.74),
		pos + Vector2(0, -cima * h * 0.42)])
	draw_colored_polygon(pts, Color("ffd65c"))

func gol(x: float, esquerda: bool) -> void:
	var gh := GB.GOAL_H
	var d := GB.GOLO_D
	var dir := -1.0 if esquerda else 1.0
	var topo := GB.F_H / 2.0 - gh / 2.0
	var x_fundo := x + dir * d
	# fundo escuro + rede
	draw_rect(Rect2(minf(x, x_fundo), topo, d, gh), Color(0.05, 0.12, 0.07, 0.55))
	for i in range(1, 6):
		var yy := topo + float(i) * gh / 6.0
		draw_line(Vector2(x, yy + 1.4), Vector2(x_fundo, yy + 1.4), Color(0, 0, 0, 0.22), 1.0)
		draw_line(Vector2(x, yy), Vector2(x_fundo, yy), Color(1, 1, 1, 0.45), 1.4)
	for j in range(1, 5):
		var xx := x + dir * d * float(j) / 5.0
		draw_line(Vector2(xx, topo), Vector2(xx, topo + gh), Color(1, 1, 1, 0.30), 1.2)
	# moldura branca grossa (é o que faz o gol "aparecer" de longe)
	var moldura := Rect2(minf(x, x_fundo), topo, d, gh)
	draw_rect(Rect2(moldura.position + Vector2(2, 3), moldura.size), Color(0, 0, 0, 0.35), false, 4.2)
	draw_rect(moldura, Color("f4f8f4"), false, 4.2)
