#!/usr/bin/env python
# coding: utf-8

# In[2]:

import os
import math
import numpy as np
from numpy import array
import cv2
import time

# In[3]:


def eq(x1,y1,x2,y2,x,y,f):
    m = (y2-y1)/(x2-x1)
    if (f == 1):
        c = (m*x) - y <= (m*x1) - y1 
    else:
        c = (m*x) - y >= (m*x1) - y1 
    return c


# In[4]:


def create_map():
    m = np.zeros((250,400))
    am = np.zeros((250,400,3))
    hl = 40.4145
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            if (((y - 65) ** 2) + ((x - 300) ** 2) <= ((40) ** 2) ):
                m[y,x]=1
                am[y,x]=[255,0,0]
            if ((x > 200-35) and (x < 200 + 35) and (y <= 150) and eq(200,150-hl,165,150-(hl/2),x,y,1) and eq(200,150-hl,235,150-(hl/2),x,y,1) ):
                m[y,x]=1
                am[y,x]=[255,0,0]
            if ((x > 200-35) and (x < 200 + 35) and (y >= 150) and eq(200,150+hl,165,150+(hl/2),x,y,2) and eq(200,150+hl,235,150+(hl/2),x,y,2) ):
                m[y,x]=1
                am[y,x]=[255,0,0]
            if (eq(36,65,115,40,x,y,1) and eq(36,65,105,150,x,y,2) and (eq(80,70,105,150,x,y,1) and (y >= 250-180))):
                m[y,x]=1
                am[y,x]=[255,0,0]
            if (eq(36,65,115,40,x,y,1) and eq(36,65,105,150,x,y,2) and (eq(115,40,80,70,x,y,2) and (y <= 250-180))):
                m[y,x]=1
                am[y,x]=[255,0,0]
    # cv2.imshow("Zeros matx", m)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows()
    return m,am


# In[5]:


class Node:
    def __init__(self, data, cost, parent):
        self.d = data
        self.c = cost
        self.p = parent


# In[55]:


def detect(x,y):
	#global cl
	for cl in range(0,5):
		if (250 - (y+cl) > 0):
			if (m[249-(y+cl)][x] == 1):
				#print("1")
				return True
		if (250 - (y-cl) <= 249):
			if (m[249-(y-cl)][x] == 1):
				#print("2")
				return True
		if ( x+cl < 399 ):
			if (m[249-y][x+cl] == 1):
				#print("3")
				return True
		if ( x-cl > 0 ):
			if (m[249-y][x-cl] == 1):
				#print("4")
				return True
			
		if (250 - (y+cl) > 0) and ( x+cl < 399 ):
			if (m[249-(y+cl)][x+cl] == 1):
				#print("1")
				return True
		if (250 - (y+cl) > 0) and ( x-cl > 0 ):
			if (m[249-(y+cl)][x-cl] == 1):
				#print("2")
				return True
		if (250 - (y-cl) <= 249) and ( x+cl < 399 ):
			if (m[249-(y-cl)][x+cl] == 1):
				#print("2")
				return True
		if (250 - (y-cl) <= 249) and ( x-cl > 0 ):
			if (m[249-(y-cl)][x-cl] == 1):
				#print("2")
				return True
	
	return False
		
# In[56]:


def ActionMoveUp(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if ((250-(y+1)) > 0):
        if (detect(x,y)):
            return None
        if (m[249-(y+1)][x] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x,y+1],cost+1,CurrentNode)
            return child_node
    else:
        return None 


# In[57]:


def ActionMoveDown(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if ((250-(y-1)) <= 250):
        if (detect(x,y)):
            return None
        if (m[249-(y-1)][x] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x,y-1],cost+1,CurrentNode)
            return child_node
    else:
        return None 


# In[58]:


def ActionMoveRight(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if (x < 399):
        if (detect(x,y)):
            return None
        if (m[249-y][x+1] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x+1,y],cost+1,CurrentNode)
            return child_node
    else:
        return None 


# In[59]:


def ActionMoveLeft(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if (x > 0):
        if (detect(x,y)):
            return None
        if (m[249-y][x-1] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x-1,y],cost+1,CurrentNode)
            return child_node
    else:
        return None


# In[60]:


def ActionMoveUpRight(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if ((250-(y+1)) > 0) and (x < 399):
        if (detect(x,y)):
            return None
        if (m[249-(y+1)][x+1] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x+1,y+1],cost+1.4,CurrentNode)
            return child_node
    else:
        return None 


# In[61]:


def ActionMoveUpLeft(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if ((250-(y+1)) > 0) and (x > 0):
        if (detect(x,y)):
            return None
        if (m[249-(y+1)][x-1] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x-1,y+1],cost+1.4,CurrentNode)
            return child_node
    else:
        return None


# In[62]:


def ActionMoveDownRight(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if ((250-(y-1)) <= 250) and (x < 399):
        if (detect(x,y)):
            return None
        if (m[249-(y-1)][x+1] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x+1,y-1],cost+1.4,CurrentNode)
            return child_node
    else:
        return None 


# In[63]:


def ActionMoveDownLeft(CurrentNode):
    x,y = CurrentNode.d
    global cl
    if ((250-(y-1)) <= 250) and (x > 0):
        if (detect(x,y)):
            return None
        if (m[249-(y-1)][x-1] == 1):
            return None
        else:
            cost = CurrentNode.c
            child_node = Node([x-1,y-1],cost+1.4,CurrentNode)
            return child_node
    else:
        return None 


# In[64]:


def check(root):
    c = ActionMoveDownRight(root)
    if c != None :
        print(c.d)
        print(c.c)
    else :
        print("Cant GO")


# In[51]:


def move(direction, node):
    if direction == 3:
        return ActionMoveUp(node)
    elif direction == 4:
        return ActionMoveDown(node)
    elif direction == 2:
        return ActionMoveLeft(node)
    elif direction == 1:
        return ActionMoveRight(node)
    elif direction == 5:
        return ActionMoveUpRight(node)
    elif direction == 6:
        return ActionMoveUpLeft(node)
    elif direction == 7:
        return ActionMoveDownRight(node)
    elif direction == 8:
        return ActionMoveDownLeft(node)


# In[52]:


def DS(node, goal):
    Q = [node]
    CL = []
    OL,cOL = [],[]
    OL.append(node.d)
    cOL.append(node.c)
    action_set = [1,2,3,4,5,6,7,8]
    p=0
    while Q:
        l = cOL.index(min(cOL))
        #print(l)
        cn = Q.pop(l)
        o=cOL.pop(l)
        o=OL.pop(l)
        ox,oy=o
        if (p == 0):
            os.system('clear')
            print("Processing")
            print("Current Node : "+str(o))
            p=p+1
        else :
            os.system('clear')
            print("Processing...")
            print("Current Node : "+str(o))
            p=0
        CL.append(cn.d)
        if cn.d == goal :
        	return cn,CL
        for a in action_set:
            NewNode = move(a,cn)
            if NewNode != None:
                # if NewNode.d == goal :
                #     CL.append(NewNode.d)
                #     return NewNode,CL
                if (NewNode.d not in CL):
                    if(NewNode.d not in OL):
                        Q.append(NewNode)
                        OL.append(NewNode.d)
                        cOL.append(NewNode.c)
                    else:
                        T = Q[OL.index(NewNode.d)]
                        if(T.c > NewNode.c):
                            T.p = NewNode.p
                            

def reverse_path(node):
    path = []
    path = [node]
    c=0
    while node.p != None:
        x,y = node.d
        c=c+1
        m[249-(y)][x] = 1
        node = node.p
        path.append(node)
    path.reverse()
    return path

def get_input():
	global cl
	
	print('Enter Initial X (Range: 0 - 399):')
	x = int(input())
	if (x<0) or (x>399):
		print('INVALID X SETTING INITIAL X AS 0')
		x=0
		
	print('Enter Initial Y (Range: 0 - 249):')
	y = int(input())
	if (y<0) or (y>249):
		print('INVALID Y SETTING INITIAL Y AS 0')
		y=0
	
	if detect(x,y):
		print('INVALID POINTS SETTING INITIAL POINT AS [0,0]')
		x=0
		y=0
		
	print('Enter Goal X (Range: 0 - 399):')
	xg = int(input())
	if (xg<0) or (xg>399):
		print('INVALID X SETTING GOAL X AS 399')
		xg=399
		
	print('Enter Goal Y (Range: 0 - 249):')
	yg = int(input())
	if (yg<0) or (yg>249):
		print('INVALID Y SETTING GOAL Y AS 249')
		yg=0
	
	if detect(xg,yg):
		print('INVALID POINTS SETTING INITIAL POINT AS [399,249]')
		xg=399
		yg=249
		
	return [x,y],[xg,yg]

def Vi(P,C):
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter("Output.mp4", fourcc, 20.0, (400,250))
	for x,y in C:
		am[249-(y)][x] = [255,255,255]
		out.write(np.uint8(am))
		cv2.imshow("Zeros matx", am)
		cv2.waitKey(1)
	for n in P:
		x,y = n.d 
		am[249-(y)][x] = [0,0,255]
		out.write(np.uint8(am))
		cv2.imshow("Zeros matx", am)
		cv2.waitKey(1)
	cv2.imshow("Zeros matx", am)
	cv2.waitKey(0)
	out.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	st = time.time()
	m,am = create_map()
	global cl
	cl = 5
	start = []
	goal = []
	start,goal=get_input()
	root = Node([start[0],start[1]], 0 , None)
	F,C = DS(root,goal)
	et = time.time()
	#print(et-st)
	p=reverse_path(F)
	Vi(p,C)
	
