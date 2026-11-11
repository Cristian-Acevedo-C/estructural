// Prueba del cotizador: node herramientas/cotizador_test.mjs  (desde estructural/; usa Playwright de orbe-conecta y Edge)
import {createRequire} from 'node:module';
import {readFileSync, mkdirSync} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
const raiz = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(resolve(raiz, '../orbe-conecta/package.json'));
const {chromium} = require('@playwright/test');
const dir = resolve(raiz, '../insumos/interno_NO_PUBLICAR/cotizador');
const casos = JSON.parse(readFileSync(join(raiz, 'trabajo/cotizador/casos.json'), 'utf8'));
const shots = join(raiz, 'trabajo/cotizador/capturas'); mkdirSync(shots, {recursive:true});
let fallas = 0; const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLA') + ' ' + m); if(!c) fallas++ };
const n = s => +String(s).replace(/[^0-9]/g, '');
let browser; try{ browser = await chromium.launch() }catch(e){ browser = await chromium.launch({channel:'msedge'}) }

async function abrir(archivo, vp){
  const page = await browser.newPage({viewport:{width:vp.w, height:vp.h}});
  const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await page.goto(pathToFileURL(join(dir, archivo)).href);
  return {page, errs};
}
const ESC = {n:'escritorio', w:1280, h:900}, CEL = {n:'celular', w:390, h:844};
const st = page => page.getAttribute('#estado', 'data-st');
const set = (page, o) => page.evaluate(x => __cot.set(x), o);

// ---------- versión interna
{
  const {page, errs} = await abrir('cotizador_interno.html', ESC);
  // 1. seguridad: ningún "se puede cotizar" que el motor exacto no apruebe
  const r = await page.evaluate(cs => cs.map(c => { const p = __cot.D.postes.find(x => x.codigo === c.codigo); const e = __cot.evaluar(p, c.V, c.N, c.kg, c.epa, c.sop); return {...c, st:e.st, F2:e.F, P2:e.P} }), casos);
  ok(r.every(c => Math.abs(c.F - c.F2) <= 1e-9 * Math.max(1, c.F) && Math.abs(c.P - c.P2) <= 1e-9), `fuerza y peso iguales a los de Python en ${r.length} casos`);
  const inseguros = r.filter(c => c.st === 'ok' && c.motor !== 'cumple');
  ok(inseguros.length === 0, `ningún "Puedes cotizarlo" que el motor no apruebe (${r.length} casos) ${JSON.stringify(inseguros.slice(0, 3))}`);
  const tabla = {}; for(const c of r){ const k = `${c.st}/${c.motor}`; tabla[k] = (tabla[k] || 0) + 1 }
  console.log('      cotizador/motor:', JSON.stringify(tabla));
  ok(r.filter(c => c.tipo !== 'tubular').every(c => c.st !== 'ok'), 'cuadrados y facetados nunca salen "Puedes cotizarlo"');
  // 2. datos
  const d = await page.evaluate(() => { const P = __cot.D.postes; return {
    total: P.length, tub: P.filter(p => p.tipo === 'tubular').length, sinCosto: P.filter(p => !(p.costo > 0)).length,
    malSuma: P.filter(p => p.partidas.length && Math.abs(p.partidas.reduce((s, x) => s + x[1], 0) - p.costo_recalculado) > 5).map(p => p.codigo),
    difs: P.filter(p => p.tipo === 'tubular' && !p.costo_origen.startsWith('recalc')).map(p => [p.codigo, p.costo_recalculado / p.costo - 1]),
    cinco: P.filter(p => p.cuerpos > 4).map(p => [p.codigo, __cot.evaluar(p, 130, 1, 5, 0.01, 0).st]) } });
  ok(d.total === 129 && d.tub === 49 && d.sinCosto === 0, `129 postes (49 tubulares), todos con costo`);
  ok(d.malSuma.length === 0, `las partidas suman el costo recalculado ${d.malSuma}`);
  const recalc = await page.evaluate(() => __cot.D.postes.filter(p => p.tipo === 'tubular' && p.costo_origen.startsWith('recalc')).length);
  const todas = await page.evaluate(() => __cot.D.postes.filter(p => p.tipo === 'tubular').map(p => [p.codigo, p.costo_recalculado / p.costo - 1]));
  const fuera = todas.filter(x => Math.abs(x[1]) > 0.05);
  ok(recalc === 0, 'los 49 tubulares usan el costo del recetario (ninguno recalculado)');
  console.log(`      control: recálculo por partidas fuera de ±5 % en ${fuera.length} de 49: ${fuera.map(x => `${x[0]} ${(x[1] * 100).toFixed(0)} %`).join(', ')}`);
  ok(d.cinco.length === 6 && d.cinco.every(x => x[1] === 'eng'), `los ${d.cinco.length} tubulares de 5 cuerpos van a revisión técnica`);
  // 3. valores por omisión seguros
  await page.evaluate(() => localStorage.clear()); await page.reload();
  const s0 = await page.evaluate(() => ({...__cot.estado(), V: __cot.V()}));
  ok(s0.zona === 'nose' && s0.V === 150 && s0.M === 0.3 && s0.eq === 'vial' && s0.Q === 1, 'por omisión: "No sé la comuna" (150 km/h), margen 30 %, 1 luminaria de calle');
  const velocidades = await page.evaluate(() => [...document.querySelectorAll('[name=zona]')].map(i => i.closest('label').innerText).join(' '));
  ok(!/100 km|110 km|120 km/.test(velocidades), 'no se ofrecen vientos menores a 130 km/h');
  // 4. precio, IVA, despacho y margen con ITUB6B
  await set(page, {poste:'ITUB6B', Q:1, N:1, eq:'vial', KG:15, EPA:0.1, zona:'nose', brazo:false, FL:false, M:0.3});
  const costo = n(await page.textContent('#costo')), unit = n(await page.textContent('#unit'));
  ok(costo === 97138 && Math.abs(unit - costo / 0.7) <= 1, `ITUB6B: costo ${costo} (el del recetario) y precio ${unit} = costo ÷ 0,70`);
  await page.click('[data-pm="fQ,1"]'); await page.fill('#fQ', '10');
  const neto = n(await page.textContent('#neto')), iva = n(await page.textContent('#iva')), tot = n(await page.textContent('#total'));
  ok(Math.abs(neto - 10 * costo / 0.7) <= 2 && Math.abs(iva - neto * 0.19) <= 2 && Math.abs(tot - neto - iva) <= 2, `10 postes: neto ${neto} + IVA ${iva} = ${tot}`);
  await page.check('#fFlete'); ok(n(await page.textContent('#total')) - tot === 80000, 'despacho en Santiago suma $80.000');
  await page.uncheck('#fFlete'); await page.locator('[name=margen][value="0.4"]').check({force:true});
  ok(Math.abs(n(await page.textContent('#unit')) - costo / 0.6) <= 1, 'margen 40 %: precio = costo ÷ 0,60');
  // 5. a prueba de errores
  await set(page, {M:0.3, Q:1});
  ok(await st(page) === 'ok', 'ITUB6B con 1 luminaria de calle: se puede cotizar');
  await page.check('#fBrazo'); ok(await st(page) === 'eng', 'con brazo, gancho o cruceta: siempre revisión técnica');
  await page.uncheck('#fBrazo');
  for(const [campo, valor, texto] of [['#fQ', '', 'cuántos postes'], ['#fQ', '0', 'cuántos postes'], ['#fQ', '2.5', 'sin decimales'], ['#fQ', '-3', 'cuántos postes'], ['#fN', '0', 'al menos 1'], ['#fN', '40', 'Más de 12']]){
    await page.fill(campo, valor);
    const e = await st(page), msg = await page.textContent(campo === '#fQ' ? '#eQ' : '#eN');
    ok(e === 'err' && msg.includes(texto) && await page.locator('#total').count() === 0, `"${valor}" en ${campo}: no muestra precio y explica ("${msg}")`);
    await page.fill(campo, '1');
  }
  await page.locator('[name=eq][value="ficha"]').check({force:true});
  for(const [campo, valor, texto] of [['#fEpa', '', 'metros cuadrados'], ['#fEpa', '1500', 'cm²'], ['#fEpa', '-1', 'metros cuadrados'], ['#fKg', '0', 'peso en kilos'], ['#fKg', '900', 'Más de 150']]){
    await page.fill(campo, valor);
    const msg = await page.textContent(campo === '#fEpa' ? '#eEpa' : '#eKg');
    ok(await st(page) === 'err' && msg.includes(texto), `"${valor}" en ${campo}: bloquea y explica ("${msg}")`);
    await page.fill(campo, campo === '#fEpa' ? '0.1' : '15');
  }
  await page.fill('#fEpa', '0,12'); ok((await page.evaluate(() => __cot.estado().EPA)) === 0.12 && await st(page) !== 'err', 'acepta coma decimal (0,12)');
  await page.fill('#fEpa', '1.5'); ok(/Seguro/.test(await page.textContent('#eEpa')) && await st(page) !== 'err', 'EPA 1,5 m²: avisa, pero deja seguir');
  // más viento o más equipos nunca mejora el resultado
  const orden = {ok:0, eng:1, no:2};
  await set(page, {poste:'ITUB9A', eq:'ficha', KG:15, EPA:0.15, N:1, zona:'normal'}); const a = await st(page);
  await set(page, {zona:'expuesto'}); const b = await st(page);
  await set(page, {N:4}); const c = await st(page);
  ok(orden[a] <= orden[b] && orden[b] <= orden[c], `ITUB9A: normal "${a}" → expuesto "${b}" → 4 equipos "${c}"`);
  ok(await page.locator('[data-alt]').count() > 0 || /Ninguno/.test(await page.textContent('#alt')), 'si no sirve, propone postes que sí o lo dice');
  // copiar: el texto de cotización no lleva costos
  await set(page, {poste:'ITUB6B', eq:'vial', KG:15, EPA:0.1, N:1, zona:'nose', Q:2});
  await page.evaluate(() => { window.__txt = null; Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText: t => { window.__txt = t; return Promise.resolve() }}}) });
  await page.click('#bCopiar'); const txt = await page.evaluate(() => window.__txt);
  ok(/COTIZACIÓN ORBE/.test(txt) && /TOTAL: \$/.test(txt) && !/costo|margen/i.test(txt), 'el texto copiado trae el total y no menciona costos ni margen');
  // 6. accesorios del recetario
  const A = await page.evaluate(() => ({n: __cot.D.accesorios.length, conCosto: __cot.D.accesorios.filter(a => a.costo > 0).length, des: [...document.querySelectorAll('#fAcc option[disabled]')].length}));
  ok(A.n === 77 && A.conCosto === 56 && A.des === 21, `77 accesorios: 56 con precio y 21 "sin precio" que no se pueden elegir`);
  await set(page, {poste:'ITUB6B', eq:'vial', KG:15, EPA:0.1, N:1, zona:'nose', Q:2, M:0.3, acc:[], brazo:false, FL:false});
  const base = n(await page.textContent('#neto'));
  await page.selectOption('#fAcc', 'AC72'); await page.click('#bAcc'); await page.click('[data-acc="AC72,1"]');
  ok(n(await page.textContent('#neto')) === Math.round(base + 2 * 2 * 18235 / 0.7) && await st(page) === 'ok', 'placa + canastillo AC72 × 2 por poste: suma al neto y no cambia el resultado');
  await page.selectOption('#fAcc', 'BR1*1000-2'); await page.click('#bAcc');
  ok(await st(page) === 'eng' && await page.isDisabled('#fBrazo') && await page.isChecked('#fBrazo'), 'al agregar un brazo (BR1*1000-2) pasa a revisión técnica y marca la casilla de brazo');
  ok(n(await page.textContent('#accs')) === Math.round(2 * 18235 / 0.7 + 10052 / 0.7), 'accesorios por poste = suma de sus precios');
  await page.click('[data-acc="BR1*1000-2,-1"]'); ok(await st(page) === 'ok' && !(await page.isDisabled('#fBrazo')), 'al quitar el brazo vuelve a "Puedes cotizarlo"');
  await page.click('#bAcc'); ok((await page.evaluate(() => __cot.estado().acc.length)) === 1, '"Agregar" sin elegir accesorio no agrega nada');
  await page.click('#bCopiar'); const txt2 = await page.evaluate(() => window.__txt);
  ok(/Accesorio por poste: 2 × AC72/.test(txt2) && !/costo|margen/i.test(txt2), 'la cotización copiada lista los accesorios, sin costos');
  await page.click('#bReset'); ok((await page.evaluate(() => __cot.estado().acc.length)) === 0 && (await page.evaluate(() => __cot.estado().Q)) === 1 && await st(page) !== 'err', '"Empezar de nuevo" vuelve a los valores iniciales');
  await set(page, {poste:'ITUB6B'});
  await page.screenshot({path: join(shots, 'interno-escritorio.png'), fullPage: true});
  ok(errs.length === 0, `[interno] sin errores de consola ${errs.join(' | ')}`);
  await page.close();
}
// ---------- versión de vendedores: sin costos en ninguna parte
{
  const html = readFileSync(join(dir, 'cotizador_vendedores.html'), 'utf8');
  const datos = html.slice(html.indexOf('const D = '), html.indexOf('const INT'));
  ok(!/"costo|"partidas"|galvanizado|Acero \(|"margenes":\[0/.test(datos), 'vendedores: los datos del archivo no contienen costos, partidas ni márgenes');
  for(const vp of [ESC, CEL]){
    const {page, errs} = await abrir('cotizador_vendedores.html', vp);
    await set(page, {poste:'ITUB6B'});
    await page.locator('details').last().evaluate(d => d.open = true);
    const visible = await page.evaluate(() => document.body.innerText);
    ok(!/costo|margen/i.test(visible) && await page.locator('#fM').count() === 0 && await page.locator('#costo').count() === 0, `[vendedores ${vp.n}] no muestra costo ni margen`);
    ok(n(await page.textContent('#unit')) === Math.round(97138 / 0.7), `[vendedores ${vp.n}] precio ITUB6B = ${Math.round(97138 / 0.7)}`);
    const ov = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    ok(ov <= 0, `[vendedores ${vp.n}] sin scroll horizontal`);
    const chicos = await page.evaluate(() => [...document.querySelectorAll('button,select,input[type=number],label.opt,label.chk')].filter(e => e.offsetParent && e.getBoundingClientRect().height < 38).length);
    ok(chicos === 0, `[vendedores ${vp.n}] todos los controles miden 38 px o más de alto`);
    await page.locator('details').last().evaluate(d => d.open = false);
    await page.screenshot({path: join(shots, `vendedores-${vp.n}.png`), fullPage: true});
    ok(errs.length === 0, `[vendedores ${vp.n}] sin errores de consola ${errs.join(' | ')}`);
    await page.close();
  }
}
await browser.close();
console.log(fallas ? `\n${fallas} FALLAS` : '\nTODO OK'); process.exit(fallas ? 1 : 0);
