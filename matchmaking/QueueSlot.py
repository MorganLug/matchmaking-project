import random as rd
from Player import *

class QueueSlot:

    def __init__(self, player, prefered_role, prefered_subrole, joining_queue_time):
        self.player = player
        self.prefered_role = prefered_role
        self.prefered_subrole = prefered_subrole
        self.joining_queue_time = joining_queue_time

    def __repr__(self):
        return("Player of id " + str(self.player.id) + " joined queue on step " + str(self.joining_queue_time) + " trying to find roles : " + self.prefered_role + ", " + self.prefered_subrole + ".")

    @staticmethod
    def generatePlayerQueueing(id, joining_queue_time):
        roles = ["top", "jungle", "mid", "adc", "supp"]
        index1 = rd.randint(0,4)
        index2 = rd.randint(0,4)
        while index2 == index1 :
            index2 = rd.randint(0,4)
        return(QueueSlot(Player(id), roles[index1], roles[index2], joining_queue_time))