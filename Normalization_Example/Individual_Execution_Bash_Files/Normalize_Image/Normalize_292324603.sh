#!/usr/bin/env bash
####
################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N N_292324603
#$ -l h_vmem=256G
#$ -pe threaded 1
#$ -o SgeDump/Normalize_292324603_$JOB_ID.stdout
#$ -e SgeDump/Normalize_292324603_$JOB_ID.stderr
############################## END OF DEFAULT EMBEDDED SGE COMMANDS ########################
for Enviroment_Loop in {1..10..1}; do # CBICA Cluster may need more than one attempt to load enviroment
       echo "Interation_Number=${Enviroment_Loop}"
       echo "Loading conda python enviroment"
       source activate Color_Normalization_Environment  
       if [ $? == 0 ]; then                                                                 
           echo "Enviroment Active"   
           # ------------------------------------------------------------------------------------------------                                                      
           # Normalize image
           python ../Python_Scripts/Normalize_Image.py\
             --Image_To_Normalize         Images_and_Maps/Images/292324603.jpg\
             --Normalizing_Histogram      Normalization_Parameters/4_Image_Cohort_Aggregated_Normalization_Parameters/4ImageCohortHistograms.npy\
             --Normalizing_Stain_Vectors  Normalization_Parameters/4_Image_Cohort_Aggregated_Normalization_Parameters/4ImageCohortStainVectors.npy\
             --Output_Directory           Images_and_Maps
           # ------------------------------------------------------------------------------------------------
           break
       fi
done


