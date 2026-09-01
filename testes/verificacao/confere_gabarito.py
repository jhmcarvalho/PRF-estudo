# -*- coding: utf-8 -*-
"""Compara o gabarito da aplicação com a LEITURA VISUAL da tabela oficial
(transcrita à mão a partir da imagem renderizada do PDF do CEBRASPE)."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Transcrição feita olhando gab_tabela.png, linha a linha da tabela oficial.
LIDO_VISUALMENTE = {}
linhas = [
    (9,   "C E C C C E E C C E C E E E E C E C C E"),
    (29,  "E E C C E E C C E E X C E E C E X E C C"),
    (49,  "E C C E C C E C C E E C E E C C C E X E"),
    (69,  "X E C C E E E X C E E C E E X C E E E E"),
    (89,  "X C E C E C C E C X X E E C E C E C E E"),
    (109, "C E C C C C E C E C C E"),
]
for inicio, seq in linhas:
    for i, v in enumerate(seq.split()):
        LIDO_VISUALMENTE[inicio + i] = v

gab = json.load(open('f:/Dev/estudo/prf-simulado/dados/gabaritos.json', encoding='utf-8'))
app = {int(k): v for k, v in gab['principal'].items()}

print('itens lidos na imagem :', len(LIDO_VISUALMENTE))
print('itens na aplicação    :', len(app))
falta = sorted(set(range(9, 121)) - set(LIDO_VISUALMENTE))
print('cobertura 9–120       :', 'completa' if not falta else f'faltam {falta}')

divergencias = [(n, LIDO_VISUALMENTE[n], app.get(n))
                for n in sorted(LIDO_VISUALMENTE) if app.get(n) != LIDO_VISUALMENTE[n]]
print('DIVERGÊNCIAS          :', len(divergencias))
for n, lido, na_app in divergencias:
    print(f'  item {n}: imagem={lido}  aplicação={na_app}')

anulados_img = sorted(n for n, v in LIDO_VISUALMENTE.items() if v == 'X')
anulados_app = sorted(n for n, v in app.items() if v == 'X')
print('anulados na imagem    :', anulados_img)
print('anulados na aplicação :', anulados_app)
print('conferem              :', anulados_img == anulados_app)
