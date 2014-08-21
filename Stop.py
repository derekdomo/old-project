__author__ = 'Derek.Sun'
'''
requestList:  A List of request
'''
class Stop:
    def __init__(self,y,name):
        self.requestList=[]
        self.y=y
        self.name=name
    '''
    load the request to the bus
    '''
    def loadtoBus(self,request):
        if request in self.requestList:
            self.requestList.remove(request)
            return True
        else:
            return False

    '''
    load new requests to the stop
    '''
    def loadnew(self,requests):
        self.requestList=self.requestList+requests
