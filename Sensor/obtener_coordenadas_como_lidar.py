#Program that obtains the sensor data and plots it on a graph as a function of x,y.

# Import libraries 
import time
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

#Initialize the sensor through the port
lidar = RPLidar('/dev/ttyUSB0')
    
datos = [] #Variable to store the measurements
time.sleep(5) #To avoid the error of 'Wrong body size'

#Method to store the distance and angle of sensor measurements 
def obtener_datos():

    for i, scan in enumerate(lidar.iter_scans()):
        print('%d: Got %d measurements' % (i, len(scan)))
    #     datos.append('Escaneo %d' % i)
        for medida in scan[:len(scan)]:
            if len(datos) < 500:
                datos.append(medida[1:])
            else:    
                print(len(datos))
                lidar.stop_motor()
                return datos

#Method for processing sensor data and converting it into xy coordinates
def obtener_coordenadas():
    x = [0] 
    y = [0]
    
    datos = obtener_datos()
    print(datos)
    for punto in datos:
        #the distance must be in meters and the angle must be converted to radians so that python can deal with
        x.append(((punto[1]*np.cos(((-90+punto[0])*np.pi)/180.0)))/1000)  
        y.append(-((punto[1]*np.sin(((-90+punto[0])*np.pi)/180.0)))/1000)
        
    matriz = np.array([x,y])
    matriz1 = np.transpose(matriz)
   
    #Store the data in a txt file
    encabezado = 'x y'
    np.savetxt('datost_xy.txt', matriz1, fmt='%d', header=encabezado)

     #To plot the points on an xy plane
    plt.clf()
    plt.scatter(x,y,marker='.',norm='0.5')
    plt.pause(.1)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.xlim(-8,8)
    plt.ylim(-8,8)
    plt.savefig("Graficat_xy_simple.jpg",bbox_inches='tight')
    plt.show()
    paro_sensor()
    return matriz1

def paro_sensor():
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
 
 
 #For testing 
if __name__ == '__main__':
    valores0=obtener_coordenadas()