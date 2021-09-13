USER = "keshavgubbi"
date = input("Enter line name of the fish: ")
# base_fish_num = input("Enter base fish number you have chosen: ")
tag = input("Enter the tag name for the fish line:")

L6 = ["#SBATCH -o /u/keshavgubbi/scripts/live/output/tjob_hybrid_out.%j \n",
      "#SBATCH -e /u/keshavgubbi/scripts/live/output/tjob_hybrid_err.%j \n"]
L7 = ["#SBATCH -D /u/keshavgubbi/ \n", "# Job name: \n", "#SBATCH -J avg_templ\n", "# Number of nodes and MPI tasks per node: \n",
      "#SBATCH --nodes=1 \n", "#SBATCH --ntasks-per-node=1 \n", "# for OpenMP: \n", "#SBATCH --cpus-per-task=72\n",
      "# \n"]
L8 = ["#SBATCH --mem=128000 \n", "#SBATCH --mail-type=none \n", "#SBATCH --mail-user=keshavgubbi@rzg.mpg.de \n",
      "# Wall clock limit: \n", "#SBATCH --time=08:00:00 \n", "export OMP_NUM_THREADS=72 \n",
      "# For pinning threads correctly: \n", "export OMP_PLACES=cores \n", " \n"]
L9 = ["mkdir /ptmp/${USER}/avg_templ/live/reformatted/${date} \n", "mkdir /ptmp/${"
      "USER}/avg_templ/live/Registration/${date} \n", "antsbin=/u/${USER}/ANTs/antsInstallExample/install/bin/ \n"]

output = ["output1=/ptmp/${USER}/avg_templ/live/Registration/${date}/${date}_${SLURM_ARRAY_TASK_ID}_ \n",
          "output2=/ptmp/${USER}/avg_templ/live/reformatted/"f"${date}/${date}_""${SLURM_ARRAY_TASK_ID}"f"_{tag}.nrrd "
          f"\n",
          "output3=/ptmp/${USER}/avg_templ/live/reformatted/"f"${date}/${date}_""${SLURM_ARRAY_TASK_ID}"f"_GFP.nrrd \n"]

input = ["input1=/ptmp/${USER}/avg_templ/live/images/high_res/"f"${date}_""${SLURM_ARRAY_TASK_ID}"f"_{tag}.nrrd \n",
         "input2=/ptmp/${USER}/avg_templ/live/images/high_res/"f"${date}_""${SLURM_ARRAY_TASK_ID}"f"_GFP.nrrd \n"]


L10 = ["srun $antsbin/antsRegistration -d 3 \ \n", "--float 1 \ \n", "--verbose 1 \ \n",
      "-o [${output1},${output2}] \ \n", "--interpolation WelchWindowedSinc \ \n", "--use-histogram-matching 0 \ \n",
      "-r [${template1},${input1},1] \ \n", "-t rigid[0.1] \ \n", "-m MI[${template1},${input1},1,32,Regular,0.25] \ \n",
      "-c [200x200x200x0,1e-8,10] \ \n", "--shrink-factors 12x8x4x2 \n", "--smoothing-sigmas 4x3x2x1 \ \n",
      "-t Affine[0.1] \ \n", "-m MI[${template1},${input1},1,32,Regular,0.25] \ \n", "-c [200x200x200x0,1e-8,10] \ \n",
      "--shrink-factors 12x8x4x2  \ \n", "--smoothing-sigmas 4x3x2x1 \ \n", "-t SyN[0.1,6,0] \ \n",
      "-m CC[${template1},${input1},1,2] \n", "-c [200x200x200x200x10,1e-7,10] \ \n",
      "--shrink-factors 12x8x4x2x1 \ \n", "--smoothing-sigmas 4x3x2x1x0 \n"]


L11 = ["$antsbin/antsApplyTransforms -d 3 \ \n", "-v 0 \ \n", "-- float \ \n", "-n WelchWindowedSinc \ \n",
       "-i ${input2} \ \n", "-r ${template1} \ \n", "-o ${output3} \ \n", "-t ${output1}1Warp.nii.gz \ \n",
       "-t ${output1}0GenericAffine.mat \n", " \n", "rm -rf ${input1} ${input2} \n"]

# \n is placed to indicate EOL (End of Line)
# if __name__ == '__main__':
#
file2 = open(rf"C:\Users\keshavgubbi\Desktop\AutomatedScripts\ANTs_lines_{date}.sh", "w")
file2.write("#!/bin/bash -l \n")
file2.write("# Standard output and error: \n")
file2.writelines(L6)
file2.write("# Initial working directory: \n")
file2.writelines(L7)
file2.write("# Request 128 GB of main Memory per node in Units of MB: \n")
file2.writelines(L8)
file2.write(f"date={date} \n")
file2.write("\n")
file2.writelines(L9)
file2.write("\n")
file2.writelines(output)
file2.write("\n")
file2.writelines(input)
file2.write("\n")
file2.write(f"template1=/u/{USER}/templates/live_standard_{tag}.nrrd")
file2.write("\n")
# file2.write(f"target1=/ptmp/{USER}/avg_templ/live/images/low_res/${date}_{base_fish_num}_{tag}.tif \n")
# file2.write(f"target2=/ptmp/{USER}/avg_templ/live/images/low_res/${date}_{base_fish_num}_GFP.tif \n")
# file2.write("\n")aa
file2.write("\n")
file2.write("#Run the ANTs Program: \n")
file2.writelines(L10)
file2.write("\n")
file2.writelines(L11)
file2.close()  # to change file access modes


