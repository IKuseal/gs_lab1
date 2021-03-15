from socket import *
from general import *

import math

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'



def hemingDecode(data, wordLength):
    controlBitN = getControlBitsNum(wordLength)
    pos = [2 ** i for i in range(0, controlBitN)]
    extWordLength = wordLength + controlBitN

    word = ""
    matrix = generateHemingMatrix(wordLength)
    simptomStr = ''
    catMistakesN = [0,0,0]

    dataList = list(data)

    for i in range(0, len(data)//(extWordLength)):
        word = data[i*extWordLength:(i+1)*extWordLength]
        wordStr = ''.join(word)

        # получаем вектор симптомов
        simptomStr = ""
        for j in range(0, controlBitN):
            simptomStr = str(mult2BitStringsMod2(wordStr, matrix[j])) + simptomStr

        # определяем позицию и тип ошибки
        mistIndex = int(simptomStr, 2)

        if(mistIndex == 0):
            continue
        elif(mistIndex <= extWordLength):
            catMistakesN[1] += 1

            # исправляем ошибку
            el = data[i*extWordLength + mistIndex-1]
            if (el == '0'):
                dataList[i * extWordLength + mistIndex - 1] = '1'
            else:
                dataList[i * extWordLength + mistIndex - 1] = '0'
        else:
            catMistakesN[2] += 1

    catMistakesN[0] = len(data)// extWordLength - catMistakesN[1] - catMistakesN[2]
    data = ''.join(dataList)

    decodedData = ""
    decodedWord = ""
    for i in range(0,len(data)//(extWordLength)):
        word = data[i*extWordLength:(i+1)*extWordLength]
        decodedWord = ""
        for j in range(0,len(pos) - 1):
            decodedWord += word[pos[j]:pos[j+1]-1]
        decodedWord+= word[pos[-1]:]
        decodedData += decodedWord

    return (decodedData, catMistakesN)


def main():
    wordLength = 59
    # подготавливаем необходимое для сети
    serverAddress = ("127.0.0.1", 55555)
    serverSocket = socket()
    serverSocket.bind(serverAddress)
    serverSocket.listen()
    print("server is ready...")

    clientSocket, clientAddress = serverSocket.accept()

    catMistakesN = []

    # сообщение 1
    # получить сообщение
    message = clientSocket.recvfrom(30000)[0]
    # декодирование Хемминга
    message, catMistakesN = hemingDecode(message.decode('cp1251'), wordLength)

    message = text_from_bits(message, 'cp1251')
    # вывод сообщения
    print(message)
    # отправить статистику
    statistic = ':'.join(map(lambda x: str(x), catMistakesN))
    clientSocket.send(statistic.encode())

    # сообщение 2
    # получить сообщение
    message = clientSocket.recvfrom(30000)[0]
    # декодирование Хемминга
    message, catMistakesN = hemingDecode(message.decode('cp1251'), wordLength)

    message = text_from_bits(message,'cp1251')
    # вывод сообщения
    print()
    print()
    print()
    print(message)
    # отправить статистику
    statistic = ':'.join(map(lambda x: str(x), catMistakesN))
    clientSocket.send(statistic.encode())

    # сообщение 3
    # получить сообщение
    message = clientSocket.recvfrom(30000)[0]
    # декодирование Хемминга
    message, catMistakesN = hemingDecode(message.decode('cp1251'), wordLength)

    message = text_from_bits(message, 'cp1251')
    # вывод сообщения
    print()
    print()
    print()
    print(message)
    # отправить статистику
    statistic = ':'.join(map(lambda x: str(x), catMistakesN))
    clientSocket.send(statistic.encode())


    serverSocket.close()

    return 0;

if __name__ == '__main__':
    main()
