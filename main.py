import itertools
import time
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename

tk.Tk().withdraw()
import numpy as np
import math


# function reads the input file, separating it into the number of points from the first line
# and then adds the rest of lines as a list of lists for the points
def readIn():
    # Replace open statement with next 2 lines in order to open file explorer for user to choose file
    # filepath = askopenfilename(initialdir=os.getcwd())
    # inFile = open(filepath, 'r')
    inFile = open("C:/Users/JGMan/PycharmProjects/3230_TSP/biggestTest.txt", 'r')
    # Reads and removes first line to be read
    numPoints = int(inFile.readline())
    # add 1 to num points to include (0,0)
    numPoints += 1
    # reads, and splits rest of file into points delimited by a space
    # creates a list of lists, with each point being a list like [87, 45]
    # add (0,0) before appending all other points
    points = [[0, 0]]
    for line in inFile:
        point = line.strip()
        point = point.split(" ")
        # converts point to integer values
        for i in range(0, len(point)):
            point[i] = int(point[i])
        points.append(point)

    return numPoints, points


# creates a distance matrix for each possible edge
def distanceMatrixCalc(numberPoints, listPoints):
    # init distanceMatrix to all 0's dynamically based on numberPoints
    distanceMatrix = np.zeros((numberPoints, numberPoints))
    # loops 2 pointers through matrix to fill it out
    for a in range(numberPoints):
        for b in range(numberPoints):
            # diagonal 0's
            if a == b:
                distanceMatrix[a][b] = 0
            else:
                # math.dist calculates pythagorean theorem on the 2 points
                pDistance = math.dist(listPoints[a], listPoints[b])
                pDistance = round(pDistance, 2)
                distanceMatrix[a][b] = pDistance
                # distanceMatrix[b][a] = pDistance
                # could add inverse, to cut down number of calculations, but unnecessarily complicated.
    return distanceMatrix


# I stole this from geeksForGeeks or something.  I don't exactly know
# how it works, other perm function seems to work better
def permutation(lst):
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
    # If there is only one element in lst then, only
    # one permutation is possible
    if len(lst) == 1:
        return [lst]
    # Find the permutations for lst if there are
    # more than 1 characters
    l = []  # empty list that will store current permutation
    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
        m = lst[i]
        # Extract lst[i] or m from the list.  remLst is
        # remaining list
        remLst = lst[:i] + lst[i + 1:]
        # Generating all permutations where m is first
        # element
        count = 0
        for p in permutation(remLst):
            l.append([m] + p)
            count += 1
    return l


# permutation function working well at least for brute force?
def calcPermutationDist(numPoints, dm):
    timeLimit = 180.0
    # itertools creates data for all perms of 1 to numPoints
    # idk how this works under the hood, but seems to not be a normal
    # list or array
    x = itertools.permutations(range(1, numPoints))
    start = time.time()
    keepGoing = True
    # tuple to hold the best path found along with distance
    bestPath = ([], 9999999999999999999999999999999999999999)
    numPerms = 0
    while keepGoing:
        # next(x) is next perm in order that itertools creates
        try:
            p = next(x)
            numPerms += 1
        except StopIteration:
            print("Checked all possible permutations")
            break

        # convert itertools item into list
        currentPerm = list(p)
        # add 0 to front and back of list to start and end at home base
        currentPerm = [0] + currentPerm + [0]
        totalDist = 0
        # loops through perm adding distances of each edge from distance matrix
        # ex: perm = [0, 1, 2, 3, 0] is distance from 0 to 1
        # plus 1 to 2 plus 2 to 3 plus 3 to 0
        for e in range(0, len(currentPerm) - 1):
            totalDist += dm[currentPerm[e]][currentPerm[e + 1]]
        # replaces current best path with new best when found
        if totalDist < bestPath[1]:
            bestPath = (currentPerm, totalDist)
        # print(currentPerm)
        # print(totalDist)
        # breaks out of loop if over the timeLimit defined above
        if time.time() - start > timeLimit:
            endTime = time.time()
            keepGoing = False
        # print(stepTime - start)
    if keepGoing:
        endTime = time.time()
    bfTime = endTime - start
    if not keepGoing:
        print("Could not check all possible permutations within " + str(timeLimit)
              + " seconds")
    return bestPath, bfTime, numPerms


numofpoints, listPoints = readIn()
# print(numofpoints)
# print(listPoints)
# print(listPoints[2])
dMatrix = distanceMatrixCalc(numofpoints, listPoints)
print(dMatrix)
bestPathFound, BFTIME, numChecked = calcPermutationDist(numofpoints, dMatrix)
print("Best Path Found: " + str(bestPathFound[0]))
print("Distance of Path: " + str(round(bestPathFound[1], 2)))
print("Calculation Time: " + str(round(BFTIME, 4)))
print("Number of permutations checked: " + str(numChecked))
# Driver program to test above function
data = [1, 2, 3, 4, 5, 6]
# count = 0
# perms = permutation(data)
# print(len(perms))
# print(perms)
# end = time.time()
#
# # for p in permutation(data):
# #     print(p)
# #     count += 1
# print(count)
# print("time:")
# print(end - start)
