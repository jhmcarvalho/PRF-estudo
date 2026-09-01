# -*- coding: utf-8 -*-
"""Recorta do PDF a região de cada item indicado e salva como imagem, para
conferência visual — um canal de verificação que não depende de extração de texto."""
import pdfplumber, pypdfium2 as pdfium, sys

ALVOS = [int(x) for x in sys.argv[1:]] or [33, 50, 80, 92, 103, 115]
PDF = '578_PRF_001_01.PDF'
ESCALA = 3

# localiza o número do item na página (coordenada só serve para escolher o recorte)
pos = {}
with pdfplumber.open(PDF) as pdf:
    for i, page in enumerate(pdf.pages):
        for w in page.extract_words():
            if w['text'].isdigit() and int(w['text']) in ALVOS:
                n = int(w['text'])
                margem = w['x0'] < 40 or 295 < w['x0'] < 310
                if margem and n not in pos:
                    pos[n] = (i, w['x0'], w['top'], page.width, page.height)

doc = pdfium.PdfDocument(PDF)
for n in ALVOS:
    if n not in pos:
        print('não localizei o item', n); continue
    i, x0, top, W, H = pos[n]
    img = doc[i].render(scale=ESCALA).to_pil()
    sx, sy = img.size[0] / W, img.size[1] / H
    esq = 20 if x0 < 40 else 295
    dir_ = 300 if x0 < 40 else 580
    caixa = (int(esq * sx), int((top - 6) * sy), int(dir_ * sx), int((top + 78) * sy))
    img.crop(caixa).save(f'item_{n}.png')
    print(f'item {n}: página {i+1}, recorte salvo')
