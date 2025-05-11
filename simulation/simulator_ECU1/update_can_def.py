
import json, os
from argparse import ArgumentParser


def update_can_def_file(file_path):
    """
    Update the CAN definition file with new data.

    :param file_path: Path to the CAN definition file.
    :param new_data: New data to be added to the CAN definition file.
    """
    try:
        # Read the existing data from the file
        with open(file_path, 'r') as file:
            can_def = json.load(file)

        # Structure it to can_def.h
        signal_matrix = can_def.get("signals",[])


        # Identify pwd
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open (f"{dir_path}/can_def.h","w") as f:
            for index in range (0, len(signal_matrix)):
                if (signal_matrix[index]["ECU_name"]!="" and signal_matrix[index]["ECU_name"]!=""):
                    string_to_write = f"#define {signal_matrix[index]["ECU_name"]} {signal_matrix[index]["can_id"]} \n"
                    f.write (string_to_write)
        print(f"CAN definition file  updated successfully.")
    except Exception as e:
        print(f"Error updating CAN definition file: {e}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", required = True, type = str, help="Path to .json containing can def")
    args = parser.parse_args()
    if os.path.exists(args.path):
        update_can_def_file(args.path)
    else:
        print ("Path is invalid")


        
