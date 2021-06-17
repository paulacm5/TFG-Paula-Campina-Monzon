
import time
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar
from conv_to_bin_mat import ConvBinMap

class Sensor:
    
    """ Usage: Obtains sensor information and processes it in a way that provides a list of xy values
                    representing each point in the environment.

          intantiatate with Sensor()        
    """


    def __init__(self, trueMap):
  
        self.MAP_DIMS = trueMap.getDimensions()
        self.MAP_OBJ = trueMap
        self.TRUE_MAP = trueMap.getTrueMap()
        self.MAP_SCALE = trueMap.getScale()
        self.lidar = RPLidar('/dev/ttyUSB0') #Assign the sensor port
        self.datos = [] #Create a variable to store the measurements
        time.sleep(5) #To avoid the error of 'Wrong body size'

        print("Sensor Initialized")

    def ObtenerScan(self):
        """
        The information captured by the sensor is obtained and the distance and angle
        values of each measurement are stored in a variable.            
       
        """
        for i, scan in enumerate(self.lidar.iter_scans()):
            for medida in scan[:len(scan)]:
                if len(self.datos) < 500:
                    self.datos.append(medida[1:])
                else:    
                    self.lidar.stop_motor()
                    return self.datos
        
    def ObtenerCoordenadas(self):
        """
            The list of data provided by the method ObtenerScan() is processed so that a matrix
            with the xy coordinates of each point is obtained.
        
        """
        matriz = []  
        for punto in self.ObtenerScan():
            x = (((punto[1]*np.cos(((-90+punto[0])*np.pi)/180.0)))/1000)
            y = (-((punto[1]*np.sin(((-90+punto[0])*np.pi)/180.0)))/1000)
               
            point = np.array([x,y,1.0])
            matriz.append(point)          
    
        return np.array(matriz)
    
        #Store the data in a txt file
        #      encabezado = 'x y'
        #      np.savetxt('datost_xy.txt', matriz, fmt='%d', header=encabezado)
    
    def GraficarEntorno(self,matriz0,matriz1):
        #To plot the data, they must be separated into x-coordinates and y-coordinates.
        punto_x0 = [item[0] for item in matriz0]
        punto_y0 = [item[1] for item in matriz0]
        punto_x1 = [item[0] for item in matriz1]
        punto_y1 = [item[1] for item in matriz1]
        
        #To plot the point clouds (environment pos 1 and environment pos 2)
        plt.clf()
        plt.scatter(punto_x0,punto_y0,marker='.',norm='0.2')
        plt.pause(.1)
        plt.ylabel('y')
        plt.xlabel('x')
        plt.xlim(-5,7)
        plt.ylim(-5,7)

        #Store the figures 
        plt.scatter(punto_x1,punto_y1,marker='.',norm='0.2')
        plt.pause(.1)
        plt.savefig("Graficat_xy_odometria.jpg",bbox_inches='tight')
        plt.show()


    def PararSensor(self):
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()
    
    def reset(self):
        self.lidar.reset()
        


 







