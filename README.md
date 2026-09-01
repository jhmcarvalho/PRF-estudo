# Quilometragem PRF 2021

Simulado comentado da prova objetiva do concurso da Polícia Rodoviária Federal
(Edital nº 1, de 18 de janeiro de 2021 — banca CEBRASPE), montado para estudo pessoal.

Abra o arquivo **`index.html`** no navegador. Não precisa de servidor, internet ou instalação —
só as fontes tipográficas são baixadas do Google Fonts (sem elas a página continua legível).
O progresso fica salvo no próprio navegador (`localStorage`).

## O que tem dentro

- **128 itens**: os 112 itens comuns (9 a 120) mais os 8 itens de inglês e os 8 de espanhol,
  que na prova real eram alternativos. Você escolhe o caderno de língua no início.
- **Gabarito oficial definitivo** da banca, incluindo os **10 itens anulados**
  (39, 45, 67, 69, 76, 83, 89, 98, 99 do caderno comum + item 1 de cada caderno de língua).
- **Explicação para cada item**, com o dispositivo que resolve a questão e link para a fonte.
- **Aviso de norma revogada** nos itens cuja base legal mudou depois de 2021 — útil justamente
  porque o objetivo é a *próxima* prova.
- **Diagnóstico final**: acertos, erros, saldo (C − E, como a banca corrige), desempenho por
  disciplina e ranking de temas por taxa de erro.
- Modos: prova inteira, um bloco por vez, disciplinas escolhidas, ou só os itens que você errou.

## De onde vieram os dados

Enunciados, textos de apoio, figura e gabaritos foram **extraídos programaticamente** dos PDFs
oficiais do CEBRASPE (nada foi redigitado, para não introduzir erro de transcrição):

| Documento | Arquivo oficial |
|---|---|
| Caderno de prova (itens 9–120) | `578_PRF_001_01.PDF` |
| Caderno de língua inglesa (1–8) | `578_PRF_ING_01.PDF` |
| Caderno de língua espanhola (1–8) | `578_PRF_ESP_02.PDF` |
| Gabaritos oficiais definitivos | `GAB_DEFINITIVO_578_PRF_*.PDF` |

Todos em `https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/`.

**Sobre as explicações:** o CEBRASPE não publica comentário item a item — divulga apenas o
gabarito e as anulações. As explicações deste site foram escritas por mim a partir da norma
que resolve cada item, sempre verificada no texto oficial e citada com link: Constituição,
CTB, leis e decretos (Planalto), resoluções do CONTRAN (repositório do Ministério dos
Transportes), Manual de Redação da Presidência da República (3ª edição), REGIC 2018 (IBGE),
NIST, CERT.br e julgados do STF. O corpus baixado está em `fontes/` (33 MB — pode apagar
sem quebrar o site).

## Estrutura

```
index.html          site pronto para uso (dados embutidos)
artefato.html       mesma página no formato publicado na web
src/corpo.html      template: HTML, CSS e JavaScript da página
dados/
  itens_*.json      itens extraídos dos PDFs oficiais
  gabaritos.json    gabaritos oficiais definitivos
  exp_*.json        explicações e fundamentos, por bloco
  questoes.json     resultado do build (o que a página consome)
build.py            junta itens + gabaritos + explicações → dados/questoes.json
gerar_site.py       injeta os dados no template → index.html e artefato.html
fontes/             legislação e normas usadas para fundamentar as explicações
testes/             testes funcionais headless (jsdom)
capturas/           telas renderizadas para conferência visual
```

## Publicar na Vercel

O site é um único HTML estático: não tem build, backend, banco nem variável de ambiente.
A pasta **`public/`** já sai pronta do `gerar_site.py` e é a única coisa que precisa subir.

Caminho mais curto (uma vez só, sem repositório):

```bash
npm i -g vercel        # se ainda não tiver
cd public
vercel                 # cria o projeto e publica em preview
vercel --prod          # promove para o domínio definitivo
```

Se preferir versionar o projeto inteiro no Git e importar na Vercel, o `vercel.json`
da raiz já aponta `outputDirectory: "public"`, e o `.vercelignore` impede o upload de
`fontes/` (33 MB de PDFs de legislação) e do restante do material de origem. Nesse caso
basta `vercel --prod` na raiz — ou conectar o repositório pelo painel, que a cada push
o site é reconstruído sozinho.

Depois de qualquer alteração, rode `python build.py && python gerar_site.py` antes de
publicar: é o que atualiza `public/index.html`.

Dois detalhes que valem saber:

- O `localStorage` (onde fica seu progresso) é **por origem**. No domínio da Vercel ele
  começa zerado — o histórico do arquivo local não vai junto. Em compensação, funciona
  melhor do que via `file://` e sincroniza entre abas do mesmo domínio.
- A página vai com `noindex` no HTML e no cabeçalho HTTP, então não entra em buscador.
  Ainda assim, uma URL da Vercel no plano gratuito é acessível a quem tiver o link;
  proteção por senha só existe nos planos pagos. Como o conteúdo vem de documentos
  públicos do CEBRASPE, não há problema — mas fica o registro.

## Para alterar alguma coisa

Edite a explicação em `dados/exp_*.json` (ou o layout em `src/corpo.html`) e rode:

```bash
python build.py && python gerar_site.py
```

Para rodar os testes (precisa de `npm install jsdom@24 html-encoding-sniffer@3`):

```bash
node testes/t2.mjs
```

## Limites conhecidos

- A prova discursiva não está aqui — só a objetiva.
- O item 32 teve o enunciado recomposto à mão (`CORRECOES`, em `build.py`): os subíndices
  q₁, q₂ e qₙ ficam em linha própria no PDF e quebravam o agrupamento da extração. Nos itens
  26 e 35, o exemplo destacado foi separado do enunciado (`EXEMPLOS`) para reproduzir o
  caderno original.
- Onde a anulação da banca não veio acompanhada de justificativa pública, a explicação diz
  qual é a regra aplicável e aponta a provável ambiguidade, sem inventar motivação oficial.
