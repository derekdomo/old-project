__author__ = 'Derek.Sun'
import Request
import kmeans

class Monitor:
    def __init__(self,AllStop,AllBus):
        self.AllStop=AllStop
        self.AllBus=AllBus
        self.ProduceRequest()
    #Assign new Requests(-1) to the Bus and Set the Flag of Assigned 1
    def work(self):
        requestMatrix=[]
        for it in self.AllStop:
            for i in it.requestList:
                if i.Assigned==-1:
                    requestMatrix.append(i)
        #self.Cal(requestMatrix)
        if len(requestMatrix)==0:
            return
        else:
            for i in self.AllStop:
                for j in i.requestList:
                    j.Assigned=1
            self.AllBus[0].request.append(self.AllStop[0].requestList[0]);
            self.AllBus[0].request.append(self.AllStop[0].requestList[1]);
            self.AllBus[1].request.append(self.AllStop[3].requestList[0]);
            self.AllBus[1].request.append(self.AllStop[1].requestList[1]);
            self.AllBus[1].request.append(self.AllStop[4].requestList[1]);
            self.AllBus[2].request.append(self.AllStop[1].requestList[0]);
            self.AllBus[2].request.append(self.AllStop[2].requestList[1]);
            self.AllBus[2].request.append(self.AllStop[2].requestList[0]);
            self.AllBus[3].request.append(self.AllStop[4].requestList[0]);
            self.AllBus[3].request.append(self.AllStop[5].requestList[0]);
    #Produce the Requests on each Stop
    def ProduceRequest(self):
        self.AllStop[0].requestList.append(Request.Request(self.AllStop[0],self.AllStop[4],1));
        self.AllStop[1].requestList.append(Request.Request(self.AllStop[1],self.AllStop[2],1));
        self.AllStop[2].requestList.append(Request.Request(self.AllStop[2],self.AllStop[0],-1));
        self.AllStop[3].requestList.append(Request.Request(self.AllStop[3],self.AllStop[5],1));
        self.AllStop[4].requestList.append(Request.Request(self.AllStop[4],self.AllStop[2],-1));
        self.AllStop[5].requestList.append(Request.Request(self.AllStop[5],self.AllStop[4],-1));
        self.AllStop[2].requestList.append(Request.Request(self.AllStop[2],self.AllStop[3],1));
        self.AllStop[1].requestList.append(Request.Request(self.AllStop[1],self.AllStop[4],1));
        self.AllStop[0].requestList.append(Request.Request(self.AllStop[0],self.AllStop[2],1));
        self.AllStop[4].requestList.append(Request.Request(self.AllStop[4],self.AllStop[0],-1));
    def Cal(self,requestList):
        #Generating the Matrix
        #Maybe we can add these bused into the matrix
        #So this problem can be treated as a traveller problem
        #In this way the graph has len(requestList)+len(AllBus) nodes.

        Starter=[]
        for i in self.AllBus:
            Start=i.NowStop
            if len(i.schedule)==0:
                End=i.NowStop
            else:
                End=i.schedule[-1]
            if Start.y>End.y:
                Dir=-1
            else:
                Dir=1
            Starter.append(Request.Request(Start,End,Dir))

        #SO Now this is a problem of graph traversing
        #The thought I have now is to iterate all the nodes, first add similar nodes together.
            #What are similar nodes: The path is included
        #Second is to find the biggest nodes

        #Overall we need to find the least cost belonging for a node

        #1.Include the Node:
        for i in requestList:
            for j in range(len(Starter)):
                if i.Direction==1 and Starter[j].Direction==1 and Starter[j].Start.y<=i.Start.y and Starter[j].Destination.y>=i.Destination.y or i.Direction==-1 and Starter[j].Direction==-1 and Starter[j].Start.y>=i.Start.y and Starter[j].Destination.y<=i.Destination.y:
                    requestList.remove(i)
                    i.Assigned=1
                    self.AllBus[j].request.append(i)
                    break

        StartMatrix=[[0]*len(Starter) for i in range(len(requestList))]
        for i in range(len(Starter)):
            for j in range(len(requestList)):
                StartMatrix[j][i]=requestList[j].Destination.y-Starter[i].Destination.y
        #2.total Multi Traveller
        #for bus in self.AllBus:
    def brachandbound(self):
        return
    def kmeans(self):
        return

