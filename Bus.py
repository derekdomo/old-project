import Request
import Stop
import random
import wx
__author__ = 'Derek.Sun'
class Bus:
    def __init__(self,console,name,now,AllStop):
        self.console=console
        self.name=name
        self.schedule=[]
        self.NowStop=now
        self.Direction=0
        self.AllStop=AllStop
        self.request=[]
    '''
    System assign the requests to each bus
    '''
    def getRequest(self,request):
        self.request=self.request+request

    '''
       Stop at this stop to check whether
       1)someone want to get on
       2)someone want to get down
    '''
    def collect(self):
        if len(self.schedule)!=0:
            if self.NowStop is self.schedule[0]:
                self.schedule.pop(0)
        removeList=[]
        for it in self.NowStop.requestList:
        #for the stop's all request to collect all the requests have been assigned to this BUS
            if it in self.request:
                #add this request to the schedule and delete this request from the requestList
                removeList.append(it)
                self.addRequest(it)
                self.console.AppendText("\nBus "+str(self.name)+" Pick up Request: Stop "+str(self.AllStop.index(it.Start))+" to Stop "+str(self.AllStop.index(it.Destination))+"\n")
                self.request.remove(it)
        for i in removeList:
            self.NowStop.requestList.remove(i)
        '''
        print str(self.name)+" Stop"
        for i in self.schedule:
            print i.name
        '''
    '''
    Add the request to the schedule
    '''
    def addRequest(self,request):
        #The schedule is EMPTY
        if len(self.schedule) is 0:
            if self.NowStop.y>request.Destination.y:
                self.Direction=-1
            else:
                self.Direction=1
            self.schedule.append(request.Destination)
        #The schedule is not EMPTY
        else:
            #if the request is between now stop and next stop
            if self.NowStop.y>request.Destination.y and request.Destination.y>self.schedule[0].y or self.NowStop.y<request.Destination.y and request.Destination.y<self.schedule[0].y:
                self.schedule.insert(0,request.Destination)
            else:
            #Three conditions to insert:
            #As the schedule of a bus has Straightly one Direction
                #0 stands for not
                insertFlag=0
                for i in range(len(self.schedule)-1):
                    #1.schedule[i]>request.Destination>schedule[i+1]
                    if self.schedule[i].y>request.Destination.y and request.Destination.y>self.schedule[i+1].y:
                        self.schedule.insert(i+1,request.Destination)
                        insertFlag=1
                        break
                    #2.schedule[i]<request.Destination<schedule[i+1]
                    elif self.schedule[i].y<request.Destination.y and request.Destination.y<self.schedule[i+1].y:
                        self.schedule.insert(i+1,request.Destination)
                        insertFlag=1
                        break
                #3.The end of the schedule
                if insertFlag==0:
                    self.schedule.append(request.Destination)
    def move(self):
        if len(self.request)==0 and len(self.schedule)==0:
            self.Direction=0
            return
        elif len(self.schedule)==0:
            if self.name==1:
                print "--------"
                print self.request[0].Start.name
            self.schedule.append(self.request[0].Start)
        temp=self.schedule[0]
        if temp.y>self.NowStop.y:#Down
            self.NowStop=self.AllStop[self.AllStop.index(self.NowStop)+1]
            self.Direction=1
        else:
            self.NowStop=self.AllStop[self.AllStop.index(self.NowStop)-1]
            self.Direction=-1

