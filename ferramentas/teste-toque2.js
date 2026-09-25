const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  const ctx = await browser.createBrowserContext();
  const page = await ctx.newPage();
  await page.setViewport({ width: 844, height: 390, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await page.goto('http://127.0.0.1:8099/ceifalume/index.html', { waitUntil: 'load', timeout: 120000 });
  await new Promise(r => setTimeout(r, 40000));
  const q = await page.evaluate(() => { const r = document.getElementById('canvas').getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; });
  const clip = { x: q.x, y: q.y, width: q.w, height: q.h };
  // 1) CONTROLE: duas fotos sem nenhum toque (a animação do dia se move sozinha)
  await page.screenshot({ path: '/tmp/c1.png', clip }); await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: '/tmp/c2.png', clip });
  // 2) TOQUE no centro do primeiro cartão de campo (x ~ 0,34 do quadro, y ~ 0,34)
  const alvo = { x: q.x + q.w * 0.34, y: q.y + q.h * 0.34 };
  await page.touchscreen.tap(alvo.x, alvo.y);
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: '/tmp/d2.png', clip });
  console.log(JSON.stringify({ quadro: q, alvo }));
  await browser.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
