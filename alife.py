import math
from random import randrange
from collections import deque


class kernel():
    def __init__(self,arity : int, sym : str, runFunc):
        self.arity = arity
        self.symbol = sym
        self.runFunc = runFunc

    def run(self,argList):
        assert len(argList) == self.arity
        return self.runFunc(argList)

class node():
    def __init__(self,kern,nodeArgList=[]):
        self.kern = kern
        assert len(nodeArgList) == kern.arity
        self.nodeArgList = nodeArgList

    def calc(self):
#        args = [node.calc() for node in self.nodeArgList]
        args = []
        for node in self.nodeArgList:
            args.append(node.calc())
            print("hello")
        return self.kern.run(args)

def getRandListItem(lst):
    return lst[randrange(len(lst))]

def stateMachine(isOp,isStack,isLastBranch):
    return int(isLastBranch)+2*int(isStack)+4*int(isOp)

def spanNodeTree(nodeTree):
    nodeIdx = 1
    kern = nodeTree[0]  # take the first item = this controls the root kernel
    argIndex = 1
    stack = [(kern,argIndex)]
    argQueue = deque()

    while len(stack) > 0 or argIndex < kern.arity:
        newKern = nodeTree[nodeIdx]
        nodeIdx += 1
        if newKern.arity > 0:
            argIndex = 1
            stack.append((newKern,argIndex))
            kern = newKern
        else:   # got a terminal
            argQueue.append(newKern.run([]))
            while argIndex >= kern.arity and len(stack) > 0:
                ## this is a terminal that finished arguments - compute the kernel
                kern,argIndex = stack.pop()
                if argIndex == kern.arity:
                # pop terminals off the queue and compute kernel
                    tmpArgList = []
                    for arg in range(kern.arity):
                        tmpArgList.append(argQueue.popleft())
                    val = kern.run(tmpArgList)
                    argQueue.append(val)
            argIndex += 1
    return val

def buildNodeTree(kernList,maxLevel=2):
    val = None
    nodeList = []
    stack = []
    kern = kernList[0]  # take the first item = this controls the root kernel
    nodeList.append(kern)
    functString = kern.symbol+'('
    argIndex = 1
    while len(stack) > 0 or kern.arity >= argIndex:
        if len(stack) < maxLevel: # max level
            newKern = getRandListItem(kernList)
        else:
            newKern = getRandListItem(kernList[8:10])
        nodeList.append(newKern)
        if newKern.arity > 0:
            stack.append([kern,argIndex])
            kern = newKern
            argIndex = 1
            functString += kern.symbol + '('
        else:
            functString += newKern.symbol
            while argIndex >= kern.arity and len(stack) > 0:
                kern,argIndex = stack.pop()
                functString += ')'
            argIndex += 1
            functString += ','
    functString = functString.rstrip(',') + ')'
    return nodeList

## primordial soup of kernel operators

mult = kernel(2,'*', lambda xy:xy[0] * xy[1])
div  = kernel(2,'/', lambda xy: 0 if xy[1] == 0.0 else xy[0]/xy[1])
add  = kernel(2,'+', lambda xy:xy[0] + xy[1])
sub  = kernel(2,'-', lambda xy:xy[0] - xy[1])
sqr  = kernel(1,'^', lambda xy:xy[0]**2)
sqrt = kernel(1,'sqrt',lambda xy:math.sqrt(abs(xy[0])))
ifgt = kernel(4,'if_gt',lambda xy:xy[2] if xy[0] > xy[1] else xy[3])
ifle = kernel(4,'if_le',lambda xy:xy[2] if xy[0] <= xy[1] else xy[3])
pi   = kernel(0,'pi',lambda x:3.141592 )
c4   = kernel(0,'4', lambda x:4.0)

kernList = [mult,div,add,sub,sqr,sqrt,ifgt,ifle,pi,c4]

testTree = [mult,add,c4,pi,c4]

population = [buildNodeTree(kernList,1) for i in range(1)]

val = spanNodeTree(testTree)

print("finished. . .")
