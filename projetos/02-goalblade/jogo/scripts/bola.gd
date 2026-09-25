extends Node2D
## A bola: rola, desacelera sozinha, tem sombra no chão e os gomos giram conforme ela rola.
## O chute forte deixa um rastro curto — é o retorno visual do chute cheio.

var vel := Vector2.ZERO
var rot := 0.0
var dono = null            # último jogador que tocou (para creditar o autor do gol)

func _draw() -> void:
	var r := GB.RB * GB.PESSOA          # desenhada um pouco maior que o real (leitura)
	var v := vel.length()
	# sombra
	draw_set_transform(Vector2(1.4, 2.4), 0.0, Vector2(1.6, 0.9))
	draw_circle(Vector2.ZERO, 6.4, Color(0, 0, 0, 0.30))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(1.0, 1.0))
	# rastro do chute forte
	if v > 150.0:
		for i in range(1, 4):
			draw_circle(-vel * 0.010 * float(i), r * (1.0 - 0.20 * float(i)), Color(1, 1, 1, 0.16 / float(i)))
	# a bola com os gomos girando
	draw_set_transform(Vector2.ZERO, rot, Vector2.ONE)
	draw_circle(Vector2.ZERO, r, Color.WHITE)
	draw_arc(Vector2.ZERO, r, 0.0, TAU, 20, Color(0, 0, 0, 0.30), 0.6)
	draw_circle(Vector2.ZERO, r * 0.34, Color(0.13, 0.13, 0.13))
	for i in 5:
		var ang := float(i) * TAU / 5.0
		draw_circle(Vector2(cos(ang), sin(ang)) * r * 0.62, r * 0.22, Color(0.13, 0.13, 0.13))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
