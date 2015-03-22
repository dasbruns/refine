#!/usr/bin/env python
import refine
from lxml import etree as ET

def sum(l):
    if len(l) == 1:
        return l[0]
    return l[0]+sum(l[1:])

def cycle(path):
    return path[path.index(path[-1]):]

def detectSame(paths):
    trueCircs = [paths[0]]
    dic = {paths[0][-1]:[paths[0]]}
    seen = [cycle(paths[0])]
    for i in paths[1:]:
        cyc = cycle(i)
        if cyc not in seen:
            if i[-1] not in dic:
                dic[i[-1]]=[i]
            else:
                dic[i[-1]] += [i]
            trueCircs.append(i)
            seen.append(cyc)
    return trueCircs, dic

if __name__ == '__main__':
    stat = refine.makeTrees()
    root = stat.pitTree.getroot()
    sm = root.find('StateModel')
    container = []
    diction = {}
    IDtoNode = {}
    for state in sm:
        if not '00' in state.attrib['name']:
            obj = refine.Node(state)
            diction.update({obj.name:obj})
            container.append(obj)
    for node in container:
        node.nextNodes = refine.Node.getNextNodes(node,diction)
        #print(node)
    freqOLD = len(container)*[0]
    for obj in container:
        for nxt in obj.nextNodes:
            freqOLD[nxt.identifier] += 1
    freq = len(container)*[0]
    container,diction = refine.Node.sanitize(container,diction)
    for obj in container:
        IDtoNode.update({obj.identifier:obj})
    #print(len(container))
    for node in container:
        if node.nextNodes == []:
            print(node)
    for obj in container:
        for nxt in obj.nextNodes:
            freq[nxt.identifier] += 1
    for obj in container:
        if obj.state.attrib['name'] == '[-1];[-1];[-1]':
            start = obj
    #print(diction[IDtoNode[4].name])
    #print(diction)
    #exit()
    #start.identifier='s'
    #container[0].identifier=0
    #container[1].identifier=1
    #container[2].identifier=2
    #container[3].identifier=3
    #container[4].identifier=4
    #container[5].identifier=5
    #container[6].identifier=6
    #start.nextNodes = [container[0]]
    #container[0].nextNodes = [container[1]]
    #container[1].nextNodes = [container[2]]
    #container[2].nextNodes = [container[0]]
    #container[2].nextNodes += [container[3]]
    #container[2].nextNodes += [container[4]]
    #container[2].nextNodes += [start]
    #container[3].nextNodes = [container[2]]
    #container[3].nextNodes += [container[5]]
    #container[4].nextNodes = [container[5]]
    #container[5].nextNodes = [container[6]]
    #container[5].nextNodes += [container[3]]
    #container[6].nextNodes = [container[4]]
    #container[6].nextNodes += [start]
    #print(refine.Node.tostr(container[0],0,True))
    #print(refine.Node.tostr(container[1],0,True))
    #print(refine.Node.tostr(container[3],0,True))

    #circles = refine.Node.getCircles(start,maxSearchDepth=5)
    #print(len(circles))
    #circles = refine.Node.getCircles(start,maxSearchDepth=7)
    #print(len(circles))
    print('searching the machine')
    circles = []
    c = container[:]
    circleNodes = []
    count = 0
    for depth in range(1,13,2):
     #   print(depth)
        for node in c:
            circs = refine.Node.getCircles(node,maxSearchDepth=2)
            if circs != []:
                circles.append(circs)
                circleNodes.append(c.pop(c.index(node)))
                count += 1
        #circles += refine.Node.getCircles(node,maxSearchDepth=4)
    #for i in circles:
     #   print(i,IDtoNode[i[0][0]])
    print(len(c),count)
    print(len(container))
    print(IDtoNode[start.identifier])
    print(len(circleNodes))
    routes = []
    for node in circleNodes:
        routes.append(refine.Node.pathFinder(start,node,IDtoNode))
    for route in routes:
        print('\n'+20*'='+'\n')
        #print('searching for ',route)
        for ID in route:
            print(IDtoNode[ID])
    #print(IDtoNode[10])#,'\n',IDtoNode[41])
    newStateModel = ET.Element('StateModel')
    for node in routes[0]:
        newStateModel.append(IDtoNode[node].state)
    exit()
    print('reducing')
    trueCircs,dic = detectSame(circles)
    print(len(trueCircs))
    for i in dic.keys():
        print(i,len(dic[i]))
    #for node in container:
    #    tmp = refine.Node.getCircles(node,maxSearchDepth=6)
    #    if not tmp == []:
    #        circles += tmp
    #print(len(circles))
    #trueCircles = [circ for circ in circles if circ[0] == circ[-1]]
    #print(len(trueCircles))
    #l6 = [true for true in trueCircles if len(true) == 5]
    #tree = ET.ElementTree(ET.Element('cycle'))
    #cycle = tree.getroot()
    #for nodeID in l6[0]:
    #    cycle.append((IDtoNode[nodeID].state))
    #    #print(str(ET.tostring(IDtoNode[nodeID].state,pretty_print=True)))
    #tree.write('out', pretty_print=True)


