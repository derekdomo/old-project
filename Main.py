import wx
import pygame
import Stop
import Request
import Bus
import random
import time
import Monitor
from pygame.locals import *
from sys import exit
__author__ = 'Derek.Sun'
'''
Function: MainFrame
'''
class Frame(wx.Frame):
    def __init__(self,icon,parent=None,id=-1,pos=wx.DefaultPosition,title="BusSchedule"):
        size=(1000,1000)
        wx.Frame.__init__(self,parent,id,title,pos,size)
        self.panel=wx.Panel(self)
        self.panel.SetBackgroundColour('White')
        self.console=wx.TextCtrl(self.panel,-1,"Welcome!",size=(400,910),style=wx.TE_AUTO_SCROLL|wx.TE_MULTILINE)
        self.condition=wx.TextCtrl(self.panel,-1,"Request At Each Stop!\n",size=(600,910),pos=(400,-1),style=wx.TE_AUTO_SCROLL|wx.TE_MULTILINE)

        #ToolBar Init
        toolBar=self.CreateToolBar()
        init=wx.Image('init.png',wx.BITMAP_TYPE_PNG)
        init.Rescale(20,20)
        start=wx.Image('start.png',wx.BITMAP_TYPE_PNG)
        start.Rescale(20,20)
        InitID=wx.NewId()
        StartID=wx.NewId()
        InitTool=toolBar.AddSimpleTool(InitID,init.ConvertToBitmap(),"Init","Long help for 'Init'")
        self.StopNum=6
        self.BusNum=4
        StartTool=toolBar.AddSimpleTool(StartID,start.ConvertToBitmap(),'Start',"Long help for 'Start'")
        toolBar.Realize()
        wx.EVT_TOOL(self,InitID,self.InitDataDialog)
        wx.EVT_TOOL(self,StartID,self.OnClickForStart)

        #MenuBar Init
        menuBar=wx.MenuBar()
        menu1=wx.Menu()
        menuBar.Append(menu1,"&Settings")
        menu1.Append(wx.NewId(),"Init","")
        self.SetIcon(icon)
        self.SetMenuBar(menuBar)

    def InitDataDialog(self,Event):
        self.dlg=wx.Frame(None,-1,"InitData",wx.DefaultPosition,(500,500))
        panel=wx.Panel(self.dlg)
        panel.SetBackgroundColour('White')

        #Set the Number of Buses and Stops
        BusLabel=wx.StaticText(panel,-1,"Bus Number:",(30,50))
        self.BusVal=wx.TextCtrl(panel,-1,'4',pos=(130,50),size=(175,20))
        StopLabel=wx.StaticText(panel,-1,"Stop Number:",(30,100))
        self.StopVal=wx.TextCtrl(panel,-1,'6',pos=(130,100),size=(175,20))
        ButtonOK=wx.Button(panel,-1,"Confirm",pos=(200,400))

       #Bind The Button
        self.dlg.Bind(wx.EVT_BUTTON,self.OnClickForInit, ButtonOK)
        self.dlg.Show()

    def OnClickForInit(self,event):
        self.BusNum=int(self.BusVal.GetValue())
        self.StopNum=int(self.StopVal.GetValue())
        self.dlg.Close()

    def OnClickForStart(self,event):
        self.Animation()

    #Animation
    def Animation(self):
        screen = pygame.display.set_mode((506, 709),HWSURFACE | DOUBLEBUF,32)
        pygame.display.set_caption(u'BusSchedule'.encode('utf-8'))
        background = pygame.image\
            .load("road.jpg").convert()
        stop=pygame.image.load("stop.png").convert()
        bus=pygame.image.load("bus.png").convert()
        screen.blit(background,(40,0))
        #init the data
        AllStop=[]
        AllBus=[]
        BusRec=[]
        stopV=[]
        print(self.StopNum)
        #init the Stop Information
        for i in range(self.StopNum):
            it=Stop.Stop(i*709/self.StopNum,i)
            AllStop.append(it)
            x=i*709/self.StopNum
            stopV.append(x)
            screen.blit(stop,(20,stopV[-1]))
            screen.blit(stop,(506-60,stopV[-1]))

        #init the Bus Information
        for i in range(self.BusNum):
            it=Bus.Bus(self.console,i,AllStop[i],AllStop)
            AllBus.append(it)
            BusRec.append(bus.get_rect())
            BusRec[-1].topleft=[70+i*426/self.BusNum,it.NowStop.y]
            screen.blit(bus,BusRec[-1])

        #init the Monitor
        ControlSystem=Monitor.Monitor(AllStop,AllBus)

        #tart the Animation
        speedAll=[]
        for i in range(self.BusNum):
            speedAll.append([0,0])

        #Run the Whole Application
        while True:
            screen.blit(background,(40,0))
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame,quit()
                    exit()
            #Check each Bus, Assign the Requests and ReSchedule
            for i in range(self.BusNum):
                #Change the Speed to make the Bus Run the right Direction
                BusRec[i]=BusRec[i].move(speedAll[i])
                #Draw the Bus
                screen.blit(bus,BusRec[i])
                #Check the Bus has arrived at a stop
                if BusRec[i].top in stopV:
                    #Assign the requests and change the Information of the Bus
                    ControlSystem.work()
                    AllBus[i].collect()
                    AllBus[i].move()
                    self.condition.Clear()
                    for ii in range(len(AllStop)):
                        self.condition.AppendText("Requests of Stop "+str(ii)+" : \n")
                        if len(AllStop[ii].requestList)==0:
                            continue
                        for jj in range(len(AllStop[ii].requestList)):
                            self.condition.AppendText("Dest: Stop"+str(AllStop.index(AllStop[ii].requestList[jj].Destination))+" ,")
                        self.condition.AppendText("\n")
                    speedAll[i]=[0,AllBus[i].Direction]
            pygame.display.update()


'''
Function: Run App
'''
class App(wx.App):
    def OnInit(self):
        image=wx.Icon('bus.jpg',wx.BITMAP_TYPE_JPEG)
        self.frame=Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


#main
def main():
    app=App()
    app.MainLoop()


#run
if __name__=='__main__':
    main()