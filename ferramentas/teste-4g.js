const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  async function cenario(nome, redes) {
    const ctx = await browser.createBrowserContext();
    const page = await ctx.newPage();
    const cdp = await page.createCDPSession();
    await page.setViewport({ width: 844, height: 390, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
    let bytes = 0;
    page.on('response', async r => { try { const h = r.headers(); bytes += parseInt(h['content-length'] || '0', 10); } catch (e) {} });
    if (redes) await cdp.send('Network.emulateNetworkConditions', redes);
    const t0 = Date.now();
    await page.goto('http://127.0.0.1:8099/ceifalume/index.html', { waitUntil: 'domcontentloaded', timeout: 300000 });
    // espera o motor assumir a tela (o overlay #status some quando o jogo sobe)
    let pronto = false, tPronto = 0;
    for (let i = 0; i < 900; i++) {
      pronto = await page.evaluate(() => { const s = document.getElementById('status'); return !s || getComputedStyle(s).display === 'none'; });
      if (pronto) { tPronto = Date.now() - t0; break; }
      await new Promise(r => setTimeout(r, 500));
    }
    const fps = await page.evaluate(() => new Promise(res => { const t = []; let u = performance.now(), n = 0;
      function loop(){ const a = performance.now(); t.push(a-u); u=a; if (++n < 60) requestAnimationFrame(loop);
        else { const s = t.sort((x,y)=>x-y); res(+(1000/s[Math.floor(s.length/2)]).toFixed(1)); } } requestAnimationFrame(loop); }));
    console.log(JSON.stringify({ cenario: nome, motor_pronto_em_s: +(tPronto/1000).toFixed(1), bytes_anunciados_na_carga_MB: +(bytes/1048576).toFixed(2), fps: fps, carregou: pronto }));
    await ctx.close();
  }
  await cenario('rede normal (sandbox)', null);
  await cenario('4G ~6 Mbps, 120 ms', { offline: false, latency: 120, downloadThroughput: 6e6/8, uploadThroughput: 1.5e6/8 });
  await cenario('3G lento ~1.6 Mbps, 300 ms', { offline: false, latency: 300, downloadThroughput: 1.6e6/8, uploadThroughput: 400e3/8 });
  await browser.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
