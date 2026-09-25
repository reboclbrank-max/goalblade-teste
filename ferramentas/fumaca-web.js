// CEIFALUME — fumaça da versão web (ferramenta, não é o jogo)
// Sobe o export web no Chromium, clica Jogar → tutorial → planta,
// e prova: zero erro de página, tela viva (pixels mudam), áudio
// destravado após o gesto (AudioContext running).
// Uso: servir export/web em /ceifalume (porta 8099) e rodar:
//   node tools/fumaca-web.js
const puppeteer = require('puppeteer-core');
const fs = require('fs');
(async () => {
  const browser = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--autoplay-policy=document-user-activation-required',
           '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--mute-audio'] });
  const page = await (await browser.createBrowserContext()).newPage();
  await page.setViewport({ width: 1280, height: 720 });
  await page.evaluateOnNewDocument(() => {
    window.__actx = [];
    const Orig = window.AudioContext || window.webkitAudioContext;
    function Fake(...a) { const c = new Orig(...a); window.__actx.push(c); return c; }
    Fake.prototype = Orig.prototype;
    window.AudioContext = Fake; window.webkitAudioContext = Fake;
  });
  const erros = [];
  page.on('pageerror', e => erros.push('pageerror: ' + String(e).slice(0, 120)));
  page.on('console', m => { if (m.type() === 'error') erros.push('console: ' + m.text().slice(0, 120)); });
  await page.goto('http://127.0.0.1:8099/ceifalume/index.html', { waitUntil: 'load', timeout: 120000 });
  // espera o motor assumir (overlay #status some)
  await page.waitForFunction(() => { const s = document.getElementById('status'); return !s || s.style.display === 'none'; }, { timeout: 120000 });
  await new Promise(r => setTimeout(r, 6000)); // abertura (3s) + título
  await page.screenshot({ path: '/tmp/web-titulo.png' });
  const audioAntes = await page.evaluate(() => window.__actx.map(c => c.state));
  // Jogar (centro-x, ~68% altura) = primeiro gesto
  await page.mouse.click(640, 490);
  await new Promise(r => setTimeout(r, 3000)); // fazenda + tutorial
  await page.screenshot({ path: '/tmp/web-tutorial.png' });
  // "Entendi, jogar!" (centro ~50%, ~53%)
  await page.mouse.click(640, 330);
  await new Promise(r => setTimeout(r, 1000));
  // semente Nabo (~34%, ~16%) + primeiro campo (~40%, ~36%)
  await page.mouse.click(435, 115);
  await new Promise(r => setTimeout(r, 500));
  await page.mouse.click(508, 256);
  await new Promise(r => setTimeout(r, 2500));
  await page.screenshot({ path: '/tmp/web-jogo.png' });
  const audioDepois = await page.evaluate(() => window.__actx.map(c => c.state));
  const b1 = fs.readFileSync('/tmp/web-titulo.png');
  const b2 = fs.readFileSync('/tmp/web-jogo.png');
  const resumo = { erros: erros.slice(0, 8), nErros: erros.length,
    tituloBytes: b1.length, jogoBytes: b2.length,
    telasDiferentes: !b1.equals(b2), audioAntes, audioDepois };
  console.log('FUMACA-WEB: ' + JSON.stringify(resumo));
  await browser.close();
  process.exit(erros.length === 0 && resumo.telasDiferentes ? 0 : 1);
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
