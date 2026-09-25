extends Node2D
## O goleiro — v8 (24/09/2026): passou a usar a MESMA arte dos jogadores de linha.
## Ele sai da folha "res://arte/jogadores.png", linhas 10 e 11 (o de amarelo e o de verde),
## com luvas, e mergulha com a pose de impulso. Sem desenho por código: uma imagem por quadro.

const FOLHA := "res://arte/jogadores.png"
const Q_W := 64.0
const Q_H := 72.0
const POSES := ["parado", "c0", "c1", "c2", "c3", "chute", "dividida", "comemora"]
const ESCALA := 1.26                    # mesma presença v11 dos jogadores de linha

var time := 0
var camisa := Color("ffd34d")
var luvas := Color("25c0c9")
var direcao := Vector2.LEFT
var dive := 0.0            # 0 = em pé · >0 = mergulhando (fase da animação)

var sprite: Sprite2D = null
var atlas: AtlasTexture = null
var passo := 0.0
var _pos_ant := Vector2.ZERO

func _ready() -> void:
	_pos_ant = position
	atlas = AtlasTexture.new()
	atlas.atlas = load(FOLHA)
	atlas.region = Rect2(0, 0, Q_W, Q_H)
	sprite = Sprite2D.new()
	sprite.texture = atlas
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	sprite.scale = Vector2(ESCALA, ESCALA)
	add_child(sprite)

func _draw() -> void:
	# O goleiro acompanha a mesma perspectiva do restante do elenco e entra
	# na ordem de profundidade correta quando dois corpos se sobrepõem.
	var profundidade := clampf(position.y / GB.F_H, 0.0, 1.0)
	var escala_perspectiva := ESCALA * lerpf(0.90, 1.08, profundidade)
	sprite.scale = Vector2(escala_perspectiva, escala_perspectiva)
	z_index = 10 + int(position.y)
	var v := position.distance_to(_pos_ant) * 60.0     # velocidade aproximada (para a passada)
	_pos_ant = position
	var pose := "parado"
	if dive > 0.0:
		pose = "chute"
	elif v > 6.0:
		pose = ["c0", "c1", "c2", "c3"][int(passo * 4.0) % 4]
		passo += v / 88.0 * 0.016 * 3.0
	var a := fposmod(90.0 - rad_to_deg(direcao.angle()), 360.0)
	var ca := int(round(a / 45.0)) % 8
	var ci := POSES.find(pose)
	atlas.region = Rect2(ca * 8.0 * Q_W + ci * Q_W, (10 + time) * Q_H, Q_W, Q_H)
