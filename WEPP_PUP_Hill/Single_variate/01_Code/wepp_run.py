import subprocess
import os



def run_wepp(wepp_path, working_folder, run_file_name):
    print("Running WEPP...")
    
    run_file = os.path.join(working_folder, run_file_name)
    
    if not os.path.exists(run_file):
        raise FileNotFoundError(f"{run_file} not found!")


    with open(run_file, 'r') as run_input:
        process = subprocess.run(
            [wepp_path],
            cwd=working_folder,
            stdin=run_input,
            #stdout=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

    if process.returncode == 0:
        print("✅ WEPP ran successfully.")
        
    else:
        print("❌ WEPP failed.")
        print("Error message:")
        print(process.stderr)
        return none
    
    return True
