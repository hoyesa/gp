import math
from random import randrange, randint, uniform


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
        args = []
        for node in self.nodeArgList:
            args.append(node.calc())
            print("hello")
        return self.kern.run(args)

class Soup():
    def __init__(self) -> None:
        self.kernList = []
        self.opList = []
        self.termList = []

    def append(self,kern:kernel) -> None:
        self.kernList.append(kern)
        if kern.arity == 0:
            self.termList.append(kern)
        else:
            self.opList.append(kern)

    def addRandConst(self,n:int,loLim:float,hiLim:float) -> None:
        for i in range(n):
            r = uniform(loLim, hiLim)
            self.append(kernel(0, str(r), lambda x: r))

    def getRandKern(self) -> kernel:
        idx = randint(0,len(self.kernList)-1)
        return self.kernList[idx]

    def getRandOp(self) -> kernel:
        idx = randint(0, len(self.opList) - 1)
        return self.opList[idx]

    def getRandTerm(self) -> kernel:
        idx = randint(0, len(self.termList) - 1)
        return self.termList[idx]

class Alife():
    def __init__(self, soup: Soup, maxLevel:int=2):
        self.nodeList = []
        stack = []
        kern = soup.getRandOp()
        self.nodeList.append(kern)
        self.funcString = kern.symbol + '('
        argIndex = 1
        while len(stack) > 0 or kern.arity >= argIndex:
            if len(stack) < maxLevel:  # max level
                newKern = soup.getRandKern()
            else:
                newKern = soup.getRandTerm()
            self.nodeList.append(newKern)
            if newKern.arity > 0:
                stack.append([kern, argIndex])
                kern = newKern
                argIndex = 1
                self.funcString += kern.symbol + '('
            else:
                self.funcString = self.funcString + newKern.symbol
                while argIndex >= kern.arity and len(stack) > 0:
                    kern, argIndex = stack.pop()
                    self.funcString = self.funcString + ')'
                argIndex += 1
                self.funcString = self.funcString + ','
        self.funcString = self.funcString.rstrip(',') + ')'

    def spanNodeTree(self,argList) -> float:
        # check if first node is a terminal and return it
        if self.nodeList[0].arity == 0:
            return self.nodeList[0].run([])
        argKernList = [kernel(0,'_arg'+str(i),lambda x:argList[i]) for i in range(len(argList))]
        nodeIdx = 1
        curOp = self.nodeList[0]  # take the first item = this controls the root kernel
        argIndex = 1
        opStack = []
        argStack = []

        while True:
            # get the next node in the tree
            curNode = self.nodeList[nodeIdx]
            nodeIdx += 1

            # cuckoos egg: replace arg kernels with argList items
            if curNode.symbol[0:4] == '_arg':
                idx = int(curNode.symbol[4:])
                curNode = argKernList[idx]

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
                argIndex += 1

def getRandListItem(lst):
    return lst[randrange(len(lst))]

def stateMachine(isOp,isStack,isLastBranch):
    '''
    isOp: boolean - current Node is an operator (has arity > 0)
    isStack: boolean - the operator stack has non-zero length, means that we are not at top level in tree
    isLastBranch: boolean - is the current argument index the final; means argument looked for is the arity of operator
    '''
    return int(isLastBranch)+2*int(isStack)+4*int(isOp)


## primordial soup of kernel operators

soup = Soup()
# arguments
soup.append(kernel(0,'_arg0',lambda x: 0.0))

soup.append(kernel(2,'*', lambda xy: xy[0] * xy[1]))
soup.append(kernel(2,'/', lambda xy: 0 if xy[1] == 0.0 else xy[0]/xy[1]))
soup.append(kernel(2,'+', lambda xy: xy[0] + xy[1]))
soup.append(kernel(2,'-', lambda xy: xy[0] - xy[1]))
soup.append(kernel(1,'sqr',  lambda xy: xy[0]**2))
soup.append(kernel(1,'sqrt', lambda xy: math.sqrt(abs(xy[0]))))
soup.append(kernel(4,'if_gt',lambda xy: xy[2] if xy[0] > xy[1] else xy[3]))
soup.append(kernel(4,'if_le',lambda xy: xy[2] if xy[0] <= xy[1] else xy[3]))
soup.append(kernel(0,'pi', lambda x: 3.141592 ))
soup.append(kernel(1,'exp',lambda x: math.exp(34.0) if x[0] > 34.0 else math.exp(x[0])))
soup.append(kernel(1,'ln', lambda x: 0 if x[0] <= 0.0 else math.log(x[0])))
soup.append(kernel(1,'sin',lambda x: math.sin(x[0])))
soup.append(kernel(1,'cos',lambda x: math.cos(x[0])))

soup.addRandConst(10,-4.0,4.0)

popSize = 500
maxLevs = 7
target  = 3.0

population = [Alife(soup,maxLevs) for i in range(popSize)]

vals = [alife.spanNodeTree([.99]) for alife in population]

fitness = [math.fabs(vals[i]-target) for i in range(len(vals))]

print("finished. . .")
