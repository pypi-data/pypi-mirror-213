#! /usr/bin/env python3
"""
Modulo que, dado um determinado texto, anónimiza a sua informação.
"""
__version__ = '0.3'

import json
from .utils import trata_geral
from .args_ import parse_args
from .nomes_ import get_nomes, get_apelidos
import os

conf = {}
args = {}
apelidos = {}
nomes = {}

path = os.path.dirname(os.path.abspath(__file__))

def get_conf():
    """
    Função que atualiza o dicionario de configuração 
    """
    global path
    with open(path + "/conf/config.json", "r") as f:
        global conf 
        conf = json.load(f)

def separa_por_linhas(texto: str):
    """
    Função que separa o texto por linhas
    """

    out = [frase.strip()[:-1] if frase.strip()[-1] == "."  else frase.strip() for frase in texto.split(". ")]
    return out

def init():
    """
    Função que inicializa o programa
    """
    global args
    global nomes
    global apelidos

    get_conf()
    args = parse_args()
    global path
    if args["input"] == "stdin":
        print("Exemplo de input a partir do texto em "+ path + "/exemplo.txt")        
        args['input'] = path + "/exemplo.txt"

    nomes = get_nomes(conf,nomes)
    apelidos = get_apelidos(conf,apelidos)

def main():
    init()
    
    global args
    global apelidos
    global nomes

    texto = ""
    with open(args["input"], "r") as f:
        texto = f.read()
    
    linhas = separa_por_linhas(texto)
    out = ""
    nlp = None
    print("A anonimizar...",end="\n\n")
    for linha in linhas:
        res,nlp = trata_geral(linha,{"nomes": nomes, "apelidos" : apelidos},nlp=nlp,extra=args['nlp'])
        out += res + ". "

    if args["output"] == "stdout":
        print(out)
    else:
        with open(args["output"], "w") as f:
            f.write(out)