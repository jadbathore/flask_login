class Error(BaseException) :
    def __init__(self,message):
        BaseException.__init__(self)
        self.message = message
    
    def __get__(self):
        return self.message