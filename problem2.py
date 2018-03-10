# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 17:13:12 2017

@author: dmatt
"""
# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

from matplotlib import pyplot
import numpy
import random

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
        if not 0 < maxBirthProb < 1 and 0 < clearProb < 1:
            raise ValueError("value should be between 0 and 1")
        self.maxBirthProb = float(maxBirthProb)
        self.clearProb = float(clearProb)
    
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        # TODO
        return abs(random.random() - self.clearProb) < 0.01
    
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
        if type(viruses) != list and type(maxPop) != int: raise TypeError("Wrong input types")
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
        for virus in self.viruses[:]:
            if virus.doesClear(): self.viruses.remove(virus)
        popDensity = self.getTotalPop()/float(self.maxPop)
        for virus in self.viruses[:]:
            try:
                self.viruses.append(virus.reproduce(popDensity))
            except NoChildException: continue
        return self.getTotalPop()

#
# PROBLEM 2
#
#==============================================================================
# SimplePatient should be instantiated with the following parameters: 
# viruses, a list of 100 SimpleVirus instances 
# maxPop, Maximum Sustainable Virus Population = 1000
# maxBirthProb, Maximum Reproduction Probability for a Virus Particle = 0.1
# clearProb, Maximum Clearance Probability for a Virus Particle = 0.05 
#==============================================================================
def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    # TODO
    #create a patient with 100 virus particles
    maxPop,maxBirthProb,clearProb = 1000,0.1,0.05
    viruses = [SimpleVirus(maxBirthProb,clearProb)]*100
    PatientZero = SimplePatient(viruses,maxPop)
    
    population_over_time = [PatientZero.getTotalPop()]
    #simulate the virus population after 300 timesteps
    for i in xrange(1,300):
        #update the virus population
        PatientZero.update()
        #store the new virus population
        population_over_time.append(PatientZero.getTotalPop())

    #plot the population vs time
    #if you omit x, it will plot based on len(y)
    pyplot.plot(population_over_time)
    pyplot.title("Virus Population vs Time")
    pyplot.xlabel("Time(t)")
    pyplot.ylabel("Virus Population")

problem2()
#
#for pop in problem2():
#    print pop