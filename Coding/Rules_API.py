# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:37:21 2022

@author: aless
"""
#HINT GIVING METHODS
def get_chop_index(player, players, hints, len_hand = False):
    """returns the index of the chopping card"""
    if len(players) < 4:
        hand_index = [0,1,2,3,4]
    else:
        hand_index = [0,1,2,3]
    if len_hand != False:
        hand_index = [i for i in range(len_hand)]
    #print(hand_index)
    hint_position = []
    subtraction = [0] 
    for hint in hints[player]:
        for position in hint[0]:
            if position not in hint_position:
                hint_position.append(position)
        subtraction = [position for position in hand_index if position not in hint_position]
        subtraction.sort()
    if subtraction==[]: #Full chop
        return "full chop"
    return subtraction[0]

def get_hintable_cards(player, players, hints):
    """return the list of indexes of hintable cards for play hints"""
    if len(players) < 4:
        hand_index = [0,1,2,3,4]
        subtraction = [0,1,2,3,4] 
    else:
        hand_index = [0,1,2,3]
        subtraction = [0,1,2,3]  
    hint_position = []
    for hint in hints[player]:
        for position in hint[0]:
            if position not in hint_position:
                hint_position.append(position)
        subtraction = [position for position in hand_index if position not in hint_position]
        subtraction.sort()
    #print(subtraction)
    if subtraction==[]: #Full chop
        return "full chop"
    return subtraction

def chop_discard(player, players, hints, len_hand):
    """Function used to discard the chop card"""
    #print(len_hand)
    chop_index = get_chop_index(player, players, hints, len_hand)
    action = f"discard {chop_index}"
    return action

def search_save_hint_5(current_player, players, hints, tableCards):
    """hints a 5 to the player if it is in the chop zone"""
    try:
        for player in players:
            if current_player == player.name:
                continue
            chop_player = get_chop_index(player.name, players, hints)
            if chop_player == "full chop":
                return False
            if player.hand[chop_player].value == 5 and len(tableCards[player.hand[chop_player].color])<=4:
                action = f"hint value {player.name} 5"
                return action
    except:
        return False
    return False

def search_save_hint_2(current_player, players, hints, discardPile, tableCards):
    """hints a 2 to the player if that 2 is the only copy on the field and is on the chop zone"""
    try:
        flag = False
        for player in players:
            if current_player == player.name:
                continue
            chop_player = get_chop_index(player.name,players, hints)
            if chop_player == "full chop":
                return False
            if player.hand[chop_player].value == 2:
                flag = True
                if player.hand[chop_player].value <= len(tableCards[player.hand[chop_player].color]):
                    flag = False
                for player2 in players:
                    for card2 in player2.hand:
                        if player.hand[chop_player].id == card2.id:
                            continue
                        if card2.value == player.hand[chop_player].value and player.hand[chop_player].color == card2.color:
                            flag = False
                for card in discardPile:
                    if player.hand[chop_player].value == card.value and player.hand[chop_player].color == card.color:
                        flag = True
            if flag==True and len(tableCards[player.hand[chop_player].color])<=1:
                action = f"hint value {player.name} 2"
                return action
    except:
        return False
    return False
    
def search_save_hint_critical(current_player, players, hints, discardPile, tableCards):
    """search for hints related to cards with one copy remaining and is on the chop zone"""
    try:
        #print("SONO IN SAVE CRITICAL")
        flag = False
        for player in players:
            if current_player == player.name:
                continue
            chop_player = get_chop_index(player.name,players, hints)
            if chop_player == "full chop":
                return False
            for card in discardPile:
                if player.hand[chop_player].value == card.value and player.hand[chop_player].color == card.color:
                    flag+=1
            if player.hand[chop_player].value == len(tableCards[player.hand[chop_player].color]):
                flag = False
            for player2 in players:
                for card2 in player2.hand:
                    if player.hand[chop_player].id == card2.id:
                        continue
                    if card2.value == player.hand[chop_player].value and player.hand[chop_player].color == card2.color:
                        flag = False
            if player.hand[chop_player].value == 1:
                if flag==2 and len(tableCards[player.hand[chop_player].color])==0:
                    action = f"hint value {player.name} 1"
                    return action
            if player.hand[chop_player].value != 1:
                if flag==1 and len(tableCards[player.hand[chop_player].color])<=player.hand[chop_player].value:
                    action = f"hint value {player.name} {player.hand[chop_player].value}"
                    return action
    except:
        return False
    return False
            
def search_play_hint(current_player, players, hints, discardPile, tableCards):
    """gives an hint to a player, hoping it will play that card"""
    try:
        if len(players) == 2:
            #print("SONO SU PLAY HINT PER DUE")
            action = "" 
            for player in players:
                if current_player == player.name:
                    continue
                possible_hints = get_hintable_cards(player.name,players, hints)
                if possible_hints == "full chop":
                    continue
                for candidate in possible_hints: 
                    
                    flag = "default"
                    if len(tableCards[player.hand[candidate].color]) == 0:
                        print("aaaaa")
                        if player.hand[candidate].value == 1:
                            print("Bbbbbb")
                            if candidate == get_chop_index(player.name,players, hints):
                                flag = "color"
                                print("IMMEDIATE COLOR ACTIVATE")
                            if flag!= "color":
                                for card in player.hand:
                                    if card.id == player.hand[candidate].id:
                                        continue
                                    elif card.value == player.hand[candidate].value:
                                        if flag == "value":
                                            flag = "false"
                                            break
                                        flag = "color"
                                    elif card.color == player.hand[candidate].color:
                                        if flag == "color":
                                            flag = "false"
                                            break
                                        flag = "value"
                            if flag=="value":
                                #Search hints to see if hint is redundant or dangerous
                                flag_other_hints = True
                                for player2 in players:
                                     if player2.name == current_player:
                                         for hint in hints[player2.name]:
                                             for info in hint[3]:
                                                 if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                     if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                         #print("CHECK REDUNDANT VALUE SELF")
                                                         flag_other_hints = False
                                     elif player2.name != current_player:
                                         for index2, card2 in enumerate(player2.hand):
                                                 for hint in hints[player2.name]:
                                                     if index2 in hint[0]:
                                                         if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                             #print("CHECK REDUNDANT VALUE")
                                                             flag_other_hints = False
                                if flag_other_hints == True:
                                    action = f"hint value {player.name} {player.hand[candidate].value}"
                                    return action
                            elif flag=="color" or flag=="default":
                                flag_other_hints = True
                                for player2 in players:
                                    for hint in hints[player2.name]:
                                        for info in hint[3]:
                                            if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                #print("CHECK REDUNDANT COLOR")
                                                flag_other_hints = False
                                if flag_other_hints == True:
                                    action = f"hint color {player.name} {player.hand[candidate].color}"
                                    return action
            
                    elif len(tableCards[player.hand[candidate].color]) != 0:
                        if player.hand[candidate].value == tableCards[player.hand[candidate].color][-1].value+ 1:
                            if candidate == get_chop_index(player.name,players, hints):
                                flag = "color"
                                #print("IMMEDIATE COLOR ACTIVATE")
                            if flag != "color":
                                for card in player.hand:
                                    if card.id == player.hand[candidate].id:
                                        continue
                                    if card.value == player.hand[candidate].value:
                                        if flag == "value":
                                            flag = "false"
                                            break
                                        flag = "color"
                                    elif card.color == player.hand[candidate].color:
                                        if flag == "color":
                                            flag = "false"
                                            break
                                        flag = "value"
                            if flag=="value":
                                #Search hints to see if hint is redundant or dangerous
                                flag_other_hints = True
                                for player2 in players:
                                     if player2.name == current_player:
                                         for hint in hints[player2.name]:
                                             for info in hint[3]:
                                                 if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                     if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                         #print("CHECK REDUNDANT VALUE SELF")
                                                         flag_other_hints = False
                                     elif player2.name != current_player:
                                         for index2, card2 in enumerate(player2.hand):
                                                 for hint in hints[player2.name]:
                                                     if index2 in hint[0]:
                                                         if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                             #print("CHECK REDUNDANT VALUE")
                                                             flag_other_hints = False
                                if flag_other_hints == True and candidate != get_chop_index(player.name, players, hints):
                                    action = f"hint value {player.name} {player.hand[candidate].value}"
                                    return action
                            elif flag=="color" or flag=="default":
                                flag_other_hints = True
                                for player2 in players:
                                    for hint in hints[player2.name]:
                                        for info in hint[3]:
                                            if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                #print("CHECK REDUNDANT COLOR")
                                                flag_other_hints = False
                                if flag_other_hints == True:
                                    action = f"hint color {player.name} {player.hand[candidate].color}"
                                    return action
        elif len(players) > 2:
           action = "" 
           for player in players:
               if current_player == player.name:
                   continue
               possible_hints = get_hintable_cards(player.name,players, hints)
               if possible_hints == "full chop":
                   continue
               for candidate in possible_hints: 
                   flag = "default"
                   if len(tableCards[player.hand[candidate].color]) == 0:
                       
                       if player.hand[candidate].value == 1:
                           
                           if candidate == get_chop_index(player.name,players, hints):
                               flag = "color"
                               #print("IMMEDIATE COLOR ACTIVATE")
                           if flag!= "color":
                               for card in player.hand:
                                   if card.id == player.hand[candidate].id:
                                       continue
                                   elif card.value == player.hand[candidate].value:
                                       if flag == "value":
                                           flag = "false"
                                           break
                                       flag = "color"
                                   elif card.color == player.hand[candidate].color:
                                       if flag == "color":
                                           flag = "false"
                                           break
                                       flag = "value"
                           if flag=="value":
                               #Search hints to see if hint is redundant or dangerous
                               flag_other_hints = True
                               for player2 in players:
                                    if player2.name == current_player:
                                        for hint in hints[player2.name]:
                                            for info in hint[3]:
                                                if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                    if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                        #print("CHECK REDUNDANT VALUE SELF")
                                                        flag_other_hints = False
                                    elif player2.name != current_player:
                                        for index2, card2 in enumerate(player2.hand):
                                                for hint in hints[player2.name]:
                                                    if index2 in hint[0]:
                                                        if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                            #print("CHECK REDUNDANT VALUE")
                                                            flag_other_hints = False
                               if flag_other_hints == True:
                                   action = f"hint value {player.name} {player.hand[candidate].value}"
                                   return action
                           elif flag=="color" or flag=="default":
                               flag_other_hints = True
                               for player2 in players:
                                   for hint in hints[player2.name]:
                                       for info in hint[3]:
                                           if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                               #print("CHECK REDUNDANT COLOR")
                                               flag_other_hints = False
                               if flag_other_hints == True:
                                   action = f"hint color {player.name} {player.hand[candidate].color}"
                                   return action
           
                   elif len(tableCards[player.hand[candidate].color]) != 0:
                       if player.hand[candidate].value == tableCards[player.hand[candidate].color][-1].value+ 1:
                           if candidate == get_chop_index(player.name,players, hints):
                               flag = "color"
                               #print("IMMEDIATE COLOR ACTIVATE")
                           if flag != "color":
                               for card in player.hand:
                                   if card.id == player.hand[candidate].id:
                                       continue
                                   if card.value == player.hand[candidate].value:
                                       if flag == "value":
                                           flag = "false"
                                           break
                                       flag = "color"
                                   elif card.color == player.hand[candidate].color:
                                       if flag == "color":
                                           flag = "false"
                                           break
                                       flag = "value"
                           if flag=="value":
                                flag_other_hints = True
                                for player2 in players:
                                    if player2.name == current_player:
                                        for hint in hints[player2.name]:
                                            for info in hint[3]:
                                                if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                    if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                        #print("CHECK REDUNDANT VALUE SELF")
                                                        flag_other_hints = False
                    
                                    elif player2.name != current_player:
                                        for index2, card2 in enumerate(player2.hand):
                                                for hint in hints[player2.name]:
                                                    if index2 in hint[0]:
                                                        if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                            #print("CHECK REDUNDANT VALUE")
                                                            flag_other_hints = False
                                if flag_other_hints == True:
                                    action = f"hint value {player.name} {player.hand[candidate].value}"
                                    return action
                           elif flag=="color" or flag=="default":
                               flag_other_hints = True
                               for player2 in players:
                                   for hint in hints[player2.name]:
                                       for info in hint[3]:
                                           if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                               #print("CHECK REDUNDANT")
                                               flag_other_hints = False
                               if flag_other_hints == True:
                                   action = f"hint color {player.name} {player.hand[candidate].color}"
                                   return action  
    except:
        return False        
    return False
    
#HINT RECEIVING METHODS
        
def evaluate_hint(current_player, players, hints, tableCards, discardPile):
    """Function used by the bot to evaluate an hint and understand its probable identity"""
    #print(hints)   
    for player in hints:
        for hint in hints[player]:
            
            flag_skip_evaluation = False
            if len(hint[0]) == 1:
                if len(hint[3]) != 0:
                    for info in hint[3]:
                        if info.split(" ")[0] == "save":
                            flag_skip_evaluation = "save"
                            continue #No revaluation of save hints
                        if info.split(" ")[0] == "keep":
                            flag_skip_evaluation = "keep"
                            continue #No revaluation of save hints
                        if info.split(" ")[0] == "certain":
                            flag_skip_evaluation = True
                            continue #No revaluation of save hints
                        if info.split(" ")[0] == "play":
                            flag_skip_evaluation = False
                            break
                if flag_skip_evaluation == "save": #Handle a save hint
                    flag_same_level = True
                    flag_discard = True
                    for pile in tableCards:
                        if len(tableCards[pile]) != 0:
                            if tableCards[pile][-1].value != int(hint[1]) - 1:
                                flag_same_level = False
                            if tableCards[pile][-1].value < hint[1]:
                                flag_discard = False
                        else:
                            if hint[1] != 1:
                                flag_same_level = False
                            flag_discard = False
                        
                    if flag_same_level == True:
                        hint[3] = []
                        hint[3].append(f"save play {hint[0][0]}")
                    elif flag_discard == True:
                        hint[3] = []
                        hint[3].append(f"save discard {hint[0][0]}")
                    else:
                        hint[3] = []
                        hint[3].append(f"save {hint[1]}")
                        
                if flag_skip_evaluation == "keep": #Handle a keep hint
                    flag_same_level = True
                    flag_discard = True
                    if hint[2] == "value":
                        for pile in tableCards:
                            if len(tableCards[pile]) != 0:
                                if tableCards[pile][-1].value != hint[1] - 1:
                                    flag_same_level = False
                                if tableCards[pile][-1].value < hint[1]:
                                    flag_discard = False
                            else:
                                if hint[1] != 1:
                                    flag_same_level = False
                                flag_discard = False
                            
                        if flag_same_level == True:
                            hint[3] = []
                            hint[3].append(f"keep play {hint[0][0]}")
                        elif flag_discard == True:
                            hint[3] = []
                            hint[3].append(f"keep discard {hint[0][0]}")
                        else:
                            hint[3] = []
                            hint[3].append(f"keep {hint[1]}")
                    elif hint[2] == "color":
                        if len(tableCards[hint[1]]) == 5:
                            hint[3] = []
                            hint[3].append(f"keep discard {hint[0][0]}")
                        else:
                            hint[3] = []
                            hint[3].append(f"keep {hint[1]}")
                        
                if flag_skip_evaluation == False:        
                    hint[3] = [] #reset
                    #Used to adjust obsolete hints
                    
                    #Can it be a play hint?
                    for pile in tableCards:
                        if len(tableCards[pile]) != 0:
                            if hint[2] == "color" and len(hint[0])==1 and hint[1] == pile and len(tableCards[hint[1]])<5:
                                hint[3].append(f"play {hint[0][-1]} {tableCards[pile][-1].value+1} {hint[1]}")
                            elif hint[2] == "value" and len(hint[0])==1 and tableCards[pile][-1].value == hint[1]-1:
                                hint[3].append(f"play {hint[0][-1]} {hint[1]} {pile}")
                        elif len(tableCards[pile]) == 0:
                            if hint[2] == "color" and hint[1] == pile and len(hint[0])==1:
                                hint[3].append(f"play {hint[0][-1]} 1 {hint[1]}")
                            elif hint[2] == "value" and len(hint[0])==1 and hint[1]==1:
                                hint[3].append(f"play {hint[0][-1]} {hint[1]} {pile}")
                    if len(hint[3]) == 0:
                        hint[3].append(f"keep {hint[1]}")
                            
            if len(hint[0]) > 1:
                if len(hint[3]) != 0:
                    for info in hint[3]:
                        if info.split(" ")[0] == "save":
                            flag_skip_evaluation = "save"
                            continue #No revaluation of save hints
                        if info.split(" ")[0] == "keep":
                            flag_skip_evaluation = "keep"
                            continue #No revaluation of save hints
                        if info.split(" ")[0] == "certain":
                            flag_skip_evaluation = True
                            continue #No revaluation of save hints
                        
                if hint[4] != "":
                    focus = hint[4].split(" ")[1]
                else:
                    focus = hint[0][-1]
                
                if flag_skip_evaluation == "save": #Handle a save hint
                    flag_same_level = True
                    flag_discard = True
                    for pile in tableCards:
                        if len(tableCards[pile]) != 0:
                            if tableCards[pile][-1].value != int(hint[1]) - 1:
                                flag_same_level = False
                            if tableCards[pile][-1].value < hint[1]:
                                flag_discard = False
                        else:
                            if hint[1] != 1:
                                flag_same_level = False
                            flag_discard = False
                        
                    if flag_same_level == True:
                        hint[3] = []
                        hint[3].append(f"save play {focus}")
                    elif flag_discard == True:
                        hint[3] = []
                        hint[3].append(f"save discard {focus}")
                    else:
                        hint[3] = []
                        hint[3].append(f"save {hint[1]}")
                        
                if flag_skip_evaluation == "keep": #Handle a keep hint
                
                    flag_same_level = True
                    flag_discard = True
                    if hint[2] == "value":
                        for pile in tableCards:
                            if len(tableCards[pile]) != 0:
                                if tableCards[pile][-1].value != hint[1] - 1:
                                    flag_same_level = False
                                if tableCards[pile][-1].value < hint[1]:
                                    flag_discard = False
                            else:
                                if hint[1] != 1:
                                    flag_same_level = False
                                flag_discard = False
                            
                        if flag_same_level == True:
                            hint[3] = []
                            hint[3].append(f"keep play {focus}")
                        elif flag_discard == True:
                            hint[3] = []
                            hint[3].append(f"keep discard {focus}")
                        else:
                            hint[3] = []
                            hint[3].append(f"keep {hint[1]}")
                    elif hint[2] == "color":
                        if len(tableCards[hint[1]]) == 5:
                            hint[3] = []
                            hint[3].append(f"keep discard {focus}")
                        else:
                            hint[3] = []
                            hint[3].append(f"keep {hint[1]}")
                if flag_skip_evaluation == False:
                    hint[3] = [] #reset
                
                    #Can it be a play hint?
                    for pile in tableCards:
                        if len(tableCards[pile]) != 0:
                            if hint[2] == "color" and hint[1] == pile and len(tableCards[hint[1]])<5:
                                hint[3].append(f"play {focus} {tableCards[pile][-1].value+1} {hint[1]}")
                            elif hint[2] == "value" and tableCards[pile][-1].value == hint[1]-1:
                                hint[3].append(f"play {focus} {hint[1]} {pile}")
    
                        elif len(tableCards[pile]) == 0:
                            if hint[2] == "color" and hint[1] == pile:
                                hint[3].append(f"play {focus} 1 {hint[1]}")
                            elif hint[2] == "value" and hint[1]==1:
                                hint[3].append(f"play {focus} {hint[1]} {pile}")
                    if len(hint[3]) == 0:
                        hint[3].append(f"keep {hint[1]}")
    if False:
        #Can it be a delayed play hint
        for player in hints:
            if player != current_player:
                continue
            for hint in hints[player]:
                if hint[3][0].split(" ")[0] == "play" :
                    if len(hint[0]) == 1:
                        if hint[2] == "color":
                            for player2 in players:
                                if player2.name == player:
                                    continue
                                for index, card in enumerate(player2.hand):
                                    for hint2 in hints[player2.name]:
                                        if len(tableCards[hint[1]]) == 0:
                                            if card.value == 1 and index in hint2[0] and card.color == hint[1]:
                                                hint[3].append(f"delayed play 2 {hint[1]}")
                                        else:
                                            if card.value == tableCards[hint[1]][-1].value -1 and index in hint2[0] and card.color == hint[1]:
                                                hint[3].append(f"delayed play {tableCards[hint[1]][-1].value+1} {hint[1]}")
                        if hint[2] == "value":
                            for player2 in players:
                                if player2.name == player:
                                    continue
                                for index, card in enumerate(player2.hand):
                                    for hint2 in hints[player2.name]:
                                        if len(tableCards[card.color]) == 0:
                                            if card.value == 1 and index in hint2[0] and hint[1] == 2:
                                                hint[3].append(f"delayed play 2 {card.color}")
                                        else:
                                            if card.value == tableCards[card.color][-1].value -1 and index in hint2[0] and hint[1] == card.value + 1:
                                                hint[3].append(f"delayed play {tableCards[card.color][-1].value+1} {card.color}")
                    if len(hint[0]) > 1:
                        if hint[4] != "":
                            focus = hint[4].split(" ")[1]
                        else:
                            focus = hint[0][-1]
                            
                        if hint[2] == "color":
                            for player2 in players:
                                if player2.name == player:
                                    continue
                                for index, card in enumerate(player2.hand):
                                    for hint2 in hints[player2.name]:
                                        if len(tableCards[hint[1]]) == 0:
                                            if card.value == 1 and index in hint2[0] and card.color == hint[1]:
                                                hint[3].append(f"delayed play 2 {hint[1]}")
                                        else:
                                            if card.value == tableCards[hint[1]][-1].value -1 and index in hint2[0]:
                                                hint[3].append(f"delayed play {tableCards[hint[1]][-1].value+1} {hint[1]}")
                        if hint[2] == "value":
                            for player2 in players:
                                if player2.name == player:
                                    continue
                                for index, card in enumerate(player2.hand):
                                    for hint2 in hints[player2.name]:
                                        if len(tableCards[card.color]) == 0:
                                            if card.value == 1 and index in hint2[0] and hint[1] == 2:
                                                hint[3].append(f"delayed play 2 {card.color}")
                                        else:
                                            if card.value == tableCards[card.color][-1].value -1 and index in hint2[0] and hint[1] == card.value + 1:
                                                hint[3].append(f"delayed play {tableCards[card.color][-1].value+1} {card.color}")
         

def multi_focus_play(current_player, players, hints, discardPile, tableCards):
    """Function used to suggest a playable card which is multi focus"""
    try:
        if len(players) == 2:
            action = "" 
            for player in players:
                if current_player == player:
                    continue
                possible_hints = get_hintable_cards(player.name,players, hints)
                if possible_hints == "full chop":
                    continue
                for candidate in possible_hints:
                    if candidate == possible_hints[0]: #Not consider the chop
                        continue
                    flag = "default"
                    if len(tableCards[player.hand[candidate].color]) == 0:
                        if player.hand[candidate].value == 1:
                            for index, card in enumerate(player.hand):
                    
                                if card.id == player.hand[candidate].id:
                                    continue
                                #if card.color == player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                #    flag = "same card"
                                #    break
                                if card.value != 1 and (index > candidate or index == possible_hints[0]) and card.color == player.hand[candidate].color:
                                    if flag== "not value":
                                        flag = "break"
                                        break
                                    flag = "not color"
                                    
                                if card.color != player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                    if flag == "not color":
                                        flag = "break"
                                        break
                                    flag = "not value"
                                #if (card.color == player.hand[candidate].color or card.value == player.hand[candidate].value) and index==possible_hints[0]:
                                #    flag="break"
                                #    break
                            if flag=="break":
                                continue
                            if flag == "not color":
                                flag = "value"
                            else:
                                flag = "color"
                        if flag=="color": 
                            flag_other_hints = True
                            for player2 in players:
                                
                                for hint in hints[player2.name]:
                                    for info in hint[3]:
                                        if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                            #print("CHECK REDUNDANT COLOR MULTI")
                                            #print(candidate, card.color, card.value, hint)
                                            flag_other_hints = False
                            if flag_other_hints == True:
                                action = f"hint color {player.name} {player.hand[candidate].color}"
                                return action
                        elif flag=="value":
                             flag_other_hints = True
                             for player2 in players:
                                 if player2.name == current_player:
                                     for hint in hints[player2.name]:
                                         for info in hint[3]:
                                             if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                 if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                     #print("CHECK REDUNDANT VALUE SELF MULTI")
                                                     #print(candidate, card.color, card.value, hint)
                                                     flag_other_hints = False
                                 elif player2.name != current_player:
                                     for index2, card2 in enumerate(player2.hand):
                                             for hint in hints[player2.name]:
                                                 if index2 in hint[0]:
                                                     if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                         #print("CHECK REDUNDANT VALUE MULTI")
                                                         #print(candidate, card.color, card.value, hint)
                                                         flag_other_hints = False
                             if flag_other_hints == True and candidate != get_chop_index(player.name, players, hints):
                                 action = f"hint value {player.name} {player.hand[candidate].value}"
                                 return action
                             
                    elif len(tableCards[player.hand[candidate].color]) != 0:
                        if player.hand[candidate].value == tableCards[player.hand[candidate].color][-1].value+ 1:
                            for index, card in enumerate(player.hand):
                                if card.id == player.hand[candidate].id:
                                    continue
                                #if card.color == player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                #    flag = "same card"
                                #    break
                                if card.value != player.hand[candidate].value and (index > candidate or index == possible_hints[0]) and card.color == player.hand[candidate].color:
                                    if flag == "not value":
                                        flag = "break"
                                        break
                                    flag = "not color"
                                    
                                if card.color != player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                    if flag == "not color":
                                        flag = "break"
                                        break
                                    flag = "not value"
                                #if (card.color == player.hand[candidate].color or card.value == player.hand[candidate].value) and index==possible_hints[0]:
                                #    flag="break"
                                #    break
                            if flag == "break":
                                continue
                            if flag == "not color":
                                flag = "value"
                            else:
                                flag = "color"
                                    
                        if flag=="color": 
                            flag_other_hints = True
                            for player2 in players:
                                for hint in hints[player2.name]:
                                    for info in hint[3]:
                                        if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                            #print("CHECK REDUNDANT COLOR")
                                            #print(candidate)
                                            flag_other_hints = False
                            if flag_other_hints == True:
                                action = f"hint color {player.name} {player.hand[candidate].color}"
                                return action
                        elif flag=="value":
                             flag_other_hints = True
                             for player2 in players:
                                 if player2.name == current_player:
                                     for hint in hints[player2.name]:
                                         for info in hint[3]:
                                             if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                 if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                     #print("CHECK REDUNDANT VALUE SELF")
                                                     #print(candidate)
                                                     flag_other_hints = False
                                 elif player2.name != current_player:
                                     for index2, card2 in enumerate(player2.hand):
                                             for hint in hints[player2.name]:
                                                 if index2 in hint[0] :
                                                     if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                         #print("CHECK REDUNDANT VALUE")
                                                         #print(candidate)
                                                         flag_other_hints = False
                             if flag_other_hints == True and candidate != get_chop_index(player.name, players, hints):
                                 action = f"hint value {player.name} {player.hand[candidate].value}"
                                 return action
        elif len(players) > 2:
            action = "" 
            for player in players:
                if current_player == player:
                    continue
                possible_hints = get_hintable_cards(player.name,players, hints)
                if possible_hints == "full chop":
                    continue
                for candidate in possible_hints:
                    if candidate == possible_hints[0]: #Not consider the chop
                        continue
                    flag = "default"
                    if len(tableCards[player.hand[candidate].color]) == 0:
                        if player.hand[candidate].value == 1:
                            for index, card in enumerate(player.hand):
                    
                                if card.id == player.hand[candidate].id:
                                    continue
                                #if card.color == player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                #    flag = "same card"
                                #    break
                                if card.value != 1 and (index > candidate or index == possible_hints[0]) and card.color == player.hand[candidate].color:
                                    if flag== "not value":
                                        flag = "break"
                                        break
                                    flag = "not color"
                                    
                                if card.color != player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                    if flag == "not color":
                                        flag = "break"
                                        break
                                    flag = "not value"
                                #if (card.color == player.hand[candidate].color or card.value == player.hand[candidate].value) and index==possible_hints[0]:
                                #    flag="break"
                                #    break
                            if flag=="break":
                                continue
                            if flag == "not color":
                                flag = "value"
                            else:
                                flag = "color"
                        if flag=="color": 
                            flag_other_hints = True
                            for player2 in players:
                                
                                for hint in hints[player2.name]:
                                    for info in hint[3]:
                                        if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                            #print("CHECK REDUNDANT COLOR MULTI")
                                            #print(candidate, card.color, card.value, hint)
                                            flag_other_hints = False
                            if flag_other_hints == True:
                                action = f"hint color {player.name} {player.hand[candidate].color}"
                                return action
                        elif flag=="value":
                             flag_other_hints = True
                             for player2 in players:
                                 if player2.name == current_player:
                                     for hint in hints[player2.name]:
                                         for info in hint[3]:
                                             if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                 if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                     #print("CHECK REDUNDANT VALUE SELF MULTI")
                                                     #print(candidate, card.color, card.value, hint)
                                                     flag_other_hints = False
                                 elif player2.name != current_player:
                                     for index2, card2 in enumerate(player2.hand):
                                             for hint in hints[player2.name]:
                                                 if index2 in hint[0]:
                                                     if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                         #print("CHECK REDUNDANT VALUE MULTI")
                                                         #print(candidate, card.color, card.value, hint)
                                                         flag_other_hints = False
                             if flag_other_hints == True and candidate != get_chop_index(player.name, players, hints):
                                 action = f"hint value {player.name} {player.hand[candidate].value}"
                                 return action
                             
                    elif len(tableCards[player.hand[candidate].color]) != 0:
                        if player.hand[candidate].value == tableCards[player.hand[candidate].color][-1].value+ 1:
                            for index, card in enumerate(player.hand):
                                if card.id == player.hand[candidate].id:
                                    continue
                                #if card.color == player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                #    flag = "same card"
                                #    break
                                if card.value != player.hand[candidate].value and (index > candidate or index == possible_hints[0]) and card.color == player.hand[candidate].color:
                                    if flag == "not value":
                                        flag = "break"
                                        break
                                    flag = "not color"
                                    
                                if card.color != player.hand[candidate].color and (index > candidate or index == possible_hints[0]) and card.value == player.hand[candidate].value:
                                    if flag == "not color":
                                        flag = "break"
                                        break
                                    flag = "not value"
                                #if (card.color == player.hand[candidate].color or card.value == player.hand[candidate].value) and index==possible_hints[0]:
                                #    flag="break"
                                #    break
                            if flag == "break":
                                continue
                            if flag == "not color":
                                flag = "value"
                            else:
                                flag = "color"
                                    
                        if flag=="color": 
                            flag_other_hints = True
                            for player2 in players:
                                for hint in hints[player2.name]:
                                    for info in hint[3]:
                                        if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play") and int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                            #print("CHECK REDUNDANT COLOR")
                                            #print(candidate)
                                            flag_other_hints = False
                            if flag_other_hints == True:
                                action = f"hint color {player.name} {player.hand[candidate].color}"
                                return action
                        elif flag=="value":
                             flag_other_hints = True
                             for player2 in players:
                                 if player2.name == current_player:
                                     for hint in hints[player2.name]:
                                         for info in hint[3]:
                                             if (info.split(" ")[0] == "certain" or info.split(" ")[0] == "play"):
                                                 if int(info.split(" ")[2]) == player.hand[candidate].value and info.split(" ")[3] == player.hand[candidate].color:
                                                     #print("CHECK REDUNDANT VALUE SELF")
                                                     #print(candidate)
                                                     flag_other_hints = False
                                 elif player2.name != current_player:
                                     for index2, card2 in enumerate(player2.hand):
                                             for hint in hints[player2.name]:
                                                 if index2 in hint[0] :
                                                     if card2.value == player.hand[candidate].value and card2.color == player.hand[candidate].color:
                                                         #print("CHECK REDUNDANT VALUE")
                                                         #print(candidate)
                                                         flag_other_hints = False
                             if flag_other_hints == True and candidate != get_chop_index(player.name, players, hints):
                                 action = f"hint value {player.name} {player.hand[candidate].value}"
                                 return action
    except:
        return False
    return False              
                    
def fake_save_turn(current_player, players, hints, tableCards, fake_hint):
    """Desperate moves used when there are no feasible moves and the discard is impossible"""
    flag_no_hint = True
    for player in hints:
        if player==current_player:
            continue
        if len(hints[player]) != 0:
            flag_no_hint = False
    if flag_no_hint == False: #Hint available
        for player in players:
            for index, card in enumerate(player.hand):
                #Check hints 
                for hint in hints[player.name]:
                    for info in hint[3]:
                        #print(info)
                        if index in hint[0] and (info.split(" ")[0] == "delayed" or info.split(" ")[0] == "save" or info.split(" ")[0] == "keep"):
                            type_hint = hint[2]
                            #Give an additional hint to clarify
                            #It will be merged by update hints
                            if type_hint == "color":
                                flag_other_hints = False
                                for player2 in players:
                                    if player2.name == player.name:
                                        continue
                                    if player2.name == current_player:
                                        for hint2 in hints[player2.name]:
                                            if hint2[1] == hint[1]:
                                                flag_other_hints = True
                                    elif player2.name != current_player:
                                        for index2, card2 in enumerate(player2.hand):
                                            for hint2 in hints[player2.name]:
                                                if index2 in hint2[0] and card2.value == card.value and card2.color == card.color:
                                                    flag_other_hints = True
                                                    print("FLAG_OTHER_HINTS COLOR")
                                if flag_other_hints == False:
                                    action = f"hint value {player.name} {card.value}"
                                    return action
                            elif type_hint == "value":  
                                flag_other_hints = False
                                for player2 in players:
                                    if player2.name == player.name:
                                        continue
                                    if player2.name == current_player:
                                        for hint2 in hints[player2.name]:
                                            if hint2[1] == hint[1]:
                                                flag_other_hints = True
                                    elif player2.name != current_player:
                                        for index2, card2 in enumerate(player2.hand):
                                            for hint2 in hints[player2.name]:
                                                if index2 in hint2[0] and card2.value == card.value and card2.color == card.color:
                                                    flag_other_hints = True
                                                    #print("FLAG_OTHER_HINTS VALUE")
                                if flag_other_hints == False:
                                    action = f"hint color {player.name} {card.color}"
                                    return action 
    if fake_hint==True:
        for player in players:
            if player.name == current_player:
                continue    
            #SHOULD APPEND A "FAKE SAVE"
            try:
                action = f"hint value {player.name} {player.hand[get_chop_index(player.name, players, hints)].value}"
            except:
                action = f"hint value {player.name} {player.hand[-1].value}"
            return action
    return False
    

def play_certain(current_player, hints, tableCards, discardPile, available_tokens):
    """Function used to detect the need to use certain cards"""
    #print("SONO SU PLAY CERTAIN")
    for hint in hints[current_player]:
        flag_critical = False
        if hint[3][0].split(" ")[0] == "certain":
            if len(tableCards[hint[3][0].split(" ")[3]]) != 0:
                if tableCards[hint[3][0].split(" ")[3]][-1].value == int(hint[3][0].split(" ")[2]) -1:
                    action = f"play {hint[0][0]}"
                    return action
                if tableCards[hint[3][0].split(" ")[3]][-1].value >= int(hint[3][0].split(" ")[2]) and available_tokens != 0:
                    action = f"discard {hint[0][0]}"
                    return action
                if tableCards[hint[3][0].split(" ")[3]][-1].value < int(hint[3][0].split(" ")[2]) - 1 and available_tokens != 0: #Not immediately useful, check if should discard
                    counter_one = 0
                    #print("HARD DISCARD")
                    #print(hint[3][0].split(" ")[2])
                    if int(hint[3][0].split(" ")[2]) != 5:
                        for card in discardPile:
                            print(card.value, card.color)
                            if card.value == int(hint[3][0].split(" ")[2]) and card.color == hint[3][0].split(" ")[3] and hint[3][0].split(" ")[2] != 1:
                                print("FLAG CRITICAL TRUE")
                                flag_critical = True
                            if card.value == int(hint[3][0].split(" ")[2]) and card.color == hint[3][0].split(" ")[3] and hint[3][0].split(" ")[2] == 1:
                                counter_one += 1
                                if counter_one == 2:
                                    flag_critical = True
                        if flag_critical == False:
                            action = f"discard {hint[0][0]}"
                            return action 
                        
            if len(tableCards[hint[3][0].split(" ")[3]]) == 0:
                if 1 == int(hint[3][0].split(" ")[2]):
                    action = f"play {hint[0][0]}"
                    return action
                if 1 != int(hint[3][0].split(" ")[2]) and available_tokens != 0:
                    #print("HARD DISCARD ONE")
                    if int(hint[3][0].split(" ")[2]) != 5:
                        for card in discardPile:
                            if card.value == int(hint[3][0].split(" ")[2]) and card.color == hint[3][0].split(" ")[3] and hint[3][0].split(" ")[2] != 1:
                                flag_critical = True
                                
                        if flag_critical == False:
                            action = f"discard {hint[0][0]}"
                            return action                 
    return False

def manage_full_chop(current_player,players, hints, available_tokens):
    """Function used to manage the chop when all cards are hinted"""
    possible_hints = get_hintable_cards(current_player,players, hints)
    if possible_hints == "full chop":
        #print("HANDLING FULL CHOP")
        if available_tokens != 0:
            for hint in hints[current_player]:
                if hint[2] == "value" and hint[1] != 5: #Easy handle for now
                    action = f"discard {hint[0][0]}"
                    return action
                if hint[2] == "color":
                    action = f"discard {hint[0][0]}"
                    return action
            for hint in hints[current_player]:
                if hint[2] == "value" and hint[1] == 5: #Easy handle for now
                    action = f"discard {hint[0][0]}"
                    return action
                if hint[2] == "color":
                    action = f"discard {hint[0][0]}"
                    return action
                
    return "discard 0"

def discard_until_critical(current_player, hints, discardPile, tableCards):
    for hint in hints[current_player]:
        if hint[2] == "value":
            flag_critical = False
            if hint[3][0].split(" ")[0] == "save" and hint[1] != 5:
                #Check discard pile 
                for card in discardPile:
                    if card.value == hint[1]:
                        flag_critical = True
                if flag_critical == False:
                    action = f"discard {hint[0][0]}"
                    #print("DISCARD UNTIL CRIT")
                    return action
    return False


def search_delayed_play_hint(current_player, players, hints, discardPile, tableCards):
    for index, player in enumerate(players): #Player that will receive the hint
        if player.name == current_player:
            continue
        for index2, card in enumerate(player.hand):          
            for index3, player2 in enumerate(players): #Player with the already available hint
                if player2.name == player.name:
                    continue
                if player2.name != current_player:
                    for index4, card2 in enumerate(player2.hand):
                        for hint in hints[player2.name]:
                            #Hint is playable?
                            print(hint)
                            print("ENTERING DELAYED")
                            if len(tableCards[card2.color]) != 0:
                                if len(hint[3]) == 1:
                                    if hint[3][0].split(" ")[0] =="play" and index4 in hint[0] and card2.value == tableCards[card2.color][-1].value + 1:
                                        if card.value == card2.value + 1 and card.color == card2.color:
                                            flag = "default"
                                            for index5, card3 in enumerate(player.hand):
                                                if index2 == index5:
                                                    continue
                                                #Possible candidate: let's check if hintable
                                                if (index5 > index2 or index5 == get_hintable_cards(player.name, players, hints)[0]) and card.color == card3.color:
                                                    if flag=="color":
                                                        flag="break"
                                                        break
                                                    flag = "value"
                                                elif (index5 > index2 or index5 == get_hintable_cards(player.name, players, hints)[0]) and card.value == card3.value:
                                                    if flag=="value":
                                                        flag="break"
                                                        break
                                                    flag = "color"
                                            if flag == "break":
                                                break #Next hint
                                            if flag=="value":
                                                print("DELAYED HAPPENED")
                                                action = f"hint {player.name} value {card.value}"
                                                return action
                                            if flag=="color" or flag=="default":
                                                print("DELAYED HAPPENED")
                                                action = f"hint {player.name} color {card.color}"
                                                return action
                            elif len(tableCards[card2.color]) == 0:
                                if len(hint[3]) == 1:
                                    if hint[3][0].split(" ")[0] =="play" and index4 in hint[0] and card2.value == 1:
                                        if card.value == card2.value + 1 and card.color == card2.color:
                                            flag = "default"
                                            for index5, card3 in enumerate(player.hand):
                                                if index2 == index5:
                                                    continue
                                                #Possible candidate: let's check if hintable
                                                if (index5 > index2 or index5 == get_hintable_cards(player.name, players, hints)[0]) and card.color == card3.color:
                                                    if flag=="color":
                                                        flag="break"
                                                        break
                                                    flag = "value"
                                                elif (index5 > index2 or index5 == get_hintable_cards(player.name, players, hints)[0]) and card.value == card3.value:
                                                    if flag=="value":
                                                        flag="break"
                                                        break
                                                    flag = "color"
                                            if flag == "break":
                                                break #Next hint
                                            if flag=="value":
                                                print("DELAYED HAPPENED")
                                                action = f"hint {player.name} value {card.value}"
                                                return action
                                            if flag=="color" or flag=="default":
                                                print("DELAYED HAPPENED")
                                                action = f"hint {player.name} color {card.color}"
                                                return action
                elif player2.name == current_player:
                    continue        
    return False
                        
                