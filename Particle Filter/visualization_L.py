
import matplotlib.pyplot as plt
import numpy as np

# for testing purposes
from conv_to_bin_mat import ConvBinMap
from TrueMap import TrueMap


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
        
        'replot_particles' to plot particle dots

        'display_plot' must be called after every 'replot:_particles' otherwise you wont see the updated locations

    """

    def __init__(self, trueMap, floorplan=None, rob_size=7, part_size=6,start_x=500, start_y=200):
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
            # limits for the plot axes (in number of pixels)
            map_rows, map_cols = trueMap.getDimensions()
            self.xmin = 0
            self.xmax = map_cols
            self.ymin = 0
            self.ymax = map_rows

        self.IM = plt.imread(self.FLOORPLAN)  # image of the floorplan
        self.MAP_OBJ = trueMap

        # Robot variables ***************
        self.RSIZE = rob_size  # diameter of the robot dot
        self.start_x = start_x   # robot's initial x coordinate
        self.start_y = start_y   # robot's initial y coordinate
        self.LAST_LOC = (start_x, start_y)  # the robot's last location 

        # Particle variables ***************
        self.PSIZE = part_size  # diameter of the particle dots
        self.PARTICLES = []  # a list of particle coordinates in (x,y) tuple form
        
        print("Visualization engine initialized")


    def replot_particles(self, particlelist, numtoplot=100):
        """ Takes in a list of particle locations (one for each particle) and updates the self.PARTICLES variable:
            example: [(p1x, p1y), (p2x, p2y), (p3x, p3y)]

            Retains the locations of these particles, and updates the visual representation only when this 
            function is called and given a new list of locations.

            numtoplot limits the amount of particles that are actually plotted (because plotting more particles
            makes transition time between states slower).  Default to the first 100 particles.  If there are 
            fewer than numtoplot particles, then it plots all of them.
        """
        # Overlay particles and the floorplan
        if len(particlelist) <= numtoplot:
            self.PARTICLES = particlelist
        else:
            for i in range(numtoplot):
                self.PARTICLES.append(particlelist[i])

    def display_plot(self):
        """ Uses matplotlib to create a figure with the floorplan overlayed with the
            dots representing the robot and the particles.

            MUST BE CALLED AFTER EVERY CALL OF replot_particles OR move_robot.  Otherwise
            the plot will not show.

            Can be optimized to be more memory efficient, but for the time being it works.
        """
        # must close all previous figures or else the function will eat up all the 
        # computer's memory
        plt.close("all")

        # each iteration creates a new figure to give the illusion of movement
        plt.figure(figsize=(20,15))  # figsize specifies the window size (in inches)

        # the image of the floorplan onto which the dots will be overlayed
        im1 = plt.imshow(self.IM, cmap=plt.cm.gray, interpolation='nearest')

        axes = plt.gca()
        axes.set_xlim([self.xmin, self.xmax])
        axes.set_ylim([self.ymax, self.ymin])  # must be reversed in order to plot (0,0) on top left corner
     
        rob_x, rob_y = self.LAST_LOC
        plt.scatter(x=[rob_x], y=[rob_y], c='b', s=self.RSIZE)

        # Here's where the particles are actually plotted
        # scatter() takes values in x, y order (so the opposite of the numpy array ordering)
        if self.PARTICLES:
            for (py,px) in self.PARTICLES:
                plt.scatter(px, py, c='r', s=self.PSIZE)

            self.PARTICLES = []  # in order to make the visualization faster, it erases the particle list from memory 
                                            # (only plots every time replot_particles)
        plt.show()



    # For testing with the terminal:
if __name__ == '__main__':

    rand_mat = np.random.rand(100,100)

    # test the trueMap object
    testmap = TrueMap()
    c = Visualization(testmap, floorplan="BinaryMaps/EEBE_A5_L_binary.png")
    c.display_plot()


 
