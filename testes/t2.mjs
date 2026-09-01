import { JSDOM } from 'jsdom';
import fs from 'fs';
const html = fs.readFileSync('../index.html', 'utf8');
function novo(){
  const dom = new JSDOM(html, { runScripts:'dangerously', pretendToBeVisual:true, url:'https://exemplo.local/' });
  dom.window.scrollTo = () => {};
  return dom;
}
const dom = novo(); const w = dom.window, d = w.document;
const $ = s => d.querySelector(s), $$ = s => [...d.querySelectorAll(s)];
const click = el => el.dispatchEvent(new w.MouseEvent('click', {bubbles:true}));
const erros = []; w.addEventListener('error', e => erros.push(e.message));

console.log('1. total inicial      :', $('#btn-comecar').textContent.trim());
// troca para espanhol
click($$('#escolha-lingua .escolha').find(b=>b.dataset.valor==='esp'));
click($$('#escolha-modo .escolha').find(b=>b.dataset.valor==='disciplina'));
click($$('#escolha-disciplina .escolha').find(b=>b.dataset.valor.includes('Espanhola')));
console.log('2. espanhol           :', $('#btn-comecar').textContent.trim());
click($('#btn-comecar'));
console.log('3. 1º item espanhol   :', $('#enunciado').textContent.slice(0,55));
console.log('4. texto de apoio     :', $('#texto-apoio').textContent.slice(0,45).replace(/\n/g,' '));
console.log('5. apoio aberto?      :', $('#bloco-apoio').open, '| resumo:', $('#bloco-apoio summary').textContent);

// item ESP1 é anulado: responde e confere
click($('#area-julgamento .botao[data-resposta="C"]'));
console.log('6. veredito anulado   :', $('#area-resposta .veredito').textContent);
console.log('7. classe             :', $('#area-resposta .resultado').className);

// erra alguns e testa "refazer erradas"
for(let i=0;i<7;i++){ click($('#btn-proxima')); const b=$('#area-julgamento .botao[data-resposta="C"]'); if(b) click(b); }
click($('#btn-relatorio'));
console.log('8. placar espanhol    :', $('#placar').textContent.replace(/\s+/g,' ').trim());
console.log('9. refazer habilitado :', !$('#btn-refazer-erradas').disabled);
click($('#btn-refazer-erradas'));
console.log('10. refazendo         :', $('#posicao').textContent, '|', $('#trilha').textContent.replace(/\s+/g,' ').trim().slice(0,40));

// persistência: nova instância reaproveita
const salvo = w.localStorage.getItem('prf2021.simulado.v1');
console.log('11. localStorage      :', salvo ? Math.round(salvo.length/1024)+' KB gravados' : 'NADA');

// modo correção final
const dom2 = novo(); const w2 = dom2.window, d2 = dom2.window.document;
w2.localStorage.clear();
const $b = s => d2.querySelector(s), $$b = s => [...d2.querySelectorAll(s)];
const clickb = el => el.dispatchEvent(new w2.MouseEvent('click', {bubbles:true}));
clickb($$b('#escolha-correcao .escolha').find(b=>b.dataset.valor==='final'));
clickb($$b('#escolha-modo .escolha').find(b=>b.dataset.valor==='bloco'));
clickb($$b('#escolha-bloco .escolha').find(b=>b.dataset.valor==='BLOCO III'));
clickb($b('#btn-comecar'));
const antes = $b('#posicao').textContent;
clickb($b('#area-julgamento .botao[data-resposta="C"]'));
console.log('12. correção final    : sem revelar =', $b('#area-resposta').classList.contains('oculto'), '| avançou:', antes, '->', $b('#posicao').textContent);
console.log('\nerros de runtime:', erros.length ? erros : 'nenhum');
