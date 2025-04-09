import numpy
from ai_multi_layer import NeuralNetwork_multiLayer as AI

nodes = [20, 30, 25, 15, 1]
#       dist last cycle
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration
#       dist b4 that
#       corresponding turn ration

turn_ratios = [100, 100, 90, 80, 70, 60, 50, 40, 30, 20]
def get_turn_ratio_input(turn_ratios):
    adjusted_turn_ratio = []
    for ratio in turn_ratios:
        input_turn_ratio = ratio/100
        if input_turn_ratio >= 0.99:
            input_turn_ratio = 0.99
        elif input_turn_ratio <= 0.01:
            input_turn_ratio = 0.01
        adjusted_turn_ratio.append(input_turn_ratio)
    return adjusted_turn_ratio

last_dists = [20, 19, 18, 17, 16, 13, 10, 7, 5, 1]
def get_adjusted_dists(last_dists):
    last_dists_adjusted = []
    for dist in last_dists:
        a_dist = dist/255
        if a_dist >= 0.99:
            a_dist = 0.99
        elif a_dist <= 0.01:
            a_dist = 0.01
        last_dists_adjusted.append(a_dist)
    return last_dists_adjusted

def get_full_input(last_dists, turn_ratio):
    ai_input = []
    a_dists = get_adjusted_dists(last_dists)
    a_turn_ratio = get_turn_ratio_input(turn_ratio)
    for x in a_dists:
        ai_input.append(x)
    i = 1
    for x in a_turn_ratio:
        ai_input.insert(i, x)
        i += 2
    return ai_input



Ai = AI(_nodes = nodes, learning_rate= 0.1)

new_ratio = Ai.query(get_full_input(last_dists= last_dists, turn_ratio= turn_ratios))
new_ratio = new_ratio*100
new_ratio = new_ratio.tolist()


print(new_ratio)