# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 11:08:15 2017

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
        #if there is a drug(s), check if its resistant to all drugs
        resistant = len(activeDrugs) == 0 or not bool([drug for drug in activeDrugs if self.resistances[drug] == False])
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
            try:
                self.viruses.append(virus.reproduce(popDensity, self.getPrescriptions()))
            except NoChildException: continue
        return self.getTotalPop()
    
#
# PROBLEM 5
#
def createPatient():
    maxPop = 1000
    maxBirthProb,clearProb,mutProb = 0.1,0.05,0.005
    resistances = {'guttagonol':False}
    viruses = [ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)]*100
    return Patient(viruses, maxPop)    

def trialForNTimes(n):
    """Takes n = number of time steps and simulates
    the virus population for 25 patients, returning the mean population"""
    pool_pop = []
    for i in xrange(25):
        PatientZero = createPatient()
        population_after_time = [PatientZero.getTotalPop()]
        
        #trial for 300 time steps
        for i in xrange(1,n + 150):
            if i >= n:
                #introduce drug
                PatientZero.addPrescription('guttagonol')
            population_after_time.append(PatientZero.update())
            
        pool_pop.append(PatientZero.getTotalPop())
    return pool_pop

def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    # TODO
#    start = time.time()
    hist1 = numpy.array(trialForNTimes(0))
#    hist2 = numpy.array(trialForNTimes(75))
#    hist3 = numpy.array(trialForNTimes(150))
#    hist4 = numpy.array(trialForNTimes(300))
#    end = time.time()
#    print (int(end - start))/60,"minutes"

#    bins = numpy.array(range(0,1100,100))
    pyplot.hist(hist1)
    pyplot.yticks(range(0, 30, 5))
    pyplot.title("Delayed Treatment by 150 Timesteps")
    pyplot.xlabel("Total Virus Populations")
    pyplot.ylabel("Number of Patients")
    pyplot.show()
problem5()









