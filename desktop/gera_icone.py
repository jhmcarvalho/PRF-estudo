# -*- coding: utf-8 -*-
"""Gera o ícone do executável: placa de rodovia sobre fundo asfalto."""
from PIL import Image, ImageDraw, ImageFont
import os

TAM = 512
ASFALTO, PLACA, FAIXA = (17, 25, 23), (237, 240, 238), (200, 137, 12)

img = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([0, 0, TAM - 1, TAM - 1], radius=int(TAM * .19), fill=ASFALTO)

# poste
d.rectangle([TAM * .47, TAM * .56, TAM * .53, TAM * .84], fill=FAIXA)
# placa
d.rounded_rectangle([TAM * .16, TAM * .17, TAM * .84, TAM * .58],
                    radius=int(TAM * .05), fill=PLACA)

fonte = None
for c in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeuib.ttf"):
    if os.path.exists(c):
        fonte = ImageFont.truetype(c, int(TAM * .26))
        break
texto = "BR"
if fonte:
    cx = (TAM * .16 + TAM * .84) / 2
    cy = (TAM * .17 + TAM * .58) / 2
    d.text((cx, cy), texto, font=fonte, fill=ASFALTO, anchor="mm")

img.save("icone.ico", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
img.resize((256, 256), Image.LANCZOS).save("icone.png")
print("icone.ico gerado:", os.path.getsize("icone.ico"), "bytes")
