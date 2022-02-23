## Robust Image Population-based Stain Normalization: How Many Reference Images Are Enough to Normalize?

## Contents

- [Image Population Based Histological Normalization](#submission-or-project-name)
  - [Description](#short-description)
    - [What's the problem?](#whats-the-problem)
    - [How can technology help?](#how-can-technology-help)
  - [Installation](#Installation)
  - [Getting started](#getting-started)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Description

### What's the problem?

Variation in materials, equipment, and staining protocols, make tissue slide staining rife with color aberrations. Although, pathologists train to compensate for slide color variations, the color disparity introduces inaccuracies in automated computational analysis, hindering algorithmic generalizability and accentuating data domain shift, hence highlighting the need for stain color normalization. Histopathology, more specifically whole slide image (WSI) digital pathology, lacks the color reference standards of other medical imaging domains. Digital pathology state-of-the-art WSI stain normalization methods employ a single WSI as the reference standard for cohort stain color normalization. Moreover, selecting a WSI representative of a WSI cohort is challenging, progressively for large cohort staining variations and image sizes, inadvertently introducing a color normalization bias.

### How can technology help?

The aggregation of a whole slide image (WSI) cohort subset is representative of an entire WSI cohort as a result of the law of large numbers theorem and shown as a power law distribution. This tool calculates the stain vectors and histogram for a given WSI cohort subset and normalizes a given WSI using Vahadane's structure-preserving color normalization algorithm

## Installation

1. Execute installation [Conda packages](./Installation_Bash_Files/Conda_Packages_Install.sh) bash file

2. Execute installation [Python packages](./Installation_Bash_Files/Python_Packages_Install.sh) bash file 

   Note: See a full list of CBICA's python conda environment [packages and respective versions](./Installation_Bash_Files/CBICA_Cluster_Package_Versions.txt) 


## Project roadmap

The project provides the following features:

- Calculates the stain vectors and histogram for a given image
- Aggregates the stain vectors and histogram for a given set of images
- Normalizes a given image using the aggregated stain vectors and histogram using [Vahadane's](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7460968) algorithm

![Normalization Work Flow](./images/Flow_GitHub.svg)

Figure 1. Image normalization work flow. 1) Compute all cohort images stain vectors and optical densities. 2) Aggregate stain vectors and histograms for a give number of random images. 3) Use aggregated stain vectors and histogram to normalize all images in cohort. 

## Getting started

See provided [normalization example](./Normalization_Example) for a cohort of four images

### Work-flow python scripts

1. Compute stain vectors and pixel optical density for each of the images in the given WSI cohort using this [dataframes generator](./Python_Scripts/Produce_Image_Stain_Vectors_and_Optical_Density.py) python script. Note, calculated stain vectors and optical density will be stored in dataframes. See switch description below.

   | Switch                            | Description                                                  |
   | --------------------------------- | ------------------------------------------------------------ |
   | --Slide_Image [-s]                | Image of interest (jpg)                                      |
   | --Label_Map_Image [-l]            | Image map of image of interest (png)                         |
   | --Gray_Level_To_Label_Legend [-g] | Gray level color legend (csv file)                           |
   | --Output_Dataframe_File [-o]      | Output Stain Vectors and Histogram pandas dataframe file name |
   | --Excluding_Labels [-x]           | Small or dubious labels in the label map image to ignore (text) |

   #### Usage

   ```
   >>> Produce_Image_Stain_Vectors_and_Optical_Density.py
         --Slide_Image                    266290664.jpg
         --Label_Map_Image            W19-1-1-D.01_23_LM_266290664.png
         --Gray_Level_To_Label_Legend LV_Gray_Level_to_Label.csv
         --Output_Dataframe_File      Dataframe_266290664
         --Excluding_Labels           ""
   ```

   

2. Compute normalizing stain vectors and histogram aggregates using python [Aggregate_Stain_Vectors_and_Histograms](/Python_Scripts/Aggregate_Stain_Vectors_and_Histograms.py) script. See switch description below.

   | Switch                                  | Description                                                  |
   | --------------------------------------- | ------------------------------------------------------------ |
   | --Histogram_Dataframe_Directory [-m]    | Sum and normalized to 10,000 count histogram  (parquet files) directory |
   | --Stain_Vector_Dataframe_Directory [-s] | Percent Area Stain Vector (parquet files) directory          |
   | --Output_Directory [-o]                 | Aggregated histogram and stain vectors  (parquet files) directory |
   | --Number_of_Images [-i]                 | Number of random images                                      |

   #### Usage

   ```
   >>> Aggregate_Stain_Vectors_and_Histograms.py
        --Histogram_Dataframe_Directory     Histogram_Dataframes
        --Stain_Vector_Dataframe_Directory  Stain_Vectors_Dataframes
        --Output_Directory                  Normalization_Parameters_Directory
        --Number_of_Images                  1864
   ```

   ​       

3. Normalize image using normalizing stain vectors and histogram aggregates utilizing python [Normalize_Image](/Python_Scripts/Normalize_Image.py) script. See switch description below.

   | Switch                           | Description                        |
   | -------------------------------- | ---------------------------------- |
   | --Image_To_Normalize [-i]        | Image of interest (jpg)            |
   | --Normalizing_Histogram [-n]     | Normalizing Histogram (numpy)      |
   | --Normalizing_Stain_Vectors [-s] | Normalizing Stain Vector (numpy)   |
   | --Output_Directory [-o]          | Normalized Image of interest (png) |
   
   #### Usage
   
   ```
   >>> Normalize_Image.py
         --Image_To_Normalize        266290664.jpg
         --Normalizing_Histogram     100ImageCohortHistograms.npy
         --Normalizing_Stain_Vectors 100ImageCohortStainVectors.npy
         --Output_Directory          Normalized_Images_Directory
   ```
   
   

## Authors

![Authors](./images/authors.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to Robert S. Pozos PhD, for his invaluable feedback
