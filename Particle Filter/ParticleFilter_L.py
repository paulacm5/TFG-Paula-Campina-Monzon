

import numpy as np
import random
import copy
from numpy.random import choice
from numpy import ndarray
import math

class ParticleFilter:

    def __init__(self, trueMap, sensor, numParticles=100):
        self.NUM_PARTICLES = numParticles
        self.TRUE_MAP = trueMap.getTrueMap()
        self.legalPositions = trueMap.getLegalPositions()
        self.NUM_LEGAL_POS = len(self.legalPositions)
        self.MAP_SCALE = trueMap.getScale()
        self.TRUE_SENSOR = sensor #for assigning weights to particles when wall locations are known
        self.SENSOR_NOISE = sensor.getNoise()
        self.MAP_DIMS = trueMap.getDimensions()
        self.MAP_OBJ = trueMap
        
        self.Particles = []  

        print("Particle filter initialized")


    def initializeParticles(self):
        """ Initializes a list of particles, where each particle is a list of positions and other features, 
            and a particle's position is a list of the form [row,col] (or [y,x])

            Each particle position is a pixel location (equivalently, an element in the map matrix)

            If the number of legal positions is less than the default number of particles 'numParticles'
            then it redefines self.NUM_PARTICLES and distributes these uniformly only into legal positions
            (positions with no wall or obstacles)

            Otherwise it distributes numParticles number of particles randomly only into legal positions
            (positions with no wall or obstacles.)
        """    

        if self.NUM_PARTICLES > self.NUM_LEGAL_POS:
            self.NUM_PARTICLES = self.NUM_LEGAL_POS

        # if num of particles is equal to the number of legal positions, then distribute uniformly
        # else distribute into random legal positions (this is due to a limit on number of particles,
        # which for most maps will be in the hundreds of thousands)
        if self.NUM_PARTICLES == self.NUM_LEGAL_POS:
            for p_row, p_col in self.legalPositions: 
                # position in positions
                self.Particles.append([[p_row, p_col]])
        else:
            # pick a random legal position
            legal_positions = copy.deepcopy(self.legalPositions)
            i = 0
            while i < self.NUM_PARTICLES:
                p_row, p_col = random.choice(legal_positions)
                legal_positions.remove((p_row,p_col))
                self.Particles.append([[p_row, p_col]])
                i += 1
        print(self.Particles)



    # This is only used for localization when you know the map! Sensor reading is passed to this method to determine
    # probability of sensor reading given location P(e|X)
    def weightParticles(self, sensorReading):
        weight = [0] * self.NUM_PARTICLES   #matriz del tamaño del num de particulas [0,0,0,0,...,numpart]
        for i in range(self.NUM_PARTICLES):
            y_pos = self.Particles[i][0][0]
            x_pos = self.Particles[i][0][1]
            trueRanges = self.TRUE_SENSOR.getTrueDistances([y_pos, x_pos])
            #data from the real sensor and the simulated sensor must be sorted so that they can be analyzed together
            weight[i] = self.measurement_prob(sorted(trueRanges), sorted(sensorReading))    


        norm_weight = [float(i)/sum(weight) for i in weight]
        #print('\n','ESTOS SON LOS PESOS NORMALIZADOS :', norm_weight)
        
        newParticlesIndices = np.random.choice(range(len(self.Particles)), size = self.NUM_PARTICLES, replace = True, p = norm_weight)  # an array
        
        newParticles = []
        for i in range(len(newParticlesIndices)):
            newParticles.append(copy.deepcopy(self.Particles[newParticlesIndices[i]]))
            #print(self.Particles[newParticlesIndices[i]])   : 100 rew particles with repeated values
        self.Particles = copy.deepcopy(newParticles)


    def gaussian(self, mu, sigma, x):
        """ calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        :param mu:    distance to the landmark
        :param sigma: standard deviation
        :param x:     distance to the landmark measured by the robot
        :return gaussian value
        
        """
        return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))


    def measurement_prob(self, trueRanges, sensorReading):
        """ Calculate the measurement probability: how likely a measurement should be
        :param measurement: current measurement
        :return probability
        
        """
        prob = 1.0

        for i in range(len(trueRanges)):
            prob *= self.gaussian(trueRanges[i], self.SENSOR_NOISE, sensorReading[i])
        print('\n',"ESTAS SON LAS DISTANCIAS DE LA PARTICULA: ", trueRanges)
        #print('\n','ESTA ES LA PROBABILIDAD DE LA PARTICULA: ', prob)
        return prob

    def getNumParticles(self):
        return self.NUM_PARTICLES


   