#------------------------------------------------------------------------------------------------
# Name: Utilities
# Date: Feb 16, 2022
# Author: Jose L. Agraz, PhD, Caleb Genko, and Wang Hao
#
# Description: Set of functions to apply Vahadane's normalization algorithm
#               https://github.com/wanghao14/Stain_Normalization
#
# ------------------------------------------------------------------------------------------------
# Library imports
# ------------------------------------------------------------------------------------------------
import numpy as np
import spams

WHITE_COLOR                       = 255
INFERRED_DIMENSION                = -1 
NUMBER_OF_COLORS                  = 3   
       
def od2rgb(OD):
    """
    Transforms from optical density to red-green-blue colorspace.
    :param OD: optical density matrix to be converted.
    :return: Same values but in RGB format.
    """
    return (WHITE_COLOR * np.exp(-1 * OD)).astype(np.uint8)

def rgb2od(Image):
    """
    Transforms an RGB image to the Optical Density (OD) colorspace.
    :param I: RGB image to be converted.
    :return: Same values but in RGB format.
    optical density is calculated as OD = -log(%t)
    OD = Log10(Io / I)
    """
    NewImage = np.where(Image == 0.0, 1, Image)
    Image_Adjusted = NewImage / WHITE_COLOR

    OpticalDensity = -np.log(Image_Adjusted)
    return OpticalDensity

def CalculateStainVector(Image,Stain_Vector_Lambda,Stain_Vector_Training_Time):
    """
    Get 2x3 stain matrix. First row H and second row E
    :param I:
    :param threshold:
    :param ld:
    :return:
    Use smaller values of the lambda (0.01-0.1) for better reconstruction.
    However, if the normalized image seems not fine, increase or decrease the value accordingly.
    """
    NUMBER_OF_STAINS = 2
    X                = rgb2od(Image).reshape((INFERRED_DIMENSION, NUMBER_OF_COLORS))
    StainVectors = spams.trainDL(
        X        = X.T,
        K        = NUMBER_OF_STAINS,  
        lambda1  = Stain_Vector_Lambda,
        mode     = 2,
        modeD    = 0,
        posAlpha = True,
        iter     = -Stain_Vector_Training_Time,
        posD     = True,
        verbose  = False
    ).T
    print('Normalize vector')
    StainVectors      = normalize_rows(StainVectors)

    print('need to find H&E order by looking at color ratios')
    StainVectorOutput = SortOutStainVectors(StainVectors)
    
    return StainVectorOutput

#-----------------------------------------------------------------
# Name: Sort Out Stain Vectors
# Author: Jose L. Agraz, PhD., Caleb Grenko
# Date: 06/12/2020
# Description: Output vectors definition is undefined. Need to find 
#              H&E vector order by which is more blue.
# Input:
# Output:
#-----------------------------------------------------------------
def SortOutStainVectors(StainVectors):
    
    RED_COLOR            = 0
    GREEN_COLOR          = 1
    BLUE_COLOR           = 2
    FIRST_ITEM           = 0
    SECOND_ITEM          = 1
    print('Sort Out Stain Vectors')
    FirstStainRed        = StainVectors[FIRST_ITEM, RED_COLOR]
    FirstStainGreen      = StainVectors[FIRST_ITEM, GREEN_COLOR]
    FirstStainBlue       = StainVectors[FIRST_ITEM, BLUE_COLOR]
    
    SecondStainRed       = StainVectors[SECOND_ITEM, RED_COLOR]
    SecondStainGreen     = StainVectors[SECOND_ITEM, GREEN_COLOR]
    SecondStainBlue      = StainVectors[SECOND_ITEM, BLUE_COLOR]
    

    if FirstStainBlue >= SecondStainBlue:
        HematoxylinStainVector = [FirstStainRed,FirstStainGreen,FirstStainBlue]
        EosinStainVector       = [SecondStainRed,SecondStainGreen,SecondStainBlue]
        
    else:
        HematoxylinStainVector = [SecondStainRed,SecondStainGreen,SecondStainBlue]
        EosinStainVector       = [FirstStainRed,FirstStainGreen,FirstStainBlue]
        
    HandE_StainVectors = np.array([HematoxylinStainVector,EosinStainVector])

    return HandE_StainVectors 


def normalize_rows(A):
    """
    Normalize rows of an array
    :param A:
    :return:
    """
    print('Normalize Array')
    if np.all(A == 0.0): 
        return A
    
    A = np.where(A == 0.0, 1/WHITE_COLOR, A)
    
    return A / np.linalg.norm(A, axis=1)[:, None]

def CalculateDensityMap(Image, StainMatrix,lamda):
    """
    Get concentrations, a npix x 2 matrix
    :param I:
    :param stain_matrix: a 2x3 six
    :return:
    """
    
    OD = rgb2od(Image).reshape(INFERRED_DIMENSION, NUMBER_OF_COLORS)

    print('Executing spams.lasso')

    DensityMapW           = spams.lasso(X       = OD.T,
                                        D       = StainMatrix.T, 
                                        lambda1 = lamda,
                                        pos     = True)

    return DensityMapW.toarray().T
