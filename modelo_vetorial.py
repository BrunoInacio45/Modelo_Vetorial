import nltk
import math
import collections
import sys

stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()
index = {}
listWordsFile = []
listDictPesos = []

nomeArqBase = sys.argv[1]#'base.txt'
nomeArqConsulta = sys.argv[2]#'consulta.txt'


base = open(nomeArqBase, "r")                                                            #Abre arquivo
fileContent = base.readlines()                                                           #Recebe o conteúdo de cada arquivo
base.close()

arqQuery = open(nomeArqConsulta, "r")
query = arqQuery.readlines()
arqQuery.close()
print("Consulta: ", query)

#Função para quebrar palavras transformando-as em lista
def brokenText(fileContent):
    fileWords = (nltk.word_tokenize(fileContent))                                       #Quebra um texto em palavras
    return fileWords

#Função para manipular a base de documentos
def baseManipulate(fileContentBase):
    characters = ['','!',',','?','\n','.']
    for i in range(0, len(fileContent)):
        nameFile = fileContentBase[i].replace('\n', '')
        base = open(nameFile, "r")                                                      #Abre arquivo
        content = base.read()                                                           #Recebe o conteúdo de cada arquivo
        base.close()
        content = brokenText(content)
        content = [value for value in content if value not in characters]               #Remove os caracteres especiais
        for w in range(len(content)):                                                   #Coloca tudo em minúsculo
            content[w] = content[w].lower()
        content = [value for value in content if value not in stopwords]                #Remove as stopwords

        for j in range(0, len(content)):
            content[j] = stemmer.stem(content[j])                                       #Substitui palavra pelo radical
            if index.get(content[j]) == None:                                           #Cria um dicionario, onde a chave é cada palavra da base e o valor os documentos em que aparecem
                index[content[j]] = [i]
            else:
                listAux = index.get(content[j])
                listAux.append(i)
                index[content[j]] = listAux
        listWordsFile.append(content)

#Função criada para criar o índice ordenado
def makeTerms():                                                                        #Cria indice invetido
    terms = sorted(list(index.keys()))                                                  #onde seu número será sempre sua posição +1
    return terms

#Função criada para calcular o IDF de um termo
def calculatedIDF(word):
    numFilesAppear = len(set(index.get(word)))
    IDF = (math.log10(len(fileContent) / numFilesAppear))
    return IDF

#Função criada para calcular a frequência de um termo -Obs: O log é aplicado onde é chamado a função
def calculatedTF(word, numArquivo):                                                    #Função determina quantas ocorrencias uma palavra aparece em um arquivo
    TF = 0                                                                             #e em quantos arquivos aparece
    for i in index.get(word):
        if (i == numArquivo):
            TF += 1
    return TF

#Função criada para escrever o arquivo 'pesos.txt'
def makePesos(listTerms):
    pesos = open('pesos.txt', 'w')
    for i in range(0, len(listWordsFile)):                                              #Percorre para cada documento da base para determinar os pesos de suas palavras
        dict = {}
        pesos.write(str(fileContent[i].replace('\n', '')) + ': ')
        for word in listTerms:                                                          #Percorre o indice invertido
                TF = calculatedTF(word, i)                                              #Chama função para obter TF
                IDF = calculatedIDF(word)                                               #Chama função para obter IDF
                if TF > 0:                                                              #Se TF > 0, faz cálculo do TF-IDF
                    calculatedTF_IDF = (1 + (math.log10(TF))) * IDF
                else:                                                                   #Caso contrário, atribui 0
                    calculatedTF_IDF = 0
                number = listTerms.index(word) + 1                                      #Pega a posição da palavra no índice
                if calculatedTF_IDF != 0:                                               #Se não for 0, escreve no documento
                    pesos.write(str(number) + ',' + str(calculatedTF_IDF) + ' ')
                dict[number] = calculatedTF_IDF
        listDictPesos.append(dict)                                                           #Cria uma lista de dicionários, onde cada dicionário representa os pesos de suas respectivas palavras
        pesos.write("\n")
    return listDictPesos

#Função criada para calcular a similaridade entre um documento e uma consulta
def calculatedSimilarity(vetDocument,vetQuery):
    num = 0
    vetQueryAux = 0
    vetDocumentAux = 0
    for i in range(0, len(vetDocument)):
        num += vetDocument[i] * vetQuery[i]                                             #Cria o somatório da multiplicação entre o peso do termo no doc e na consulta
        vetDocumentAux += vetDocument[i] * vetDocument[i]                               #Cria o somatório dos vetores ao quadrado do documento
        vetQueryAux += vetQuery[i] * vetQuery[i]                                        #Cria o somatório dos vetores ao quadrado da consulta
    den = math.sqrt(vetDocumentAux) * math.sqrt(vetQueryAux)                            #Tira as raizes e depois aplica a multiplicação
    if num > 0:
        return num / den                                                                #Retorna a divisão do numerador e denominador
    else:
        return 0                                                                        #Retorna 0 se o numerador for menor ou igual a 0

#Função criada para manipular a consulta passada pelo usuário
def queryManipulate(query, listTerms):
    query = query.replace('\n','')
    query = query.split('|')                                                            #Quebra consulta no OU, para criar subconsultas
    treated_query = []                                                                  #Trata a consulta
    for i in query:
        treated_query.append(i.replace(' ', '').split('&'))

    answer = []
    numDocuments = 0
    for i in range(len(fileContent)):                                                   #Laço para definir similaridade de cada documento
        vetDocument = list(listDictPesos[i].values())                                   #Cria vetor de pesos do documento
        listSimilarity = []
        for subconsulta in treated_query:
            vetQuery = [0] * len(listDictPesos[i])
            for word in subconsulta:
                if word not in stopwords:                                               #Verifica se a palavra está na lista de stopwords
                    word = stemmer.stem(word)                                           #Calcula o IDF da palavra da consulta
                    idf_word = calculatedIDF(word)                                      #Busca o número dela no índice
                    number = listTerms.index(word) + 1
                    p = collections.OrderedDict(listDictPesos[i])
                    position = list(p.keys()).index(number)
                    vetQuery[position] = ((1 + (math.log10(1))) * idf_word)             #Cria o vetor de pesos da consulta
                    listSimilarity.append(calculatedSimilarity(vetDocument,vetQuery))   #Chama a função de calcula a similaridade passandos os dois vetores
        maxSimilarity = max(listSimilarity)                                             #Pega o maior valor entre as subconsultas
        answer.append(maxSimilarity)
        if maxSimilarity >= 0.001:                                                      #Verifica se o valor é maior que 0.001
            numDocuments += 1
    makeResposta(answer,numDocuments)                                                   #Chama função para gravar no arquivo

#Função criada para escrever o arquivo 'resposta.txt'
def makeResposta(answer,numDocuments):
    resposta = open('resposta.txt', 'w')
    print("Numero de documentos que atendem a consulta: ", numDocuments, '\nDocumentos:')
    resposta.write(str(numDocuments) + '\n')
    for i in range(len(answer)):
        if answer[i] >= 0.001:
            resposta.write(fileContent[i].replace('\n','') + ' ' + str(answer[i]) + '\n')
            print(fileContent[i].replace('\n',''))

#Função principal
def main():
    baseManipulate(fileContent)
    listTerms = makeTerms()
    makePesos(listTerms)
    queryManipulate(query[0], listTerms)

if __name__ == '__main__':
    main()