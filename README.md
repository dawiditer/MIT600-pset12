# Simulating virus population dynamics
In this problem set, you will design and implement a stochastic simulation of virus population dynamics.
There are medications for the treatment of infection by viruses; however, viruses may become resistant to one drug, sometimes to
multiple drugs due to mutations. Despite not having gone to medical school (or maybe because of this), you can still decide on a
good drug treatment regimen by observing how the virus population responds to the introduction of different drugs. We have been
unable to reserve a bio lab for 6.0

### Background: Viruses, Drug Treatments, and Computational Models ###
Viruses such as HIV and Influenza represent a significant challenge to modern medicine. One of the reasons that they are so difficult
to treat is because of their ability to evolve.
As you may know from introductory biology classes, the traits of an organism are determined by its genetic code. When organisms
reproduce, their offspring will inherit genetic information from their parent. This genetic information will be modified, either due to
mixing of the two parents’ genetic information, or through errors in the genome replication process, thus introducing diversity into a
population.

Viruses are no exception and carry and propogate their own genetic information. Two characteristics of viruses make them
particularly difficult to treat. The first is that their replication mechanism often lacks the error checking mechanisms that is present in
more complex organisms. Secondly, viruses replicate extremely quickly, orders of magnitude faster than humans. Thus, while we
may be used to thinking of evolution as a process which occurs over long time scales, populations of viruses can undergo substantial 
evolutionary changes within a single patient over the course of treatment.
These two characteristics allow a virus population to quickly acquire genetic resistance to therapies over the course of a treatment.

In this problem set, we will make use of simulations to explore the effect of introducing drugs on the virus population and determine
how best to address these treatment challenges within a simplified model.
Computational modeling has played an important role in the study of viruses such as HIV (for example, see this paper, by Time
Magazine’s Man of the Year, David Ho). In this problem set, we will implement a highly simplified stochastic model of virus
population dynamics in vivo. Many details have been swept under the rug (host cells are not explicitly modeled and the size of the
population is several orders of magnitude less than the size of actual virus populations). Nevertheless, our model exhibits biologically
relevant characteristics and will give you a chance to analyze and interpret simulation data. 

### Problem 1: Implementing a Simple Simulation (No Drug Treatments) ###
We start with a trivial model of the virus population - the patient does not take any drugs and the viruses do not acquire resistance to
drugs. We simply model the virus population in a patient as if it were left untreated.
At every time step of the simulation, each virus particle has a fixed probability of being cleared (eliminated from the patient’s body).
If the virus particle is not cleared, it is considered for reproduction. Unlike the clearance probability, which is constant, the probability
of a virus particle reproducing is a function of the virus population. With a larger virus population, there are fewer resources in the
patient’s body to facilitate reproduction, and the probability of reproduction will be lower. One way to think of this limitation is to
consider that virus particles need to make use of a the patient’s cells to reproduce, they cannot reproduce on their own. As the virus
population increases, there will be fewer available host cells for viruses to utilize for reproduction.

To implement this model, you will need to fill in the `SimpleVirus` class, which maintains the state of a single virus particle, and the
`SimplePatient` class, which maintains the state of a virus population associated with a patient. The `update()` method in the
`SimplePatient` class is the “inner loop” of the simulation. It modifies the state of the virus population for a single time step and
returns the total virus population at the end of the time step.

`update()` should first decide which virus particles are cleared and which survive by making use of the `doesClear()` method of
each `SimpleVirus` instance and update the collection of `SimpleVirus` instances accordingly. `update()` should then call the
`reproduce()` method for each virus particle. Based on the population density, `reproduce()` should either return a new instance
of `SimpleVirus` representing the offspring of the virus particle, or raise a `NoChildException` indicating that the virus particle
does not reproduce during the current time step. The `update()` method should update the attributes of the patient appropriately
under either of these conditions. After iterating through all the virus particles, the `update()` method returns the number of virus
particles in the patient at the end of the time step.
The `reproduce()` method in `SimpleVirus` should produce an offspring by returning a new instance of `SimpleVirus` with
probability:
```Python
self.maxBirthProb * ( 1 - popDensity)
```
`self.maxBirthProb` is the birth rate under optimal conditions (the virus population is negligible relative to the available host cells).
`popDensity` is defined as the ratio of the current virus population to the maximum virus population for a patient and should be
calculated in the `update()` method of the `SimplePatient` class. 

### Problem 2: Running and Analyzing a Simple Simulation (No Drug Treatments) ###
You should start by understanding the population dynamics before introducing any drug. Fill in the function `problem2()`. This
method should instantiate a `SimplePatient` and repeatedly call the `update()` method to simulate changes in the virus population
over time. Save the population values over the course of the simulation and use **pylab** to plot the virus population as a function of
time. Be sure to title and label your plot.

`SimplePatient` should be instantiated with the following parameters:
* `viruses`, a list of 100 `SimpleVirus` instances
* `maxPop`, Maximum Sustainable Virus Population = 1000

Each `SimpleVirus` instance in the viruses list should be initialized with the following parameters:
* `maxBirthProb`, Maximum Reproduction Probability for a Virus Particle = 0.1
* `clearProb`, Maximum Clearance Probability for a Virus Particle = 0.05 

### Problem 3: Implementing a Simulation With Drugs ###
In this problem, we consider the effects of both administering drugs to the patient and the ability of virus particle offspring to inherit
or mutate genetic traits that confer drug resistance.
As the virus population reproduces, mutations will occur in the virus offspring, adding genetic diversity to the virus population. Some
virus particles gain favorable mutations that confer resistance to drugs.

Drugs are given to the patient using the `Patient` class’s `addPrescription()` method. What happens when a drug is introduced?
The drugs we consider do not directly kill virus particles lacking resistance to the drug, but prevent those virus particles from
reproducing (much like actual drugs used to treat HIV). Virus particles with resistance to the drug continue to reproduce normally.
In order to model this effect, we introduce a subclass of `SimpleVirus`, `ResistantVirus`. `ResistantVirus` maintains the state
of a virus particle’s drug resistances, and account for the inheritance of drug resistance traits to offspring.

We also need a representation for a patient which accounts for the use of drug treatments and manages a collection of
`ResistantVirus` instances. For this we introduce the `Patient` class, which is a subclass of `SimplePatient`. `Patient` must
make use of the new methods in `ResistantVirus()` and maintain the list of drugs that are administered to the patient. 

### Problem 4: Running and Analyzing a Simulation with a Drug ###
In this problem, we will use the implementation you filled-in for problem 3 to run a simulation. You will create a `Patient` instance
with the following parameters, then run the simulation and answer several questions:
* `viruses`, a list of 100 ResistantVirus instances
* `maxPop`, Maximum Sustainable Virus Population = 1000

Each `ResistantVirus` instance in the viruses list should be initialized with the following parameters:
* `maxBirthProb`, Maximum Reproduction Probability for a Virus Particle = 0.1
* `clearProb`, Maximum Clearance Probability for a Virus Particle = 0.05
* `resistances`, The virus’s genetic resistance to drugs in the experiment = `{‘guttagonol’:False}`
* `mutProb`, Probability of a mutation in a virus particle’s offspring = 0.005 

### Problem 5: The Effect of Delaying Treatment on Patient Outcome ###
In this problem, we explore the effect of delaying treatment on the ability of the drug to eradicate the virus population. You will need
to run multiple simulations to observe trends in the distributions of patient outcomes.

Run the simulation for 300, 150, 75, and 0 time steps before administering guttagonol to the patient. Then run the simulation for
an additional 150 time steps. Use the same initialization parameters for ResistantVirus and Patient as you did for
Problem 4.

For each of the 4 conditions, repeat the experiment multiple times, while recording the final virus populations. Use pylab’s hist()
function to plot a histogram of the final virus populations under each condition. The _x_-axis of the histogram should be the final
total virus population and the _y_-axis of the histogram should be the number of patients belonging to each histogram bin. You 
should decide the number of times you need to repeat each condition in order to obtain a reasonable distribution. Justify your
decision in your writeup.

Include the four histograms in your writeup and answer the following questions: 
* If you consider final virus particle counts of 0–50 to be cured (or in remission), what percentage of patients were cured (or in remission) at the end of the simulation?
* What is the relationship between the number of patients cured (or in remission) and the delay in treatment? 
* Explain how this relationship arises from the model.

### Problem 6: Designing a Treatment Plan with Two Drugs ###
One approach to addressing the problem of acquired drug resisstance is to use cocktails - administration of multiple drugs that act
independently to attack the virus population.

In problems 6 and 7, we use two independently-acting drugs to treat the virus. We will use this model to decide the best way of
administering the two drugs. Specifically, we examine the effect of a lag time between administering the first and second drugs on
patient outcomes.

For problems 6–7, use the following parameters to initialize a `Patient`:
* `viruses`, a list of 100 `ResistantVirus` instances
* `maxPop`, Maximum Sustainable Virus Population = 1000

Each `ResistantVirus` instance in the viruses list should be initialized with the following parameters:
* `maxBirthProb`, Maximum Reproduction Probability for a Virus Particle = 0.1
* `clearProb`, Maximum Clearance Probability for a Virus Particle = 0.05
* `resistances`, The virus’s genetic resistance to drugs in the experiment = `{‘guttagonol’:False ‘grimpex’:False}`
* `mutProb`, Probability of a mutation in a virus particle’s offspring = 0.005

Run the simulation for 150 time steps before administering guttagonol to the patient. Then run the simulation for 300, 150, 75,
and 0 time steps before administering a second drug, grimpex, to the patient. Finally, run the simulation for an additional 150
time steps.

For each of these 4 conditions, repeat the experiment 30 times, while recording the final virus populations. Use pylab’s `hist()`
function to plot a histogram of the final total virus populations under each condition.
Include the histogram in your writeup and answer the following: 
* What percentage of patients were cured (or in remission) at the end of the simulation? 
* What is the relationship between the number of patients cured (or in remission) and the time
between administering the two drugs? 

### Problem 7: Analysis of Virus Population Dynamics With Two Drugs ###
To better understand the relationship between patient outcome and the time between administering the drugs, we examine the virus
population dynamics of two individual simulations from problem 6 in more detail.

Run a simulation for 150 time steps before administering guttagonol to the patient. Then run the simulation for an additional 300
time steps before administering a second drug, grimpex, to the patient. Then run the simulation for an additional 150 time
steps. Use the same initialization parameters for Patient and Resistantvirus as you did for problem 6.

Run a second simulation for 150 time steps before simultaneously administering guttagonol and grimpex to the patient. Then
run the simulation for an additional 150 time steps.
Make sure you run the simulation multiple times to ensure that you are analyzing results that are representative of the most
common outcome.

For both of these simulations, plot the total population, the population of guttagonol-resistant virus, the population of grimpexresistant
virus, and the population of viruses that are resistant to both drugs as a function of time.
Explain why the relationship between the patient outcome and the time between administering the two drugs arises. 

### Problem 8: Patient Non-compliance ###
A very common problem is that a patient may not consistently take the drugs they are prescribed. They can sometimes forget
or refuse to take their drugs. Describe in your writeup (do not write any code) how you would model such effects. 
