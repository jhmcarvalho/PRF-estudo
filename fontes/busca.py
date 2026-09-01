# -*- coding: utf-8 -*-
"""busca.py <arquivo.txt> <regex> [chars_contexto]"""
import sys, re, io
sys.stdout.reconfigure(encoding='utf-8')
path, pat = sys.argv[1], sys.argv[2]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 320
t = open(path, encoding='utf-8', errors='replace').read()
t = re.sub(r'\s+', ' ', t)
n = 0
for m in re.finditer(pat, t, re.I):
    a = max(0, m.start()); b = min(len(t), m.start() + ctx)
    print('»', t[a:b].strip(), '\n')
    n += 1
    if n >= 6: break
if not n: print('(sem match)')
