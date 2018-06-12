import nltk
import math

stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()

base = open("base.txt", "r")                                                           #Abre arquivo
fileContent = base.readlines()                                                         #Recebe o conteúdo de cada arquivo
base.close()


def brokenText(fileContent):
    fileWords = (nltk.word_tokenize(fileContent))                                      #Quebra um texto em palavras
    return fileWords

def tf(word, list):
    return list.count(word) / len(list)

#def idf(word, )

def baseManipulate(fileContentBase):
    characters = ['','!',',','?','\n','.']
    listDict = []
    for i in range(0, len(fileContent)):
        dict = {}
        nameFile = 'Bases/' + fileContentBase[i].replace('\n', '')
        base = open(nameFile, "r")  # Abre arquivo
        content = base.read()       # Recebe o conteúdo de cada arquivo
        base.close()
        content = brokenText(content)
        content = [value for value in content if value not in characters]               #Remove os caracteres especiais
        for i in range(len(content)):
            content[i] = content[i].lower()
        content = [value for value in content if value not in stopwords]                #Remove as stopwords

        #print(content)

        for j in range(0, len(content)):
            content[j] = stemmer.stem(content[j])                                       #Substitui palavra pelo radical
            if dict.get(content[j]) == None:
                dict[content[j]] = 1
            else:
                dict[content[j]] += 1
        dict['tamanho'] = len(content)
        listDict.append(dict)
    return listDict



