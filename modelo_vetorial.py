import nltk

stopwords = nltk.corpus.stopwords.words("portuguese")
stemmer = nltk.stem.RSLPStemmer()

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
        content = [value for value in content if value not in characters]               #Remove os caracteres
        content = [value for value in content if value not in stopwords]                #Remove as stopwords
        for j in range(0, len(content)):
            content[j] = stemmer.stem(content[j].lower())                               #Substitui palavra pelo radical e a coloca em minuscula

        print(content)




baseManipulate(fileContent)