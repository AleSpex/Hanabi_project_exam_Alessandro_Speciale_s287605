# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 01:59:50 2022

@author: aless
"""
#import copy
import Rules_API



def rule_based_IA(game, currentPlayer, players, hints, handsize):
    available_tokens = game.usedNoteTokens
    Rules_API.evaluate_hint(currentPlayer, players, hints, game.tableCards, game.discardPile)
    #print(hints)
    if available_tokens < 8: #PRIORITIZE HINTS GIVING      
    #SAVE HINTS
        result_save_5 = Rules_API.search_save_hint_5(game.currentPlayer, players, hints, game.tableCards)
        if result_save_5 != False: #Need to save a 5
            #print("save 5")
            return result_save_5
        
        #result_save_2 = Rules_API.search_save_hint_2(currentPlayer, players, hints, game.discardPile, game.tableCards)
        #if result_save_2 != False: #Need to save a 2
        #    print("save 2")
        #    return result_save_2
        
        result_save_critical = Rules_API.search_save_hint_critical(currentPlayer, players, hints, game.discardPile, game.tableCards)
        if result_save_critical != False: #Need to save a critical card
            #print("save crit")
            return result_save_critical
        
        #Check certain hints
        result_play_certain = Rules_API.play_certain(currentPlayer, hints, game.tableCards, game.discardPile, available_tokens)
        if result_play_certain != False:
            #print("certain play")
            return result_play_certain
            
        if len(players) == 2:
        #EVALUATE THE SAVE PLAY / KEEP PLAY HINTS IF ANY
            flag_multi_play = True
            for hint in hints[currentPlayer]:
                if len(hint[3]) == 1: #only one possibility
                    if (hint[3][0].split(" ")[0] == "save" and hint[3][0].split(" ")[1] == "play") or (hint[3][0].split(" ")[0] == "keep" and hint[3][0].split(" ")[1] == "play"):
                        slot = hint[3][0].split(" ")[2]
                        action = f"play {slot}"
                        return action
                    elif hint[3][0].split(" ")[0] == "play":
                        slot = hint[3][0].split(" ")[1]
                        action = f"play {slot}"
                        return action
                   
            for hint in hints[currentPlayer]:
                if len(hint[3]) > 1: #More possibilities
                    #saved_part = ""
                    for parts in hint[3]:
                        if parts.split(" ")[0] != "play":
                            flag_multi_play = False
                            #saved_part = parts.split(" ")[1]
                            #break
                    if flag_multi_play == True:
                        slot = hint[3][0].split(" ")[1]
                        action = f"play {slot}"
                        return action  
        
        
        #PLAY HINTS
            result_play = Rules_API.search_play_hint(currentPlayer, players, hints, game.discardPile, game.tableCards)
            print(result_play)
            if result_play != False: #Can hint a play
                print("play hint")
                return result_play
            
        #Check multiplay hints
            multi_play = Rules_API.multi_focus_play(currentPlayer, players, hints, game.discardPile, game.tableCards)
            if multi_play != False: #Can hint a play
                #print("multi hint")
                return multi_play
            
            result_fake_save = Rules_API.fake_save_turn(currentPlayer, players, hints, game.tableCards, False)
            if result_fake_save != False:
                #print("fake save CERTAIN HINT")
                return result_fake_save
            
        elif len(players) > 2:
            #PLAY HINTS
            result_play = Rules_API.search_play_hint(currentPlayer, players, hints, game.discardPile, game.tableCards)
            #print(result_play)
            if result_play != False: #Can hint a play
                #print("play hint")
                return result_play
                
            #Check multiplay hints
            multi_play = Rules_API.multi_focus_play(currentPlayer, players, hints, game.discardPile, game.tableCards)
            if multi_play != False: #Can hint a play
                #print("multi hint")
                return multi_play
                
            #delayed_hint = Rules_API.search_delayed_play_hint(currentPlayer, players, hints, game.discardPile, game.tableCards)
            #if delayed_hint != False:
            #    print("delayed hint")
            #    return delayed_hint
                
            flag_multi_play = True
            for hint in hints[currentPlayer]:
                if len(hint[3]) == 1: #only one possibility
                    if (hint[3][0].split(" ")[0] == "save" and hint[3][0].split(" ")[1] == "play") or (hint[3][0].split(" ")[0] == "keep" and hint[3][0].split(" ")[1] == "play"):
                        slot = hint[3][0].split(" ")[2]
                        action = f"play {slot}"
                        return action
                    elif hint[3][0].split(" ")[0] == "play":
                        slot = hint[3][0].split(" ")[1]
                        action = f"play {slot}"
                        return action
                   
            for hint in hints[currentPlayer]:
                if len(hint[3]) > 1: #More possibilities
                    #saved_part = ""
                    for parts in hint[3]:
                        if parts.split(" ")[0] != "play":
                            flag_multi_play = False
                            #saved_part = parts.split(" ")[1]
                            #break
                    if flag_multi_play == True:
                        slot = hint[3][0].split(" ")[1]
                        action = f"play {slot}"
                        return action  
                    
            result_fake_save = Rules_API.fake_save_turn(currentPlayer, players, hints, game.tableCards, False)
            if result_fake_save != False:
                #print("fake save CERTAIN HINT")
                return result_fake_save
        #CHOP DISCARD
        if available_tokens != 0:
            #Check discardable cards
            for hint in hints[currentPlayer]:
                if len(hint[3]) == 1: #only one possibility
                    if (hint[3][0].split(" ")[0] == "save" and hint[3][0].split(" ")[1] == "discard") or (hint[3][0].split(" ")[0] == "keep" and hint[3][0].split(" ")[1] == "discard"): 
                        slot = hint[3][0].split(" ")[2]
                        action = f"discard {slot}"
                        #print(hints)
                        return action
            
            #Is full chop?
            full_chop_result = Rules_API.manage_full_chop(currentPlayer,players, hints, available_tokens)
            if full_chop_result != False:
                #print("full chop manage")
                return full_chop_result
            
            discard_until_crit = Rules_API.discard_until_critical(currentPlayer, hints, game.discardPile, game.tableCards)
            if discard_until_crit != False:
                #print("not useful save for now")
                return discard_until_crit
            
            result_chop_discard = Rules_API.chop_discard(currentPlayer,players, hints, handsize)
            #print("chop discard")
            return result_chop_discard
        
        else:
            result_fake_save = Rules_API.fake_save_turn(currentPlayer, players, hints, game.tableCards, True)
            #print("fake save")
            return result_fake_save
    
    if available_tokens == 8: #Let's focus on our hints and chop discards
        
        #Check certain hints
        result_play_certain = Rules_API.play_certain(currentPlayer, hints, game.tableCards, game.discardPile, available_tokens)
        if result_play_certain != False:
            #print("certain play")
            return result_play_certain
        
        flag_multi_play = True
        for hint in hints[currentPlayer]:
            if len(hint[3]) == 1: #only one possibility
                if (hint[3][0].split(" ")[0] == "save" and hint[3][0].split(" ")[1] == "play") or (hint[3][0].split(" ")[0] == "keep" and hint[3][0].split(" ")[1] == "play"):
                    slot = hint[3][0].split(" ")[2]
                    action = f"play {slot}"
                    return action
                elif hint[3][0].split(" ")[0] == "play":
                    slot = hint[3][0].split(" ")[1]
                    action = f"play {slot}"
                    return action
               
        for hint in hints[currentPlayer]:
            if len(hint[3]) > 1: #More possibilities
                #saved_part = ""
                for parts in hint[3]:
                    if parts.split(" ")[0] != "play":
                        flag_multi_play = False
                        #saved_part = parts.split(" ")[1]
                        #break
                if flag_multi_play == True:
                    slot = hint[3][0].split(" ")[1]
                    action = f"play {slot}"
                    return action  
                    
        #Is full chop?
        full_chop_result = Rules_API.manage_full_chop(currentPlayer,players, hints, available_tokens)
        #print(full_chop_result)
        if full_chop_result != False:
            print("full chop manage")
            return full_chop_result
        
        #Check discardable cards
        for hint in hints[currentPlayer]:
            if len(hint[3]) == 1: #only one possibility
                if (hint[3][0].split(" ")[0] == "save" and hint[3][0].split(" ")[1] == "discard") or (hint[3][0].split(" ")[0] == "keep" and hint[3][0].split(" ")[1] == "discard"): 
                    slot = hint[3][0].split(" ")[2]
                    action = f"discard {slot}"
                    #print(hints)
                    return action
           
        discard_until_crit = Rules_API.discard_until_critical(currentPlayer, hints, game.discardPile, game.tableCards)
        if discard_until_crit != False:
            #print("not useful save for now")
            return discard_until_crit
        
        #CHOP DISCARD
        result_chop_discard = Rules_API.chop_discard(currentPlayer,players, hints, handsize)
        #print(result_chop_discard)
        return result_chop_discard


              
                    
        
    