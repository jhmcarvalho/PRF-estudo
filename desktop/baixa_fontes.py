# -*- coding: utf-8 -*-
"""Baixa os WOFF2 do Google Fonts e monta um CSS com as fontes embutidas em base64,
para que o executável tenha a mesma tipografia do site mesmo sem internet."""
import urllib.request, re, base64, os

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
CSS = ("https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700"
       "&family=IBM+Plex+Mono:wght@400;500"
       "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400"
       "&display=swap")

def baixa(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()

css = baixa(CSS).decode('utf-8')
blocos = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})', css, re.S)
print('blocos @font-face:', len(blocos))

saida, total = [], 0
mantidos = 0
for subset, bloco in blocos:
    if subset != 'latin':
        continue
    m = re.search(r"url\((https://[^)]+\.woff2)\)", bloco)
    if not m:
        continue
    dados = baixa(m.group(1))
    total += len(dados)
    b64 = base64.b64encode(dados).decode()
    bloco = bloco.replace(m.group(1), f"data:font/woff2;base64,{b64}")
    saida.append(bloco)
    mantidos += 1

print(f'faces embutidas: {mantidos} | {total/1024:.0f} KB de fonte')
with open('fontes_embutidas.css', 'w', encoding='utf-8') as f:
    f.write('/* Fontes do Google Fonts embutidas para uso offline. */\n')
    f.write('\n'.join(saida))
print('gravado fontes_embutidas.css:', os.path.getsize('fontes_embutidas.css')/1024, 'KB')
