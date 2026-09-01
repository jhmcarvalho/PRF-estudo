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
gerar_site.py       injeta os dados no template → index.html, public/ e desktop/app/
docs/index.html     pasta publicada pelo GitHub Pages
desktop/            lançador, ícone e script que geram o .exe do Windows
fontes/             legislação e normas usadas para fundamentar as explicações
testes/             testes funcionais headless (jsdom)
capturas/           telas renderizadas para conferência visual
```

## Publicar o site (GitHub Pages)

O site é um único HTML estático — sem build, backend, banco ou variável de ambiente.
A pasta **`docs/`** já sai pronta do `gerar_site.py` e é a única coisa publicada.
O GitHub Pages só serve a raiz do repositório ou a pasta `/docs`; por isso a saída
vai para `docs/`, que já vem com um `.nojekyll` para o Jekyll não reprocessar nada.

Primeira publicação:

```bash
git add docs .gitignore vercel.json .vercelignore
git commit -m "Publica o simulado no GitHub Pages"
git push
```

Depois, no GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a
branch**, e escolha **Branch: `main`** e pasta **`/docs`**. Salve e espere cerca de um
minuto. O endereço fica:

```
https://jhmcarvalho.github.io/PRF-estudo/
```

A partir daí, para atualizar basta:

```bash
python build.py && python gerar_site.py
git add docs && git commit -m "Atualiza o simulado" && git push
```

O Pages republica sozinho a cada push — não precisa de GitHub Actions, porque o
`docs/index.html` já vai pronto no commit.

Três detalhes que valem saber:

- A página funciona em subpasta (`/PRF-estudo/`) porque não tem nenhuma referência
  relativa: dados, fontes do executável, figura e ícone estão todos embutidos ou em URL
  absoluta.
- No plano gratuito, um site do Pages é **público** — Pages a partir de repositório
  privado exige plano pago. A página vai com `noindex`, então não entra em buscador,
  mas quem tiver o link acessa. Como o conteúdo vem de documentos públicos do CEBRASPE,
  não há problema. Para um domínio próprio, basta um arquivo `CNAME` dentro de `docs/`.
- O `localStorage` (onde fica o progresso) é **por origem**: o histórico do arquivo local
  não vai junto para o endereço do Pages, e vice-versa.

Se algum dia quiser voltar para a Vercel, a mesma pasta serve: o `vercel.json` aponta
`outputDirectory: "docs"` e o `.vercelignore` evita subir `fontes/` e o material de origem.

## Gerar o executável do Windows

Para enviar a alguém sem depender de link, `desktop/` produz um **.exe único de 8,8 MB**
que não instala nada e funciona sem internet.

```bash
python build.py && python gerar_site.py   # atualiza desktop/app/index.html
python desktop/compilar.py                # gera desktop/dist/
```

Sai `Quilometragem PRF.exe` e um `.zip` com o exe mais um `LEIA-ME.txt` (e-mail costuma
bloquear `.exe` solto no anexo). Requer `pip install pyinstaller pillow`.

**Como o app funciona.** O executável sobe um servidor local em `127.0.0.1:47121` e abre o
Edge (ou o Chrome) em *modo aplicativo*: janela sem barra de endereço, ícone próprio na barra
de tarefas e um perfil separado em `%LOCALAPPDATA%\QuilometragemPRF` — o navegador pessoal de
quem usa não é tocado. Fechar a janela encerra tudo. A porta é fixa de propósito: o progresso
fica no `localStorage`, que é vinculado à origem, e uma porta aleatória apagaria o histórico a
cada abertura. As três famílias tipográficas vão embutidas em base64 (`desktop/fontes_embutidas.css`,
gerado por `baixa_fontes.py`), então a página fica idêntica offline.

**O que esperar ao enviar para alguém:**

- Na primeira execução o Windows mostra *"O Windows protegeu o seu computador — editor
  desconhecido"*. É o SmartScreen reagindo à falta de assinatura digital; some só com um
  certificado de code signing, que é pago e anual. A pessoa precisa clicar em
  "Mais informações" → "Executar assim mesmo". O `LEIA-ME.txt` já explica isso.
- Executáveis gerados com PyInstaller às vezes disparam falso positivo em antivírus.
- Gmail e vários webmails **bloqueiam anexos `.exe`**, inclusive dentro de `.zip` comum.
  Na prática você acaba usando WhatsApp, Drive ou pendrive.
- Só Windows. Em Mac ou Linux, o caminho é o `index.html` ou o site.

Se o objetivo for parecer um trabalho sério, vale considerar que um domínio próprio apontando
para a Vercel (um `.com.br` custa cerca de R$ 40/ano) transmite isso melhor do que um
executável sem assinatura que abre um alerta de segurança logo de cara. Uma terceira via, sem
nenhum atrito: mandar o próprio `index.html` (392 KB) — abre com dois cliques, sem instalação
e sem aviso.

## Para alterar alguma coisa

Edite a explicação em `dados/exp_*.json` (ou o layout em `src/corpo.html`) e rode:

```bash
python build.py && python gerar_site.py
```

Para rodar os testes (precisa de `npm install jsdom@24 html-encoding-sniffer@3`):

```bash
node testes/t2.mjs
```

## Fidelidade à prova oficial

Enunciados e gabaritos foram conferidos em cinco camadas independentes — o relatório
completo está em [`testes/verificacao/VERIFICACAO.md`](testes/verificacao/VERIFICACAO.md).
Resumo: **128 de 128 itens conferidos, nenhuma divergência**.

1. Os seis PDFs oficiais foram rebaixados do CEBRASPE e batem por SHA-256 com as cópias
   usadas no build (`sha256sum -c testes/verificacao/pdfs_oficiais.sha256`).
2. Os 128 enunciados foram reextraídos por um caminho independente (outro motor de PDF,
   outra lógica de colunas) e comparados caractere a caractere: 104 idênticos.
3. Os 24 restantes foram conferidos por leitura visual do PDF renderizado — todos batem.
4. Os gabaritos foram transcritos à mão da imagem da tabela oficial e comparados com
   `dados/gabaritos.json`: zero divergências, mesmos nove anulados.
5. A lista de anulados coincide com a noticiada à época.

As **explicações** não entram nessa certificação: não são transcrição — a banca não
publica comentário item a item. São escritas com base na norma citada, mas envolvem
interpretação. O link do "Fundamento" existe para você conferir na fonte.

## Limites conhecidos

- A prova discursiva não está aqui — só a objetiva.
- O item 32 teve o enunciado recomposto à mão (`CORRECOES`, em `build.py`): os subíndices
  q₁, q₂ e qₙ ficam em linha própria no PDF e quebravam o agrupamento da extração. Nos itens
  26 e 35, o exemplo destacado foi separado do enunciado (`EXEMPLOS`) para reproduzir o
  caderno original.
- Onde a anulação da banca não veio acompanhada de justificativa pública, a explicação diz
  qual é a regra aplicável e aponta a provável ambiguidade, sem inventar motivação oficial.
