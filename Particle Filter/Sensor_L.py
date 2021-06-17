
# Class provides framework for simulating noisy distance sensor data. Stores an occupancy grid map as a basis for returning data
import numpy as np
import math
import random
from conv_to_bin_mat import ConvBinMap


class Sensor:

    def __init__(self, trueMap, sensor_noise = 1.5):
        # define sensor characteristics
        self.MAX_RANGE = 10 #meters
        self.APERTURE_ANGLE = 360 #degrees
        self.ANGULAR_RESOLUTION = 2 #degrees
        self.RANGE_RESOLUTION = trueMap.getScale() # range resolution need not be better than plan scale
        self.MAP_DIMS = trueMap.getDimensions()
        self.MAP_OBJ = trueMap
        
        # determine at what specific angles the sensor will be detecting
        # theta is measured from a line coming out of the robot pointing directly right. Clockwise is positive, counterclockwise negative
        self.sensorAngles = np.linspace(-self.APERTURE_ANGLE/2, self.APERTURE_ANGLE/2, int(self.APERTURE_ANGLE/self.ANGULAR_RESOLUTION) + 1)
        for i in range(len(self.sensorAngles)):
            self.sensorAngles[i] = math.radians(self.sensorAngles[i])


        # Store true map. The map is indexed (0,0) in the top left with the form (y,x) (aka row, column)
        self.TRUE_MAP = trueMap.getTrueMap()
        self.MAP_SCALE = trueMap.getScale()   # meters per pixel

        self.NOISE_MODEL = sensor_noise # sensor noise is the standard deviation of a Gaussian noise model

        print("Sensor Initialized")


    def getTrueDistances(self, truePosition):
          """
                Returns an np array (vector) of distances corresponding to each of the sensor angles. Returns MAX_RANGE or higher if no wall in range.
        
          """
        # truePosition should be of the form [y, x]
        y = truePosition[0]
        x = truePosition[1]

        sensorDistances = [0]*len(self.sensorAngles)
        # return a distance associated with each scan angle
        for angle in range(len(self.sensorAngles)):
            # cast a ray increasingly farther out and check the pixel value at its endpoint. 
            # distance is point at which wall is hit or distance maxes out
            for distance in np.linspace(0, self.MAX_RANGE, int(self.MAX_RANGE/self.RANGE_RESOLUTION)): # distance here is in meters
                dx = distance * math.cos(self.sensorAngles[angle] % (2 * math.pi))
                dy = -distance * math.sin(self.sensorAngles[angle] % (2 * math.pi))
                # keep in mind np array accessed [row, col]


                # divide dy and dx by scale to convert meters to pixels
                y_pos = y+int(dy/self.MAP_SCALE)
                x_pos = x+int(dx/self.MAP_SCALE)

                # Map limits enforced
                x_pos, y_pos = self.MAP_OBJ.imposeMapLimits(x_pos, y_pos)

                if self.TRUE_MAP[y_pos][x_pos] == 1 or distance >= self.MAX_RANGE:
                    sensorDistances[angle] = distance
                    break
        return sensorDistances

   
    def getNoisyDistances(self, truePosition):
         """
               Adds noise to sensor return values based on a noise model.
        
          """
        distances = self.getTrueDistances(truePosition)

        for i in range(len(distances)):
            distances[i] = random.gauss(distances[i], self.NOISE_MODEL)
            
            # ensure noise doesn't go beyond sensor range
            if distances[i] > self.MAX_RANGE:
                distances[i] = self.MAX_RANGE
            elif distances[i] < 0:
                distances[i] = 0
                
        #print(distances)
        return distances
    
    def getNoise(self):
        return self.NOISE_MODEL

    def getSensorAngles(self):
        return self.sensorAngles





