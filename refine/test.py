#!/usr/bin/env python
from lxml import etree as ET

def stats():
    print('world')
    tree = ET.parse('pitClient.xml')
    root = tree.getroot()
    print(root.tag)
    print('\\\\')
    stateModel = root.find('StateModel')
    print(2*' '+stateModel.tag)
    print(2*' '+'\\\\')
    container = []
    for state in stateModel:
        print(4*' '+state.attrib['name'])
        container.append(state)
        if state.attrib['name'] == '[-1];[-1];[-1]':
            start = state

    tree = ET.ElementTree(ET.Element('paths'))
    paths = tree.getroot()
    paths.append(ET.Element(start.attrib['name']))
    tree.write('out', pretty_print=True)
    exit()
    getPaths(start, container, paths)



def getPaths(curRoot, container, path):
        #if '00' in start.attrib['name']:
        #    path +='-> end'
        #    path += '\t' + str(d) + '\n'
        #    f = open('paths','a')
        #    f.write(path)
        #    f.close()
        #    return
        for child in start:
            if child.attrib['type'] == 'changeState':
                for i in container:
                    #find nextState for changeState reference
                    if i.attrib['name'] == child.attrib['ref']:
                        nextState = i
                        break
                #only go if not already been there
                if i.attrib['name'] not in path:
                    curRoot.append(i)
                    nextRoot = curRoot.find(i)
                    getPaths(nextRoot,container,path)
                else:
                    curRoot.append(ET.Element('CYCLE'))
                return
                #print(child.tag,child.attrib)

if __name__=="__main__":
    print('hello'),
    stats()
