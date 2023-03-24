import random
import numpy as np
from matplotlib import pyplot as plt
import initialiser_functions as i
import environment_class as e


def checks_v2(child, named_cars, number_of_witnesses_needed, threshold):
    """checks called from the child with respect to the parent node, to ensure that 
    all criteria for T-PoP are met."""
    counter = 0
    parent = child.parent
    parent_position = parent.claim_position()

    
    if (
    #checking the parent is a neighbour of the child
    child.is_car_a_neighbour(parent) is True and
    #checking the parent is in the range of sight of the child
    child.is_in_range_of_sight(parent_position) is True and
    #checking the child has not been named before
    child.ID not in named_cars and 
    #checking the parent has named enough witnesses (ie children)
    len(parent.children) >= int(number_of_witnesses_needed * threshold) and
    #checking that there is no repeats in the named witnesses (ie children) 
    len(parent.children) == len(set(parent.children))
    ):

        counter += 1
        named_cars.add(child.ID)


    return counter

def checks_v3(child, named_cars, number_of_witnesses_needed, threshold):
    """checks called from the child with respect to the parent node, to ensure that 
    all criteria for T-PoP are met."""
    counter = 0
    parent = child.parent
    parent_position = parent.claim_position()

    
    if (
    #checking the parent is a neighbour of the child
    child.is_car_a_neighbour(parent) is True and
    #checking the parent is in the range of sight of the child
    child.is_in_range_of_sight(parent_position) is True and
    #checking the child has not been named before
    child.ID not in named_cars and 
    #checking the parent has named enough witnesses (ie children)
    len(parent.children) >= int(number_of_witnesses_needed * threshold) and
    #checking that there is no repeats in the named witnesses (ie children) 
    len(parent.children) == len(set(parent.children))
    ):
        named_cars.add(child.ID)
        return True
    else:
        return False
        

    




#---------------------START OF AIDA POL protocol----------------------:
    
""" if len(witness_number_per_depth) != depth:
    raise Exception('Make sure there is number of witnesses defined for each round') """



class Tree2:

    def __init__(self, prover, depth, n):
        #prover is the root of the tree, and the agent calling this function
        self.prover = prover
        #all nodes in the tree, indexed by depth level
        self.nodes = [[self.prover]]
        self.depth = depth
        
        for d in range(depth):
            
            s = []
            #for all nodes in the given depth level
            for node in self.nodes[d]:
                #the node names some witnesses
                witnesses = node.name_witness(n[d])
                if witnesses is not None:

                    for witness in witnesses:
                        #we set the parent of that witness to be the node naming them
                        witness.parent = node
                        s.append(witness)
                #and set the children of the nodes to be the named witnesses    
                node.children = s
            self.nodes.append(s)



def reverse_bfs(tree, witness_number_per_depth, threshold):

    root = tree.prover
    #we keep track of the agents named in each round
    named_cars = set()
    
    #we start from the leaves and do a reverse BFS upwards until the root
    for level in reversed(range(0, tree.depth + 1)):
        #retrieve the number of witnesses(ie children) necessary at that level.
        #NOTE: we start indexing from the 0th level.
        number_of_witnesses_needed = witness_number_per_depth[level]

        #for each depth level, we need to keep track of the number of children that approve the parent
        parent_counter = 0
        for child in tree.nodes[level]:
            parent = child.parent
            #if we are at the root, do not perform any more checks because the root has no parent
            if child.parent is None:
                break
                
            #return the number of approvals 
            counter = checks_v2(child, named_cars, number_of_witnesses_needed, threshold)
            #add the child to the set of visited/named agents
            named_cars.add(child.ID)

            #update the parent counter
            parent_counter = parent_counter + counter
            parent.counter = parent_counter

            print(parent.counter)
            
        if parent.counter >= int(number_of_witnesses_needed * threshold):
            parent.algorithm_honesty_output = True
        else:
            parent.algorithm_honesty_output = False
            
    
    if child.counter is not None:
        print('root counter ', root.counter, int(number_of_witnesses_needed * threshold))
        #check that the root has enough approvals to be considered honest
        if root.counter >= int(number_of_witnesses_needed * threshold):
            root.algorithm_honesty_output = True
        else:
            root.algorithm_honesty_output = False
                

    return root.algorithm_honesty_output



def TPoP(tree, threshold:float, witness_number_per_depth:int) -> bool:
    named_cars = set()
    for level in range(tree.depth - 1, -1, -1):
        number_of_witnesses_needed = witness_number_per_depth[level]
        counterDepth = 0
        for parent in tree.nodes[level]:
                counterChildren = 0
                for child in parent.children:
                    
                    if child.verified and checks_v3(child, named_cars, number_of_witnesses_needed, threshold):

                        counterChildren += 1
                        counterDepth += 1

                if counterChildren < threshold*len(parent.children):
                    parent.verified = False
                
        if counterDepth < threshold*len(tree.nodes[level+1]):
            parent.algorithm_honesty_output = False
        else:
            parent.algorithm_honesty_output = True
        
    return parent.algorithm_honesty_output



def results(cars):
    True_Positive = 0
    True_Negative = 0
    False_Positive = 0
    False_Negative = 0


    for car in cars:

        if car.honest is True and car.algorithm_honesty_output is True:
            True_Positive += 1
        if car.honest is True and car.algorithm_honesty_output is False:
            False_Negative += 1
        if car.honest is False and car.algorithm_honesty_output is True:
            False_Positive += 1
        if car.honest is False and car.algorithm_honesty_output is False:
            True_Negative += 1

    Accuracy = ((True_Positive + True_Negative) / (True_Positive + True_Negative + False_Positive + False_Negative)) * 100
    
    return True_Positive, True_Negative, False_Positive, False_Negative, Accuracy

#True_Positive, True_Negative, False_Positive, False_Negative, Accuracy = results(car_list)
#print(True_Positive, True_Negative, False_Positive, False_Negative)
#print(False_Negative_cars)


