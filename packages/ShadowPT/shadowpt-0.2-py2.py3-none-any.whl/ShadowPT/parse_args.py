"""
Módulo de tratamento de argumentos com argparse
"""
import argparse


def parse_args():
    """
    Processa e gera o dicionário de argumentos
    """
    parser = argparse.ArgumentParser(
                    prog='ShadowPT',
                    description='Ferramenta de anonimização de texto',
                    epilog='Módulo desenvolvido no contexto da UC de SPLN do Mestrado Integrado em Engenharia Informática da Universidade do Minho (UMinho).')
    
    dic = {}

    parser.add_argument('-i', '--input', help='Ficheiro de input', default='stdin')
    parser.add_argument('-o', '--output', help='Ficheiro de output', default='stdout')
    parser.add_argument('--nlp', help='Flag para funcionalidade experimental', action='store_true')
    
    args = parser.parse_args()
    dic['input'] = args.input
    dic['output'] = args.output
    dic['nlp'] = args.nlp

    return dic