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

class Application:

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

    def stopAndWaitCrc(self, signal):

        return 1

    def stopAndWait(self, signal):

        x = int(input("Wprowadz 0 dla kodowania z dodaniem bitu parzystosci lub 1 dla kodowania przy pomocy algorytmu CRC: "))
        print("\n-----------")

        if(x == 0):
            self.stopAndWaitParityBit(signal)

    def run(self):

        numberOfBits = int(input("Wprowadź wielkość sygnału w postaci liczby bitów: "))

        signal = Generator.generateSignal(numberOfBits)
        print("Sygnał: \n",signal, "\n")

        packetSize = int(input("Wprowadź wielkość jednego pakietu: "))

        signal = Coder.divideSignal(signal, packetSize)
        print("Podzielony sygnał: \n", signal, "\n")

        simulationType = int(input("Wprowadź 0 aby wykonać symulację stop and wait: "))

        if(simulationType == 0):

           self.stopAndWait(signal)


app = Application()
app.run()

    