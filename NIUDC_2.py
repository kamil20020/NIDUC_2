import random
import math
import csv

def makeParityBit(packet):

    numberOfOnes = 0

    for i in packet:
        if(i == 1):
            numberOfOnes += 1

    if(numberOfOnes % 2 == 0):
        return 0
    else:
        return 1

def returnCrcRest(first, second):

    i = 0
    doEnd = False

    while doEnd == False:

        firstNumberOfLeftBits = len(first)-i

        if(firstNumberOfLeftBits < len(second)):
            break

        if(first[i] == 1):

            subI = 0
            inI = i
            while subI < len(second):

                first[inI] = first[inI]^second[subI]
                inI += 1
                subI += 1

                if(inI >= len(first)):
                    doEnd = True
                    break

        else:
            i += 1

            if(i >= len(first)):
                doEnd = True
                break

    rest = []
    
    for i in range(len(first)-(len(second)-1), len(first)):
        rest.append(first[i])

    return rest

class Generator:

    @staticmethod
    def generateSignal(howMuch):

        signal = []

        for i in range(howMuch):
            signal.append(random.randint(0,1))

        return signal

class Coder:

    @staticmethod
    def divideSignal(signal, inPackets):

        preparedSignal = []

        packetsNumber = math.ceil(len(signal)/inPackets)

        for i in range(packetsNumber):

            packet = []

            for j in range(inPackets):

                if(len(signal) -1 < inPackets*i+j):
                    packet.append(0)
                else:
                    packet.append(signal[inPackets*i+j])

            preparedSignal.append(packet)

        return preparedSignal

    @staticmethod
    def codePacketWithParity(packet):

        packet.append(makeParityBit(packet))

        return packet

    @staticmethod
    def encodeCrc(packet, n):

        x = [1,0,1,1]

        testPacket = packet.copy()

        for i in range(n):
            testPacket.append(0)
  
        rest = returnCrcRest(testPacket, x)

        for i in range(len(rest)):
            packet.append(rest[i])
  
        return packet

class Noise:

    @staticmethod
    def noisePacket(packet, changeChance):

        for i in range(len(packet)):

            rand = random.randint(0,100)

            if(rand > 100 - changeChance):

                if(packet[i] == 1):
                    packet[i] = 0
                else:
                    packet[i] = 1

        return packet

class Decoder:

    @staticmethod
    def decodeParityBit(packet):

        if(makeParityBit(packet) == 1):
            return False

        return True

    @staticmethod
    def decodeCrc(packet, n):

        x = [1,0,1,1]

        testPacket = packet.copy()
  
        rest = returnCrcRest(testPacket, x)

        checkingRest = []
        
        for i in range(n):
            checkingRest.append(0)

        if(checkingRest == rest):
            return True
  
        return False


class Application:

    def stopAndWaitCrc(self, signal, crcType):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)): 

            signal[i] = Coder.encodeCrc(signal[i], crcType)
            print("\nZakodowany (kodem nadmiarowym) pakiet numer ", i, ": ", signal[i], "\n")

            beforeNoisePackets.append(signal[i].copy())

        print("-----------\n")

        for i in range(len(signal)):

            crcMatch = False

            while crcMatch == False:

                signal[i] = Noise.noisePacket(list(beforeNoisePackets[i]), 10)

                if(howMuchRepeats[i] == 0):

                    print("Przesłany pakiet numer ", i, ": ", signal[i], "\n")

                else:
                    print("Powtórnie przesłany pakiet numer ", i, ": ", signal[i], "\n")

                if(Decoder.decodeCrc(signal[i], crcType) == False):

                    howMuchRepeats[i] += 1

                    print("Błędnie odebrany pakiet numer ", i, ": ", signal[i], "\n")

                else:

                    if(beforeNoisePackets[i] != signal[i]):
                        notDetectedErrors += 1

                    for j in range(crcType):
                        signal[i].pop(len(signal[i])-1)

                    receivedSignal.append(signal[i])

                    print("Pomyślnie odebrany pakiet numer ", i, ": ", signal[i], "\n")

                    crcMatch = True

            print("-----------\n")

        packetsWithMoreThanFourRepeats = 0

        for i in howMuchRepeats:

            if(i > 4):
                packetsWithMoreThanFourRepeats += 1

        print("Przesłano ", howMuchRepeats.count(0), " pakietów bezbłędnie")
        print("Przesłano ", howMuchRepeats.count(1), " pakietów, które wymagały jednego powtórzenia")
        print("Przesłano ", howMuchRepeats.count(2), " pakietów, które wymagały dwóch powtórzeń")
        print("Przesłano ", howMuchRepeats.count(3), " pakietów, które wymagały trzech powtórzeń")
        print("Przesłano ", howMuchRepeats.count(4), " pakietów, które wymagały czterech powtórzeń")
        print("Przesłano ", packetsWithMoreThanFourRepeats, " pakietów, które wymagały więcej niż cztery powtórzenia")
        print("Wystąpiło ", notDetectedErrors, " błędów niewykrytych")

        return receivedSignal

    def stopAndWaitCrcForTests(self, signal, crcType):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)): 

            signal[i] = Coder.encodeCrc(signal[i], crcType)

            beforeNoisePackets.append(signal[i].copy())

        for i in range(len(signal)):

            crcMatch = False

            while crcMatch == False:

                signal[i] = Noise.noisePacket(list(beforeNoisePackets[i]), 10)

                if(Decoder.decodeCrc(signal[i], crcType) == False):

                    howMuchRepeats[i] += 1

                else:

                    if(beforeNoisePackets[i] != signal[i]):
                        notDetectedErrors += 1

                    for j in range(crcType):
                        signal[i].pop(len(signal[i])-1)

                    receivedSignal.append(signal[i])

                    crcMatch = True

        packetsWithMoreThanTwoRepeats = 0

        for i in howMuchRepeats:

            if(i > 2):
                packetsWithMoreThanTwoRepeats += 1
           
        #pakiety wyslane bez bledow, wymagajace 1 powtorzenie, wymagajace 2, wiecej niz 2 powtorzenia, z niewykrytymi bledami
        return howMuchRepeats.count(0), howMuchRepeats.count(1), howMuchRepeats.count(2), packetsWithMoreThanTwoRepeats, notDetectedErrors

    def stopAndWaitParityBitForTests(self, signal):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)): 

            signal[i] = Coder.codePacketWithParity(signal[i]) 

            beforeNoisePackets.append(signal[i].copy())

        for i in range(len(signal)): 

            parityBitMatch = False

            while parityBitMatch == False:

                signal[i] = Noise.noisePacket(list(beforeNoisePackets[i]), 10)

                if(Decoder.decodeParityBit(signal[i]) == False):

                    howMuchRepeats[i] += 1

                else:

                    if(beforeNoisePackets[i] != signal[i]):
                        notDetectedErrors += 1

                    signal[i].pop(len(signal[i])-1)

                    receivedSignal.append(signal[i])

                    parityBitMatch = True

        packetsWithMoreThanTwoRepeats = 0

        for i in howMuchRepeats:

            if(i > 2):
                packetsWithMoreThanTwoRepeats += 1
           
        #pakiety wyslane bez bledow, wymagajace 1 powtorzenie, wymagajace 2, wiecej niz 2 powtorzenia, z niewykrytymi bledami
        return howMuchRepeats.count(0), howMuchRepeats.count(1), howMuchRepeats.count(2), packetsWithMoreThanTwoRepeats, notDetectedErrors

    def stopAndWaitParityBit(self, signal):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)): 

            signal[i] = Coder.codePacketWithParity(signal[i]) 
            print("\nZakodowany (bitem parzystosci) pakiet numer ", i, ": ", signal[i], "\n")

            beforeNoisePackets.append(signal[i].copy())

        for i in range(len(signal)): 

            parityBitMatch = False

            while parityBitMatch == False:

                signal[i] = Noise.noisePacket(list(beforeNoisePackets[i]), 10)

                if(howMuchRepeats[i] == 0):

                    print("Przesłany pakiet numer ", i, ": ", signal[i], "\n")

                else:
                    print("Powtórnie przesłany pakiet numer ", i, ": ", signal[i], "\n")

                if(Decoder.decodeParityBit(signal[i]) == False):

                    howMuchRepeats[i] += 1

                    print("Błędnie odebrany pakiet numer ", i, ": ", signal[i], "\n")

                else:

                    if(beforeNoisePackets[i] != signal[i]):
                        notDetectedErrors += 1

                    signal[i].pop(len(signal[i])-1)

                    receivedSignal.append(signal[i])

                    print("Pomyślnie odebrany pakiet numer ", i, ": ", signal[i], "\n")

                    parityBitMatch = True

            print("-----------\n")

        packetsWithMoreThanFourRepeats = 0

        for i in howMuchRepeats:

            if(i > 4):
                packetsWithMoreThanFourRepeats += 1

        print("Przesłano ", howMuchRepeats.count(0), " pakietów bezbłędnie")
        print("Przesłano ", howMuchRepeats.count(1), " pakietów, które wymagały jednego powtórzenia")
        print("Przesłano ", howMuchRepeats.count(2), " pakietów, które wymagały dwóch powtórzeń")
        print("Przesłano ", howMuchRepeats.count(3), " pakietów, które wymagały trzech powtórzeń")
        print("Przesłano ", howMuchRepeats.count(4), " pakietów, które wymagały czterech powtórzeń")
        print("Przesłano ", packetsWithMoreThanFourRepeats, " pakietów, które wymagały więcej niż cztery powtórzenia")
        print("Wystąpiło ", notDetectedErrors, " błędów niewykrytych")

        return signal

    def goBackNParityBitForTests(self, signal, frameSize):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)):

            signal[i] = Coder.codePacketWithParity(signal[i]) 

            beforeNoisePackets.append(signal[i].copy())

        index = 0

        while index < len(signal): 

            parityBitMatch = False
            end = False

            while parityBitMatch == False and end == False:

                jIndex = index

                whichSubFrame = 0

                while jIndex < index + len(beforeNoisePackets) and whichSubFrame < frameSize:

                    signal[jIndex] = Noise.noisePacket(list(beforeNoisePackets[jIndex]), 10)

                    if(Decoder.decodeParityBit(signal[jIndex]) == False):

                        howMuchRepeats[jIndex] += 1

                        end = True
                        break

                    else:

                        if(beforeNoisePackets[jIndex] != signal[jIndex]):
                            notDetectedErrors += 1

                        signal[jIndex].pop(len(signal[jIndex])-1)

                        receivedSignal.append(signal[jIndex])

                        index += 1
                        jIndex += 1

                        whichSubFrame += 1

                        if(index == len(signal)):
                           end = True
                           break

                        parityBitMatch = True

        packetsWithMoreThanTwoRepeats = 0

        for i in howMuchRepeats:

            if(i > 2):
                packetsWithMoreThanTwoRepeats += 1
           
        #pakiety wyslane bez bledow, wymagajace 1 powtorzenie, wymagajace 2, wiecej niz 2 powtorzenia, z niewykrytymi bledami
        return howMuchRepeats.count(0), howMuchRepeats.count(1), howMuchRepeats.count(2), packetsWithMoreThanTwoRepeats, notDetectedErrors

    def goBackNParityBit(self, signal, frameSize):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)):

            signal[i] = Coder.codePacketWithParity(signal[i]) 
            print("\nZakodowany (bitem parzystosci) pakiet numer ", i, ": ", signal[i], "\n")

            beforeNoisePackets.append(signal[i].copy())

        print("-----------\n")

        index = 0

        while index < len(signal): 

            parityBitMatch = False
            end = False

            while parityBitMatch == False and end == False:

                jIndex = index

                whichSubFrame = 0

                while jIndex < index + len(beforeNoisePackets) and whichSubFrame < frameSize:

                    signal[jIndex] = Noise.noisePacket(list(beforeNoisePackets[jIndex]), 10)

                    if(howMuchRepeats[jIndex] == 0):

                        print("Przesłany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                    else:
                        print("Powtórnie przesłany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                    if(Decoder.decodeParityBit(signal[jIndex]) == False):

                        howMuchRepeats[jIndex] += 1

                        print("Błędnie odebrany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                        end = True
                        break

                    else:

                        if(beforeNoisePackets[jIndex] != signal[jIndex]):
                            notDetectedErrors += 1

                        signal[jIndex].pop(len(signal[jIndex])-1)

                        receivedSignal.append(signal[jIndex])

                        print("Pomyślnie odebrany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                        index += 1
                        jIndex += 1

                        whichSubFrame += 1

                        if(index == len(signal)):
                           end = True
                           break

                        parityBitMatch = True

            print("-----------\n")

        packetsWithMoreThanFourRepeats = 0

        for i in howMuchRepeats:

            if(i > 4):
                packetsWithMoreThanFourRepeats += 1

        print("Przesłano ", howMuchRepeats.count(0), " pakietów bezbłędnie")
        print("Przesłano ", howMuchRepeats.count(1), " pakietów, które wymagały jednego powtórzenia")
        print("Przesłano ", howMuchRepeats.count(2), " pakietów, które wymagały dwóch powtórzeń")
        print("Przesłano ", howMuchRepeats.count(3), " pakietów, które wymagały trzech powtórzeń")
        print("Przesłano ", howMuchRepeats.count(4), " pakietów, które wymagały czterech powtórzeń")
        print("Przesłano ", packetsWithMoreThanFourRepeats, " pakietów, które wymagały więcej niż cztery powtórzenia")
        print("Wystąpiło ", notDetectedErrors, " błędów niewykrytych")

        return receivedSignal

    def goBackNCrcForTests(self, signal, frameSize, crcType):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)):

            signal[i] = Coder.encodeCrc(signal[i], crcType)

            beforeNoisePackets.append(signal[i].copy())

        print("-----------\n")

        index = 0

        while index < len(signal): 

            crcMatch = False
            end = False

            while crcMatch == False and end == False:

                jIndex = index

                whichSubFrame = 0

                while jIndex < index + len(beforeNoisePackets) and whichSubFrame < frameSize:

                    signal[jIndex] = Noise.noisePacket(list(beforeNoisePackets[jIndex]), 10)

                    if(Decoder.decodeCrc(signal[jIndex], crcType) == False):

                        howMuchRepeats[jIndex] += 1

                        end = True
                        break

                    else:

                        if(beforeNoisePackets[jIndex] != signal[jIndex]):
                            notDetectedErrors += 1

                        for i in range(crcType):
                            signal[jIndex].pop(len(signal[jIndex])-1)

                        receivedSignal.append(signal[jIndex])

                        index += 1
                        jIndex += 1

                        whichSubFrame += 1

                        if(index == len(signal)):
                           end = True
                           break

                        crcMatch = True

        packetsWithMoreThanTwoRepeats = 0

        for i in howMuchRepeats:

            if(i > 2):
                packetsWithMoreThanTwoRepeats += 1
           
        #pakiety wyslane bez bledow, wymagajace 1 powtorzenie, wymagajace 2, wiecej niz 2 powtorzenia, z niewykrytymi bledami
        return howMuchRepeats.count(0), howMuchRepeats.count(1), howMuchRepeats.count(2), packetsWithMoreThanTwoRepeats, notDetectedErrors


    def goBackNCrc(self, signal, frameSize, crcType):

        receivedSignal = []

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        beforeNoisePackets = []

        for i in range(len(signal)):

            signal[i] = Coder.encodeCrc(signal[i], crcType)
            print("\nZakodowany (kodem nadmiarowym) pakiet numer ", i, ": ", signal[i], "\n")

            beforeNoisePackets.append(signal[i].copy())

        print("-----------\n")

        index = 0

        while index < len(signal): 

            crcMatch = False
            end = False

            while crcMatch == False and end == False:

                jIndex = index

                whichSubFrame = 0

                while jIndex < index + len(beforeNoisePackets) and whichSubFrame < frameSize:

                    signal[jIndex] = Noise.noisePacket(list(beforeNoisePackets[jIndex]), 10)

                    if(howMuchRepeats[jIndex] == 0):

                        print("Przesłany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                    else:
                        print("Powtórnie przesłany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                    if(Decoder.decodeCrc(signal[jIndex], crcType) == False):

                        howMuchRepeats[jIndex] += 1

                        print("Błędnie odebrany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                        end = True
                        break

                    else:

                        if(beforeNoisePackets[jIndex] != signal[jIndex]):
                            notDetectedErrors += 1

                        for i in range(crcType):
                            signal[jIndex].pop(len(signal[jIndex])-1)

                        receivedSignal.append(signal[jIndex])

                        print("Pomyślnie odebrany pakiet numer ", jIndex, ": ", signal[jIndex], "\n")

                        index += 1
                        jIndex += 1

                        whichSubFrame += 1

                        if(index == len(signal)):
                           end = True
                           break

                        crcMatch = True

            print("-----------\n")

        packetsWithMoreThanFourRepeats = 0

        for i in howMuchRepeats:

            if(i > 4):
                packetsWithMoreThanFourRepeats += 1

        print("Przesłano ", howMuchRepeats.count(0), " pakietów bezbłędnie")
        print("Przesłano ", howMuchRepeats.count(1), " pakietów, które wymagały jednego powtórzenia")
        print("Przesłano ", howMuchRepeats.count(2), " pakietów, które wymagały dwóch powtórzeń")
        print("Przesłano ", howMuchRepeats.count(3), " pakietów, które wymagały trzech powtórzeń")
        print("Przesłano ", howMuchRepeats.count(4), " pakietów, które wymagały czterech powtórzeń")
        print("Przesłano ", packetsWithMoreThanFourRepeats, " pakietów, które wymagały więcej niż cztery powtórzenia")
        print("Wystąpiło ", notDetectedErrors, " błędów niewykrytych")

        return receivedSignal

    def run(self):

        numberOfBits = int(input("Wprowadź wielkość sygnału w postaci liczby bitów (-1 kończy program): "))
        if(numberOfBits == -1):
            return 0
           
        signal = Generator.generateSignal(numberOfBits)
        print("Sygnał: \n",signal, "\n")

        packetSize = int(input("Wprowadź wielkość jednego pakietu: "))

        signal = Coder.divideSignal(signal, packetSize)
        print("Podzielony sygnał: \n", signal, "\n")

        print("Menu: \n 0 - kodowanie bitem parzystosci \n 1 - kodowanie kodem nadmiarowym \n")

        codingType = int(input("Wprowadz odpowiedni znak: "))
        print("\n-----------\n")

        #if(codingType == 1):
        #    crcType = int(input("Wprowadz typ crc (rozmiar wielomianu generujacego - 1): "))

        print("\nMenu: \n 0 - sumulacja stop and wait\n 1 - symulacja go back n \n")
        simulationType = int(input("Wprowadz odpowiedni znak: "))

        if(simulationType == 0):
            
            if(codingType == 0):
                self.stopAndWaitParityBit(signal)

            elif(codingType == 1):
                self.stopAndWaitCrc(signal, 3)

        elif(simulationType == 1):
            
            if(codingType == 0):
                self.goBackNParityBit(signal, 3)

            elif(codingType == 1):
                self.goBackNCrc(signal, 3, 3)

        
        if(simulationType != -1):
            print("\n")
            self.run()

    def tests(self):

        file = open("tests.csv", "w", newline='')

        for i in range(1000):

            signal = Generator.generateSignal(200)

            signal = Coder.divideSignal(signal, 10)

            csvWriter = csv.writer(file)

            #pakiety wyslane bez bledow, wymagajace 1 powtorzenie, wymagajace 2, wiecej niz 2 powtorzenia, z niewykrytymi bledami
            csvWriter.writerow(self.stopAndWaitParityBitForTests(signal))

        file.close()


app = Application()
#app.run()
app.tests()



    