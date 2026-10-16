import csv
import os

from soil_description import PARAMETER_LOCATIONS

def read_parameter_file(param_file):
    parameters = []
    lower_bounds = []
    upper_bounds = []
    
    with open(param_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')				#  tab delimiter
        next(reader)  # skips header if present;  #rows=list (reader)   #num_rows=len(rows)
        #num_cols=len(rows(col[0]))
        for row in reader:
            try: 
                if len(row) < 9:			#checks the col. num. in parameter file
                    raise ValueError ("insufficient col") 

            
                if int(row[3]) == 1:  # file name col (index 4) is '1' # calibration index
                    param = {
                    'Serial': row[0],
		    'Entity': row[1],
                    'variable': row[2],		#'variable': rows[2][col].strip(),
		    'Cal_index': int(row[3]),
                    'Unit': row[4],
                    'file_ext':row[5],		#'file_ext': rows[5][col].strip(),
                    'initial': float(row[6]),
                    'lower': float(row[7]),
                    'upper': float(row[8])
                    }
                    parameters.append(param) 
                    lower_bounds.append(param['lower'])                                                                                  
                    upper_bounds.append(param['upper'])
	        

            except ValueError as e:
                print(f"Error parsing row: {row}. Error: {e}")
                continue
    
    return parameters, lower_bounds, upper_bounds
  
 #==============================================================================


def read_initial_values(
    working_folder,
    parameters
):
    """
    Read actual starting values of all parameters
    with Cal_index == 1 directly from the freshly
    copied WEPP input file.

    For the present hillslope calibration these
    values are read from p0.sol.
    """

    initial_values = []

    for param in parameters:

        file_ext = param[
            'file_ext'
        ]

        variable = param[
            'variable'
        ]

        input_file_path = (
            os.path.join(
                working_folder,
                file_ext
            )
        )

        if not os.path.exists(
            input_file_path
        ):

            raise FileNotFoundError(
                f"Input file for initial "
                f"parameter '{variable}' "
                f"was not found: "
                f"{input_file_path}"
            )

        if (
            variable
            not in PARAMETER_LOCATIONS
        ):

            raise KeyError(
                f"Parameter '{variable}' "
                f"is not defined in "
                f"PARAMETER_LOCATIONS."
            )

        row_idx, col_idx = (
            PARAMETER_LOCATIONS[
                variable
            ]["position"]
        )

        with open(
            input_file_path,
            'r'
        ) as f:

            lines = f.readlines()

        target_line = (
            lines[row_idx]
            .split()
        )

        initial_value = float(
            target_line[col_idx]
        )

        initial_values.append(
            initial_value
        )

       # print(
       #     f"Initial value read "
        #    f"from {file_ext}: "
         #   f"{variable} = "
          #  f"{initial_value}"
        #)

    return initial_values


#===================================================================       

def update_parameter_file(working_folder,param, new_value):
    file_ext = param['file_ext']
    variable = param['variable']
    #initial_values = []

    input_file_path = os.path.join(working_folder, file_ext)

    if not os.path.exists(input_file_path):
        print(f" ❌ Input file {input_file_path} does not exist.")
        return input_file_path

    if variable not in PARAMETER_LOCATIONS:
        print(f" ❌{variable} not found in mapping")
        return input_file_path

    row_idx, col_idx = PARAMETER_LOCATIONS[variable]["position"]

    with open(input_file_path, 'r') as f:
        lines = f.readlines()
        #f.close()


    target_line = lines[row_idx].split()
    initial_value = float(target_line[col_idx])			

   # print(
    #    f"Initial value read "
     #   f"from {file_ext}: "
      #  f"{variable} = "
      #  f"{initial_value}"
    #)

    old_value = target_line[col_idx]
    target_line[col_idx] = str(new_value)
    lines[row_idx] = ' '.join(target_line) + '\n'

    with open(input_file_path, 'w') as f:
        f.writelines(lines)

   # print(f"✅ Updated '{variable}' in {file_ext} at row {row_idx}, col {col_idx}: {old_value} ➜ {new_value}")


    return new_value  			
    f.close()














