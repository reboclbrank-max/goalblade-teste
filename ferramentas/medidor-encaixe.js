const puppeteer = require('puppeteer-core');
const URL = 'http://127.0.0.1:8099/ceifalume/index.html';
(async () => {
  const browser = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  for (const [nome, w, h] of [['celular-deitado', 844, 390], ['celular-retrato', 390, 844], ['desktop', 1280, 720]]) {
    const ctx = await browser.createBrowserContext();      // contexto limpo: sem zoom lembrado
    const page = await ctx.newPage();
    const erros = [], falhas = [];
    page.on('pageerror', e => erros.push(String(e.message || e)));
    page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text()); });
    page.on('requestfailed', r => falhas.push(r.url()));
    await page.setViewport({ width: w, height: h, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
    await page.goto(URL, { waitUntil: 'load', timeout: 120000 });
    await new Promise(r => setTimeout(r, 40000));
    const m = await page.evaluate(() => {
      const c = document.getElementById('canvas'), a = document.getElementById('rd-arena');
      const r = c.getBoundingClientRect(), ari = a.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      return {
        quadro_css: [Math.round(r.width), Math.round(r.height)],
        topo: Math.round(r.top), base: Math.round(r.bottom), esquerda: Math.round(r.left), direita: Math.round(r.right),
        caixa: [Math.round(ari.width), Math.round(ari.height)],
        cabe_inteiro: r.top >= ari.top - 0.5 && r.bottom <= ari.bottom + 0.5 && r.left >= ari.left - 0.5 && r.right <= ari.right + 0.5,
        precisa_rolar: a.scrollWidth > a.clientWidth + 1 || a.scrollHeight > a.clientHeight + 1,
        escala_do_jogo: +(r.width / 1280).toFixed(3),
        px_reais_de_17: +(17 * (r.width / 1280) * dpr).toFixed(1),
        motor_rodando: !document.getElementById('status') || getComputedStyle(document.getElementById('status')).display === 'none',
        selo: (document.querySelector('.rd-selo') || {}).textContent,
      };
    });
    await page.screenshot({ path: `/home/user/tools/renders/final-${nome}.png` });
    console.log(nome, JSON.stringify({ ...m, erros_js: erros.slice(0, 3), pedidos_quebrados: falhas.slice(0, 3) }));
    await ctx.close();
  }
  await browser.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
