# -*- coding: latin1 -*-
#102618-OOMS AURELIEN-BA1 INFORMATIQUE-G2/CountingTree.py
from Urn import *
from myAssert import *
from BinaryTree import *
from Stack import *

import math

class CountingTree:

    def toRegularTree(self,numberOfChildren = 2):   #1) je ne vois pas en quoi le second paramètre est nécessaire,
                                                    #   le résultat de la méthode n'est d'ailleurs pas logique si
                                                    #   numberOfChildren est différent de 2
                                                    #   je ne lui ai donné aucun rôle dans cette méthode afin d'éviter de potentielles erreurs
                                                    #2) je ne crée pas l'arbre binaire à partir de l'arbre courant
                                                    #   car si jamais (et ce n'est pas le cas dans les tests fournis)
                                                    #   on désire créer un arbre m-aire avec m > 2 en tant qu'arbre courant,
                                                    #   on sera obligé de partir du niveau le plus bas.. cad l'urne de départ..
	
        stack = Stack()
        current = self.__urn
        stack.push(current)
	    
        while current.getSize() != 1:           #push chaque niveau de l'arbre sur le stack
	    
            current = current.getCompressed(2)
            stack.push(current)
            
	
        f = Queue()
        root = stack.pop().getBallot(0)     #initialisation à la racine de l'arbre (taille du premier niveau = 1)
        tree = BinaryTree(str(root)+str(root.getIdentifier()))
        f.insert(tree)
        
        while not stack.isEmpty():          #tant qu'il y a des niveaux à rajouter
                     
            level = stack.pop()                 #niveau à lier au niveau précédent
            i = 0
            toModify = f.size()                 #nombre de noeuds du niveau précédent
            while i < toModify:                 #on ajoute un fils gauche et un fils droit à chacun de ces noeuds(un gauche minimum)       
                n = f.remove()
                node = level.getBallot(i*2)              #indice du fils gauche = indice du père * 2
                n.insertLeft(str(node) + str(node.getIdentifier()))     #ajout d'un fils gauche
                f.insert(n.getLeftChild())                              #on ajoute le fils à la liste des noeuds qui doivent être modifiés
                if i*2+1 < level.getSize():                
                    node = level.getBallot(i*2+1)        #indice du fils droit = indice du père * 2 + 1
                    n.insertRight(str(node) + str(node.getIdentifier()))#ajout d'un fils droit
                    f.insert(n.getRightChild())                         #on ajoute le fils à la liste des noeuds qui doivent être modifiés
                i += 1

        return tree
        
    def __init__(self,urn,m):
    
        self.__urn = urn
        self.m = m
	    
    def tally(self):
	
        return self.__urn.tally()
        
    def __repr__(self):
        m = self.m
        if m == 1 or m == 0:
            raise Exception("Si le facteur de compression est de 0 ou de 1, il est impossible de créer un arbre fini.")
        stack = Stack()
        current = self.__urn
        stack.push(current)
	    

        while current.getSize() != 1:           #push chaque niveau de l'arbre sur le stack
	    
            current = current.getCompressed(m)
            stack.push(current)
            
	
        f = Queue()
        root = stack.pop().getBallot(0)         #initialisation à la racine de l'arbre (taille du premier niveau = 1)
        tree = Forest(str(root))

        f.insert(tree)
        
        while not stack.isEmpty():              #tant qu'il y a des niveaux à rajouter
                     
            level = stack.pop()                     #niveau à lier au niveau précédent
            i = 0
            toModify = f.size()                     #nombre de noeuds du niveau précédent
            while i < toModify:
                
                n = f.remove()
                node = level.getBallot(i*m)
                n.modifyChild(str(node))    #on ajoute un premier fils
                f.insert(n.getChild())                                  #on le mémorise pour modifier son fils par après
                                    
                j=1
                n = n.getChild()
                while (j < m and (i*m)+j < level.getSize()):            #on ajoute m-1 frère(s) à ce fils
                    node = level.getBallot(i*m+j)
                    n.modifyBrother(str(node))  #on ajoute un frère
                    f.insert(n.getBrother())                                #on le mémorise pour modifier son fils par après
                    n = n.getBrother()                                      #n devient le frère de n afin de lui ajouter un frère à l'itération suivante
                    j+=1

                i += 1
                
        tree.niveau(m)
        return ""
    
        
        
class Queue :
    def __init__(self):
        self.items = []
    def head(self):
        return self.items[len(self.items)-1]
    def isEmpty (self):
        return self.items == []
    def insert(self,item):
        self.items.insert(0,item )
    def remove(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    def __repr__(self):
        print self.items
        return ""
    def isFullOfNone(self):
        test = True
        i = 0
        while i < self.size() and test:
            if self.items[i] != None:
                test = False
            i += 1
        return test
        
class Forest:

    def __init__(self,item):
        self.info = item
        self.child = None
        self.brother = None
    def getRootVal(self):
        return self.info
    def setRootVal(self,item):
        self.info = item       
    def getChild(self):
        return self.child
    def getBrother(self):
        return self.brother
    def modifyChild(self,newNode):
        self.child = Forest(newNode)
    def modifyBrother(self,newNode):
        self.brother = Forest(newNode)


    def niveau(self,m):#affichage par niveau
        f = Queue()
        f.insert(self)
        i = 0
        j = 0
        af = 45
        tailleNiveauPrecedent = 0
        print "*"*af+"\nLevel " + str(j)
        while not f.isEmpty():
            n = f.remove()
            
            while n != None:
                
                print n.getRootVal(),
                f.insert(n.getChild())
                n = n.getBrother()
                i += 1
            if i > m*(tailleNiveauPrecedent-1):#tailleNiveauPrecedent-1 noeuds pécédents ont m fils et le dernier noeud précédent à au moins un fils 
                print "\n"+"*"*af,
                tailleNiveauPrecedent = i
                i = 0
                j+= 1
                if not f.isFullOfNone():
                    print "\nLevel " + str(j)
                    
if __name__ == '__main__':
	from Urn import *
	from Ballot import *
	from Constants_Test import *
	from Functions_Test import *
	myUrn = randomFilledUrnCreator()
	myCT = CountingTree(myUrn,2)
	print(myCT)
