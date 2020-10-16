from config import *

#
#
#
class FwError(Exception):

    def __init__(self,param=None):
        self.param = param if (param is not None) else None
        super().__init__()


    def out(self):
        if (self.param is not None):
            print(CONSOLE_CLR_ERROR +  f"FwError.out() message:")
            print(f"{self.param}")
        else:
            print(CONSOLE_CLR_ERROR +  f"FwError.out() NO message.")






