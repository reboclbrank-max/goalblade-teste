#!/usr/bin/env python3
"""Mede tráfego e engajamento do Ceifalume em todos os canais e anexa uma linha em
projetos/01-ceifalume/marketing/METRICAS.md.

Uso:  python3 ferramentas/medir-marketing.py [--nota "texto"]
Lê a chave da itch em ferramentas/chaves.md (linha `- **Chave:** ...`). Bluesky/Mastodon
usam só endpoints públicos (não precisa de token para medir).
"""
import json, re, sys, os, urllib.request, datetime, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
MET = BASE / "projetos/01-ceifalume/marketing/METRICAS.md"
ITCH_GAME_ID = 5017404
BSKY_HANDLE = "reboclbrank.bsky.social"
BSKY_DID = "did:plc:ypmicjqbhpoxf6xd3ee4zke3"
MASTO = "https://mastodon.social"
MASTO_ACCT = "reboclbrank"
YT_ID = "tB449xupDzY"

def get(url, headers=None):
    r = urllib.request.Request(url, headers={"User-Agent": "medir-marketing/1.0", **(headers or {})})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.read()

def jget(url, headers=None):
    return json.loads(get(url, headers))

def itch_key():
    txt = (BASE / "ferramentas/chaves.md").read_text(encoding="utf-8")
    m = re.search(r"itch.*?`([A-Za-z0-9]{40})`", txt, re.S)
    return m.group(1) if m else None

def main():
    nota = ""
    if "--nota" in sys.argv:
        nota = sys.argv[sys.argv.index("--nota") + 1]
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    row = {"data": now.strftime("%Y-%m-%d %H:%M")}

    # itch
    try:
        k = itch_key()
        d = jget("https://api.itch.io/profile/games", {"Authorization": f"Bearer {k}"})
        games = d.get("data", d).get("games", []) if isinstance(d, dict) else []
        g = next((x for x in games if x.get("id") == ITCH_GAME_ID), None) or (games[0] if games else {})
        row.update(itch_views=g.get("views_count"), itch_dl=g.get("downloads_count"), itch_buy=g.get("purchases_count"))
    except Exception as e:
        row.update(itch_views="?", itch_dl="?", itch_buy="?"); print("itch:", e, file=sys.stderr)

    # github release: downloads do APK
    try:
        rel = jget("https://api.github.com/repos/reboclbrank-max/site/releases/latest")
        row["gh_apk"] = next((a["download_count"] for a in rel.get("assets", []) if a["name"] == "ceifalume.apk"), "?")
    except Exception as e:
        row["gh_apk"] = "?"; print("gh:", e, file=sys.stderr)

    # dev.to
    try:
        k = re.search(r"dev\.to.*?API key:\*\* `([A-Za-z0-9]+)`", (BASE / "ferramentas/chaves.md").read_text(encoding="utf-8"), re.S).group(1)
        arts = jget("https://dev.to/api/articles/me/published", {"api-key": k})
        row.update(devto_views=sum(a.get("page_views_count", 0) for a in arts), devto_react=sum(a.get("public_reactions_count", 0) for a in arts), devto_com=sum(a.get("comments_count", 0) for a in arts))
    except Exception as e:
        row.update(devto_views="?", devto_react="?", devto_com="?"); print("devto:", e, file=sys.stderr)

    # tumblr (público: notas do blog)
    try:
        tj = json.loads(pathlib.Path("/home/user/tools/.tumblr.json").read_text())
        b = jget(f"https://api.tumblr.com/v2/blog/reboclbrank/posts?limit=20&api_key={tj['consumer_key']}")["response"]
        row.update(tumblr_notes=sum(p.get("note_count", 0) for p in b.get("posts", [])), tumblr_posts=b.get("total_posts"))
    except Exception as e:
        row.update(tumblr_notes="?", tumblr_posts="?"); print("tumblr:", e, file=sys.stderr)

    # threads (insights por post: views, likes, replies, reposts)
    try:
        th = json.loads(pathlib.Path("/home/user/tools/.threads.json").read_text())
        posts = jget(f"https://graph.threads.net/v1.0/{th['user_id']}/threads?fields=id&limit=50&access_token={th['access_token']}").get("data", [])
        v = l = 0
        for po in posts:
            ins = jget(f"https://graph.threads.net/v1.0/{po['id']}/insights?metric=views,likes&access_token={th['access_token']}").get("data", [])
            for mtr in ins:
                val = mtr.get("values", [{}])[0].get("value", 0)
                if mtr["name"] == "views": v += val
                if mtr["name"] == "likes": l += val
        row.update(threads_posts=len(posts), threads_views=v, threads_likes=l)
    except Exception as e:
        row.update(threads_posts="?", threads_views="?", threads_likes="?"); print("threads:", e, file=sys.stderr)

    # youtube (scrape do viewCount público)
    try:
        h = get(f"https://www.youtube.com/watch?v={YT_ID}").decode("utf-8", "ignore")
        m = re.search(r'"viewCount":"(\d+)"', h); row["yt_views"] = int(m.group(1)) if m else "?"
    except Exception as e:
        row["yt_views"] = "?"; print("yt:", e, file=sys.stderr)

    # bluesky
    try:
        p = jget(f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={BSKY_HANDLE}")
        row.update(bsky_seg=p.get("followersCount"), bsky_posts=p.get("postsCount"))
        f = jget(f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor={BSKY_HANDLE}&limit=30")
        likes = reposts = replies = 0
        for it in f.get("feed", []):
            po = it.get("post", {})
            if po.get("author", {}).get("did") != BSKY_DID: continue
            likes += po.get("likeCount", 0); reposts += po.get("repostCount", 0); replies += po.get("replyCount", 0)
        row.update(bsky_likes=likes, bsky_rep=reposts, bsky_resp=replies)
    except Exception as e:
        row.update(bsky_seg="?", bsky_posts="?", bsky_likes="?", bsky_rep="?", bsky_resp="?"); print("bsky:", e, file=sys.stderr)

    # mastodon
    try:
        a = jget(f"{MASTO}/api/v1/accounts/lookup?acct={MASTO_ACCT}")
        row.update(masto_seg=a.get("followers_count"), masto_posts=a.get("statuses_count"))
        st = jget(f"{MASTO}/api/v1/accounts/{a['id']}/statuses?limit=40&exclude_replies=true")
        row.update(masto_fav=sum(s.get("favourites_count", 0) for s in st),
                   masto_boost=sum(s.get("reblogs_count", 0) for s in st),
                   masto_resp=sum(s.get("replies_count", 0) for s in st))
    except Exception as e:
        row.update(masto_seg="?", masto_posts="?", masto_fav="?", masto_boost="?", masto_resp="?"); print("masto:", e, file=sys.stderr)

    cols = ["data", "itch_views", "itch_dl", "itch_buy", "gh_apk", "yt_views", "bsky_seg", "bsky_posts", "bsky_likes", "bsky_rep", "bsky_resp",
            "masto_seg", "masto_posts", "masto_fav", "masto_boost", "masto_resp", "devto_views", "devto_react", "devto_com", "tumblr_posts", "tumblr_notes", "threads_posts", "threads_views", "threads_likes"]
    line = "| " + " | ".join(str(row.get(c, "")) for c in cols) + f" | {nota} |"

    if not MET.exists():
        MET.write_text(
            "# Métricas de marketing — Ceifalume\n\n"
            "Uma linha por medição (`python3 ferramentas/medir-marketing.py --nota \"...\"`). Horário de Fortaleza (UTC-3).\n"
            "Linha de base oficial: **2026-09-17 = 14 views / 1 download / 0 compras** (antes de qualquer marketing).\n\n"
            "| data | itch views | itch downloads | itch compras | APK GitHub | YT views trailer | Bsky seguidores | Bsky posts | Bsky likes | Bsky reposts | Bsky respostas | Masto seguidores | Masto posts | Masto favoritos | Masto boosts | Masto respostas | dev.to views | dev.to reações | dev.to coment. | Tumblr posts | Tumblr notas | Threads posts | Threads views | Threads likes | nota |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
    with MET.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

    # painel humano
    print(f"📊 {row['data']} (Fortaleza)")
    print(f"  itch:     {row['itch_views']} views · {row['itch_dl']} downloads · {row['itch_buy']} compras")
    print(f"  GitHub:   {row['gh_apk']} downloads do APK (Release)")
    print(f"  YouTube:  {row['yt_views']} views no trailer")
    print(f"  Bluesky:  {row['bsky_seg']} seguidores · {row['bsky_posts']} posts · {row['bsky_likes']} likes · {row['bsky_rep']} reposts · {row['bsky_resp']} respostas")
    print(f"  dev.to:   {row['devto_views']} views · {row['devto_react']} reações · {row['devto_com']} comentários")
    print(f"  Tumblr:   {row['tumblr_posts']} posts · {row['tumblr_notes']} notas")
    print(f"  Threads:  {row['threads_posts']} posts · {row['threads_views']} views · {row['threads_likes']} likes")
    print(f"  Mastodon: {row['masto_seg']} seguidores · {row['masto_posts']} posts · {row['masto_fav']} favoritos · {row['masto_boost']} boosts · {row['masto_resp']} respostas")
    # variação vs linha anterior
    lines = [l for l in MET.read_text(encoding="utf-8").splitlines() if l.startswith("| 20")]
    if len(lines) >= 2:
        prev = [c.strip() for c in lines[-2].strip("|").split("|")]
        cur = [c.strip() for c in lines[-1].strip("|").split("|")]
        names = ["", "itch views", "itch downloads", "itch compras", "APK GitHub", "YT views", "Bsky seg", "Bsky posts", "Bsky likes", "Bsky reposts", "Bsky resp", "Masto seg", "Masto posts", "Masto fav", "Masto boosts", "Masto resp", "dev.to views", "dev.to reações", "dev.to coment.", "Tumblr posts", "Tumblr notas", "Threads posts", "Threads views", "Threads likes"]
        deltas = []
        for i in range(1, 24):
            try:
                dlt = int(cur[i]) - int(prev[i])
                if dlt: deltas.append(f"{names[i]} {'+' if dlt > 0 else ''}{dlt}")
            except (ValueError, IndexError): pass
        print("  Δ desde a última medição:", ", ".join(deltas) if deltas else "sem variação")
    print(f"  → gravado em {MET.relative_to(BASE)}")

if __name__ == "__main__":
    main()
