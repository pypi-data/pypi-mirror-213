import argparse


def parse_args():
    """
    Processa e gera o dicionário de argumentos
    """
    parser = argparse.ArgumentParser(
                    prog='Anonimator',
                    description='Ferramenta anonimizadora de texto',
                    epilog='Trabalho realizado no contexto da UC de SPLN do Mestrado Integrado em Engenharia Informática da Universidade do Minho (UMinho).')
    
    dic = {}

    parser.add_argument('-i', '--input', help='Ficheiro de input', default='stdin')
    parser.add_argument('-o', '--output', help='Ficheiro de output', default='stdout')
    #parser.add_argument('-n', '--nomes', help='Diretoria do ficheiro de nomes próprios, apenas utilizar esta flag se pretender atualizar o programa com um novo ficheiro de nomes', default=None)
    #parser.add_argument("-a", "--apelidos", help="Diretoria do ficheiro de apelidos, apenas utilizar esta flag se pretender atualizar o programa com um novo ficheiro de apelidos", default=None)
    parser.add_argument('--nlp', help='Flag para funcionalidade experimental', action='store_true')
    
    args = parser.parse_args()
    dic['input'] = args.input
    dic['output'] = args.output
    #dic['nomes'] = args.nomes
    #dic['apelidos'] = args.apelidos
    dic['nlp'] = args.nlp

    return dic