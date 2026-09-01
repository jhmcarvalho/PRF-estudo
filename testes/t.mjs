import { JSDOM } from 'jsdom';
import fs from 'fs';
const html = fs.readFileSync('../index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://exemplo.local/' });
const { window } = dom;
const d = window.document;
const erros = [];
window.addEventListener('error', e => erros.push(String(e.error && e.error.stack || e.message)));

const $ = s => d.querySelector(s);
const click = el => el.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));

console.log('config visível:', !$('#tela-config').classList.contains('oculto'));
console.log('botão começar   :', $('#btn-comecar').textContent.trim());

// modo bloco II
click([...d.querySelectorAll('#escolha-modo .escolha')].find(b => b.dataset.valor === 'bloco'));
click([...d.querySelectorAll('#escolha-bloco .escolha')].find(b => b.dataset.valor === 'BLOCO II'));
console.log('bloco II        :', $('#btn-comecar').textContent.trim());

click($('#btn-comecar'));
console.log('tela questão    :', !$('#tela-questao').classList.contains('oculto'));
console.log('trilha          :', $('#trilha').textContent.replace(/\s+/g,' ').trim());
console.log('comando         :', $('#comando').textContent.slice(0,60));
console.log('enunciado       :', $('#enunciado').textContent.slice(0,60));

// responde item 56 (gabarito C) errado de propósito
click(d.querySelector('#area-julgamento .botao[data-resposta="E"]'));
console.log('resposta visível:', !$('#area-resposta').classList.contains('oculto'));
console.log('veredito        :', $('#area-resposta .veredito').textContent);
console.log('fundamentos     :', d.querySelectorAll('#area-resposta .fundamentos li').length);

// segue e acerta o próximo (57 = C)
click($('#btn-proxima'));
click(d.querySelector('#area-julgamento .botao[data-resposta="C"]'));
console.log('veredito 57     :', $('#area-resposta .veredito').textContent);

// pula para o relatório
click($('#btn-relatorio'));
console.log('relatório       :', !$('#tela-relatorio').classList.contains('oculto'));
console.log('placar          :', $('#placar').textContent.replace(/\s+/g,' ').trim());
console.log('temas linhas    :', d.querySelectorAll('#tabela-temas tbody tr').length);
console.log('revisão itens   :', d.querySelectorAll('#lista-revisao button').length);
console.log('\nerros de runtime:', erros.length ? erros : 'nenhum');
