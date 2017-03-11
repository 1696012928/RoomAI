#!/bin/python
#coding:utf-8

import roomai.abstract

class Card:
    def __init__(self, point, suit):
        self.point = point
        self.suit  = suit
def compareCard(c1,c2):
    if c1.point != c2.point:
        return c1.point - c2.point
    else:
        return c1.suit - c2.suit
    
#point
#0, 1, 2, 3, ..., 7,  8, 9, 10, 11,  12
#^                ^   ^              ^       
#|                |   |              |       
#2,               9, 10, J,  Q,  K,  A
#
#suit
#0, 1, 2, 3


AllCardsPattern = dict() 
#name, isStraight, isSamePoint, isSameSuit, [SizeOfPair1, SizeOfPair2](desc), rank, cards
AllCardsPattern["Straight_SameSuit"] = \
["Straight_SameSuit",   True,  False, True,  [], 100, []]   
AllCardsPattern["4_1"] = \
["4_1",                 False, True,  False, [4,1], 98,[]]
AllCardsPattern["3_2"] = \
["3_2",                 False, True,  False, [3,2], 97,[]]
AllCardsPattern["SameSuit"] = \
["SameSuit",            False, False, True,  [], 96,[]]
AllCardsPattern["Straight_DiffSuit"] = \
["Straight_DiffSuit",   True,  False, False, [], 95,[]]
AllCardsPattern["3_1_1"] = \
["3_1_1",               False, True,  False, [3,1,1], 94,[]]
AllCardsPattern["2_2_1"] = \
["2_2_1",               False, True,  False, [2,2,1], 93,[]]
AllCardsPattern["2_1_1_1"] = \
["2_1_1_1",             False, True,  False, [2,1,1,1], 92, []]

def Cards2Pattern(hand_cards, remaining_cards):
    point2cards = dict()
    for c in hand_cards + remaining_cards:
        if c.point in point2cards:  point2cards[c.point].append(c)
        else:   point2cards[c.point] = [c]
    for p in point2cards:
        point2cards[p].sort(compareCard)

    suit2cards  = dict()
    for c in hand_cards + remaining_cards:
        if c.suit in suit2cards:    suit2cards[c.suit].append(c)
        else:   suit2cards[c.suit] = [c]
    for s in suit2cards:
        suit2cards[s].sort(compareCard)

    num2point = [[],[],[],[],[]]
    for p in point2cards:
        num = len(point2cards[p])
        num2point[num].append(p)    

    sorted_point = []
    for p in point2cards:
        sorted_point.append(p)
    sorted_point.sort()
   
    ##straight_samesuit 
    for s in suit2cards:
        if len(suit2cards[s]) >= 5:
            numStraight = 1
            for i in xrange(len(suit2cards[s])-2,-1,-1):
                if suit2cards[s][i].point == suit2cards[s][i+1].point -1:
                    numStraight += 1
                else:
                    numStraight  = 1

                if numStraight == 5: 
                    pattern = AllCardsPattern["Straight_SameSuit"]   
                    pattern[6] = suit2cards[s][i:i+5]
                    pattern[6].sort(compareCard)
                    return pattern
    
    ##4_1
    if len(num2point[4]) > 0:
        p4 = num2point[4][0]
        p1 = -1
        for i in xrange(len(sorted_point)-1,-1,-1):
            if sorted_point[i] != p4:   
                p1 = sorted_point[i]
                break
        pattern = AllCardsPattern["4_1"]
        pattern[6] = point2cards[p4][0:4]
        pattern[6].append(point2cards[p1][0])
        pattern[6].sort(compareCard)
        return pattern

    ##3_2 
    if len(num2point[3]) >= 1:
        pattern = AllCardsPattern["3_2"]
        
        if len(num2point[3]) == 2:
            p3 = num2point[3][1]
            pattern[6] = point2cards[p3][0:3]
            p2 = num2point[3][0]            
            pattern[6].append(point2cards[p2][0])
            pattern[6].append(point2cards[p2][1])
            pattern[6].sort(compareCard)
            return pattern

        if len(num2point[2]) >= 1:        
            p3 = num2point[3][0]
            pattern[6] = point2cards[p3][0:3]
            p2 = num2point[3][len(num2point[2])-1]
            pattern[6].append(point2cards[p2][0])
            pattern[6].append(point2cards[p2][1])
            pattern[6].sort(compareCard)
            return pattern
            

    ##SameSuit    
    for s in suit2cards:
        if len(suit2cards[s]) >= 5:
            pattern = AllCardsPattern["SameSuit"]
            len1    = len(suit2cards[s])
            pattern[6] = suit2cards[s][len1-5:len1]  
            pattern[6].sort(compareCard)
            return pattern

    ##Straight_DiffSuit
    numStraight = 1
    for idx in xrange(len(sorted_point)-2,-1,-1):
        if sorted_point[idx] + 1 == sorted_point[idx]:
            numStraight += 1
        else:
            numStraight  = 1

        if numStraight  == 5:
            pattern = AllCards["Straight_DiffSuit"]
            for p in xrange(idx,idx+5):
                point = sorted_point[p]
                pattern[6].append(point2cards[point][0])
            pattern[6].sort(compareCard)
            return pattern

    ##3_1_1
    if len(num2point[3]) == 1:
        pattern = AllCardsPattern["3_1_1"]
        
        p3 = num2point[3][0]
        pattern[6] = point2cards[p3][0:3]       

        num = 0
        for i in xrange(len(sorted_point)-1,-1,-1):
            p = sorted_point[i]
            if p != p3: 
                pattern[6].append(point2cards[p][0])
                num += 1
            if num == 2:    break
        pattern[6].sort(compareCard)
        return pattern


    ##2_2_1
    if len(num2point[2]) >= 2:
        pattern    = AllCards["2_2_1"]
        p21        = num2point[2][len(num2point[2])-1]
        for c in point2cards[p21]:
            pattern[6].append(c)
        p22        = num2point[2][len(num2point[2])-2]
        for c in point2cards[p22]:
            pattern[6].append(c)
        
        flag = False
        for i in xrange(len(sorted_point)-1,-1,-1):
            p = sorted_point[i]
            if p != p21 and p != p22:
                c = point2cards[p][0]
                pattern[6].append(c)
                flag = True
            if flag == True:    break;
        pattern[6].sort(compareCard)
        return pattern

    ##2_1_1_1
    if len(num2point[2]) == 1:
        pattern    = AllCardsPattern["2_1_1_1"]
        p2         = num2point[2][0]
        pattern[6] = point2cards[p2][0:2]
        num     = 0
        for p in xrange(len(sorted_point)-1,-1,-1):
            p1 = sorted_point[p]
            if p1 != p2:
                pattern[6].append(point2cards[p1][0])
            if num == 3:    break
        pattern[6].sort(compareCard)
        return pattern

class Action:
    def __init__(self):
        self.quit   = 0 
        self.cheat  = 1
        self.bet    = 2
        self.price  = 0



class PublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.public_cards       = [] ##public keep_cards
        self.turn               = -1
        self.chips              = [0,0]
        self.blind_id           = -1  
        self.previous_id        = -1
        self.previous_action    = None        

class PrivateState(roomai.abstract.AbstractPrivateState):
    def __init__(self):
        self.keep_cards = []
        self.hand_cards = []

class Info(roomai.abstract.AbstractInfo):
    def __init__(self):
        self.player_id      = -1
        self.public_state   = PublicState()
        self.private_state  = PrivateState()




        
