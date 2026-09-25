const puppeteer = require('puppeteer-core');
const URL = 'http://127.0.0.1:8099/ceifalume/index.html';

async function perfil(browser, nome, w, h, zoomes) {
  const page = await browser.newPage();
  const erros = [], falhas = [];
  page.on('pageerror', e => erros.push(String(e.message || e)));
  page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text()); });
  page.on('requestfailed', r => falhas.push(r.url() + ' :: ' + (r.failure() || {}).errorText));
  await page.setViewport({ width: w, height: h, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await page.goto(URL, { waitUntil: 'load', timeout: 120000 });
  await new Promise(r => setTimeout(r, 45000));   // carregar 35 MB de wasm e iniciar

  const mede = () => page.evaluate(() => {
    const c = document.getElementById('canvas'), a = document.getElementById('rd-arena');
    const r = c.getBoundingClientRect();
    return {
      tela_css: r.width, altura_css: r.height, x: Math.round(r.x), y: Math.round(r.y),
      buffer: c.width + 'x' + c.height,
      escala: +(r.width / c.width).toFixed(3),
      arena: a ? a.className : 'AUSENTE',
      rolagem: a ? (a.scrollWidth + 'x' + a.scrollHeight + ' em caixa ' + a.clientWidth + 'x' + a.clientHeight) : '',
      status_ainda_ali: !!document.getElementById('status') && getComputedStyle(document.getElementById('status')).display !== 'none',
      selo: (document.querySelector('.rd-selo') || {}).textContent || '(sem selo)',
      botao_zoom: !!document.getElementById('rd-zoom'),
      WebGL2: (() => { try { return !!document.createElement('canvas').getContext('webgl2'); } catch (e) { return false; } })(),
    };
  });

  const base = await mede();
  await page.screenshot({ path: `/home/user/tools/renders/pagina-${nome}.png` });
  const resultados = [{ zoom: '1x', ...base }];

  for (let i = 0; i < zoomes; i++) {
    await page.evaluate(() => { const b = document.getElementById('rd-zoom'); if (b) b.click(); });
    await new Promise(r => setTimeout(r, 2500));
    resultados.push({ ...await mede(), });
    await page.screenshot({ path: `/home/user/tools/renders/pagina-${nome}-zoom${i + 2}.png` });
  }
  // toque no centro do quadro: o motor tem de receber a coordenada certa
  const toque = await page.evaluate(() => {
    const r = document.getElementById('canvas').getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  });
  await page.touchscreen.tap(toque.x, toque.y);
  await new Promise(r => setTimeout(r, 1200));

  console.log(JSON.stringify({ nome, viewport: w + 'x' + h, medidas: resultados, erros_js: erros.slice(0, 6), pedidos_que_falharam: falhas.slice(0, 6) }, null, 1));
  await page.close();
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader',
           '--enable-unsafe-swiftshader', '--mute-audio', '--autoplay-policy=no-user-gesture-required'],
  });
  await perfil(browser, 'celular-retrato', 390, 844, 2);
  await perfil(browser, 'celular-deitado', 844, 390, 2);
  await perfil(browser, 'desktop', 1280, 720, 0);
  await browser.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
