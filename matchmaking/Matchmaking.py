from QueueSlot import QueueSlot
import random as rd

class Matchmaking:

    def __init__(self):
        self.players_queueing = []
        self.time = 1
        self.id_count = 1
        self.prefered_role_stats = [0, 0, 0, 0, 0]
        self.prefered_subrole_stats = [0, 0, 0, 0, 0]
    
    def addPlayerQueuing(self, nb_of_players):
        for i in range(nb_of_players):
            self.players_queueing.append(QueueSlot.generatePlayerQueueing(self.id_count+i, self.time))
        self.id_count += nb_of_players

    def refreshStatistics(self) :
        self.prefered_role_stats=[0,0,0,0,0]
        self.prefered_subrole_stats=[0,0,0,0,0]
        switcher = {
                "top" : 0,
                "jungle" : 1,
                "mid" : 2,
                "adc" : 3,
                "supp" : 4
        }
        for player in self.players_queueing :
            self.prefered_role_stats[switcher[player.prefered_role]]+=1
            self.prefered_subrole_stats[switcher[player.prefered_subrole]]+=1
        
    def createMatch(self):
        self.refreshStatistics()
        if len(self.players_queueing) < 10 :
            print("Not enough players")
            return(False)
        else :
            available_players = [self.prefered_role_stats[i]+self.prefered_subrole_stats[i] for i in range(5)]
            players = self.players_queueing.copy()
            roles = ["top", "jungle", "mid", "adc", "supp"]
            team1 = [False, False, False, False, False]
            team2 = [False, False, False, False, False]
            switcher = {
                "top" : 0,
                "jungle" : 1,
                "mid" : 2,
                "adc" : 3,
                "supp" : 4
            }
            #Affecting each role 2 players (one per team)
            while roles != [] :
                #Searching role with the least players queueing for
                index_min=0
                value_min=available_players[0]
                for i in range(1,len(roles)) :
                    if available_players[i] < value_min :
                        value_min = available_players[i]
                        index_min = i
                
                print("Matching for " + roles[index_min])
                #If we have less than 2 players, we can't create a match
                if value_min < 2 :
                    return(False)
                #Else, we affect 2 players to that role
                else :
                    for player in players :
                        if player.prefered_role==roles[index_min] :
                            if not team1[switcher[roles[index_min]]] :
                                players.remove(player)
                                team1[switcher[roles[index_min]]]=player
                                print(roles[index_min] + " of team1 is affected")
                            elif not team2[switcher[roles[index_min]]] :
                                players.remove(player)
                                team2[switcher[roles[index_min]]]=player
                                print(roles[index_min] + " of team2 is affected")
                            else :
                                pass
                    for player in players :
                        if player.prefered_subrole==roles[index_min] :
                            if not team1[switcher[roles[index_min]]] :
                                players.remove(player)
                                team1[switcher[roles[index_min]]]=player
                                print(roles[index_min] + " of team1 is affected")
                            elif not team2[switcher[roles[index_min]]] :
                                players.remove(player)
                                team2[switcher[roles[index_min]]]=player
                                print(roles[index_min] + " of team2 is affected")
                            else :
                                pass

                    #Then, we delete the role from the list
                    del roles[index_min]
                    available_players = computeStatistics(players, roles)
            return(team1,team2)

    def removeTeamsFromQueue(self, team1, team2) :
        for player1 in team1 :
            self.players_queueing.remove(player1)
        for player2 in team2 :
            self.players_queueing.remove(player2)
    
    def simulateStep(self) :
        nb_of_players_added = rd.randint(100,500)
        self.addPlayerQueuing(nb_of_players_added)
        possibility_of_a_match = True
        while possibility_of_a_match :
            res = self.createMatch()
            if not res :
                possibility_of_a_match = False
            else :
                team1, team2 = res
                self.removeTeamsFromQueue(team1, team2)
        self.time+=1
        

def computeStatistics(players_queueing, roles) :
    #Creating switcher to count players
    switcher = dict()
    for i in range(len(roles)):
        switcher[roles[i]]=i
    
    #Counting how many players want to play these roles
    available_players = [0 for i in range(len(roles))]
    for player in players_queueing :
        if player.prefered_role in roles :
            available_players[switcher[player.prefered_role]]+=1
        if player.prefered_subrole in roles :
            available_players[switcher[player.prefered_subrole]]+=1
    
    return available_players