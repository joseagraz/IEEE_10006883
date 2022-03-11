#!/usr/bin/env bash
####
################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N D_266290664
#$ -l h_vmem=256G
#$ -pe threaded 1
#$ -o SgeDump/Dataframe_266290664_$JOB_ID.stdout
#$ -e SgeDump/Dataframe_266290664_$JOB_ID.stderr
############################## END OF DEFAULT EMBEDDED SGE COMMANDS ########################
for Enviroment_Loop in {1..10..1}; do # CBICA Cluster may need more than one attempt to load enviroment
       echo "Interation_Number=${Enviroment_Loop}"
       echo "Loading conda python enviroment"
       source activate Color_Normalization_Environment  
       if [ $? == 0 ]; then                                                                 
           echo "Enviroment Active"   
           # ------------------------------------------------------------------------------------------------                                                      
           # Generate pandas dataframes containing stain vectors and optical density for each cohort image 
           python Python_Scripts/Produce_Image_Stain_Vectors_and_Optical_Density.py\
             --Slide_Image                Normalization_Example/Images_and_Maps/Images/266290664.jpg\
             --Label_Map_Image            Normalization_Example/Images_and_Maps/Image_Maps/W19-1-1-D.01_23_LM_266290664.png\
             --Gray_Level_To_Label_Legend Normalization_Example/Csv_Files/LV_Gray_Level_to_Label.csv\
             --Output_Dataframe_File      Normalization_Example/Dataframe_266290664\
             --Excluding_Labels           ""
           # ------------------------------------------------------------------------------------------------
           break
       fi
done


