const puppeteer = require('puppeteer-core');
const URLS = process.argv.slice(2);
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  for (const url of URLS) {
    const ctx = await b.createBrowserContext(); const page = await ctx.newPage();
    await page.setViewport({ width: 844, height: 390, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
    const t0 = Date.now();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 300000 });
    let pronto = false, tPronto = 0;
    for (let i = 0; i < 1200; i++) {
      pronto = await page.evaluate(() => { const s = document.getElementById('status'); return !s || getComputedStyle(s).display === 'none'; }).catch(() => false);
      if (pronto) { tPronto = Date.now() - t0; break; }
      await new Promise(r => setTimeout(r, 250));
    }
    const fps = await page.evaluate(() => new Promise(res => { const t = []; let u = performance.now(), n = 0;
      (function loop(){ const a = performance.now(); t.push(a-u); u=a; if (++n < 90) requestAnimationFrame(loop);
        else { const s = t.sort((x,y)=>x-y); res(+(1000/s[Math.floor(s.length/2)]).toFixed(1)); } })(); }));
    const quadro = await page.evaluate(() => { const r = document.getElementById('canvas').getBoundingClientRect(); return Math.round(r.width)+'x'+Math.round(r.height); });
    console.log(JSON.stringify({ url: url.split('/').slice(-2)[0], motor_pronto_ms: tPronto, fps_llvmpipe: fps, quadro, carregou: pronto }));
    await ctx.close();
  }
  await b.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
