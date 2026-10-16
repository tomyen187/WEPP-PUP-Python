from datetime import datetime, timedelta


Obs_path = r"...\input_files\obs_runoff.txt"

runoff_cont = r"...\input_files\continuous_observed_runoff.txt"

def generate_continuous_runoff(input_file, output_file):
    runoff_cont = {}

    # Read observed file
    with open(input_file, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            try:
                year, month, day = map(int, parts[:3])
                runoff = float(parts[3])
                date = datetime(year, month, day)
                runoff_cont[date] = runoff
            except:
                continue

    # Determine start and end date
    all_dates = sorted(runoff_cont.keys())
    first_date = all_dates[0].year
    start_date=datetime(first_date, 1,1)
    end_date = all_dates[-1]

    # Write continuous data
    with open(output_file, 'w') as f_out:
        f_out.write("Year\tMonth\tDay\tRunoff\n")
        current_date = start_date
        while current_date <= end_date:
            runoff = runoff_cont.get(current_date, '-99')
            f_out.write(f"{current_date.year}\t{current_date.month}\t{current_date.day}\t{runoff}\n")
            current_date += timedelta(days=1)

# Usage
generate_continuous_runoff(Obs_path, runoff_cont)


print("✅ Continuous runoff file has been created successfully.")


#input("Press Enter to exit...")
