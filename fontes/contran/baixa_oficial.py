# -*- coding: utf-8 -*-
import urllib.request, os, time
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0 Safari/537.36"
B = "https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes"
RES = [("004","1998"),("014","1998"),("036","1998"),("092","1999"),("110","2000"),
       ("160","2004"),("210","2006"),("211","2006"),("216","2006"),("254","2007"),
       ("349","2010"),("360","2010"),("432","2013"),("441","2013"),("471","2013"),
       ("508","2014"),("520","2015"),("525","2015"),("552","2015"),("561","2015"),
       ("667","2017"),("735","2018"),("740","2018"),("780","2019"),("789","2020"),
       ("798","2020"),("803","2020"),("806","2020"),("810","2020")]

def nomes(n, a):
    s = n.lstrip('0')
    for num in (s, n):
        yield f"resolucao{num}{a}.pdf"
        yield f"Resolucao{num}{a}.pdf"
        yield f"resolucao{num}-{a}.pdf"
        yield f"resolucao{num}_{a}.pdf"
        yield f"resolucao_contran_{num}.pdf"

ok, faltam = [], []
for n, a in RES:
    dest = f"res_{n.lstrip('0')}_{a}.pdf"
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        ok.append(dest); continue
    achou = False
    for nome in dict.fromkeys(nomes(n, a)):
        try:
            req = urllib.request.Request(f"{B}/{nome}", headers={'User-Agent': UA})
            data = urllib.request.urlopen(req, timeout=40).read()
            if data[:4] == b'%PDF' and len(data) > 5000:
                open(dest, 'wb').write(data)
                print('OK  ', n, a, '->', nome, len(data), flush=True)
                ok.append(dest); achou = True; break
        except Exception:
            pass
    if not achou:
        print('----', n, a, 'nao encontrado', flush=True)
        faltam.append((n, a))
print('\nbaixados:', len(ok), '| faltam:', faltam)
