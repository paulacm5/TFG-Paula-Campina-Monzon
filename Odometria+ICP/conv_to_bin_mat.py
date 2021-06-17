
from PIL import Image
import numpy as np
import os
import scipy.misc
import imageio


class ConvBinMap:

    @staticmethod
    def map_to_binary_image():
        """ Converts an image stored in the 'SourceMaps' directory
            into a black and white image (0 = black, 255 = white) that is 
            then stored in the 'BinaryMaps' directory.

            User is prompted to enter the filename of the chosen map first (e.g. MD_0.png)
            Output file sis named the same thing as the input file name, but with '_binary' 
            appended to the end.
        """
        source_im = input("Enter the path of your file: ")
        # print source_im

        col = Image.open("SourceMaps/" + source_im)
        gray = col.convert('L')

        # converting pixels to pure black or white
        bw = np.asarray(gray).copy()

        # Pixel range is 0...255, 256/2 = 128
        bw[bw < 128] = 0    # Black
        bw[bw >= 128] = 255 # White

        # Now we put it back in Pillow/PIL land
        imfile = Image.fromarray(bw)

        source_im_wo_ext = os.path.splitext(source_im)[0]
        out_im = source_im_wo_ext + "_binary.png"

        imfile.save("BinaryMaps/" + out_im)


    @staticmethod
    def map_to_mat(map_image_path):
        """ Uses a black and white png image produced by map_to_binary_image() and converts it 
            into a matrix of the same dimensions as the image (there is a one-to-one mapping 
            of pixels to matrix elements).

            The white pixels (color value of 255) are converted into '0' in the new matrix.
            The black pixels (color value of 0) are converted into '1' in the new matrix.

            1 means obstacle cell
            0 means empty cell

            Takes a string as an argument (the name of the black and white image).
            Returns a numpy matrix of zeros and ones, indexed as: map_matrix[rows][cols]
            
        """
        map_matrix = imageio.imread(map_image_path)
            
        for (x,y), value in np.ndenumerate(map_matrix):
            if map_matrix[x][y] == 255:
                map_matrix[x][y] = 0  # no obstacle
            elif map_matrix[x][y] == 0:
                map_matrix[x][y] = 1  # obstacle
                
        return map_matrix


# For testing with the terminal:
if __name__ == '__main__':
    ConvBinMap.map_to_binary_image()
    matrix=ConvBinMap.map_to_mat('BinaryMaps/EEBE_A5_binary.png')

