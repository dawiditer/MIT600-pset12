# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 14:56:27 2017

@author: dmatt
"""
# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        # TODO
        if 0 < maxBirthProb < 1 and 0 < clearProb < 1:
            raise ValueError("value should be between 0 and 1")
        self.maxBirthProb = float(maxBirthProb)
        self.clearProb = float(clearProb)
    
    #determines the state of a virus, has it been cleared or not
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        # TODO
        #create a random number, if that random number is the probability,
        #clear the virus
        #since its a float, am going to use epsilon for close enough
        #if the random_float is close enough to self.clearProb, return True
        return abs(random.random() - self.clearProb) < 0.01
    
    #check if the surviving virus will reproduce or not
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # TODO
        #use this probability: self.maxBirthProb * (1 - popDensity) to reproduce an offspring
        #to make a choice based on probability, use random() <= probability
#        if random.random() <= self.maxBirthProb * (1 - popDensity):
#            #if its lucky, create a new instance of the virus with the same details
#            return SimpleVirus(self.maxBirthProb,self.clearProb)
#        else:
#            raise NoChildException
        #the idea is using random numbers and asking where they fall, either
        #in the probability range or outside the probability range
        #modded
        if random.random() > self.maxBirthProb * (1 - popDensity):
            raise NoChildException
        return SimpleVirus(self.maxBirthProb,self.clearProb)
        
class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO
        assert type(viruses) != list and type(maxPop) != int
        self.viruses = viruses
        self.maxPop = maxPop
    #accessor
    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        # TODO        
        return len(self.viruses)
    
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO    
        #survive or die, for each virus
        #use anonymous copy to correctly mutate the list
        for virus in self.viruses[:]:
            if virus.doesClear(): self.viruses.remove(virus)
        
        #calculate population density
        #ratio of virus population to maximum virus population
        popDensity = self.getTotalPop()/float(self.maxPop)
        
        #reproduce or no?
        for virus in self.viruses[:]:
            try:
                self.viruses.append(virus.reproduce(popDensity))
            except NoChildException: continue
        #return the new population
        return self.getTotalPop()

                
            