import os

USER = "elaurell"
#folder = input("Enter line name of the fish: ")
#tag = input("Enter the Reference Channel name for the fish line:")

L1 = ["#SBATCH -o /u/elaurell/scripts/live/output/tjob_hybrid_out.%j \n",
      "#SBATCH -e /u/elaurell/scripts/live/output/tjob_hybrid_err.%j \n"]
L2 = ["#SBATCH -D /u/elaurell/ \n", "# Job name: \n", "#SBATCH -J avg_templ\n", "# Number of nodes and MPI tasks per node: \n",
      "#SBATCH --nodes=1 \n", "#SBATCH --ntasks-per-node=1 \n", "# for OpenMP: \n", "#SBATCH --cpus-per-task=72\n",
      "# \n"]
L3 = ["#SBATCH --mem=490000 \n", "#SBATCH --mail-type=none \n", "#SBATCH --mail-user=elaurell@rzg.mpg.de \n",
      "# Wall clock limit: \n", "#SBATCH --time=24:00:00 \n", "export OMP_NUM_THREADS=72 \n",
      "# For pinning threads correctly: \n", "export OMP_PLACES=cores \n", " \n"]
L4 = ["mkdir /ptmp/${USER}/avg_templ/live/results/${folder} \n",
      "inputPath=/ptmp/${USER}/avg_templ/live/images/low_res/${folder}_*.tif \n",
      "outputPath=/ptmp/${USER}/avg_templ/live/results/${folder} \n", " \n"]
ANTsPath = ["ANTSPATH=/u/${USER}/ANTs/antsInstallExample/install/bin \n", "export ANTSPATH \n"]
L5 = ["srun ${ANTSPATH}/antsMultivariateTemplateConstruction2.sh \ \n", "-d 3 \ \n", "-o ${outputPath}/T_ \ \n",
      "-i 4 \ \n", "-g 0.2 \ \n", "-j 32 \ \n", "-v 500 \ \n", "-c 2 \ \n", "-k 2 \ \n", "-w 1x1 \ \n", "-f 12x8x4x2 \n",
      "-s 4x3x2x1 \ \n", "-n 0 \ \n", "-r 1 \ \n", "-l 1 \ \n", "-z ${target1} \ \n", "-z ${target2} \ \n",
      "-m CC[2] \ \n", "-t SyN[0.05,6,0.5] \ \n", "${inputPath} \n", "\n"]


def create_averaging_script(slurmpath, base_fish_num, tag, folder):
      file1 = open(rf"{slurmpath}/ANTs_average_{folder}.sh", "w")
      file1.write("#!/bin/bash -l \n")
      file1.write("# Standard output and error: \n")
      file1.writelines(L1)
      file1.write("# Initial working directory: \n")
      file1.writelines(L2)
      file1.write("# Request 500 GB of main Memory per node in Units of MB: \n")
      file1.writelines(L3)
      file1.write(f"folder={folder} \n")
      file1.write("\n")
      file1.writelines(L4)
      file1.write(f"target1=/ptmp/{USER}/avg_templ/live/images/low_res/${folder}_{base_fish_num}_{tag}.tif \n")
      file1.write(f"target2=/ptmp/{USER}/avg_templ/live/images/low_res/${folder}_{base_fish_num}_GFP.tif \n")
      file1.write("\n")
      file1.writelines(ANTsPath)
      file1.write("\n")
      file1.write("#Run the ANTs Program: \n")
      file1.writelines(L5)
      file1.close()  # to change file access modes
      return file1


if __name__ == '__main__':
      pass
# file1 = open(r"C:\Users\elaurell\Desktop\AutomatedScripts\*.sh", "r+")
#
# # print("Output of Read function is ")
# print(file1.read())

#       file1 = open(rf"C:\Users\elaurell\Desktop\AutomatedScripts\ANTs_average_{folder}.sh", "w")
#       file1.write("#!/bin/bash -l \n")
#       file1.write("# Standard output and error: \n")
#       file1.writelines(L1)
#       file1.write("# Initial working directory: \n")
#       file1.writelines(L2)
#       file1.write("# Request 500 GB of main Memory per node in Units of MB: \n")
#       file1.writelines(L3)
#       file1.write(f"folder={folder} \n")
#       file1.writelines(L4)
#       file1.write(f"target1=/ptmp/${USER}/avg_templ/live/images/low_res/${folder}_{base_fish_num}_lynTagRFP.tif \n")
#       file1.write(f"target2=/ptmp/${USER}/avg_templ/live/images/low_res/${folder}_{base_fish_num}_GFP.tif \n")
#       file1.writelines(ANTsPath)
#       file1.write("#Run the ANTs Program: \n")
#       file1.writelines(L5)
#       file1.close()  # to change file access modes
