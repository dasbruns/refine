class Node(object):
    identifier = 0

    def getNextNodes(node, diction):
        nextNodes = []
        for child in node.state:
            if child.attrib['type'] == 'changeState':
                if child.attrib['ref'] in diction:
                    nextNodes.append(diction[child.attrib['ref']])
        return nextNodes

    def sanitize(container,diction):
        goon = False
        for node in container:
            if node.nextNodes == []:
                #print('removing '+ str(node))
                container.remove(node)
                del diction[node.name]
                goon = True
        for node in container:
            for nextNode in node.nextNodes:
                if nextNode.name not in diction:
                    #print('deleting '+ str(nextNode) + ' in ' + str(node))
                    node.nextNodes.remove(nextNode)
                    goon = True
        if goon == True:
            #print(20*'#'+'\nre-iterating\n'+20*'#'+'\n')
            Node.sanitize(container,diction)
        return container,diction

    def getCirclesOLD(node, path=[],depth=0, maxSearchDepth=5):
        #print('expanding '+Node.tostr(node,depth=1)+' on path '+str(path))
        circles = []
        if node.identifier in path or depth > maxSearchDepth:
            if depth <= maxSearchDepth:
                #print('circle detected: '+ str(path+[node.identifier]))
                #print(path)
                return [path + [node.identifier]]
            return circles
        for child in node.nextNodes:
            circles += Node.getCircles(child,path[:]+[node.identifier],depth+1,maxSearchDepth)
        return circles

    def getCircles(node, path=[],depth=0, maxSearchDepth=3):
        #print('expanding '+Node.tostr(node,depth=1)+' on path '+str(path))
        circles = []
        if path != [] and node.identifier == path[0] or depth > maxSearchDepth:
            if depth <= maxSearchDepth:
                #print('circle detected: '+ str(path+[node.identifier]))
                #print(path)
                return path + [node.identifier]
            return circles
        for child in node.nextNodes:
            circles += Node.getCircles(child,path[:]+[node.identifier],depth+1,maxSearchDepth)
        return circles

    def pathFinder(start, node, dic):
        toExpand = [[start.identifier]]
        visited = [start.identifier]
        while toExpand != []:
            #print(toExpand[0])
            path = toExpand.pop(0)
            curNode = dic[path[-1]]
            #print(curNode)
            if curNode != node:
                for nxt in curNode.nextNodes:
                    if nxt.identifier not in visited:
                        toExpand.append(path+[nxt.identifier])
                        visited.append(nxt.identifier)
            else:
                return path

    def identifySame(circ, circles):
        #print('testing ', circ,'on:')
        #for i in circles:
            #print(i)
        new = False
        for circs in circles:
            for i in circ:
                if i not in circs:
                    new = True
                    break
            if new == False:
                return False
            new = False
        return True


    def __init__(self,state):
        self.identifier = Node.identifier
        self.name = state.attrib['name']
        self.nextNodes = []
        self.state = state
        Node.identifier += 1

    def __str__ (self):
        return Node.tostr(self)#,raw=True)

    def tostr(self, depth=1, raw=False,peach=(not True)):
        if depth != 1:
            s = peach*str(self.identifier) + raw**peach*' ' + raw**peach*self.name + raw*peach*' goes to' 
        else:
            s = peach*str(self.identifier) + raw**peach*' ' + raw**peach*self.name 
        if depth != 1:
            for nxt in self.nextNodes:
                s += peach*'\n\t' + peach*Node.tostr(nxt,1)
        return s
