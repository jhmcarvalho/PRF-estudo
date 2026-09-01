# -*- coding: utf-8 -*-
"""Quilometragem PRF — lançador do aplicativo de desktop.

Serve o simulado (um único HTML embutido no executável) em 127.0.0.1 e abre o
Edge em modo aplicativo: janela sem barra de endereço, com perfil próprio, de
modo que o progresso de estudo fique guardado entre uma sessão e outra e o
navegador pessoal de quem usa não seja tocado.
"""
import http.server
import os
import socket
import subprocess
import sys
import threading
import urllib.request
import webbrowser

NOME = "Quilometragem PRF"
# Porta fixa: o localStorage (onde fica o progresso) é vinculado à origem,
# então mudar de porta a cada execução apagaria o histórico do usuário.
PORTA = 47121
ASSINATURA = "<title>Quilometragem PRF 2021</title>"


def recurso(nome):
    """Caminho do arquivo embutido, tanto no executável quanto rodando pelo fonte."""
    base = getattr(sys, "_MEIPASS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))
    return os.path.join(base, nome)


def pasta_perfil():
    raiz = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    caminho = os.path.join(raiz, "QuilometragemPRF", "perfil")
    os.makedirs(caminho, exist_ok=True)
    return caminho


with open(recurso("index.html"), "rb") as arquivo:
    PAGINA = arquivo.read()


class Servidor(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGINA)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(PAGINA)

    def log_message(self, *args):
        pass  # sem console


def ja_esta_no_ar(porta):
    """Verifica se a porta já está ocupada por outra instância deste mesmo app."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{porta}/", timeout=2) as r:
            return ASSINATURA.encode() in r.read(4096)
    except Exception:
        return False


def sobe_servidor():
    """Devolve (porta, servidor). O servidor é None quando outra instância já responde."""
    try:
        httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), Servidor)
        return PORTA, httpd
    except OSError:
        if ja_esta_no_ar(PORTA):
            return PORTA, None
        # porta tomada por outro programa: cai para uma livre (o histórico
        # anterior não aparece, porque a origem muda)
        httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Servidor)
        return httpd.server_address[1], httpd


def caminho_navegador():
    candidatos = []
    for var in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
        raiz = os.environ.get(var)
        if not raiz:
            continue
        candidatos += [
            os.path.join(raiz, "Microsoft", "Edge", "Application", "msedge.exe"),
            os.path.join(raiz, "Google", "Chrome", "Application", "chrome.exe"),
        ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    return None


def main():
    porta, httpd = sobe_servidor()
    if httpd is not None:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()

    endereco = f"http://127.0.0.1:{porta}/"
    navegador = caminho_navegador()

    if navegador:
        # --app abre uma janela sem barra de endereço; o perfil próprio garante
        # que o processo lançado seja o dono da janela, e não um Edge já aberto.
        comando = [
            navegador,
            f"--app={endereco}",
            f"--user-data-dir={pasta_perfil()}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-features=Translate,EdgeCollections",
            "--window-size=1180,900",
        ]
        try:
            processo = subprocess.Popen(comando)
            processo.wait()          # segura o app enquanto a janela estiver aberta
            return
        except OSError:
            pass

    # Sem Edge nem Chrome: abre no navegador padrão e espera o usuário fechar.
    webbrowser.open(endereco)
    print(f"{NOME} está rodando em {endereco}")
    print("Feche esta janela para encerrar.")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
