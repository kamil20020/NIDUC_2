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
    def noiseSignal(signal):
        print("Noise")


class Application:

    def run(self):
        self.signal = Generator.generateSignal(10)
        print(self.signal)
        self.signal = Coder.divideSignal(self.signal, 3)
        print(self.signal)
        self.signal = Coder.codeSignal(self.signal)
        print(self.signal)
        

app = Application()
app.run()
    