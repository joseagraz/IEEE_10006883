#!/usr/bin/env bash
####
################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N Example
#$ -l h_vmem=128G
#$ -pe threaded 1
#$ -o ../SgeDump/Example_$JOB_ID.stdout
#$ -e ../SgeDump/Example_$JOB_ID.stderr
############################## END OF DEFAULT EMBEDDED SGE COMMANDS ########################
echo "Enviroment Loading"   
Enviroment_Loading_Attempts=3  # CBICA Cluster may need more than one attempt to load enviroment
for Enviroment_Loop in {1..$Enviroment_Loading_Attempts..1}                                                       
do                                                                                       
       echo "Interation="$Enviroment_Loop                                                   
       source activate Color_Normalization_Enviroment                                                 
       if [ $? == 0 ]; then                                                                 
           echo "Enviroment Active"   
           # ------------------------------------------------------------------------------------------------                                                      
           # Generate pandas dataframes containing stain vectors and optical density for image 266290664.jpg
           # Must do for every iamge in cohort. This is only a single image example
           python ../Python_Scripts/Produce_Image_Stain_Vectors_and_Optical_Density.py\
             --Slide_Image                Images_and_Maps/Images/266290664.jpg\
             --Label_Map_Image            Images_and_Maps/Image_Maps/W19-1-1-D.01_23_LM_266290664.png\
             --Gray_Level_To_Label_Legend Csv_Files/LV_Gray_Level_to_Label.csv\
             --Output_Dataframe_File      Images_DataFrames\
             --Excluding_Labels           ""
           # ------------------------------------------------------------------------------------------------
           # Aggregate stain vectors and histograms
           # Pre-computed stain vectors and histograms for 3 other images to speed up the process 
           python ../Python_Scripts/Aggregate_Stain_Vectors_and_Histograms.py\
             --Histogram_Dataframe_Directory    Images_Dataframes/Images_Histograms_DataFrames\
             --Stain_Vector_Dataframe_Directory Images_Dataframes/Images_Stain_Vectors_DataFrames\
             --Output_Directory                 Normalization_Parameters\
             --Number_of_Images                 4
           # ------------------------------------------------------------------------------------------------
           # Normalize image 266290664.jpg using aggregated parameters above
           # Must do for every iamge in cohort. This is only a single image example
           python ../Python_Scripts/Normalize_Image.py\
             --Image_To_Normalize         Images_and_Maps/Images/266290664.jpg\
             --Normalizing_Histogram      Normalization_Parameters/4_Image_Cohort_Aggregated_Normalization_Parameters/4ImageCohortHistograms.npy\
             --Normalizing_Stain_Vectors  Normalization_Parameters/4_Image_Cohort_Aggregated_Normalization_Parameters/4ImageCohortStainVectors.npy\
             --Output_Directory           Images_and_Maps/Normalized_Images
           # ------------------------------------------------------------------------------------------------
           break                                                                            
       fi                                                                                   
done                                                                                     
