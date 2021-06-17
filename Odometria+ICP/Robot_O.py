#-------------------------------------
#ODOMETRY MAIN PROGRAM
#-------------------------------------

from Odometry_O import Align2D
from Sensor_O import Sensor
from TrueMap import TrueMap
from visualization_O import Visualization
import time
import numpy as np
from copy import deepcopy  


def RadToDegree(matrix):
     """
            Convert the rotacion of the transformation matrix from radians to degrees.
            It is necessary to stop the sensor after each data acquisition, and then re-initialize
            it to avoid an error from the sensor itself.
     """
    matrix_ang = deepcopy(matrix)
    for item in range(len(matrix_ang)):
        if item == 0:
            matrix_ang[0][0]=np.arccos(matrix_ang[item][0])*180/np.pi
            matrix_ang[0][1]=np.arcsin(matrix_ang[item][1])*180/np.pi
        if item == 1:
            matrix_ang[1][0]=np.arcsin(matrix_ang[item][0])*180/np.pi
            matrix_ang[1][1]=np.arccos(matrix_ang[item][1])*180/np.pi
    return matrix_ang


if __name__ == '__main__':
   
    #Initial coordinates of the robot
    initx = 519   #520  519
    inity = 145   #140  145

    #Instantiate the objects for each class
    the_map = TrueMap(floorplan='BinaryMaps/EEBE_A5_binary.png',plan_scale = .04173)
    viz = Visualization(the_map, start_x=initx, start_y=inity)
    sensor = Sensor(the_map)
    
    viz.display_plot()
    
    #Variable initialisation
    matriz_final=[]
    matrix_ang=[]
    i = 0  #position counter
    datos=[]
    
    #Finite loop with the number of robot movements
    while i < 35:
        
        sensor = Sensor(the_map)      #sensor initialisation
        datos.append(sensor.ObtenerCoordenadas())
        
        #Condition for the first movement (instant 0)
        if len(datos) == 1:
            initial_T = np.identity(3)     #first case, when the transformation matrix has not yet been calculated
            target_points = datos[i]      #target points cloud
            time.sleep(3)                      #delay in order to move the robot to the next location
            sensor.PararSensor()          
            sensor = Sensor(the_map)
            datos.append(sensor.ObtenerCoordenadas())
            source_points = datos[i+1]     #source points cloud
            print('\n', 'Matriz de traslación+rotación de la posición %d a la posición %d' % (i,i+1))
            aligner = Align2D(source_points, target_points, initial_T)    #matrix transformation for this movement
            matriz_final = np.matmul(initial_T,aligner.transform)          
            i=i+1
            time.sleep(2)
            sensor.PararSensor()
            
        #Condition for the rest of the movements (instants != 0)
        else:
            initial_T = aligner.transform
            target_points = datos[i]
            source_points = datos[i+1]
            print('\n', 'Matriz de traslación+rotación de la posición %d a la posición %d' % (i,i+1))
            aligner = Align2D(source_points, target_points, initial_T)
            matriz_final = np.matmul(matriz_final, aligner.transform)        #matrix transformation relative to the inital position
            i = i+1
            time.sleep(2)
            sensor.PararSensor()
               
        if i == 3 or i == 9 or i == 11 or i == 15 or i == 19 or i == 23 or i == 27 or i == 31 or i == 35:
            mat_rot = RadToDegree(matriz_final)
            print('\n', 'Esta es la matriz de transformación final:')
            print(mat_rot)
            print('\n', 'Esta es la segunda posicion:')
            print(matriz_final[0][2], matriz_final[1][2])  
            
            # update the visual position
            viz.move_robot(matriz_final[0][2], matriz_final[1][2],mat_rot[0][0])    #robot displacement in pixels
            viz.display_plot()   #display the robot's locations

   









     


