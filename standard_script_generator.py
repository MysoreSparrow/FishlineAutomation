import os

USER = "elaurell"
#GAL4= input("Enter line name of the fish: ")
# base_fish_num = input("Enter base fish number you have chosen: ")
#tag = input("Enter the tag name for the fish line:")

L6 = ["#SBATCH -o /u/elaurell/scripts/live/output/tjob_hybrid_out.%j \n",
      "#SBATCH -e /u/elaurell/scripts/live/output/tjob_hybrid_err.%j \n"]
L7 = ["#SBATCH -D /u/elaurell/ \n", "# Job name: \n", "#SBATCH -J avg_templ\n", "# Number of nodes and MPI tasks per node: \n",
      "#SBATCH --nodes=1 \n", "#SBATCH --ntasks-per-node=1 \n", "# for OpenMP: \n", "#SBATCH --cpus-per-task=72\n",
      "# \n"]
L8 = ["#SBATCH --mem=100000 \n", "#SBATCH --mail-type=none \n", "#SBATCH --mail-user=elaurell@rzg.mpg.de \n",
      "# Wall clock limit: \n", "#SBATCH --time=18:00:00 \n", "export OMP_NUM_THREADS=72 \n",
      "# For pinning threads correctly: \n", "export OMP_PLACES=cores \n", " \n"]
L9 = ["antsbin=/u/${USER}/ANTs/antsInstallExample/install/bin/ \n"]

output = ["output1=/ptmp/${USER}/avg_templ/live/Registration/${GAL4}/T_${GAL4}_ \n",
          "output2=/ptmp/${USER}/avg_templ/live/reformatted/"f"${GAL4}/T_${GAL4}_AVG_{tag}.nrrd \n",
          "output3=/ptmp/${USER}/avg_templ/live/reformatted/"f"${GAL4}/T_${GAL4}_AVG_GFP.nrrd \n"]

input = ["input1=/ptmp/${USER}/avg_templ/live/averages/"f"${GAL4}_AVG_{tag}.nrrd \n",
         "input2=/ptmp/${USER}/avg_templ/live/averages/"f"${GAL4}_AVG_GFP.nrrd \n"]


L10 = ["srun $antsbin/antsRegistration -d 3 \ \n", "--float 1 \ \n",
      "-o [${output1},${output2}] \ \n", "--interpolation WelchWindowedSinc \ \n", "--use-histogram-matching 0 \ \n",
      "-r [${template1},${input1},1] \ \n", "-t rigid[0.1] \ \n", "-m MI[${template1},${input1},1,32,Regular,0.25] \ \n",
      "-c [200x200x200x0,1e-8,10] \ \n", "--shrink-factors 12x8x4x2 \n", "--smoothing-sigmas 4x3x2x1vox \ \n",
      "-t Affine[0.1] \ \n", "-m MI[${template1},${input1},1,32,Regular,0.25] \ \n", "-c [200x200x200x0,1e-8,10] \ \n",
      "--shrink-factors 12x8x4x2  \ \n", "--smoothing-sigmas 4x3x2x1 \ \n", "-t SyN[0.05,6,0.5] \ \n",
      "-m CC[${template},${input1},1,2] \n", "-c [200x200x200x200x10,1e-7,10] \ \n",
      "--shrink-factors 12x8x4x2x1 \ \n", "--smoothing-sigmas 4x3x2x1x0 \n"]


L11 = ["$antsbin/antsApplyTransforms -d 3 \ \n", "-v 0 \ \n", "-- float \ \n", "-n WelchWindowedSinc \ \n",
       "-i ${input2} \ \n", "-r ${template} \ \n", "-o ${output3} \ \n", "-t ${output1}1Warp.nii.gz \ \n",
       "-t ${output1}0GenericAffine.mat \n", " \n", "rm -rf ${input1} ${input2} \n"]

# \n is placed to indicate EOL (End of Line)
# if __name__ == '__main__':
def create_standard_script(slurmpath, tag, GAL4)
    file3 = open(rf"{slurmpath}/ANTs_standard_{GAL4}.sh", "w")
    file3.write("#!/bin/bash -l \n")
    file3.write("# Standard output and error: \n")
    file3.writelines(L6)
    file3.write("# Initial working directory: \n")
    file3.writelines(L7)
    file3.write("# Request 100 GB of main Memory per node in Units of MB: \n")
    file3.writelines(L8)
    file3.write(f"GAL4={GAL4} \n")
    file3.write("\n")
    file3.writelines(L9)
    file3.write("\n")
    file3.writelines(output)
    file3.write("\n")
    file3.writelines(input)
    file3.write("\n")
    file3.write(f"template1=/u/{USER}/templates/live_standard_{tag}.nrrd")
    file3.write("\n")
    file3.write("\n")
    file3.write("#Run the ANTs Program: \n")
    file3.writelines(L10)
    file3.write("\n")
    file3.writelines(L11)
    file3.close()  # to change file access modes
    return file3



if __name__ == '__main__':
    pass