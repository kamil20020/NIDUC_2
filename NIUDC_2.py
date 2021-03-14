import random
import math

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
    def makeParityBit(packet):

        numberOfOnes = 0

        for i in packet:
            if(i == 1):
                numberOfOnes += 1

        if(numberOfOnes % 2 == 0):
            return 0
        else:
            return 1

    @staticmethod
    def codeSignal(signal):

        for i in range(len(signal)):
            signal[i].append(Coder.makeParityBit(signal[i]))

        return signal

class Noise:

    @staticmethod
    def noiseSignal(signal, changeChance):

        preparedSignal = []

        for i in signal:

            packet = []

            for j in i:

                rand = random.randint(0,100)

                if(rand >= 100 - changeChance):

                    if(j == 1):
                        j = 0
                    else:
                        j = 1

                packet.append(j)

            preparedSignal.append(packet)

        return preparedSignal

class Application:

    def run(self):
        self.signal = Generator.generateSignal(20)
        print(self.signal)

        self.signal = Coder.divideSignal(self.signal, 3)
        print(self.signal)

        self.signal = Coder.codeSignal(self.signal)
        print(self.signal)

        self.signal = Noise.noiseSignal(self.signal, 10)
        print(self.signal)


app = Application()
app.run()
    