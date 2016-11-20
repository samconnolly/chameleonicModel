"""
winModel.py

Chameleonic Alien Model

Created on Sat Nov 19 12:23:36 2016

Author: Sam Connolly
"""
import numpy as np
import pylab as plt
import scipy.stats.mstats as scm

turns = 10


class Stats(object):
    def __init__(self):
        self.research = 0
        self.components = 0
        self.atmospherics = 5
        self.engineering = 5
        self.hydroponics = 5
        self.comms = 0
        self.security = 0
        
    def Hard_Reset(self):
        self.research = 0
        self.components = 0
        self.atmospherics = 5
        self.engineering = 5
        self.hydroponics = 5
        self.comms = 0
        self.security = 0

class Character(object):
    def __init__(self,charType):
        self.type = charType
        if charType == "tank":
            self.health = 6
            self.maxHealth = 6
        else:
            self.health = 3
            self.maxHealth = 3
        self.nutrified = True
        self.dead = False
        self.busy = False
        
    def Damage(self,damage):
        if self.health > 0:
            self.health -= damage
        if self.health <= 0:
            self.Death()
            
    def Heal(self,heal):
        self.health += heal
        if self.health > self.maxHealth:
            self.health = self.maxHealth
            
    def Death(self):
        self.dead = True
        
    def Reset(self):
        self.busy = False
        
    def Hard_Reset(self):
        if self.type == "tank":
            self.health = 6
            self.maxHealth = 6
        else:
            self.health = 3
            self.maxHealth = 3
        self.nutrified = True
        self.dead = False
        self.busy = False
        
        
class Room(object):
    def __init__(self, roomType,statsCounter):
        self.type = roomType
        self.stats = statsCounter
        self.done = False
        self.broken = False
        self.blocked = False
        
    def Use(self,character):
        if self.type == "research":
            self.stats.research += 2
            if character.type == "scientist" and character.nutrified:
                self.stats.research += 1
        if self.type == "manufactory":
            self.stats.components += 2
            if character.type == "manufacturer" and character.nutrified:
                self.stats.components += 1
        if self.type == "hydroponics":
            self.stats.hydroponics += 1
            if character.type == "engineer" and character.nutrified:
                self.stats.hydroponics += 1
        if self.type == "engineering":
            self.stats.engineering += 1
            if character.type == "engineer" and character.nutrified:
                self.stats.engineering += 1
        if self.type == "atmospherics":
            self.stats.atmospherics += 1
            if character.type == "engineer" and character.nutrified:
                self.stats.atmospherics += 1
        if self.type == "comms":
            self.stats.comms += 1
            self.stats.components -= 4
        if self.type == "security":
            fixing = False
            for room in rooms:
                if room.blocked:
                    room.blocked = False
                    room.broken = False
                    fixing = True
            if fixing == False:
                self.stats.security += 1
                self.stats.research -= 2
        if self.type == "outside":
            self.stats.research += 1
            self.stats.components += 1
        if self.type == "medibay":
            character.Heal(1)
            
        character.busy = True
        self.done = True
            
    def Unuse(self):
        if self.type == "hydroponics":
            self.stats.hydroponics -= 1
           
        if self.type == "engineering":
            self.stats.engineering -= 1
           
        if self.type == "atmospherics":
            self.stats.atmospherics -= 1
        self.done = True
        
    def Reset(self):
        self.done = False
        
    def Hard_Reset(self):
        self.done = False
        self.broken = False
        self.blocked = False

def Pick_Best_Engineer():
    if engineer.dead == False and engineer.busy == False:
        return engineer
    elif tank.dead == False and tank.busy == False:
        return tank
    elif manufacturer.dead == False and manufacturer.busy == False:
        return manufacturer
    elif scientist.dead == False and scientist.busy == False:
        return scientist
    elif leader.dead == False and leader.busy == False:
        return leader
    else:
       # print "everyone dead, no one to pick!"
        return None
    
def Pick_Nonessential_Room(nonEssentialRooms):
    pickFrom = []
    for room in nonEssentialRooms:
        if room.done == False:
            if room.type == "comms" and (statsCounter.comms < 3 or (research.done == True and manufactory.done == True)):
                pickFrom.append(room)
            elif room.type == "security" and (statsCounter.security < 5 or (research.done == True and manufactory.done == True)):
                pickFrom.append(room)
            elif room.type == "research" or room.type == "manufactory":
                pickFrom.append(room)                
    #print len(pickFrom)
    p = np.random.randint(len(pickFrom))
    return pickFrom[p]

class Alien_Deck(object):
    def __init__(self,characters,rooms,stats):
        self.deck = [3,2,2,2,2,3,3,2,3,2,2,3,3,2] 
        self.cards = [3,2,2,2,2,3,3,2,3,2,2,3,3,2]       
        self.characters = characters
        self.rooms = rooms
        self.stats = stats
    
    def Pick_Character(self):
        picked = False
        while picked == False:
            c = np.random.randint(5)
            if self.characters[c].dead == False:
                picked = True
                return self.characters[c]
                
    def Pick_Room(self,includeSecurity=True):
        picked = False
        while picked == False:
            r = np.random.randint(8)
            if self.rooms[r].broken == False and (includeSecurity == True or self.rooms[r].type != "security"):
                picked = True
                return self.rooms[r]
                
    def Return_Cards(self):
        self.cards = np.copy(self.deck)
    
    def Draw_Alien_Card(self):
        chances = np.cumsum(self.cards)
        p = np.random.randint(np.sum(self.cards))
        i = 1
        for c in chances:
            if p < c:
                card = i
            else:
                i += 1

        self.cards[i-1] -= 1         
        
        if card == 1:
            #print "alien attack"
            character = self.Pick_Character()
            character.Damage(1)
        elif card == 2:
            #print "alien assault"
            character = self.Pick_Character()
            character.Damage(2)
        elif card == 3:
            #print "life support down"
            self.stats.atmospherics = 0 
        elif card == 4:
            #print "hydroponics attacked"
            self.stats.hydroponics = 0            
        elif card == 5:
            #print "power down"
            self.stats.engineering = 0
        elif card == 6:
           # print "power drain"
            if (self.stats.components > 0):
                self.stats.engineering -= 1
        elif card == 7:
            #print "door broken"
            room = self.Pick_Room(False)
            room.broken = True
            room.blocked = True
        elif card == 8:
            #print "fire"
            room = self.Pick_Room()
            room.broken = True
        elif card == 9:
            #print "lights out"
            room = self.Pick_Room()
            room.broken = True
        elif card == 10:
            #print "security hack"
            if (self.stats.security > 0):
                self.stats.security -= 1
        elif card == 11:
            #print "comms hack"
            if (self.stats.comms > 0):
                self.stats.comms -= 1
        elif card == 12:
            #print "research lost"
            if (self.stats.research > 0):
                self.stats.research -= 2
        elif card == 13:
            #print "components lost"
            if (self.stats.components > 0):
                self. stats.components -= 2
        elif card == 14:
            #print "resources lost"
            if (self.stats.research > 0):
                self.stats.research -= 1
            if (self.stats.components > 0):
                self. stats.components -= 1
        


# MODEL

# stats        
statsCounter = Stats()

# rooms
research = Room("research",statsCounter)
manufactory = Room("manufactory",statsCounter)
hydroponics = Room("hydroponics",statsCounter)
engineering = Room("engineering",statsCounter)
atmospherics = Room("atmospherics",statsCounter)
comms = Room("comms",statsCounter)
security = Room("security",statsCounter)
outside = Room("outside",statsCounter)
medibay = Room("medibay",statsCounter)

# in order of importance
rooms = [atmospherics,medibay,comms,engineering,manufactory,research,hydroponics,\
                security,outside]
nonEssentialRooms = [research,manufactory,comms,security,outside]     

# characters
scientist = Character("scientist")
manufacturer = Character("manufacturer")
engineer = Character("engineer")
leader = Character("leader")
tank = Character("tank")

# in order of importance
characters = [leader,engineer,scientist,manufacturer,tank] 

# decks
alienDeck = Alien_Deck(characters,rooms,statsCounter)

def Run_Sim():
    
    # tracking
    researchTrack = np.zeros(11)
    componentsTrack = np.zeros(11)
    commsTrack = np.zeros(11)
    securityTrack = np.zeros(11)
    healthTrack = np.zeros((5,11))
    healthTrack[:4,0] = 3
    healthTrack[4,0] = 6
    nutritionTrack = np.zeros(11)
    nutritionTrack[0] = 1
    hydroponicsTrack = np.zeros(11)
    hydroponicsTrack[0] = 5
    engineeringTrack = np.zeros(11)
    engineeringTrack[0] = 5    
    atmosphericsTrack = np.zeros(11)
    atmosphericsTrack[0] = 5
    winConditionsMet = [0,0,0]
        
    turns = range(1,11)
    
    for turn in turns:
        #print "Turn",turn
        
        # fix blocked rooms if possible
        for room in rooms:
            if room.blocked:
                if tank.busy == False and tank.dead == False:
                    security.Use(tank)
                elif scientist.busy == False and scientist.dead == False:
                    security.Use(scientist)
                elif manufacturer.busy == False and manufacturer.dead == False:
                    security.Use(manufacturer)
                elif leader.busy == False and leader.dead == False:
                    security.Use(leader)
                elif engineer.busy == False and engineer.dead == False:
                    security.Use(engineer)
        
        #=== Use characters ===
        remainingCharacters = 0
        for character in characters:
            if character.dead == False:
                remainingCharacters += 1
        
        # make sure everything is working well enough
        if statsCounter.atmospherics <= 3 and atmospherics.broken == False:
            choice = Pick_Best_Engineer()
            if choice == None:
                break
            atmospherics.Use(choice)
            remainingCharacters -= 1
            
        if statsCounter.engineering <= 3 and engineering.broken == False:
            choice = Pick_Best_Engineer()        
            if choice == None:
                break
            engineering.Use(choice)
            remainingCharacters -= 1
            
        if statsCounter.hydroponics <= 3 and hydroponics.broken == False:
            choice = Pick_Best_Engineer()        
            if choice == None:
                break
            hydroponics.Use(choice)
            remainingCharacters -= 1
            
        # heal whoever needs it most

        if medibay.broken == False:
            done = False
            healthCheck = 1
            char = 0
            while done == False and healthCheck < 4:
                if characters[char].health == healthCheck:
                    medibay.Use(characters[char])
                    done = True
                    remainingCharacters -= 1
                else:
                    char += 1
                if char == len(characters):
                    char = 0
                    healthCheck += 1
                
        # fix comms a bit if possible
        if statsCounter.components >= 4 and statsCounter.comms < 3 and comms.broken == False:
            if tank.busy == False and tank.dead == False:
                comms.Use(tank)
            elif leader.busy == False and leader.dead == False:
                comms.Use(leader)
            elif scientist.busy == False and scientist.dead == False:
                comms.Use(scientist)
            elif manufacturer.busy == False and manufacturer.dead == False:
                comms.Use(manufacturer)
            elif engineer.busy == False and engineer.dead == False:
                comms.Use(engineer)
            remainingCharacters -= 1
                    
        # run security if possible
        if remainingCharacters > 0 and statsCounter.research >= 2 and statsCounter.security < 5 and security.broken == False:
            if tank.busy == False and tank.dead == False:
                security.Use(tank)
            elif leader.busy == False and leader.dead == False:
                security.Use(leader)
            elif scientist.busy == False and scientist.dead == False:
                security.Use(scientist)
            elif manufacturer.busy == False and manufacturer.dead == False:
                security.Use(manufacturer)
            elif engineer.busy == False and engineer.dead == False:
                security.Use(engineer)                
            remainingCharacters -= 1
                
        # prioritise getting components
        if remainingCharacters > 0 and statsCounter.components/4 < statsCounter.research/2 + 1 and manufactory.broken == False:
            if manufacturer.busy == False and manufacturer.dead == False:
                manufactory.Use(manufacturer)
            elif tank.busy == False and tank.dead == False:
                manufactory.Use(tank)
            elif leader.busy == False and leader.dead == False:
                manufactory.Use(leader)
            elif scientist.busy == False and scientist.dead == False:
                manufactory.Use(scientist)
            elif engineer.busy == False and engineer.dead == False:
                manufactory.Use(engineer)                  
            remainingCharacters -= 1            

        # then get research
        if remainingCharacters > 0 and statsCounter.research/2 < statsCounter.components/4 + 1 and research.broken == False:
            if scientist.busy == False and scientist.dead == False:
                research.Use(scientist)
            elif tank.busy == False and tank.dead == False:
                research.Use(tank)
            elif leader.busy == False and leader.dead == False:
                research.Use(leader)
            elif manufacturer.busy == False and manufacturer.dead == False:
                research.Use(manufacturer)
            elif engineer.busy == False and engineer.dead == False:
                research.Use(engineer)                 
            remainingCharacters -= 1 

        # or go outside if fairly even
        if remainingCharacters > 0:
            if manufacturer.busy == False and manufacturer.dead == False:
                outside.Use(manufacturer)
            elif tank.busy == False and tank.dead == False:
                outside.Use(tank)
            elif leader.busy == False and leader.dead == False:
                outside.Use(leader)
            elif scientist.busy == False and scientist.dead == False:
                outside.Use(scientist)
            elif engineer.busy == False and engineer.dead == False:
                outside.Use(engineer)                  
            remainingCharacters -= 1 
            
        # then components...
        if remainingCharacters > 0 and manufactory.done == False and manufactory.broken == False:
            if manufacturer.busy == False and manufacturer.dead == False:
                manufactory.Use(manufacturer)
            elif tank.busy == False and tank.dead == False:
                manufactory.Use(tank)
            elif leader.busy == False and leader.dead == False:
                manufactory.Use(leader)
            elif scientist.busy == False and scientist.dead == False:
                manufactory.Use(scientist)
            elif engineer.busy == False and engineer.dead == False:
                manufactory.Use(engineer) 
            remainingCharacters -= 1            

        # then research
        if remainingCharacters > 0 and research.done == False and research.broken == False:
            if scientist.busy == False and scientist.dead == False:
                research.Use(scientist)
            elif tank.busy == False and tank.dead == False:
                research.Use(tank)
            elif leader.busy == False and leader.dead == False:
                research.Use(leader)
            elif manufacturer.busy == False and manufacturer.dead == False:
                research.Use(manufacturer)
            elif engineer.busy == False and engineer.dead == False:
                research.Use(engineer)                 
            remainingCharacters -= 1         
    
        #=== tracking ===
        researchTrack[turn] = (statsCounter.research)
        componentsTrack[turn] = (statsCounter.components)
        commsTrack[turn] = (statsCounter.comms)
        securityTrack[turn] = (statsCounter.security)
        for i in range(5):
            healthTrack[i][turn] = (characters[i].health)
        nutritionTrack[turn] = ((statsCounter.hydroponics < 3))
        hydroponicsTrack[turn] = (statsCounter.hydroponics)
        engineeringTrack[turn] = (statsCounter.engineering)
        atmosphericsTrack[turn] = (statsCounter.atmospherics)   
        

        #=== Stats impact ====    
        if statsCounter.atmospherics < 3:
            for character in characters:
                character.Damage(1)
        nutrified = True
        if statsCounter.hydroponics < 3:
            nutrified = False
        for character in characters:
            character.nutrified = nutrified        
        
        #==== Run empty rooms & free up burning/lights out rooms ====
        for room in rooms:
            if room.done == False:
                room.Unuse()
            if room.broken and room.blocked == False:
                room.broken = False                
                
        #=== Run Alien Cards ====            
        alienDeck.Draw_Alien_Card()
        alienDeck.Draw_Alien_Card()
        alienDeck.Return_Cards()
        
        #=== Reset characters and rooms ===
        for room in rooms:
            room.Reset()
        for character in characters:
            character.Reset()
            
        #=== check failure ====
        deadCount = 0
        for character in characters:
            if character.dead:
                deadCount += 1
                
        if deadCount == 5:
            #print "FAILURE: All characters dead."
            break
        
    # track win conditions
    if statsCounter.comms == 3:
        winConditionsMet[0] = 1.0
    if statsCounter.security == 5:
        winConditionsMet[1] = 1.0
    winConditionsMet[2] += deadCount
    
    # reset everything for next time
    for character in characters:
        character.Hard_Reset()
    for room in rooms:
        room.Hard_Reset()
    statsCounter.Hard_Reset()
            
    return  researchTrack,componentsTrack,commsTrack,securityTrack,healthTrack,hydroponicsTrack,engineeringTrack,atmosphericsTrack,np.array(winConditionsMet)
        

sims = 100

researchTracks,componentsTracks,commsTracks,securityTracks,healthTracks,hydroponicsTracks,engineeringTracks,atmosphericsTracks = [],[],[],[],[],[],[],[]

winConditionsMetAverage  = np.array([0,0,0])

for s in range(sims):
    
    researchTrack,componentsTrack,commsTrack,securityTrack,healthTrack,hydroponicsTrack,engineeringTrack,atmosphericsTrack,winConditionsMet = Run_Sim()        
    researchTracks.append(researchTrack)
    commsTracks.append(commsTrack)
    securityTracks.append(securityTrack)
    healthTracks.append(healthTrack)
    hydroponicsTracks.append(hydroponicsTrack)
    componentsTracks.append(componentsTrack)
    engineeringTracks.append(engineeringTrack)
    atmosphericsTracks.append(atmosphericsTrack)
    winConditionsMetAverage = winConditionsMetAverage + winConditionsMet

    
# tracking
researchTrack = np.mean(researchTracks,axis=0)
commsTrack = np.mean(commsTracks,axis=0)
securityTrack = np.mean(securityTracks,axis=0)
healthTrack = np.mean(healthTracks,axis=0)
hydroponicsTrack = np.mean(hydroponicsTracks,axis=0)
engineeringTrack = np.mean(engineeringTracks,axis=0)
componentsTrack = np.mean(componentsTracks,axis=0)
atmosphericsTrack = np.mean(atmosphericsTracks,axis=0)

# final conditions
winConditionsMetAverage = winConditionsMetAverage / float(sims)
#mostCommonDeaths = scm.mode(deathCount)
print "Comms success fraction",winConditionsMetAverage[0]
print "Security success fraction",winConditionsMetAverage[1]
print "Average number of deaths",winConditionsMetAverage[2]

turns = range(11)
plt.subplot(2,2,1)
# means
plt.plot(turns,researchTrack,linewidth=5.0,color='purple',label='research',zorder=1)
plt.plot(turns,componentsTrack,linewidth=5.0,color='orange',label='components',zorder=1)
for rt in researchTracks[:100]:
    plt.plot(turns,rt,linewidth=2.0,color='purple',alpha=0.1,zorder=0)
for ct in componentsTracks[:100]:
    plt.plot(turns,ct,linewidth=2.0,color='orange',alpha=0.1,zorder=0)
plt.legend()
plt.subplot(2,2,2)
plt.plot(turns,commsTrack,linewidth=5.0,color='blue',label='comms',zorder=1)
plt.plot(turns,securityTrack,linewidth=5.0,color='green',label='security',zorder=1)
for ct in commsTracks[:100]:
    plt.plot(turns,ct,linewidth=2.0,color='blue',alpha=0.1,zorder=0)
for st in securityTracks[:100]:
    plt.plot(turns,st,linewidth=2.0,color='green',alpha=0.1,zorder=0)


plt.legend()
plt.subplot(2,2,3)
for i in range(5):
    if i == 0:
        plt.plot(turns,healthTrack[i],linewidth=5.0,color='red',label='health',zorder=1)
    else:
        plt.plot(turns,healthTrack[i],linewidth=5.0,color='red',zorder=1)
    for ht in healthTracks[:100]:   
        plt.plot(turns,ht[i],linewidth=2.0,color='red',alpha=0.1,zorder=0)     

plt.legend()
plt.subplot(2,2,4)
plt.plot(turns,hydroponicsTrack,linewidth=5.0,color='green',label='hydroponics',zorder=1)
for ct in hydroponicsTracks[:100]:
    plt.plot(turns,ct,linewidth=2.0,color='green',alpha=0.1,zorder=0)
plt.plot(turns,engineeringTrack,linewidth=5.0,color='red',label='engineering',zorder=1)
for ct in engineeringTracks[:100]:
    plt.plot(turns,ct,linewidth=2.0,color='red',alpha=0.1,zorder=0)
plt.plot(turns,atmosphericsTrack,linewidth=5.0,color='blue',label='atmospherics',zorder=1)
for ct in atmosphericsTracks[:100]:
    plt.plot(turns,ct,linewidth=2.0,color='blue',alpha=0.1,zorder=0)
plt.legend()
plt.show()




            
            