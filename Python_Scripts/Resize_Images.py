
#------------------------------------------------------------------------------------------------
# Name: Normalize Image
# Date: Feb 16, 2022
# Author: Jose L. Agraz, PhD
#
# Description: This script normalizes image stain colors by applying a set of stain vectors and histogram
#
# Usage Example:
#       python Normalize_Image.py\
#             --Image_To_Normalize        /home/jlagraz/Documents/Normalization/BaSSaN-Update/IvyGapPictures/266290664.jpg\
#             --Normalizing_Histogram     /home/jlagraz/Documents/Normalization/BaSSaN-Update/Produce_Single_Image_Normalization/Dataframes_Single_Image/100_Images_Normalization/1/100Image_Cohort_Results/100ImageCohortHistograms.npy\
#             --Normalizing_Stain_Vectors /home/jlagraz/Documents/Normalization/BaSSaN-Update/Produce_Single_Image_Normalization/Dataframes_Single_Image/100_Images_Normalization/1/100Image_Cohort_Results/100ImageCohortStainVectors.npy\
#             --Output_Directory          /home/jlagraz/Documents/Normalization/BaSSaN-Update/Produce_Single_Image_Normalization/Output/
#
# Notes:
#
# ------------------------------------------------------------------------------------------------
# Library imports
# ------------------------------------------------------------------------------------------------
import dask 
import spams
import argparse
import itertools
import skimage.io    
import numpy            as np
import dask.array       as da
from PIL                import Image
from datetime           import datetime
from pathlib            import Path
from skimage.color      import rgb2lab
from skimage.exposure   import match_histograms

from PIL import Image
#
__author__  = 'Jose L. Agraz, PhD'
__status__  = "Public_Access"
__email__   = 'software@cbica.upenn.edu'
__credits__ = ['Spyros Bakas','Caleb Grenko']
__license__ = "GPL"
__version__ = "0.0.1"
#
#------------------------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------------------------
Image.MAX_IMAGE_PIXELS                      = None
if __name__ == "__main__":

    im = Image.open('/home/jlagraz/Documents/Manuscript_Test_Code/GitHub/shiny-fortnight/Normalization_Example/Images_and_Maps/Image_Maps/W19-1-1-D.01_23_LM_266290664.png')
    width, height = im.size
    
    newsize = (int(width*.75), int(height*.75))
    im1 = im.resize(newsize)
    im1 = im1.save('/home/jlagraz/Documents/Manuscript_Test_Code/GitHub/shiny-fortnight/Normalization_Example/Images_and_Maps/Image_Maps/Resized_Images/W19-1-1-D.01_23_LM_266290664.png')