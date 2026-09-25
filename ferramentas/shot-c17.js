// Fotos C.17 no navegador real: abertura -> título -> (clique Jogar) -> jogo.
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--mute-audio'] });
  const page = await b.newPage();
  const erros = [];
  page.on('pageerror', e => erros.push(String(e.message || e)));
  page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 120)); });
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto('http://127.0.0.1:8099/ceifalume/index.html', { waitUntil: 'load', timeout: 120000 });
  await new Promise(r => setTimeout(r, 45000));
  await page.screenshot({ path: '/home/user/tools/renders/web-c17-abertura.png' });
  await new Promise(r => setTimeout(r, 6000));
  await page.screenshot({ path: '/home/user/tools/renders/web-c17-titulo.png' });
  await page.mouse.click(640, 460); // BotaoJogar (calculado do titulo.tscn)
  await new Promise(r => setTimeout(r, 8000));
  await page.screenshot({ path: '/home/user/tools/renders/web-c17-jogo.png' });
  console.log('erros_js:', JSON.stringify(erros));
  await b.close();
})().catch(e => { console.error('SHOT FALHOU:', e.message); process.exit(1); });
