import nltk
import math

stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()
index = {}
listWordsFile = []
listDictPesos = []

base = open("base.txt", "r")                                                            #Abre arquivo
fileContent = base.readlines()                                                          #Recebe o conteúdo de cada arquivo
base.close()

arqQuery = open("consulta.txt", "r")
query = arqQuery.readlines()
arqQuery.close()

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
            if index.get(content[j]) == None:                                           #Cria um dicionario, onde a chave é cada palavra da base e o valor os documentos em que aparecem
                index[content[j]] = [i]
            else:
                listAux = index.get(content[j])
                listAux.append(i)
                index[content[j]] = listAux
        listWordsFile.append(content)

def makeTerms():                                                                        #Cria indice invetido
    terms = sorted(list(index.keys()))                                                  #onde seu número será sempre sua posição +1
    return terms

def calculatedIDF(word):
    numFilesAppear = len(set(index.get(word)))
    IDF = (math.log10(len(fileContent) / numFilesAppear))
    return IDF

def calculatedTF(word, numArquivo):                                                    #Função determina quantas ocorrencias uma palavra aparece em um arquivo
    TF = 0                                                                             #e em quantos arquivos aparece
    for i in index.get(word):
        if (i == numArquivo):
            TF += 1
    return TF

def makePesos(listTerms):
    pesos = open('pesos.txt', 'w')
    for i in range(0, len(listWordsFile)):                                              #Percorre para cada documento da base para determinar os pesos de suas palavras
        dict = {}
        pesos.write(str(fileContent[i].replace('\n', '')) + ': ')
        for word in listTerms:                                                          #Percorre o indice invertido
            if word in listWordsFile[i]:                                                #Verifica se a palavra atual, pertence ao documento atual
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

def queryManipulate(query, listTerms):
    query = query.replace('\n','')
    query = query.split('|')                                                            #Quebra consulta no OU, para criar subconsultas
    treated_query = []
    for i in query:
        treated_query.append(i.replace(' ', '').split('&'))

    for i in range(1):
        listSimiliaridade = []
        for subconsulta in treated_query:
            print(subconsulta)
            num = 0
            resultado = 0
            vetWord = 0
            vetQuery = 0
            for word in subconsulta:
                if word not in stopwords:
                    word = stemmer.stem(word)
                    idf_word = calculatedIDF(word)
                    tfidf_query = (1 + (math.log10(1))) * idf_word
                    number = listTerms.index(word) + 1
                    tfidf_word = listDictPesos[2].get(number)
                    if tfidf_word != None:
                        num += tfidf_word * tfidf_query
                        vetWord += tfidf_word * tfidf_word
                        vetQuery += tfidf_query * tfidf_query
            if num > 0:
                resultado = num / (math.sqrt(vetWord) * math.sqrt(vetQuery))
            else:
                resultado = 0
            listSimiliaridade.append(resultado)
    print(listSimiliaridade)
baseManipulate(fileContent)
listTerms = makeTerms()
print(makePesos(listTerms)[2])
#print(listDictPesos)
queryManipulate(query[0], listTerms)