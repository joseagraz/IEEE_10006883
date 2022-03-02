#!/usr/bin/env bash
####
################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N Example
#$ -l h_vmem=256G
#$ -pe threaded 1
#$ -o SgeDump/Example_$JOB_ID.stdout
#$ -e SgeDump/Example_$JOB_ID.stderr
############################## END OF DEFAULT EMBEDDED SGE COMMANDS ########################
#
# Example using a cohort of four images
#   1) Calculate stain vectors and histogram for each image and store info in a dataframe
#   2) Aggregate stain vectors and histogram from four images in step 1
#   3) Normalize each image using aggregated stain vectors and histogram in step 2
#
############################### END OF DEFAULT EMBEDDED SGE COMMANDS #######################
Image_Array=(          "266290664.jpg"                    "268005945.jpg"                   "292324603.jpg"                     "292324711.jpg")
Image_Map_Array=(      "W19-1-1-D.01_23_LM_266290664.png" "W18-1-1-A.01_2_LM_268005945.png" "W1-1-2-A.1.02_32_LM_292324603.png" "W1-1-2-A.1.02_14_LM_292324711.png")
Excluding_Labels=(     ""                                 ""                                "Infiltrating Tumor"                "Infiltrating Tumor")
Output_Dataframe_Name=("Dataframe_266290664"              "Dataframe_268005945"             "Dataframe_292324603"               "Dataframe_292324711")
# ------------------------------------------------------------------------------------------------
for Enviroment_Loop in {1..10..1}; do # CBICA Cluster may need more than one attempt to load enviroment
       echo "Interation_Number=${Enviroment_Loop}"
       echo "Loading conda python enviroment"
       source activate ColorNormalization  
       # ------------------------------------------------------------------------------------------------                                                
       if [ $? == 0 ]; then                                                                 
           echo "Enviroment Active"   
           for i in ${!Image_Array[@]}; do           
               # ------------------------------------------------------------------------------------------------
               echo Generate pandas dataframes containing stain vectors and optical density for each cohort image 
               python ../Python_Scripts/Produce_Image_Stain_Vectors_and_Optical_Density.py\
                 --Slide_Image                Images_and_Maps/Images/${Image_Array[$i]}\
                 --Label_Map_Image            Images_and_Maps/Image_Maps/${Image_Map_Array[$i]}\
                 --Gray_Level_To_Label_Legend Csv_Files/LV_Gray_Level_to_Label.csv\
                 --Output_Dataframe_File      ${Output_Dataframe_Name[$i]}\
                 --Excluding_Labels           "${Excluding_Labels[$i]}"
           done
           # ------------------------------------------------------------------------------------------------
           echo Aggregate stain vectors and histograms
           python ../Python_Scripts/Aggregate_Stain_Vectors_and_Histograms.py\
             --Histogram_Dataframe_Directory    Images_Histograms_DataFrames\
             --Stain_Vector_Dataframe_Directory Images_Stain_Stats_DataFrames\
             --Output_Directory                 Normalization_Parameters\
             --Number_of_Images                 ${#Image_Array[@]}
           #
           for i in ${!Image_Array[@]}; do
               # ------------------------------------------------------------------------------------------------
               echo Normalize image using aggregated parameters above
               python ../Python_Scripts/Normalize_Image.py\
                 --Image_To_Normalize         Images_and_Maps/Images/${Image_Array[$i]}\
                 --Normalizing_Histogram      Normalization_Parameters/${#Image_Array[@]}_Image_Cohort_Aggregated_Normalization_Parameters/${#Image_Array[@]}ImageCohortHistograms.npy\
                 --Normalizing_Stain_Vectors  Normalization_Parameters/${#Image_Array[@]}_Image_Cohort_Aggregated_Normalization_Parameters/${#Image_Array[@]}ImageCohortStainVectors.npy\
                 --Output_Directory           Images_and_Maps/Normalized_Images
               # ------------------------------------------------------------------------------------------------
           done
           break                                                                            
       fi                                                                                   
done
