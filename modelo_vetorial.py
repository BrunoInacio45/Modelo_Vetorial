import nltk
import math

stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()
index = {}
listWordsFile = []

base = open("base.txt", "r")                                                            #Abre arquivo
fileContent = base.readlines()                                                          #Recebe o conteúdo de cada arquivo
base.close()

def brokenText(fileContent):
    fileWords = (nltk.word_tokenize(fileContent))                                       #Quebra um texto em palavras
    return fileWords

def baseManipulate(fileContentBase):
    characters = ['','!',',','?','\n','.']
    for i in range(0, len(fileContent)):
        nameFile = 'Bases/' + fileContentBase[i].replace('\n', '')
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
            if index.get(content[j]) == None:                                           #Cria dicionario com arquivos que a palavra aparece
                index[content[j]] = [i]
            else:
                listAux = index.get(content[j])
                listAux.append(i)
                index[content[j]] = listAux
        listWordsFile.append(content)



def makeTerms():                                                                        #Cria indice invetido
    terms = sorted(list(index.keys()))                                                  #onde seu número será sempre sua posição +1
    return terms

def numberInFiles(word, numArquivo):                                                    #Função determina quantas ocorrencias uma palavra aparece em um arquivo
    contOcorrencia = 0                                                                  #e em quantos arquivos aparece
    numFilesAppear = len(set(index.get(word)))
    for i in index.get(word):
        if (i == numArquivo):
            contOcorrencia += 1
    return contOcorrencia, numFilesAppear

def makePesos():
    listDict = []
    listTerms = makeTerms()
    pesos = open('pesos.txt', 'w')
    for i in range(0, len(listWordsFile)):                                              #Percorre para cada documento da base
        dict = {}
        pesos.write(str(fileContent[i].replace('\n', '')) + ': ')
        for word in listTerms:                                                          #Percorre o indice invertido
            if word in listWordsFile[i]:                                                #Verifica se a palavra atual, pertence ao documento atual
                frequency, numberOfDocuments = numberInFiles(word, i)                   #Chama função para cálculo do TF e IDF
                TF = frequency
                IDF = len(fileContent) / numberOfDocuments
                if TF > 0:                                                              #Se TF > 0, faz cálculo do TF-IDF
                    calculatedTF_IDF = (1 + (math.log10(TF))) * (math.log10(IDF))
                else:                                                                   #Caso contrário, atribui 0
                    calculatedTF_IDF = 0
                number = listTerms.index(word) + 1                                      #Pega a posição da palavra no índice
                if calculatedTF_IDF != 0:                                               #Se não for 0, escreve no documento
                    pesos.write(str(number) + ',' + str(calculatedTF_IDF) + ' ')
                dict[number] = calculatedTF_IDF
        listDict.append(dict)                                                           #Cria uma lista de dicionários, onde cada dicionário representa os pesos de suas respectivas palavras
        pesos.write("\n")
    return listDict


baseManipulate(fileContent)
print(makePesos())
