# ------------------------------------------------------------------------------------------------
# Name: Produce_Image_Stain_Vectors_and_Optical_Density
# Date: February 17, 2022
# Author: Jose L. Agraz, PhD
#
# Description: This script calculates the stain vectors and color histogram for H & E histology image
#
# Usage Example:
#       python Produce_Image_Stain_Vectors_and_Optical_Density.py\ 
#       --Slide_Image                /home/jlagraz/Documents/Normalization/BaSSaN-Update/IvyGapPictures/266290664.jpg\
#       --Label_Map_Image            ./Normalization_Example/Images_and_Maps/W18-1-1-A.01_2_LM_268005945.png\
#       --Gray_Level_To_Label_Legend ./Normalization_Example/Csv_Files/LV_Gray_Level_to_Label.csv\
#       --Output_Dataframe_File      ./Normalization_Example/Output/Images_DataFrames/Dataframe_268005945\
#       --Excluding_Labels           ""
#     
#
# Notes:
# ------------------------------------------------------------------------------------------------
# Library imports
# ------------------------------------------------------------------------------------------------
from __future__     import division
from pathlib        import Path
from datetime       import datetime
import re
import cv2
import pathlib
import argparse
import Utilities
import numpy          as np
import pandas         as pd
import dask.array     as da
__author__  = ['Jose L. Agraz, PhD']
__status__  = "Public_Access"
__email__   = "jose@agraz.email"
__credits__ = ["Spyros Bakas"]
__credits__ = ["Caleb C."]
__license__ = "GPL"
__version__ = "Feb_17_2022"
# ------------------------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------------------------
HEMATOXYLIN_STAIN                   = 0
EOSIN_STAIN                         = 1
OUTPUT_FILE_EXTENSION               = 'parquet'
IMAGES_DATAFRAMES                   = 'Images_Stain_Stats_DataFrames'
HISTOGRAMS_DATAFRAMES               = 'Images_Histograms_DataFrames'
HEMATOXYLIN_STAIN_LABEL             = 'Hematoxylin'
EOSIN_STAIN_LABEL                   = 'Eosin'
# ------------------------------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------------------------------
InputImagesDictionary       = dict()
GrayLevelLabelMapDataFrame  = pd.DataFrame()
# ------------------------------------------------------------------------------------------------
class CompositeStatistics:
    def __init__(self):
        print('Define Image Info Class Variables')
        self.SlideImageName                         = str()
        self.LabelMapImageName                      = str()
        self.FeatureName                            = str()
        # ------------------------------------
        print('Define Hematoxylin Info Class Variables')
        self.HematoxylinAreaInPixels                = int()
        self.HematoxylinPixelDensity                = np.array([])
        # ------------------------------------
        self.HematoxylinStainOpticalDensity_Red     = int()
        self.HematoxylinStainOpticalDensity_Green   = int()
        self.HematoxylinStainOpticalDensity_Blue    = int()
        # ------------------------------------
        self.HematoxylinRGBStainVector_Red          = int()
        self.HematoxylinRGBStainVector_Green        = int()
        self.HematoxylinRGBStainVector_Blue         = int()
        # ------------------------------------
        self.HematoxylinDensityMeans                = float()
        self.HematoxylinDensitySDs                  = float()
        self.HematoxylinDensityMedians              = float()
        # ------------------------------------
        print('Define Image wide stats class')                
        self.Hematoxylin_Image_Count                = int()
        self.Hematoxylin_Image_Mean                 = float()
        self.Hematoxylin_Image_Standard_deviation   = float()
        self.Hematoxylin_Image_Min                  = float()
        self.Hematoxylin_Image_25_Percent           = float()
        self.Hematoxylin_Image_50_Percent           = float()
        self.Hematoxylin_Image_75_Percent           = float()        
        self.Hematoxylin_Image_Max                  = float()        
        # ------------------------------------
        print('Define Eosin Info Class Variables')
        self.EosinAreaInPixels                      = int()
        self.EosinPixelDensity                      = np.array([])
        # ------------------------------------
        self.EosinStainOpticalDensity_Red           = int()
        self.EosinStainOpticalDensity_Green         = int()
        self.EosinStainOpticalDensity_Blue          = int()
        # ------------------------------------
        self.EosinRGBStainVector_Red                = int()
        self.EosinRGBStainVector_Green              = int()
        self.EosinRGBStainVector_Blue               = int()
        # ------------------------------------
        self.EosinDensityMeans                      = float()
        self.EosinDensitySDs                        = float()
        self.EosinDensityMedians                    = float()
        # ------------------------------------
        print('Define Image wide stats class')        
        self.Eosin_Image_Count                      = int()
        self.Eosin_Image_Mean                       = float()
        self.Eosin_Image_Standard_deviation         = float()
        self.Eosin_Image_Min                        = float()
        self.Eosin_Image_25_Percent                 = float()
        self.Eosin_Image_50_Percent                 = float()
        self.Eosin_Image_75_Percent                 = float()        
        self.Eosin_Image_Max                        = float()
 
    # ------------------------------------------------------
    def ImageComposite(self, ImageName, MapName, Feature, ImageData):
        global InputArguments
        RED_COLOR                               = 0
        GREEN_COLOR                             = 1
        BLUE_COLOR                              = 2
        HEMATOXYLIN_STAIN                       = 0
        EOSIN_STAIN                             = 1
        
        print('Define Image Info Variables')
        SlideImageName                          = str()
        LabelMapImageName                       = str() 
        # ------------------------------------
        print('Define Hematoxylin Info Variables')
        HematoxylinAreaInPixels                 = int()
        HematoxylinPixelDensity                 = np.array([])
        # ------------------------------------
        HematoxylinStainOpticalDensity_Red      = int()
        HematoxylinStainOpticalDensity_Green    = int()
        HematoxylinStainOpticalDensity_Blue     = int()
        # ------------------------------------
        HematoxylinRGBStainVector_Red           = int()
        HematoxylinRGBStainVector_Green         = int()
        HematoxylinRGBStainVector_Blue          = int()
        # ------------------------------------
        HematoxylinDensityMeans                 = float()
        HematoxylinDensitySDs                   = float()
        HematoxylinDensityMedians               = float()
        # ------------------------------------
        print('Define Image wide stats')
        Hematoxylin_Image_Count                 = int()
        Hematoxylin_Image_Mean                  = float()
        Hematoxylin_Image_Standard_Deviation    = float()
        Hematoxylin_Image_Min                   = float()
        Hematoxylin_Image_25_Percent            = float()
        Hematoxylin_Image_50_Percent            = float()
        Hematoxylin_Image_75_Percent            = float()
        Hematoxylin_Image_Max                   = float()        
        # ------------------------------------
        print('Define Eosin Info Variables')
        EosinAreaInPixels                       = int()
        EosinPixelDensity                       = np.array([])
        # ------------------------------------
        EosinStainOpticalDensity_Red            = int()
        EosinStainOpticalDensity_Green          = int()
        EosinStainOpticalDensity_Blue           = int()
        # ------------------------------------
        EosinRGBStainVector_Red                 = int()
        EosinRGBStainVector_Green               = int()
        EosinRGBStainVector_Blue                = int()
        # ------------------------------------
        EosinDensityMeans                       = float()
        EosinDensitySDs                         = float()
        EosinDensityMedians                     = float()
        # ------------------------------------
        print('Define Image wide stats')
        Eosin_Image_Count                       = int()
        Eosin_Image_Mean                        = float()
        Eosin_Image_Standard_Deviation          = float()
        Eosin_Image_Min                         = float()
        Eosin_Image_25_Percent                  = float()
        Eosin_Image_50_Percent                  = float()
        Eosin_Image_75_Percent                  = float()
        Eosin_Image_Max                         = float()
        # --------------------------------------------------------------------------
        SlideImageName                              = Path(ImageName).name
        LabelMapImageName                           = Path(MapName).name        
        print('Calculating Image Stain Vectors')
        StainVectors_S                              = Utilities.CalculateStainVector(ImageData,float(InputArguments.Stain_Vector_Lambda),int(InputArguments.Stain_Vector_Training))
        print('Calculating Image Density Map')
        StainPixelDensity_W                         = Utilities.CalculateDensityMap(ImageData, StainVectors_S,float(InputArguments.Density_Map_Lambda))        
        print('Converting Stain Vectors from RGB to Optical Density')
        RgbStainVectors                             = Utilities.od2rgb(StainVectors_S)
        print('Extracting Hematoxylin Density')
        AllHematoxylinDensities                     = StainPixelDensity_W[:, HEMATOXYLIN_STAIN]
        print('Remove all pixels that do not actually contain hematoxylin')
        NonZeroHematoxylinDensities                 = AllHematoxylinDensities[np.nonzero(AllHematoxylinDensities)] 
        # ------------------------------------        
        HematoxylinPixelDensity                     = np.array(NonZeroHematoxylinDensities.tolist())        
        HematoxylinAreaInPixels                     = len(NonZeroHematoxylinDensities) 
        print('Hematoxylin Calculate Optical Density Stain Vectors')
        HematoxylinStainOpticalDensity_Red          = StainVectors_S[HEMATOXYLIN_STAIN][RED_COLOR]
        HematoxylinStainOpticalDensity_Green        = StainVectors_S[HEMATOXYLIN_STAIN][GREEN_COLOR]
        HematoxylinStainOpticalDensity_Blue         = StainVectors_S[HEMATOXYLIN_STAIN][BLUE_COLOR]
        print('Hematoxylin Calculate RGB Stain Vectors')
        HematoxylinRGBStainVector_Red               = RgbStainVectors[HEMATOXYLIN_STAIN][RED_COLOR]
        HematoxylinRGBStainVector_Green             = RgbStainVectors[HEMATOXYLIN_STAIN][GREEN_COLOR]
        HematoxylinRGBStainVector_Blue              = RgbStainVectors[HEMATOXYLIN_STAIN][BLUE_COLOR]
        print('Hematoxylin Density Stats')
        HematoxylinDensityMeans                     = np.mean(NonZeroHematoxylinDensities)
        HematoxylinDensitySDs                       = np.std(NonZeroHematoxylinDensities)
        HematoxylinDensityMedians                   = np.median(NonZeroHematoxylinDensities)
        # --------------------------------------------------------------------------
        print('Extracting Eosin Density')
        AllEosinDensities                           = StainPixelDensity_W[:, EOSIN_STAIN]
        print('Remove all pixels that don not actually contain hematoxylin')
        NonZeroEosinDensities                       = AllEosinDensities[np.nonzero(AllEosinDensities)]   
        # ------------------------------------
        EosinPixelDensity                           = np.array(NonZeroEosinDensities.tolist())
        EosinAreaInPixels                           = len(NonZeroEosinDensities)
        print('Hematoxylin Calculate Optical Density Stain Vectors')
        EosinStainOpticalDensity_Red                = StainVectors_S[EOSIN_STAIN][RED_COLOR]
        EosinStainOpticalDensity_Green              = StainVectors_S[EOSIN_STAIN][GREEN_COLOR]
        EosinStainOpticalDensity_Blue               = StainVectors_S[EOSIN_STAIN][BLUE_COLOR]
        print('Hematoxylin Calculate RGB Stain Vectors')
        EosinRGBStainVector_Red                     = RgbStainVectors[EOSIN_STAIN][RED_COLOR]
        EosinRGBStainVector_Green                   = RgbStainVectors[EOSIN_STAIN][GREEN_COLOR]
        EosinRGBStainVector_Blue                    = RgbStainVectors[EOSIN_STAIN][BLUE_COLOR]
        print('Eosin Density Stats')
        EosinDensityMeans                           = np.mean(NonZeroEosinDensities)
        EosinDensitySDs                             = np.std(NonZeroEosinDensities)
        EosinDensityMedians                         = np.median(NonZeroEosinDensities)
        # -----------------------------------------------------------------        
        self.SlideImageName                         = SlideImageName
        self.LabelMapImageName                      = LabelMapImageName
        self.FeatureName                            = Feature
        # ------------------------------------
        self.HematoxylinAreaInPixels                = HematoxylinAreaInPixels
        self.HematoxylinStainOpticalDensity_Red     = HematoxylinStainOpticalDensity_Red
        self.HematoxylinStainOpticalDensity_Green   = HematoxylinStainOpticalDensity_Green
        self.HematoxylinStainOpticalDensity_Blue    = HematoxylinStainOpticalDensity_Blue
        # ------------------------------------
        self.HematoxylinRGBStainVector_Red          = HematoxylinRGBStainVector_Red
        self.HematoxylinRGBStainVector_Green        = HematoxylinRGBStainVector_Green
        self.HematoxylinRGBStainVector_Blue         = HematoxylinRGBStainVector_Blue
        # ------------------------------------
        self.HematoxylinDensityMeans                = HematoxylinDensityMeans
        self.HematoxylinDensitySDs                  = HematoxylinDensitySDs
        self.HematoxylinDensityMedians              = HematoxylinDensityMedians        
        self.HematoxylinPixelDensity                = HematoxylinPixelDensity
        # ------------------------------------
        self.Hematoxylin_Image_Count                = Hematoxylin_Image_Count
        self.Hematoxylin_Image_Mean                 = Hematoxylin_Image_Mean
        self.Hematoxylin_Image_Standard_Deviation   = Hematoxylin_Image_Standard_Deviation
        self.Hematoxylin_Image_Min                  = Hematoxylin_Image_Min
        self.Hematoxylin_Image_25_Percent           = Hematoxylin_Image_25_Percent
        self.Hematoxylin_Image_50_Percent           = Hematoxylin_Image_50_Percent
        self.Hematoxylin_Image_75_Percent           = Hematoxylin_Image_75_Percent
        self.Hematoxylin_Image_Max                  = Hematoxylin_Image_Max
        # ------------------------------------
        self.EosinAreaInPixels                      = EosinAreaInPixels
        self.EosinStainOpticalDensity_Red           = EosinStainOpticalDensity_Red
        self.EosinStainOpticalDensity_Green         = EosinStainOpticalDensity_Green
        self.EosinStainOpticalDensity_Blue          = EosinStainOpticalDensity_Blue
        # ------------------------------------
        self.EosinRGBStainVector_Red                = EosinRGBStainVector_Red
        self.EosinRGBStainVector_Green              = EosinRGBStainVector_Green
        self.EosinRGBStainVector_Blue               = EosinRGBStainVector_Blue
        # ------------------------------------
        self.EosinDensityMeans                      = EosinDensityMeans
        self.EosinDensitySDs                        = EosinDensitySDs
        self.EosinDensityMedians                    = EosinDensityMedians
        self.EosinPixelDensity                      = EosinPixelDensity
        # ------------------------------------        
        self.Eosin_Image_Count                      = Eosin_Image_Count
        self.Eosin_Image_Mean                       = Eosin_Image_Mean
        self.Eosin_Image_Standard_Deviation         = Eosin_Image_Standard_Deviation
        self.Eosin_Image_Min                        = Eosin_Image_Min
        self.Eosin_Image_25_Percent                 = Eosin_Image_25_Percent
        self.Eosin_Image_50_Percent                 = Eosin_Image_50_Percent
        self.Eosin_Image_75_Percent                 = Eosin_Image_75_Percent
        self.Eosin_Image_Max                        = Eosin_Image_Max
        # ------------------------------------
        print('Calculations completed')    

# ------------------------------------------------------------------------------------------------
# Function Name: Get Arguments
# Author: Jose L. Agraz, PhD., 
# Date: 03/12/2020
# Description: Define input arguments using flags
# Input: Slides, Label Map Color file, and output file
# Output: Argument list
# ------------------------------------------------------------------------------------------------
def GetArguments():
    DESCRITPTION_MESSAGE = \
    'This scripts calculates the stain vectors and histogram for a given image.                       \n' + \
    'The calculation is based on Vahadane algorithm and loosely on work by manuscript titled:         \n' + \
    'Towards Population-based Histologic Stain Normalization of Glioblastoma. The script              \n' + \
    'calculates the parameters below per image and feature. Then, stores the results                  \n' + \
    'in a dataframe. The dataframe is saved in pickle format at given path for later                  \n' + \
    'analysis.                                                                                        ' 
        
    parser = argparse.ArgumentParser(description=DESCRITPTION_MESSAGE)
    # ------------------------------------
    parser.add_argument('-s', '--Slide_Image',                required=True,  help='Slide Image')
    parser.add_argument('-l', '--Label_Map_Image',            required=True,  help='Label Map Image')
    parser.add_argument('-g', '--Gray_Level_To_Label_Legend', required=True,  help='CSV file containing gray level legend')    
    parser.add_argument('-o', '--Output_Dataframe_File',      required=True,  help='Output File where to place Dataframe results')
    parser.add_argument('-x', '--Excluding_Labels',           required=True,  help='Feature Names to exclude. format Example: "Label 1, Label 2,...Label N"')    
    parser.add_argument('-t', '--Stain_Vector_Training',      required=False, default=600,  help='Stain Vector Training time in seconds')
    parser.add_argument('-v', '--Stain_Vector_Lambda',        required=False, default=0.1, help='Stain Vector Lambda')
    parser.add_argument('-d', '--Density_Map_Lambda',         required=False, default=0.01,  help='Density Map Lambda')
    # ------------------------------------
    args = parser.parse_args()

    return args

# ------------------------------------------------------------------------------------------------
# Function Name: Parse Invalid Labels
# Author: Jose L. Agraz, PhD., 
# Date: 03/12/2020
# Description: 
# Input: Excluding Feature List
# Output: gray level label 
# ------------------------------------------------------------------------------------------------
def ExcludeFeatureLabels(ExcludingFeatureList):
    EXCLUDING_LABELS_NAMES_REGEX  = '((?:\w+\s?){0,6}),?'
    GRAY_LEVEL_VALID_LABELS_TUPLE = ('Leading Edge',
                                     'Infiltrating Tumor',
                                     'Cellular Tumor',
                                     'Necrosis',
                                     'Perinecrotic Zone',
                                     'Pseudopolisading Cells around Necrosis',
                                     'Pseudopolisading Cells but no visible Necrosis',
                                     'Hyperplastic Blood',
                                     'Microvascular Proliferation'
                                     )
    FeatureName                  = str()
    FeatureIndex                 = int()
    GroupList                    = list()
    NewGrayLevelLabelList        = list(GRAY_LEVEL_VALID_LABELS_TUPLE)
    # ------------------------------------
    print('Check for empty input')
    if ExcludingFeatureList:
        print('Find all features to exclude')
        GroupList = re.findall(EXCLUDING_LABELS_NAMES_REGEX,ExcludingFeatureList)
        print('Scan list of excluding features')
        for FeatureName in GroupList:
            print('Delete feature')
            if FeatureName in GRAY_LEVEL_VALID_LABELS_TUPLE:
                FeatureIndex = NewGrayLevelLabelList.index(FeatureName)
                print('Excluding feature: {}'.format(FeatureName))
                NewGrayLevelLabelList.pop(FeatureIndex)            
    else:        
        print('No features to exclude')
        NewGrayLevelLabelList = GRAY_LEVEL_VALID_LABELS_TUPLE      
    
    print('Surviving features:\n\t{}'.format(NewGrayLevelLabelList))
    
    return NewGrayLevelLabelList
# ------------------------------------------------------------------------------------------------
# Function Name: Creates a directory
# Author: Jose L. Agraz, PhD., 
# Date: 04/12/2020
# Description: Created a directory
# Input: path
# Output: output path
# ------------------------------------------------------------------------------------------------
def CreateDirectory(OutputPath):
    try:
        print('Creating directory:\n{}'.format(OutputPath))
        Path(OutputPath).mkdir(parents=True, exist_ok=True)
    except:
        print('Could not created directory:\n{}'.format(OutputPath))
        raise IOError()
    return str(OutputPath)
# ------------------------------------------------------------------------------------------------
# Function Name: Import Gray Level Legend Data
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Reads Label Map legend CSV data as a DataFrame and trims unused data
# Input: Data path
# Output: Dataframe
# ------------------------------------------------------------------------------------------------
def ImportGrayLevelLegendData(SpreadsheetPath,GreyLevelLabels):
    # Initialize variables
    FEATURE_LABEL_COLUMN_TITLE    = 'FeatureLabel'
    GrayLevelLegendData           = pd.DataFrame()
    TrimmedGrayLevelLegendData    = pd.DataFrame()
    IndexedNewGrayLevelLegendData = pd.DataFrame()
    # ------------------------------------
    try:
        print('\tLoading Gray Level Legend File: ../{}'.format(Path(SpreadsheetPath).name))
        GrayLevelLegendData = pd.read_csv(SpreadsheetPath)
    except:
        print('No graylevel file data retrieved')
        raise IOError()
    # ------------------------------------
    print('Delete unwanted rows')
    TrimmedGrayLevelLegendData    = GrayLevelLegendData[GrayLevelLegendData.FeatureLabel.isin(GreyLevelLabels)]
    # ------------------------------------
    print('Index data frame by Label')
    IndexedNewGrayLevelLegendData = TrimmedGrayLevelLegendData.set_index(FEATURE_LABEL_COLUMN_TITLE)
    # ------------------------------------
    
    return IndexedNewGrayLevelLegendData

# ------------------------------------------------------------------------------------------------
# Function Name: Initialize
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Sets up input, directories, and images for process
# Input: None
# Output: Image and map data
# ------------------------------------------------------------------------------------------------
def Initialize():
    global GrayLevelLabelMapDataFrame
    global InputImagesDictionary
    global InputArguments

    print('----------------------------------------------------')
    print('Initialization Begins')
    # ------------------------------------
    print('Fetch input arguments')
    InputArguments                     = GetArguments()
    print('Exclude invalid features')
    GreyLevelLabels                    = ExcludeFeatureLabels(InputArguments.Excluding_Labels)   
    # ------------------------------------
    print('Create output directories')
    CreateDirectory(str(Path(InputArguments.Output_Dataframe_File).parent/ IMAGES_DATAFRAMES))  
    CreateDirectory(str(Path(InputArguments.Output_Dataframe_File).parent/ HISTOGRAMS_DATAFRAMES))  
    # ------------------------------------
    print('Fetch Slides and Level Map Images')
    InputImagesDictionary              = {InputArguments.Slide_Image: InputArguments.Label_Map_Image}
    print('Import Gray Level Legend CSV file')
    GrayLevelLabelMapDataFrame         = ImportGrayLevelLegendData(InputArguments.Gray_Level_To_Label_Legend,GreyLevelLabels)
    # ------------------------------------
    print('Get image pairs')
    SlideImageArray,\
    LabelMapImageArray      = LoadImagePairs(InputArguments.Slide_Image, InputArguments.Label_Map_Image)
    
    print('Initialization Ends')
    print('----------------------------------------------------')

    return SlideImageArray,LabelMapImageArray

# ------------------------------------------------------------------------------------------------
# Function Name: Find and Label Unique Pixels
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Match unique pixels to label map
# Input: Label map and image
# Output: Matching Features to gray level pixel map
# ------------------------------------------------------------------------------------------------
def FindAndLabelUniquePixels(MapDataFrame, ImageLabelMap):  # Pixel by pixel find unique pixels
    global InputArguments
    GRAY_LEVEL_COLUMN_TITLE = 'GrayLevel'
    FIRST_ITEM              = 0
    FeaturesFoundInImage    = pd.DataFrame()
    # ------------------------------------
    print('Scanning for unique pixel colors in Label Map Legend')
    UniqueColors = np.unique(ImageLabelMap) 
    # ------------------------------------
    for UniqueColor in UniqueColors:
        print('Search for pixel color matches in Label Map Legend file') # Rather than using a single line, code below is more readable
        # FoundPixelInLabelMap = MapDataFrame[MapDataFrame[GRAY_LEVEL_COLUMN_TITLE]==UniqueColor]
        SeriesOfInterest        = MapDataFrame[GRAY_LEVEL_COLUMN_TITLE]
        BooleanSeriesOfInterest = SeriesOfInterest.isin([UniqueColor])
        FoundPixelInLabelMap    = MapDataFrame[BooleanSeriesOfInterest]
        # ------------------------------------
        print('If a match is found, collect results')
        if BooleanSeriesOfInterest.any():
            print('Found Grey Level pixel \"{}\" for feature: {}'.format(UniqueColor,FoundPixelInLabelMap.index[FIRST_ITEM]))
            FeaturesFoundInImage = FeaturesFoundInImage.append(FoundPixelInLabelMap)
         
    return FeaturesFoundInImage  # Annotations with matching pixels

# ------------------------------------------------------------------------------------------------
# Function Name: Load Image Pairs
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Loads image pairs
# Input: path and image pair names
# Output: Images
# ------------------------------------------------------------------------------------------------
def LoadImagePairs(SlideName, LabelMapName):
    GRAY_SCALE_MODE                     = 0
    
    print('Processing Image Pairs: ')
    print('\tSlide: \t\t{}  '.format(Path(SlideName).name))
    print('\tLabel Map: \t{}'.format(Path(LabelMapName).name))

    TestFileForExistance(SlideName)
    TestFileForExistance(LabelMapName)
    # ------------------------------------
    ImageOfInterestBGR = cv2.imread(SlideName,cv2.IMREAD_COLOR)
    print('OpenCV retrieves images in a BGRcolor sequence')
    ImageOfInterestRGB = cv2.cvtColor(ImageOfInterestBGR, cv2.COLOR_BGR2RGB)
    LabelMapImage      = cv2.imread(LabelMapName, GRAY_SCALE_MODE)

    return ImageOfInterestRGB, LabelMapImage


# ------------------------------------------------------------------------------------------------
# Function Name: Test File For Existance
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Verify there are no problems with file
# Input: File name
# Output: None
# ------------------------------------------------------------------------------------------------
def TestFileForExistance(FileName):
    try:

        FileNamePath = pathlib.Path(FileName)
        if not FileNamePath.exists():
            print('I/O error')
            print('File Name: {}'.format(Path(FileName).name))
            print('Path Name: {}'.format(Path(FileName).parent))
            raise IOError()
    except:
        print('Unexpected I/O error')
        raise IOError()

# ------------------------------------------------------------------------------------------------
# Function Name: DataFrame to a Lists
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Convert a dataframe to a list
# Input: Label Dataframe
# Output: Gray level, Feature, and RGB lists
# ------------------------------------------------------------------------------------------------
def SplitLabelDataFrameToLists(DataFrame):
    RGB_COLOR       = -1
    GRAY_COLOR      = 0
    FeaturesList    = list()
    GrayLevelList   = list()
    RgbColorList    = list()

    GrayLevelDictionary = DataFrame.T.to_dict('list')
    for Features, GrayLevelValues in GrayLevelDictionary.items():
        GrayLevelList.append(GrayLevelValues[GRAY_COLOR])
        RgbColorList.append(GrayLevelValues[RGB_COLOR])
        FeaturesList.append(Features)

    return FeaturesList, GrayLevelList, RgbColorList

# ------------------------------------------------------------------------------------------------
# Function Name: Build Mask for Target feature
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Build Mask for Target feature
# Input: Image data, Gray Level values
# Output: Pixel Mask
# ------------------------------------------------------------------------------------------------
def BuildMaskForTargetFeature(Image, GrayLevel):
    WHITE_COLOR = 255
    BLACK_COLOR = 0
    PixelMask   = np.where(Image == GrayLevel, WHITE_COLOR, BLACK_COLOR)    
    print('Pixel Mask Size               : {}'.format(PixelMask.shape))
    print('Pixel Mask based on Gray Level: {}'.format(GrayLevel))
    return PixelMask

# ------------------------------------------------------------------------------------------------
# Function Name: Fetch Data Frame
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Building list for dataframe export
# Input: Composite statistics data
# Output: List of Composite statistics data
# ------------------------------------------------------------------------------------------------
def ClassDataToList(CompositeData):
    print('Initialize variables')
    # ------------------------------------------------------------------------
    HematoxylinComponentList = list()
    EosinComponentList       = list()
    # ------------------------------------------------------------------------
    print('Assign Hematoxylin data')
    HematoxylinComponentList = [CompositeData.SlideImageName,                       \
                                CompositeData.LabelMapImageName,                    \
                                CompositeData.FeatureName,                          \
                                HEMATOXYLIN_STAIN_LABEL,                            \
                                CompositeData.HematoxylinAreaInPixels,              \
                                CompositeData.HematoxylinPixelDensity,              \
                                CompositeData.HematoxylinStainOpticalDensity_Red,   \
                                CompositeData.HematoxylinStainOpticalDensity_Green, \
                                CompositeData.HematoxylinStainOpticalDensity_Blue,  \
                                CompositeData.HematoxylinRGBStainVector_Red,        \
                                CompositeData.HematoxylinRGBStainVector_Green,      \
                                CompositeData.HematoxylinRGBStainVector_Blue,       \
                                CompositeData.HematoxylinDensityMeans,              \
                                CompositeData.HematoxylinDensitySDs,                \
                                CompositeData.HematoxylinDensityMedians,            \
                                CompositeData.Hematoxylin_Image_Count,              \
                                CompositeData.Hematoxylin_Image_Mean,               \
                                CompositeData.Hematoxylin_Image_Standard_deviation, \
                                CompositeData.Hematoxylin_Image_Min,                \
                                CompositeData.Hematoxylin_Image_25_Percent,         \
                                CompositeData.Hematoxylin_Image_50_Percent,         \
                                CompositeData.Hematoxylin_Image_75_Percent,         \
                                CompositeData.Hematoxylin_Image_Max                 \
                                ]
    # ------------------------------------------------------------------------
    print('Assign Eosin data')
    EosinComponentList =       [CompositeData.SlideImageName,                       \
                                CompositeData.LabelMapImageName,                    \
                                CompositeData.FeatureName,                          \
                                EOSIN_STAIN_LABEL,                                  \
                                CompositeData.EosinAreaInPixels,                    \
                                CompositeData.EosinPixelDensity,                    \
                                CompositeData.EosinStainOpticalDensity_Red,         \
                                CompositeData.EosinStainOpticalDensity_Green,       \
                                CompositeData.EosinStainOpticalDensity_Blue,        \
                                CompositeData.EosinRGBStainVector_Red,              \
                                CompositeData.EosinRGBStainVector_Green,            \
                                CompositeData.EosinRGBStainVector_Blue,             \
                                CompositeData.EosinDensityMeans,                    \
                                CompositeData.EosinDensitySDs,                      \
                                CompositeData.EosinDensityMedians,                  \
                                CompositeData.Eosin_Image_Count,                    \
                                CompositeData.Eosin_Image_Mean,                     \
                                CompositeData.Eosin_Image_Standard_deviation,       \
                                CompositeData.Eosin_Image_Min,                      \
                                CompositeData.Eosin_Image_25_Percent,               \
                                CompositeData.Eosin_Image_50_Percent,               \
                                CompositeData.Eosin_Image_75_Percent,               \
                                CompositeData.Eosin_Image_Max                       \
                               ]
    print('Merge Hematoxylin & Eosin data')
    return [HematoxylinComponentList] + [EosinComponentList] 

# ----------------------------------------------------------------------------------
# Function Name: Get Image Composite Statistics
# Author: Jose L. Agraz, PhD
# Date: 04/14/2020
# Description:
# Input: none
# Output: none
# ----------------------------------------------------------------------------------
def ExecuteDeconvolution(SlideImage,LabelMapImage):
    global InputArguments
    global GrayLevelLabelMapDataFrame
    NO_PIXELS                       = 0
    MainList                        = list()
    FeatureList                     = list()
    GrayLevelList                   = list()
    RGBList                         = list()
    Feature                         = str()
    GrayLevel                       = int()
    PixelsFeaturesInImageDataFrame  = pd.DataFrame()
    Statistics                      = CompositeStatistics()

    print('Extract image file names')
    SlideImageName                  = str(Path(InputArguments.Slide_Image).name)
    LabelMapImageName               = str(Path(InputArguments.Label_Map_Image).name)
    
    print('List of colors present in the label map. Find all pixels with features')
    PixelsFeaturesInImageDataFrame = FindAndLabelUniquePixels(GrayLevelLabelMapDataFrame, LabelMapImage)

    print('Check for existing feature areas')
    if not PixelsFeaturesInImageDataFrame.empty:
        # --------------------------------------------
        print('Fetch Gray Level Legend parameters')
        FeatureList, GrayLevelList, RGBList = SplitLabelDataFrameToLists(PixelsFeaturesInImageDataFrame)
        print('Scan through gray levels')
        for Feature, GrayLevel in zip(FeatureList, GrayLevelList):
            print('----------------------------------------')
            print('Feature: \"{}\", Gray level color: \"{}\"'.format(Feature, GrayLevel))
            print('----------------------------------------')
            Statistics = ApplyingFilters(SlideImage, SlideImageName, Statistics, LabelMapImage, LabelMapImageName,GrayLevel,Feature)
            print('If the feature has an area, keep feature statistics')
            HematoxylinPixelsFound      =  Statistics.HematoxylinAreaInPixels 
            EosinPixelsFound            =  Statistics.EosinAreaInPixels
            # --------------------------------------------
            if HematoxylinPixelsFound > NO_PIXELS or EosinPixelsFound > NO_PIXELS:
                print('Add feature statistics to output list')
                MainList               += ClassDataToList(Statistics)  
                print('Update feature counter')
            else:
                print('Discarded Feature: \"{}\", Gray level color: \"{}\"'.format(Feature, GrayLevel))
    else:
        print('Empty dataframe, no unique colors found')
        
    del Statistics
    return MainList

# ----------------------------------------------------------------------------------
# Function Name: Applying Filters
# Author: Jose L. Agraz, PhD., 
# Date: 04/14/2020
# Description: Wraps up program
# Input: none
# Output: none
# ------------------------------------------------------------------------------------------------
def ApplyingFilters(SlideImage, SlideImageName, Statistics, LabelMapImage, LabelMapImageName, GrayLevel,Feature):       
    
    NO_PIXELS       = 0
    WHITE_COLOR     = 255
    PixelMask       = BuildMaskForTargetFeature(LabelMapImage, GrayLevel)
    print('Mask For Target Feature: {}'.format(PixelMask.shape))
    SurvivingPixels = np.count_nonzero(PixelMask)
    print('Surviving Pixels: {}'.format(SurvivingPixels))    
    print('Areas kept to analyze')
    if SurvivingPixels > NO_PIXELS:
        print('-----------------------------------------------')      
        print('Processing Feature: {}'.format(Feature))
        WhiteMask   = PixelMask.astype(bool) 
        print('Applying 3D White Mask to Image: {}'.format(SlideImageName))
        NewImage    = np.where(WhiteMask[...,None], SlideImage, WHITE_COLOR)
        Statistics.ImageComposite(SlideImageName,LabelMapImageName,Feature,NewImage)                                          
    else:
        print('-----------------------------------------------')        
        print('No areas left to process after filters')
        print('Skipping feature: {}'.format(Feature))   
        print('Output empty statistics class')
        Statistics  = CompositeStatistics()  
    
    return Statistics

# ----------------------------------------------------------------------------------
# Function Name: Terminate Process
# Author: Jose L. Agraz, PhD
# Date: 04/14/2020
# Description: Wraps up program
# Input: none
# Output: none
# ------------------------------------------------------------------------------------------------
def Terminate(ComponentList):   
    global InputArguments
    BIN_SIZE                   = 32768
    MAXIMUM_COLOR_BIN          = 10
    MINIMUM_COLOR_BIN          = 0
    PERCENT_MINIMUM_PIXEL_AREA = 0.5 
    DATAFRAME_COLUMN_NAMES     = {     'SlideImageName'             :0,\
                                       'ImageLabelMapName'          :1,\
                                       'FeatureName'                :2,\
                                       'Stain'                      :3,\
                                       'Area'                       :4,\
                                       'PixelDensity'               :5,\
                                       'OpticalDensity_Red_S'       :6,\
                                       'OpticalDensity_Green_S'     :7,\
                                       'OpticalDensity_Blue_S'      :8,\
                                       'RGBStainVector_Red_W'       :9,\
                                       'RGBStainVector_Green_W'     :10,\
                                       'RGBStainVector_Blue_W'      :11,\
                                       'DensityMeans'               :12,\
                                       'StandardDev'                :13,\
                                       'MedianDensity'              :14,\
                                       'Image_Count'                :15,\
                                       'Image_Mean'                 :16,\
                                       'Image_Standard_Deviation'   :17,\
                                       'Image_Min'                  :18,\
                                       'Image_25_Percent'           :19,\
                                       'Image_50_Percent'           :20,\
                                       'Image_75_Percent'           :21,\
                                       'Image_Max'                  :22\
                                      }    

    print('Initialize variables')
    BinsArray              = np.arange(MINIMUM_COLOR_BIN, MAXIMUM_COLOR_BIN, MAXIMUM_COLOR_BIN/BIN_SIZE)
    DataframeIndex         = np.arange(BIN_SIZE-1).tolist()
    DataBase               = pd.DataFrame([], columns=[*DATAFRAME_COLUMN_NAMES])   
    DaskBinsArray          = da.from_array(BinsArray)  
    HematoxylinHistogram   = da.from_array([0]*len(DataframeIndex))    
    EosinHistogram         = da.from_array([0]*len(DataframeIndex))        
    DataFramePath          = str()     
    HematoxylinList        = list()   
    EosinList              = list()    
    
    print('Check for missing feature information')
    if len(ComponentList):
        
        print('Fill Image Dataframe')                
        DataBase           = pd.DataFrame(ComponentList, columns=[*DATAFRAME_COLUMN_NAMES])          
        # --------------------------------------------           
        Stain_Name = HEMATOXYLIN_STAIN_LABEL
        print('Process {} Stain'.format(Stain_Name))
        Hematoxylin_Total_Pixel_Area   = DataBase[DataBase.Stain == Stain_Name].Area.sum()
        Hematoxylin_Area_Threshold     = int(PERCENT_MINIMUM_PIXEL_AREA * Hematoxylin_Total_Pixel_Area / 100)
        print('Image Pixel Area Threshold: {}% or {} pixels, for {} pixels total'.format(PERCENT_MINIMUM_PIXEL_AREA,Hematoxylin_Area_Threshold,Hematoxylin_Total_Pixel_Area))
        Filtered_Dataframe = DataBase[(DataBase.Area > Hematoxylin_Area_Threshold) & (DataBase.Stain == Stain_Name)]
        # --------------------------------------------                    
        print('Check for feature with succifient area: {} of {} pixels'.format(Hematoxylin_Area_Threshold,Hematoxylin_Total_Pixel_Area))
        Number_Of_Survaving_Features = len(Filtered_Dataframe.index)
        if Number_Of_Survaving_Features:
            # --------------------------------------------                    
            print('Number of Survaving Features: {}'.format(Number_Of_Survaving_Features))
            for Index_Row, Feature_Row in Filtered_Dataframe.iterrows():      
                print('Exploring Feature: {}'.format(Feature_Row.FeatureName))
                # --------------------------------------------                    
                if Feature_Row.Stain == Stain_Name:
                    HematoxylinList +=  Feature_Row.PixelDensity.tolist()
                    print('Delete Pixel Density from DataFrame')         
                    DataBase.loc[Index_Row,'PixelDensity']= np.array([0])                      
        # --------------------------------------------     
        Stain_Name = EOSIN_STAIN_LABEL
        print('Process {} Stain'.format(Stain_Name))
        Eosin_Total_Pixel_Area   = DataBase[DataBase.Stain == Stain_Name].Area.sum()
        Eosin_Area_Threshold     = int(PERCENT_MINIMUM_PIXEL_AREA * Eosin_Total_Pixel_Area / 100)
        print('Image Pixel Area Threshold: {}% or {} pixels, for {} pixels total'.format(PERCENT_MINIMUM_PIXEL_AREA,Eosin_Area_Threshold,Eosin_Total_Pixel_Area))
        Filtered_Dataframe = DataBase[(DataBase.Area > Eosin_Area_Threshold) & (DataBase.Stain == Stain_Name)]
        # --------------------------------------------                    
        print('Check for feature with succifient area: {} of {} pixels'.format(Eosin_Area_Threshold,Eosin_Total_Pixel_Area))
        Number_Of_Survaving_Features = len(Filtered_Dataframe.index)
        if Number_Of_Survaving_Features:
            
            print('Number of Survaving Features: {}'.format(Number_Of_Survaving_Features))
            for Index_Row, Feature_Row in Filtered_Dataframe.iterrows():      
                print('Exploring Feature: {}'.format(Feature_Row.FeatureName))

                if Feature_Row.Stain == Stain_Name:
                    EosinList +=  Feature_Row.PixelDensity.tolist()
                    print('Delete Pixel Density from DataFrame')                
                    DataBase.loc[Index_Row,'PixelDensity']= np.array([0])   
              
        # --------------------------------------------                    
        if len(HematoxylinList):
            Hematoxylin_Statistics = pd.Series(HematoxylinList).describe()
            # --------------------------------------------
            print('Calculating {} Histogram'.format(HEMATOXYLIN_STAIN_LABEL))       
            HematoxylinHistogram,_ = da.histogram(da.from_array(HematoxylinList),DaskBinsArray)       
            
        if len(EosinList):   
            Eosin_Statistics       = pd.Series(EosinList).describe()
            # --------------------------------------------
            print('Calculating {} Histogram'.format(EOSIN_STAIN_LABEL))        
            EosinHistogram,_       = da.histogram(da.from_array(EosinList)      ,DaskBinsArray)
        
        print('Build Stain Dictionary')
        # --------------------------------------------                        
        StainDictionary      = {'idx'                          :DataframeIndex,\
                                HEMATOXYLIN_STAIN_LABEL.lower():HematoxylinHistogram,\
                                EOSIN_STAIN_LABEL.lower()      :EosinHistogram}
        # --------------------------------------------              
        StainHistograms      = pd.DataFrame(StainDictionary)
        print('Create Index in dataframe')
        StainHistograms      = StainHistograms.set_index('idx')
        print('Type Cast Dataframe to int16')
        StainHistograms.astype(np.uint16).dtypes                
        DataFramePath        = str(Path(InputArguments.Output_Dataframe_File).parent / HISTOGRAMS_DATAFRAMES / Path(InputArguments.Output_Dataframe_File).name) + '.' + OUTPUT_FILE_EXTENSION        
        print('Create Stain Density Dask Dataframe')
        print('Save dataframe to disk')          
        StainHistograms.to_parquet(DataFramePath,engine='pyarrow')  
        # --------------------------------------------        
        
        if len(HematoxylinList):            
            Stain_Name       = HEMATOXYLIN_STAIN_LABEL
            Area_Threshold   = Hematoxylin_Area_Threshold
            Stain_Statistics = Hematoxylin_Statistics            
            print('Insert Image Wide Statistics for {}'.format(Stain_Name))
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Count'             ] = Stain_Statistics['count']
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Mean'              ] = Stain_Statistics['mean' ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Standard_Deviation'] = Stain_Statistics['std'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Min'               ] = Stain_Statistics['min'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_25_Percent'        ] = Stain_Statistics['25%'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_50_Percent'        ] = Stain_Statistics['50%'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_75_Percent'        ] = Stain_Statistics['75%'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Max'               ] = Stain_Statistics['max'  ]
        # --------------------------------------------        
        if len(EosinList):  
            Stain_Name       = EOSIN_STAIN_LABEL
            Area_Threshold   = Eosin_Area_Threshold
            Stain_Statistics = Eosin_Statistics            
            print('Insert Image Wide Statistics for {}'.format(Stain_Name))
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Count'             ] = Stain_Statistics['count']
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Mean'              ] = Stain_Statistics['mean' ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Standard_Deviation'] = Stain_Statistics['std'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Min'               ] = Stain_Statistics['min'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_25_Percent'        ] = Stain_Statistics['25%'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_50_Percent'        ] = Stain_Statistics['50%'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_75_Percent'        ] = Stain_Statistics['75%'  ]
            DataBase.loc[(DataBase.Stain == Stain_Name) & (DataBase.Area > Area_Threshold),'Image_Max'               ] = Stain_Statistics['max'  ]
        # --------------------------------------------       
        print('Save dataframe to disk')      
        DataFramePath             = str(Path(InputArguments.Output_Dataframe_File).parent / IMAGES_DATAFRAMES / Path(InputArguments.Output_Dataframe_File).name) + '.' + OUTPUT_FILE_EXTENSION          
        print('Concatenate both stains dataframes')
        Filtered_Dataframe = pd.concat([DataBase[(DataBase.Stain == HEMATOXYLIN_STAIN_LABEL) & (DataBase.Area > Hematoxylin_Area_Threshold)],\
                                        DataBase[(DataBase.Stain == EOSIN_STAIN_LABEL)       & (DataBase.Area > Eosin_Area_Threshold)]])        
        Filtered_Dataframe.to_parquet(DataFramePath,engine='pyarrow')
    else:
        print('Empty Dataframe')
      
# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # ---------------------------------------
    ComponentList = list()
    # ---------------------------------------
    StartTimer = datetime.now()
    TimeStamp = 'Start Time (hh:mm:ss.ms) {}'.format(StartTimer)
    print(TimeStamp)  
    # ---------------------------------------
    try:
        # ---------------------------------------   
        print('Begin housekeeping')
        SlideImageArray,\
        LabelMapImageArray  = Initialize()   
        print('Image Deconvolution')
        ComponentList       = ExecuteDeconvolution(SlideImageArray,LabelMapImageArray)
        Terminate(ComponentList)
        # ---------------------------------------
    except:
        raise IOError('Exception triggered!!!')
    # ---------------------------------------
    TimeElapsed = datetime.now() - StartTimer
    TimeStamp   = 'Time elapsed (hh:mm:ss.ms) {}\n'.format(TimeElapsed)
    print(TimeStamp)   