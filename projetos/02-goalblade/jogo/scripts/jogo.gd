extends Node2D
## GOALBLADE — o jogo. Versão 6 (24/09/2026) — depois de o dono testar no celular e dizer:
## "ainda tá travando ao extremo, não tá rodando liso nunca, e o controle tá horrível,
##  sem start e select sem funcionalidade".
##
## O que muda na v6 (celular liso):
##  · o jogo NÃO desenha mais na resolução física da tela (era até 3× mais pixels do que precisa);
##  · teto de 60 quadros por segundo (telas de 90/120 Hz dobravam o trabalho à toa);
##  · imagem do campo caiu de 2.560×1.440 para 1.280×720 (menos memória e menos enchimento);
##  · "MODO LEVE" automático: se os quadros caírem, o jogo reduz a resolução sozinho e avisa na tela;
##  · linha de desempenho no canto (fps + motor de vídeo do aparelho) para o dono informar o número;
##  · controles refeitos (START e SELECT com função, botões pelo tamanho da tela) — ver controles.gd.
##
## (A v4, logo abaixo, é o que valia antes — o texto fica como histórico do que já foi corrigido.)
##
## O que mudou na versão 4, ponto por ponto da reclamação do dono:
##  · "não é 2D, tá mais pra 1D"      -> CÂMERA DE CIMA mostrando o campo inteiro (gol na esquerda/direita),
##                                       com arquibancada, cerca e sombra nos bonecos (profundidade de verdade);
##  · "jogo muito rápido"              -> RITMO 30% mais lento (constantes em consts.gd) e chute com mais carga;
##  · "sem estratégia"                 -> goleiros que defendem de verdade (partidas de 1 a 4 gols),
##                                       IA que prefere o PASSE, apoia com largura e só chuta em boa posição;
##  · "jogo trava muito"               -> desenho sem polígonos montados por quadro, listas reaproveitadas
##                                       e ordenação sem criar objetos novos (o que pesava no celular);
##  · "desorganizado"                  -> HUD limpa (placar + relógio + pausa) e botões grandes e alinhados;
##  · "sem bonecos reais"              -> bonecos desenhados de verdade, maiores para leitura, com sombra.

const C_CAMPO = preload("res://scripts/campo.gd")
const C_BOLA = preload("res://scripts/bola.gd")
const C_JOGADOR = preload("res://scripts/jogador.gd")
const C_GOLEIRO = preload("res://scripts/goleiro.gd")
const C_HUD = preload("res://scripts/hud.gd")
const C_CONTROLES = preload("res://scripts/controles.gd")

var campo
var campo_vp: SubViewport
var campo_textura: Sprite2D
var quadros_visuais = 0
var bola
var camada: Node2D
var cam: Camera2D
var hud
var controles
var camada_hud: CanvasLayer

var times = [[], []]
var todos = []                    # os dez jogadores numa lista só (reaproveitada)
var usuario
var cacadores = [null, null]
var gols = [null, null]
var desenhos_goleiro = [null, null]   # o goleiro desenhado na arte do campo (v6.3)

var estado = "inicio"             # inicio | jogando | pausado | fim
var pontos = [0, 0]
var relogio = GB.MEIO_TEMPO
var congelar = 0.0
var fim = false
var proximo = 0
var posse = -1
var cam_mode = "campo"            # "campo" (padrão, escolha do dono) | "jogador"

var carregando = false
var potencia = 0.0

# --- modo de teste ---
var modo_teste = false
var auto_teste = false
var tempo_teste = 60.0
var tempo_jogo = 0.0
var t_parado = 0.0
var t_travamentos = 0
var t_anomalias = 0
var t_ultima = Vector2.ZERO
var t_posse = [0.0, 0.0]
var t_frames = 0
var t_cpu_us = 0
var t_gols = [0, 0]
var t_etapa = 0
var foto_path = ""
var foto_quadro = 90
var foto_feita = false
var t_pausa_quadros = 0
var _j_antes = false

# --- desempenho (v6) ---
var modo_leve = 0                 # 0 = normal · 1 = leve · 2 = leve forte
var sem_leve = false              # --sem-leve: desliga o ajuste automático (testes)
var fps_agora = 0.0
var _vida_app = 0.0               # segundos desde a abertura (os primeiros não contam)
var _fps_baixo = 0.0
var _fps_alto = 0.0
var _gpu = ""
var foto_tela = ""                # --foto-tela=inicio|pausa (foto dessas telas)
var t_pfisicos = 0                # quadros físicos desde a abertura (a foto usa este contador)

func _ready() -> void:
	var args = OS.get_cmdline_args() + OS.get_cmdline_user_args()
	modo_teste = "--teste" in args
	auto_teste = "--auto" in args
	for a in args:
		if a.begins_with("--tempo="):
			tempo_teste = float(a.split("=")[1])
		elif a.begins_with("--foto="):
			foto_path = a.split("=")[1]
		elif a.begins_with("--foto-quadro="):
			foto_quadro = int(a.split("=")[1])
		elif a.begins_with("--camera="):
			cam_mode = a.split("=")[1]
		elif a.begins_with("--foto-tela="):
			foto_tela = a.split("=")[1]
	Engine.max_fps = 60            # teto: em telas de 90/120 Hz o jogo desenhava 2× à toa
	if "--sem-leve" in args:
		sem_leve = true            # usado só nos testes do assistente
	_montar()
	if auto_teste:
		usuario.eh_usuario = false
	novo_jogo(modo_teste)
	if foto_tela == "inicio":
		novo_jogo(false)
	elif foto_tela == "pausa":
		novo_jogo(true)
		pausar()

func _montar() -> void:
	campo = C_CAMPO.new()
	var sem_tela = DisplayServer.get_name() == "headless"
	if ResourceLoader.exists("res://arte/campo.png"):
		# v6.2: o campo é uma IMAGEM feita pelo MOTOR RB — não precisa mais da imagem intermediária
		# (SubViewport). Menos memória, menos trabalho por quadro e desenho muito melhor.
		add_child(campo)
		var fundo_camada2 = CanvasLayer.new()
		fundo_camada2.layer = -1
		var fundo2 = ColorRect.new()
		fundo2.color = Color("122216")
		fundo2.size = Vector2(1280, 720)
		fundo_camada2.add_child(fundo2)
		add_child(fundo_camada2)
	elif sem_tela:
		add_child(campo)
	else:
		# DESEMPENHO (a queixa "jogo trava muito"): o campo é desenhado UMA vez
		# numa imagem (1.280×720 — caiu de 2.560×1.440 na v6) e depois aparece como
		# UMA imagem por quadro, em vez de ~2.500 traços de grama/torcida/cerca.
		campo_vp = SubViewport.new()
		campo_vp.size = Vector2i(int(GB.TEX_W), int(GB.TEX_W * 0.5625))
		campo_vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		campo_vp.disable_3d = true
		add_child(campo_vp)
		campo_vp.add_child(campo)
		var cam_campo = Camera2D.new()
		cam_campo.zoom = Vector2(GB.TEX_ZOOM, GB.TEX_ZOOM)
		cam_campo.position = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
		cam_campo.enabled = true
		campo_vp.add_child(cam_campo)
		campo_textura = Sprite2D.new()
		campo_textura.texture = campo_vp.get_texture()
		campo_textura.centered = true
		campo_textura.position = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
		campo_textura.scale = Vector2(GB.TEX_ESCALA, GB.TEX_ESCALA)
		campo_textura.z_index = -10
		add_child(campo_textura)
		# fundo (o que aparece fora do campo, quando a câmera aproxima)
		var fundo_camada = CanvasLayer.new()
		fundo_camada.layer = -1
		var fundo = ColorRect.new()
		fundo.color = Color("122216")
		fundo.position = Vector2.ZERO
		fundo.size = Vector2(1280, 720)
		fundo_camada.add_child(fundo)
		add_child(fundo_camada)
	camada = Node2D.new()
	camada.name = "Jogadores"
	add_child(camada)
	bola = C_BOLA.new()
	add_child(bola)
	cam = Camera2D.new()
	cam.zoom = Vector2(GB.ZOOM_CAMPO, GB.ZOOM_CAMPO)
	cam.enabled = true
	cam.position = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
	add_child(cam)
	camada_hud = CanvasLayer.new()
	camada_hud.layer = 2
	add_child(camada_hud)
	hud = C_HUD.new()
	hud.jogo = self
	camada_hud.add_child(hud)
	controles = C_CONTROLES.new()
	controles.jogo = self
	camada_hud.add_child(controles)
	hud.definir_camera(cam_mode)
	for t in 2:
		for i in GB.POR_TIME:
			var p = C_JOGADOR.new()
			p.jogo = self
			p.time = t
			p.numero = i + 1
			p.funcao = GB.FUNCOES[i]
			p.eh_usuario = (t == 0 and i == GB.INDICE_USUARIO)
			var lx: float = GB.FORM_X[i] * GB.F_W
			var ly: float = GB.FORM_Y[i] * GB.F_H
			if t == 1:
				lx = GB.F_W - lx
			p.casa = Vector2(lx, ly)
			p.position = p.casa
			camada.add_child(p)
			times[t].append(p)
			todos.append(p)
			if p.eh_usuario:
				usuario = p
			if p.funcao == "gol":
				gols[t] = p
				var g = C_GOLEIRO.new()
				g.time = t
				g.camisa = Color("ffd34d") if t == 0 else Color("7ef2a8")
				g.position = p.position
				g.z_index = 1
				camada.add_child(g)
				desenhos_goleiro[t] = g

# ------------------------------------------------------------------ partida
func novo_jogo(direto: bool = false) -> void:
	pontos = [0, 0]
	relogio = tempo_teste if modo_teste else GB.MEIO_TEMPO
	fim = false
	congelar = 0.0
	tempo_jogo = 0.0
	t_travamentos = 0
	t_anomalias = 0
	t_posse = [0.0, 0.0]
	t_frames = 0
	t_cpu_us = 0
	t_gols = [0, 0]
	t_borda = 0.0
	carregando = false
	potencia = 0.0
	hud.atualizar(pontos, relogio)
	if direto:
		estado = "jogando"
		hud.esconder_tela()
		if modo_teste:
			t_etapa = 3
	else:
		estado = "inicio"
		hud.mostrar_tela("inicio")
	saida_de_bola(0)

var selecao_casa_id: String = "BRA"
var selecao_fora_id: String = "ARG"

func aplicar_selecoes(casa: String, fora: String) -> void:
	selecao_casa_id = casa
	selecao_fora_id = fora
	hud.selecao_casa = casa
	hud.selecao_fora = fora

func comecar_partida() -> void:
	estado = "jogando"
	hud.esconder_tela()

func pausar() -> void:
	if estado == "jogando":
		estado = "pausado"
		carregando = false
		potencia = 0.0
		controles.chute_pressionado = false
		hud.mostrar_tela("pausa")

func retomar() -> void:
	if estado == "pausado":
		estado = "jogando"
		hud.esconder_tela()

func toque_na_tela() -> void:
	match estado:
		"inicio":
			hud.mostrar_tela("selecao")
		"pausado":
			retomar()
		"saindo": pass
		"fim":
			novo_jogo(false)

func trocar_camera() -> void:
	cam_mode = "jogador" if cam_mode == "campo" else "campo"
	hud.definir_camera(cam_mode)

func saida_de_bola(quem: int) -> void:
	for t in 2:
		for i in GB.POR_TIME:
			var p = times[t][i]
			p.position = p.casa
			p.vel = Vector2.ZERO
			p.direcao = Vector2.RIGHT if t == 0 else Vector2.LEFT
			p.cd = 0.0
			p.dive = 0.0
			p.dive_cd = 0.0
			p.pensar_cd = 0.0
			p.acabou_de_chutar = false
	bola.position = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
	bola.vel = Vector2.ZERO
	bola.rot = 0.0
	bola.dono = null
	var lado = -1.0 if quem == 0 else 1.0
	var cand = null
	var melhor = 1.0e9
	for p in times[quem]:
		if p.funcao == "gol" or p.eh_usuario:
			continue
		var d: float = p.position.distance_to(bola.position)
		if d < melhor:
			melhor = d
			cand = p
	if cand != null:
		cand.position = bola.position + Vector2(lado * 22.0, 5.0)
	if quem == 0:
		usuario.position = bola.position + Vector2(-34.0, -10.0)
	congelar = 0.0
	posse = -1
	_camera(0.0)
	_redesenhar()

# ------------------------------------------------------------------ passo fixo
func _physics_process(dt: float) -> void:
	var t0 = Time.get_ticks_usec()
	t_pfisicos += 1                     # conta SEMPRE (inclusive nas telas de início/pausa)
	if foto_path != "" and not foto_feita and t_pfisicos >= foto_quadro:
		foto_feita = true
		_tirar_foto()
	if modo_teste:
		_testes_de_tela()
	if estado == "jogando":
		_passo(dt)
	else:
		_redesenhar()
	if modo_teste:
		t_cpu_us += Time.get_ticks_usec() - t0

func _passo(dt: float) -> void:
	if congelar > 0.0:
		congelar -= dt
		if congelar <= 0.0:
			saida_de_bola(proximo)
		return

	relogio -= dt
	if relogio <= 0.0:
		relogio = 0.0
		hud.atualizar(pontos, relogio)
		_acabar()
		return

	tempo_jogo += dt
	t_frames += 1

	# 1) comando (dedo + teclado) — ou o robô, no teste automático
	var dir = Vector2.ZERO
	if auto_teste:
		pass
	elif modo_teste:
		dir = _robo_dir(dt)
	else:
		dir = controles.vetor + _teclado_dir()
		_atualizar_chute(dt)

	# 2) movimento — 4 botões: VELOCIDADE acelera, DRIBLE segura a bola
	if not auto_teste:
		var vel_max = GB.MAXV
		var acel = GB.ACC
		if controles.velocidade_pressionada:
			vel_max *= 1.48
			acel *= 1.25
		elif controles.drible_pressionado:
			vel_max *= 0.68
			acel *= 0.85
		usuario.aplicar_movimento(dir, dt, vel_max, acel)
	for t in 2:
		for p in times[t]:
			if not p.eh_usuario:
				p.pensar(dt)

	# 3) posse, caçadores e mergulho do goleiro
	_atualizar_posse()
	_atualizar_cacadores()
	_mergulho_goleiros()

	# 4) bola
	bola.vel -= bola.vel * GB.BFRI * dt
	var bs: float = bola.vel.length()
	if bs < GB.BSTOP:
		bola.vel = Vector2.ZERO
	bola.position += bola.vel * dt
	bola.rot += bs * dt * 0.10

	# 5) toques: quem está mais perto age primeiro
	todos.sort_custom(_mais_perto_primeiro)
	for q in todos:
		if q.eh_usuario:
			_toque_usuario(q)
		else:
			_toque_ia(q)
		if q.acabou_de_chutar:
			q.acabou_de_chutar = false
			break
	_limites()

	# 6) regras
	if bola.position.x + GB.RB < 0.0 and absf(bola.position.y - GB.F_H * 0.5) < GB.GOAL_H * 0.5:
		_marcar_gol(1)
		return
	if bola.position.x - GB.RB > GB.F_W and absf(bola.position.y - GB.F_H * 0.5) < GB.GOAL_H * 0.5:
		_marcar_gol(0)
		return
	_fora_de_campo()

	hud.atualizar(pontos, relogio)
	_camera(dt)
	_redesenhar()
	if modo_teste:
		_telemetria(dt)

func _mais_perto_primeiro(a, b) -> bool:
	return a.position.distance_to(bola.position) < b.position.distance_to(bola.position)

func _process(dt: float) -> void:
	if campo_vp != null:
		quadros_visuais += 1
		if quadros_visuais == 3:
			# a imagem do campo já está pronta: para de redesenhá-la (economia de celular)
			campo_vp.render_target_update_mode = SubViewport.UPDATE_DISABLED
	_vigiar_desempenho(dt)

# ------------------------------------------------------------------ desempenho (v6)
func _vigiar_desempenho(dt: float) -> void:
	## Se os quadros caírem, o jogo se ajusta sozinho em vez de ficar travado:
	## reduz a resolução de desenho (o "modo leve") e volta ao normal quando o aparelho aguentar.
	if DisplayServer.get_name() == "headless":
		return
	fps_agora = float(Engine.get_frames_per_second())     # a linha da tela nunca fica vazia
	if sem_leve:
		return
	_vida_app += dt
	fps_agora = float(Engine.get_frames_per_second())
	if _vida_app < 3.0:               # os primeiros segundos (carregando o jogo) não contam
		return
	if fps_agora < 46.0:
		_fps_baixo += dt
		_fps_alto = 0.0
	elif fps_agora > 57.0:
		_fps_alto += dt
		_fps_baixo = 0.0
	else:
		_fps_baixo = 0.0
		_fps_alto = 0.0
	if _fps_baixo > 2.0 and modo_leve < 2:
		modo_leve += 1
		_fps_baixo = 0.0
		_aplicar_qualidade()
	elif _fps_alto > 5.0 and modo_leve > 0:
		modo_leve -= 1
		_fps_alto = 0.0
		_aplicar_qualidade()

func _aplicar_qualidade() -> void:
	if DisplayServer.get_name() == "headless":
		return
	var escalas = [1.0, 0.75, 0.62]
	var escala: float = escalas[modo_leve]
	var jan = get_window()
	jan.content_scale_size = Vector2i(1280, 720)     # a "moldura" de desenho nunca muda
	jan.content_scale_factor = escala                # só a quantidade de pixels é que cai
	# CORREÇÃO v6.1: depois de mudar a escala é OBRIGATÓRIO reposicionar HUD e controles —
	# era isso que deixava START/CHUTE no lugar errado quando o modo leve ligava sozinho.
	hud._layout()
	controles.reposicionar()
	_camera(0.0)
	print("[DESEMPENHO] modo leve %d — desenhando em %.0f%% (%.0f fps)" % [modo_leve, escala * 100.0, fps_agora])

func _nome_gpu() -> String:
	if _gpu == "":
		_gpu = "?"
		var info = OS.get_video_adapter_driver_info()
		if info.size() >= 2:
			_gpu = str(info[1])
		_gpu = _gpu.replace("ANGLE (", "").replace(")", "")
		if _gpu.length() > 44:
			_gpu = _gpu.substr(0, 44)
	return _gpu

func resumo_desempenho() -> String:
	## A linha pequena do canto da tela — é por ela que o dono responde "quantos fps?"
	var leve = "" if modo_leve == 0 else "  ·  MODO LEVE %d" % modo_leve
	return "%d fps%s  ·  %s" % [int(fps_agora), leve, _nome_gpu()]

func diagnostico() -> String:
	## Texto longo (tela de pausa): o que o assistente precisa saber do aparelho.
	var tela_px = "?"
	if DisplayServer.get_name() != "headless":
		tela_px = "%dx%d" % [int(get_window().size.x), int(get_window().size.y)]
	return "desempenho: %s  ·  janela %s  ·  escala %.2f  ·  campo 1280  ·  motor Godot %s" % [
		resumo_desempenho(), tela_px, get_window().content_scale_factor if DisplayServer.get_name() != "headless" else 1.0,
		Engine.get_version_info()["string"]]

func _redesenhar() -> void:
	# o campo virou imagem estática — só a bola e os jogadores se redesenham
	bola.queue_redraw()
	for p in todos:
		p.queue_redraw()
	for t in 2:
		var g = desenhos_goleiro[t]
		var p = gols[t]
		if g != null and p != null:
			g.position = p.position
			g.direcao = p.direcao
			g.dive = p.dive
			g.queue_redraw()

func _teclado_dir() -> Vector2:
	var d = Vector2.ZERO
	if Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A):
		d.x -= 1.0
	if Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D):
		d.x += 1.0
	if Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W):
		d.y -= 1.0
	if Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S):
		d.y += 1.0
	if d.length() > 1.0:
		d = d.normalized()
	return d

func _atualizar_chute(dt: float) -> void:
	var quer: bool = controles.chute_pressionado or Input.is_key_pressed(KEY_SPACE)
	if quer and not carregando:
		carregando = true
		potencia = 0.0
	if not quer and carregando:
		carregando = false
		chutar(potencia)
	if carregando:
		potencia = minf(1.0, potencia + dt / GB.CHARGE_TIME)
	var j = Input.is_key_pressed(KEY_J)
	if (j and not _j_antes) or controles.pedir_passe:
		controles.pedir_passe = false
		passar()
	_j_antes = j

func _input(evento: InputEvent) -> void:
	if evento is InputEventKey and evento.pressed and not evento.echo:
		if evento.keycode == KEY_C:
			trocar_camera()
		elif evento.keycode == KEY_ESCAPE and estado == "jogando":
			pausar()

# ------------------------------------------------------------------ chute e passe
func chutar(forca: float) -> void:
	if usuario.position.distance_to(bola.position) > GB.SHOT_RANGE:
		potencia = 0.0
		return
	var ax: Vector2 = usuario.direcao
	if usuario.velocidade() <= 25.0:
		var d: Vector2 = bola.position - usuario.position
		if d.length() > 0.01:
			ax = d.normalized()
	var v: float = GB.SHOT_MIN + (GB.SHOT_MAX - GB.SHOT_MIN) * clampf(forca, 0.0, 1.0)
	bola.vel = ax * v
	bola.dono = usuario
	usuario.cd = 0.3
	usuario.acabou_de_chutar = true
	potencia = 0.0

func passar() -> void:
	if usuario.position.distance_to(bola.position) > GB.SHOT_RANGE:
		return
	var alvo = _melhor_passe(usuario)
	var ax: Vector2 = usuario.direcao
	if alvo != null:
		var d: Vector2 = alvo.position - usuario.position
		if d.length() > 0.01:
			ax = d.normalized()
	var v: float = GB.SHOT_MAX * GB.PASS_POW
	bola.vel = ax * v
	bola.dono = usuario
	usuario.cd = 0.25
	usuario.acabou_de_chutar = true

# ------------------------------------------------------------------ toques
func _toque_usuario(p) -> void:
	# MODO BOTÃO — COLA + DRIBLE + VELOCIDADE (25/09/2026)
	# Cola: a bola não sai do pé; Drible: condução curta e rápida; Velocidade: resposta instantânea
	var d: float = p.position.distance_to(bola.position)
	var n: Vector2 = bola.position - p.position
	if n.length() < 0.01:
		n = Vector2.RIGHT
	n = n.normalized()
	if d < GB.CONTATO:
		bola.position += n * (GB.CONTATO - d)
		if p.cd > 0.0:
			return
		bola.dono = p
		var ps: float = p.velocidade()
		if ps > 12.0:
			# drible em velocidade: bola colada na frente, com impulso do botão
			bola.vel = p.direcao * maxf(ps * 1.32, 68.0)
		else:
			# cola parada: bola cola exatamente na frente do botão, não quica
			bola.vel = bola.vel * 0.22 + p.direcao * 22.0
			var alvo_pos: Vector2 = p.position + p.direcao * (GB.CONTATO + 1.8)
			bola.position = bola.position.lerp(alvo_pos, 0.55)
		return
	if p.cd > 0.0:
		return
	if d < GB.CTRL:
		var sp: float = p.velocidade()
		if sp > 8.0:
			# controle à distância: traz a bola para o pé rapidamente (cola magnética)
			var alvo: Vector2 = p.direcao * maxf(sp * 1.28, 72.0)
			bola.vel += (alvo - bola.vel) * 0.58
			# puxa a posição também, não só a velocidade — efeito cola visível
			var alvo_pos2: Vector2 = p.position + p.direcao * (GB.CONTATO + 2.2)
			bola.position = bola.position.lerp(alvo_pos2, 0.18)
		else:
			# parado mas dentro da área de controle: bola desliza até colar
			var alvo_pos3: Vector2 = p.position + p.direcao * (GB.CONTATO + 1.5)
			var dir: Vector2 = alvo_pos3 - bola.position
			bola.vel += dir * 6.0
			bola.vel *= 0.88

func _toque_ia(p) -> void:
	# IA DIFICIL + ESTRATEGICA v7 — nao joga de qualquer jeito, pensa como humano
	var raio: float = GB.CONTATO
	if p.funcao == "gol" and p.dive > 0.0:
		raio = GB.CONTATO * 1.9
	var d: float = p.position.distance_to(bola.position)
	if d >= raio:
		return
	var n: Vector2 = bola.position - p.position
	if n.length() < 0.01:
		n = Vector2.RIGHT
	n = n.normalized()
	bola.position += n * (raio - d)
	bola.dono = p
	if p.cd > 0.0:
		return
	if p.funcao == "gol":
		_chute_goleiro(p)
		p.cd = 0.65
		p.acabou_de_chutar = true
		return
	# avalia a situacao como um humano pensaria
	var gol_adv = Vector2(GB.F_W if p.time == 0 else 0.0, GB.F_H * 0.5)
	var dgol: float = bola.position.distance_to(gol_adv)
	var pressao = 0
	var pressao_perto = 0
	for adv in adversarios_de(p):
		if adv.funcao == "gol": continue
		var dd = adv.position.distance_to(bola.position)
		if dd < 28.0:
			pressao += 1
			if dd < 18.0: pressao_perto += 1
	# campo em 3 faixas (defesa/meio/ataque) — estrategia muda em cada
	var terco = bola.position.x / GB.F_W
	if p.time == 1: terco = 1.0 - terco
	var no_ataque: bool = terco > 0.66
	var no_meio: bool = terco > 0.33 and terco <= 0.66
	# avalia chute com nota 0..1 (humano so chuta quando vale)
	var nota_chute = _avaliar_chute(p, gol_adv, dgol, pressao)
	# avalia melhor passe com nota
	var melhor_passe_info = _avaliar_melhor_passe(p)
	var colega = melhor_passe_info[0]
	var nota_passe: float = melhor_passe_info[1]
	# 1) SE ESTOU NO ATAQUE ou META ABERTA e tenho boa chance: FINALIZA (dificil erra pouco)
	if nota_chute > 0.58 and (no_ataque or dgol < GB.F_W*0.48):
		_chute_para(p, gol_adv, nota_chute)
		p.cd = 0.68
		p.acabou_de_chutar = true
		return
	# 2) PASSE INTELIGENTE: triangula, usa o humano, nao força passe arriscado
	# parceiro do usuario tem bonus: a IA do seu time quer jogar COM voce
	var bonus_usuario = 0.0
	if colega != null and colega.eh_usuario:
		nota_passe += 0.12
	# no meio campo prefere passe curto, no ataque prefere passe vertical
	var limite_passe = 0.45 if no_meio else (0.38 if pressao>0 else 0.52)
	# se estou pressionado, aceita passe com nota menor (precisa sair)
	if pressao_perto >= 1: limite_passe -= 0.12
	if colega != null and nota_passe > limite_passe:
		_passe_ia(p, colega, nota_passe)
		p.cd = 0.52
		p.acabou_de_chutar = true
		return
	# 3) PRESSIONADO sem passe bom: protege + tabela na mureta ou recuo seguro
	if pressao_perto >= 2 or (pressao >= 2 and nota_passe < 0.30):
		# humano usa tabela: chuta na mureta lateral para si ou para companheiro
		var usa_tabela: bool = (int(bola.position.x + bola.position.y) % 2 == 0) and (bola.position.y < GB.F_H*0.25 or bola.position.y > GB.F_H*0.75)
		if usa_tabela:
			var parede_y = 0.0 if bola.position.y < GB.F_H*0.5 else GB.F_H
			# chutao diagonal para frente usando parede
			var frente = Vector2(1 if p.time==0 else -1, signf(parede_y - bola.position.y)*0.6).normalized()
			bola.vel = frente * GB.KICK_NEAR_Y * 0.78
		else:
			var desvio_det: float = (float(p.numero % 5) - 2.0) * 0.14
			var frente2 = Vector2(1 if p.time==0 else -1, desvio_det).normalized()
			bola.vel = frente2 * GB.KICK_NEAR_Y * 0.82
		p.cd = 0.48
		p.acabou_de_chutar = true
		return
	# 4) DRIBLE HUMANO: conduz para o espaco livre, nao em linha reta contra adversario
	var alvo_drible = _melhor_drible(p, gol_adv)
	bola.vel = alvo_drible * maxf(p.velocidade()*0.92, 58.0)
	# cola a bola na frente para conduzir
	bola.position = bola.position.lerp(p.position + p.direcao*(GB.CONTATO+2.0), 0.12)
	p.cd = 0.32
	p.acabou_de_chutar = true

func _avaliar_chute(p, gol: Vector2, dgol: float, pressao: int) -> float:
	# retorna 0..1 (quanto maior, melhor para chutar)
	var nota = 0.0
	# distancia: quanto mais perto, melhor (mas nao precisa estar colado)
	nota += clampf(1.0 - dgol / (GB.F_W*0.62), 0.0, 1.0) * 0.45
	# angulo: centralizado vale mais
	var meio = GB.F_H*0.5
	var desvio_y = absf(bola.position.y - meio) / (GB.F_H*0.5)
	nota += (1.0 - desvio_y) * 0.15
	# meta aberta: goleiro fora
	var gk = gols[1 - p.time]
	if gk != null:
		var dgk = gk.position.distance_to(gol)
		if dgk > GB.GOAL_H*1.0:
			nota += 0.28
		elif dgk > GB.GOAL_H*0.65:
			nota += 0.15
		else:
			# goleiro bem posicionado: chute no canto oposto vale mais
			var canto_oposto = meio + GB.GOAL_H*0.30 * (1 if gk.position.y < meio else -1)
			var dist_canto = absf(bola.position.y - canto_oposto) / GB.GOAL_H
			nota += (1.0 - dist_canto)*0.10
	else:
		nota += 0.30
	# bloqueadores na frente
	var livres = 0
	var dir = (gol - bola.position).normalized() if (gol - bola.position).length()>0.01 else Vector2(1,0)
	for adv in adversarios_de(p):
		if adv.funcao=="gol": continue
		var rel = adv.position - bola.position
		if rel.length() < 34 and rel.normalized().dot(dir) > 0.55:
			nota -= 0.22
			livres -= 1
	if livres == 0:
		nota += 0.10
	# pressao: se muito pressionado, chuta pior
	nota -= pressao * 0.07
	# parceiro bem posicionado? prefere passe a chute forcado (humano pensante)
	var melhor = _avaliar_melhor_passe(p)
	if melhor[1] > 0.62 and nota < 0.75:
		nota -= 0.12
	return clampf(nota, 0.0, 1.0)

func _avaliar_melhor_passe(p):
	# retorna [melhor_colega, nota 0..1] — humano avalia linha de passe, distancia e abertura
	var melhor = null
	var melhor_nota = -1e9
	var sinal = 1 if p.time==0 else -1
	for c in time_de(p):
		if c == p or c.funcao=="gol": continue
		var d = p.position.distance_to(c.position)
		if d < 26 or d > GB.F_W*0.58: continue
		var para_frente = (c.position.x - p.position.x) * sinal
		# nao passa para tras no ataque, a nao ser recuo seguro
		if para_frente < -18 and p.position.x * sinal > GB.F_W*0.55:
			continue
		var nota = 0.0
		# progresso a frente vale (mas nao precisa ser sempre frente)
		nota += clampf(para_frente / (GB.F_W*0.28), -0.4, 1.0) * 0.35
		# distancia confortavel (triangula 70-110)
		var conforto = 1.0 - clampf(absf(d - 88) / 88.0, 0, 1)
		nota += conforto * 0.22
		# abertura do colega (quanto mais livre, melhor)
		var abertura = 1e9
		for adv in adversarios_de(p):
			var da = adv.position.distance_to(c.position)
			if da < abertura: abertura = da
		nota += clampf(abertura / 48.0, 0, 1) * 0.30
		# linha de passe livre (sem adversario cortando)
		if _passe_livre_real(p.position, c.position, p.time):
			nota += 0.28
		else:
			nota -= 0.35
		# bonus humano: prioriza o jogador que voce controla
		if c.eh_usuario:
			nota += 0.18
			# se humano esta bem aberto na frente, vale ainda mais
			if para_frente > 20 and abertura > 26:
				nota += 0.10
		# penaliza se colega esta colado na mureta pressionado
		if c.position.y < 12 or c.position.y > GB.F_H-12:
			nota -= 0.10
		if nota > melhor_nota:
			melhor_nota = nota
			melhor = c
	# converte para 0..1
	var nota01 = clampf((melhor_nota + 0.5) / 1.25, 0, 1) if melhor != null else 0.0
	return [melhor, nota01]

func _passe_livre_real(orig: Vector2, dest: Vector2, time_p: int) -> bool:
	var seg = dest - orig
	var L = seg.length()
	if L < 0.01: return true
	var dir = seg / L
	for t in 2:
		if t == time_p: continue
		for adv in times[t]:
			if adv.funcao=="gol": continue
			var rel = adv.position - orig
			var proj = rel.dot(dir)
			if proj < 14 or proj > L - 14: continue
			var perp = (rel - dir*proj).length()
			if perp < 20.0:
				return false
	return true

func _melhor_passe(p):
	return _avaliar_melhor_passe(p)[0]

func _passe_ia(p, colega, nota: float = 0.5) -> void:
	var d = p.position.distance_to(colega.position)
	var dest = colega.position + colega.vel * 0.18
	# antecipa corrida do colega
	var dir = dest - bola.position
	if dir.length() < 0.01: dir = Vector2.RIGHT
	# erro humano dificil: quanto menor a nota, mais erro; IA dificil erra pouco mesmo em passe longo
	# v8 DETERMINISTICO — sem randf: erro = 0 (IA dificil, sempre precisa). Pequeno desvio deterministico por posicao (nao sorteio)
	dir = dir.normalized()  # sem rotacao aleatoria
	var forca = clampf(d * 0.92, GB.SHOT_MAX*0.36, GB.SHOT_MAX*0.86)
	# passe rapido no ataque, mais cadenciado na defesa
	if bola.position.x / GB.F_W > 0.55 and p.time==0 or bola.position.x / GB.F_W < 0.45 and p.time==1:
		forca *= 1.08
	bola.vel = dir * forca

func _chute_para(p, gol: Vector2, nota: float = 0.6) -> void:
	var gk = gols[1 - p.time]
	var meio = GB.F_H*0.5
	# mira no canto oposto ao goleiro (humano inteligente)
	var canto: float = meio - GB.GOAL_H*0.32
	if gk != null and gk.position.y <= meio:
		canto = meio + GB.GOAL_H*0.32
	# se goleiro muito adiantado, tenta por cima
	if gk != null and gk.position.distance_to(gol) > GB.GOAL_H*0.85:
		# chute colocado no canto mais distante do goleiro
		var dist_gk_top = absf(gk.position.y - (meio - GB.GOAL_H*0.32))
		var dist_gk_bot = absf(gk.position.y - (meio + GB.GOAL_H*0.32))
		canto = meio - GB.GOAL_H*0.32 if dist_gk_top > dist_gk_bot else meio + GB.GOAL_H*0.32
	var alvo = Vector2(gol.x, canto)
	var d = bola.position.distance_to(alvo)
	var dir = alvo - bola.position
	if dir.length() < 0.01: dir = Vector2(1 if p.time==0 else -1, 0)
	# v8 DETERMINISTICO — sem randf: mira perfeita (IA dificil). Antes erro_base com rotacao aleatoria.
	dir = dir.normalized()
	# forca calibrada pela distancia, nao sempre maxima (humano dosa)
	var forca = clampf(d * 1.08, GB.KICK_FAR_X*0.92, GB.KICK_NEAR_Y)
	if nota > 0.78:
		forca = minf(forca*1.04, GB.SHOT_MAX)
	bola.vel = dir * forca

func _melhor_drible(p, gol: Vector2) -> Vector2:
	# escolhe direcao livre para driblar, nao contra o adversario
	var frente = Vector2(1 if p.time==0 else -1, 0)
	var dir_gol = (gol - p.position).normalized() if (gol - p.position).length()>0.01 else frente
	var melhor_dir = dir_gol
	var melhor_score = -1e9
	for ang in [-42.0, -22.0, 0.0, 22.0, 42.0]:
		var dir = dir_gol.rotated(deg_to_rad(ang))
		var cand = p.position + dir * 42.0
		cand.x = clampf(cand.x, 10, GB.F_W-10)
		cand.y = clampf(cand.y, 10, GB.F_H-10)
		var score = 0.0
		score += dir.dot(dir_gol) * 28.0
		var abertura = 1e9
		for adv in adversarios_de(p):
			var da = adv.position.distance_to(cand)
			if da < abertura: abertura = da
		score += abertura * 0.9
		# evita conduzir para dentro do aglomerado
		if abertura < 18: score -= 22
		if score > melhor_score:
			melhor_score = score
			melhor_dir = dir
	return melhor_dir

func _chute_livre(p, gol: Vector2) -> bool:
	var dir: Vector2 = gol - bola.position
	if dir.length() < 0.01: return true
	dir = dir.normalized()
	for adv in adversarios_de(p):
		if adv.funcao == "gol": continue
		var rel: Vector2 = adv.position - bola.position
		if rel.length() < 30.0 and rel.normalized().dot(dir) > 0.58:
			return false
	return true

func _chute_goleiro(p) -> void:
	# goleiro pensa: sai jogando com o humano se possivel, senao recuo seguro
	var melhor = _avaliar_melhor_passe(p)
	if melhor[0] != null and melhor[1] > 0.40:
		_passe_ia(p, melhor[0], melhor[1])
		return
	# procura o humano
	var u = usuario
	if u and u.time == p.time and u.position.distance_to(p.position) < GB.F_W*0.65:
		if _passe_livre_real(p.position, u.position, p.time):
			_passe_ia(p, u, 0.55)
			return
	# v8 deterministico: desvio fixo por numero, sem sorteio
	var desvio_gk: float = (float(p.numero % 5) - 2.0) * 0.12
	var dir = Vector2(1 if p.time==0 else -1, desvio_gk).normalized()
	bola.vel = dir * GB.KICK_NEAR_Y * 0.88

# ------------------------------------------------------------------ regras
func _limites() -> void:
	for p in todos:
		p.position.x = clampf(p.position.x, 5.0, GB.F_W - 5.0)
		p.position.y = clampf(p.position.y, 5.0, GB.F_H - 5.0)
	var vmax: float = bola.vel.length()
	if vmax > 620.0:
		bola.vel = bola.vel / vmax * 620.0

var t_borda = 0.0

func _fora_de_campo() -> void:
	# CAMPO FECHADO com TABELA (mureta): a bola quica e não sai — permite tabela na parede
	# (os gols continuam vazados: a checagem de gol vem antes, em _passo)
	if bola.position.y - GB.RB < 0.0:
		bola.position.y = GB.RB
		bola.vel.y = absf(bola.vel.y) * 0.62
		bola.vel.x *= 0.92
	if bola.position.y + GB.RB > GB.F_H:
		bola.position.y = GB.F_H - GB.RB
		bola.vel.y = -absf(bola.vel.y) * 0.62
		bola.vel.x *= 0.92
	if bola.position.x - GB.RB < 0.0:
		# se for na boca do gol, deixa passar (o gol já foi marcado antes) — senão quica
		if absf(bola.position.y - GB.F_H * 0.5) < GB.GOAL_H * 0.5:
			return
		bola.position.x = GB.RB
		bola.vel.x = absf(bola.vel.x) * 0.66
		bola.vel.y *= 0.92
	if bola.position.x + GB.RB > GB.F_W:
		if absf(bola.position.y - GB.F_H * 0.5) < GB.GOAL_H * 0.5:
			return
		bola.position.x = GB.F_W - GB.RB
		bola.vel.x = -absf(bola.vel.x) * 0.66
		bola.vel.y *= 0.92
	var na_borda: bool = bola.position.y < 5.0 or bola.position.y > GB.F_H - 5.0 or bola.position.x < 5.0 or bola.position.x > GB.F_W - 5.0
	if na_borda and bola.vel.length() < 16.0:
		t_borda += 1.0 / 60.0
		if t_borda > 1.2:
			t_borda = 0.0
			var centro = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
			var d: Vector2 = centro - bola.position
			if d.length() < 1.0:
				d = Vector2.RIGHT
			bola.vel = d.normalized() * 70.0
			if modo_teste:
				print("[TESTE] bola recolocada em jogo aos %.1fs" % tempo_jogo)
	else:
		t_borda = 0.0

func _marcar_gol(quem: int) -> void:
	pontos[quem] += 1
	t_gols[quem] += 1
	proximo = 1 - quem
	congelar = 1.6
	var autor = 0
	var d = bola.dono
	if d != null and d.time == quem:
		autor = d.numero
	hud.atualizar(pontos, relogio)
	hud.mostrar_anuncio("GOL!" if autor <= 0 else "GOL do %d!" % autor)
	if modo_teste:
		print("[TESTE] GOL aos %.1fs — placar %d x %d" % [tempo_jogo, pontos[0], pontos[1]])

func _acabar() -> void:
	fim = true
	estado = "fim"
	hud.mostrar_tela("fim")
	if modo_teste:
		_resumo_teste()
		get_tree().quit()

# ------------------------------------------------------------------ posse, caçadores, câmera
func _atualizar_posse() -> void:
	var melhor = 1.0e9
	var dono = -1
	for p in todos:
		var d: float = p.position.distance_to(bola.position)
		if d < melhor:
			melhor = d
			dono = p.time
	posse = dono if melhor < GB.CTRL * 1.6 else -1
	if modo_teste and posse >= 0:
		t_posse[posse] += 1.0 / 60.0

func _atualizar_cacadores() -> void:
	for t in 2:
		var melhor = 1.0e9
		var cand = null
		for p in times[t]:
			if p.funcao == "gol" or p.eh_usuario:
				continue
			var d: float = p.position.distance_to(bola.position)
			if d < melhor:
				melhor = d
				cand = p
		cacadores[t] = cand

func sou_cassador(p) -> bool:
	return cacadores[p.time] == p

func time_de(p) -> Array:
	return times[p.time]

func adversarios_de(p) -> Array:
	return times[1 - p.time]

func _mergulho_goleiros() -> void:
	for t in 2:
		var gk = gols[t]
		if gk == null or gk.dive_cd > 0.0:
			continue
		var meta_x: float = 0.0 if gk.casa.x < GB.F_W * 0.5 else GB.F_W
		var centro = Vector2(meta_x, GB.F_H * 0.5)
		var dg: float = bola.position.distance_to(centro)
		if dg < GB.F_W * 0.22 and bola.vel.length() > 60.0 and absf(bola.vel.x) > 1.0:
			var t_chega: float = (meta_x - bola.position.x) / bola.vel.x
			var prev: Vector2 = bola.position + bola.vel * t_chega
			if t_chega > 0.0 and t_chega < 0.55 and absf(prev.y - centro.y) < GB.GOAL_H * 0.9:
				gk.dive = 0.35
				gk.dive_cd = 1.0

func _fator_leve() -> float:
	if DisplayServer.get_name() == "headless":
		return 1.0
	return maxf(0.3, get_window().content_scale_factor)

func _camera(dt: float) -> void:
	# o zoom acompanha o modo leve: o campo continua do MESMO tamanho na tela,
	# só que desenhado com menos pixels (é assim que o modo leve ajuda sem mudar a cara do jogo)
	var k = 1.0 / _fator_leve()
	if cam_mode == "campo":
		var alvo_z = Vector2(GB.ZOOM_CAMPO, GB.ZOOM_CAMPO) * k
		cam.zoom += (alvo_z - cam.zoom) * minf(1.0, dt * 4.0)
		var alvo = Vector2(GB.F_W * 0.5, GB.F_H * 0.5)
		cam.position += (alvo - cam.position) * minf(1.0, dt * 5.0)
	else:
		var alvo_z2 = Vector2(GB.ZOOM_JOGADOR, GB.ZOOM_JOGADOR) * k
		cam.zoom += (alvo_z2 - cam.zoom) * minf(1.0, dt * 4.0)
		var alvo: Vector2 = usuario.position + usuario.direcao * 26.0
		cam.position += (alvo - cam.position) * minf(1.0, dt * 6.0)

# ------------------------------------------------------------------ foto da tela
func _tirar_foto() -> void:
	## Espera o quadro ser desenhado e grava um PNG — é assim que o assistente
	## confere o visual do jogo de verdade, sem depender de ninguém olhar.
	await RenderingServer.frame_post_draw
	var img = get_viewport().get_texture().get_image()
	var erro = img.save_png(foto_path)
	print("[TESTE] foto salva em %s (erro %d) — %dx%d" % [foto_path, erro, img.get_width(), img.get_height()])
	if modo_teste and foto_quadro >= 0 and "--so-foto" in OS.get_cmdline_args() + OS.get_cmdline_user_args():
		get_tree().quit()

# ------------------------------------------------------------------ robô de teste
func _robo_dir(dt: float) -> Vector2:
	var b: Vector2 = bola.position
	var p: Vector2 = usuario.position
	var d: float = b.distance_to(p)
	var gk = gols[1]
	var canto: float = GB.F_H * 0.5 - GB.GOAL_H * 0.30
	if gk != null and gk.position.y <= GB.F_H * 0.5:
		canto = GB.F_H * 0.5 + GB.GOAL_H * 0.30
	var gol = Vector2(GB.F_W, canto)
	var dir_gol: Vector2 = gol - b
	if dir_gol.length() < 0.01:
		dir_gol = Vector2(1, 0)
	dir_gol = dir_gol.normalized()
	if d > 16.0:
		var mira: Vector2 = b - dir_gol * 10.0
		var v: Vector2 = mira - p
		if v.length() < 1.0:
			return Vector2.ZERO
		return v.normalized()
	if not carregando:
		carregando = true
		potencia = 0.0
	potencia = minf(1.0, potencia + dt / GB.CHARGE_TIME)
	if potencia >= 1.0:
		carregando = false
		chutar(1.0)
	return dir_gol

# ------------------------------------------------------------------ testes
func _testes_de_tela() -> void:
	if t_etapa == 0 and tempo_jogo > 20.0:
		t_etapa = 1
		t_pausa_quadros = 0
		pausar()
		print("[TESTE] pausa pedida aos %.1fs (relógio %.0f, estado %s)" % [tempo_jogo, relogio, estado])
	elif t_etapa == 1:
		t_pausa_quadros += 1
		if t_pausa_quadros == 30:
			print("[TESTE] 30 quadros de pausa: relógio %.0f (não pode ter andado)" % relogio)
			t_etapa = 2
			retomar()
			print("[TESTE] retomada ok — estado %s" % estado)
	elif t_etapa == 2 and tempo_jogo > 35.0:
		t_etapa = 3
		novo_jogo(true)
		print("[TESTE] partida recomeçada no meio: relógio %.0f, placar %d x %d, jogadores %d" % [
			relogio, pontos[0], pontos[1], todos.size()])

func _telemetria(dt: float) -> void:
	for p in todos:
		if not p.position.is_finite() or not p.vel.is_finite():
			t_anomalias += 1
		if p.position.x < -1.0 or p.position.x > GB.F_W + 1.0 or p.position.y < -1.0 or p.position.y > GB.F_H + 1.0:
			t_anomalias += 1
	if not bola.position.is_finite() or not bola.vel.is_finite():
		t_anomalias += 1
	var moveu: float = bola.position.distance_to(t_ultima)
	if moveu < 2.5:
		t_parado += dt
	else:
		t_parado = 0.0
	if t_parado > 5.0:
		t_travamentos += 1
		t_parado = 0.0
		print("[TESTE] AVISO: bola parada por 5s aos %.1fs (x=%.0f y=%.0f)" % [tempo_jogo, bola.position.x, bola.position.y])
	t_ultima = bola.position
	if t_frames % 600 == 0:
		var total: float = t_posse[0] + t_posse[1]
		var pn: float = (100.0 * t_posse[0] / total) if total > 0.0 else 0.0
		var ms: float = float(t_cpu_us) / 1000.0 / maxf(1.0, float(t_frames))
		print("[TESTE] t=%.0fs placar=%d x %d relogio=%.0f posse_nos=%.0f%% bola_x=%.0f cpu=%.2fms/quadro anomalias=%d" % [
			tempo_jogo, pontos[0], pontos[1], relogio, pn, bola.position.x, ms, t_anomalias])

func _resumo_teste() -> void:
	var total: float = t_posse[0] + t_posse[1]
	var pn: float = (100.0 * t_posse[0] / total) if total > 0.0 else 0.0
	var ms: float = float(t_cpu_us) / 1000.0 / maxf(1.0, float(t_frames))
	print("[TESTE] FIM — placar %d x %d | posse nossa %.0f%% | travamentos: %d | anomalias: %d | cpu: %.2f ms/quadro | tempo %.1fs" % [
		pontos[0], pontos[1], pn, t_travamentos, t_anomalias, ms, tempo_jogo])
