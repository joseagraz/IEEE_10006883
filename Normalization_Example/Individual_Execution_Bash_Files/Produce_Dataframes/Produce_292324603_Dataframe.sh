#!/usr/bin/env bash
####
################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N D_292324603
#$ -l h_vmem=256G
#$ -pe threaded 1
#$ -o SgeDump/Dataframe_292324603_$JOB_ID.stdout
#$ -e SgeDump/Dataframe_292324603_$JOB_ID.stderr
############################## END OF DEFAULT EMBEDDED SGE COMMANDS ########################
for Enviroment_Loop in {1..10..1}; do # CBICA Cluster may need more than one attempt to load enviroment
       echo "Interation_Number=${Enviroment_Loop}"
       echo "Loading conda python enviroment"
       source activate Color_Normalization_Environment  
       if [ $? == 0 ]; then                                                                 
           echo "Enviroment Active"   
           # ------------------------------------------------------------------------------------------------                                                      
           # Generate pandas dataframes containing stain vectors and optical density for each cohort image 
           python ../Python_Scripts/Produce_Image_Stain_Vectors_and_Optical_Density.py\
             --Slide_Image                Images_and_Maps/Images/292324603.jpg\
             --Label_Map_Image            Images_and_Maps/Image_Maps/W1-1-2-A.1.02_32_LM_292324603.png\
             --Gray_Level_To_Label_Legend Csv_Files/LV_Gray_Level_to_Label.csv\
             --Output_Dataframe_File      Dataframe_292324603\
             --Excluding_Labels           "Infiltrating Tumor"
           # ------------------------------------------------------------------------------------------------
           break
       fi
done


