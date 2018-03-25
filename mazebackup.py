#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 20:07:45 2017

@author: anish
"""

import numpy as np
import cv2
import math

'''
def on_mouse(event,x,y,flag,param):
  if(event==cv2.EVENT_LBUTTONDOWN):
    print("In on_mouse")
    image = cv2.imread("maze33.jpg")
    pixel = image[y, x] # Note y index "row" of matrix and x index "col".
    tolerance = 30
    #print image.shape
    # Ensure your bounds are within 0 and 255.
    lower = map(lambda x: max(0, x - tolerance), pixel)
    upper = map(lambda x: min(255, x + tolerance), pixel)
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    res = cv2.inRange(image, lower, upper)
    cv2.imshow("Result", res)
'''

class node:
    def __init__(self):
        self.right=0
        self.left=0
        self.top=0
        self.bottom=0
        self.xpos=0
        self.ypos=0
    def isDeadend(self):
        sumsides=self.right+self.left+self.top+self.bottom
        if(sumsides==3):
            return True
        return False
    def isDecisionPoint(self):
        sumsides=self.right+self.left+self.top+self.bottom
        if(sumsides==1):
            return True
        return False
    
def reduced_image(filename):
    img = cv2.imread(filename)
    lower = [0,0,0]
    upper = [30,30,30]
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    res = cv2.inRange(img, lower, upper)
    i=0
    j=0

    num=0
    l=len(res)/2
    c=0
    fracs=[0.5,0.25,0.75]
    nums=[]
    while(c<len(fracs)-1):
        l=math.ceil(fracs[c]*len(res))
        num=0
        while(i<len(res)):
            if(res[i][l]!=0):
                j=i
                while(j<len(res)):
                    if(res[j][l]!=0):
                        num+=1
                        j+=1
                    else:
                        break
                break
            i+=1
        if(num): 
            nums.append(num)
        c+=1
    if(len(nums)):
        num=min(nums)
    else:
        num=0
    ##print(num)
    if(num):
        newres = []
        i=0
        while(i<len(res)):
            if(i%num==0):
                newres.append(res[i])
            i+=1
        newres = np.asarray(newres)
        ##print(newres[len(newres)/2])
        ##cv2.imshow('Result', newres)
        finres=[]


        for i in newres:
            j=0
            row=[]
            while(j<len(i)):
                if(j%num==0):
                    row.append(i[j])
                j+=1
            finres.append(row)
        finres = np.asarray(finres)
        fin2=[]
        for i in finres:
            for j in i:
                if(j!=0):
                    fin2.append(i)
                    break
        fin2=np.asarray(fin2)

        finfin=[]
        i=0
        l=len(fin2[0])
        l1=len(fin2)
        nonzerocols=[]
        while(i<l):
            j=0
            while(j<l1):
                if(fin2[j][i]!=0):
                    nonzerocols.append(i)
                    break
                j+=1
            i+=1
        for i in fin2:
            row=[]
            j=0
            while(j<len(i)):
                if(j in nonzerocols):
                    row.append(i[j])
                j+=1
            finfin.append(row)
        finfin=np.asarray(finfin)
        return finfin
    else:
        return []

def get_width(mazearr):
    width=0
    i=0
    flag=0
    if(not(width)):
        while(i<len(mazearr[0])):
            if(mazearr[0][i]!=255):
                j=i
                while(j<len(mazearr[0])):
                    if(mazearr[0][j]!=255):
                        width+=1
                    else:
                        break
                    j+=1
                break
            i+=1
    if(not(width)):
        l=len(mazearr)-1
        l1=len(mazearr[0])
        i=0
        while(i<l1):
            if(mazearr[l][i]!=255):
                j=i
                while(j<l1):
                    if(mazearr[l][j]!=255):
                        width+=1
                    else:
                        break
                    j+=1
                break
            i+=1
    if(not(width)):
        l=len(mazearr)-1
        l1=len(mazearr[0])
        i=0
        j=0
        while(i<=l):
            if(mazearr[i][0]!=255):
                k=i
                while(k<=l):
                    if(mazearr[k][0]!=255):
                        width+=1
                    else:
                        break
                    k+=1
                break
            i+=1
    if(not(width)):
        l=len(mazearr)-1
        l1=len(mazearr[0])-1
        i=0
        j=0
        while(i<=l):
            if(mazearr[i][l1]!=255):
                k=i
                while(k<=l):
                    if(mazearr[k][l1]!=255):
                        width+=1
                    else:
                        break
                    k+=1
                break
            i+=1
    return width

def is_deadend(view):
    k=0
    d=node()
    d.top=0
    d.bottom=0
    d.left=0
    d.right=0
    dflag=0
    while(k<width):
        if(view[0][k]==255):
            d.top=1
        else:
            d.top=0
            break
        k+=1
    k=0
    while(k<width):
        if(view[width-1][k]==255):
            d.bottom=1
        else:
            d.bottom=0
            break
        k+=1
    k=0
    while(k<width):
        if(view[k][0]==255):
            d.left=1
        else:
            d.left=0
            break
        k+=1
    k=0
    while(k<width):
        if(view[k][width-1]==255):
            d.right=1
        else:
            d.right=0
            break
        k+=1
    if(d.isDeadend()):
        return d
    return 0

def getView(mazearr,i,j,width):
    k=0
    view=[]
    while(k<width):
        row=[]
        c=0
        while(c<width):
            row.append(mazearr[i+k][j+c])
            c+=1
        view.append(row)
        k+=1
    return view

def find_deadends(mazearr, width):
    i=0
    deadends=[]
    l=len(mazearr)
    l1=len(mazearr[0])
    while(i<=l-width):
        j=0
        while(j<=l1-width):
            res = is_deadend(getView(mazearr, i, j, width))
            if(res):
                mazearr[i+width/2][j+width/2]=255
                print("Deadend at :",i+width/2, j+width/2)
                res.xpos=i
                res.ypos=j
                deadends.append(res)
            j+=1
        i+=1
    return mazearr, deadends

def processMaze(mazearr, nodeArray, width):
    for dEnd in nodeArray:
        view = getView(mazearr, dEnd.xpos, dEnd.ypos, width)





        
filename = "maze4.png"
mazearr=reduced_image(filename)
if(mazearr.any()):
    width = get_width(mazearr)+2
    deadends,nodeArray = find_deadends(mazearr, width)
    #print(mazearr[len(mazearr)-1])
    #print(width)
    cv2.imshow('Maze', cv2.imread(filename))

    cv2.imshow('Result', deadends)
    #processMaze(mazearr, nodeArray, width)
    while (cv2.getWindowProperty('Maze', 0) >= 0 or cv2.getWindowProperty('Result', 0) >= 0):
        r = cv2.waitKey(20)
        if(r==32):
            cv2.destroyAllWindows()
            break

    cv2.destroyAllWindows()
else:
    print("Error")

