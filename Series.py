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
        # print('newSeries')

        self.generation_num = None
        self.party_num = None


        self.population = Population(
            POPULATION_SIZE,
            NN_STRUCTURE,
        )


        self.newGeneration()


    #
    # принудительно завершить серию
    #
    def destroySeries(self):
        del self.population
        self.population = None

        self.Map_wnd.destroyMap()



    def newGeneration(self):
        self.generation_num = 0 if self.generation_num is None else (self.generation_num + 1)

        if self.generation_num:
            # для всех кроме нулевого
            self.population.calcNextGeneration()

        self.party_num = None
        self.newParty()


    def newParty(self):
        self.party_num = 0 if self.party_num is None else (self.party_num + 1)
        NN = self.population.getIndivid(self.party_num)

        arrangement_arr = {
            'Car': {
                'x': 100,
                'y': 300,
                'NN': NN,
            },
        }

        self.frames = 0
        self.Map_wnd.newParty(arrangement_arr)
        self.Tool_wnd.sendMessage('WM_SET_PARTY', {'party':self.party_num,'generation':self.generation_num,})



    #
    #
    #
    def endParty(self):

        self.Map_wnd.endParty()





    #
    #
    #
    def updateTraining(self):
        self.frames += 1
        self.Tool_wnd.sendMessage("WM_SET_TICKS", self.frames)

        self.Map_wnd.updateTraining()
        if self.isEndParty():

            # посчитаеть фитнесс, запищет в NN
            fit = self.Map_wnd.car.getFitness()
            print(fit)

            self.endParty()

            if self.party_num < POPULATION_SIZE-1:
                # переходим к следующей партии
                self.newParty()

            else:

                # генерейшен/поколение завершено
                if self.generation_num < GENE_MAX_COUNT-1:
                    self.newGeneration()

                else:
                    # серия завершена
                    self.parent_wnd.sendMessage('WM_END_SERIES', self.party_num)


    # проверка на конец парти, один из следующих случаев
    # 1. истекло 20 сек - пределная длинна партии
    # 2. прошло минимум 5 сек и минимальная скоромть меньше 5 пикселей/сек
    # 3. машина ударилась о край дороги
    def isEndParty(self):

        if (
                self.frames >= 1200 or \
                self.frames >= 300 and self.Map_wnd.car.getMediumSpeed() < 5 or\
                self.Map_wnd.testOffRoad()
        ):
            # партия завершена
            return True
        else:
            return False





    def updateShow(self):
        self.Map_wnd.updateShow()


    def draw(self):
        self.Map_wnd.draw()






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
