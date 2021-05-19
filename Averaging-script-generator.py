import os
import re

root_dir = r'C:\Users\keshavgubbi\Desktop\AutomatedScripts'
output_scripts_dir = r'C:\Users\keshavgubbi\Desktop\AutomatedScripts\linescript'
avg_template_path = r"C:\Users\keshavgubbi\Desktop\AutomatedScripts\templatescripts\ANTs_average_template.sh"

linename = input('Enter line name:')
# basefish_number = input('Enter basefish_number:')
# tagName = input('Enter tag name:')
# t1 = target1=/ptmp/${USER}/avg_templ/live/images/low_res/${folder}_2_lynTagRFP.tif

# os.listdir(root_dir) gaves me all the fish folders names inside root_dir
for folder_name in os.listdir(root_dir):
    if not os.path.isfile(os.path.join(output_scripts_dir, f'ANTs_average_{linename}.sh')):
        # path of scripts files
        new_output_script_path = os.path.join(output_scripts_dir, f'ANTs_average_{linename}.sh')
        # create new script file
        averaging_script_file = open(new_output_script_path, "wt+")
        # open template file
        template_file = open(avg_template_path, 'rt')
        # copy the template file to the new script file
        for line in template_file:
            if line.strip() == "folder=linename":
                averaging_script_file.write("folder=" + linename.replace('\r', ''))
            # if line.strip() == "target1":
            #     print(line)
            #     if '_2_' in line.strip():
            #         text = re.sub('_2_', f'{basefish_number}', line.strip())
            #         averaging_script_file.write(text)
            else:
                averaging_script_file.write(line.replace('\r', ''))

        print(f"The averaging script for {linename} has been created!")

# with open(averaging_script_file, 'rw') as f:
#     text = f.read()
#     text = re.sub('human', 'cat', text)
#     f.seek(0)
#     f.write(text)
#     f.truncate()

# if line.strip() == "_2_":
#     text = re.sub('2', f'{basefish_number}', line.strip())
#     averaging_script_file.write(text)
# if line.strip() == "lynTagRFP":
#     text1 = re.sub('lynTagRFP', f'{tagName}', line.strip())
#     averaging_script_file.write(text1)