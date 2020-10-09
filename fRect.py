#import math
from fw.functions import *
from fw.FwError import FwError

class fRect():

    def __init__(self,*args):

        args_count = len(args)

        if (args_count == 1):
            raise FwError()

        elif (len == 2):
            raise FwError()

        elif (len == 4):
            for v in args:
                if (not (isinstance(v,int) or isinstance(v,float))):
                    raise FwError()

            self.left = float(args[0])
            self.top  = float(args[1])
            self.width = float(args[2])
            self.height  = float(args[3])

        else:
            raise FwError()





