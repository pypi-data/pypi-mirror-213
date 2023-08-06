import csv
import re
import os
import spacy

from faker import Faker

input = [
    # input com morada, nome próprio e localidade
("O meu nome é João e moro na Rua da Alegria, 123, 4567-890 Lisboa", {"entities" : [(13, 17, "NOME"), (28, 64, "MOR")]}),
("A minha morada é Rua do Meio  3850-093 Albergaria-a-velha, nasci em 1990 e chamo-me Karim Benzema",   {"entities" : [(17, 57, "MOR"), (68,72,"DATA"),(84, 97, "NOME")]}),
("Desde o dia 27 de Agosto que moro na Praceta Professor Júlio Catarino  Ílhavo Ílhavo 3830-216", {"entities" : [(12, 23, "DATA"),(37, 93, "MOR")]}),
("Sou o Gonçalo da Cunha Freitas, nasci na Avenida General Humberto Delgado 7780-123 Castro Verde",{ "entities" : [(6, 30, "NOME"),(41, 95, "MOR")]}),
("O novo local será no Caminho do Espinheiro Milhazes, tendo sido o Henrique Machado o organizador do evento", {"entities" : [(21, 51, "MOR"),(67, 82, "NOME")]}),
("O meu nome é Maria e moro na Rua das Flores, 567, 1234-567 Porto.",{"entities": [(13, 18, "NOME"), (29, 64, "MOR")]}),
("A minha morada é Travessa das Oliveiras, 4567-890 Braga, nasci em 1985 e chamo-me Ana Silva.",{"entities": [(17, 55, "MOR"), (66, 70, "DATA"), (82, 91, "NOME")]}),
("Desde 10/09/2001 moro na Avenida Central, 7890-123 Coimbra.",{"entities": [(6, 16, "DATA"), (25, 58, "MOR")]}),
("Sou o Pedro Santos da Silva Pereira e nasci a 27 de Janeiro de 2013.",{"entities": [(6, 35, "NOME"), (46, 67, "DATA")]}),
("O organizador do evento foi Miguel Oliveira.", {"entities": [(28, 43, "NOME")]}),
("O meu nome é Sofia Teixeira Ribeiro e moro na Avenida Professor Maximino Correia - Vila Flor - 5360-304.", {"entities": [(13, 35, "NOME"), (46, 103, "MOR")]}),
("A Travessa do Sol, 6789-012 Porto é a minha nova casa.", {"entities": [(2, 33, "MOR")]}),
("Desde Julho de 1900, o senhor Roberto mora comigo na Avenida Principal, 3456-789 Braga.", {"entities": [(6, 19, "DATA"), (30, 37, "NOME"), (53, 86, "MOR")]}),
("O jornalista João do Bronx entrevistou Wilson Carvalho.", {"entities": [(13, 26, "NOME"), (39, 54, "NOME")]}),
]


def get_random(max: int):
    """
    Retorna um inteiro aleatório entre 0 e max
    """
    return int.from_bytes(os.urandom(3), byteorder="big") % max

def trata_espacos(texto):
    """
    Função que trata os espaços no texto
    """
    regex = r'\s+'

    out = ""
    if len(texto.strip()) > 0:
        out = re.sub(regex, ' ', texto)

    return out

def moradas():
    """
    Função que trata o dataset de moradas para o formato desejado 
    """
    # get moradas from csv file
    moradas = []
    with open('dados/codigos_postais.csv',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
       
        idx = 0
        for row in reader:
            if get_random(10000) <= 9900:
                continue
            idx = get_random(3)
            if idx % 3 == 0:
                sep = " "
            elif idx % 3 == 1:
                sep = ", "
            else:
                sep = " - "
            

            # rua
            
            
            txt = trata_espacos(" ".join(row[5:13]))

            rand = get_random(2)

            if rand == 0:
                # codigo postal
                if len(txt.strip()) > 0:
                    txt += sep
                txt += "-".join(row[14:16])

            # localidade
            if len(txt.strip()) > 0:
                txt += sep
            txt += row[16][0] + row[16][1:].lower() + sep + row[3]

            if rand == 1:
                # codigo postal
                txt += sep + "-".join(row[14:16])
            

            entry = (txt, {"entities" : [(0, len(txt), "MOR")]})

            moradas.append(entry)

    with open('dados/moradas.txt', 'w',encoding="utf-8") as f:
        for morada in moradas:
            f.write(morada[0] + "\n")


    return moradas


def train_module():
    nlp = spacy.blank("pt")  # Initialize a blank Portuguese model
    ner = nlp.add_pipe("ner")  # Add the NER component

    ner.add_label("MOR")
    ner.add_label("NOME")
    ner.add_label("DATA")

    idx = 0
    optimizer = nlp.begin_training()
    losses = {}
    global input
    for it in range(100):
        for text, annotations in input:
            doc = nlp.make_doc(text)
            example = spacy.training.Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
            idx += 1
            if idx % 1000 == 0:
                print(idx)
        print("Losses: ",losses)

    nlp.to_disk("dados/moradas_model")

#model = moradas()

train_module()