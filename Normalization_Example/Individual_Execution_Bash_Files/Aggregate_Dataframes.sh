#!/usr/bin/env bash
####
################################## START OF EMBEDDED SGE COMMANDS ##########################
#$ -S /bin/bash
#$ -cwd
#$ -N Aggregate
#$ -l h_vmem=256G
#$ -pe threaded 1
#$ -o SgeDump/Aggregate_$JOB_ID.stdout
#$ -e SgeDump/Aggregate_$JOB_ID.stderr
############################## END OF DEFAULT EMBEDDED SGE COMMANDS ########################
for Enviroment_Loop in {1..10..1}; do # CBICA Cluster may need more than one attempt to load enviroment
       echo "Interation_Number=${Enviroment_Loop}"
       echo "Loading conda python enviroment"
       source activate Color_Normalization_Environment  
       if [ $? == 0 ]; then                                                                 
           echo "Enviroment Active"   
           # ------------------------------------------------------------------------------------------------                                                      
           echo Aggregate stain vectors and histograms
           python ../Python_Scripts/Aggregate_Stain_Vectors_and_Histograms.py\
             --Histogram_Dataframe_Directory    Images_Histograms_DataFrames\
             --Stain_Vector_Dataframe_Directory Images_Stain_Stats_DataFrames\
             --Output_Directory                 Normalization_Parameters\
             --Number_of_Images                 4
           # ------------------------------------------------------------------------------------------------
           break
       fi
done


