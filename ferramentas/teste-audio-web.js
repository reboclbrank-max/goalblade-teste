// O AudioContext no navegador mobile nasce suspenso até existir gesto do usuário.
// Se o jogo chamar play() nesse intervalo, nada toca e nada quebra — é o defeito
// silencioso clássico. Aqui eu conto os contextos e leio o estado antes/depois do toque.
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=document-user-activation-required',
           '--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  const ctx = await b.createBrowserContext(); const page = await ctx.newPage();
  await page.setViewport({ width: 844, height: 390, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await page.evaluateOnNewDocument(() => {
    window.__actx = [];
    const Orig = window.AudioContext || window.webkitAudioContext;
    function Fake(...a) { const c = new Orig(...a); window.__actx.push(c); return c; }
    Fake.prototype = Orig.prototype;
    window.AudioContext = Fake; window.webkitAudioContext = Fake;
  });
  const avisos = [];
  page.on('console', m => { if (/audio|autoplay|gesture/i.test(m.text())) avisos.push(m.text().slice(0, 90)); });
  await page.goto('http://127.0.0.1:8099/ceifalume/index.html', { waitUntil: 'domcontentloaded', timeout: 300000 });
  for (let i = 0; i < 600; i++) {
    const pronto = await page.evaluate(() => { const s = document.getElementById('status'); return !s || getComputedStyle(s).display === 'none'; });
    if (pronto) break;
    await new Promise(r => setTimeout(r, 250));
  }
  const antes = await page.evaluate(() => ({ n: window.__actx.length, estados: window.__actx.map(c => c.state) }));
  // um toque real no canvas (o gesto que libera o áudio)
  const r = await page.evaluate(() => { const b = document.getElementById('canvas').getBoundingClientRect(); return { x: b.x + b.width * 0.6, y: b.y + b.height * 0.7 }; });
  await page.touchscreen.tap(r.x, r.y);
  await new Promise(res => setTimeout(res, 2500));
  const depois = await page.evaluate(() => ({ n: window.__actx.length, estados: window.__actx.map(c => c.state) }));
  console.log(JSON.stringify({ contextos_antes: antes, contextos_depois_do_toque: depois, avisos: avisos.slice(0, 3) }));
  await b.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
