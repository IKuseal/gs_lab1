from socket import *
from general import *
import math
import random

text = "Стек протоколов TCP/IP (Transmission Control Protocol/Internet Protocol, протокол управления " \
           "передачей/протокол интернета) — сетевая модель, описывающая процесс передачи цифровых данных. Она названа по " \
           "двум главным протоколам, по этой модели построена глобальная сеть — интернет. Сейчас это кажется " \
           "невероятным, но в 1970-х информация не могла быть передана из одной сети в другую, с целью обеспечить такую " \
           "возможность был разработан стек интернет-протоколов также известный как TCP/IP. Разработкой этих протоколов " \
           "занималось Министерство обороны США, поэтому иногда модель TCP/IP называют DoD (Department of Defence) " \
           "модель. Если вы знакомы с моделью OSI, то вам будет проще понять построение модели TCP/IP, потому что обе " \
           "модели имеют деление на уровни, внутри которых действуют определенные протоколы и выполняются собственные " \
           "функции. Мы разделили статью на смысловые части, чтобы было проще понять, как устроена модель TCP/IP: Выше " \
           "мы уже упоминали, что модель TCP/IP разделена на уровни, как и OSI, но отличие двух моделей в количестве " \
           "уровней. Документом, регламентирующим уровневую архитектуру модели и описывающий все протоколы, входящие в " \
           "TCP/IP, является RFC 1122. Стандарт включает четыре уровня модели TCP/IP, хотя, например, " \
           "согласно Таненбауму (Таненбаум Э., Уэзеролл Д. Т18 Компьютерные сети. 5-е изд. — СПб.: Питер, 2012. — 960 " \
           "с.: ил. ISBN 978-5-459-00342-0), в модели может быть пять уровней. Три верхних уровня — прикладной, " \
           "транспортный и сетевой — присутствуют как в RFC, так и у Таненбаума и других авторов. А вот стоит ли " \
           "говорить только о канальном или о канальном и физическом уровнях — нет единого мнения. В RFC они объединены, " \
           "поскольку выполняют одну функцию. В статье мы придерживаемся официального интернет-стандарта RFC и не " \
           "выделяем физический уровень в отдельный. Далее мы рассмотрим четыре уровня модели. Предназначение канального " \
           "уровня — дать описание тому, как происходит обмен информацией на уровне сетевых устройств, определить, " \
           "как информация будет передаваться от одного устройства к другому. Информация здесь кодируется, делится на " \
           "пакеты и отправляется по нужному каналу, т.е. среде передачи. Этот уровень также вычисляет максимальное " \
           "расстояние, на которое пакеты возможно передать, частоту сигнала, задержку ответа и т.д. Все это — " \
           "физические свойства среды передачи информации. На канальном уровне самым распространенным протоколом " \
           "является Ethernet, но мы рассмотрим его на примере в конце статьи."

def textToBits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def hemingEncode(data,wordLength):
    data = data.zfill(wordLength*((len(data)+wordLength-1)//wordLength))
    codeBitN = getControlBitsNum(wordLength)
    pos = [2**i for i in range(0,codeBitN)]
    controlBitsValues = []
    wordHeming = ""
    dataHeming = ""
    word = ""
    matrix = generateHemingMatrix(wordLength)

    for j in range(0,len(data)//wordLength):
        # берём след слово и вставляем контрольные биты
        word = data[j*wordLength:(j+1)*wordLength]
        wordList = list(word)
        wordHeming = ""
        fromP = 0
        numCh = 0
        # for i in range(0, codeBitN - 1):
        #     wordHeming += '0'
        #     numCh = pos[i+1] - pos[i] - 1
        #     wordHeming += word[fromP:fromP+numCh]
        #     fromP += numCh
        # wordHeming += '0'
        # wordHeming += word[fromP:]
        for i in range(0, codeBitN):
            if(pos[i] >= len(wordList)):
                wordList.append('0')
            else:
                wordList.insert(pos[i]-1,'0')
        wordHeming = ''.join(wordList)

        # высчитываем остатки и вставляем на место контрольных битов
        controlBitsValues = []
        for i in range(0, codeBitN):
            controlBitsValues.append(str(mult2BitStringsMod2(matrix[i], wordHeming)))

        wordHemingList = list(wordHeming)

        # print(wordHeming)

        for i in range(0, codeBitN):
            wordHemingList[pos[i]-1] = controlBitsValues[i]

        # print(wordHemingList)
        wordHeming = ''.join(wordHemingList)

        dataHeming += wordHeming

    return dataHeming

def addMistakes(seq, extWordLeng, catMistakesSpread):
    # мешаю последовательность
    wordsIndexes = list(range(0, len(seq) // extWordLeng))
    wordsElementIndexes = list(range(0, extWordLeng))
    random.shuffle(wordsIndexes)

    mistakeCat = 0
    procWordN = 0

    for numMistakesOfCat in catMistakesSpread:
        mistakeCat += 1
        for i in range(0,numMistakesOfCat):
            wordIndex = wordsIndexes[procWordN]
            procWordN += 1
            mistakeIndexes = random.sample(wordsElementIndexes, mistakeCat)
            for j in mistakeIndexes:
                el = seq[wordIndex*extWordLeng + j]
                if(el == '0'):
                    seq[wordIndex * extWordLeng + j] = '1'
                else:
                    seq[wordIndex * extWordLeng + j] = '0'
    return seq

def main():
    # подготавливаем необходимое для сети
    wordLength = 59
    serverAddress = ("127.0.0.1", 55555)

    clientSocket = socket()
    clientSocket.connect(serverAddress)

    print("client is ready...")

    # подготавливаем текст
    message = textToBits(text, 'cp1251')
    # кодирование Хемминга
    extWordLeng = getControlBitsNum(wordLength) + wordLength
    message = hemingEncode(message,wordLength)
    extWordsN = len(message) // extWordLeng

    # сообщение 1
    message1 = message
    catMistakesSpread = [extWordsN,0,0]

    # отослать
    clientSocket.send(message1.encode('cp1251'))

    # получить ответ
    statistic = clientSocket.recvfrom(1024)[0].decode()
    statistic = statistic.split(':')
    # вывести результаты в сравнении
    print("слов с количеством ошибок:")
    print("добавлено:  с 0 = {0}, с 1 = {1}, с >1 = {2}".format(catMistakesSpread[0], catMistakesSpread[1],
                                                                catMistakesSpread[2]))
    print("распознано: с 0 = {0}, с 1 = {1}, с >1 = {2}".format(statistic[0], statistic[1], statistic[2]))

    # сообщение 2
    message2 = message
    cat1MistakesN = int(0.4 * extWordsN)
    cat0MistakesN = extWordsN - cat1MistakesN
    catMistakesSpread = [cat1MistakesN]

    # добавить ошибки
    message2 = ''.join(addMistakes(list(message2), extWordLeng, catMistakesSpread))

    # отослать
    clientSocket.send(message2.encode('cp1251'))

    # получить ответ
    catMistakesSpread = [extWordsN - cat1MistakesN - 0, cat1MistakesN, 0]
    statistic = clientSocket.recvfrom(1024)[0].decode()
    statistic = statistic.split(':')
    # вывести результаты в сравнении
    print("слов с количеством ошибок:")
    print("добавлено:  с 0 = {0}, с 1 = {1}, с >1 = {2}".format(catMistakesSpread[0],catMistakesSpread[1],catMistakesSpread[2]))
    print("распознано: с 0 = {0}, с 1 = {1}, с >1 = {2}".format(statistic[0],statistic[1],statistic[2]))

    # сообщение 3
    message3 = message
    cat1MistakesN = int(0.4 * extWordsN)
    cat2MistakesN = int(0.1 * extWordsN)
    cat3MistakesN = int(0.1 * extWordsN)
    cat4MistakesN = int(0.1 * extWordsN)
    catMore1MistakesN = cat2MistakesN + cat3MistakesN + cat4MistakesN
    cat0MistakesN = extWordsN - cat1MistakesN - catMore1MistakesN
    catMistakesSpread = [cat1MistakesN, cat2MistakesN, cat3MistakesN, cat4MistakesN]

    # добавить ошибки
    message3 = ''.join(addMistakes(list(message3), extWordLeng, catMistakesSpread))

    # отослать
    clientSocket.send(message3.encode('cp1251'))

    # получить ответ
    catMistakesSpread = [cat0MistakesN, cat1MistakesN, catMore1MistakesN]
    statistic = clientSocket.recvfrom(1024)[0].decode()
    statistic = statistic.split(':')
    # вывести результаты в сравнении
    print("слов с количеством ошибок:")
    print("добавлено:  с 0 = {0}, с 1 = {1}, с >1 = {2}".format(catMistakesSpread[0], catMistakesSpread[1],
                                                                catMistakesSpread[2]))
    print("распознано: с 0 = {0}, с 1 = {1}, с >1 = {2}".format(statistic[0], statistic[1], statistic[2]))

    clientSocket.close()

    return 0;

if __name__ == '__main__':
    main()
