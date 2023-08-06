import subprocess
import re
import spacy
import spacy.cli
import os

path = os.path.dirname(os.path.abspath(__file__)) 

def limpa(txt):
    """
    Função que limpa o texto de caracteres indesejados
    """
    regex = r'(\[\d+\])|(\(.*\))'
    regex += r'|(\d)'
    regex += r'|(.+\s+)+'
    return re.sub(regex, '', txt.strip())

def runcmd(cmd, verbose = False, *args, **kwargs):
    """
    Função que executa um comando de terminal
    """
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

def trata_usernames_url(linha):
    """
    Função que trata os usernames imbutidos em urls, facebook e linkedin 
    """
    # https://www.facebook.com/goncalo.freitas.12/
    
    regex_1 = r'((https|http)\:\/\/)?(www\.)?facebook\.com\/[a-zA-Z0-9\.\-\_]+\/?'
        
    # https://www.linkedin.com/in/pedro-ferreira-56031a267/
    regex_2 = r'((https|http)\:\/\/)?(www\.)?linkedin\.com\/in\/[a-zA-Z0-9\.\-\_]+\/?'

    # https://twitter.com/goncalofr8tas
    regex_3 = r'((https|http)\:\/\/)?(www\.)?twitter\.com\/[a-zA-Z0-9\.\-\_]+\/?'

    # https://www.instagram.com/goncalofr8as/
    regex_4 = r'((https|http)\:\/\/)?(www\.)?instagram\.com\/[a-zA-Z0-9\.\-\_]+\/?'

    if re.search(regex_1,linha):
        return re.sub(regex_1, 'facebook...', linha)

    
    elif re.search(regex_2,linha):
        return re.sub(regex_2, 'linkedin...', linha)
    
    elif re.search(regex_3,linha):
        return re.sub(regex_3, 'twitter...', linha)
    
    elif re.search(regex_4,linha):
        return re.sub(regex_4, 'instagram...', linha)
    
    else:
        return linha

def trata_handles(linha):
    """
    Função que trata os handles do gênero de twitter/instagram
    """
    regex = r'(@[a-zA-Z0-9\_]+)'
    return re.sub(regex, '@...', linha)

def trata_emails(linha):
    """
    Função que trata os emails
    """
    regex = r'([a-zA-Z0-9\.\-\_]+@[a-zA-Z0-9\.\-\_]+)'
    return re.sub(regex, 'email...', linha)

def trata_urls(linha):
    """
    Função que trata os urls
    """
    regex = r'(((http|https|ftp|ftps)\:\/\/)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?)'
    regex += r'|((www\.)?[a-zA-Z0-9\-\.]+\.[a-z]{2,3}(\/\S*)?)'

    return re.sub(regex, 'www...', linha)

def trata_nomes(linha: str,dic_nomes,dic_apelidos):
    """
    Função que trata os nomes e apelidos
    """
    
    for word in linha.split(" "):
        if len(word) > 0:
            inicial = word[0]
            if (inicial in dic_nomes.keys() and word in dic_nomes[inicial]) or \
               (inicial in dic_apelidos.keys() and word in dic_apelidos[inicial]):
                    linha = linha.replace(word, word[0]+".")

    return linha


def trata_datas(linha: str):
    """
    Função que trata as datas
    """
    sep = ["-", "/"]

    # 27/02/1998
    # 1998/02/27
    # #
    # fomarto numerico
    for s in sep:
        # dia mes ano | mes dia ano
        regex = r'(\d{1,2})'+s+'(\d{1,2})'+s+'(\d{2,4})'
        # ano mes dia | ano dia mes
        regex += r'|((1|2)\d{3})'+s+'(\d{1,2})'+s+'(\d{1,2})'
        # mes ano | dia mes
        regex += r'|(\d{1,2})'+s+'(\d{2,4})'
        # ano mes | dia mes
        regex += r'|(\d{2,4})'+s+'(\d{1,2})'

            
        linha = re.sub(regex, 'data...', linha)

    # formato textual
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho","agosto", "setembro", "outubro", "novembro", "dezembro"]
    # diferents representacoes de meses


    # 27 de fevereiro de 1998

    for mes in meses:
        # janeiro | jan | Janeiro | Jan | JANEIRO | JAN
        mes = r'(('+mes+')|('+mes[:3]+')|('+mes[0].upper()+mes[1:]+')|('+mes[0].upper()+mes[1:3]+')|('+mes.upper()+')|('+mes[:3].upper()+'))'

        # 26 de fevereiro de 1998 | 26 de fevereiro 1998 
        regex = r'((\d{1,2})\s+(de)?\s*'+ mes + '\s+(de)?\s*\d{2,4})'
        # 26 de fevereiro
        regex += r'|((\d{1,2})\s+de\s+'+ mes + ')'
        # Fevereiro 21, 2012 | fevereiro 21 2012
        regex += r'|('+mes+'\s+(\d{1,2})\s*,?\s+(\d{2,4}))'
        # 21 Fevereiro, 2012 | 21 Fevereiro 2012
        regex += r'|((\d{1,2})\s+(de)?\s*'+mes+'\s*(de)?,?\s+(\d{2,4}))'

  
        linha = re.sub(regex, 'data...', linha)

    return linha

def trata_spacy(text: str, nlp=None):
    """
    Função que trata o reconhecimento de nomes de organizações
    """
    if nlp is None:
        try:
            nlp = spacy.load('xx_ent_wiki_sm')

        except OSError:
            spacy.cli.download('xx_ent_wiki_sm')
            nlp = spacy.load('xx_ent_wiki_sm')

    words = []
    doc = nlp(text)    

    #sprint("--------  MULTI  ---------")
    for w in doc.ents:
        #print(w.text, w.start_char, w.end_char, w.label_)
        if w.label_ == "ORG":
            words.append(w.text)


    return words, nlp

def trata_codigos_postais(linha):
    """
    Função que trata os códigos postais
    """
    regex = r'(\d{4})\s*\-\s*(\d{3})'
    return re.sub(regex, 'cod-postal...', linha)

def trata_entre_aspas(linha):
    """
    Função que trata o texto entre aspas
    """
    regex = r'\"(.+?)\"'
    return re.sub(regex, '"..."', linha)


def trata_moradas(linha):
    """
    Função que trata as moradas
    """ 
    regex = r'((Rua)|(Travessa)|(Avenida)|(Praceta)|(Praça)|(Largo)|(Alameda))'
    regex += r'.*?(,|-).*?\d{4}-\d{3}'
    return re.sub(regex, 'morada...', linha)

def trata_documentos(linha):
    
    carta_conducao = r'[A-Z]{2}-\d+ \d'
    linha = re.sub(carta_conducao, 'carta-conducao...', linha)

    cc = r'\d{8} \d [A-Z]{2}\d'
    linha = re.sub(cc, 'cc...', linha)

    niss = r'\d{11}'
    linha = re.sub(niss, 'niss...', linha)

    nif = r'\d{9}'
    linha = re.sub(nif, 'nif...', linha)

    passaporte = r'[A-Z]{2}\d{6}'
    linha = re.sub(passaporte, 'passaporte...', linha)

    return linha

def trata_experimental(linha):
    """
    Função que utiliza um pequeno modelo treinado por nós para identificar nomes, datas e moradas 
    """
    # carrega o modelo
    nlp = spacy.load(path + "/dados/moradas_model")
    doc = nlp(linha)
    print("-------- EXPERIMENTAL --------")
    for ent in doc.ents:
        print(linha)
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == "NOME":
            linha = linha.replace(ent.text, "NOME...")
        elif ent.label_ == "DATA":
            linha = linha.replace(ent.text, "DATA...")
        elif ent.label_ == "MOR":
            linha = linha.replace(ent.text, "MORADA...")
    return linha

def trata_geral(linha,args,nlp=None,extra=False):
    """
    Função que aplica todas as funções de tratamento
    """
    init = linha
    # o que está entre aspas é considera como sensível
    linha = trata_entre_aspas(linha)
    linha = trata_usernames_url(linha)
    linha = trata_emails(linha)
    linha = trata_handles(linha)
    linha = trata_urls(linha)    
    linha = trata_moradas(linha)
    linha = trata_nomes(linha,args["nomes"],args["apelidos"])
    linha = trata_documentos(linha)
    linha = trata_codigos_postais(linha)
    linha = trata_datas(linha)

    words, nlp = trata_spacy(linha,nlp)
    for word in words:
        linha = linha.replace(word, "ORG...")

    if extra:
        linha = trata_experimental(linha)

    return linha,nlp