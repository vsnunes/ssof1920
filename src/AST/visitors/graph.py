from copy import deepcopy

class Graph():
    def __init__(self):
        self.graph = []

    def addRoot(self, element):
        """
        Adds an element to the root of the graph
        """
        self.graph.append([element, []])

    def addRootGraph(self, sub_graph):
        """
        Adds another graph to top root
         self          other          self become
           a            g             a            g
          / \          / \           / \          / \
         b   c        h   j         b   c        h   j 
         |  / \                     |  / \
         y x   w                    y x   w
        
        """
        self.graph += sub_graph.graph

    def getRootElement(self, element):
        """
        Searches for a root element in the graph
        """
        for el in self.graph:
            if el[0] == element:
                return el
        return []

    def getChildren(self, element, sub_graph=None):
        """
        Get children of a element
        Example: element = c
        self                returns
           a                   / \
          / \                 x   w
         b   c
         |  / \
         y x   w
        """
        if sub_graph is None:
            sub_graph = self.graph

        children = []

        for el in sub_graph:
            if el[0] == element:
                children += el[1]
            else:
                children += self.getChildren(element, el[1])
        return children

    def addChild(self, element, child, sub_graph=None):
        """
        Adds a child to an element
        Example: element = x child = c
        before      after
        a             a
        |             |
        x             x
                      |
                      c
        """
        if sub_graph is None:
            sub_graph = self.graph

        for el in sub_graph:
            if el[0] == element:
                el[1].append([child, []])
            elif el[1] != []:
                self.addChild(element, child, el[1])

    def addChildGraph(self, element, child_graph):
        """
        Adds a subgraph as a child of an element
        Example: element = x
        child_graph   self      self after this
          b            a              a
         / \          / \            / \
        c   d        x   y          x   y
                                   /
                                  b
                                 / \
                                c   d
        """
        for el in self.graph:
            if el[0] == element:
                el[1].append(child_graph)

    def merge(self, other_graph):
        """
        Given two graphs merge them by the root

        other    self        self after merger
          a       a                 a
          |      / \              / | \
          x     y   z            x  y  z
        """
        for el in self.graph:
            children = other_graph.getChildren(el[0])
            for n in children:
                self.addChildGraph(el[0], n)

    def replace(self, other_graph):
        """
        Given two graphs, replace current root elements by
        others element.
        other       self          self after replace
          a          a   b               a    b
         / \         |   |              / \   |
        x   y        z   i             x   y  i
        """
        for el in self.graph:
            other_el = other_graph.getRootElement(el[0])
            if len(other_el) > 0:
                self.graph.remove(el)
                self.graph.append(other_el)
                break

    def remove(self, element, sub_graph=None):
        """
        Given a node remove itself and its children
        """
        if sub_graph is None:
            sub_graph = self.graph
        
        markForDel = None
        for el in sub_graph:
            if el[0] == element:
                markForDel = el
                break
            elif el[1] != []:
                self.remove(element, el[1])
        
        if markForDel is not None:
            sub_graph.remove(el)

    def append(self, other_graph):
        """
        Given another graph append it to the root.
        other    self           self after append
        c         a              c
        |        / \             |
        a       x   y            a
                                / \
                               x   y
        """
        leaves = other_graph.getLeaves()
        graph2 = Graph()
        graph2.graph = deepcopy(other_graph.graph)

        for leaf in leaves:
            children = self.getChildren(leaf)
            graph2.addLeaves(leaf, children)
            self.remove(leaf)
        
        self.addRootGraph(graph2)

    def addLeaves(self, element, leaves, sub_graph=None):
        """
        Adds leaves to element.
        Ex: element = y
        a            a
        |            |
        x            x
                     |
                     y

        """
        if sub_graph is None:
            sub_graph = self.graph

        for el in sub_graph:
            if el[1] == []:
                if el[0] == element:
                    el[1] += leaves
            else:
                self.addLeaves(element, leaves, el[1])

    def getLeaves(self, sub_graph=None):
        """
        Returns all leaves from a graph
        Example
             self     
              a
             / \
            x   y
           /
          b
         / \
        c   d

        Will return ['c', 'd', 'y']
        """
        if sub_graph is None:
            sub_graph = self.graph

        leaves = []
        for el in sub_graph:
            #this element has no children
            if el[1] == []:
                leaves.append(el[0])
            else:
                leaves += self.getLeaves(el[1])
        
        return leaves

    def isDescendant(self, parent_element, child_element, sub_graph=None, alreadyFoundParent=False):
        """
        Given a parent_element searches if child_element is a descendant
        of that parent
        Example: parent_element = a      child_element = w
        self
                 a
                / \
               b   c
              / \  |
             x   y w
        
        Will return True in this case since a is a grandson of w.
        """
        if sub_graph is None:
            sub_graph = self.graph

        for el in sub_graph:

            if el[0] == child_element:
                #found the child after found the parent
                if alreadyFoundParent:
                    return True
                else: #found the child before found the parent
                    return False
            
            elif el[0] == parent_element:
                #Found the parent!
                #But he has no children
                if el[1] == []:
                    return False
                else:
                    #Have children let search for child_element under the parent!
                    return self.isDescendant(parent_element, child_element, el[1], True)
            elif el[1] != []:
                return self.isDescendant(parent_element, child_element, el[1], alreadyFoundParent)
        
        return False

    def getDescendants(self, element, sub_graph=None, alreadyFoundParent=False):
        """
        Given a parent_element searches returns a list with all child_elements whose parent is parent_element.
        Example: element = a
        self
                 a
                / \
               b   c
              / \  |
             x   y w
        
        Will return ['b', 'y', 'x']
        """
        if sub_graph is None:
            sub_graph = self.graph

        descendents = []

        for el in sub_graph:
            if el[0] == element:
                if el[1] != []:
                    descendents += self.getDescendants(element, el[1], True)
            elif alreadyFoundParent:
                descendents.append(el[0])
                
                

    def __repr__(self):
        return "<Graph " + str(self.graph) + " >"
