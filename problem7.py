# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 13:30:59 2017

@author: dmatt
"""

from matplotlib import pyplot
from matplotlib import style
import time
import numpy
import random

style.use('ggplot')
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
        self.viruses = [virus for virus in self.viruses if not virus.doesClear()]
        popDensity = self.getTotalPop()/float(self.maxPop)
        for virus in self.viruses[:]:
            try: self.viruses.append(virus.reproduce(popDensity))
            except NoChildException: continue
        return self.getTotalPop()
    
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        # TODO
        if type(resistances) != dict: 
            raise TypeError("ResistantVirus.__init__(): expected dict for type(resistances)")
        if not 0 < mutProb <= 1:
            raise ValueError("ResistantVirus.__init__(): expected a float between 0-1")
        SimpleVirus.__init__(self,maxBirthProb,clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO    
        try:
            return self.resistances[drug]
        except KeyError:
            return False
            
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO    
        if type(activeDrugs) != list: 
            raise TypeError("reproduce(): expected list for type(activeDrugs)")
        #if there is no drug, the virus is completely resistant
        #if there is a drug(s), check if its resistant to all drugs, due to cocktails
        resistant = bool(len(activeDrugs) == 0) or not bool([drug for drug in activeDrugs if self.resistances[drug] == False])
        if resistant and random.random() <= self.maxBirthProb * (1 - popDensity):
            child_resistances = self.resistances.copy()
            for drug,resistance in self.resistances.iteritems():
                if random.random() < self.mutProb:
                    child_resistances[drug] = not resistance
            return ResistantVirus(self.maxBirthProb,self.clearProb,child_resistances,self.mutProb)    
        else: raise NoChildException
        
    
class Patient(SimplePatient):
    """Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes. """
    
    def __init__(self, viruses, maxPop):
        """Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).  
        
        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the maximum virus population for this patient (an integer)
        """
        # TODO
        SimplePatient.__init__(self,viruses,maxPop)
        self.drugs_given = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO
        if type(newDrug) != str:
            raise TypeError("addPrescription():expected string for type(newDrug)")
        if newDrug not in self.drugs_given:
            self.drugs_given.append(newDrug)
    #accessors
    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO
        return self.drugs_given
    
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        if type(drugResist) != list:
            raise TypeError("getResistPop():expected list for type(drugResist)")
        i,j,resistant_viruses = 0,0,0
        while i < len(self.viruses) and j < len(drugResist):
            if not self.viruses[i].getResistance(drugResist[j]):
                i += 1
            else:
                j += 1
                if j >= len(drugResist):
                    resistant_viruses += 1
                    i += 1
                    j = 0
        return resistant_viruses
    
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO
        self.viruses = [virus for virus in self.viruses if not virus.doesClear()]
        popDensity = self.getTotalPop()/float(self.maxPop)
        for virus in self.viruses[:]:
            try: self.viruses.append(virus.reproduce(popDensity, self.getPrescriptions()))
            except NoChildException: continue
        return self.getTotalPop()
    
#
# PROBLEM 5
#
def createPatient():
    maxPop = 1000
    maxBirthProb,clearProb,mutProb = 0.1,0.05,0.005
    resistances = {'guttagonol':False,'grimpex':False}
    viruses = [ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)]*100
    return Patient(viruses, maxPop)    

def trialForNTimeSteps(n):
    """Takes n = number of time steps and simulates
    the virus population for 30 patients, returning the all populations"""
    stop = 150 + n + 150
    total_pop,resist_pop,gut_pop,grimp_pop = [0]*stop,[0]*stop,[0]*stop,[0]*stop
    for i in xrange(20):
        PatientZero = createPatient()
        total_pop[0] += PatientZero.getTotalPop()
        for i in xrange(1,stop):
            if i >= 150: PatientZero.addPrescription('guttagonol')
            if i >= 150 + n: PatientZero.addPrescription('grimpex')
            total_pop[i] += PatientZero.update()
            resist_pop[i] += PatientZero.getResistPop(['guttagonol','grimpex'])
            gut_pop[i] += PatientZero.getResistPop(['guttagonol'])
            grimp_pop[i] += PatientZero.getResistPop(['grimpex'])

    return [t/20 for t in total_pop],[r/20 for r in resist_pop],\
            [gut/20 for gut in gut_pop],[grimp/20 for grimp in grimp_pop]



 
def problem4_6():
    """
    Runs simulations and plots graphs for problem 6

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO
    #delay of 300
    start = time.time()
    virus_population,resistant_pop,gut_resistant,grimp_resistant = trialForNTimeSteps(0)
    end = time.time()
    print "Took",int(end - start)/60,"minute(s)"
    
    pyplot.plot(virus_population,label = "Total Virus Population")
    pyplot.plot(resistant_pop,label = "Total Resistant Population")
    pyplot.plot(gut_resistant,label = "guttogonol Resistant Population",color='k')
    pyplot.plot(grimp_resistant,label = "grimpex Resistant Population",color='g')
    pyplot.scatter(150,virus_population[150],label = "guttagonol Induced",color='k')
    pyplot.scatter(150,virus_population[150],label = "grimpex Induced",color='g')
    pyplot.title("Effects of Delaying Treatment by 0 Time Steps")
    pyplot.ylabel("Total Virus Population")
    pyplot.xlabel("Time")
    pyplot.legend()
    pyplot.show()        

problem4_6()        








