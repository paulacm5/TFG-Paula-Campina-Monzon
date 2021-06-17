
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# for testing purposes
from conv_to_bin_mat import ConvBinMap
from TrueMap import TrueMap
from copy import deepcopy  #para evitar modificar el original


class Visualization:
    """ Usage:
        intantiatate with Visualization()
            - can specify:
                - intial robot coordinates using start_x and start_y
                - the floorplan image that is being used
                - the size of the robot representation
                - the size of the particle representations
        
        then use any of the functions other than 'display_plot' to specify the object/s to be drawn
        then use 'display_plot' to actually display the stuff


        Functions:
        
        'move_robot' to update the robot position when given a list of movements

        'display_plot' must be called after every 'move_robot' otherwise you wont see the updated locations

    """


    def __init__(self, trueMap, start_x=500, start_y=200, angle = -105 , floorplan=None, rob_size=85, part_size=6):
        # Map variables ***************
        # can pass in a trueMap object or expliitly define the floorplan filepath for testing purposes
        if floorplan is not None:
            self.FLOORPLAN = floorplan
            self.xmin = -100
            self.xmax = 1900
            self.ymin = -50
            self.ymax = 800
        else:
            self.FLOORPLAN = trueMap.getFloorPlanFile()  # the floorplan filepath
            self.MAP_SCALE = trueMap.getScale()
            # limits for the plot axes (in number of pixels)
            map_rows, map_cols = trueMap.getDimensions()
            self.xmin = 0
            self.xmax = map_cols
            self.ymin = 0
            self.ymax = map_rows

        self.IM = plt.imread(self.FLOORPLAN)  # image of the floorplan
        self.MAP_OBJ = trueMap

        # Robot variables ***************
        self.start_x = start_x  # robot's initial x coordinate
        self.start_y = start_y  # robot's initial y coordinate
        self.angle = angle      # robot's initial angle refer to the coordinate system of the floorplan
        self.LAST_LOC = (start_x, start_y)  # the robot's last location 
        self.RSIZE = rob_size  # diameter of the robot marker
        self.positions = []
        self.orientations = []


        print("Visualization engine initialized")

    def move_robot(self, x, y, theta):

            # Calculate the reference coordinate.  If this is the first plot, the robot will start at location (start_x, start_y). 
            x_start, y_start = self.start_x, self.start_y
            
            # Changes that need to be taken into consideration in order to adapt the movements of the real robot
            # to the coordinate system of the floorplan.
            
            # Initial angle of the robot with respect to the floorplan
            self.angle = -105 + theta      
            print('\n','Este es el ángulo de giro: ', self.angle)
            
            # Adaptation of translational movements
            x_axis_map = - np.cos((15)/180*np.pi)*x - np.sin((15)/180*np.pi)*y
            y_axis_map = np.cos((15)/180*np.pi)*y -  np.sin((15)/180*np.pi)*x
            
            print('X inicial',x,'\n','X cambio', x_axis_map)
            print('\n','Y inicial',y,'\n','Y cambio', y_axis_map)
            
            #To obtain the final location in pixels
            new_x = x_start + x_axis_map/self.MAP_SCALE  
            new_y = y_start + y_axis_map/self.MAP_SCALE

            self.LAST_LOC = (new_x, new_y)


    def generate_marker(self, rot):
        """Generate the marker representing the robot on the  map with the orientation of the
            actual robot.

        Parameters:
            rot : float
                   rotation in degree
                   0 is positive x direction

        Returns:
            arrow_head_marker : Path
            use this path for marker argument of plt.scatter
            multiply an argument of plt.scatter with this factor got get markers
            with the same size independent of their rotation.
            
        """
        arr = np.array([[.20, .25], [.20, -.25], [1, 0]])  # arrow shape
        angle = rot / 180 * np.pi
        rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                                        [-np.sin(angle), np.cos(angle)]])
        arr = np.matmul(arr, rot_mat)  # rotates the arrow

        arrow_head_marker = mpl.path.Path(arr)
        return arrow_head_marker

    def display_plot(self):
        """ Uses matplotlib to create a figure with the floorplan overlayed with the
              marker representing the robot.

              MUST BE CALLED AFTER EVERY CALL OF move_robot.  Otherwise the plot will not show.
        """
        # must close all previous figures or else the function will eat up all the 
        # computer's memory
        plt.close("all")


        plt.figure(figsize=(20,15))  # figsize specifies the window size (in inches)    

        # the image of the floorplan onto which the robot's representation will be overlayed
        im1 = plt.imshow(self.IM, cmap=plt.cm.gray, interpolation='nearest')

        axes = plt.gca()
        axes.set_xlim([self.xmin,self.xmax])
        axes.set_ylim([self.ymax, self.ymin])  # must be reversed in order to plot (0,0) on top left corner

        # Here's where the robot positions are plotted
        # scatter() takes values in [x][y] order (so the opposite of the numpy array ordering)
        rob_x, rob_y = self.LAST_LOC
        print('\n',"LAST_LOC: ", self.LAST_LOC)
        arrow = self.generate_marker(self.angle)
        
        self.positions.append(self.LAST_LOC)   #list of robot positions
        self.orientations.append(arrow)  #list with the orientation in each position of the robot
        
        for item in range(len(self.positions)):   #in order to plot within the same map every position the robot takes.
            plt.scatter(x=self.positions[item][0], y=self.positions[item][1], c='r', s=(self.RSIZE)*3 ,marker=self.orientations[item])
        plt.show()
        

    # For testing with the terminal:
if __name__ == '__main__':

    testmap = TrueMap()
    c = Visualization(testmap, floorplan="BinaryMaps/EEBE_A5_binary.png")
    c.display_plot()


