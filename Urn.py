# -*- coding: latin1 -*-
#102618-OOMS AURELIEN-BA1 INFORMATIQUE-G2/Urn.py
from Ballot import *
from myAssert import *
from copy import deepcopy

class Urn:
    
    def __init__(self):               
        self.__ballots = []
 
    def addBallot(self,b):   
        self.__ballots.append(b)
    
    def getSize(self):   
        return len(self.__ballots)
    
    def tally(self):            
        return self.getCompressed(len(self.__ballots)).__ballots[0]
        
    
    def assertInvariant(self):
        
        for i in range(len(self.__ballots)-1):
            assert(self.getBallot(i).numberOfPossibleChoices == self.getBallot(i+1).numberOfPossibleChoices)
    
        
        
    def getCompressed(self,f):
        try:
            f = int(f)
            
        except ValueError:
            
            raise Exception("Le facteur de compression doit être un entier positif.")
        
        if f < 0:#si f = 1 ou 0 getCompressed renvoie une "deepcopy" (les identifier ont été modifiés) de l'urne donnée en paramètre
            raise Exception("Le facteur de compression doit être un entier positif.")
                
                
        newUrn = Urn()
        i = 0        
        while i < self.getSize():
        
            compressedBallot = deepcopy(self.__ballots[i]) #pour modifier l'identifiant au cas où
            i+=1
            
            for j in range(f-1):
                try:
                    compressedBallot += self.__ballots[i]
                    i+=1
                except:
                    break
                    
            if compressedBallot == self.__ballots[i-1]:   #on modifie l'identifiant si le ballot résultat est égal au précédent
                compressedBallot.identifier = Ballot.getNewIdentifier()
            newUrn.addBallot(compressedBallot)

    
        return newUrn
        
        
    def getBallot(self,index):
    
        return self.__ballots[index]
             
if __name__ == '__main__':
	from Constants_Test import *
	from Functions_Test import *
	u = Urn()
	# print(u)
	b = randomFilledBallotCreator()
	u.addBallot(b)
	#for i in range(5):
		#u.addBallot(randomFilledBallotSimilator(b))	#randomFilledBallotSimilator() n'existe pas
	print(u)
	# print(u.getCompressed(1))
	# print(u.getCompressed(2))
	print(u.getCompressed(3))
