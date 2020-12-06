from config import *
from fw.functions import *
# from fw.FwError import FwError
import numpy as np

from fw.fwWindow import fwWindow
from MapWnd import MapWnd
from Car import *
from fw.Population import *




class Series(fwWindow):

    def __init__(self, params):
        super().__init__(params)        # parent - fwMapWnd

        self.generation_num = None
        self.party_num = None
        self.car = None

        self.population = None

        # номер шага обучения (1-based)
        # когда трайнинг не идет переменная тоже стоит
        self.frames = None


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

        np.random.RandomState(3000)

        self.population = Population(POPULATION_SIZE, NN_STRUCTURE)

        self.newParty()



    def newGeneration(self):
        self.generation_num += 1
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

        self.frames = 0
        self.Map_wnd.reset(arrangement_arr)
        self.Tool_wnd.sendMessage('WM_SET_PARTY', self.party_num)

        self.car = self.Map_wnd.arr_cars[0]     # для ускорения обращения к авто



    def updateTraining(self):
        self.frames += 1
        self.Tool_wnd.sendMessage("WM_SET_TICKS", self.frames)

        self.Map_wnd.updateTraining()

        # проверка на конец парти, один из следующих случаев
        # 1. истекло 20 сек - пределная длинна партии
        # 2. прошло минимум 5 сек и минимальная скоромть меньше 5 пикселей/сек
        # 3. машина ударилась о край дороги


        if (
                self.frames >= 1200 or \
                self.frames >= 300 and self.car.getMediumSpeed() < 5 or\
                self.Map_wnd.testOffRoad()
        ):
            # парти завершена
            print(self.car.getFitness())
            self.endParty()



    def updateShow(self):
        self.Map_wnd.updateShow()


    def draw(self):
        self.Map_wnd.draw()

        # if self.Map_wnd.testOffRoad() or 0:
        #     #съехали с дороги
        #     # конец Party
        #     self.endParty()

    #
    #
    #
    def endParty(self):
        if self.party_num < POPULATION_SIZE:
            # переходим к следующей партии
            self.newParty()

        else:
            # генерейшен/поколение завершено
            if self.generation_num < GENE_MAX_COUNT:
                self.newGeneration()

            else:
                # серия завершена
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
