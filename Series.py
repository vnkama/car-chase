from config import *
from fw.functions import *
# from fw.FwError import FwError

from Party import Party


class Series:

    def __init__(self):
        self.generation_num = None
        self.party_num = None
        self.party = Party()


    def newTrainig(self):
        self.generation_num = 1
        self.party_num = 1

        self.party.newTrainig()


    def playShow(self):
        pass

    def playTraining(self):
        pass

    def pauseShow(self):
        pass

    def pauseTraining(self):
        pass

    def setShowMode(self):
        pass

    def setTrainingMode(self):
        pass


    #
    #
    #   return True если сообщение обработано
    #   False если сообщение не обработано
    #
    def sendMessage(self, msg, param1=None, param2=None):
        pass

        # if msg == 'WM_DRAW':
        #     self.draw()
        #
        # elif msg == 'WM_UPDATE':
        #     self.update()

