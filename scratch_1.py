from random import randrange
print(randrange(10))


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
    return randrange(len(lst))

def buildNodeTree(kernList):
    nodeList = []
    stack = []
    kern = kernList[0]  # take the first item = this controls the root kernel
    nodeList.append(kern)
    argIndex = 1
    while len(stack) > 0 or kern.arity > argIndex:
        newKern = getRandListItem(kernList)
        nodeList.append(newKern)
        if newKern.Arity > 0:
            stack.push([kern,argIndex])
            kern = newKern
            argIndex = 1
        else:
            argIndex += 1
            if argIndex > kern.Arity:
                kern,argIndex = stack.pop()
                argIndex += 1
    return nodeList



mult = kernel(2,'*', lambda xy:xy[0] * xy[1])
add  = kernel(2,'+', lambda xy:xy[0] + xy[1])
sub  = kernel(2,'-', lambda xy:xy[0] - xy[1])
pi   = kernel(0,'pi',lambda x:3.141592 )
c4   = kernel(0,'4', lambda x:4.0)

kernList = [mult,add,sub,pi,c4]

test = buildNodeTree(kernList)

piNode1 = node(pi)
piNode2 = node(pi)
realNode = node(mult,[piNode1,piNode2])

test = realNode.calc()

