class_name Selecoes
# 16 seleções mais conhecidas — força real FIFA 2026 aprox. (ARG campeã 92, etc.)
# Cada entrada: nome, força (barra), camisa hex, bandeira_key para pintor_botao, emoji
const LISTA := [
	{"id":"ARG","nome":"Argentina","forca":92,"camisa":"7dd3fc","bandeira":"ARGENTINA","emoji":"🇦🇷"},
	{"id":"FRA","nome":"França","forca":90,"camisa":"1e3a8a","bandeira":"FRANCA","emoji":"🇫🇷"},
	{"id":"BRA","nome":"Brasil","forca":89,"camisa":"facc15","bandeira":"BRASIL","emoji":"🇧🇷"},
	{"id":"ING","nome":"Inglaterra","forca":88,"camisa":"ffffff","bandeira":"INGLATERRA","emoji":"🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
	{"id":"ESP","nome":"Espanha","forca":87,"camisa":"dc2626","bandeira":"ESPANHA","emoji":"🇪🇸"},
	{"id":"POR","nome":"Portugal","forca":86,"camisa":"064e3b","bandeira":"PORTUGAL","emoji":"🇵🇹"},
	{"id":"NED","nome":"Holanda","forca":85,"camisa":"f97316","bandeira":"HOLANDA","emoji":"🇳🇱"},
	{"id":"GER","nome":"Alemanha","forca":84,"camisa":"d1d5db","bandeira":"ALEMANHA","emoji":"🇩🇪"},
	{"id":"BEL","nome":"Bélgica","forca":83,"camisa":"7f1d1d","bandeira":"BELGICA","emoji":"🇧🇪"},
	{"id":"CRO","nome":"Croácia","forca":82,"camisa":"991b1b","bandeira":"CROACIA","emoji":"🇭🇷"},
	{"id":"URU","nome":"Uruguai","forca":81,"camisa":"e0f2fe","bandeira":"URUGUAI","emoji":"🇺🇾"},
	{"id":"ITA","nome":"Itália","forca":80,"camisa":"60a5fa","bandeira":"ITALIA","emoji":"🇮🇹"},
	{"id":"MEX","nome":"México","forca":78,"camisa":"16a34a","bandeira":"MEXICO","emoji":"🇲🇽"},
	{"id":"USA","nome":"USA","forca":77,"camisa":"bfdbfe","bandeira":"USA","emoji":"🇺🇸"},
	{"id":"JPN","nome":"Japão","forca":76,"camisa":"fff7ed","bandeira":"JAPAO","emoji":"🇯🇵"},
	{"id":"SEN","nome":"Senegal","forca":75,"camisa":"84cc16","bandeira":"SENEGAL","emoji":"🇸🇳"},
]

static func por_id(id: String) -> Dictionary:
	for s in LISTA:
		if s["id"] == id: return s
	return LISTA[0]

static func nome_por_id(id: String) -> String:
	return por_id(id)["nome"]

static func forca_por_id(id: String) -> int:
	return por_id(id)["forca"]
