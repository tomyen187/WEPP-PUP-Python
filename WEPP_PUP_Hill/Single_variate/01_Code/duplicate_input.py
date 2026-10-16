import os
import shutil

def prepare_working_inputs(input_folder, working_folder):	# Copy all original input files to working folder before running DDS
        
    if os.path.exists(working_folder):
        shutil.rmtree(working_folder)  # Clear if already exists
    shutil.copytree(input_folder, working_folder)

