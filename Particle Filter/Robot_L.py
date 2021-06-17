#-----------------------------------------------------------------------
#LOCALIZATION WITH PARTICLE FILTER MAIN PROGRAM
#-----------------------------------------------------------------------

from ParticleFilter_L import ParticleFilter
from Sensor_L import Sensor
from Sensor_O import Sensor_L
from TrueMap import TrueMap
from visualization_L import Visualization
import time


if __name__ == '__main__':

    # Initialize ***

    # coordinates in the middle of a room (elevators area in this case)
    initx = 162 #162    173    190    180  165  250   910  165    70  170  190
    inity = 250   #250   227   80      120  180  210   550  365  370  150  390
    the_map = TrueMap(floorplan='BinaryMaps/EEBE_A5_L_binary.png',plan_scale = .04173)

    #Instantiate the objects for each class
    viz = Visualization(the_map,start_x=initx, start_y=inity)
    sensor = Sensor(the_map)
    part_filt = ParticleFilter(the_map, sensor, numParticles=140)
    
    #Initialize and display the particles on the map
    part_filt.initializeParticles()
    viz.replot_particles(part_filt.getParticleLocations(), numtoplot=140)
    viz.display_plot()
    
    
    i = 0    #lidar scan counter
    while i < 2:   
        lidar = Sensor_L(the_map)                       #get data from real sensor
        distancias = lidar.obtener_distancias()     #store data from real sensor
        lidar.parar_sensor()
        part_filt.weightParticles(distancias)            #calculate the weight of each particle

        viz.replot_particles(part_filt.getParticleLocations(), numtoplot=140)    #update particles
        viz.display_plot()                                        #display changes
        i=i+1
 



