#! /usr/bin/env python3
"""
Modulo que, dado um determinado texto, anónimiza a sua informação.
"""
__version__ = '0.2'

import json
from .utils import trata_geral
from .parse_args import parse_args
from .nomes import get_nomes, get_apelidos
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
    # current path
    global path
    with open(path + "/conf/config.json", "r") as f:
        global conf 
        conf = json.load(f)

def separa_por_linhas(texto: str):
    """
    Função que separa o texto por linhas
    """
    return texto.split(". ")

def init():
    """
    Função que inicializa o programa
    """
    global args
    get_conf()
    args = parse_args()
    global path
    if args["input"] == "stdin":
        print("Exemplo de input a partir do texto em "+ path + "/exemplo.txt")        
        args['input'] = path + "/exemplo.txt"

    get_nomes(conf)
    get_apelidos(conf)

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
    print("A anonimizar...")
    for linha in linhas:
        res,nlp = trata_geral(linha,{"nomes": nomes, "apelidos" : apelidos},nlp=nlp,extra=args['nlp'])
        out += res + ". "

    if args["output"] == "stdout":
        print(out)
    else:
        with open(args["output"], "w") as f:
            f.write(out)

    with open("out.txt", "w") as f:
            f.write(out)