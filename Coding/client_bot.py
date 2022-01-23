#!/usr/bin/env python3

from sys import argv, stdout
from threading import Thread, Condition
import GameData
import socket
from constants import *
import os
import time
import TestMethods3
import Rules_API
import numpy as np


INFINITE_PLAY = True


# PROBLEM: the AI should know what hints the other players have in order to avoid repeating a hint
players = list()
current_player_index = 0

scores = list()

showed = False
started = False

if len(argv) < 4:
    print("You need the player name to start the game.")
    #exit(-1)
    playerName = f"Test{np.random.randint(300000)}" # For debug
    ip = HOST
    port = PORT
else:
    playerName = argv[3]
    ip = argv[1]
    port = int(argv[2])

run = True

statuses = ["Lobby", "Game", "GameHint", "Showed"]

game_state = None

status = statuses[0]

hintState = ("", "")

def initialize_hints_dict(players):
    hints = {}
    for p in players:
        hints[p] = []
    return hints

#Function to save hints in a dictionary (key: player with the hint, value: hints data)
def memorize_hint(hint_dict, player, cards_index, hint_content, hint_type, players):
    chop = Rules_API.get_chop_index(player, players, hint_dict)
    #print(chop)
    #print("SONO MEMORIZE HINT")
    for hint in hint_dict[player]:
        if len(hint[3]) != 0:
            #print(hint)
            if len(hint[0]) == 1:
                if hint[3][0].split(" ")[0] == "certain" and hint[0][0] in cards_index:
                    cards_index.remove(hint[0][0])
            elif len(hint[0]) > 1:
                for position in hint[0]:
                    if hint[3][0].split(" ")[0] == "certain" and position in cards_index:
                        cards_index.remove(position)  
    
    if len(cards_index) ==1: 
        #print(chop)
        #print("TESTING IMMEDIATE SAVE")
        if chop in cards_index and hint_type == "value":
            #print("CHOPPING")
            hint_dict[player].append([cards_index, hint_content, hint_type, [f"save {hint_content}"], ""])
        else:
            hint_dict[player].append([cards_index, hint_content, hint_type, [], ""])
    elif len(cards_index) >1:
        if chop in cards_index and hint_type == "value":
            #print("CHOPPING")
            hint_dict[player].append([cards_index, hint_content, hint_type, [f"save {hint_content}"], f"focus {chop}"])
        elif chop in cards_index:
            hint_dict[player].append([cards_index, hint_content, hint_type, [], f"focus {chop}"])
        else:
            hint_dict[player].append([cards_index, hint_content, hint_type, [], f"focus {cards_index[-1]}"])
            
def update_hint(hint_dict, player, card_index):
    for index, hint in enumerate(hint_dict[player]):
        positions = hint[0]
        #print("SONO DENTRO UPDATE HINT")
        if card_index in hint[0]:
            hint[3] = []
            hint[3].append(f"keep {hint[1]}")
        if len(positions) == 1:
            if card_index in positions:
                #print(index)
                
                hint_dict[player][index][1] = "to remove"
            if card_index not in positions:
                if positions[0] > card_index:
                    positions[0] -= 1
        if len(positions) > 1:
            for index, position in enumerate(positions):
                if position == card_index:
                    positions[index] = None
                    if hint[4] != "":
                        hint[4] = ""
                elif position > card_index:
                    position -= 1
                    positions[index] = position
            if hint[4] != "" and int(hint[4].split(" ")[1]) > card_index:
                new_focus = int(hint[4].split(" ")[1]) - 1
                hint[4] = f"focus {new_focus}"
            hint[0] = [position for position in positions if position != None]

    hint_dict[player] = [hint for hint in hint_dict[player] if hint[1] != "to remove"]  
        
                
def merge_hint(hint_dict, player):
    #print(hint_dict)
    #Merging: if two hints are overlapping, defining the card, it will be clarified
    for index, hint in enumerate(hint_dict[player]):
        if hint[4] != "to remove":
            for index2, hint2 in enumerate(hint_dict[player]):
                #flag_save = False
                if index >= index2: #Not consider already considered couples
                    continue
                
                if (hint[2] == "value" and hint2[2] == "color") or(hint2[2] == "value" and hint[2] == "color"):
                    #print("INSIDE MERGING")
                    #print(hint)
                    #print(hint2)
                    intersection = [position for position in hint[0] if position in hint2[0]]
                    if len(intersection) != 0:
                        #Create a new "certain" hint and remove the old positions
                        hint_data = (intersection, hint[1], hint2[1])
                        if len(hint[0]) == 1 or len(hint2[0]) == 1:
                            if len(hint[0]) == 1:
                                #print(hint)
                                #print("REMOVING 1^")
                                hint[4] = "to remove"
                            if len(hint2[0]) == 1:
                                #print(hint2)
                                #print("REMOVING 2^")
                                hint2[4] = "to remove"
                        if len(hint[0]) > 1 or len(hint2[0]) > 1:
                            if len(hint[0]) > 1:
                                hint[0] = [position for position in hint[0] if position not in intersection]
                                if len(hint[0]) == 0:
                                    hint[4] = "to remove"
                                hint[3] = []
                                hint[3].append(f"keep {hint[1]}")   
                            if len(hint2[0]) > 1:
                                hint2[0] = [position for position in hint2[0] if position not in intersection]
                                if len(hint2[0]) == 0:
                                    hint2[4] = "to remove"
                                hint2[3] = []
                                hint2[3].append(f"keep {hint2[1]}")
                            
                        if hint[2] == "value":
                            if len(intersection) == 1:
                                hint_dict[player].append([hint_data[0], None, None, [f"certain play {hint_data[1]} {hint_data[2]}"], ""])
                            else:
                                hint_dict[player].append([hint_data[0], None, None, [f"certain play {hint_data[1]} {hint_data[2]}"], f"focus {hint_data[0][-1]}"])
                        if hint[2] == "color":
                            if len(intersection) == 1:
                                hint_dict[player].append([hint_data[0], None, None, [f"certain play {hint_data[2]} {hint_data[1]}"], ""])
                            else:
                                hint_dict[player].append([hint_data[0], None, None, [f"certain play {hint_data[2]} {hint_data[1]}"], f"focus {hint_data[0][-1]}"])
            #if False:        
                if (hint[2] == "value" and hint2[2] == "value") or(hint2[2] == "color" and hint[2] == "color"):
                    intersection = [position for position in hint[0] if position in hint2[0]]
                    if len(intersection) != 0:
                        hint_data = ""
                        if len(hint[0]) >= len(hint2[0]):
                            #print(hint2)
                            #print("REMOVING 3^")
                            hint[3] = []
                            hint[3] = hint2[3]
                            hint_dict[player].remove(hint2)
                        elif len(hint[0]) < len(hint2[0]):
                            hint2[3] = []
                            hint2[3] = hint[3]
                            #print(hint)
                            #print("REMOVING 4^")
                            hint_dict[player].remove(hint)
                    
    hint_dict[player] = [hint for hint in hint_dict[player] if hint[4] != "to remove"]    

def decide(cv):
    global status
    global game_state
    global showed

    if status == statuses[0]:
        return 'ready'
    elif status == statuses[1]:
        cv.acquire()
        while (not started or players[current_player_index] != playerName or showed) and run:
            cv.wait()
        status = statuses[3]
        cv.release()
        return 'show'

    elif status == statuses[3]: # game state retrieved
        cv.acquire()
        while not showed:
            cv.wait()
        status = statuses[1]
        cv.release()

        # INSERT MOVES HERE
        action = TestMethods3.rule_based_IA(game_state, playerName, game_state.players, hints, game_state.handSize)
        print(action)
        return action


def manageInput(cv):
    global run
    global started
    global status
    while run:
        command = decide(cv)
        if run:
            # Choose data to send
            if command == "exit":
                run = False
                os._exit(0)
            elif command == "ready" and status == statuses[0]:
                s.send(GameData.ClientPlayerStartRequest(playerName).serialize())
                status = statuses[1]
            elif command == "show":
                s.send(GameData.ClientGetGameStateRequest(playerName).serialize())
            elif command.split(" ")[0] == "discard":
                try:
                    cardStr = command.split(" ")
                    cardOrder = int(cardStr[1])
                    s.send(GameData.ClientPlayerDiscardCardRequest(playerName, cardOrder).serialize())
                except:
                    print("Maybe you wanted to type 'discard <num>'?")
                    continue
            elif command.split(" ")[0] == "play":
                try:
                    cardStr = command.split(" ")
                    cardOrder = int(cardStr[1])
                    s.send(GameData.ClientPlayerPlayCardRequest(playerName, cardOrder).serialize())
                except:
                    print("Maybe you wanted to type 'play <num>'?")
                    continue
            elif command.split(" ")[0] == "hint":
                try:
                    destination = command.split(" ")[2]
                    t = command.split(" ")[1].lower()
                    if t != "colour" and t != "color" and t != "value":
                        print("Error: type can be 'color' or 'value'")
                        continue
                    value = command.split(" ")[3].lower()
                    if t == "value":
                        value = int(value)
                        if int(value) > 5 or int(value) < 1:
                            print("Error: card values can range from 1 to 5")
                            continue
                    else:
                        if value not in ["green", "red", "blue", "yellow", "white"]:
                            print("Error: card color can only be green, red, blue, yellow or white")
                            continue
                    s.send(GameData.ClientHintData(playerName, destination, t, value).serialize())
                except:
                    print("Maybe you wanted to type 'hint <type> <destinatary> <value>'?")
                    continue
            elif command == "":
                print("[" + playerName + " - " + status + "]: ", end="")
            else:
                print("Unknown command: " + command)
                continue
            stdout.flush()

def print_state(data):
    print("Current player: " + data.currentPlayer)
    print("Player hands: ")
    for p in data.players:
        print(p.toClientString())
    print("Cards in your hand: " + str(data.handSize))
    print("Table cards: ")
    for pos in data.tableCards:
        print(pos + ": [ ")
        for c in data.tableCards[pos]:
            print(c.toClientString() + " ")
        print("]")
    print("Discard pile: ")
    for c in data.discardPile:
        print("\t" + c.toClientString())            
    print("Note tokens used: " + str(data.usedNoteTokens) + "/8")
    print("Storm tokens used: " + str(data.usedStormTokens) + "/3")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    request = GameData.ClientPlayerAddData(playerName)
    s.connect((HOST, PORT))
    s.send(request.serialize())
    data = s.recv(DATASIZE)
    data = GameData.GameData.deserialize(data)
    if type(data) is GameData.ServerPlayerConnectionOk:
        print("Connection accepted by the server. Welcome " + playerName)
    print("[" + playerName + " - " + status + "]: ", end="")
    cv = Condition() # create the condition variable
    t = Thread(target=manageInput, args=(cv,))
    t.start()
    while run:
        dataOk = False
        data = s.recv(DATASIZE)
        if not data:
            continue
        data = GameData.GameData.deserialize(data)
        if type(data) is GameData.ServerPlayerStartRequestAccepted:
            dataOk = True
            print("Ready: " + str(data.acceptedStartRequests) + "/"  + str(data.connectedPlayers) + " players")
            data = s.recv(DATASIZE)
            data = GameData.GameData.deserialize(data)
        if type(data) is GameData.ServerStartGameData:
            dataOk = True
            print("Game start!")
            s.send(GameData.ClientPlayerReadyData(playerName).serialize())
            players = data.players
            hints = initialize_hints_dict(players)
            hints_id = 0
            cv.acquire()
            status = statuses[1]
            started = True
            showed = False
            cv.notify()
            cv.release()
        if type(data) is GameData.ServerGameStateData:
            dataOk = True
            game_state = data
            cv.acquire()
            showed = True
            cv.notify()
            cv.release()
            print_state(data)
        if type(data) is GameData.ServerActionInvalid:
            dataOk = True
            print("Invalid action performed. Reason:")
            print(data.message)
        if type(data) is GameData.ServerActionValid:
            dataOk = True
        
            #HINT UPDATING
            #print(hints)
            update_hint(hints, data.lastPlayer, data.cardHandIndex)
            #print(hints)
            
            print("Action valid!")
            print("Current player: " + data.player)
            cv.acquire()
            current_player_index = (current_player_index + 1) % len(players)
            showed = False
            cv.notify()
            cv.release()
        if type(data) is GameData.ServerPlayerMoveOk:
            dataOk = True
            #print(data.lastPlayer)
            #print(hints)
            
            update_hint(hints, data.lastPlayer, data.cardHandIndex)
            
            #print(hints)
            
            print("Nice move!")
            
            #HINT UPDATING
            
            
            print("Current player: " + data.player)
            cv.acquire()
            current_player_index = (current_player_index + 1) % len(players)
            showed = False
            cv.notify()
            cv.release()
        if type(data) is GameData.ServerPlayerThunderStrike:
            dataOk = True
            
            #HINT UPDATING
            #print(hints)
            update_hint(hints, data.lastPlayer, data.cardHandIndex)
            #print(hints)
            
            print("OH NO! The Gods are unhappy with you!")
            cv.acquire()
            current_player_index = (current_player_index + 1) % len(players)
            showed = False
            cv.notify()
            cv.release()
        if type(data) is GameData.ServerHintData:
            dataOk = True
            
            #HINT MEMORIZATION (NAMES ARE KEY)
            memorize_hint(hints, data.destination, data.positions, data.value, data.type, players)
            
            #HINT MERGING
            merge_hint(hints, data.destination)
            
            print("Hint type: " + data.type)
            print("Player " + data.destination + " cards with value " + str(data.value) + " are:")
            for i in data.positions:
                print("\t" + str(i))
          
            cv.acquire()
            current_player_index = (current_player_index + 1) % len(players)
            showed = False
            cv.notify()
            cv.release()
        if type(data) is GameData.ServerInvalidDataReceived:
            dataOk = True
            print(data.data)
        if type(data) is GameData.ServerGameOver:
            cv.acquire()
            run = False
            cv.notify()
            cv.release()
            t.join()
            dataOk = True
            print(data.message)
            print(data.score)
            print(data.scoreMessage)
            stdout.flush()
            if INFINITE_PLAY:
                scores.append(data.score)
                print(f'Scores history: {scores}')
                print(f'Avg score over {len(scores)} matches: {round(sum(scores)/len(scores), 2)}')
                if len(scores) == 1000:
                    break
                run = True
                print("Ready for a new game!")
                # reinitialize
                status = statuses[1]
                current_player_index = 0
                showed = False
                hints = initialize_hints_dict(players)
                t = Thread(target=manageInput, args=(cv,))
                t.start()
        if not dataOk:
            print("Unknown or unimplemented data type: " +  str(type(data)))
        print("[" + playerName + " - " + status + "]: ", end="")
        #os.system("ready")
        stdout.flush()
        