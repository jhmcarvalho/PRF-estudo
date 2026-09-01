# -*- coding: utf-8 -*-
"""Injeta os dados no template e gera as saídas:
   index.html        — documento completo, para abrir direto no navegador
   public/index.html — o mesmo arquivo, isolado para publicação estática (Vercel)
   artefato.html     — só o conteúdo, no formato exigido pela publicação como Artifact
"""
import json, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))

# Favicon em SVG embutido: a placa de quilometragem da rodovia.
FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='6' fill='%23111917'/%3E"
    "%3Crect x='7' y='6' width='18' height='11' rx='2' fill='%23EDF0EE'/%3E"
    "%3Ctext x='16' y='15' font-family='monospace' font-size='9' font-weight='700'"
    " text-anchor='middle' fill='%23111917'%3EBR%3C/text%3E"
    "%3Crect x='15' y='19' width='2' height='8' fill='%23C8890C'/%3E%3C/svg%3E"
)

CABECALHO = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Simulado comentado da prova objetiva da PRF 2021 (CEBRASPE): 120 itens com gabarito oficial, explicacao fundamentada na norma e diagnostico por tema.">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="%s">
<style>
  :root{color-scheme:light dark}
  body{margin:0;font:14px system-ui,-apple-system,"Segoe UI",sans-serif;background:#EDF0EE}
  img{max-width:100%%}
  [hidden]{display:none!important}
</style>
""" % FAVICON

RODAPE = "\n</body>\n</html>\n"


def main():
    with open(os.path.join(BASE, 'dados', 'questoes.json'), encoding='utf-8') as f:
        dados = json.load(f)
    # "</" escapado para que nenhuma string feche o <script> antes da hora
    payload = json.dumps(dados, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

    with open(os.path.join(BASE, 'src', 'corpo.html'), encoding='utf-8') as f:
        corpo = f.read()
    corpo = corpo.replace('/*__DADOS__*/', payload)

    # artefato: exatamente o conteúdo (sem doctype/html/head/body)
    caminho_art = os.path.join(BASE, 'artefato.html')
    with open(caminho_art, 'w', encoding='utf-8') as f:
        f.write(corpo)

    # local: o mesmo conteúdo dentro de um documento completo
    corte = corpo.index('<div class="faixa-topo">')
    cabeca, resto = corpo[:corte], corpo[corte:]
    caminho_idx = os.path.join(BASE, 'index.html')
    with open(caminho_idx, 'w', encoding='utf-8') as f:
        f.write(CABECALHO + cabeca + '</head>\n<body>\n' + resto + RODAPE)

    # cópia isolada: é só esta pasta que sobe para a hospedagem estática
    os.makedirs(os.path.join(BASE, 'public'), exist_ok=True)
    caminho_pub = os.path.join(BASE, 'public', 'index.html')
    shutil.copyfile(caminho_idx, caminho_pub)

    for p in (caminho_art, caminho_idx, caminho_pub):
        rotulo = os.path.relpath(p, BASE).replace('\\', '/')
        print(f'{rotulo:20} {os.path.getsize(p)/1024:8.0f} KB')


if __name__ == '__main__':
    main()
