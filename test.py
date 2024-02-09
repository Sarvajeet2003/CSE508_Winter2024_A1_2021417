import os

def merge_text_files(directory_path, output_file_path):
    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # Open the output file in write mode
    with open(output_file_path, 'w') as output_file:
        # Loop through each file in the directory
        for file_name in files:
            # Construct the full path of the file
            file_path = os.path.join(directory_path, file_name)

            # Open each file in read mode and append its contents to the output file
            with open(file_path, 'r') as input_file:
                output_file.write(input_file.read())
                
            # Add a newline between files to separate their contents
            output_file.write('\n')

    print(f'Merged files into {output_file_path}')

# Example usage:
input_directory = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/text_files'
output_file = '/Users/sarvajeethuk/Downloads/IR/Assignment-1/fileOLD.txt'

merge_text_files(input_directory, output_file)
