# -*- coding: utf-8 -*-
"""Monta dados/questoes.json a partir dos cadernos oficiais + gabaritos + explicações."""
import json, re, os, base64, glob

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, 'dados')


def carregar(nome):
    with open(os.path.join(D, nome), encoding='utf-8') as f:
        return json.load(f)


# Fragmentos do cabeçalho de instruções que a extração em duas colunas mistura
# ao texto de apoio dos cadernos de língua estrangeira.
RUIDO = [
    'Cada um dos itens da prova objetiva', 'cada um deles esteja vinculado',
    'o item CERTO; ou o campo designado', 'ambos os campos não serão apenadas',
    'Respostas, único documento válido', 'Nos itens que avaliarem conhecimentos',
    'informado o contrário, considere que', 'proteção, de funcionamento e de uso',
    'Eventuais espaços livres', 'ser utilizados para rascunho',
    'que imediatamente o antecede', 'para cada item: o campo designado',
    'o item ERRADO. A ausência de marcação', 'pontuação negativa. Para as devidas',
    'tecnologia da informação, a menos que', 'estão em configuração-padrão',
    'arquivos, diretórios, recursos e equipamentos', 'Espaço livre',
    '-- PROVA OBJETIVA --', 'PROVA OBJETIVA',
]

COMANDO_RE = re.compile(r'(julgue|juzgue|judge)\b', re.I)


def limpar(ctx):
    linhas = []
    for ln in ctx.split('\n'):
        s = ln.strip()
        if not s or s == '--' or s == 'objetiva.':
            continue
        if any(r in s for r in RUIDO):
            continue
        linhas.append(s)
    return linhas


def separar(ctx):
    """Devolve (texto_de_apoio, comando)."""
    linhas = limpar(ctx)
    if not linhas:
        return '', ''
    # o comando é o último bloco que contém "julgue/juzgue/judge"
    corte = None
    for i in range(len(linhas) - 1, -1, -1):
        if COMANDO_RE.search(linhas[i]):
            corte = i
            break
    if corte is None:
        return ' '.join(linhas), ''
    # sobe enquanto as linhas anteriores fizerem parte do mesmo período
    ini = corte
    while ini > 0 and not linhas[ini - 1].rstrip().endswith(('.', ':', '!', '?')):
        ini -= 1
    # desce até fechar o período do comando ("... julgue os itens" + "a seguir.")
    fim = corte
    while fim < len(linhas) - 1 and not linhas[fim].rstrip().endswith(('.', ':', '!', '?')):
        fim += 1
    apoio = ' '.join(linhas[:ini]).strip()
    comando = ' '.join(linhas[ini:fim + 1]).strip()
    return apoio, comando


# O item 32 usa subíndices (q₁, q₂, qₙ) que o PDF grafa em linha própria, o que
# quebra o agrupamento por linha na extração e faz o resto do enunciado vazar
# para o item seguinte. Os dois são recompostos aqui a partir do caderno oficial.
CORRECOES = {
    32: {'texto':
         'Considere que {qₙ}, para n variando de 1 a 10, seja a sequência numérica '
         'formada pelas quantidades de veículos fiscalizados apenas no decorrer da '
         'n-ésima hora de realização da operação, ou seja, q₁ é a quantidade de '
         'veículos fiscalizados apenas no decorrer da primeira hora de realização da '
         'operação; q₂ é a quantidade de veículos fiscalizados apenas no decorrer da '
         'segunda hora de realização da operação; e assim por diante. Nessa situação, '
         'a sequência {qₙ}, para n variando de 1 a 10, é uma progressão aritmética.'},
    33: {'contexto':
         'No que se refere a Internet, intranet e noções do sistema operacional '
         'Windows, julgue os itens que se seguem.'},
}

# Itens que, no caderno, trazem um exemplo destacado abaixo do enunciado.
EXEMPLOS = {
    26: 'Assunto: Realização de concurso público.',
    35: 'campanha PRF @twitter',
}


def imagem_b64():
    p = os.path.join(BASE, 'figura_43_44.png')
    if not os.path.exists(p):
        return None
    with open(p, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()


def main():
    gab = carregar('gabaritos.json')
    exp = {}
    for f in glob.glob(os.path.join(D, 'exp_*.json')):
        exp.update(json.load(open(f, encoding='utf-8')))

    fig = imagem_b64()
    questoes = []

    def adicionar(itens, chave_gab, prefixo, lingua):
        apoio_atual, comando_atual = '', ''
        nomeados = {}   # textos identificados por código (ex.: "1A18-I")
        for it in itens:
            n = it['n']
            if not prefixo and n in CORRECOES:
                it = dict(it, **CORRECOES[n])
            apoio, comando = separar(it.get('contexto', ''))
            if apoio:
                apoio_atual = apoio
                m = re.search(r'Texto\s+([0-9A-Z]+-[IVX]+)', apoio)
                if m:
                    nomeados[m.group(1)] = apoio
            elif comando:
                # novo comando sem texto novo: o apoio só permanece se for
                # referenciado pelo código (ex.: "texto 1A18-I") ou se o caderno
                # inteiro girar em torno de um único texto (línguas estrangeiras)
                m = re.search(r'texto\s+([0-9A-Z]+-[IVX]+)', comando, re.I)
                if m and m.group(1) in nomeados:
                    apoio_atual = nomeados[m.group(1)]
                elif not lingua:
                    apoio_atual = ''
            if comando:
                comando_atual = comando
            cid = f'{prefixo}{n}' if prefixo else str(n)
            e = exp.get(cid, {})
            q = {
                'id': cid,
                'n': n,
                'lingua': lingua,
                'bloco': it.get('bloco') or ('BLOCO I' if not prefixo and n <= 55 else it.get('bloco')),
                'disciplina': e.get('disciplina', '(a classificar)'),
                'tema': e.get('tema', '(a classificar)'),
                'textoApoio': apoio_atual,
                'comando': comando_atual,
                'enunciado': it['texto'],
                'gabarito': gab[chave_gab][str(n)],
                'explicacao': e.get('explicacao', ''),
                'fundamentos': e.get('fundamentos', []),
            }
            if not prefixo and n in EXEMPLOS:
                exemplo = EXEMPLOS[n]
                if q['enunciado'].endswith(exemplo):
                    q['enunciado'] = q['enunciado'][:-len(exemplo)].strip()
                q['exemplo'] = exemplo
            if e.get('alerta'):
                q['alerta'] = e['alerta']
            if n in (43, 44) and not prefixo and fig:
                q['figura'] = fig
            questoes.append(q)

    adicionar(carregar('itens_ing.json'), 'ing', 'ING', 'ing')
    adicionar(carregar('itens_esp.json'), 'esp', 'ESP', 'esp')
    adicionar(carregar('itens_9_120.json'), 'principal', '', None)

    meta = {
        'concurso': 'Polícia Rodoviária Federal — Edital nº 1, de 18 de janeiro de 2021',
        'cargo': 'Policial Rodoviário Federal',
        'banca': 'CEBRASPE',
        'caderno': '578_PRF_001_01 (+ cadernos de língua inglesa e espanhola)',
        'fontes': [
            {'rotulo': 'Caderno de prova objetiva (itens 9 a 120)',
             'url': 'https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/578_PRF_001_01.PDF'},
            {'rotulo': 'Caderno de língua inglesa (itens 1 a 8)',
             'url': 'https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/578_PRF_ING_01.PDF'},
            {'rotulo': 'Caderno de língua espanhola (itens 1 a 8)',
             'url': 'https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/578_PRF_ESP_02.PDF'},
            {'rotulo': 'Gabarito oficial definitivo (itens 9 a 120)',
             'url': 'https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/GAB_DEFINITIVO_578_PRF_001_01.PDF'},
            {'rotulo': 'Gabarito oficial definitivo (inglês)',
             'url': 'https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/GAB_DEFINITIVO_578_PRF_ING_01.PDF'},
            {'rotulo': 'Gabarito oficial definitivo (espanhol)',
             'url': 'https://cdn.cebraspe.org.br/concursos/prf_21/arquivos/GAB_DEFINITIVO_578_PRF_ESP_02.PDF'},
            {'rotulo': 'Edital de abertura',
             'url': 'https://cdn.cebraspe.org.br/concursos/PRF_21/arquivos/ED_1_PRF_2021_ABERTURA.PDF'},
        ],
    }

    saida = {'meta': meta, 'questoes': questoes}
    with open(os.path.join(D, 'questoes.json'), 'w', encoding='utf-8') as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)

    sem_exp = [q['id'] for q in questoes if not q['explicacao']]
    print(f'questões: {len(questoes)}')
    print(f'com explicação: {len(questoes) - len(sem_exp)}')
    print(f'sem explicação ({len(sem_exp)}): {sem_exp}')


if __name__ == '__main__':
    main()
