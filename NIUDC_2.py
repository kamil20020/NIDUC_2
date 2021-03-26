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


class Application:

    def stopAndWait(self, signal):

        parityBitMatch = False

        howMuchRepeats = []

        notDetectedErrors = 0

        for i in range(len(signal)):
            howMuchRepeats.append(0)

        x = int(input("Wprowadz 0 dla kodowania z dodaniem bitu parzystosci lub 1 dla kodowania przy pomocy algorytmu CRC: "))

        for i in range(len(signal)): 

            if(x == 0):

                signal[i] = Coder.codePacketWithParity(self.signal[i]) 
                print("\nZakodowany (bit parzystosci) pakiet numer ", i, ": ", signal[i], "\n")

                previousPacket = []

                previousPacket = signal.copy()

            while parityBitMatch == False:

                signal[i] = Noise.noisePacket(self.signal[i], 10)

                if(howMuchRepeats[i] == 0):

                    print("Przesłany pakiet numer ", i, ": ", signal[i], "\n")

                else:
                    print("Powtórnie przesłany pakiet numer ", i, ": ", signal[i], "\n")

                if(makeParityBit(signal[i]) == 1):

                    howMuchRepeats[i] += 1

                else:

                    if(previousPacket != signal[i]):
                        notDetectedErrors += 1

                    parityBitMatch = True

            parityBitMatch = False

            signal[i].pop(len(signal[i])-1)

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

        self.signal = Generator.generateSignal(100)
        print("Sygnał: \n", self.signal, "\n")

        self.signal = Coder.divideSignal(self.signal, 8)
        print("Podzielony sygnał: \n", self.signal, "\n")

        x = int(input("Wprowadź 0 aby wykonać symulację stopAndWhite: "))

        if(x == 0):
            self.stopAndWait(self.signal)


app = Application()
app.run()

    