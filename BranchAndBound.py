'''
QUEEN'S UNIVERSITY
CISC 365 2015F
Assignment 2
Brianna Rubin

Upper Bound Implementation 1:
takes the cost so far (value of all the rejected objects that will definitely
not be in the complete solution) and adds it to the value of the objects we
will not be able to choose in the future

Upper Bound Implementation 2:
uses the maximum capacity, or K

Lower Bound Implementation 1:
finds the total value of the partial solution's remaining objects and adds
it to the cost so far

Lower Bound Implementation 2:
finds the cost so far as described above

TO DO: implement my own min-heap, instead of importing the heapq package 

'''

import heapq
from copy import deepcopy

class Object:
#The object class creates an object that has an ID, a value, a mass, and a
#ratio, and is compared based on the ratio
        def __init__(self, i, v, m):
                self.ID = i
                self.mass = m
                self.value = v
                self.ratio = v * 1.0 / m
        def __cmp__(self,other):
                return self.ratio > other.ratio

class partialSolution:
        def __init__(self, c, r, re, u, l):
                self.chosen = c
                self.rejected = r
                self.remaining = re
                self.upper = u
                self.lower = l
        def __cmp__(self,other):
                return self.lower > other.lower

def openFile(filename):
#Opens the data file and returns the instance name, K, the number of objects,
#and the list of objects, each as an instance of the Object class
        myFile = open(filename)
        lines = []
        for line in myFile:
                newLine = str.split(line)
                lines.append(newLine)
        problemInstance = ""
        for word in lines[0]:
                problemInstance = problemInstance + (" ")
                problemInstance = problemInstance + (word)
        K = lines[1][0]
        numObjects = lines[1][1]
        objects = lines[2:]
        for i in range(len(objects)):
                objects[i] = map(int, objects[i])
                objects[i] = Object(objects[i][0], objects[i][1], objects[i][2])
        sortedObjects = sorted(objects, key=lambda x: x.ratio, reverse=True)
        return problemInstance, K, numObjects, sortedObjects


def totalValue(objects):
#takes the objects, and finds the total value, which we will try to minimize
#for the objects we don't choose
        value = 0
        for obj in objects:
                value += int(obj.value)
        return value

def totalMass(objects):
#takes the objects, and finds the total value, which we will try to minimize
#for the objects we don't choose
        mass = 0
        for obj in objects:
                mass += int(obj.mass)
        return mass

def GlobalUpper(objects, K, totalValue):
#Uses a greedy heuristic to find value if items are chosen in the order of their
#value/mass ratio in descending order, until the total mass reaches K
        mass = 0
        value = 0
        K = float(K)
        for obj in objects:
                objmass = obj.mass
                totalmass = objmass + mass
                if (totalmass) <= K:
                        mass += obj.mass
                        value += obj.value
        return totalValue - value


def Upper1(P,K):
#takes the CSF and adds the items that cannot be chosen (rejected ones)
        chosenMass = totalMass(P.chosen)
        value = 0
        for obj in P.remaining:
                if obj.mass + chosenMass <= K:
                        chosenMass += obj.mass
                else:
                        value += obj.value

        return value + totalValue(P.rejected)

def Upper2(P,K):
        return K

def Lower1(P,K):

        value = 0
        for obj in P.chosen:
                K -= obj.mass

        for obj in P.remaining:
                if obj.mass > K:
                        value += obj.value
        return value + totalValue(P.rejected)

def Lower2(P,K):
        return totalValue(P.rejected)

def BandB(objects, K, option):
#The branch and bound algorithm, expands partial solutions and puts them in a min heap
#and returns the best solution (root of the heap), when a complete solution is found
        value = totalValue(objects)
        globalUpper = GlobalUpper(objects, int(K), value)
        first = partialSolution([],[],objects,globalUpper,0)
        solutionCount = 1
        heap = []
        heapq.heappush(heap,(first.lower,first))

        while True:
                current = heapq.heappop(heap)[1]

                if len(current.remaining) == 0:
                        print " Partial Solutions Created: ", solutionCount
                        return current
                else:
                        chosen = current.remaining[0]
                        del current.remaining[0]

                        next1 = deepcopy(current)
                        next2 = deepcopy(current)

                        cost = chosen.mass + totalMass(current.chosen)
                        # if the item is chosen, change its upper and lower bounds
                        # and if necessary, change the global upper bound

                        if cost <= K and current.lower <= globalUpper:
                                next1.chosen.append(chosen)
                                if option == 0:
                                        next1.upper = Upper1(next1,K)
                                        next2.lower = Lower1(next1,K)
                                else:
                                        next1.upper = Upper2(next1,K)
                                        next2.lower = Lower2(next1,K)
                                if next1.upper < globalUpper:
                                        globalUpper = next1.upper

                                heapq.heappush(heap, (next1.lower, next1))
                                solutionCount += 1

                        next2.rejected.append(chosen)
                        if option == 0:
                                next2.upper = Upper1(next2, K)
                                next2.lower = Lower1(next2, K)
                        else:
                                next2.upper = Upper2(next2, K)
                                next2.lower = Lower2(next2, K)

                        if next2.lower <= globalUpper:
                                if next2.upper < globalUpper:
                                        globalUpper = next2.upper

                                heapq.heappush(heap, (next2.lower, next2))
                                solutionCount +=1

def formatPrint(P):
        chosenObjects = ""
        for obj in P.chosen:
                chosenObjects = chosenObjects + str(obj.ID) + " "
        print " Chosen Objects: ", chosenObjects

        value = totalValue(P.chosen)
        mass = totalMass(P.chosen)

        print " Total Value: {}".format(value)
        print " Total Mass: {}".format(mass)

def main():

        filename = "inputs/input20.txt"
        instance = openFile(filename)[0]
        K = openFile(filename)[1]
        K = int(K)
        numObjects = openFile(filename)[2]
        objects = openFile(filename)[3]
        print instance
        bestSolution = BandB(objects, K, 0)
        chosenObjects = bestSolution.chosen
        formatPrint(bestSolution)

main()
