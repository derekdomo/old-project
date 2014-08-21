__author__ = 'Derek.Sun'
'''
Start:       DataStructure(Stop)
Destination: DataStructure(Stop)
Direction:   -1=UP 1=DOWN
'''
class Request:
    def __init__(self,Start,Destination,Direction):
        self.Start=Start
        self.Destination=Destination
        self.Direction=Direction
        self.Assigned=-1
