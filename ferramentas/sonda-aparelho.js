// O que um "painel de diagnóstico" conseguiria ler NO CELULAR dele — testado aqui
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: '/usr/bin/chromium', headless: 'new',
    args: ['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage();
  await p.setContent('<canvas id=c></canvas>');
  const s = await p.evaluate(() => {
    const c = document.getElementById('c');
    const gl = c.getContext('webgl2');
    const ext = gl && gl.getExtension('WEBGL_debug_renderer_info');
    const caps = gl ? gl.getParameter(gl.MAX_TEXTURE_SIZE) : 0;
    const mem = gl ? gl.getExtension('WEBGL_memory_info') : null;
    return {
      gpu_relatada: ext && gl ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : '(sem extensão)',
      versao: gl ? gl.getParameter(gl.VERSION) : 'sem WebGL2',
      max_textura: caps,
      deviceMemory_GB: navigator.deviceMemory ?? 'inexistente neste navegador',
      conexao: navigator.connection ? navigator.connection.effectiveType + '/' + navigator.connection.downlink + 'Mbps' : 'inexistente',
      cores: navigator.hardwareConcurrency ?? 'n/a',
      dpr: window.devicePixelRatio,
      tela: screen.width + 'x' + screen.height,
      memoria_js_MB: performance.memory ? +(performance.memory.usedJSHeapSize / 1048576).toFixed(1) : 'só Chromium',
      fullscreen_suportado: !!(document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen),
      apple_pwa: 'onappinstalled' in window || 'onbeforeinstallprompt' in window,
    };
  });
  console.log(JSON.stringify(s, null, 1));
  await b.close();
})().catch(e => { console.error('FALHOU:', e.message); process.exit(1); });
