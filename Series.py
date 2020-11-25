from config import *
from fw.functions import *
# from fw.FwError import FwError

from fw.fwWindow import fwWindow
from MapWnd import MapWnd


class Series(fwWindow):

    def __init__(self, params):
        super().__init__(params)        # parent - fwMapWnd

        self.generation_num = None
        self.party_num = None



        self.Tool_wnd = params['Tool_wnd']

        self.Map_wnd = MapWnd({
            'type': 'normal',
            'parent_wnd': self,
            'parent_surface': self.parent_surface,
            'Tool_wnd': self.Tool_wnd,
        })
        # self.addChildWnd(self.Map_wnd)


    def newSeries(self):
        print('newSeries')
        self.generation_num = 1

        self.party_num = None

        self.newParty()




    def newParty(self):
        self.party_num = (self.party_num or 0) + 1

        arrangement_arr = {
            'Car': {
                'x': 100,
                'y': 300,
            },
        }

        self.Map_wnd.reset(arrangement_arr)
        self.Tool_wnd.sendMessage('WM_SET_PARTY', self.party_num)



    def updateTraining(self):
        self.Map_wnd.updateTraining()


    def updateShow(self):
        self.Map_wnd.updateShow()


    def draw(self):
        self.Map_wnd.draw()

        if self.Map_wnd.testOffRoad() or 0:
            #съехали с дороги
            # конец Party
            self.endParty()

    #
    #
    #
    def endParty(self):
        if self.party_num < PARTY_COUNT_IN_GENE:
            # переходим к следующей партии
            self.newParty()


        else:
            # поколение завершено
            self.parent_wnd.sendMessage('WM_END_SERIES', self.party_num)


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
