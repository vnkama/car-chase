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
        self.party_num = 1

        arrangement_arr = {
            'Car': {
                'x': 0,
                'y': 300,
            },
        }

        self.Map_wnd.reset(arrangement_arr)



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


    def updateTraining(self):

        self.Map_wnd.updateTraining()

    def updateShow(self):
        self.Map_wnd.updateShow()

    def draw(self):
        self.Map_wnd.draw()

