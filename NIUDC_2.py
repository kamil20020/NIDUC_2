import random
import math

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

    def stopAndWaitCrc(self, signal, n):

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        for i in range(len(signal)): 

            beforeNoisePacket = []

            beforeNoisePacket = signal[i].copy()

            signal[i] = Coder.encodeCrc(signal[i], n)
            print("\nZakodowany (kodem nadmiarowym) pakiet numer ", i, ": ", signal[i], "\n")

            crcMatch = False

            while crcMatch == False:

                signal[i] = Noise.noisePacket(signal[i], 10)

                if(howMuchRepeats[i] == 0):

                    print("Przesłany pakiet numer ", i, ": ", signal[i], "\n")

                else:
                    print("Powtórnie przesłany pakiet numer ", i, ": ", signal[i], "\n")

                if(Decoder.decodeCrc(signal[i], n) == False):

                    howMuchRepeats[i] += 1

                else:

                    for i in range(n):
                        signal[i].pop(len(signal[i])-1)

                    if(beforeNoisePacket != signal[i]):
                        notDetectedErrors += 1

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

        return signal

    def stopAndWaitParityBit(self, signal):

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        for i in range(len(signal)): 

            beforeNoisePacket = []

            beforeNoisePacket = signal[i].copy()

            signal[i] = Coder.codePacketWithParity(signal[i]) 
            print("\nZakodowany (bitem parzystosci) pakiet numer ", i, ": ", signal[i], "\n")

            parityBitMatch = False

            while parityBitMatch == False:

                signal[i] = Noise.noisePacket(signal[i], 10)

                if(howMuchRepeats[i] == 0):

                    print("Przesłany pakiet numer ", i, ": ", signal[i], "\n")

                else:
                    print("Powtórnie przesłany pakiet numer ", i, ": ", signal[i], "\n")

                if(Decoder.decodeParityBit(signal[i]) == False):

                    howMuchRepeats[i] += 1

                else:

                    signal[i].pop(len(signal[i])-1)

                    if(beforeNoisePacket != signal[i]):
                        notDetectedErrors += 1

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

    def run(self):

        numberOfBits = int(input("Wprowadź wielkość sygnału w postaci liczby bitów: "))

        signal = Generator.generateSignal(numberOfBits)
        print("Sygnał: \n",signal, "\n")

        packetSize = int(input("Wprowadź wielkość jednego pakietu: "))

        signal = Coder.divideSignal(signal, packetSize)
        print("Podzielony sygnał: \n", signal, "\n")

        print("Menu: \n 0 - kodowanie bitem parzystosci \n 1 - kodowanie kodem nadmiarowym \n")

        codingType = int(input("Wprowadz odpowiedni znak: "))
        print("\n-----------\n")

        print("\nMenu: \n 0 - sumulacja stop and wait\n")
        simulationType = int(input("Wprowadz odpowiedni znak: "))

        if(simulationType == 0):
            
            if(codingType == 0):
                self.stopAndWaitParityBit(signal)

            elif(codingType == 1):
                self.stopAndWaitCrc(signal, 3)

        elif(simulationType == 1):
            print("Not implemented")

        
        if(simulationType != -1):
            print("\n")
            self.run()


app = Application()
app.run()



    