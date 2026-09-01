# Verificação da fidelidade à prova oficial

Objetivo: garantir que **enunciados e gabaritos** da aplicação são exatamente os da
prova aplicada, sem depender de transcrições de terceiros.

Data da verificação: 01/09/2026. Resultado: **128 de 128 itens conferidos, nenhuma
divergência**.

## Por que não conferimos por comparação com outros sites

Sites de questões são transcrições feitas por pessoas ou por OCR — erram, cortam
formatação e às vezes reproduzem o gabarito *preliminar*, não o definitivo. Comparar
com eles trocaria uma fonte primária por uma secundária. Foram usados só como
corroboração final, depois da conferência contra os documentos oficiais.

## Camada 1 — os PDFs são os oficiais e não mudaram

Os seis arquivos foram rebaixados de `cdn.cebraspe.org.br/concursos/prf_21/arquivos/`
e comparados por SHA-256 com as cópias usadas no build: **idênticos byte a byte**.
As somas estão em `pdfs_oficiais.sha256` e podem ser reconferidas a qualquer momento:

```bash
sha256sum -c pdfs_oficiais.sha256
```

## Camada 2 — extração independente e diff caractere a caractere

`extrai_independente.py` refaz a extração dos 128 enunciados por um caminho que não
compartilha nada com o pipeline do projeto:

| | pipeline do projeto | verificador independente |
|---|---|---|
| motor de PDF | pdfplumber | Xpdf `pdftotext -layout` |
| divisão de colunas | coordenada x das palavras | posição de caractere no texto |
| montagem dos itens | indentação em pontos | indentação em espaços |

```bash
python extrai_independente.py ../../dados/questoes.json
```

Resultado: **104 itens idênticos**, 8 divergentes e 16 não localizados. Nenhum dos 24
restantes era erro da aplicação:

- **8 divergentes** — em todos, o defeito estava no verificador: o corte por coluna de
  caractere come letras na borda ("contrataçã" em vez de "contratação" no item 50,
  "salv vidas" no 80, "síti" no 33, vírgula perdida no 103), ou interrompe o item cedo
  demais (92 e 115). Os itens 32 e 35 divergiam por decisões deliberadas do build
  (subíndices e exemplo em campo próprio).
- **16 não localizados** — os cadernos de língua estrangeira têm layout misto, que o
  verificador simplificado não separa.

## Camada 3 — leitura visual do PDF renderizado

Os 24 itens acima foram conferidos olhando o PDF renderizado em alta resolução
(`recorta.py`), um canal que não passa por nenhuma extração de texto. Todos batem com
a aplicação, inclusive os subíndices q₁/q₂/qₙ do item 32 e a linha de exemplo
`campanha PRF @twitter` do item 35.

```bash
python recorta.py 33 50 80 92 103 115
```

## Camada 4 — gabaritos lidos à mão na tabela oficial

`confere_gabarito.py` guarda a transcrição feita **visualmente** da tabela do
`GAB_DEFINITIVO_578_PRF_001_01.PDF` e compara com `dados/gabaritos.json`:

```
itens lidos na imagem : 112
DIVERGÊNCIAS          : 0
anulados              : 39, 45, 67, 69, 76, 83, 89, 98, 99  (idênticos nos dois)
```

Os gabaritos de inglês (`X C E C E C C E`) e espanhol (`X E C C E E C C`) também foram
lidos na imagem e conferem.

## Camada 5 — corroboração externa

A lista de anulados coincide com a divulgada à época pela imprensa especializada:
"nove (das 120) questões foram anuladas — 39, 45, 67, 69, 76, 83, 89, 98 e 99"
([Estratégia Concursos](https://www.estrategiaconcursos.com.br/blog/concurso-prf-sairam-gabaritos-confira-anulados/)).
Somando o item 1 anulado em cada caderno de língua, chega-se aos 10 itens anulados
noticiados no total.

## O que esta verificação NÃO cobre

Enunciados e gabaritos estão certificados. As **explicações** são de outra natureza:
não são transcrição de nada — a banca não publica comentário item a item. Foram
escritas com base na norma citada em cada item, conferida no texto oficial, mas
envolvem interpretação e podem conter erro de análise. Ao estudar, o link do
"Fundamento" leva à fonte para você conferir por conta própria.
