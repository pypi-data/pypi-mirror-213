"""
Módulo que trata os nomes e apelidos, sendo obtidos a partir de Web Scraping.
Os nomes e apelidos são apenas os considerados válidos em Portugal.
"""

import requests
import bs4
from .utils import limpa, runcmd
import os

path = os.path.dirname(os.path.abspath(__file__))

def guarda_apelidos(conf):
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

def guarda_nomes(conf):
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

def get_apelidos(conf):
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

def get_nomes(conf):
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