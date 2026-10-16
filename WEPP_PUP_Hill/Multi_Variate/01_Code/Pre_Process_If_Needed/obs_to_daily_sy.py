from datetime import datetime, timedelta


Obs_path = r"...Input_files\Obs_sediment.txt"

sed_cont = r"...\Input_files\continuous_observed_sediment.txt"

def generate_continuous_sedi(input_file, output_file):
    sed_cont = {}

    # Read observed file
    with open(input_file, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            try:
                year, month, day = map(int, parts[:3])
                sed = float(parts[3])
                date = datetime(year, month, day)
                sed_cont[date] = sed
            except:
                continue

    # Determine start and end date
    all_dates = sorted(sed_cont.keys())
    first_date = all_dates[0].year
    start_date=datetime(first_date, 1,1)
    end_date = all_dates[-1]

    # Write continuous data
    with open(output_file, 'w') as f_out:
        f_out.write("Year\tMonth\tDay\tSediemnt\n")
        current_date = start_date
        while current_date <= end_date:
            sed = sed_cont.get(current_date, '-99')
            f_out.write(f"{current_date.year}\t{current_date.month}\t{current_date.day}\t{sed}\n")
            current_date += timedelta(days=1)

# Usage
generate_continuous_sedi(Obs_path, sed_cont)


print("✅ Continuous sediment file has been created successfully.")


#input("Press Enter to exit...")