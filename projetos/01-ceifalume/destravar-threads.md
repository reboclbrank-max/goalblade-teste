# Desbloquear o Threads — lista única (24/09/2026, noite)

**Onde estamos:** o aplicativo da Meta (`arena`, ID `1063985229878724`) está bloqueado por dentro. O acesso que o assistente
tinha **expirou** (a Meta recusou renovar; token de 1 hora venceu). Então são 2 partes: **A) destravar o app** e
**B) me dar um acesso novo**. Depois disso **o assistente publica** — você não precisa postar nada.

Faça na ordem. Se aparecer algo diferente do que está escrito, **pare e me diga o que apareceu** (print ajuda).

---

## Parte A — destravar o app (5 telas, ~5 minutos)

**A1. Alertas** — é aqui que a Meta escreve o motivo do bloqueio.
👉 https://developers.facebook.com/apps/1063985229878724/alerts/
Procure faixa **vermelha ou amarela**. Se tiver alguma escrita `API access`, `Data Use Checkup`, `restricted` ou `policy`,
clique nela e me diga o texto (ou mande print).

**A2. Data Use Checkup** — causa mais comum desse erro.
👉 https://developers.facebook.com/apps/1063985229878724/app-review/data-use-checkup/
Se estiver **pendente/atrasado**, clique em **Começar/Revisar** e vá clicando em **Próximo → Próximo → Confirmar** (não precisa
escrever nada). No fim, a Meta libera o acesso.

**A3. Permissões do Threads** — precisam estar concedidas.
👉 https://developers.facebook.com/apps/1063985229878724/app-review/permissions/
Veja as linhas **`threads_basic`** e **`threads_content_publish`**. Se alguma estiver cinza / "em revisão", clique e me diga o que
escreve.

**A4. Você como testador** — seu nome tem que estar na lista.
👉 https://developers.facebook.com/apps/1063985229878724/roles/roles/
Aba **Testers** → seção **Threads Testers**: confira se `@reboclbrank` está lá, **sem** "convite pendente". Se não estiver:
**Adicionar pessoas → Threads Tester** → digite `reboclbrank`.

**A5. Reiniciar o status do app** — conserto conhecido para este erro exato.
👉 https://developers.facebook.com/apps/1063985229878724/settings/basic/
Troque o modo para **Em desenvolvimento (Development)** → **Salvar** → espere **1 minuto** → volte para **Ativo (Live/Publicado)**
→ **Salvar**. *(Se essa tela não tiver esse botão, pule este passo.)*

**Se nada disso resolver:** é bloqueio interno da Meta e só o suporte deles destrava —
👉 https://developers.facebook.com/support/bugs/ — escreva: *"Threads API — API access blocked mesmo com permissões concedidas"* e
cite o código de rastreio `ANV6TZPWKhLNycNSZ3DXW`.

---

## Parte B — me dar um acesso novo (30 segundos, depois da Parte A)

**B1.** Com você logado no Threads como `@reboclbrank`, abra este link:

https://threads.net/oauth/authorize?client_id=1063985229878724&redirect_uri=https://reboclbrank-max.github.io/site&scope=threads_basic,threads_content_publish&response_type=code

**B2.** Clique em **Permitir/Autorizar**.

**B3.** A página cai no seu site e a **barra de endereço** termina com `?code=...`. **Copie o link inteiro da barra** e cole aqui no
chat. ⏱️ O código dura poucos minutos — mande na hora.

**B4.** O assistente troca o código pelo acesso de 60 dias e **publica o post imediatamente** (texto já pronto).

---

## Se você não quiser mexer nisso agora

Poste você mesmo — 1 minuto: abra https://www.threads.com/, cole o texto abaixo e publique. Depois me diga "postei" que eu marco a
rodada como 6 de 6 e meço o efeito.

> 🌙 Ceifalume 0.1 completou 1 semana: jogadores no navegador e no Android, e o trailer rodando. Obrigado!
>
> Antes de começar a 0.2, quero ouvir quem jogou:
> 1. Os 3 primeiros dias foram lentos, rápidos ou confusos?
> 2. O que você quer primeiro: (a) resumo do que a fazenda rendeu enquanto você dormia, (b) uma cultura nova, (c) eventos de clima?
> 3. Algo travou ou ficou pequeno demais no celular?
>
> Já decidido para a 0.2: APK bem menor (de 79 MB para ~36 MB).
>
> ▶ https://rebocl-brank.itch.io/ceifalume
>
> #indiedev #godot #idlegame #jogosbr
