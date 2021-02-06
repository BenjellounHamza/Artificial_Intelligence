#!/usr/bin/env python3
import random
from math import inf, sqrt
from fishing_game_core.game_tree import Node, compute_caught_fish
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

# def distance(node, player):
#     d = inf
#     coefs = []
#     for i in node.state.get_fish_positions().keys():
#         if(i not in [node.state.get_caught()[1 - player]]):
#             coef = node.state.get_fish_scores()[i]
#             coefs.append(coef)
#             if(coef > 0):
#                 player_position = node.state.get_hook_positions()[player]
#                 opponent_position = node.state.get_hook_positions()[1 - player]
#                 distance = distance_basique(player_position, opponent_position, node.state.get_fish_positions()[i])*coef
#                 if(d >  distance):
#                     d = distance
#         #elif(len(node.state.get_fish_positions().keys()) == 1):
#         #    return sqrt((20 - (pt2_x - pt1_x))**2 + (pt1_y - pt2_y)**2) + (20 - node.state.get_hook_positions()[player][1])
#     if(d == inf):
#         for i in node.state.get_fish_positions().keys():
#             coef = node.state.get_fish_scores()[i]
#             if(0 >= coef):
#                 coefs.append(coef)
#                 player_position = node.state.get_hook_positions()[player]
#                 opponent_position = node.state.get_hook_positions()[1 - player]
#                 distance = distance_basique(player_position, opponent_position, node.state.get_fish_positions()[i])*-coef + (20 - node.state.get_hook_positions()[player][1])
#                 if(d > distance):
#                     d = distance
#         if(len(coefs) != 0):
#             return d/sum(coefs)
#         else:
#             return inf
#     if(len(coefs) != 0):
#         return d/sum(coefs)
#     else:
#         return d

def distance_basique(player_position, opponent_position, fish_position):
    pt1_x, pt1_y = player_position
    pt2_x, pt2_y = opponent_position
    if pt2_x > min(pt1_x, fish_position[0]) and max(pt1_x, fish_position[0]) > pt2_x:
        deltax = 20 - abs(fish_position[0] - pt1_x)
    else:
        deltax = fish_position[0] - pt1_x
    return sqrt(deltax**2 + (fish_position[1] - pt1_y)**2) + (20 - fish_position[1])


def distance(node, player):
    distance = 0
    for i in node.state.get_fish_positions().keys():
        if(i not in [node.state.get_caught()[1 - player]]):
            coef = node.state.get_fish_scores()[i]
            player_position = node.state.get_hook_positions()[player]
            opponent_position = node.state.get_hook_positions()[1 - player]
            fish_position = node.state.get_fish_positions()[i]
            d = distance_basique(player_position, opponent_position, fish_position)
            if(d != 0):
                d = coef/d
            else:
                d = 30*coef
            if(d > distance):
                distance = d
    return distance

def heuristic(node):
    score0, score1 = node.state.get_player_scores()
    d1 = distance(node, 0)
    d2 = distance(node, 1)
    return (d1 - d2) + 30*(score0 - score1)
def heuristic1(node):
    score0, score1 = node.state.get_player_scores()
    return (score0 - score1)
def alphabeta(node, depth, alpha, beta, player):
    if (depth == 0):
        v = heuristic(node)
    else:
        childs = node.compute_and_get_children()
        ordred = [(child, heuristic(child)) for child in childs]
        ordred = sorted(ordred , key=lambda child: child[1], reverse=True)
        #ordred = childs
        if player == 0:
            v = -inf
            for child in ordred:
                v = max(v, alphabeta(child[0], depth - 1, alpha, beta, 1))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break # Beta prune
        else:
            v = inf
            for child in ordred:
                v = min(v, alphabeta(child[0], depth - 1, alpha, beta, 0))
                beta = min(beta, v)
                if beta <= alpha:
                    break # alpha prune
    node.probability = v
    return v

def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", node.probability, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)

class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)
        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)
            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3},
          'fish1': {'score': 2, 'type': 1},
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return initial_data

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!
        v = alphabeta(initial_tree_node, 4, -inf, +inf, 0)
        childs = initial_tree_node.children
        childs_value = [child.probability for child in childs]
        if(len(childs_value) == 0):
            return ACTION_TO_STR[0]
        else:
            maximum = max(childs_value)
            max_indices = [i for i in range(len(childs_value)) if childs_value[i] == maximum]
        #pprint_tree(initial_tree_node)
        return ACTION_TO_STR[random.choice(max_indices)]
