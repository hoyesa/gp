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
    '''
    isOp: boolean - current Node is an operator (has arity > 0)
    isStack: boolean - the operator stack has non-zero length, means that we are not at top level in tree
    isLastBranch: boolean - is the current argument index the final; means argument looked for is the arity of operator
    '''
    return int(isLastBranch)+2*int(isStack)+4*int(isOp)

def spanNodeTree(nodeTree):
    nodeIdx = 1
    curOp = nodeTree[0]  # take the first item = this controls the root kernel
    argIndex = 1
    opStack = []
    argStack = []

    while True:
        # get the next node in the tree
        curNode = nodeTree[nodeIdx]
        nodeIdx += 1

        # calculate the state of the tree spanner
        state = stateMachine(curNode.arity>0,len(opStack)>0,argIndex==curOp.arity)

        # current node is an operator
        if 4 <= state <= 7:
            opStack.append((curOp,argIndex))
            argIndex = 1
            curOp = curNode

        # current token is terminal but need more to finish
        if state in (0,2):
            argStack.append(curNode.run([]))
            argIndex += 1

        # current token is finishing terminal in top level operator
        if state == 1:
            # push queue; dequeue argList; solve;  RETURN
            argStack.append(curNode.run([]))
            tmpArgList = [argStack.pop() for i in range(curOp.arity)]
            val = curOp.run(tmpArgList[::-1])
            return val

        # current token is finishing terminal in a lower level operator
        if state == 3:
            # push queue; dequeue argList; solve; push solution; pop stack; inc Curbranch
            argStack.append(curNode.run([]))
            while True:
                tmpArgList = [argStack.pop() for i in range(curOp.arity)]
                val = curOp.run(tmpArgList[::-1])
                if len(opStack) == 0:
                    return val
                argStack.append(val)
                curOp,argIndex = opStack.pop()
                if curOp.arity > argIndex:
                    break
            argIndex += 1  # TODO bug here?

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

testTree = [mult,add,c4,pi,sub,c4,pi]

population = [buildNodeTree(kernList,3) for i in range(50)]

vals = [spanNodeTree(population[i]) for i in range(len(population))]

print("finished. . .")
