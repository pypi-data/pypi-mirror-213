#! /usr/bin/env python3
"""
Modulo que anonimiza textos portugueses com nomes portugueses
"""
__version__ = '0.1'

import requests
import bs4
import json
from utils import limpa, runcmd, trata_geral
from parse_args import parse_args
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

def guarda_apelidos():
    """
    Função que guarda a lista de apelidos portugueses retirados da web
    Url usado definido no ficheiro de configuração
    """
    response = requests.get(conf["url_apelidos"])
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    soup = soup.find_all("table", {"class": "wikitable"})
    with open(path + "/" + conf["apelidos"], "w") as f:
        # entrar nas tabelas
        for table in soup:
            lines = table.find_all("tr")
            
            # entrar nas linhas
            for line in lines[1:]:
                columns = line.find_all("td")
                if len(columns) == 6:
                    f.write(limpa(columns[1].text)+ "\n")
                    if len(columns[3].text.strip()) > 0:
                        for apelido in columns[3].text.split(","):
                            f.write(limpa(apelido) + "\n")

def guarda_nomes():
    """
    Função que guarda a lista de nomes portugueses retirados da web
    Url usado definido no ficheiro de configuração
    """

    runcmd("wget -O dados/nomes.pdf " + conf["url_nomes"])
    runcmd("pdftotext dados/nomes.pdf dados/nomes.txt")

    nomes_limpos = ""
    with open(path + "/" + conf["nomes"],"r") as f:
        for line in f:
            line = limpa(line)
            if len(line) > 0:
                nomes_limpos += line + "\n" 

    with open(path + "/" + conf["nomes"], "w") as f:
        f.write(nomes_limpos)

def get_apelidos():
    """
    Função que atualiza o dicionario de apelidos
    """
    global apelidos
    with open(path + "/" + conf["apelidos"], "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                nome = line[0].upper() + line[1:]
                letra_inicial = nome[0] 
                if letra_inicial in apelidos.keys():
                    apelidos[letra_inicial].append(line)
                else:
                    apelidos[letra_inicial] = [line] 

def get_nomes():
    """
    Função que atualiza o dicionario de nomes
    """
    global nomes
    with open(path + "/" + conf["nomes"], "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                nome = line[0].upper() + line[1:]
                letra_inicial = nome[0] 
                if letra_inicial in nomes.keys():
                    nomes[letra_inicial].append(line)
                else:
                    nomes[letra_inicial] = [line]

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
        #args["input"] = input("Ficheiro de input: ")

#    if args["nomes"]:
#        guarda_nomes()
#    
#    if args["apelidos"]:
#        guarda_apelidos()
    
    get_nomes()
    get_apelidos()

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

main()