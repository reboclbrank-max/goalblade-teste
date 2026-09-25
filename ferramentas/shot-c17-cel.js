// Foto C.17 no perfil do dono: celular deitado 844x390 até o jogo.
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  const page = await b.newPage();
  const erros = [];
  page.on('pageerror', e => erros.push(String(e.message || e)));
  await page.setViewport({ width: 844, height: 390, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await page.goto('http://127.0.0.1:8099/ceifalume/index.html', { waitUntil: 'load', timeout: 120000 });
  await new Promise(r => setTimeout(r, 45000));
  await page.screenshot({ path: '/home/user/tools/renders/web-c17-cel-titulo.png' });
  await page.touchscreen.tap(347, 249); // Jogar em escala 0.542
  await new Promise(r => setTimeout(r, 8000));
  await page.screenshot({ path: '/home/user/tools/renders/web-c17-cel-jogo.png' });
  console.log('erros_js:', JSON.stringify(erros));
  await b.close();
})().catch(e => { console.error('SHOT CEL FALHOU:', e.message); process.exit(1); });
