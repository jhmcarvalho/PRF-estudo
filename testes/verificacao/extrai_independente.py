# -*- coding: utf-8 -*-
"""Extração INDEPENDENTE dos enunciados, para conferir a base da aplicação.

Tudo aqui é feito por um caminho diferente do pipeline do projeto:
  - motor de PDF: Xpdf `pdftotext -layout`  (o projeto usa pdfplumber);
  - divisão de colunas: por posição de caractere no texto, achando a coluna
    branca em quase todas as linhas  (o projeto usa a coordenada x das palavras);
  - montagem dos itens: por indentação medida em espaços  (o projeto usa pontos).

Se os dois caminhos produzirem exatamente o mesmo texto, erro de extração fica
descartado: seriam necessários dois bugs independentes com o mesmo resultado.

Uso: python extrai_independente.py <caminho para questoes.json>
"""
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

RUIDO = re.compile(r'^\s*(CEBRASPE|Espaço livre|BLOCO [IVX]+|-- PROVA OBJETIVA --)')


def texto_layout(pdf):
    subprocess.check_call(['pdftotext', '-layout', '-enc', 'UTF-8', pdf, pdf + '.ind.txt'])
    return open(pdf + '.ind.txt', encoding='utf-8').read()


def indentacoes(linhas):
    """Indentações recorrentes de uma coluna, da esquerda para a direita."""
    uteis = [l for l in linhas if l.strip()]
    if not uteis:
        return [0, 5]
    contagem = Counter(len(l) - len(l.lstrip()) for l in uteis)
    limite = max(3, len(uteis) * .05)
    rec = sorted(i for i, n in contagem.items() if n >= limite)
    return rec or sorted(contagem)


def dedenta(linhas):
    """Remove a margem da coluna: a indentação passa a ser relativa a ela."""
    rec = indentacoes(linhas)
    margem = rec[0]
    return [(l[margem:] if len(l) - len(l.lstrip()) >= margem else l.lstrip())
            if l.strip() else l for l in linhas]


def corta_colunas(pagina):
    linhas = [l.rstrip() for l in pagina.split('\n')]
    uteis = [l for l in linhas if l.strip()]
    if not uteis:
        return []
    largura = max(len(l) for l in uteis)
    melhor, nota = None, -1
    for c in range(int(largura * .30), int(largura * .70)):
        brancas = sum(1 for l in uteis if l[c:c + 3].strip() == '')
        if brancas > nota:
            nota, melhor = brancas, c
    if nota < len(uteis) * .85:
        return [dedenta(linhas)]                       # página de coluna única
    return [dedenta([l[:melhor] for l in linhas]),
            dedenta([l[melhor:] for l in linhas])]


def itens(pdf, primeiro, ultimo):
    """{numero: enunciado} montado só a partir do texto do PDF."""
    linhas = []                                        # (linha, indentação do corpo)
    for pagina in texto_layout(pdf).split('\f'):
        for coluna in corta_colunas(pagina):
            rec = indentacoes(coluna)
            corpo = rec[1] if len(rec) > 1 else 5
            for l in coluna:
                if l.strip() and not RUIDO.match(l):
                    linhas.append((l, corpo))

    achados, atual, esperado = {}, None, primeiro
    for l, corpo in linhas:
        s = l.strip()
        recuo = len(l) - len(l.lstrip())
        m = re.match(r'^%d\s+(.+)$' % esperado, s)
        if m and recuo <= 2 and esperado <= ultimo:
            # item novo: número na margem da coluna, na sequência esperada
            achados[esperado] = m.group(1)
            atual, esperado = esperado, esperado + 1
        elif atual is not None and abs(recuo - corpo) <= 1:
            # continuação: exatamente na indentação do corpo. Parágrafo de texto
            # de apoio começa mais adentro e por isso não é confundido com ela.
            achados[atual] += ' ' + s
        else:
            atual = None
    return achados


def normaliza(t):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', t)).strip()


def main():
    base = json.load(open(sys.argv[1], encoding='utf-8'))
    app = {q['id']: q for q in base['questoes']}

    conjuntos = [('578_PRF_001_01.PDF', 9, 120, ''),
                 ('578_PRF_ING_01.PDF', 1, 8, 'ING'),
                 ('578_PRF_ESP_02.PDF', 1, 8, 'ESP')]

    iguais, diferentes, ausentes = [], [], []
    for pdf, a, b, prefixo in conjuntos:
        extraidos = itens(pdf, a, b)
        for n in range(a, b + 1):
            cid = f'{prefixo}{n}' if prefixo else str(n)
            if n not in extraidos:
                ausentes.append(cid)
                continue
            na_app = app[cid]['enunciado']
            if app[cid].get('exemplo'):      # o exemplo destacado é campo à parte
                na_app += ' ' + app[cid]['exemplo']
            if normaliza(extraidos[n]) == normaliza(na_app):
                iguais.append(cid)
            else:
                diferentes.append((cid, normaliza(extraidos[n]), normaliza(na_app)))

    total = len(iguais) + len(diferentes) + len(ausentes)
    print(f'itens conferidos : {total}')
    print(f'IDÊNTICOS        : {len(iguais)}')
    print(f'divergentes      : {len(diferentes)}')
    print(f'não localizados  : {len(ausentes)} {ausentes}')
    for cid, ind, na_app in diferentes:
        print(f'\n=== item {cid} ===')
        print('extração independente:', ind[:260])
        print('na aplicação         :', na_app[:260])


if __name__ == '__main__':
    main()
