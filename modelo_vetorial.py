import nltk
import math

stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()
index = {}
listWordsFile = []
listWordsFileOrigin = []

base = open("base.txt", "r")                                                           #Abre arquivo
fileContent = base.readlines()                                                         #Recebe o conteúdo de cada arquivo
base.close()

def brokenText(fileContent):
    fileWords = (nltk.word_tokenize(fileContent))                                      #Quebra um texto em palavras
    return fileWords

def baseManipulate(fileContentBase):
    characters = ['','!',',','?','\n','.']
    for i in range(0, len(fileContent)):
        nameFile = 'Bases/' + fileContentBase[i].replace('\n', '')
        base = open(nameFile, "r")  # Abre arquivo
        content = base.read()       # Recebe o conteúdo de cada arquivo
        base.close()
        content = brokenText(content)
        content = [value for value in content if value not in characters]               #Remove os caracteres especiais
        listWordsFileOrigin.append(content)
        for w in range(len(content)):                                                   #Coloca tudo em minúsculo
            content[w] = content[w].lower()
        content = [value for value in content if value not in stopwords]                #Remove as stopwords

        for j in range(0, len(content)):
            content[j] = stemmer.stem(content[j])                                       #Substitui palavra pelo radical

            if index.get(content[j]) == None:                                           #Cria dicionario com arquivos que
                index[content[j]] = [i]                                                 #a palavra aparece
            else:
                listAux = index.get(content[j])
                listAux.append(i)
                index[content[j]] = listAux
        listWordsFile.append(content)
    return listWordsFile

def numberInFiles(word, numArquivo):
    contOcorrencia = 0
    numFilesAppear = len(set(index.get(word)))
    for i in index.get(word):
        if (i == numArquivo):
            contOcorrencia+=1
    return contOcorrencia, numFilesAppear


def makePesos():
    listDict = []
    pesos = open('pesos.txt', 'w')
    for i in range(0, len(listWordsFileOrigin)):
        dict = {}
        pesos.write(str(fileContent[i].replace('\n', '')) + ': ')
        for j in range(0,len(listWordsFileOrigin[i])):
            if listWordsFileOrigin[i][j] not in stopwords:
                word = stemmer.stem(listWordsFileOrigin[i][j])
                frequency, numberOfDocuments = numberInFiles(word, i)
                TF = frequency
                IDF = len(fileContent) / numberOfDocuments
                if TF > 0:
                    calculatedTF_IDF = (1 + (math.log10(TF))) * (math.log10(IDF))
                else:
                    calculatedTF_IDF = 0
                if calculatedTF_IDF != 0:
                    dict[j+1] = calculatedTF_IDF
                    pesos.write(str(j+1) + ','  + str(calculatedTF_IDF) + ' ')
        pesos.write("\n")
        listDict.append(dict)
    return listDict

baseManipulate(fileContent)
print(makePesos())

