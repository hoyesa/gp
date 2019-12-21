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

def buildNodeTree(kernList):
    kern = kernList[randrange(len(kernList))]
    nodeList = []
    if kern.arity > 0:
        for branch in range(kern.arity):
            nodeList.append(buildNodeTree(kernList))
    return node(kern,nodeList)



mult = kernel(2,'*', lambda xy:xy[0] * xy[1])
add  = kernel(2,'+', lambda xy:xy[0] + xy[1])
sub  = kernel(2,'-', lambda xy:xy[0] - xy[1])
pi   = kernel(0,'pi',lambda x:3.141592 )
c4   = kernel(0,'4', lambda x:4.0)

kernList = [mult,add,sub,pi,c4]

treeList = [buildNodeTree(kernList).calc() for i in range(10)]

piNode1 = node(pi)
piNode2 = node(pi)
realNode = node(mult,[piNode1,piNode2])

test = realNode.calc()

