import itertools
import time
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw()
import numpy as np
import math

# Python function to print permutations of a given list
def readIn():
    # Replace open statement with next 2 lines in order to open file explorer for user to choose file
    # filepath = askopenfilename(initialdir=os.getcwd())
    # inFile = open(filepath, 'r')
    inFile = open("C:/Users/JGMan/PycharmProjects/3230_TSP/bigTest.txt", 'r')
    # Reads and removes first line to be read
    numPoints = int(inFile.readline())
    numPoints += 1
    # reads, and splits rest of file into points delimited by a space
    # creates a list of lists, with each point being a list like [87, 45]
    points = [[0, 0]]
    for line in inFile:
        point = line.strip()
        point = point.split(" ")
        # converts point to integer values
        for i in range(0, len(point)):
            point[i] = int(point[i])
        points.append(point)

    return numPoints, points


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
                # could add inverse, to cut down number of calculations, but unnecessary.
    return distanceMatrix


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


def calcPermutationDist(numPoints, dm):
    x = itertools.permutations(range(1, numPoints))
    while True:
        p = next(x)
        currentPerm = list(p)
        currentPerm = [0] + currentPerm + [0]
        totalDist = 0
        for e in range(0, len(currentPerm) - 1):
            totalDist += dm[currentPerm[e]][currentPerm[e+1]]
        print(currentPerm)
        print(totalDist)
    # return next(x)


numofpoints, listPoints = readIn()
# print(numofpoints)
# print(listPoints)
# print(listPoints[2])
dMatrix = distanceMatrixCalc(numofpoints, listPoints)
print(dMatrix)
calcPermutationDist(numofpoints, dMatrix)
# Driver program to test above function
data = [1, 2, 3, 4, 5, 6]
# count = 0
# start = time.time()
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
