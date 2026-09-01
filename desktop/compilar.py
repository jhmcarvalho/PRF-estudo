# -*- coding: utf-8 -*-
"""Gera o executável do Windows e o .zip pronto para enviar.

    python gerar_site.py      (na raiz — atualiza desktop/app/index.html)
    python desktop/compilar.py

Requisitos: pyinstaller e pillow (`pip install pyinstaller pillow`).
"""
import os
import shutil
import subprocess
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
NOME = "Quilometragem PRF"

LEIAME = """Quilometragem PRF — simulado comentado da prova da PRF de 2021
=============================================================

Como usar
---------
Dê dois cliques em "Quilometragem PRF.exe". O programa abre em uma janela
própria. Não instala nada, não precisa de internet e não mexe no seu
navegador: ele usa um perfil separado, só dele.

Na primeira vez o Windows pode mostrar um aviso azul dizendo
"O Windows protegeu o seu computador". Isso acontece com qualquer programa
sem certificado de assinatura digital (que é pago), não é sinal de vírus.
Para seguir: clique em "Mais informações" e depois em "Executar assim mesmo".

Seu progresso fica salvo no seu computador, em
%LOCALAPPDATA%\\QuilometragemPRF. Para zerar tudo, use o botão
"Apagar meu histórico" dentro do programa.

O que tem dentro
----------------
Os 120 itens da prova objetiva do concurso da Polícia Rodoviária Federal
(Edital nº 1, de 18 de janeiro de 2021), com o gabarito oficial definitivo
da banca CEBRASPE e uma explicação para cada item, com link para a norma
que resolve a questão. No final sai um diagnóstico com os temas em que você
mais errou.

Enunciados e gabaritos foram extraídos dos arquivos oficiais publicados pelo
CEBRASPE em cdn.cebraspe.org.br. As explicações foram escritas com base na
legislação citada em cada item.
"""


def executa(*args):
    print("$", " ".join(args))
    subprocess.check_call(args, cwd=AQUI)


def main():
    pagina = os.path.join(AQUI, "app", "index.html")
    if not os.path.exists(pagina):
        sys.exit("Falta desktop/app/index.html — rode antes: python gerar_site.py")

    if not os.path.exists(os.path.join(AQUI, "icone.ico")):
        executa(sys.executable, "gera_icone.py")

    # Com --specpath, o PyInstaller resolve os caminhos relativos a partir do
    # .spec, e não do diretório de trabalho: por isso todos vão absolutos.
    executa(
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--noconsole",
        "--name", NOME,
        "--icon", os.path.join(AQUI, "icone.ico"),
        "--version-file", os.path.join(AQUI, "versao.txt"),
        "--add-data", pagina + ";.",
        "--distpath", os.path.join(AQUI, "dist"),
        "--workpath", os.path.join(AQUI, "build"),
        "--specpath", os.path.join(AQUI, "build"),
        os.path.join(AQUI, "app.py"),
    )

    exe = os.path.join(AQUI, "dist", NOME + ".exe")
    leiame = os.path.join(AQUI, "dist", "LEIA-ME.txt")
    with open(leiame, "w", encoding="utf-8") as f:
        f.write(LEIAME)

    # .zip para enviar: e-mail costuma bloquear .exe solto
    destino = os.path.join(AQUI, "dist", NOME + ".zip")
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(exe, os.path.basename(exe))
        z.write(leiame, os.path.basename(leiame))

    shutil.rmtree(os.path.join(AQUI, "build"), ignore_errors=True)

    for p in (exe, destino):
        print(f"{os.path.basename(p):28} {os.path.getsize(p)/1024/1024:6.1f} MB")


if __name__ == "__main__":
    main()
