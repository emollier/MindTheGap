from pipeline.genome_graph.utils import reverse_complement
from pipeline.genome_graph.genome_graph import *

class LinearPath:
    def __init__(self,g,nodeId):
        self.nodes = [g.nodes[abs(nodeId)]]
        self.nodeIds = [nodeId]
        self.nNodes = 1
    
    def extend(self,g):
        lastNode = self.nodeIds[-1]
        neighbors = g.edges[lastNode].copy()
        if len(neighbors)==1:
            neighbor = neighbors.pop()
            if abs(neighbor) not in [abs(n) for n in self.nodeIds]: # Node has not been visited by path
                rev_neighbors = g.edges[-neighbor]
                if rev_neighbors == {-lastNode}:
                    self.nodes.append(g.nodes[abs(neighbor)]) 
                    self.nodeIds.append(neighbor)
                    self.nNodes += 1
                    return(True)
        return(False)

    def getSeq(self,g):
        seq = ''
        rev = False
        for node in self.nodeIds:
            nodeSeq = g.nodes[abs(node)].nodeSeq
            if node < 0:
                rev = not rev
            if rev:
                nodeSeq = reverse_complement(nodeSeq)
            if seq != '':
                nodeSeq = nodeSeq[g.overlap:]    
            seq = seq + nodeSeq
        return(seq)

    def getName(self,g):
        name = ''
        rev = False
        for node in self.nodeIds:
            nodeName = g.nodes[abs(node)].nodeName
            if node < 0:
                rev = not rev
            if rev:
                nodeName = nodeName + "_Rc"
            if name != '':
                nodeName = "_" + nodeName   
            name = name + nodeName
        return(name)

    def merge(self,g):
        newName = self.getName(g)
        newSeq = self.getSeq(g)
        g.add_node(newName,newSeq)
        newId = max(g.nodes.keys())
        print(newId)

        neighbors_left = g.get_neighbors(-self.nodeIds[1])
        for n in neighbors_left:
            g.add_edge(-newId,n)

        neighbors_right = g.get_neighbors(self.nodeIds[-1])
        for n in neighbors_right:
            g.add_edge(newId,n)

            
