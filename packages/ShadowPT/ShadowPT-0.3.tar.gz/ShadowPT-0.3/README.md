# Anonimização de dados

"If you think you've anonymized your data, you're probably wrong"


A anonimização de dados é um processo que tem como objetivo remover ou
ocultar informações pessoais identificáveis dos dados, de forma a
garantir a privacidade dos indivíduos e a proteção de dados sensíveis.
Instituições como Tribunais ou Hospitais possuem grandes quantidades de
informação que pode ser utilizada para vários fins. Tratando-se de
informações sensíveis, tais como acórdãos judiciais e relatórios médicos
é necessário proceder à anonimização dos mesmos de modo a garantir a
segurança e privacidade das pessoas mencionadas nesses documentos.

Dados considerados para anonimização:

-   Nomes de pessoas, alcunhas e apelidos

-   Moradas e códigos postais

-   Datas

-   Números pessoais ou fiscais, número de passaporte, número de carta
    de condução ou qualquer outro documento pessoal

-   Endereços de correio eletrónico, endereços web,endereço de redes
    sociais (e nomes de utilizador)

-   Nomes de Organizações

-   Informação entre aspas

No que diz respeito ao método concreto de anonimização apresentamos as
seguintes abordagens:

-   O nome, alcunha e apelido reais são substituídos pelas
    correspondentes iniciais intercaladas com ponto final;

-   Os endereços de correio electrónico, endereços web e de redes
    sociais são substituídos pelo tipo de serviços de internet seguido
    de três pontos. Por exemplo:

    -   Endereço de correio electrónico = email\...

    -   Página web = www\...

    -   Endereço de rede social = facebook\... , twitter\... , linkedin\... ou instagram\...

-   Os nomes de utilizador (*handles*) do gênero de twitter e instagram são substituidos pelo arroba inicial. Poe exemplo:
    -   @spln2223 = @\... 

-   Os números de cartão de cidadão, carta de condução, segurança social e identificação fiscal são anonimizados através da utilização de
    uma palavra para a descrição do documento, seguida de três pontos.
    Por exemplo:

    -   Número de passaporte AA000000 = passaporte\....

-   A informação entre aspas é considerada sensível e portanto é completamente subsituida por "..."

-   As datas e moradas (e em casos especiais códigos postais) são anonimizados através da utilização de uma palavra que a descreve. Por exemplo:
    -   Rua 25 de Abril, Silvares, Guimarães = morada\...
    -   4834-300 = codigo-postal\... 
    -   27 de Agosto = data\...


# Utilização

    shadow [-h] [-i INPUT] [-o OUTPUT] [--nlp]

    -h, --help            Mostra uma mensagem de ajuda e termina
    -i INPUT, --input INPUT
                        Ficheiro de input
    -o OUTPUT, --output OUTPUT
                        Ficheiro de output
    --nlp
        Flag opcional para utilização de funcionalidade experimental

# Identificação de entidades

Para a maior parte da identificação é utilizado regex, contudo isto não acontece com a identificação de Organizações e identificação de pessoas. No primeiro caso é utilizado um modelo multi-língua do *spacy*, com o qual obtivemos os melhores resultados. No segundo caso em primeiro lugar procuramos por todos os nomes próprios e apelidos permitidos em Portugal e fazemos match no texto com estes nomes. 

# Funcionalidade Experimental

Invocando o programa com a *flag* "--nlp", o programa passa a utilizar um modelo treinado no ficheiro moradas.py. Esta funcionalidade está implementada contudo o modelo continua a não ser extenso o suficiente e sendo obtidos resultados estranhos. 

Módulo desenvolvido no contexto da UC de SPLN do Mestrado Integrado em Engenharia Informática da Universidade do Minho (UMinho).